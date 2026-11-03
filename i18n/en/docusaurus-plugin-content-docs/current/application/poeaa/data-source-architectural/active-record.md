---
title: Active Record
pattern_slug: active-record
category: Data Source Architectural
tags:
  - Simplicity
source: https://martinfowler.com/eaaCatalog/activeRecord.html
sidebar_label: "Active Record"
---

# Active Record

## Description

Active Record is an object that wraps a row in a table or view, encapsulates database access, and adds domain logic on top of that data. The object's fields map directly to the columns, and the object itself knows how to load, save, and delete itself.

In essence, it's a Row Data Gateway with business logic. Finder methods are usually static or live in a helper class, and the object brings together data and behavior, which gives the impression of an object model without a separate mapping layer.

It works well as long as the domain model is similar to the database schema; when the two diverge, the coupling becomes a problem.

## Problems it solves

- Too much infrastructure code to persist simple domain objects.
- The need for a lightweight data access layer, without separate mapping.
- Duplication between data classes and logic classes when the model is almost identical to the tables.

## When to use

- When the domain logic is moderate: create, read, update, delete, and simple validations.
- When the object model can closely follow the database schema.
- To quickly deliver CRUD applications, as in Rails and Laravel.

### When to avoid

- When the business logic is complex and requires inheritance, collections, and relationships that diverge from the schema.
- When you want to test the domain without a database.
- When the schema changes often and shouldn't affect the domain model.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Very simple and quick to get started | Domain object coupled to the schema and the database |
| Data and behavior together, easy to understand | Makes unit testing without a database harder |
| Little mapping code | Refactoring schema and model independently is difficult |
| Good for CRUD | Mixes responsibilities (persistence and rules) |

- **Coupling:** high between domain and schema; changes in one affect the other.
- **Testability:** limited, unless you use an in-memory database or test doubles.
- **Complexity:** low at first, but it can grow as the domain becomes richer.

## Diagram

```mermaid
classDiagram
    class Client
    class Person {
        +id
        +name
        +birthDate
        +find(id)$
        +save()
        +delete()
        +calculateAge()
    }
    class Database
    Client --> Person
    Person --> Database
```

The `Client` uses `Person` directly. `Person` holds the data of one row, contains the domain logic (`calculateAge`), and accesses the `Database` through `save`, `delete`, and `find`.

## Example

A store has products with simple rules, such as applying a discount. The `Product` class represents the row and knows how to save itself, as in the models of Rails ActiveRecord, Django ORM, or Eloquent.

```python
class Product:
    def __init__(self, conn, id, name, price):
        self.conn, self.id, self.name, self.price = conn, id, name, price

    @classmethod
    def find(cls, conn, id):
        r = conn.execute(
            "SELECT id, name, price FROM products WHERE id = ?", (id,)).fetchone()
        return cls(conn, *r)

    def apply_discount(self, percent):  # domain logic
        self.price = round(self.price * (1 - percent / 100), 2)

    def save(self):
        self.conn.execute(
            "UPDATE products SET name = ?, price = ? WHERE id = ?",
            (self.name, self.price, self.id))

product = Product.find(conn, 7)
product.apply_discount(10)
product.save()
```

## Related patterns

- [Row Data Gateway](/application/poeaa/data-source-architectural/row-data-gateway) — same structure, but without domain logic.
- [Table Data Gateway](/application/poeaa/data-source-architectural/table-data-gateway) — per-table access, instead of one object per row.
- [Data Mapper](/application/poeaa/data-source-architectural/data-mapper) — separates domain and persistence when the model is rich.
- [Domain Model](/application/poeaa/domain-logic/domain-model) — with a simple model, Active Record is one way to implement it.
- [Transaction Script](/application/poeaa/domain-logic/transaction-script) — a more procedural alternative for simple logic.
- [Identity Field](/application/poeaa/object-relational-structural/identity-field) — the primary key stored in the object.

## Reference

- [Pattern page in Fowler's catalog](https://martinfowler.com/eaaCatalog/activeRecord.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
- [Active record pattern on Wikipedia](https://en.wikipedia.org/wiki/Active_record_pattern)
