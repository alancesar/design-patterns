---
title: API Description
pattern_slug: api-description
category: Documentation
tags:
  - Shared Understanding
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "API Description"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/documentation/api-description.mdx';

# API Description

## Description

The API Description pattern defines, in a human- and machine-readable form, the technical and semantic contract of an API: endpoints, operations, structure and meaning of messages, errors and any other knowledge that provider and clients must share to interact successfully.

Without this contract, client developers have to guess required parameters, effects on state, call order and guarantees such as idempotency. A good description replaces trial and error with lookup: it can be read by business analysts, validated by tools and used to generate client code, server skeletons and tests. For HTTP APIs, a recognized language such as the OpenAPI Specification usually covers the technical part; the semantic part (what each operation means in the domain, pre- and postconditions, invariants) is written as complementary text.

There are two variants at the ends of a spectrum. The **Minimal Description** holds only the essentials: endpoint addresses, operation names, and the structure and meaning of request and response messages. The **Elaborate Description** adds usage examples, tables of parameters and constraints, error codes, security requirements, behavior (idempotency, state changes), version information, conformance test cases and metadata such as owner and support channel. Hybrid forms are common.

## Problems it solves

- Clients that do not know how to build calls or what to expect in responses
- Implicit assumptions about idempotency, transactionality and call order that only surface in production
- Reverse-engineering sample responses to discover the structure and meaning of fields
- The lack of a common base to generate code, mocks and contract tests

## When to use

- Whenever an endpoint is exposed to developers who are not the provider's own team
- When clients and provider use different languages and platforms and need a neutral format
- When the API is mission critical and its behavior (errors, state, versions) must be unambiguous
- To feed developer portals, SDK generation and contract tests

## When to avoid

- In throwaway prototypes or very short-lived internal APIs, where a sample call is enough
- When a detailed description would be maintained by hand with nobody to keep it current: an outdated description is worse than a minimal one
- When an elaborate description would expose implementation details, such as downstream dependencies, that should stay hidden

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Fewer assumptions and less rework for API consumers | Keeping the description current as the API evolves has an ongoing cost |
| Interoperability and generation of code and tests from the contract | Elaborate descriptions are redundant and may contradict themselves |
| A common language between business and technology | Too much detail becomes waste and leaks internals |
| A base to version and communicate changes | Minimal descriptions leave gaps that clients fill by guessing |

- **Depth:** an overspecified description is hard to consume and maintain; an underspecified one is easy to read but does not guarantee interoperable conversations.
- **Single source:** generate the description from the code or the code from the description so they do not diverge.
- **Information hiding:** describe what the client needs to know, not how the provider implements it.
- **Quality of service:** availability and performance goals fit better in a [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) that the description references.

## Diagram

<Diagram />

The description gathers the technical contract plus the semantic and organizational information, and is consumed by people and tools on the client side.

## Example

An excerpt of an OpenAPI description for creating Pix charges at a fictional fintech, with the fields a client needs to integrate: operation, body, responses and the semantic note about idempotency. Monetary values are integers in cents.

```yaml
openapi: 3.0.3
info:
  title: Pix Charges API
  version: 2.1.0
  description: >
    Creates and retrieves Pix charges. Contact: apis@fintech.example.
    Limits and availability: see the Rate Limit and SLA in the portal.
paths:
  /v2/pix-charges:
    post:
      operationId: createPixCharge
      summary: Creates a Pix charge
      description: >
        Idempotent when the Idempotency-Key header is repeated: the same
        key returns the charge already created. Effect: stores a PixCharge
        with status PENDING.
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema: { type: string, maxLength: 64 }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [accountId, amountCents]
              properties:
                accountId: { type: string, example: "acc_1042" }
                amountCents: { type: integer, minimum: 1, example: 15000 }
      responses:
        "201":
          description: Charge created
        "422":
          description: Invalid amount or blocked account (Error Report)
        "429":
          description: Rate Limit exceeded
```

The same document is the basis for generating SDKs, validating requests and building the developer portal.

## Related patterns

- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — complements the description with measurable quality goals
- [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan) — states the cost of use and is attached to the description
- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — usage limits are part of what the description communicates
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — the API version is part of the described contract
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — the description lists the errors and their structure
- [Published Language](/design/ddd/context-mapping/published-language) — a documented, shared language; the API Description is the artifact that records it in an API
- [Open Host Service](/design/ddd/context-mapping/open-host-service) — requires a well-documented protocol, a role the description fulfills
- [Consumer-Driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test) — checks in practice whether the provider honors the described contract

## Reference

- [Patterns for API Design, chapter 9: API Description](https://api-patterns.org/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
