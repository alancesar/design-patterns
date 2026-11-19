---
title: Frontend Integration
pattern_slug: frontend-integration
category: Foundations
tags:
  - Decoupling
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Frontend Integration"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/foundations/frontend-integration.mdx';

# Frontend Integration

## Description

The Frontend Integration pattern exposes the services of a distributed application's backend to one or more frontends through a message-based remote API. It is the API that connects the user interface, physically separated from business logic and storage, to the processing and data it needs to show or change.

The consumer of this API is always a client that serves people: a mobile app, a web application or the frontend of another system. The natural entry point in the backend is the business logic layer, which already concentrates access control, transactions and rules. In practice it is usually a resource API over HTTP, but gRPC, WebSockets and GraphQL also fit. The API can be general-purpose, serving every client, or specialized by client type, as in Backends for Frontends.

After choosing this type of integration, you still need to decide the API's visibility (public, community or internal), compose the messages, define endpoint roles, a versioning strategy and the contract description.

## Problems it solves

- Populating and updating the user interface with processing results, searches and entity details that live on the server
- Letting the frontend trigger activities in the backend or send data to it
- Keeping the interface independent of business logic and storage, which change at different paces
- Giving clients of different kinds (mobile, web, partners) a stable access contract

## When to use

- When a mobile or web app needs to query balance, statements or start a Pix in a remote backend
- When the interface and the backend are deployed and evolve separately
- When several frontends share the same server capabilities
- When messages need to be designed for the user experience, with fewer round trips and responses shaped to the screen

## When to avoid

- To integrate two backend systems with each other: use [Backend Integration](/architecture/api-patterns/foundations/backend-integration), whose protocol and message structure needs differ
- When the interface runs in the same process as the logic and there is no network boundary
- When one API would try to serve frontends and backends at once, forcing compromises or options that complicate its use

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Interface decoupled from business logic and storage | Every call crosses the network, with latency and partial failures |
| Clear contract between whoever builds the screen and whoever builds the server | The contract must be versioned and documented carefully |
| Messages can be shaped to the needs of the experience | Several per-client specializations multiply what must be maintained |
| The same capabilities are reused by several frontends | A generic API may serve every client poorly |

- **Visibility:** the same integration can be public, community or internal; the choice changes security and stability demands.
- **Technology:** HTTP is the natural choice, while GraphQL promises to reduce over- and under-fetching, at the cost of another surface to operate.
- **General or specialized:** a single API simplifies maintenance; one per client type brings the response closer to what each screen needs.

## Diagram

<Diagram />

The frontend never touches the logic or the data directly: everything goes through the remote API exposed by the backend.

## Example

The fintech's app shows the account balance and statement and lets the user create a Pix charge. The messages are designed for the screen: the balance arrives ready, with `Money` in integer cents, never as a floating-point number.

```http
GET /accounts/acc-7781/overview HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "accountId": "acc-7781",
  "balance": { "amountCents": 125090, "currency": "BRL" },
  "recentEntries": [
    { "id": "le-9001", "description": "Pix recebido", "amountCents": 5000, "currency": "BRL" },
    { "id": "le-9000", "description": "Boleto pago", "amountCents": -23000, "currency": "BRL" }
  ]
}
```

```http
POST /accounts/acc-7781/pix-charges HTTP/1.1
Content-Type: application/json

{ "amountCents": 5000, "currency": "BRL", "description": "Aluguel de novembro" }

HTTP/1.1 201 Created
Location: /pix-charges/pc-3310
```

A single overview call keeps the app from assembling the screen with several separate requests.

## Related patterns

- [Backend Integration](/architecture/api-patterns/foundations/backend-integration) — the other integration type, between backends instead of between interface and server
- [Public API](/architecture/api-patterns/foundations/public-api), [Community API](/architecture/api-patterns/foundations/community-api) and [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) — the visibilities the frontend API can take
- [Backends for Frontends](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) — specializes the API per client type; it is one way to organize Frontend Integration
- [Remote Facade](/design/poeaa/distribution/remote-facade) — a coarse-grained facade that often backs this kind of API
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) and [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — let the client shape the response to the screen
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — supports contract evolution without breaking installed clients

## Reference

- [Patterns for API Design, chapter 4: Frontend Integration](https://api-patterns.org/)
