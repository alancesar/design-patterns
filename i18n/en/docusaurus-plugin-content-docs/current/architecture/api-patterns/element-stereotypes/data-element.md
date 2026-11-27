---
title: Data Element
pattern_slug: data-element
category: Element Stereotypes
tags:
  - Decoupling
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Data Element"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/element-stereotypes/data-element.mdx';

# Data Element

## Description

The Data Element pattern defines a dedicated vocabulary of data elements for an API's request and response messages, wrapping and mapping the relevant parts of the provider's internal model without exposing its internal definitions. It is the most general of the element stereotypes: it describes the role of any parameter that carries domain or application information.

A Data Element can be a plain [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter), an [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) or a leaf of a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree); richer ones usually contain an [Id Element](/architecture/api-patterns/element-stereotypes/id-element) and several domain attributes. Several instances transferred together form an element collection. The message schema should be explicit and documented, and the mapping between the internal model (tables, entities, aggregates) and this public vocabulary is the provider's responsibility, so the client never needs to know how data is stored.

In DDD terms, the vocabulary of Data Elements works as a Published Language that shields aggregates, entities and value objects in the domain layer.

Two variants deserve mention: the **Entity Element**, which contains an identifier and hints at an object life cycle in the Published Language, and the **Query Parameter**, which does not represent entities of the API but an expression used to select a subset of them in a [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation). Elements can be strongly typed, with a rich schema, or generic, such as lists of key-value pairs, which are flexible but weakly validated. DDD patterns should not be translated one to one into the API; the provider should design its public language to minimize undesired coupling.

## Problems it solves

- Leaking of internal tables, columns or classes into the API contract
- Coupling between client and provider through free-form strings interpreted by implicit convention
- Difficulty evolving the internal model without breaking consumers
- Lack of a common vocabulary that makes the API understandable and documentable

## When to use

- When defining the messages of any operation that exchanges business information
- When the internal model changes at a different pace than the public contract
- When several clients with different needs consume the same API
- When you want a contract described by a schema that is testable and versionable

## When to avoid

- For trivial messages with a single value, where an atomic parameter is enough
- When client and provider share the same model and team and the extra mapping only adds ceremony
- To expose remote object references or stubs, which make the communication stateful
- When the public vocabulary would mirror the internal model field by field, with no isolation gain

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Decouples the API contract from the internal data model | Requires mapping code between the internal model and the public vocabulary |
| Explicit vocabulary that eases documentation and understanding | More elements to document, test and maintain as the API evolves |
| Freedom to refactor the internal model without breaking clients | Deciding what to expose is hard and affects future compatibility |
| Verifiable schemas improve interoperability | Too much flexibility (optional fields, variations) raises testing costs |

- **Functionality versus simplicity:** the more data and behavior exposed, the more usage options and the more risk of inconsistency and lengthy documentation.
- **Security and privacy:** exposing less reduces the attack surface but may require extra configuration.
- **Maintenance versus flexibility:** each new field needs compatibility analysis and support for as long as clients use it.
- **Names and types:** choose business-domain names, not column names, and monetary values as integer cents.
- **Granularity:** a rich, deeply structured language is expressive but hard to secure and maintain; a simple one is easy to teach but may not capture domain specifics. If in doubt, leave the element out.

## Diagram

<Diagram />

The client only exchanges Data Elements with the endpoint; the mapping translates this vocabulary into the internal model, which stays invisible.

## Example

The fintech's accounts API returns an account as a set of domain Data Elements, not the columns of the `tb_acct` table. Monetary values are integer cents.

```http
GET /accounts/acc_7f3a91 HTTP/1.1
Accept: application/json
```

```json
{
  "id": "acc_7f3a91",
  "holderName": "Maria Souza",
  "status": "ACTIVE",
  "balance": { "amountCents": 1523050, "currency": "BRL" },
  "openedOn": "2024-03-12"
}
```

The provider can rename columns, split tables or switch databases without changing this contract.

## Related patterns

- [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) and [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — structures that give Data Elements their shape
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — specialized Data Element that identifies the other entities
- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — complements the data with information that explains its meaning
- [Published Language](/design/ddd/context-mapping/published-language) — the shared public vocabulary, from the DDD perspective
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — transfer object that carries Data Elements between layers
- [Anti-Corruption Layer](/architecture/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) — protects your own model from a third party's, while the Data Element protects the provider's model from its clients

## Reference

- [Patterns for API Design, chapter 6: Data Element](https://api-patterns.org/)
