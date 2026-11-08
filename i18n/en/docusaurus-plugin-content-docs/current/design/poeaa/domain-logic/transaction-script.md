---
title: Transaction Script
pattern_slug: transaction-script
category: Domain Logic
tags:
  - Simplicity
  - Performance
source: https://martinfowler.com/eaaCatalog/transactionScript.html
sidebar_label: "Transaction Script"
---

# Transaction Script

## Description

Transaction Script organizes business logic as procedures, with one procedure for each request coming from the presentation layer. Each script receives the input, validates it, calculates, accesses the database (directly or through a thin gateway), and returns the result.

An enterprise application can be seen as a series of transactions: some only display data, others change it. Each transaction gets its own script, which runs linearly from start to finish. Common steps can be extracted into subprocedures, and several related scripts are usually grouped in the same class.

It's the most direct way to structure domain logic and works well as long as the rules are simple. As the logic grows, duplication between scripts tends to increase.

## Problems it solves

- The need to quickly implement simple use cases without building an infrastructure of objects and mapping.
- Teams with no object-modeling experience that need a style that's easy to understand.
- Operations that boil down to read, calculate, and write, where each request has a well-defined flow.

## When to use

- Simple business logic, with few rules and few interactions between them.
- Applications that need fine-grained control over SQL queries and performance.
- Small systems, prototypes, or reporting and import modules.

### When to avoid

- When the rules are complex and repeat across several use cases: duplication between scripts piles up.
- When the domain has many behavior variations that benefit from polymorphism.
- When the application must keep growing for a long time and logic scattered across procedures will become hard to maintain.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Simple to understand and implement | Logic duplicated across scripts as the system grows |
| No object-relational mapping layer; easy to control the SQL | Hard to refactor into a richer model later |
| Clear transaction boundaries: one script, one transaction | Business rules coupled to the table structure |
| Good, predictable performance | Tests depend on the database or on mocked gateways |

- **Complexity:** grows nonlinearly; what starts out simple becomes a tangle of procedures.
- **Testability:** good for small scripts, but depends on separating logic from data access.
- **Evolution:** migrating to a Domain Model is usually costly.

## Diagram

```mermaid
classDiagram
    class Presentation
    class OrderScripts {
        +placeOrder(customerId, items)
        +cancelOrder(orderId)
        +recognizeRevenue(contractId)
    }
    class Gateway {
        +find(id)
        +insert(row)
        +update(row)
    }
    class Database
    Presentation --> OrderScripts
    OrderScripts --> Gateway
    Gateway --> Database
```

The presentation layer calls one script per request. The scripts, grouped in `OrderScripts`, use a thin gateway to access the `Database`.

## Example

An order system needs to calculate the total with a discount and save the order. A single procedure does all the work.

```python
class OrderScripts:
    def __init__(self, db):
        self.db = db

    def place_order(self, customer_id: int, items: list[dict]) -> int:
        with self.db.transaction():
            total = sum(i["price"] * i["qty"] for i in items)
            customer = self.db.fetch_one(
                "SELECT vip FROM customers WHERE id = %s", customer_id
            )
            if customer["vip"]:
                total *= 0.9
            order_id = self.db.insert(
                "INSERT INTO orders (customer_id, total) VALUES (%s, %s)",
                customer_id, total,
            )
            for i in items:
                self.db.insert(
                    "INSERT INTO order_items (order_id, sku, qty) VALUES (%s, %s, %s)",
                    order_id, i["sku"], i["qty"],
                )
            return order_id
```

## Related patterns

- [Domain Model](/design/poeaa/domain-logic/domain-model) — an alternative for complex logic, with objects that combine data and behavior.
- [Table Module](/design/poeaa/domain-logic/table-module) — organizes logic by table instead of by request.
- [Service Layer](/design/poeaa/domain-logic/service-layer) — can be implemented with transaction scripts as the application boundary.
- [Table Data Gateway](/design/poeaa/data-source-architectural/table-data-gateway) — thin gateway frequently used by the scripts to access the database.
- [Command](/coding/gof/behavioral/command) — scripts can be organized as command objects, one per transaction.

## Reference

- [Pattern page in Fowler's catalog](https://martinfowler.com/eaaCatalog/transactionScript.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
