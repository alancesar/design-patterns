---
title: Abstract Factory
pattern_slug: abstract-factory
category: Creational
tags:
  - Decoupling
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Abstract Factory"
---

# Abstract Factory

## Description

Abstract Factory provides an interface for creating families of related or dependent objects without specifying their concrete classes. The client talks only to the abstract factory and to the abstract product interfaces, without knowing which implementation is behind them.

Each concrete factory implements the abstract factory interface and produces a coherent variant of every product in the family (for example, all UI components in the "Windows" style or all in the "Mac" style). Swapping the concrete factory, usually at a single configuration point, swaps the entire family at once.

In practice, the pattern works as a "factory of factories": it groups several related Factory Methods into a single object and ensures consistency among the products it creates.

## Problems it solves

- Client code becomes coupled to concrete classes when it instantiates objects with `new`, making it hard to swap implementations.
- Products from different families get mixed by mistake (for example, a button from one theme with a dialog from another).
- Supporting a new platform, theme, or vendor requires changing many places scattered across the code.

## When to use

- The system must be independent of how its products are created, composed, and represented.
- The system must be configured with one of several families of products (UI themes, database drivers, cloud providers).
- Related products are designed to be used together and that constraint must be enforced.
- You want to expose a library of products revealing only the interfaces, not the implementations.

## When to avoid

- There's only one product family or a single product; a Factory Method or direct construction is enough.
- New product types are added frequently: each new product requires changing the abstract factory interface and every concrete factory.
- The flexibility gained doesn't justify the extra interfaces and classes.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Isolates the client from concrete classes | Increases the number of interfaces and classes |
| Ensures consistency among products of the same family | Adding a new product type requires changing every factory |
| Makes it easy to swap the entire family at a single point | Extra indirection can make the creation flow harder to read |
| Supports the Open/Closed Principle for new families | Can become over-engineering in simple domains |

- **Coupling:** the client depends only on abstractions, which reduces coupling to implementations.
- **Testability:** it's simple to inject a fake factory that produces mocks or stubs.
- **Complexity:** the parallel hierarchy of factories and products grows quickly with the number of variants.
- **Performance:** negligible impact; creation goes through one additional polymorphic call.

## Diagram

```mermaid
classDiagram
    class AbstractFactory {
        <<interface>>
        +createProductA() AbstractProductA
        +createProductB() AbstractProductB
    }
    class ConcreteFactory1 {
        +createProductA() AbstractProductA
        +createProductB() AbstractProductB
    }
    class ConcreteFactory2 {
        +createProductA() AbstractProductA
        +createProductB() AbstractProductB
    }
    class AbstractProductA {
        <<interface>>
    }
    class AbstractProductB {
        <<interface>>
    }
    class ProductA1
    class ProductA2
    class ProductB1
    class ProductB2
    class Client

    AbstractFactory <|.. ConcreteFactory1
    AbstractFactory <|.. ConcreteFactory2
    AbstractProductA <|.. ProductA1
    AbstractProductA <|.. ProductA2
    AbstractProductB <|.. ProductB1
    AbstractProductB <|.. ProductB2
    ConcreteFactory1 ..> ProductA1 : creates
    ConcreteFactory1 ..> ProductB1 : creates
    ConcreteFactory2 ..> ProductA2 : creates
    ConcreteFactory2 ..> ProductB2 : creates
    Client --> AbstractFactory
    Client --> AbstractProductA
    Client --> AbstractProductB
```

The `Client` uses only `AbstractFactory` and the product interfaces. Each concrete factory (`ConcreteFactory1`, `ConcreteFactory2`) creates a coherent family of products (`ProductA1`/`ProductB1` or `ProductA2`/`ProductB2`).

## Example

A desktop application needs to render buttons and checkboxes with the operating system's native look. The factory is chosen once at startup and the rest of the code doesn't know the concrete classes.

```typescript
interface Button { render(): string; }
interface Checkbox { render(): string; }

interface GUIFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
}

class WinButton implements Button { render() { return "[Win Button]"; } }
class WinCheckbox implements Checkbox { render() { return "[Win Checkbox]"; } }
class MacButton implements Button { render() { return "(Mac Button)"; } }
class MacCheckbox implements Checkbox { render() { return "(Mac Checkbox)"; } }

class WinFactory implements GUIFactory {
  createButton() { return new WinButton(); }
  createCheckbox() { return new WinCheckbox(); }
}

class MacFactory implements GUIFactory {
  createButton() { return new MacButton(); }
  createCheckbox() { return new MacCheckbox(); }
}

function renderForm(factory: GUIFactory): string {
  return [factory.createButton(), factory.createCheckbox()]
    .map((w) => w.render())
    .join(" ");
}

const factory: GUIFactory = process.platform === "darwin" ? new MacFactory() : new WinFactory();
console.log(renderForm(factory));
```

## Related patterns

- [Factory Method](/coding/gof/creational/factory-method) — concrete factories are often implemented with Factory Methods.
- [Prototype](/coding/gof/creational/prototype) — an alternative for implementing concrete factories by cloning prototypes instead of instantiating subclasses.
- [Singleton](/coding/gof/creational/singleton) — usually one instance of each concrete factory is enough in the application.
- [Builder](/coding/gof/creational/builder) — focuses on building a complex object step by step, whereas Abstract Factory creates families of objects immediately.
- [Facade](/coding/gof/structural/facade) — an Abstract Factory can be used as an alternative to Facade to hide the creation of a subsystem's specific objects.
- [Bridge](/coding/gof/structural/bridge) — an Abstract Factory can create and configure a specific implementation of a Bridge.

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Abstract Factory on Refactoring.Guru](https://refactoring.guru/design-patterns/abstract-factory)
