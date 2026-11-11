---
title: Table Module
pattern_slug: table-module
category: Domain Logic
tags:
  - Simplicity
  - Performance
source: https://martinfowler.com/eaaCatalog/tableModule.html
sidebar_label: "Table Module"
---

# Table Module

## Description

Table Module is a single instance that handles the business logic for all the rows in a database table or view. There is one class per table, and its methods receive or operate on a set of tabular data.

Unlike Domain Model, which creates one object per record (one object for each installment), Table Module has a single `Installments` object that processes all the installments. To identify a row, the client passes a key or the method receives the record as an argument.

The pattern works very well with Record Set, in-memory tabular structures provided by platforms such as .NET (DataSet), which integrate them with user interface and data access tools.

## Problems it solves

- Avoiding the cost and complexity of object-relational mapping for a Domain Model.
- Organizing logic in a predictable place instead of scattering it across scripts.
- Taking advantage of platforms and tools oriented toward tabular data.

## When to use

- When the platform offers strong support for Record Set and for data-bound UI controls.
- Logic of moderate complexity, organized around tables.
- When you want more structure than Transaction Script, without the cost of a Domain Model.

## When to avoid

- When the rules require polymorphism, inheritance, and rich relationships between entities.
- When the logic grows and spreads across many table modules that need to call each other.
- When the platform's Record Set support is weak.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Clearer structure than loose scripts | No polymorphism or per-object identity |
| No object-relational mapping needed | Coupled to the tabular shape of the data |
| Integrates well with data-oriented tools | Complex logic is hard to express |
| Few queries and efficient batch operations | Hard to migrate to a Domain Model later |

- **Performance:** processing many rows at once is usually efficient.
- **Testability:** requires building in-memory Record Sets, but doesn't need a database.
- **Evolution:** relationships between tables become calls between modules.

## Diagram

```mermaid
classDiagram
    class Client
    class Contracts {
        +PayoffCents(contractId) long
    }
    class Installments {
        +OutstandingBalanceCents(contractId) long
    }
    class RecordSet
    class TableDataGateway
    Client --> Contracts
    Contracts --> Installments
    Contracts --> RecordSet
    Installments --> RecordSet
    TableDataGateway --> RecordSet
```

Each table has a module (`Contracts`, `Installments`) that operates on a `RecordSet` loaded by a table gateway.

## Example

An `Installments` module calculates a contract's outstanding balance from the loaded set of installments, and the `Contracts` module uses that balance to calculate the early payoff amount (the discount is illustrative).

```csharp
public class Installments
{
    private readonly DataTable table;
    public Installments(DataTable table) { this.table = table; }

    // Sums the contract's unpaid installments, in cents.
    public long OutstandingBalanceCents(int contractId) =>
        table.AsEnumerable()
             .Where(r => r.Field<int>("ContractId") == contractId
                      && r.IsNull("PaidAt"))
             .Sum(r => r.Field<long>("AmountCents"));
}

public class Contracts
{
    private readonly DataTable table;
    private readonly Installments installments;
    public Contracts(DataTable table, Installments installments) { this.table = table; this.installments = installments; }

    public long PayoffCents(int contractId)
    {
        var row = table.AsEnumerable().Single(r => r.Field<int>("Id") == contractId);
        var balance = installments.OutstandingBalanceCents(contractId);
        var discount = row.Field<decimal>("EarlyPayoffDiscount");   // rate, for example 0.05m
        return (long)Math.Round(balance * (1m - discount));
    }
}
```

## Related patterns

- [Transaction Script](/design/poeaa/domain-logic/transaction-script) — organizes by request instead of by table.
- [Domain Model](/design/poeaa/domain-logic/domain-model) — one object per record, instead of one per table.
- [Record Set](/design/poeaa/base/record-set) — in-memory tabular structure that Table Module operates on.
- [Table Data Gateway](/design/poeaa/data-source-architectural/table-data-gateway) — loads the table data for the module.
- [Service Layer](/design/poeaa/domain-logic/service-layer) — can serve as the boundary over the modules.

## Reference

- [Pattern page in Fowler's catalog](https://martinfowler.com/eaaCatalog/tableModule.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
