---
title: Solution-Internal API
pattern_slug: solution-internal-api
category: Foundations
tags:
  - Decoupling
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Solution-Internal API"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/foundations/solution-internal-api.mdx';

# Solution-Internal API

## Description

The Solution-Internal API pattern limits access to and use of an API to a single application, logically decomposing it into components that expose local or remote APIs only to their internal communication partners. These components can be services and microservices or modules inside one program, and clients and providers usually run in the same data center, or even on the same compute node.

This kind of API serves both the application's frontend and other backend components, so it appears as an internal frontend or backend API. A set of related internal APIs is sometimes called a platform API, such as the web APIs of a cloud provider or the management APIs of a message broker.

Being independently deployable does not mean being independently deployed. A modular monolith, for example, swaps data transfer objects over local APIs and can be turned into microservices with less effort than a tangle of objects coupled by remote references. Designing internal APIs that improve coupling is complex work, and that is what both service-oriented architectures and microservices try to solve.

## Problems it solves

- Structuring an application into components with explicit boundaries
- Preventing external clients from depending on details the team wants to be free to change
- Reducing coupling between the parts, even when they run together
- Preparing a modular monolith for an eventual split into services

## When to use

- When the fintech splits its backend into accounts, cards and credit services that talk to each other
- When the application needs clear module boundaries, even within a single process
- When only teams of the same solution consume the API and changes can be coordinated
- When you want freedom to evolve the contract without the stability promises of a public API

## When to avoid

- When consumers outside the organization need the capability: expose a [Public API](/architecture/api-patterns/foundations/public-api) or a [Community API](/architecture/api-patterns/foundations/community-api), with due security and stability
- When the application is small and splitting it into many components would only add remote calls and complexity
- When "internal" is an excuse to skip contract, documentation and tests: internal APIs also have consumers

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Freedom to change the contract, since consumers are known | Changes still require coordination between teams |
| Lower demands for security, external documentation and commercial terms | Temptation to relax controls that still matter |
| Network and deployment proximity, with low latency | The assumption of a fast, trusted network can hide failures |
| Boundaries that ease evolving from modules to services | Wrong cuts produce distributed coupling |

- **Network and trust:** being on the same network does not remove the need for authentication between services.
- **Visibility can grow:** an internal API that starts to be used from outside must be rethought as public or community.
- **Documentation:** even for internal use, keep a minimal contract and contract tests.

## Diagram

<Diagram />

All calls happen inside the application boundary: no external client reaches these APIs directly.

## Example

The fintech's cards service asks the accounts service whether there are funds before authorizing a purchase. The API is not exposed outside the internal network and may change according to the needs of the two teams.

```http
POST /internal/accounts/acc-7781/holds HTTP/1.1
Host: accounts.internal
Content-Type: application/json

{ "amountCents": 8990, "currency": "BRL", "reason": "card-authorization", "cardId": "card-204" }

HTTP/1.1 201 Created
Content-Type: application/json

{ "holdId": "hold-6107", "available": { "amountCents": 116100, "currency": "BRL" } }
```

The name `internal` in the path and host makes it clear that this contract is not public.

## Related patterns

- [Public API](/architecture/api-patterns/foundations/public-api) and [Community API](/architecture/api-patterns/foundations/community-api) — the other visibilities, more open and with greater stability demands
- [Backend Integration](/architecture/api-patterns/foundations/backend-integration) — the integration type the internal backend API carries out
- [Frontend Integration](/architecture/api-patterns/foundations/frontend-integration) — the integration type of the internal frontend API
- [Bounded Context](/design/ddd/model-in-practice/bounded-context) — a criterion for cutting the components that expose the APIs
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — the messages exchanged over a modular monolith's local APIs
- [Consumer-Driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test) — keeps the internal contract trustworthy across teams
- [Strangler Fig](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig) — gradual migration that relies on well-defined internal APIs

## Reference

- [Patterns for API Design, chapter 4: Solution-Internal API](https://api-patterns.org/)
