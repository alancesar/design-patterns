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

Each element in the structure exposes an `accept(visitor)` method, which simply calls back the visitor's method corresponding to its concrete type (for example, `visitor.visitCircle(this)`). This technique, called *double dispatch*, makes the code that runs depend on both the type of the visitor and the type of the element, without `instanceof` or a `switch` on types.

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

A graphics editor has stable shapes (`Circle` and `Rectangle`) and needs to compute the total area and export the drawing to JSON without adding those methods to the shape classes.

```typescript
interface ShapeVisitor<R> {
  visitCircle(c: Circle): R;
  visitRectangle(r: Rectangle): R;
}

interface Shape { accept<R>(v: ShapeVisitor<R>): R; }

class Circle implements Shape {
  constructor(public radius: number) {}
  accept<R>(v: ShapeVisitor<R>): R { return v.visitCircle(this); }
}

class Rectangle implements Shape {
  constructor(public width: number, public height: number) {}
  accept<R>(v: ShapeVisitor<R>): R { return v.visitRectangle(this); }
}

class AreaVisitor implements ShapeVisitor<number> {
  visitCircle(c: Circle) { return Math.PI * c.radius ** 2; }
  visitRectangle(r: Rectangle) { return r.width * r.height; }
}

class JsonExportVisitor implements ShapeVisitor<string> {
  visitCircle(c: Circle) { return JSON.stringify({ type: "circle", r: c.radius }); }
  visitRectangle(r: Rectangle) { return JSON.stringify({ type: "rect", w: r.width, h: r.height }); }
}

const shapes: Shape[] = [new Circle(1), new Rectangle(2, 3)];
const total = shapes.reduce((sum, s) => sum + s.accept(new AreaVisitor()), 0);
const json = shapes.map((s) => s.accept(new JsonExportVisitor()));
```

## Related patterns

- [Composite](/coding/gof/structural/composite) — Visitor is often applied to run operations over all the nodes of a Composite tree
- [Iterator](/coding/gof/behavioral/iterator) — can be used to traverse the object structure while the Visitor performs the operation on each element
- [Interpreter](/coding/gof/behavioral/interpreter) — operations on Interpreter's abstract syntax tree (evaluation, printing, optimization) are usually implemented as visitors
- [Command](/coding/gof/behavioral/command) — both encapsulate operations in objects; Visitor can be seen as a powerful Command that acts on several element types
- [Strategy](/coding/gof/behavioral/strategy) — also extracts behavior into separate objects, but varies one algorithm for a single context, with no double dispatch

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Visitor on Refactoring.Guru](https://refactoring.guru/design-patterns/visitor)
