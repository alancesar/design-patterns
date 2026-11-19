---
title: Processing Resource
pattern_slug: processing-resource
category: Endpoint Roles
tags:
  - Decoupling
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Processing Resource"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/processing-resource.mdx';

# Processing Resource

## Description

The Processing Resource pattern exposes an endpoint whose job is to carry out a business action rather than to hold data, offering one or more operations that the client invokes to trigger processing on the provider.

Instead of shaping the contract around data, the endpoint is shaped around an activity (transfer, approve, calculate, cancel). Each operation receives the parameters of the action and returns the result or an acknowledgement, and the internal state that changes as a consequence stays hidden behind the interface. It is the right role when business logic is what matters and storage details should not leak to clients.

The operations of a Processing Resource are usually state creation, state transition or computation functions; reading is typically limited to checking the progress of an activity, since broad data access is the role of the Information Holder Resource. Each operation receives a command message and, in a request-reply exchange, returns a document with the result. The resource can be stateful (a process coordinator) or stateless (a calculation utility), and the contract must state preconditions, invariants and postconditions. The difference from a data-oriented resource is intent: the client asks for something to be done instead of manipulating an entity directly.

## Problems it solves

- Business actions that do not fit well into generic create, read, update and delete operations on an entity
- Clients that would need to know and coordinate several data resources to perform a single activity
- Coupling of the contract to internal data model details, which makes the implementation hard to change
- Business rules and validations duplicated in every client instead of centralized in the provider

## When to use

- The activity has its own business semantics, such as executing a Pix transfer, approving a loan or reconciling a batch
- The action touches several internal pieces of data that the client should neither see nor coordinate
- Logic and invariants must stay in the provider even if storage changes
- The contract is consumed by diverse clients who want to request outcomes, not manipulate state

## When to avoid

- When the client only needs to read or maintain data: an [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) is simpler
- When the operations turn into a list of arbitrary verbs with no cohesion, making the endpoint a dumping ground for procedures
- When many operations share the same state and the contract becomes, in practice, disguised remote access to data
- When the client needs visibility and fine control over the intermediate state that the endpoint hides
- When activity orientation would have to be forced onto a naturally data-oriented domain, such as archives and inventories: prefer the Information Holder Resource
- Mixing actions and data in the same endpoint, although possible, is not recommended in microservices architectures because of the coupling it brings

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| The contract expresses business intent and hides the data model | The client depends on the semantics of each operation, which is hard to standardize |
| Logic and invariants are centralized in the provider | The endpoint can grow and accumulate responsibilities without cohesion |
| Freedom to change the implementation without breaking clients | Actions with side effects need care with retries and idempotency |
| Fewer calls coordinated by the client | Hard to cache and reuse, since there is no identifiable resource to store |

- **Cohesion:** group only operations that serve the same business activity; endpoints that grow too large should be split.
- **Idempotency:** operations with side effects, such as moving money, need an idempotency key to tolerate retries after a network failure.
- **Operation type:** decide for each operation whether it creates state, transitions state, computes or reads, and document it in the contract.
- **Response time:** if the action is slow or the client does not need the result right away, return an identifier and let the client follow up later (polling or callback) instead of blocking the call.
- **Compensation:** whatever a system transaction cannot undo, such as a notification already sent, needs an application-level compensating operation.
- **Security and auditing:** each action needs its own authorization and often an audit trail, which makes the provider stateful even when the domain does not ask for it.
- **RPC risk:** if the operations are just remote procedures in disguise, coupling in time and format grows; model business activities, not internal functions.
- **Response:** return an identifier of what was created or the computed result, so the client can follow up without guessing.

## Diagram

<Diagram />

The client invokes operations named after activities; the endpoint applies the rules and changes the internal data, which does not appear in the contract.

## Example

The fintech's payments service exposes a `/pix-processor` endpoint with two business operations. The client requests the transfer and receives an identifier; it knows nothing about accounts, the ledger or internal queues.

```http
POST /pix-processor/execute-transfer HTTP/1.1
Content-Type: application/json
Idempotency-Key: 6d8f2c1e-3b7a-4d51-9a10-0b4f1e22c9aa

{
  "sourceAccountId": "acc-1001",
  "pixKey": "maria@example.com",
  "amount": { "cents": 15000, "currency": "BRL" }
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{ "transferId": "pix-77231", "status": "PROCESSING" }
```

```http
POST /pix-processor/cancel-transfer HTTP/1.1
Content-Type: application/json

{ "transferId": "pix-77231", "reason": "CUSTOMER_REQUEST" }
```

The amount is sent in whole cents. If the transfer has already settled, the cancellation is refused, and the reversal enters as a new ledger entry (`LedgerEntry`), never as an edit of the original.

## Related patterns

- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the complementary role: focused on data rather than actions
- [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) — a typical operation type for a Processing Resource
- [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) — an operation that moves internal state from one stage to another
- [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) — a side-effect-free operation that computes a result
- [Remote Facade](/design/poeaa/distribution/remote-facade) — a coarse-grained facade behind which logic and data stay hidden
- [Asynchronous Request-Reply](/architecture/cloud-design-patterns/messaging/asynchronous-request-reply) — a model for long-running actions, with the result fetched later
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key), [Rate Limit](/architecture/api-patterns/documentation/rate-limit) and [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — usually protect and regulate the use of the operations
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — isolates technical parameters so they do not creep into message bodies
- [Command Message](/architecture/eip/message-construction/command-message) — the messaging counterpart of asking for an action to be executed

## Reference

- [Patterns for API Design, chapter 5: Processing Resource](https://api-patterns.org/)
