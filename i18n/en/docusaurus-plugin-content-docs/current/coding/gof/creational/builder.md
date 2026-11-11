---
title: Builder
pattern_slug: builder
category: Creational
tags:
  - Encapsulation
  - Simplicity
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Builder"
---

# Builder

## Description

Builder separates the construction of a complex object from its representation, allowing the same construction process to produce different representations. Instead of assembling the object all at once through a constructor with many parameters, creation is split into named, explicit steps.

A `Builder` defines the operations for creating each part of the product; concrete implementations (`ConcreteBuilder`) know how to assemble and store those parts and expose a method to get the final result. Optionally, a `Director` encapsulates the order of the steps for recurring construction recipes, so the client only chooses which builder to use.

In modern practice, the most common variant is the fluent builder (chained methods that return the builder itself), used to create immutable objects with many optional attributes and to validate the object's consistency before handing it over.

## Problems it solves

- Constructors with long parameter lists, many of them optional, that are hard to read and prone to ordering mistakes (the "telescoping constructor")
- The need to assemble an object step by step, sometimes with conditional or repeated steps
- The same construction process having to generate different representations (e.g., a document in HTML, Markdown, or PDF)
- Creating immutable objects whose state must be complete and valid by the time they're handed over

## When to use

- The object has many attributes, especially optional ones or ones with default values
- Construction involves several steps, meaningful ordering, or validation rules across fields
- You want to reuse the same assembly algorithm to produce different products
- You need immutable objects, but without giant constructors
- Assembling composite structures (trees, SQL queries, HTTP requests, messages)

## When to avoid

- The object is simple, with few required fields; a constructor or factory is enough
- The language already offers named parameters and default values that eliminate the problem
- The products don't share a common construction process, making the abstraction artificial
- The cost of keeping a builder in sync with every change to the product class isn't worth it

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Readable, self-documenting client code (named steps) | More classes and code to maintain (one builder per product) |
| Enables immutable products and validation centralized in `build()` | Field duplication between builder and product |
| Isolates construction code from the product's business logic | The builder can fall out of date with respect to the product |
| The same process generates different representations | Forgotten required fields only show up at run time (unless builders are typed per step) |

- **Coupling:** the client depends on the builder, not on the product's internal representation.
- **Testability:** builders make it easy to create test data ("test data builders") with sensible default values.
- **Complexity:** the `Director` is optional; it often adds layers with no real benefit.
- **Concurrency:** builders are mutable and usually shouldn't be shared between threads.

## Diagram

```mermaid
classDiagram
    class Director {
        -builder: Builder
        +construct()
    }
    class Builder {
        <<interface>>
        +buildPartA()
        +buildPartB()
        +getResult() Product
    }
    class ConcreteBuilder {
        -product: Product
        +buildPartA()
        +buildPartB()
        +getResult() Product
    }
    class Product
    class Client
    Director o--> Builder
    Builder <|.. ConcreteBuilder
    ConcreteBuilder ..> Product : creates
    Client --> Director
    Client --> ConcreteBuilder
```

The `Client` creates a `ConcreteBuilder` and hands it to the `Director`, which calls the construction steps in the correct order; at the end, the client gets the assembled `Product` from the builder itself via `getResult()`.

## Example

A Pix charge requires an amount and the receiver's key, and has an optional due date, fine, interest, discount and a message to the payer. A fluent builder keeps creation readable, validates the combinations (fine, interest and discount only make sense with a due date) and hands back an immutable `PixCharge` with the `txid` already generated. Rates and amounts are illustrative.

```java
public final class PixCharge {
    private final long amountCents;
    private final String receiverKey, txid, payerMessage;
    private final LocalDate dueDate;
    private final double fineRate, dailyInterestRate, discountRate;

    private PixCharge(Builder b) {
        amountCents = b.amountCents; receiverKey = b.receiverKey;
        payerMessage = b.payerMessage; dueDate = b.dueDate;
        fineRate = b.fineRate; dailyInterestRate = b.dailyInterestRate;
        discountRate = b.discountRate;
        txid = UUID.randomUUID().toString().replace("-", "");
    }

    public static Builder builder(long amountCents, String receiverKey) {
        return new Builder(amountCents, receiverKey);
    }

    public static final class Builder {
        private final long amountCents;
        private final String receiverKey;
        private String payerMessage;
        private LocalDate dueDate;
        private double fineRate, dailyInterestRate, discountRate;

        private Builder(long amountCents, String receiverKey) {
            this.amountCents = amountCents; this.receiverKey = receiverKey;
        }
        public Builder dueDate(LocalDate d) { this.dueDate = d; return this; }
        public Builder fineRate(double r) { this.fineRate = r; return this; }
        public Builder dailyInterestRate(double r) { this.dailyInterestRate = r; return this; }
        public Builder discountRate(double r) { this.discountRate = r; return this; }
        public Builder payerMessage(String m) { this.payerMessage = m; return this; }

        public PixCharge build() {
            if (amountCents <= 0)
                throw new IllegalStateException("amount must be positive");
            boolean hasCharges = fineRate > 0 || dailyInterestRate > 0 || discountRate > 0;
            if (hasCharges && dueDate == null)
                throw new IllegalStateException("fine, interest and discount require a due date");
            return new PixCharge(this); // the constructor generates the txid
        }
    }
}

// Usage: R$ 250.00 with a due date, a 2% fine and 0.033% daily interest
PixCharge charge = PixCharge.builder(25_000, "pagamentos@fintech.example")
    .dueDate(LocalDate.of(2026, 12, 10)).fineRate(0.02).dailyInterestRate(0.00033)
    .payerMessage("December tuition").build();
```

## Related patterns

- [Abstract Factory](/coding/gof/creational/abstract-factory) — also creates complex objects, but returns families of products at once; Builder focuses on assembling a single product step by step
- [Telescoping Constructor](/coding/gof/creational/telescoping-constructor) — an anti-pattern that Builder normally replaces
- [Factory Method](/coding/gof/creational/factory-method) — a simpler alternative when creation fits in a single call
- [Prototype](/coding/gof/creational/prototype) — another way to avoid complex construction, by cloning an already-configured object
- [Composite](/coding/gof/structural/composite) — Builder is often used to assemble Composite trees
- [Singleton](/coding/gof/creational/singleton) — a shared Director or builder is sometimes exposed as a single instance

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Builder on Refactoring.Guru](https://refactoring.guru/design-patterns/builder)
