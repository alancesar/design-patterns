---
title: Reference Data Holder
pattern_slug: reference-data-holder
category: Endpoint Roles
tags:
  - Performance
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Reference Data Holder"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/reference-data-holder.mdx';

# Reference Data Holder

## Description

The Reference Data Holder pattern exposes an endpoint for reference data, stable and read-oriented, that serves as shared lookup and rarely changes.

Reference data consists of supporting tables used by many clients: list of banks, currency codes, Pix key types, expense categories, holidays. The endpoint offers read operations only, with no create, update or delete through the API, and changes happen outside the contract, directly on backend assets or through a separate administration API. The client may download the whole set (to keep a local copy), filter it (for example, to autocomplete a field) or look up a single item (for example, to validate a value). Because values change little, clients can cache them for long periods and even embed local copies.

Without a single point of reference, the temptation is to copy the values into every client, which violates the DRY principle: when the data changes, every client is affected and some may be impossible to update. The implementation need not be a relational database; a file, a key-value store or a CDN may be enough. The challenge is deciding how occasional changes reach clients, which involves cache expiry times, dataset versions and update notices.

## Problems it solves

- Many clients repeatedly querying the same stable lists, generating unnecessary traffic
- Local copies of supporting tables diverging across systems
- Lack of a simple, official source for shared codes and catalogs
- The cost of accessing values that almost never change

## When to use

- Data is small or moderate in size, stable and read by many clients
- Absolute freshness is not critical, and slight staleness is acceptable
- Content can be cached by the client or by intermediaries
- Everyone must be guaranteed to use the same codes and labels

## When to avoid

- When data changes often and must always be current: use an [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder)
- When data consists of core entities with identity and controlled maintenance: use a [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder)
- When the set is huge and clients need only a piece: consider pagination or filters
- When a stale value could cause immediate financial or regulatory harm

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Efficient caching reduces traffic and latency | Clients may use stale values after a change |
| Simple contract, generally read-only | Propagating a change requires an invalidation or versioning strategy |
| Single, official source for shared codes | A wrong change affects all consumers at once |
| Low conflict risk, with no concurrent writes | Large sets are heavy if delivered whole |

- **Caching:** declare explicit expiry times and use validators such as ETag to revalidate without downloading everything again.
- **Dataset version:** expose a version identifier for the list so the client knows when to refresh its copy.
- **Compatibility:** adding entries is safe; removing or renaming codes may break dependents.
- **Size:** offer filters or pagination when the list grows.
- **DRY:** the endpoint avoids repeating the reference in each client, at the cost of depending on a remote API that must be developed, documented and maintained.
- **Hidden optimization:** since the data sits behind the API, the provider can introduce proxies, caches and read replicas without the client noticing.
- **Cost of a standalone endpoint:** if it brings more work than value, merge the data into an existing Master Data Holder, as an API refactoring.

## Diagram

<Diagram />

Clients read and cache the reference list; only an administrative process, outside the contract, changes it.

## Example

The fintech publishes the list of institutions taking part in Pix. The apps cache it and revalidate it with `ETag`.

```http
GET /reference/pix-participants HTTP/1.1
Accept: application/json
If-None-Match: "v42"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
ETag: "v43"
Cache-Control: max-age=86400

{
  "version": 43,
  "items": [
    { "code": "0001", "name": "Banco Exemplo" },
    { "code": "0002", "name": "Instituicao de Pagamento Modelo" }
  ]
}
```

If nothing has changed since the stored version, the server answers `304 Not Modified` with no body. The names and codes above are fictional.

## Related patterns

- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the general role of which this is a specialization
- [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — central, long-lived data maintained in a controlled way
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) — data that changes all the time
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request) — revalidates the cached copy without downloading the content again
- [Cache-Aside](/architecture/cloud-design-patterns/data-management/cache-aside) — a consumer-side caching strategy that pairs well with reference data
- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) and [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — simple static data can be embedded, dispensing with the endpoint, or referenced by link
- [Value Object](/design/poeaa/base/value-object) — many reference items (currencies, codes) are values with no identity of their own

## Reference

- [Patterns for API Design, chapter 5: Reference Data Holder](https://api-patterns.org/)
