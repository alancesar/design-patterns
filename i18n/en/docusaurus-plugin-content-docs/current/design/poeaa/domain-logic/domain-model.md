---
title: Domain Model
pattern_slug: domain-model
category: Domain Logic
tags:
  - Extensibility
  - Testability
source: https://martinfowler.com/eaaCatalog/domainModel.html
sidebar_label: "Domain Model"
---

# Domain Model

## Description

Domain Model is an object model of the business domain that incorporates both behavior and data. Each object represents a meaningful business concept, from something large, like a company, to something small, like a line on an order.

The objects form an interconnected network, and the business rules live alongside the data they govern. Calculations, validations, and decisions sit inside entities and value objects, with support from inheritance, polymorphism, and other object-oriented techniques to handle many rule variations.

The model should be independent of the user interface and of persistence; the link to the database is usually made by a data mapper.

## Problems it solves

- Complex business logic, with many rules and exceptions that turn into conditionals scattered across procedural scripts.
- Rules duplicated across different use cases.
- Difficulty expressing the business language in code.
- The need to evolve rules without rewriting the whole application.

## When to use

- Domains with complex, constantly changing rules.
- When there are behavior variations that benefit from polymorphism and from patterns such as Strategy.
- When the team is skilled at object-oriented modeling and plans to invest in a ubiquitous language for the domain.

## When to avoid

- Essentially CRUD applications, where the logic is minimal.
- Teams unfamiliar with object orientation and object-relational mapping.
- When the cost of mapping objects to tables outweighs the gain in expressiveness.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Rules expressed in a rich, reusable way | Steep learning curve |
| Easy to test without a database | Requires object-relational mapping (Data Mapper, Unit of Work) |
| Extensible through polymorphism and composition | Risk of an anemic model, with logic outside the entities |
| Business language reflected in the code | Can load too many objects and queries if poorly designed |

- **Decoupling:** the model knows nothing about persistence or the interface.
- **Performance:** loading object graphs requires attention to Lazy Load and to efficient queries.
- **Boundary:** it's usually exposed through a Service Layer to avoid leaking details to clients.

## Diagram

```mermaid
classDiagram
    class Customer {
        +currentInvoice() CardInvoice
    }
    class CardInvoice {
        +addEntry(merchant, amount)
        +total() Money
        +close()
    }
    class InvoiceEntry {
        +amount() Money
    }
    class Merchant
    Customer "1" --> "*" CardInvoice
    CardInvoice "1" *-- "*" InvoiceEntry
    InvoiceEntry --> Merchant
```

`Customer`, `CardInvoice`, `InvoiceEntry`, and `Merchant` form a network of objects in which each class holds data and the associated rules, such as `total()` and `close()`.

## Example

A card invoice calculates its own total and rejects entries once it is closed, rules that live in the entity.

```java
public class CardInvoice {
    private final List<InvoiceEntry> entries = new ArrayList<>();
    private Status status = Status.OPEN;

    public void addEntry(Merchant merchant, Money amount) {
        if (status != Status.OPEN) throw new IllegalStateException("Invoice is closed");
        entries.add(new InvoiceEntry(merchant, amount));
    }

    public Money total() {
        return entries.stream()
            .map(InvoiceEntry::amount)
            .reduce(Money.ZERO, Money::add);
    }

    public void close() {
        if (status == Status.CLOSED) throw new IllegalStateException("Already closed");
        status = Status.CLOSED;
    }
}
```

## Related patterns

- [Transaction Script](/design/poeaa/domain-logic/transaction-script) — a simpler alternative for low-complexity logic.
- [Table Module](/design/poeaa/domain-logic/table-module) — organizes logic by table, a middle ground between the two.
- [Service Layer](/design/poeaa/domain-logic/service-layer) — the usual boundary of the Domain Model, coordinating use cases and transactions.
- [Data Mapper](/design/poeaa/data-source-architectural/data-mapper) — keeps the model independent of the database.
- [Unit of Work](/design/poeaa/object-relational-behavioral/unit-of-work) — tracks changes to the model's objects.
- [Strategy](/coding/gof/behavioral/strategy) — encapsulates rule variations inside the model.
- [Null Object](/coding/gof/behavioral/null-object) — avoids null checks in the rules.

## Reference

- [Pattern page in Fowler's catalog](https://martinfowler.com/eaaCatalog/domainModel.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
- [Domain model on Wikipedia](https://en.wikipedia.org/wiki/Domain_model)
