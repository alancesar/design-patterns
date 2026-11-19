---
title: Information Holder Resource
pattern_slug: information-holder-resource
category: Endpoint Roles
tags:
  - Shared Understanding
  - Decoupling
source: https://api-patterns.org/
sidebar_label: "Information Holder Resource"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/information-holder-resource.mdx';

# Information Holder Resource

## Description

The Information Holder Resource pattern exposes an endpoint that represents an identifiable data entity and offers operations to create, read and maintain it, hiding how it is stored.

The endpoint is shaped around a domain concept (account, card, loan contract) and treats data as the center of the contract. Clients query and change the information through read and write operations, while the internal database structure, tables and supporting services remain private. The entity gets a stable identifier, used to reference it in other messages.

Each operation of the resource has a single responsibility: creating the entity, retrieving it (including filtered searches) or transitioning it, which covers updating and removing. The provider defines pre- and postconditions and invariants, decides whether the component is stateful or stateless, and coordinates concurrent access (optimistic or pessimistic locking, strict or eventual consistency).

The pattern is the generic role for data-centric endpoints and has five refinements. Three differ in mutability, relationships and lifespan of the data: [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder), [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) and [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder). The [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) holds only references to other endpoints, and the [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) holds temporary shared data that belongs to the clients.

## Problems it solves

- Exposing domain data to several clients without coupling them to the physical database schema
- Giving each business entity an identifiable access point that other resources can reference
- Preventing each client from reimplementing access, validation and consistency rules over the same data
- Letting the storage structure evolve without forcing changes on consumers
- Avoiding both extremes: hiding all data behind processing operations (many small calls or duplicated data) and exposing the database directly (total coupling to the schema and security risks)

## When to use

- The client's main activity is querying or maintaining entities, such as accounts, cards and contracts
- Data must be shared among several clients with a consistent view
- Each entity has a clear identity that can become part of the URL
- The API should be easy to understand because it mirrors the domain vocabulary

## When to avoid

- When the need is to execute a business activity: prefer a [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource)
- When the API merely mirrors database tables, exposing internal details and creating strong coupling
- When the endpoint mixes data with very different life cycles, which calls for splitting it into more specific roles
- When consistency across several entities requires a transaction that the client could not coordinate

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Contract that is easy to understand, aligned with the domain vocabulary | Risk of reflecting the internal model and leaking the database schema |
| Storage hidden behind a stable interface | The client may need several calls to assemble a full view |
| Shared data with a single point of truth | Changing the entity structure affects all consumers |
| URLs and identifiers make caching and identification easier | Exposing too much write access invites violations of domain invariants |

- **Granularity:** decide the size of the exposed entity; too small causes chattiness, too large carries data the client does not use.
- **Specialization:** classify the endpoint as operational, master or reference to settle change frequency, caching and who may write.
- **Identity:** use opaque, stable identifiers, without exposing internal database keys.
- **Evolution:** version and evolve the resource structure carefully, since the data is shared.
- **Coupling:** a data-centric design tends to push processing onto consumers and produce CRUD operations that raise semantic and operational coupling; some treat the pure data resource as an anti-pattern ("entity service"), so use it consciously and hide certain data behind a Processing Resource.
- **Security and consistency:** not every client should read or write the same way (API keys, RBAC/ABAC), and you must decide how to handle stale data, caching and temporary unavailability.
- **Many small resources:** several fine-grained Information Holders require many calls and spread responsibility for data quality.

## Diagram

<Diagram />

Several clients access the same entity through the contract; the storage and internal keys stay hidden.

## Example

The fintech's accounts API treats the digital account as an Information Holder Resource. The client reads and updates the account by identifier, without knowing how balances and entries are stored.

```http
GET /accounts/acc-1001 HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "acc-1001",
  "holderName": "Maria Souza",
  "status": "ACTIVE",
  "balance": { "cents": 250000, "currency": "BRL" }
}
```

```http
PATCH /accounts/acc-1001 HTTP/1.1
Content-Type: application/json

{ "notificationEmail": "maria@example.com" }
```

The balance is a monetary value in whole cents, never a floating-point number. Balance changes are not made by direct writes: they result from new ledger entries (`LedgerEntry`) generated by other operations.

## Related patterns

- [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) — the complementary role, focused on actions instead of data
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) — specialization for short-lived, fast-changing data
- [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — specialization for long-lived data referenced by many
- [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) — specialization for stable, read-only data
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — holds only references to other resources
- [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) — shared space for temporary data owned by the clients
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) and [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) — the typical operations, which model CRUD semantics
- [Repository](/design/poeaa/object-relational-metadata-mapping/repository) — the in-process counterpart: the Information Holder Resource is its API equivalent
- [Aggregate](/design/ddd/building-blocks/aggregate) — often the implementation basis, with no one-to-one correspondence
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — the identifier used to address the entity
- [Entity](/design/ddd/building-blocks/entity) — the domain concept usually exposed by this kind of endpoint

## Reference

- [Patterns for API Design, chapter 5: Information Holder Resource](https://api-patterns.org/)
