---
title: Side-Effect-Free Functions
pattern_slug: side-effect-free-functions
category: Supple Design
tags:
  - Simplicity
  - Consistency
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Side-Effect-Free Functions"
---

# Side-Effect-Free Functions

## Description

Side-Effect-Free Functions proposes separating operations into two categories: commands, which modify state, and queries, which only return a result. A function is free of side effects when it computes and returns a value without changing anything observable. Commands should be simple and should not return domain data.

Complex logic is placed in pure functions, preferably in Value Objects, which are immutable. That way, an operation that combines values returns a new object instead of modifying the existing one. When the calculation lives in an Entity, part of it can be extracted into a Value Object, leaving the Entity just applying the result.

The effect is a strong reduction in mental load: the developer can call and compose functions without fear of changing the state of another object, and tests become simple.

## Problems it solves

- Operations that mix calculation and state change, hard to predict and to test.
- Cascading side effects, where calling a method changes objects the caller didn't expect.
- Difficulty reusing a calculation without triggering its state change.
- Bugs caused by call order and by shared mutable state.

## When to use

- In complex domain calculations (prices, interest, deadlines, rates).
- When modeling concepts as Value Objects, which should be immutable.
- When a query is called in many places and needs to be safe to compose.

## When to avoid

- In large objects where copying on every operation is expensive and demonstrably a bottleneck.
- When the domain is by nature a sequence of state changes (for example, a long process): there the command is legitimate and should be explicit, not hidden.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Simple tests, no state setup | Creates new objects on every operation |
| Safe composition and local reasoning | Requires discipline to separate commands from queries |
| Caching and parallelism made easier | Can feel unnatural in mutable libraries |

- **Consistency:** fewer points where state can be corrupted.
- **Performance:** immutability can cost allocations; measure before giving it up.
- **Commands:** keep them small and with a clearly named effect.

## Diagram

```mermaid
classDiagram
    class Account {
        -Money balance
        +credit(Money amount)
    }
    class Money {
        -long cents
        +plus(Money other) Money
        +times(BigDecimal rate) Money
        +allocate(int[] ratios) List~Money~
    }
    Account --> Money : balance
```

`Account.credit` is a command that changes state, while `Money.times` and `Money.allocate` are pure functions that compute new values without altering any object. The book illustrates the pattern with paint mixing.

## Example

In a digital account, computing the yield and splitting an amount are delicate rules because of rounding. They live in `Money`, an immutable Value Object; the command in `Account` just applies the result. The rate is an illustrative value.

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
        return new Money(cents + other.cents, currency);
    }

    // Pure function: returns a new value, nothing is modified
    public Money times(BigDecimal rate) {
        long result = BigDecimal.valueOf(cents).multiply(rate)
            .setScale(0, RoundingMode.HALF_EVEN).longValueExact();
        return new Money(result, currency);
    }

    // Pure function: splits without losing cents (the remainder goes to the first shares)
    public List<Money> allocate(int... ratios) {
        long totalRatio = Arrays.stream(ratios).sum();
        long[] shares = new long[ratios.length];
        long remainder = cents;
        for (int i = 0; i < ratios.length; i++) {
            shares[i] = Math.floorDiv(cents * ratios[i], totalRatio);
            remainder -= shares[i];
        }
        for (int i = 0; i < remainder; i++) shares[i]++;
        return Arrays.stream(shares)
            .mapToObj(s -> new Money(s, currency)).toList();
    }
}

public class Account {
    private Money balance;

    // Command: simple, just applies the result
    public void credit(Money amount) {
        balance = balance.plus(amount);
    }

    public Money balance() { return balance; }
}

// Compute (query) and then apply (command)
Money yield = account.balance().times(new BigDecimal("0.0105"));
account.credit(yield);
```

## Related patterns

- [Value Object](/design/poeaa/base/value-object) — the natural home for pure functions, since they're immutable.
- [Entity](/design/ddd/building-blocks/entity) — keeps the commands, delegating the calculation to values.
- [Closure of Operations](/design/ddd/supple-design/closure-of-operations) — operations that return the same type go well with pure functions.
- [Assertions](/design/ddd/supple-design/assertions) — document the effects of the commands that remain.
- [Intention-Revealing Interfaces](/design/ddd/supple-design/intention-revealing-interfaces) — the name should make clear whether it's a command or a query.
- [Money](/design/poeaa/base/money) (PoEAA) — an immutable value with pure operations.

## Reference

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
- [Command Query Separation (Fowler's bliki)](https://martinfowler.com/bliki/CommandQuerySeparation.html)
