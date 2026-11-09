---
title: Abstract Core
pattern_slug: abstract-core
category: Distillation
tags:
  - Shared Understanding
  - Simplicity
  - Decoupling
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Abstract Core"
---

# Abstract Core

## Description

The Abstract Core is a separate module that holds the most fundamental concepts of the model, expressed as abstract classes and interfaces. It captures the essential vocabulary and interactions between subdomains, without the implementation details that vary from one to the next.

Specialized modules depend on the Abstract Core and implement or extend its types, but they don't depend directly on one another. This lets you understand the high-level model by reading only the abstract core, and it reduces coupling between the specialized parts.

It's a stronger tool than the [Highlighted Core](/design/ddd/distillation/highlighted-core) because it changes the structure of the code, but it can be less invasive than a [Segregated Core](/design/ddd/distillation/segregated-core) when the core is too large to move in its entirety. It's only worth it when there's a lot of interaction between modules and a clearly stable set of concepts.

## Problems it solves

- A large model in which many modules talk to each other and create a web of dependencies.
- Difficulty understanding the whole without walking through every specialized module.
- Concrete types scattered around, forcing cascading changes when one module evolves.
- The lack of a common vocabulary that cuts across subdomains.

## When to use

- When there's a lot of interaction between modules and a stable conceptual core can be identified.
- When the core is too large to be segregated in its entirety.
- When you want specialized modules to be able to vary without affecting one another.

## When to avoid

- When the model is still changing quickly and there aren't enough stable concepts to abstract.
- When few modules interact; the abstractions would be ceremony with no payoff.
- When abstracting hides important business rules or introduces excessive indirection.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| High-level view in a single module | Premature abstractions can lock the model in |
| Specialized modules decoupled from one another | More indirection and more types to maintain |
| Common vocabulary across subdomains | Takes maturity to identify what is truly stable |
| Easier testing with alternative implementations | Changes to the abstract core affect every module |

- **Stability:** the abstract core changes rarely; modifying it has a wide impact and calls for care.
- **Dependencies:** they always point from the specialized modules to the core, never the other way around.
- **Commitment:** you have to decide what goes into the core; too much content turns it into a second copy of the model.

## Diagram

```mermaid
classDiagram
    class Insurable {
        <<interface>>
        +riskScore() Score
    }
    class Policy {
        <<abstract>>
        +premium() Money
    }
    class AutoPolicy {
        +premium() Money
    }
    class LifePolicy {
        +premium() Money
    }
    class AutoVehicle {
        +riskScore() Score
    }
    class Person {
        +riskScore() Score
    }
    Policy --> Insurable
    Policy <|-- AutoPolicy
    Policy <|-- LifePolicy
    Insurable <|.. AutoVehicle
    Insurable <|.. Person
```

`Policy` and `Insurable` form the abstract core; the auto and life insurance modules specialize it without knowing about each other.

## Example

An insurer offers auto and life insurance, with modules that evolve at different paces. Both need to take part in campaigns, renewals, and exposure reports, which led to direct dependencies between the modules.

The team creates the `insurance-core` module, containing only `Policy`, `Insurable`, and `Premium`, in abstract terms. The `auto` and `life` modules implement it, and renewals and reports now depend only on the abstractions.

```java
// insurance-core module
public interface Insurable { Score riskScore(); }

public abstract class Policy {
    protected final Insurable subject;
    protected Policy(Insurable subject) { this.subject = subject; }
    public abstract Money premium();
}

// auto module (depends on insurance-core)
public class AutoPolicy extends Policy {
    public AutoPolicy(AutoVehicle vehicle) { super(vehicle); }
    public Money premium() { return Money.of(100).times(subject.riskScore()); }
}
```

## Related patterns

- [Core Domain](/design/ddd/distillation/core-domain) — the Abstract Core is one way to organize and communicate the core.
- [Highlighted Core](/design/ddd/distillation/highlighted-core) — a lighter alternative that doesn't change the structure.
- [Segregated Core](/design/ddd/distillation/segregated-core) — an alternative that moves the entire core, instead of extracting only abstractions.
- [Module](/design/ddd/building-blocks/module) — the abstract core lives in a module of its own.
- [Knowledge Level](/design/ddd/large-scale-structure/knowledge-level) — another way to separate abstract concepts from configurable rules.
- [Pluggable Component Framework](/design/ddd/large-scale-structure/pluggable-component-framework) — uses abstract interfaces to allow interchangeable components.
- [Separated Interface](/design/poeaa/base/separated-interface) — a technique for placing interface and implementation in distinct packages.
- [Abstract Factory](/coding/gof/creational/abstract-factory) — commonly used to create implementations without knowing the concrete types.

## Reference

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
