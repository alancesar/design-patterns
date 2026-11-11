---
title: Table Data Gateway
pattern_slug: table-data-gateway
category: Data Source Architectural
tags:
  - Decoupling
  - Simplicity
source: https://martinfowler.com/eaaCatalog/tableDataGateway.html
sidebar_label: "Table Data Gateway"
---

# Table Data Gateway

## Description

Table Data Gateway is an object that acts as a gateway to a database table (or view). A single instance handles all the rows in the table and concentrates all the SQL for querying, inserting, updating, and deleting.

The rest of the application doesn't write SQL: it calls methods such as `findById`, `findOverdue`, or `insert`. The gateway is normally stateless and returns simple data structures, such as Record Sets or DTOs, instead of domain objects with behavior.

As a result, the SQL lives in one place, which helps people who aren't fluent in SQL and lets DBAs find and tune the queries when the schema changes.

## Problems it solves

- SQL scattered across the business logic and the presentation layer.
- Schema changes that require edits in many places in the code.
- Difficulty for DBAs to locate and optimize the queries the application uses.
- The need for a simple access layer for table-oriented domain logic.

## When to use

- With Transaction Script, where the business logic operates on tabular data.
- With Table Module, which usually receives Record Sets produced by the gateway.
- To encapsulate access to stored procedures, treating them as a gateway.
- When you want to isolate SQL without the cost of a full object-relational mapping.

## When to avoid

- When there's a rich Domain Model with complex rules; a Data Mapper or ORM fits better.
- When you expect to map inheritance, associations, and collections of objects transparently.
- When the gateway tends to accumulate dozens of queries and turn into a table "god object".

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| All the SQL is centralized and easy to tune | Little help mapping rich domain objects |
| Simple interface, close to the table's structure | Tabular results expose the schema to their consumers |
| Fits well with Transaction Script and Table Module | Gateways can grow with many specific queries |
| Simple to replace with a test double | Doesn't manage identity or concurrency on its own |

- **Coupling:** business code depends on the gateway's interface, not on SQL; even so, it sees the shape of the tables.
- **Testability:** the gateway can be swapped for a Service Stub or an in-memory database.
- **Complexity:** low, with one class per table.

## Diagram

```mermaid
classDiagram
    class Client
    class BoletoGateway {
        +findById(id)
        +findOverdue(today)
        +insert(payerId, amountCents, dueDate)
        +updateStatus(id, status)
    }
    class Database
    Client --> BoletoGateway
    BoletoGateway --> Database
```

The `Client` (for example, a billing Transaction Script) calls only methods of the `BoletoGateway`, which contains the SQL and talks to the `Database`. One instance serves all the rows in the table.

## Example

The billing scripts of a fintech need to query and write boletos. A `BoletoGateway` isolates the SQL for the `boletos` table and returns plain rows.

```python
class BoletoGateway:
    def __init__(self, conn):
        self.conn = conn

    def find_by_id(self, boleto_id):
        cur = self.conn.execute(
            "SELECT id, payer_id, amount_cents, due_date, status "
            "FROM boletos WHERE id = ?", (boleto_id,))
        return cur.fetchone()

    def find_overdue(self, today):
        cur = self.conn.execute(
            "SELECT id, payer_id, amount_cents, due_date, status "
            "FROM boletos WHERE status = 'OPEN' AND due_date < ?", (today,))
        return cur.fetchall()

    def insert(self, payer_id, amount_cents, due_date):
        cur = self.conn.execute(
            "INSERT INTO boletos (payer_id, amount_cents, due_date, status) "
            "VALUES (?, ?, ?, 'OPEN')", (payer_id, amount_cents, due_date))
        return cur.lastrowid

    def update_status(self, boleto_id, status):
        self.conn.execute(
            "UPDATE boletos SET status = ? WHERE id = ?", (status, boleto_id))

# Transaction Script
def flag_overdue_boletos(gateway, today):
    for boleto in gateway.find_overdue(today):
        gateway.update_status(boleto[0], "OVERDUE")  # id is the first column
```

In .NET, ADO.NET's `TableAdapter` and the DAO class from the Java world follow a similar idea.

## Related patterns

- [Row Data Gateway](/design/poeaa/data-source-architectural/row-data-gateway) — one object per row instead of one per table.
- [Active Record](/design/poeaa/data-source-architectural/active-record) — the domain object also accumulates the database access.
- [Data Mapper](/design/poeaa/data-source-architectural/data-mapper) — an alternative when the domain model is rich and independent of the schema.
- [Transaction Script](/design/poeaa/domain-logic/transaction-script) — the typical pairing of domain logic with this gateway.
- [Table Module](/design/poeaa/domain-logic/table-module) — consumes the Record Sets the gateway produces.
- [Record Set](/design/poeaa/base/record-set) — the common format of the results.
- [Gateway](/design/poeaa/base/gateway) — the base pattern of which this is a specialization.
- [Facade](/coding/gof/structural/facade) — also hides the details of a subsystem behind a simple interface.

## Reference

- [Pattern page in Fowler's catalog](https://martinfowler.com/eaaCatalog/tableDataGateway.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
- [Table data gateway on Wikipedia](https://en.wikipedia.org/wiki/Table_data_gateway)
