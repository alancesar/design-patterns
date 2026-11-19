---
title: Data Transfer Resource
pattern_slug: data-transfer-resource
category: Endpoint Roles
tags:
  - Decoupling
  - Performance
source: https://api-patterns.org/
sidebar_label: "Data Transfer Resource"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/data-transfer-resource.mdx';

# Data Transfer Resource

## Description

The Data Transfer Resource pattern exposes a shared endpoint that serves as an intermediate area for exchanging data between partners that do not need to be available at the same time or to know each other directly.

It is a refinement of the [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) that works as a shared blackboard: one participant deposits the data in the resource and the others pick it up later, at their own pace. The resource has a single, global address and offers at least one state creation operation and one retrieval operation; any authorized client that knows the address can also read, update and delete. The partners are decoupled in time (they need not be active together) and in location (they only need to reach the resource), and can even communicate when one of them sits behind a firewall or runs in a browser.

Data ownership should stay with the clients, not the provider. There are three variants, depending on access patterns and resource lifetime: the **Relay Resource**, with a single writer and a single reader, where ownership moves from writer to reader; the **Published Resource**, with one writer and a large, unpredictable number of readers, sometimes years later, where the writer decides how long the resource stays available; and the **Conversation Resource**, where several clients read, write and eventually delete, and any participant owns the resource. Clients agree on the address in advance, discover it through a [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource), or the first to publish tells the others.

## Problems it solves

- Partners that are not available at the same time and still need to exchange data
- Large payloads that overload control messages and slow down calls
- Direct coupling between whoever produces and whoever consumes the data
- The need to deliver the same content to recipients who fetch it at different times, including after the data was already sent and when the number of recipients is unknown
- Participants that cannot talk to each other directly (behind NAT or firewalls, in browsers) or can only use a basic HTTP client, with no messaging middleware to install

## When to use

- Sender and receiver work asynchronously or at different times
- The volume is too large to travel in an ordinary call
- Identity, location and availability of the partners must be decoupled
- The data is temporary and can be discarded after consumption

## When to avoid

- When communication needs an immediate, synchronous response
- When the volume is small and a direct call is simpler
- When the data is sensitive and the intermediate storage cannot be properly protected
- When intermediate retention creates a risk of piling up ownerless data or of leaks
- When a messaging middleware with guaranteed delivery is already operated and available to all participants

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Partners decoupled in time and identity | Higher latency and less predictable delivery |
| Support for large volumes outside control messages | The provider holds temporary data and must manage space and deadlines |
| Each party acts at its own pace | Needs conventions about who removes the data and when |
| Reusable for several recipients | Intermediate storage widens the security surface |

- **Security:** the transfer resource requires authorization and, generally, temporary links and encryption of data at rest.
- **Retention:** define an expiry period to avoid piling up forgotten data.
- **Notification:** agree on how the receiver learns that data is there (polling, event or callback).
- **Ownership:** define who is responsible for the validity and cleanup of the content (sender, receiver or the provider bearing the storage); prefer client ownership.
- **Reliability:** HTTP does not guarantee delivery, but writing with PUT and reading with GET is idempotent, so the client retries until it works, with no need to remove duplicates.
- **Delivery visibility:** the sender does not know whether anyone read it; the resource can expose access metadata (how many reads), which also helps clean up unused resources.
- **Latency:** there are two hops instead of one; the pattern favors moving data across many participants and over time, not the speed of a single transfer.
- **Integrity:** include the content size and hash so the receiver can validate what it got.

## Diagram

<Diagram />

The sender writes to the intermediate resource, the receiver picks it up later, and the two never need to be connected at the same time.

## Example

The fintech receives fixed-income investment statements from a custodian partner, as large files sent overnight. The partner deposits the file; the reconciliation service reads it when it is ready.

```http
PUT /transfers/fixed-income-statement-2026-11-16 HTTP/1.1
Content-Type: text/csv
Content-Length: 5242880

... statement rows, with amounts in cents ...
```

```http
HTTP/1.1 201 Created
Location: /transfers/fixed-income-statement-2026-11-16
```

The `PUT` is idempotent, so the partner can repeat it if the connection drops. Later, the reconciliation service does `GET /transfers/fixed-income-statement-2026-11-16` and, after processing, a `DELETE` on the same address. Here the resource works as a Relay Resource: one writer, one reader, and ownership passes to the reader. The resource expires on its own after 24 hours if nobody removes it.

## Related patterns

- [File Transfer](/architecture/eip/integration-styles/file-transfer) — an integration style based on files; here the file passes through an API resource with its own life cycle
- [Shared Database](/architecture/microservices/service-collaboration/shared-database) — also exchanges data through a common store, but exposes the schema; the transfer resource hides it behind a contract
- [Claim Check](/architecture/cloud-design-patterns/messaging/claim-check) — sends only a reference in the message and keeps the large content aside
- [Valet Key](/architecture/cloud-design-patterns/security-and-access/valet-key) — gives the client temporary, restricted access directly to the storage
- [Asynchronous Request-Reply](/architecture/cloud-design-patterns/messaging/asynchronous-request-reply) — another way to handle work that does not finish in the same call
- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the transfer resource is a data-centric resource type, but a temporary one
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — helps clients discover the address of the shared resource
- [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) and [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — the two minimal operations of the resource

## Reference

- [Patterns for API Design, chapter 5: Data Transfer Resource](https://api-patterns.org/)
