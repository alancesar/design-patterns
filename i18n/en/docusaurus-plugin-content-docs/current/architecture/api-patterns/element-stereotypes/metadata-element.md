---
title: Metadata Element
pattern_slug: metadata-element
category: Element Stereotypes
tags:
  - Shared Understanding
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Metadata Element"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/element-stereotypes/metadata-element.mdx';

# Metadata Element

## Description

The Metadata Element pattern adds to an API's messages elements that explain and enrich the other ones, so the receiver interprets the content correctly without hardcoding assumptions about the meaning of the data. The currency of a value, the total number of items in a list, the version of a document or the author of a change are typical examples.

Many Metadata Elements are simple [Atomic Parameters](/architecture/api-patterns/basic-structure/atomic-parameter), but they can also form a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree). A flexible but error-prone approach is to use text key-value pairs that the receiver converts. They become part of the [API Description](/architecture/api-patterns/documentation/api-description) and must be kept up to date; it helps to define the expected freshness (for example, when a counter expires) and whether the value is immutable.

Three variants exist: **control** metadata (identifiers, flags, filters, links, security information, checksums) steers processing; **aggregated** metadata summarizes or analyzes other elements (counters, statistics, pagination totals); and **provenance** metadata reveals the origin of the data (author, source system, creation date, version).

A single element can realize more than one variant: a region code, for example, gives provenance and also steers processing. HTTP `ETag` values are control and provenance metadata (see [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request)). An alternative to including metadata in every message is a dedicated operation that returns it for an element identified by an [Id Element](/architecture/api-patterns/element-stereotypes/id-element) or [Link Element](/architecture/api-patterns/element-stereotypes/link-element).

## Problems it solves

- Receivers that must guess the unit, currency or format of a value
- Ambiguity between an absent, empty and not-applicable field
- Clients with interpretation rules hardcoded that break when the API evolves
- Lack of traceability about the origin and version of received data

## When to use

- When a value only makes sense with a qualifier, such as currency, unit or time zone
- When the client needs totals, counters or indicators to make decisions at runtime
- When the origin, version or date of a piece of data matters for auditing
- When you want to reduce coupling to conventions written only in the documentation

## When to avoid

- When the information is static and already complete and accessible in the contract documentation
- In message-size-sensitive APIs, where every extra byte has a relevant cost
- When the provider cannot keep the metadata correct and current, since wrong metadata is worse than none
- When the metadata exposes internal details the client should not know

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Removes syntactic and semantic ambiguities between the parties | Increases message size and processing cost |
| Makes shared knowledge explicit at runtime | Requires keeping the metadata correct and fresh as the API evolves |
| Lets the client make dynamic decisions from the received data | More elements to test, document and version |
| Eases auditing and origin traceability | Generic key-value pairs are flexible but fragile and untyped |

- **Interoperability:** explicit qualifiers, such as the currency next to the value, prevent wrong readings.
- **Coupling:** knowledge moves from the static contract into the message content, which can either increase or reduce coupling.
- **Efficiency:** include only the metadata the receiver really uses.
- **Freshness:** define when each piece of metadata stops being valid, such as pagination counters.
- **Dependency:** the client should depend on metadata only when necessary; otherwise treat it as an optional convenience, and the API should work without it. Control metadata, such as pagination links, creates a dependency as soon as it is introduced.
- **Excess:** too much metadata bloats the interface and makes evolution and versioning harder.

## Diagram

<Diagram />

The three kinds of Metadata Elements travel with the Data Elements in the same message and explain their content.

## Example

The fintech's account statement returns the ledger entries and, alongside them, metadata describing the result. Values are integer cents.

```json
{
  "entries": [
    { "id": "le_9001", "type": "PIX_IN", "amountCents": 25000 },
    { "id": "le_9002", "type": "BOLETO_OUT", "amountCents": -8990 }
  ],
  "meta": {
    "currency": "BRL",
    "totalCount": 137,
    "nextPage": "/accounts/acc_7f3a91/entries?cursor=c2",
    "generatedAt": "2026-11-17T09:30:00Z",
    "source": "ledger-service"
  }
}
```

With `currency` the client does not assume the currency, `totalCount` and `nextPage` guide navigation, and `generatedAt` and `source` give traceability.

## Related patterns

- [Data Element](/architecture/api-patterns/element-stereotypes/data-element) — the data the metadata explains
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) and [Link Element](/architecture/api-patterns/element-stereotypes/link-element) — form control metadata
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — uses counters and cursors as aggregated and control metadata
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — groups context metadata into a dedicated block of the message
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — security metadata that identifies the client
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — metadata that indicates the contract version
- [Envelope Wrapper](/architecture/eip/message-transformation/envelope-wrapper) — wraps the payload with headers, at a different message level
- [Format Indicator](/architecture/eip/message-construction/format-indicator) — metadata that declares the content format

## Reference

- [Patterns for API Design, chapter 6: Metadata Element](https://api-patterns.org/)
