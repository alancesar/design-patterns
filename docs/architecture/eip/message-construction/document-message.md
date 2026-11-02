---
title: Document Message
pattern_slug: document-message
category: Message Construction
tags:
  - Reliability
  - Performance Efficiency
source: https://www.enterpriseintegrationpatterns.com/DocumentMessage.html
sidebar_label: "Document Message"
---

# Document Message

## Descrição

Document Message transporta uma estrutura de dados de uma aplicação para outra. Diferente de um comando, não diz ao receptor o que fazer: entrega o dado e deixa a decisão de uso com quem recebe.

O documento é tratado como uma unidade, ainda que contenha partes menores. O que importa é que ele chegue de forma confiável; o momento exato da chegada costuma ser menos crítico.

## Problemas que resolve

- Transferir dados entre aplicações sem as limitações de File Transfer e Shared Database.
- Evitar que o emissor precise conhecer o que o receptor fará com os dados.
- Garantir que uma estrutura de dados chegue inteira.

## Quando usar

- Para replicar ou distribuir dados (pedidos, cadastros, resultados) entre sistemas.
- Quando o receptor deve decidir como processar o conteúdo.
- Quando a entrega confiável importa mais do que a latência, combinada com Guaranteed Delivery.

### Quando evitar

- Quando é preciso ordenar uma ação específica (use Command Message).
- Quando só importa avisar que algo aconteceu e o tempo é crítico (use Event Message).
- Quando o documento é grande demais; considere Claim Check ou Message Sequence.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Emissor desacoplado do uso que o receptor faz do dado | Receptor precisa entender a estrutura do documento |
| Entrega confiável de dados completos | Documentos grandes pesam no canal |
| Fácil de combinar com Guaranteed Delivery | Evolução do formato exige cuidado com compatibilidade |

- Intenção implícita pode gerar ambiguidade; nomeie bem o tipo do documento.
- Para reduzir o peso das mensagens, envie referência ao dado em vez do dado.

## Diagrama

```mermaid
flowchart LR
    A["Aplicação A"] -->|"Document Message (dados)"| C["Canal"]
    C --> B["Aplicação B (decide o uso)"]
```

A aplicação A envia os dados e a aplicação B decide o que fazer com eles.

## Padrões relacionados

- [Message](./message.md) — o documento é o corpo da mensagem
- [Command Message](./command-message.md) — pede uma ação em vez de entregar dados
- [Event Message](./event-message.md) — notifica um fato; o conteúdo importa menos
- [Request-Reply](./request-reply.md) — a resposta costuma ser um documento
- [Guaranteed Delivery](../messaging-channels/guaranteed-delivery.md) — garante que o documento chegue
- [Claim Check](../../../cloud/cloud-design-patterns/messaging/claim-check.md) — alternativa para documentos grandes

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/DocumentMessage.html)
