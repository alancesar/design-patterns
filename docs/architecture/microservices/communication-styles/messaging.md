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

## Descrição

No padrão Messaging, os serviços se comunicam trocando mensagens por canais de mensagens, de forma assíncrona. Um remetente publica uma mensagem em um canal gerenciado por um message broker e o destinatário a consome quando estiver pronto, sem que ambos precisem estar disponíveis ao mesmo tempo.

Esse estilo suporta várias formas de interação: requisição/resposta, notificação (sem resposta), requisição com resposta assíncrona, publicação/assinatura e publicação com respostas assíncronas. Essa flexibilidade permite modelar desde comandos até eventos de domínio, e é a base de padrões como Saga e CQRS.

O broker passa a ser um componente central da arquitetura: ele armazena as mensagens até que o consumidor possa processá-las, o que desacopla remetente e consumidor, mas exige que o broker seja operado com alta disponibilidade.

O Enterprise Integration Patterns apresenta Messaging como o estilo que move pequenos pacotes de dados de forma frequente, imediata, confiável e assíncrona, com formatos customizáveis. Ele herda boa parte do desacoplamento de File Transfer, mas com troca contínua: as mensagens podem ser transformadas em trânsito sem que remetente e destinatário saibam, difundidas a vários receptores ou roteadas a um entre vários. Isso separa o trabalho de integração do desenvolvimento das aplicações. O custo é que a comunicação remota é mais lenta, o que favorece trabalho local e chamadas remotas seletivas, e os desenvolvedores precisam raciocinar sobre respostas que não são imediatas.

## Problemas que resolve

- Serviços precisam colaborar sem o acoplamento em tempo de execução da comunicação síncrona.
- Indisponibilidade temporária do consumidor não deve impedir o remetente de prosseguir.
- Necessidade de estilos de interação além de requisição/resposta, como notificações e publicação/assinatura.

## Quando usar

- Remetente e consumidor devem operar de forma independente, com disponibilidade desacoplada.
- É preciso difundir eventos para vários interessados (publicação/assinatura).
- O fluxo é longo ou coordenado, como em sagas e atualização de visões em CQRS.

### Quando evitar

- A interação é um simples requisição/resposta síncrono e a equipe não deseja operar um broker.
- O cliente precisa de resposta imediata e a complexidade do request/reply assíncrono não compensa.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Acoplamento fraco em tempo de execução entre remetente e consumidor | Complexidade adicional: o broker precisa ser operado com alta disponibilidade |
| Maior disponibilidade, pois o broker armazena mensagens até o consumo | Request/reply é mais complexo do que os demais estilos |
| Suporta requisição/resposta, notificação, publicação/assinatura e outros | Entrega *at-least-once* gera duplicatas e exige consumidores idempotentes |

Considerações adicionais:

- **Consistência:** publicar a mensagem de forma atômica com a gravação no banco requer Transactional Outbox.
- **Configuração:** nomes lógicos de canais e a localização do broker devem vir de configuração externalizada.
- **Observabilidade:** o fluxo assíncrono dificulta o rastreamento; propague identificadores de correlação.

## Diagrama

```mermaid
flowchart LR
    A["Serviço remetente"] -->|"publica mensagem"| C["Canal de mensagens (broker)"]
    C -->|"entrega quando pronto"| B["Serviço consumidor"]
    B -.->|"resposta opcional"| R["Canal de resposta"]
    R -.-> A
```

O remetente publica a mensagem em um canal e segue seu trabalho; o broker a retém até que o consumidor a processe, podendo haver uma resposta assíncrona por outro canal.

## Padrões relacionados

- [Remote Procedure Invocation](./remote-procedure-invocation.md) — alternativa síncrona de requisição/resposta.
- [Domain-specific Protocol](./domain-specific-protocol.md) — alternativa baseada em protocolo específico do domínio.
- [Idempotent Consumer](../../../cloud/azure/messaging/idempotent-consumer.md) — torna seguro o processamento de mensagens duplicadas.
- [Saga](../../../cloud/azure/distributed-coordination/saga.md) — coordena transações distribuídas por meio de mensagens.
- [CQRS](../../../cloud/azure/data-management/cqrs.md) — usa mensagens para manter as visões de leitura atualizadas.
- [Transactional Outbox](../transactional-messaging/transactional-outbox.md) — publica mensagens como parte da transação do banco de dados.
- [Externalized Configuration](../../../cloud/azure/deployment-and-topology/external-configuration-store.md) — fornece nomes de canais e localização do broker.
- [Publisher-Subscriber](../../../cloud/azure/messaging/publisher-subscriber.md) — estilo de publicação/assinatura sobre mensageria.
- [Asynchronous Request-Reply](../../../cloud/azure/messaging/asynchronous-request-reply.md) — requisição com resposta assíncrona.
- [File Transfer](../../eip/integration-styles/file-transfer.md) — estilo em lote por arquivos, com desacoplamento semelhante, mas sem troca imediata.
- [Shared Database](../service-collaboration/shared-database.md) — estilo de integração por banco compartilhado.
- [Message Channel](../../eip/messaging-channels/message-channel.md) — o canal por onde as mensagens trafegam.
- [Message](../../eip/message-construction/message.md) — o pacote de dados trocado.
- [Message Endpoint](../../eip/messaging-endpoints/message-endpoint.md) — o ponto em que a aplicação envia e recebe mensagens.

## Referência

- [Página do padrão no microservices.io](https://microservices.io/patterns/communication-style/messaging.html)
- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/Messaging.html)
