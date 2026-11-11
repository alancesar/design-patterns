---
title: Standalone Classes
pattern_slug: standalone-classes
category: Supple Design
tags:
  - Decoupling
  - Simplicity
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Standalone Classes"
---

# Standalone Classes

## Description

Standalone Classes proposes reducing each class's dependencies to a minimum, until it can be understood and tested on its own, without referencing other classes beyond primitive types and the language's basic libraries. Every extra dependency requires the reader to understand the other concept as well.

The goal isn't to eliminate all coupling, but to make the essential coupling explicit and remove the remaining links. Each association and each parameter is examined: if the concept can be understood without the other class, the dependency is removed. Value Objects are usually ideal candidates.

When a Standalone Class is achieved, the gain is large: the concept can be understood, tested, and changed in isolation, and the model's mental load drops. The classes that can't achieve this are the ones that concentrate the domain's essential complexity.

## Problems it solves

- Classes that can only be understood together with several others, increasing mental load.
- Tests that require assembling a large graph of objects.
- Changes that propagate through unnecessary dependencies.
- Models in which every concept depends on every other one.

## When to use

- In domain concepts that can be expressed with just values and basic types.
- When modeling Value Objects and pure calculations.
- In model reviews, to identify dependencies that aren't essential.

## When to avoid

- When the concept is, by nature, a relationship with others: forcing isolation hides the real association.
- When isolation requires duplicating logic from other classes, increasing the total cost.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Isolated understanding and testing | May require rethinking the model to remove dependencies |
| Less propagation of changes | Some concepts can't be made independent |
| Easy reuse | Risk of duplicating logic to avoid a dependency |

- **Mental load:** every dependency removed is one less concept to keep in your head.
- **Essential coupling:** keep the dependencies that express the domain.
- **Priority:** apply it first to the most used and most complex classes.

## Diagram

```mermaid
classDiagram
    class Money {
        -long cents
        -Currency currency
        +plus(Money other) Money
        +minus(Money other) Money
    }
    class Account {
        -Money balance
        +credit(Money amount)
        +debit(Money amount)
    }
    class Ledger
    class LedgerEntry
    Account --> Money
    Ledger --> Account
    Ledger --> LedgerEntry
    LedgerEntry --> Money
```

`Money` depends only on primitive types and the currency, and can be understood on its own, while `Ledger` concentrates the context's dependencies. The book illustrates the pattern with paint mixing.

## Example

The `Money` class knows only numbers and a currency. It doesn't reference `Account`, `Ledger`, or any service, so it's tested with no setup at all.

```java
public final class Money {
    private final long cents;
    private final Currency currency;

    private Money(long cents, Currency currency) {
        this.cents = cents; this.currency = currency;
    }

    public static Money brl(long cents) {
        return new Money(cents, Currency.getInstance("BRL"));
    }

    public Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("different currencies cannot be added");
        }
        return new Money(cents + other.cents, currency);
    }

    public Money minus(Money other) {
        return plus(new Money(-other.cents, other.currency));
    }
}

// Isolated test, with no other domain objects
Money total = Money.brl(10_00).plus(Money.brl(5_50));
assertEquals(Money.brl(15_50), total);
```

## Related patterns

- [Value Object](/design/poeaa/base/value-object) — a natural candidate for a standalone class.
- [Module](/design/ddd/building-blocks/module) — low coupling between modules and high cohesion within them.
- [Side-Effect-Free Functions](/design/ddd/supple-design/side-effect-free-functions) — pure functions in standalone classes are very easy to understand.
- [Closure of Operations](/design/ddd/supple-design/closure-of-operations) — another way to reduce dependencies in operations.
- [Cohesive Mechanisms](/design/ddd/distillation/cohesive-mechanisms) — isolates complex mechanisms so the model stays focused.

## Reference

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
