---
title: Message Dispatcher
pattern_slug: message-dispatcher
category: Messaging Endpoints
tags:
  - Performance Efficiency
  - Reliability
source: https://www.enterpriseintegrationpatterns.com/MessageDispatcher.html
sidebar_label: "Message Dispatcher"
---

# Message Dispatcher

## Descrição

Message Dispatcher coordena vários consumidores de um mesmo canal. Ele tem dois papéis: o dispatcher retira cada mensagem do canal e a repassa; o performer recebe a mensagem e faz o processamento, podendo recorrer ao restante da aplicação.

Os performers podem ser criados sob demanda ou obtidos de um pool, cada um em sua própria thread, o que permite processar mensagens em paralelo com um único consumidor do canal. O dispatcher pode enviar qualquer mensagem a qualquer performer ou escolher performers especializados com base nas propriedades da mensagem.

Difere do Competing Consumers, em que cada consumidor tem sua própria conexão ao canal e compete diretamente; aqui há um único ponto de leitura que distribui internamente.

## Problemas que resolve

- Consumidor único que processa mensagens em série e não acompanha o ritmo.
- Custo de manter muitas conexões ao canal.
- Necessidade de rotear mensagens para tratadores diferentes conforme o tipo.

## Quando usar

- Quando se quer concorrência dentro de um único processo consumidor.
- Quando diferentes tipos de mensagem exigem tratadores distintos.

### Quando evitar

- Quando a ordem das mensagens precisa ser estritamente preservada.
- Quando o escalonamento horizontal com Competing Consumers é suficiente.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Paralelismo com uma só conexão | Ordem de processamento não garantida |
| Roteamento interno por tipo | Dispatcher pode virar gargalo e ponto único de falha |
| Pool de performers controla recursos | Gerenciar threads e falhas dos performers adiciona complexidade |

- Defina o que acontece com a mensagem se um performer falhar e se o pool estiver cheio.

## Diagrama

```mermaid
flowchart LR
    C[["Canal"]] --> D["Dispatcher"]
    D --> P1["Performer 1"]
    D --> P2["Performer 2"]
    D --> P3["Performer N"]
```

O dispatcher lê do canal e distribui cada mensagem a um performer.

## Padrões relacionados

- [Competing Consumers](/architecture/cloud-design-patterns/messaging/competing-consumers) — alternativa em que cada consumidor lê do canal.
- [Selective Consumer](/architecture/eip/messaging-endpoints/selective-consumer) — filtragem que pode ser feita pelo dispatcher.
- [Event-Driven Consumer](/architecture/eip/messaging-endpoints/event-driven-consumer) — forma comum de alimentar o dispatcher.
- [Polling Consumer](/architecture/eip/messaging-endpoints/polling-consumer) — outra forma de alimentá-lo.
- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — o dispatcher é parte do endpoint.
- [Transactional Client](/architecture/eip/messaging-endpoints/transactional-client) — cada performer pode ter sua transação.
- [Datatype Channel](/architecture/eip/messaging-channels/datatype-channel) — alternativa de separar tipos por canal.

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/MessageDispatcher.html)
