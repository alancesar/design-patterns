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
mdx:
  format: mdx
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

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

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

</TabItem>
<TabItem value="python" label="Python">

```python
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class PixCharge:
    amount_cents: int
    receiver_key: str
    due_date: Optional[date] = None
    fine_rate: float = 0.0
    daily_interest_rate: float = 0.0
    discount_rate: float = 0.0
    payer_message: Optional[str] = None
    txid: str = field(default_factory=lambda: uuid.uuid4().hex)  # generated on creation

class PixChargeBuilder:
    def __init__(self, amount_cents: int, receiver_key: str) -> None:
        self._fields: dict = {"amount_cents": amount_cents, "receiver_key": receiver_key}

    def due_date(self, d: date) -> PixChargeBuilder:
        self._fields["due_date"] = d
        return self

    def fine_rate(self, r: float) -> PixChargeBuilder:
        self._fields["fine_rate"] = r
        return self

    def daily_interest_rate(self, r: float) -> PixChargeBuilder:
        self._fields["daily_interest_rate"] = r
        return self

    def discount_rate(self, r: float) -> PixChargeBuilder:
        self._fields["discount_rate"] = r
        return self

    def payer_message(self, m: str) -> PixChargeBuilder:
        self._fields["payer_message"] = m
        return self

    def build(self) -> PixCharge:
        f = self._fields
        if f["amount_cents"] <= 0:
            raise ValueError("amount must be positive")
        has_charges = any(f.get(k, 0) > 0 for k in ("fine_rate", "daily_interest_rate", "discount_rate"))
        if has_charges and "due_date" not in f:
            raise ValueError("fine, interest and discount require a due date")
        return PixCharge(**f)

# Usage: R$ 250.00 with a due date, a 2% fine and 0.033% daily interest
charge = (
    PixChargeBuilder(25_000, "pagamentos@fintech.example")
    .due_date(date(2026, 12, 10))
    .fine_rate(0.02)
    .daily_interest_rate(0.00033)
    .payer_message("December tuition")
    .build()
)
```

</TabItem>
<TabItem value="go" label="Go">

```go
// Unexported fields: outside the package, a PixCharge can only be created through the builder.
type PixCharge struct {
	amountCents                           int64
	receiverKey, txid, payerMessage       string
	dueDate                               time.Time
	fineRate, dailyInterestRate, discount float64
}

type PixChargeBuilder struct {
	charge PixCharge
}

func NewPixChargeBuilder(amountCents int64, receiverKey string) *PixChargeBuilder {
	return &PixChargeBuilder{PixCharge{amountCents: amountCents, receiverKey: receiverKey}}
}

func (b *PixChargeBuilder) DueDate(d time.Time) *PixChargeBuilder { b.charge.dueDate = d; return b }
func (b *PixChargeBuilder) FineRate(r float64) *PixChargeBuilder  { b.charge.fineRate = r; return b }
func (b *PixChargeBuilder) DailyInterestRate(r float64) *PixChargeBuilder {
	b.charge.dailyInterestRate = r
	return b
}
func (b *PixChargeBuilder) DiscountRate(r float64) *PixChargeBuilder { b.charge.discount = r; return b }
func (b *PixChargeBuilder) PayerMessage(m string) *PixChargeBuilder {
	b.charge.payerMessage = m
	return b
}

func (b *PixChargeBuilder) Build() (PixCharge, error) {
	c := b.charge
	if c.amountCents <= 0 {
		return PixCharge{}, errors.New("amount must be positive")
	}
	hasCharges := c.fineRate > 0 || c.dailyInterestRate > 0 || c.discount > 0
	if hasCharges && c.dueDate.IsZero() {
		return PixCharge{}, errors.New("fine, interest and discount require a due date")
	}
	id := make([]byte, 16)
	rand.Read(id)
	c.txid = hex.EncodeToString(id) // the txid is generated on creation
	return c, nil
}

func main() {
	// Usage: R$ 250.00 with a due date, a 2% fine and 0.033% daily interest
	charge, err := NewPixChargeBuilder(25_000, "pagamentos@fintech.example").
		DueDate(time.Date(2026, 12, 10, 0, 0, 0, 0, time.UTC)).
		FineRate(0.02).
		DailyInterestRate(0.00033).
		PayerMessage("December tuition").
		Build()
}
```

</TabItem>
</Tabs>

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
