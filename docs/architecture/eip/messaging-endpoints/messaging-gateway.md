---
title: Messaging Gateway
pattern_slug: messaging-gateway
category: Messaging Endpoints
tags:
  - Operational Excellence
  - Reliability
source: https://www.enterpriseintegrationpatterns.com/MessagingGateway.html
sidebar_label: "Messaging Gateway"
---

# Messaging Gateway

## Descrição

Messaging Gateway é uma classe que encapsula todo o acesso ao sistema de mensageria e expõe à aplicação uma interface em termos do domínio. Em vez de montar mensagens, definir propriedades e escolher canais, o código de negócio chama um método como `obterScoreDeCredito(cliente)`, com parâmetros tipados.

Somente o gateway sabe que existe mensageria por trás. Ele cria a mensagem, a envia pelo canal e, quando há resposta, a recebe, correlaciona e devolve ao chamador como um valor comum. Trata-se da especialização para mensageria do padrão Gateway de Fowler.

Como o gateway é uma interface comum, é fácil trocá-lo por um stub em testes ou por outra implementação (por exemplo, uma chamada síncrona) sem tocar na lógica de negócio.

## Problemas que resolve

- Código de negócio espalhado com chamadas diretas à API de mensageria.
- Dificuldade de testar a aplicação sem um broker.
- Acoplamento da aplicação a formatos e nomes de canal.

## Quando usar

- Quando várias partes da aplicação precisam enviar mensagens ou solicitar algo via mensageria.
- Quando se quer poder substituir a mensageria por outra forma de integração com pouco impacto.

## Quando evitar

- Quando a aplicação tem um único ponto de envio trivial e a camada extra seria só indireção.
- Quando a lógica de negócio precisa controlar de forma fina propriedades da mensagem, que o gateway esconderia.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Código de negócio limpo e focado no domínio | Mais uma classe por integração |
| Testabilidade com gateways falsos | Interface síncrona pode esconder a natureza assíncrona da mensageria |
| Mensageria substituível | Esconder latência e falhas pode induzir uso inadequado |

- Um gateway com retorno síncrono sobre mensageria assíncrona exige correlação e tratamento de timeout.
- Ele costuma ser o ponto de aplicação de Request-Reply e de Correlation Identifier.

## Diagrama

```mermaid
flowchart LR
    A["Lógica de negócio"] -->|"obterScore(cliente)"| G["Messaging Gateway"]
    G -->|"mensagem"| C[["Canal de requisição"]]
    C --> S["Serviço remoto"]
    S --> R[["Canal de resposta"]]
    R --> G
    G -->|"score"| A
```

A lógica de negócio chama um método do domínio; o gateway cuida de montar a mensagem, enviá-la e correlacionar a resposta.

## Padrões relacionados

- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — o gateway é uma forma de organizar o endpoint.
- [Messaging Mapper](/architecture/eip/messaging-endpoints/messaging-mapper) — frequentemente usado pelo gateway para converter objetos em mensagens.
- [Request-Reply](/architecture/eip/message-construction/request-reply) — estilo de interação que o gateway costuma encapsular.
- [Correlation Identifier](/architecture/eip/message-construction/correlation-identifier) — usado para casar respostas com requisições.
- [Service Activator](/architecture/eip/messaging-endpoints/service-activator) — lado receptor equivalente ao gateway no lado emissor.
- [Gateway (PoEAA)](/design/poeaa/base/gateway) — o padrão geral do qual este é a especialização.
- [Facade (GoF)](/coding/gof/structural/facade) — também simplifica o acesso a um subsistema complexo.

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/MessagingGateway.html)
