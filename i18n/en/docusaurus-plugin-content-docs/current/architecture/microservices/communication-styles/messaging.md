---
title: Messaging
pattern_slug: messaging
category: Communication Styles
tags:
  - Reliability
  - Performance Efficiency
  - Operational Excellence
also_in:
  - architecture/eip/integration-styles
source: https://microservices.io/patterns/communication-style/messaging.html
sidebar_label: "Messaging"
---

# Messaging

## Description

In the Messaging pattern, services communicate asynchronously by exchanging messages over message channels. A sender publishes a message to a channel managed by a message broker, and the receiver consumes it when it's ready, without both having to be available at the same time.

This style supports several forms of interaction: request/response, notification (no reply), request with asynchronous response, publish/subscribe, and publish with asynchronous responses. That flexibility makes it possible to model everything from commands to domain events, and it's the foundation of patterns such as Saga and CQRS.

The broker becomes a central component of the architecture: it stores messages until the consumer can process them, which decouples sender and consumer but requires the broker to be operated with high availability.

Enterprise Integration Patterns presents Messaging as the style that moves small packets of data frequently, immediately, reliably, and asynchronously, in customizable formats. It inherits much of File Transfer's decoupling, but with continuous exchange: messages can be transformed in transit without the sender and receiver knowing, broadcast to several receivers, or routed to one of several. This separates integration work from application development. The cost is that remote communication is slower, which favors local work and selective remote calls, and developers have to reason about responses that aren't immediate.

## Problems it solves

- Services need to collaborate without the runtime coupling of synchronous communication.
- Temporary consumer unavailability shouldn't stop the sender from proceeding.
- The need for interaction styles beyond request/response, such as notifications and publish/subscribe.

## When to use

- Sender and consumer should operate independently, with decoupled availability.
- Events need to be broadcast to several interested parties (publish/subscribe).
- The flow is long or coordinated, as in sagas and CQRS view updates.

## When to avoid

- The interaction is a simple synchronous request/response and the team doesn't want to operate a broker.
- The client needs an immediate response and the complexity of asynchronous request/reply isn't worth it.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Loose runtime coupling between sender and consumer | Added complexity: the broker must be operated with high availability |
| Higher availability, since the broker stores messages until they're consumed | Request/reply is more complex than the other styles |
| Supports request/response, notification, publish/subscribe, and more | *At-least-once* delivery produces duplicates and requires idempotent consumers |

Additional considerations:

- **Consistency:** publishing the message atomically with the database write requires Transactional Outbox.
- **Configuration:** logical channel names and the broker's location should come from externalized configuration.
- **Observability:** the asynchronous flow makes tracing harder; propagate correlation identifiers.

## Diagram

```mermaid
flowchart LR
    A["Sender service"] -->|"publishes message"| C["Message channel (broker)"]
    C -->|"delivers when ready"| B["Consumer service"]
    B -.->|"optional reply"| R["Reply channel"]
    R -.-> A
```

The sender publishes the message to a channel and carries on with its work; the broker holds it until the consumer processes it, and there may be an asynchronous reply over another channel.

## Related patterns

- [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation) — the synchronous request/response alternative.
- [Domain-specific Protocol](/architecture/microservices/communication-styles/domain-specific-protocol) — the alternative based on a domain-specific protocol.
- [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer) — makes processing duplicate messages safe.
- [Saga](/architecture/cloud-design-patterns/distributed-coordination/saga) — coordinates distributed transactions through messages.
- [CQRS](/architecture/cloud-design-patterns/data-management/cqrs) — uses messages to keep read views up to date.
- [Transactional Outbox](/architecture/microservices/transactional-messaging/transactional-outbox) — publishes messages as part of the database transaction.
- [Externalized Configuration](/architecture/cloud-design-patterns/deployment-and-topology/external-configuration-store) — provides channel names and the broker's location.
- [Publisher-Subscriber](/architecture/cloud-design-patterns/messaging/publisher-subscriber) — publish/subscribe style on top of messaging.
- [Asynchronous Request-Reply](/architecture/cloud-design-patterns/messaging/asynchronous-request-reply) — request with an asynchronous response.
- [File Transfer](/architecture/eip/integration-styles/file-transfer) — a batch, file-based style with similar decoupling but no immediate exchange.
- [Shared Database](/architecture/microservices/service-collaboration/shared-database) — an integration style based on a shared database.
- [Message Channel](/architecture/eip/messaging-channels/message-channel) — the channel through which messages travel.
- [Message](/architecture/eip/message-construction/message) — the data packet being exchanged.
- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — the point where the application sends and receives messages.

## Reference

- [Pattern page on microservices.io](https://microservices.io/patterns/communication-style/messaging.html)
- [Pattern page on Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/Messaging.html)
