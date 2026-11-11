---
title: Separate Ways
pattern_slug: separate-ways
category: Context Mapping
tags:
  - Team Autonomy
  - Simplicity
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Separate Ways"
---

# Separate Ways

## Description

In Separate Ways, two contexts explicitly decide not to integrate. Each solves its own problem independently, with its own model, even if that means duplicating some functionality or some data.

Integration has a permanent cost: coordinating changes, translating models, and maintaining contracts. When the expected benefit is small, it's cheaper to cut the tie. Evans notes that if two features have no significant dependency, they don't need to be in the same context or linked by an interface.

As a strategic decision, it should appear in the Context Map so that nobody tries to reconnect the contexts without weighing the cost.

## Problems it solves

- Integrations whose maintenance cost exceeds the value they deliver.
- Unnecessary organizational coupling between teams that could work on their own.
- Models forced to reconcile when they have no requirements in common.

## When to use

- The benefit of integrating is small or doubtful.
- The contexts serve distinct business needs, with no relevant flow between them.
- It's possible to duplicate a small piece of functionality or use a simple, local solution.

## When to avoid

- There are important business flows that depend on data from both contexts.
- Duplication creates inconsistencies that users notice or that violate business rules.
- Applicable to the Core Domain, where duplication can cost differentiation or revenue.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Full autonomy and no integration cost | Duplication of functionality and data |
| Each context evolves at its own pace | Possible inconsistency between the two views of the business |
| Simple models, no translation | Difficulty having a unified view, as in reports |
| Less coordination between teams | Future integration will be more expensive, if it becomes necessary |

- **Reversibility:** it's possible to backtrack and integrate later, but at a higher cost.
- **Visibility:** record the decision and the reason, so it isn't reversed out of inertia.

## Diagram

```mermaid
flowchart LR
    A["Cashback Context"] ~~~ B["Foreign Exchange Context"]
    A --- X["no integration"]
    B --- X
```

The two contexts coexist in the same ecosystem, but with no integration relationship whatsoever.

## Example

The fintech considers integrating its Cashback program with the Foreign Exchange context, so that purchases abroad earn cashback based on the day's exchange rate and Foreign Exchange offers better fees to customers who accumulate more cashback. The team concludes that the gain is marginal and the cost of maintaining the integration would be high. The contexts go their separate ways: Cashback computes the benefit on the amount in reais already posted to the invoice, without querying Foreign Exchange, and Foreign Exchange keeps its own list of customers with a promotional fee, even though that duplicates some data. The decision is recorded in the Context Map.

## Related patterns

- [Context Map](/design/ddd/context-mapping/context-map) — where the decision should be recorded.
- [Bounded Context](/design/ddd/model-in-practice/bounded-context) — the boundary that makes it possible to part ways.
- [Shared Kernel](/design/ddd/context-mapping/shared-kernel) — the opposite extreme, with strong sharing.
- [Partnership](/design/ddd/context-mapping/partnership) — the opposite extreme, with close cooperation.
- [Conformist](/design/ddd/context-mapping/conformist) — an alternative when integration is necessary but translating isn't worth it.
- [Decompose by Subdomain](/architecture/microservices/service-boundaries/decompose-by-subdomain) — independent subdomains favor separation.

## Reference

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003), ch. 14
- [DDD Crew: Context Mapping](https://github.com/ddd-crew/context-mapping)
