---
title: Coarse-Grained Lock
pattern_slug: coarse-grained-lock
category: Offline Concurrency
tags:
  - Consistency
  - Simplicity
source: https://martinfowler.com/eaaCatalog/coarseGrainedLock.html
sidebar_label: "Coarse-Grained Lock"
---

# Coarse-Grained Lock

## Description

Coarse-Grained Lock locks a set of related objects with a single lock. Instead of acquiring a lock for each object in an aggregate (for example, an order and all its line items), the application protects the whole group through a single point, usually the aggregate root.

For optimistic locking, this is usually done with a shared version object: all members of the group reference the same version number, and changing any of them increments that version. For pessimistic locking, locking the root implies locking the whole group. One variation is the Root Lock, where each child object navigates up to the root to obtain the lock.

The pattern aligns the lock granularity with the model's consistency boundary, reducing the number of locks and eliminating the chance of locking only part of an aggregate.

## Problems it solves

- Acquiring and managing many individual locks is costly and error-prone.
- Locking only part of an aggregate leaves the group in an inconsistent state (e.g., a line item changed by someone else while the order is being recalculated).
- Forgetting to lock one member of the group breaks the aggregate's invariant.

## When to use

- When objects are always edited together, such as an aggregate or a set of entities with shared invariants.
- When the cost of managing per-object locks is high.
- Together with Optimistic or Pessimistic Offline Lock to align locking with the aggregate.

### When to avoid

- When objects in the group are frequently edited independently; the coarse lock creates unnecessary contention.
- When the group is very large, and locking all of it prevents legitimate parallel work.
- When the model has no clear aggregate boundary.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| A single lock protects the whole group | Reduces concurrency: independent edits now conflict |
| Preserves aggregate invariants | A poorly defined boundary causes contention or protection gaps |
| Fewer locks to acquire and release | Requires all members to point to the root or shared version |
| Simpler application code | Updates to children must increment the root's version |

- **Consistency:** the lock granularity matches the aggregate's transactional boundary.
- **Performance:** fewer locks per operation, but a higher chance of conflict.
- **Modeling:** reinforces the discipline of defining clear aggregates.

## Diagram

```mermaid
classDiagram
    class Version {
        +id
        +value
    }
    class Order {
        +id
    }
    class OrderLine {
        +id
    }
    class Payment {
        +id
    }
    Order --> Version : shares
    OrderLine --> Version : shares
    Payment --> Version : shares
    Order "1" --> "*" OrderLine
    Order "1" --> "*" Payment
```

`Order`, `OrderLine`, and `Payment` reference the same `Version` object. Any change to one of them increments that version, and the conflict is detected for the whole group.

## Example

In an order with line items, changing a line item while someone else changes the total should conflict. Everyone uses the version of the `Order` root.

```sql
-- Line items and order share the order's version
UPDATE order_line SET qty = 5 WHERE id = 3;

UPDATE orders
   SET version = version + 1
 WHERE id = 10 AND version = 4;  -- 0 rows => conflict on the aggregate
```

```java
@Entity
class Order {
    @Version long version;

    @OneToMany(cascade = CascadeType.ALL)
    List<OrderLine> lines;
}

// In JPA, the root's version can be incremented when children change:
// entityManager.lock(order, LockModeType.OPTIMISTIC_FORCE_INCREMENT);
```

## Related patterns

- [Optimistic Offline Lock](/application/poeaa/offline-concurrency/optimistic-offline-lock) — Coarse-Grained Lock is often implemented as a version shared by the group.
- [Pessimistic Offline Lock](/application/poeaa/offline-concurrency/pessimistic-offline-lock) — locking the root implies locking the whole group.
- [Implicit Lock](/application/poeaa/offline-concurrency/implicit-lock) — automates acquiring the group's lock.
- [Unit of Work](/application/poeaa/object-relational-behavioral/unit-of-work) — responsible for writing the group of changed objects and incrementing the shared version.
- [Layer Supertype](/application/poeaa/base/layer-supertype) — hosts the common logic for accessing the root or shared version.

## Reference

- [Pattern page in Fowler's catalog](https://martinfowler.com/eaaCatalog/coarseGrainedLock.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
