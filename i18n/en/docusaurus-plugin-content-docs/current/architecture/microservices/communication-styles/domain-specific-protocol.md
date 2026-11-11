---
title: Domain-specific Protocol
pattern_slug: domain-specific-protocol
category: Communication Styles
tags:
  - Performance Efficiency
  - Operational Excellence
source: https://microservices.io/patterns/communication-style/domain-specific.html
sidebar_label: "Domain-specific Protocol"
---

# Domain-specific Protocol

## Description

The Domain-specific Protocol pattern proposes that communication between services, or between clients and services, use a protocol native to the problem domain instead of a generic request/response or messaging protocol. These protocols already encode the semantics, formats, and guarantees typical of the field they serve.

Classic examples are email protocols (SMTP and IMAP) and media streaming protocols (RTMP, HLS, and HDS). When a service belongs to one of these domains, adopting the established protocol lets it interoperate with existing clients, servers, and tools without reinventing the mechanism.

In the microservices context, it is a third option for interprocess communication, alongside RPI and Messaging. The source describes the pattern quite briefly, without detailing forces or consequences; the text below adds general considerations.

## Problems it solves

- Services need an interprocess communication (IPC) mechanism to serve clients and collaborate with each other.
- Generic protocols may not serve the needs of specific domains well, such as media streaming or email.
- The need to interoperate with existing ecosystems that already speak a standardized protocol.

## When to use

- The domain already has an established protocol (email, media streaming, etc.) and there are clients and tools that use it.
- The domain's requirements, such as latency, continuous streaming, or specific semantics, aren't well served by REST or generic messaging.

## When to avoid

- A suitable generic protocol exists, and the team would gain more from the familiarity and tooling of RPI or Messaging.
- You'd have to invent a proprietary protocol, with high maintenance cost and poor interoperability.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Semantics and performance tuned to the domain | Less reuse of generic tooling and of the team's general knowledge |
| Interoperability with clients and servers in the ecosystem | Dependence on protocol-specific libraries and infrastructure |
| Avoids bending a generic protocol to a use it wasn't designed for | Observability, security, and resilience may require custom solutions |

## Diagram

```mermaid
flowchart LR
    C["Card authorizer"] -->|"domain protocol (e.g., ISO 8583)"| S["Card network"]
    S -->|"responses and streams over the same protocol"| C
```

Client and service talk directly using a protocol established for the domain, with no generic RPI or messaging layer. The source illustrates the pattern with media and email protocols.

## Related patterns

- [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation) — the generic alternative for synchronous request/response.
- [Messaging](/architecture/microservices/communication-styles/messaging) — the generic alternative for asynchronous communication through messages.

## Reference

- [Pattern page on microservices.io](https://microservices.io/patterns/communication-style/domain-specific.html)
