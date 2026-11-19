---
title: Master Data Holder
pattern_slug: master-data-holder
category: Endpoint Roles
tags:
  - Shared Understanding
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Master Data Holder"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/master-data-holder.mdx';

# Master Data Holder

## Description

The Master Data Holder pattern exposes an endpoint for master data, which is long-lived and widely referenced by other data, and offers careful access with clear maintenance rules to preserve its quality and consistency.

Master data describes the core entities of the business, such as customers, accounts and products. It survives many processes, changes slowly compared to operational data and is pointed to by many other records and systems. For this reason, maintenance is controlled: creating and changing requires validation, and removal is usually restricted or replaced by an inactive flag, so references do not break.

The endpoint must think about stable identity, versions and change propagation, since several clients depend on the same source of truth. Because this data is a valuable asset, an attractive target for attacks and often under the control of an external system or team, protection, auditing and compliance weigh more than for other kinds of data.

Updates can be coarse-grained, replacing most attributes (like a PUT), or partial, changing a few fields (like a PATCH). Removal is treated as a special kind of update: the data usually moves to an archived, immutable state, preserving the audit trail. Master data has many incoming references and may have outgoing ones; operational data references it, but not the other way around.

## Problems it solves

- Several systems keeping diverging copies of the same core business data
- Broken references when an important entity is changed or deleted carelessly
- Lack of a single, reliable place to query and maintain the identity of the main entities
- Changes to core data that propagate uncontrolled to whoever depends on them

## When to use

- Data is central, lasts for years and is referenced by many other resources
- A single source of truth about customers, accounts or products is needed
- Maintenance needs validation, auditing and explicit rules about who may change it
- Consumers tolerate changes being less frequent and more controlled

## When to avoid

- When data is transient and changes all the time: use an [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder)
- When data is just a stable lookup table: use a [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder)
- When each service should own its own model and local copies are acceptable
- When the governance cost outweighs the value of centralizing the source

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Single, consistent source about the core entities | Central point of dependency and potential change bottleneck |
| Stable references across systems and resources | Changing the structure affects many consumers at once |
| Quality ensured by validation and maintenance rules | Slower, more bureaucratic change process |
| Good caching candidate, since it changes slowly | Cached copies may go stale after a change |

- **Removal:** prefer archiving or deactivating to deleting, so no dangling references are left; if deletion is required by law, hide the data from consumers without destroying it, where regulation allows.
- **Contract design:** do not reduce the endpoint to CRUD over tables, which yields chatty, coupled APIs; start from aggregate roots, capabilities or business processes, and offer semantically rich operations (such as validate and archive).
- **External control:** master data management systems, sometimes outsourced, evolve at another pace and involve more parties; concentrating access in a single endpoint limits where that dependency appears.
- **Evolution:** structural changes require versioning and careful communication with consumers.
- **Ownership:** clearly define who owns the data and who may write.
- **Propagation:** consider publishing change events so consumers can update their copies.

## Diagram

<Diagram />

Several services reference and query the same master source, which concentrates validation and maintenance.

## Example

The fintech's customer registry is master data: accounts, cards and loan contracts point to it. Changes are validated and removal becomes deactivation.

```http
GET /customers/cus-9001 HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
ETag: "7"

{
  "id": "cus-9001",
  "legalName": "Maria Souza",
  "status": "ACTIVE",
  "accounts": ["acc-1001"]
}
```

```http
PATCH /customers/cus-9001 HTTP/1.1
If-Match: "7"
Content-Type: application/json

{ "status": "INACTIVE" }
```

The customer is never deleted: once deactivated, the contracts and ledger entries (`LedgerEntry`) that reference it remain valid for lookup and auditing.

## Related patterns

- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the general role of which this is a specialization
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) — the contrast: short-lived, fast-changing data
- [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) — stable, usually read-only data
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — the stable identifier that supports the references
- [Bounded Context](/design/ddd/model-in-practice/bounded-context) — defines who owns the model of the master data and where copies diverge
- [Aggregate](/design/ddd/building-blocks/aggregate) — the usual starting point for identifying the endpoint, instead of one entity per table
- [Domain Event](/architecture/microservices/service-collaboration/domain-event) — a way to propagate master data changes to consumers

## Reference

- [Patterns for API Design, chapter 5: Master Data Holder](https://api-patterns.org/)
