---
title: Service Activator
pattern_slug: service-activator
category: Messaging Endpoints
tags:
  - Operational Excellence
  - Reliability
source: https://www.enterpriseintegrationpatterns.com/MessagingAdapter.html
sidebar_label: "Service Activator"
---

# Service Activator

## Descrição

Service Activator fica entre o canal de mensageria e um serviço da aplicação. Ele recebe mensagens do canal e invoca o serviço correspondente, tornando-o acessível por mensageria sem que o serviço saiba disso.

Pode tratar requisições de mão única ou trocas Request-Reply, em que o resultado é enviado ao canal de resposta. O serviço costuma ser uma chamada local simples, por exemplo parte de uma camada de serviço. O activator pode sempre chamar o mesmo serviço ou escolher o alvo com base na mensagem, por exemplo por reflexão.

Como o activator cuida de todos os detalhes de mensageria, o serviço é chamado como por qualquer outro cliente e pode ser reutilizado por outros meios de acesso.

## Problemas que resolve

- Expor um serviço existente via mensageria sem alterá-lo.
- Misturar lógica de negócio com código de consumo de mensagens.

## Quando usar

- Quando um serviço deve ser invocado por mensagens de comando ou de requisição.
- Quando o mesmo serviço também é acessível por outros meios (API, chamada local).

### Quando evitar

- Quando o serviço já é nativo de mensageria.
- Quando a conversão exigida é tão grande que pede um componente de transformação separado.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Serviço independente da mensageria | Componente adicional por serviço |
| Reuso do serviço por vários canais de acesso | Tratamento de erros e reentregas precisa ser definido no activator |
| Ponto único para adaptar mensagens a chamadas | Resposta assíncrona exige correlação |

- Decida o comportamento diante de mensagens inválidas, enviando-as a um Invalid Message Channel.

## Diagrama

```mermaid
flowchart LR
    C[["Canal de requisição"]] --> A["Service Activator"]
    A -->|"chamada"| S["Serviço da aplicação"]
    S -->|"resultado"| A
    A --> R[["Canal de resposta"]]
```

O activator traduz a mensagem em chamada ao serviço e, se necessário, devolve o resultado por outro canal.

## Padrões relacionados

- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — o activator é um tipo de endpoint de recebimento.
- [Messaging Gateway](/architecture/eip/messaging-endpoints/messaging-gateway) — contraparte do lado emissor.
- [Command Message](/architecture/eip/message-construction/command-message) — mensagem típica que aciona o serviço.
- [Request-Reply](/architecture/eip/message-construction/request-reply) — interação suportada pelo activator.
- [Event-Driven Consumer](/architecture/eip/messaging-endpoints/event-driven-consumer) — forma habitual de recepção.
- [Polling Consumer](/architecture/eip/messaging-endpoints/polling-consumer) — outra forma de recepção.
- [Message Dispatcher](/architecture/eip/messaging-endpoints/message-dispatcher) — pode distribuir mensagens a vários activators.
- [Invalid Message Channel](/architecture/eip/messaging-channels/invalid-message-channel) — destino de mensagens que o serviço não entende.

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/MessagingAdapter.html)
