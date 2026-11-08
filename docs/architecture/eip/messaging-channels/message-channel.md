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

## Descrição

O Message Channel é o caminho lógico pelo qual duas aplicações trocam mensagens. Uma aplicação escreve no canal e a outra lê dele, de modo que nenhuma precisa conhecer a localização, a plataforma ou o ritmo da outra. Ele é o bloco de construção mais básico da integração por mensageria: sem canais, não há por onde as mensagens trafegarem.

Os canais são criados e nomeados de acordo com o tipo de informação que carregam. Quem envia escolhe o canal adequado ao assunto da mensagem, e quem recebe escuta o canal que contém o que lhe interessa. Assim, o receptor tem alguma garantia de que o que chega é relevante, e o remetente não precisa saber quem vai consumir.

Na prática, o canal é uma abstração oferecida pelo sistema de mensageria (filas, tópicos, streams). Os padrões Point-to-Point Channel e Publish-Subscribe Channel são as duas especializações principais, e vários outros padrões do grupo refinam o conceito.

## Problemas que resolve

- Duas aplicações precisam trocar informações de forma assíncrona, sem acoplamento direto de endereço ou de disponibilidade.
- O remetente não deve precisar saber qual aplicação vai receber sua informação.
- O receptor precisa de uma forma de receber apenas informações relevantes para ele.
- É preciso um ponto central e nomeado para administrar, monitorar e proteger o tráfego entre aplicações.

## Quando usar

- Sempre que a integração for feita por mensageria: todo envio e toda recepção passam por algum canal.
- Quando se deseja separar tipos de informação em fluxos distintos, cada um com seus produtores e consumidores.
- Quando é necessário definir, de forma explícita, quais aplicações podem escrever ou ler cada fluxo.

### Quando evitar

- Quando a interação exige resposta imediata e síncrona, a abstração de canal assíncrono só atrapalha; prefira uma chamada direta.
- Quando o número de canais cresceria sem controle (um por combinação de remetente e destinatário); nesse caso, repense a granularidade ou use roteamento por conteúdo.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Desacoplamento entre quem envia e quem recebe | Mais um recurso a ser configurado, nomeado e administrado |
| Separação clara de fluxos por tipo de informação | Proliferação de canais dificulta a governança |
| Ponto natural para segurança, monitoramento e retenção | A semântica do canal depende do produto de mensageria |
| Comunicação assíncrona tolerante a indisponibilidade temporária | Latência e consistência eventual em vez de resposta imediata |

- **Convenção de nomes:** nomes de canais viram parte do contrato entre as aplicações e devem ser estáveis e descritivos.
- **Criação:** em geral os canais são definidos em tempo de projeto ou implantação, não dinamicamente por cada aplicação.
- **Observabilidade:** profundidade, taxa de entrada e de saída de cada canal são métricas básicas de saúde da integração.

## Diagrama

```mermaid
flowchart LR
    A["Aplicação remetente"] -->|"escreve"| C["Message Channel"]
    C -->|"lê"| B["Aplicação receptora"]
```

A aplicação remetente escreve mensagens no canal e a receptora as lê, sem que uma conheça diretamente a outra.

## Padrões relacionados

- [Point-to-Point Channel](/architecture/eip/messaging-channels/point-to-point-channel) — especialização em que cada mensagem é consumida por um único receptor.
- [Publish-Subscribe Channel](/architecture/cloud-design-patterns/messaging/publisher-subscriber) — especialização em que cada assinante recebe uma cópia da mensagem.
- [Datatype Channel](/architecture/eip/messaging-channels/datatype-channel) — dedica um canal a cada tipo de dado.
- [Invalid Message Channel](/architecture/eip/messaging-channels/invalid-message-channel) — canal para mensagens que o receptor não consegue processar.
- [Channel Adapter](/architecture/eip/messaging-channels/channel-adapter) — conecta uma aplicação existente a um canal.
- [Message Bus](/architecture/eip/messaging-channels/message-bus) — conjunto de canais e adaptadores que forma a infraestrutura comum.
- [Messaging](/architecture/microservices/communication-styles/messaging) — o estilo de integração que depende de canais.
- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — o ponto em que a aplicação se liga ao canal.
- [Selective Consumer](/architecture/eip/messaging-endpoints/selective-consumer) — filtra as mensagens que o consumidor aceita de um canal.

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/MessageChannel.html)
