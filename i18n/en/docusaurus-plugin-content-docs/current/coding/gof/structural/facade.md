---
title: Facade
pattern_slug: facade
category: Structural
tags:
  - Simplicity
  - Decoupling
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Facade"
---

# Facade

## Description

The Facade provides a single, simplified interface to a set of interfaces in a subsystem. Instead of the client knowing about and coordinating several internal classes, it talks to a single facade object that exposes high-level operations.

The facade knows which subsystem classes are responsible for each request and delegates the work to them, in the correct order. The subsystem classes keep working independently and don't know about the facade; advanced clients can still access them directly when they need more control.

The result is a layer that reduces the coupling between clients and implementation details, making the subsystem easier to use, maintain, and evolve.

## Problems it solves

- Clients need to orchestrate many low-level classes (libraries, frameworks, legacy APIs) to perform a simple task.
- Internal changes in a subsystem propagate to all the code that uses it.
- Complex dependencies between layers make it hard to understand a module's entry point.
- Integration code repeated in several places to perform the same sequence of calls.

## When to use

- When you want to provide a simple interface to a complex subsystem.
- To structure a system into layers, defining an entry point for each one.
- To isolate client code from third-party libraries or legacy systems, making them easier to replace.
- When there are many dependencies between clients and implementation classes and you want to decouple them.

### When to avoid

- When the subsystem is already simple; the facade would only add an unnecessary layer.
- When clients need the full power and flexibility of the subsystem and the facade would end up replicating its entire API.
- When the facade tends to become a "god object", accumulating unrelated responsibilities.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Simple, easy-to-use interface | May hide useful functionality or limit advanced use cases |
| Less coupling between clients and the subsystem | One more layer of indirection to maintain |
| Internal changes are isolated behind the facade | Risk of the facade growing too large and becoming a "god object" |
| Clear entry point for layers and modules | May mask design problems in the subsystem instead of solving them |

- **Coupling:** the client depends only on the facade, but the facade is coupled to several subsystem classes.
- **Testability:** clients are easy to test with a facade double; the facade itself requires integration tests or mocks of the components.
- **Complexity:** low; the pattern requires neither inheritance nor special interfaces.
- **Performance:** negligible impact, just one extra delegation call.

## Diagram

```mermaid
classDiagram
    class Client
    class Facade {
        +operation()
    }
    class SubsystemA {
        +operationA()
    }
    class SubsystemB {
        +operationB()
    }
    class SubsystemC {
        +operationC()
    }
    Client --> Facade
    Facade --> SubsystemA
    Facade --> SubsystemB
    Facade --> SubsystemC
```

The `Client` interacts only with the `Facade`, which delegates calls to `SubsystemA`, `SubsystemB`, and `SubsystemC` in the proper order. The subsystem classes don't know about the facade.

## Example

An e-commerce site needs to complete orders by checking inventory, charging payment, and scheduling delivery. Instead of each controller coordinating these three services, an `OrderFacade` exposes a single `placeOrder` operation.

```typescript
class InventoryService {
  reserve(sku: string, qty: number): void { /* ... */ }
}

class PaymentService {
  charge(customerId: string, amount: number): string { return "tx-123"; }
}

class ShippingService {
  schedule(customerId: string, sku: string): string { return "track-456"; }
}

class OrderFacade {
  constructor(
    private inventory = new InventoryService(),
    private payment = new PaymentService(),
    private shipping = new ShippingService(),
  ) {}

  placeOrder(customerId: string, sku: string, qty: number, amount: number): string {
    this.inventory.reserve(sku, qty);
    this.payment.charge(customerId, amount);
    return this.shipping.schedule(customerId, sku);
  }
}

// Client
const tracking = new OrderFacade().placeOrder("c-1", "SKU-9", 2, 199.9);
```

## Related patterns

- [Adapter](/coding/gof/structural/adapter) — the Adapter converts an existing interface into another one that's expected; the Facade creates a new, simpler interface for a set of classes.
- [Mediator](/coding/gof/behavioral/mediator) — both centralize communication, but the Mediator coordinates colleagues that know about it, while the Facade is transparent to the subsystem.
- [Abstract Factory](/coding/gof/creational/abstract-factory) — can be used together with the Facade to create the subsystem's objects in a platform-independent way.
- [Singleton](/coding/gof/creational/singleton) — often a single instance of the facade is enough.
- [Proxy](/coding/gof/structural/proxy) — also sits between the client and the real object, but keeps the same interface instead of simplifying it.

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Facade on Refactoring.Guru](https://refactoring.guru/design-patterns/facade)
