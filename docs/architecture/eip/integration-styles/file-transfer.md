---
title: File Transfer
pattern_slug: file-transfer
category: Integration Styles
tags:
  - Cost Optimization
  - Operational Excellence
source: https://www.enterpriseintegrationpatterns.com/FileTransferIntegration.html
sidebar_label: "File Transfer"
---

# File Transfer

## Descrição

Em File Transfer, cada aplicação produz arquivos com as informações que outras aplicações precisam e consome arquivos gerados pelas demais. Não há chamada direta entre os sistemas: o arquivo é o contrato. Quem integra cuida de converter os formatos, de modo que o produtor não precise conhecer o consumidor.

Os arquivos costumam ser gerados em intervalos que fazem sentido para o negócio (por exemplo, uma exportação noturna), e não em tempo real. Isso torna o estilo simples e universal, pois qualquer sistema capaz de ler e gravar arquivos pode participar, mesmo que use outra linguagem ou plataforma.

A escolha do formato (texto delimitado, largura fixa, XML, JSON, formatos legados de mainframe) é uma decisão importante, porque determina quanto processamento de transformação será necessário e quais ferramentas de leitura e escrita estarão disponíveis.

## Problemas que resolve

- Aplicações desenvolvidas de forma independente, em linguagens e plataformas distintas, precisam trocar informação.
- A saída de uma aplicação raramente tem o formato que outra precisa, exigindo conversão.
- A frequência da troca deve acompanhar o ritmo do negócio, não necessariamente a capacidade técnica de comunicação em tempo real.
- Dispensar acesso aos internos de cada sistema: basta combinar um formato de arquivo.

## Quando usar

- A troca é naturalmente periódica ou em lote (fechamentos, cargas, relatórios, conciliações).
- Há sistemas legados ou de terceiros que só oferecem importação e exportação de arquivos.
- Os sistemas precisam ficar desacoplados em plataforma e tecnologia, com custo baixo de integração.
- Grandes volumes de dados são movidos de uma só vez e a latência não é crítica.

### Quando evitar

- Quando os dados precisam estar atualizados quase em tempo real; prefira [Messaging](/architecture/microservices/communication-styles/messaging).
- Quando é preciso invocar comportamento no sistema remoto e obter resposta imediata; veja [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation).
- Quando muitos sistemas precisam enxergar a mesma informação consistente a todo momento; veja [Shared Database](/architecture/microservices/service-collaboration/shared-database).

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Acoplamento baixo: só o formato do arquivo é compartilhado | Dados defasados: refletem apenas o último lote gerado |
| Qualquer sistema que lê e grava arquivos participa | Formato e transformação precisam de dono e de documentação |
| Ferramental maduro para leitura, escrita e conversão | Sem entrega confirmada nem tratamento de erro nativos: falhas parciais e duplicatas são problema da integração |
| Barato e fácil de implantar | Conflitos de atualização entre sistemas só aparecem depois, na reconciliação |

- **Consistência:** os sistemas ficam temporariamente divergentes entre uma troca e outra.
- **Operação:** é preciso lidar com nomes de arquivo, bloqueio durante a escrita, arquivamento e reprocessamento.
- **Observabilidade:** acompanhar chegada, volume e rejeição de arquivos exige monitoramento próprio.

## Diagrama

```mermaid
flowchart LR
    A["Aplicação A (produtora)"] -->|"grava"| F["Arquivo em formato combinado"]
    F -->|"lê"| T["Conversor de formato"]
    T --> B["Aplicação B (consumidora)"]
```

A aplicação produtora grava um arquivo periodicamente; um conversor adapta o formato e a aplicação consumidora o lê no seu próprio ritmo.

## Padrões relacionados

- [Shared Database](/architecture/microservices/service-collaboration/shared-database) — outro estilo de integração, com dados compartilhados em tempo quase real.
- [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation) — integração síncrona por chamadas a interfaces expostas.
- [Messaging](/architecture/microservices/communication-styles/messaging) — troca frequente, imediata e assíncrona de pequenos pacotes de dados.
- [Message](/architecture/eip/message-construction/message) — a unidade de dados que substitui o arquivo na mensageria.
- [Message Channel](/architecture/eip/messaging-channels/message-channel) — o canal que faz o papel do local de troca dos arquivos.
- [Message Endpoint](/architecture/eip/messaging-endpoints/message-endpoint) — o ponto em que a aplicação lê e grava no canal.

## Referência

- [Página do padrão no Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/FileTransferIntegration.html)
