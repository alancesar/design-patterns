---
title: State
pattern_slug: state
category: Behavioral
tags:
  - Extensibility
  - Runtime Flexibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "State"
---

# State

## Description

State lets an object alter its behavior when its internal state changes, giving the impression that the object changed class. Instead of concentrating conditionals (`if`/`switch`) on a state variable in every method, each possible state is encapsulated in its own class that implements a common interface.

The main object, called the context (`Context`), keeps a reference to the current state and delegates state-dependent operations to it. Transitions happen by swapping that reference for another state instance, which can be done by the context itself or by the concrete states, which know which transitions are valid from them.

In practice, the pattern is an object-oriented way to implement a finite state machine: each state knows how to react to events and which state to move to next.

## Problems it solves

- Methods full of large conditionals that check the current state before deciding what to do
- Transition rules scattered across the code, making it hard to understand which state changes are allowed
- Difficulty adding new states without modifying many existing methods (an Open/Closed violation)
- Inconsistent behavior when an operation is called in a state where it shouldn't be allowed

## When to use

- An object's behavior depends heavily on its state and must change at runtime
- There are many states and well-defined transitions (orders, documents in a workflow, network connections, vending machines)
- The same conditionals on the state are repeated across several methods of the class
- New states tend to appear frequently and should be added in isolation

### When to avoid

- The object has few states or its behavior rarely changes; an `enum` with a simple `switch` is more readable
- Transitions are trivial and there's no state-specific behavior
- The flow is better described declaratively (transition table or a state machine library)

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Eliminates lengthy conditionals on the state | Increases the number of classes |
| Each state is isolated and cohesive (Single Responsibility) | The overall view of the flow is spread across several classes |
| New states are added without changing the existing ones | States that know their successors become coupled to each other |
| Transitions are explicit and controlled | Overkill for small state machines |

- **Coupling:** if the concrete states decide the transitions, they know each other; centralizing transitions in the context reduces that coupling, but concentrates logic.
- **Testability:** each state can be tested in isolation, verifying the action and the resulting state.
- **Performance:** states with no attributes of their own can be shared (as Singletons or Flyweights), avoiding creating objects on every transition.

## Diagram

```mermaid
classDiagram
    class Context {
        -state: State
        +setState(state: State)
        +request()
    }
    class State {
        <<interface>>
        +handle(context: Context)
    }
    class ConcreteStateA {
        +handle(context: Context)
    }
    class ConcreteStateB {
        +handle(context: Context)
    }
    Context o--> State : current state
    State <|.. ConcreteStateA
    State <|.. ConcreteStateB
    ConcreteStateA ..> ConcreteStateB : transitions to
    ConcreteStateB ..> ConcreteStateA : transitions to
```

The `Context` delegates `request()` to the current `State`. Each `ConcreteState` implements that state's behavior and can call `setState()` on the context to trigger the transition to another state.

## Example

An e-commerce order goes through the states "pending payment", "paid", and "shipped"; the `pay()` and `ship()` actions are only valid in certain states.

```typescript
interface OrderState {
  pay(order: Order): void;
  ship(order: Order): void;
}

class PendingPayment implements OrderState {
  pay(order: Order) { order.setState(new Paid()); }
  ship(_: Order) { throw new Error("Order hasn't been paid yet"); }
}

class Paid implements OrderState {
  pay(_: Order) { throw new Error("Order is already paid"); }
  ship(order: Order) { order.setState(new Shipped()); }
}

class Shipped implements OrderState {
  pay(_: Order) { throw new Error("Order already shipped"); }
  ship(_: Order) { throw new Error("Order already shipped"); }
}

class Order {
  private state: OrderState = new PendingPayment();
  setState(state: OrderState) { this.state = state; }
  pay() { this.state.pay(this); }
  ship() { this.state.ship(this); }
}
```

## Related patterns

- [Strategy](/coding/gof/behavioral/strategy) — has an almost identical structure (a context delegating to an interchangeable object), but the intent differs: in Strategy the client chooses the algorithm and the strategies are independent and don't know each other; in State the swap is driven by the object itself according to its internal state, and the states usually know about and trigger the transitions between themselves.
- [Singleton](/coding/gof/creational/singleton) — states with no data of their own can be shared single instances.
- [Flyweight](/coding/gof/structural/flyweight) — allows sharing state objects among several contexts, keeping the specific data in the context.
- [Memento](/coding/gof/behavioral/memento) — can capture and restore an object's state, for example to undo transitions.
- [Bridge](/coding/gof/structural/bridge) — is also based on composition and delegation to a hierarchy of implementations, but with a structural focus, not on transitions.

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [State on Refactoring.Guru](https://refactoring.guru/design-patterns/state)
