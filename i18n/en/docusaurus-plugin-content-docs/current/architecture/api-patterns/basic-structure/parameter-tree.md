---
title: Parameter Tree
pattern_slug: parameter-tree
category: Basic Structure
tags:
  - Shared Understanding
  - Performance
source: https://api-patterns.org/
sidebar_label: "Parameter Tree"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/basic-structure/parameter-tree.mdx';

# Parameter Tree

## Description

The Parameter Tree pattern defines a hierarchical structure with a root node and one or more child nodes, each being an atomic parameter, a list of atomic parameters or another tree, to express containment relationships in API messages. Each node is identified locally by name and/or position and can have a cardinality of exactly one, zero or one, one or more, or zero or more.

The definition is recursive. In HTTP APIs, the tree appears as nested JSON objects, and multi-valued nodes as arrays of objects. It is the natural choice when the domain model is hierarchical (an order with items, a contract with installments) or when additional data, such as security information, must be structurally separated from business data, as in a [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation). A tree is costlier to process than an atom, but is usually more efficient than several simple messages when the hierarchy is deep.

## Problems it solves

- Representing containment and association relationships (1:1, 1:N, N:M) in a single message
- Avoiding the flattening of rich data into plain, hard-to-read lists
- Structurally separating metadata from business data
- Reducing the number of calls needed to transfer a whole structure

## When to use

- To exchange domain aggregates, such as a credit contract with its installments
- When the consumer needs the complete structure in a single response
- When it helps to group parts of the message with distinct roles (data, context, links)

## When to avoid

- When a flat list is enough: use an [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list)
- When the structure is very deep or large, which wastes bandwidth and stresses serializers
- When the nested part can be fetched on demand through a [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder)
- When format coupling should be kept low: every exposed level becomes part of the contract

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Expresses hierarchies and associations clearly | More complex to process and validate than atoms |
| Fewer messages than several simple calls | May carry unnecessary data and levels if optionality is not defined |
| Separates business data from context and metadata | Shares internal structure and increases format coupling |
| Maps well to JSON, Protocol Buffers and GraphQL | Trees in query strings have limited, non-portable support |

- **Depth:** keep few levels; each extra level weighs on the contract and on the payload.
- **Optionality:** state explicitly what is optional so that the provider can omit nodes.
- **Recursion:** recursive definitions are elegant but can produce huge payloads and break serializers.
- **Evolution:** adding optional nodes is compatible; changing the shape of an existing node is not.

## Diagram

<Diagram />

The root mixes an atom, a list and a collection of subtrees.

## Example

Response with a personal credit contract of the fintech: a root object with atoms, a nested record and a collection of installments. Values in cents, illustrative rate.

```http
GET /loan-contracts/loan-91c2 HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "contractId": "loan-91c2",
  "principalCents": 1000000,
  "monthlyRate": "0.0200",
  "borrower": {
    "accountId": "acc-7f3a",
    "name": "Maria Souza"
  },
  "installments": [
    { "number": 1, "dueDate": "2026-12-10", "amountCents": 120000 },
    { "number": 2, "dueDate": "2027-01-10", "amountCents": 118000 }
  ]
}
```

## Related patterns

- [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) — the leaves of the tree
- [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) — a flat tree is equivalent to a list
- [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest) — groups several trees at the top level
- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) — embedded entities often arrive as trees
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — the hierarchy separates data from context
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — a DTO is the kind of object that usually materializes a tree in code
- [Aggregate](/design/ddd/building-blocks/aggregate) — trees often mirror the shape of a domain aggregate

## Reference

- [Patterns for API Design, chapter 4: Parameter Tree](https://api-patterns.org/)
