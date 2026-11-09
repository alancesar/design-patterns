---
title: Message Channel
pattern_slug: message-channel
category: Messaging Channels
tags:
  - Reliability
  - Operational Excellence
source: https://www.enterpriseintegrationpatterns.com/MessageChannel.html
sidebar_label: "Message Channel"
---

# Message Channel

## Description

The Message Channel is the logical path through which two applications exchange messages. One application writes to the channel and the other reads from it, so neither needs to know the other's location, platform or pace. It's the most basic building block of messaging-based integration: without channels, messages have nowhere to travel.

Channels are created and named according to the type of information they carry. The sender picks the channel that fits the subject of the message, and the receiver listens to the channel containing what interests it. This gives the receiver some assurance that what arrives is relevant, and the sender doesn't need to know who will consume it.

In practice, the channel is an abstraction offered by the messaging system (queues, topics, streams). The Point-to-Point Channel and Publish-Subscribe Channel patterns are the two main specializations, and several other patterns in the group refine the concept.

## Problems it solves

- Two applications need to exchange information asynchronously, without direct coupling of address or availability.
- The sender shouldn't need to know which application will receive its information.
- The receiver needs a way to receive only information relevant to it.
- A central, named point is needed to administer, monitor and secure traffic between applications.

## When to use

- Whenever integration is done through messaging: every send and every receive goes through some channel.
- When you want to separate types of information into distinct flows, each with its own producers and consumers.
- When you need to explicitly define which applications may write to or read from each flow.

## When to avoid

- When the interaction requires an immediate, synchronous response, the asynchronous channel abstraction only gets in the way; prefer a direct call.
- When the number of channels would grow out of control (one per sender-recipient combination); in that case, rethink the granularity or use content-based routing.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Decoupling between sender and receiver | One more resource to configure, name and administer |
| Clear separation of flows by type of information | Channel proliferation makes governance harder |
| A natural point for security, monitoring and retention | Channel semantics depend on the messaging product |
| Asynchronous communication tolerant of temporary unavailability | Latency and eventual consistency instead of an immediate response |

- **Naming convention:** channel names become part of the contract between applications and should be stable and descriptive.
- **Creation:** channels are generally defined at design or deployment time, not dynamically by each application.
- **Observability:** depth, inbound rate and outbound rate of each channel are basic health metrics for the integration.

## Diagram

```mermaid
flowchart LR
    A["Sender application"] -->|"writes"| C["Message Channel"]
    C -->|"reads"| B["Receiver application"]
```

The sender application writes messages to the channel and the receiver reads them, without either knowing the other directly.

## Related patterns

- [Point-to-Point Channel](/architecture/eip/messaging-channels/point-to-point-channel) — a specialization in which each message is consumed by a single receiver.
- [Publish-Subscribe Channel](/architecture/cloud-design-patterns/messaging/publisher-subscriber) — a specialization in which each subscriber receives a copy of the message.
- [Datatype Channel](/architecture/eip/messaging-channels/datatype-channel) — dedicates one channel to each data type.
- [Invalid Message Channel](/architecture/eip/messaging-channels/invalid-message-channel) — a channel for messages the receiver can't process.
- [Channel Adapter](/architecture/eip/messaging-channels/channel-adapter) — connects an existing application to a channel.
- [Message Bus](/architecture/eip/messaging-channels/message-bus) — the set of channels and adapters that forms the common infrastructure.
- [Messaging](/architecture/microservices/communication-styles/messaging) — the integration style that depends on channels.
- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — the point where the application connects to the channel.
- [Selective Consumer](/architecture/eip/messaging-endpoints/selective-consumer) — filters the messages the consumer accepts from a channel.

## Reference

- [Pattern page on Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/MessageChannel.html)
