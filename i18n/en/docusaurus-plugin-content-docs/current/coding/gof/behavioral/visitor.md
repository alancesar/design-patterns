---
title: Visitor
pattern_slug: visitor
category: Behavioral
tags:
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Visitor"
---

# Visitor

## Description

Visitor represents an operation to be performed on the elements of an object structure. It lets you define new operations without changing the classes of the elements they operate on, by moving each operation into a separate object, the visitor.

Each element in the structure exposes an `accept(visitor)` method, which simply calls back the visitor's method corresponding to its concrete type (for example, `visitor.visitCdb(this)`). This technique, called *double dispatch*, makes the code that runs depend on both the type of the visitor and the type of the element, without `instanceof` or a `switch` on types.

So each new operation becomes a new `ConcreteVisitor` class that gathers, in one place, the behavior for all element types. The pattern is especially useful in stable hierarchies, such as syntax trees (AST), documents, and domain models, on which many different operations are applied.

## Problems it solves

- The need to add new operations (export, validation, calculation, rendering) to a class hierarchy without modifying it for every new feature
- The logic of a single operation spread across several element classes, making it hard to understand and maintain
- `if/else` or `switch` chains with type checks (`instanceof`) to decide what to do with each element
- Domain classes polluted with responsibilities unrelated to their main purpose
- Accumulating state while traversing a heterogeneous structure (for example, summing totals or collecting metrics from a tree)

## When to use

- The object structure contains classes with different interfaces and you need to perform operations that depend on the concrete type of each one
- Many distinct, unrelated operations need to be applied to the structure and you don't want to pollute the classes with them
- The element hierarchy rarely changes, but new operations are added frequently
- Compilers, interpreters, and analysis tools that traverse syntax trees (type checking, optimization, code generation, pretty printing)

## When to avoid

- The element hierarchy changes frequently: each new type requires a new method in every visitor
- There are few operations and they naturally belong to the elements themselves
- The operation needs access to the elements' private internal state, which would force you to break encapsulation
- The language offers exhaustive pattern matching over sealed types (sealed classes, union types), which solves the same problem with less ceremony

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| New operations without changing the element classes (Open/Closed for operations) | Adding a new element type requires changing the `Visitor` interface and all concrete visitors |
| Related behavior concentrated in a single visitor (SRP) | May force elements to expose internal state through public methods |
| A visitor can accumulate state while traversing the structure | Double dispatch and callbacks make the flow less intuitive |
| Eliminates type checks and `switch` on classes | Cyclic coupling between `Visitor` and the element hierarchy |

- **Coupling:** visitors know all the concrete element types; elements only know the `Visitor` interface.
- **Testability:** each operation can be tested in isolation by applying the visitor to small, controlled structures.
- **Complexity:** the responsibility for traversing the structure (in the element, in the visitor, or in an Iterator) must be decided and kept consistent.
- **Extensibility:** the pattern flips the axis of extension: it makes new operations easy and new types hard (the so-called *expression problem*).

## Diagram

```mermaid
classDiagram
    class Client
    class ObjectStructure {
        -List~Element~ elements
        +accept(Visitor visitor)
    }
    class Visitor {
        <<interface>>
        +visitConcreteElementA(ConcreteElementA element)
        +visitConcreteElementB(ConcreteElementB element)
    }
    class ConcreteVisitor1 {
        +visitConcreteElementA(ConcreteElementA element)
        +visitConcreteElementB(ConcreteElementB element)
    }
    class ConcreteVisitor2 {
        +visitConcreteElementA(ConcreteElementA element)
        +visitConcreteElementB(ConcreteElementB element)
    }
    class Element {
        <<interface>>
        +accept(Visitor visitor)
    }
    class ConcreteElementA {
        +accept(Visitor visitor)
        +operationA()
    }
    class ConcreteElementB {
        +accept(Visitor visitor)
        +operationB()
    }
    Client --> ObjectStructure
    Client --> Visitor
    ObjectStructure o--> Element : contains
    Visitor <|.. ConcreteVisitor1
    Visitor <|.. ConcreteVisitor2
    Element <|.. ConcreteElementA
    Element <|.. ConcreteElementB
    Element ..> Visitor : accept
    Visitor ..> ConcreteElementA : visits
    Visitor ..> ConcreteElementB : visits
```

The `Client` applies a `ConcreteVisitor` to the `ObjectStructure`, which hands the visitor to each `Element`. Each `ConcreteElement` implements `accept` by calling the `visit` method corresponding to its type, so the operation that runs depends on the visitor/element pair (double dispatch).

## Example

The investment portfolio has stable asset types (`Cdb`, `Stock` and `FundShare`; the same portfolio that Composite organizes into sub-portfolios), and new operations show up often: computing the tax due, generating the income report. Each operation is a visitor, with no changes to the asset classes. The tax rates in the example are illustrative.

```typescript
interface AssetVisitor<R> {
  visitCdb(cdb: Cdb): R;
  visitStock(stock: Stock): R;
  visitFundShare(share: FundShare): R;
}

interface Asset { accept<R>(v: AssetVisitor<R>): R; }

class Cdb implements Asset {
  constructor(public issuer: string, public gainCents: number) {}
  accept<R>(v: AssetVisitor<R>): R { return v.visitCdb(this); }
}

class Stock implements Asset {
  constructor(public symbol: string, public gainCents: number) {}
  accept<R>(v: AssetVisitor<R>): R { return v.visitStock(this); }
}

class FundShare implements Asset {
  constructor(public fund: string, public gainCents: number) {}
  accept<R>(v: AssetVisitor<R>): R { return v.visitFundShare(this); }
}

// illustrative rates, not an actual tax rule
class TaxCalculator implements AssetVisitor<number> {
  visitCdb(cdb: Cdb) { return Math.round(cdb.gainCents * 0.15); }
  visitStock(stock: Stock) { return Math.round(stock.gainCents * 0.15); }
  visitFundShare(share: FundShare) { return Math.round(share.gainCents * 0.20); }
}

class IncomeReportExporter implements AssetVisitor<string> {
  visitCdb(cdb: Cdb) { return JSON.stringify({ type: "cdb", issuer: cdb.issuer, gainCents: cdb.gainCents }); }
  visitStock(stock: Stock) { return JSON.stringify({ type: "stock", symbol: stock.symbol, gainCents: stock.gainCents }); }
  visitFundShare(share: FundShare) { return JSON.stringify({ type: "fund", fund: share.fund, gainCents: share.gainCents }); }
}

const assets: Asset[] = [
  new Cdb("Banco Alfa", 100_000),
  new Stock("ACME3", 50_000),
  new FundShare("Fundo Beta", 200_000),
];
const totalTaxCents = assets.reduce((sum, a) => sum + a.accept(new TaxCalculator()), 0);
console.log(totalTaxCents); // 62500
const report = assets.map((a) => a.accept(new IncomeReportExporter()));
```

## Related patterns

- [Composite](/coding/gof/structural/composite) — Visitor is often applied to run operations over all the nodes of a Composite tree, such as the investment portfolio in the example
- [Iterator](/coding/gof/behavioral/iterator) — can be used to traverse the object structure while the Visitor performs the operation on each element
- [Interpreter](/coding/gof/behavioral/interpreter) — operations on Interpreter's abstract syntax tree (evaluation, printing, optimization) are usually implemented as visitors
- [Command](/coding/gof/behavioral/command) — both encapsulate operations in objects; Visitor can be seen as a powerful Command that acts on several element types
- [Strategy](/coding/gof/behavioral/strategy) — also extracts behavior into separate objects, but varies one algorithm for a single context, with no double dispatch

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Visitor on Refactoring.Guru](https://refactoring.guru/design-patterns/visitor)
