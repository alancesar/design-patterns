---
title: Envelope Wrapper
pattern_slug: envelope-wrapper
category: Message Transformation
tags:
  - Security
  - Operational Excellence
source: https://www.enterpriseintegrationpatterns.com/EnvelopeWrapper.html
sidebar_label: "Envelope Wrapper"
---

# Envelope Wrapper

## Descrição

O Envelope Wrapper envolve os dados de uma aplicação em um "envelope" que atende aos requisitos da infraestrutura de mensageria e, no destino, remove esse envelope para devolver os dados originais. A mensagem costuma ter um cabeçalho, voltado à infraestrutura (roteamento, identificação, segurança), e um corpo com os dados da aplicação.

Aplicações existentes normalmente não conhecem os campos de cabeçalho exigidos e podem tratá-los como erro; já os componentes de roteamento podem rejeitar mensagens sem esses campos. O wrapper resolve o impasse: ele embrulha a mensagem na saída da aplicação e a desembrulha na chegada.

Em termos gerais, o fluxo tem duas etapas: um wrapper no lado do remetente, que adiciona cabeçalhos ou aplica transformações exigidas (por exemplo, criptografia), e um unwrapper no lado do destinatário, que reverte essas operações antes de entregar os dados à aplicação.

## Problemas que resolve

- Aplicações legadas não produzem os campos de cabeçalho exigidos pela infraestrutura de mensageria.
- Aplicações não preparadas para cabeçalhos podem falhar ao receber campos que não esperam.
- Requisitos como criptografia, assinatura ou compressão do conteúdo precisam ser aplicados sem alterar a aplicação.
- Componentes de roteamento e rastreamento precisam de metadados que o corpo original não traz.

## Quando usar

- Uma aplicação existente precisa participar de uma troca de mensagens que impõe cabeçalhos ou formato de envelope.
- É preciso aplicar criptografia, assinatura ou compressão de forma transparente às aplicações.
- Vários sistemas compartilham uma infraestrutura com um formato de envelope padronizado.

## Quando evitar

- A aplicação já consegue produzir e consumir o formato com cabeçalhos nativamente.
- O envelope não agrega informação útil à infraestrutura e só adiciona processamento.
- A necessidade é converter o conteúdo, e não embrulhá-lo: use um Message Translator.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Aplicações existentes entram na mensageria sem alteração | Passos extras de wrap e unwrap em cada mensagem |
| Cabeçalhos e segurança tratados de forma centralizada | Wrapper e unwrapper precisam estar sempre alinhados em versão e formato |
| Roteamento baseado em metadados sem mexer no corpo | Se o unwrapper falhar, a aplicação recebe dados inválidos ou nada |

- Garanta que o par wrapper/unwrapper seja simétrico; qualquer divergência corrompe a mensagem.
- Se houver criptografia, gerencie as chaves fora do corpo da mensagem.

## Diagrama

```mermaid
flowchart LR
    A["Aplicação origem"] --> W["Wrapper"]
    W -->|"Mensagem com envelope"| C["Canal de mensagens"]
    C --> U["Unwrapper"]
    U --> B["Aplicação destino"]
```

O wrapper adiciona o envelope exigido pela infraestrutura e o unwrapper o remove, de modo que as aplicações trabalham apenas com os dados originais.

## Padrões relacionados

- [Message Translator](/architecture/eip/message-transformation/message-translator) — converte o formato do conteúdo, enquanto o wrapper apenas o envolve.
- [Content Enricher](/architecture/eip/message-transformation/content-enricher) — pode ser usado para completar campos de cabeçalho com dados externos.
- [Content-Based Router](/architecture/eip/message-routing/content-based-router) — usa os campos do envelope para decidir o roteamento.
- [Messaging Bridge](/architecture/cloud-design-patterns/messaging/messaging-bridge) — conecta sistemas de mensageria que exigem envelopes distintos.
- [Pipes and Filters](/architecture/cloud-design-patterns/messaging/pipes-and-filters) — wrapper e unwrapper são filtros na cadeia de processamento.
- [Decorator](/coding/gof/structural/decorator) — também acrescenta responsabilidades em volta de um objeto sem alterá-lo.

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/EnvelopeWrapper.html)
