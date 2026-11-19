---
title: Atomic Parameter List
pattern_slug: atomic-parameter-list
category: Basic Structure
tags:
  - Simplicity
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Atomic Parameter List"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/basic-structure/atomic-parameter-list.mdx';

# Atomic Parameter List

## Description

The Atomic Parameter List pattern groups two or more related atomic parameters into a single cohesive representation element, keeping each item simple while making the link between them explicit in the API description and in the exchanged messages. Items are identified by position (index) or by a string key, and the list as a whole can get its own name when the receiver needs to process it as a unit.

Both the list and its elements can be optional or multi-valued, and this must appear as cardinality in the [API Description](/architecture/api-patterns/documentation/api-description). In JSON it is usually a flat object with no nested objects; in query strings, a comma-separated list. The pattern does not fit when the platform only allows one return value or one object per message, in which case a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) offers the needed expressiveness.

## Problems it solves

- A single parameter is not expressive enough for the data that must be transmitted
- Values with a strong semantic tie (such as street, postal code and city) appear loose and apparently unrelated
- The message needs parts that the client, provider or intermediaries want to tell apart
- Operation signatures with many loose parameters are hard to read and to evolve

## When to use

- To represent flat records, such as an address, a period or a value-and-currency pair
- For lists of wanted fields or filters in a query
- When the items are all of a basic type and nesting is not needed

## When to avoid

- When a single value is enough: use an [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter)
- When items have substructure or containment relationships: use a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree)
- When the platform or language does not accept multiple scalars in the same message

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| The relationship between the values is explicit and documented | Adding items changes the contract and may break clients |
| Each item stays simple to read and validate | Identifying by position is compact but fragile if the order changes |
| Maps well to query strings and flat objects | Expresses neither hierarchy nor collections of records |

- **Names and order:** use names from the domain vocabulary and a logical order, with close items grouped.
- **Position versus key:** string keys tolerate change better than indexes.
- **Cardinality:** document what is required, optional or multiple, and include examples of valid combinations.
- **Evolution:** new optional items are safer than changes of meaning.

## Diagram

<Diagram />

The named list gathers three atoms; one of them is optional.

## Example

Registering the billing address of a fintech account. The `billingAddress` object is a flat list of atoms.

```http
PUT /accounts/acc-7f3a/billing-address HTTP/1.1
Content-Type: application/json

{
  "street": "Rua das Flores, 100",
  "postalCode": "01310-100",
  "city": "Curitiba"
}
```

In a query, a comma-separated list tells which fields the client wants to receive:

```http
GET /accounts/acc-7f3a?fields=holderName,openedAt HTTP/1.1
```

This use is the essence of the [Wish List](/architecture/api-patterns/response-shaping/wish-list).

## Related patterns

- [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) — the building block that the list groups
- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — the alternative when nesting is needed
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) — a list of wanted fields is a direct application
- [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — uses lists of atoms to define the link target
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — in code, a flat record like this is usually modeled as a DTO

## Reference

- [Patterns for API Design, chapter 4: Atomic Parameter List](https://api-patterns.org/)
