---
title: Messaging Mapper
pattern_slug: messaging-mapper
category: Messaging Endpoints
tags:
  - Operational Excellence
  - Performance Efficiency
source: https://www.enterpriseintegrationpatterns.com/MessagingMapper.html
sidebar_label: "Messaging Mapper"
---

# Messaging Mapper

## Description

Messaging Mapper is a separate component that converts between domain objects and messages. When sending, it reads the objects and builds the message for the channel; when receiving, it creates or updates domain objects from the message content.

Neither the domain objects nor the messaging infrastructure know about the mapper, so both sides evolve independently. It is the messaging specialization of Fowler's Mapper pattern, analogous to the Data Mapper in object-relational mapping.

The challenge is that objects use references and inheritance, features that many messaging infrastructures don't support, and that the message must be readable by applications that aren't even object-oriented.

## Problems it solves

- Coupling between the domain model and the message format.
- Difficulty representing object graphs and inheritance in messages.
- Duplicated conversion code scattered across the application.

## When to use

- When the domain model is rich and must be exchanged through messages without coupling to them.
- When the message format is defined by third parties or by a canonical model.

## When to avoid

- When messages are simple and the data object itself is already the message.
- When a generic framework serializer does the job with no specific mapping logic.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Independent domain and messaging | Mapping code to maintain with every model change |
| Format changes stay localized | Mapping graphs and inheritance is complex |
| The same mapper can be reused across several endpoints | Possible information loss in conversion |

- It's wise to version the message format and test the mapper with old and new messages.

## Diagram

```mermaid
flowchart LR
    D["Domain objects"] <--> M["Messaging Mapper"]
    M <--> E["Message Endpoint"]
    E <--> C[["Message Channel"]]
```

The mapper sits between the domain and the endpoint, converting in both directions.

## Related patterns

- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — uses the mapper to fill and read messages.
- [Messaging Gateway](/architecture/eip/messaging-endpoints/messaging-gateway) — often delegates conversion to the mapper.
- [Message Translator](/architecture/eip/message-transformation/message-translator) — translates between message formats, not between objects and messages.
- [Canonical Data Model](/architecture/eip/message-transformation/canonical-data-model) — a common format the mapper can convert to.
- [Document Message](/architecture/eip/message-construction/document-message) — a message type often produced by the mapper.
- [Command Message](/architecture/eip/message-construction/command-message) — another message type produced by the mapper.
- [Mapper (PoEAA)](/design/poeaa/base/mapper) — the general pattern it derives from.
- [Data Mapper (PoEAA)](/design/poeaa/data-source-architectural/data-mapper) — the analogue for persistence.

## Reference

- [Pattern page on Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/MessagingMapper.html)
