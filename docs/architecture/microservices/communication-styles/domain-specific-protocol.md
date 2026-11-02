---
title: Domain-specific Protocol
pattern_slug: domain-specific-protocol
category: Communication Styles
tags:
  - Performance Efficiency
  - Operational Excellence
source: https://microservices.io/patterns/communication-style/domain-specific.html
sidebar_label: "Domain-specific Protocol"
---

# Domain-specific Protocol

## Descrição

O padrão Domain-specific Protocol propõe que a comunicação entre serviços, ou entre clientes e serviços, use um protocolo próprio do domínio do problema, em vez de um protocolo genérico de requisição/resposta ou de mensageria. Esses protocolos já codificam as semânticas, os formatos e as garantias típicas da área em que atuam.

Exemplos clássicos são os protocolos de e-mail (SMTP e IMAP) e os de transmissão de mídia (RTMP, HLS e HDS). Quando o serviço pertence a um desses domínios, adotar o protocolo estabelecido permite interoperar com clientes, servidores e ferramentas existentes sem reinventar o mecanismo.

No contexto de microsserviços, é uma terceira opção de comunicação entre processos, ao lado de RPI e Messaging. A fonte descreve o padrão de forma bastante sucinta, sem detalhar forças nem consequências; o texto abaixo complementa com considerações gerais.

## Problemas que resolve

- Serviços precisam de um mecanismo de comunicação entre processos (IPC) para atender clientes e colaborar entre si.
- Protocolos genéricos podem não atender bem às necessidades de domínios específicos, como streaming de mídia ou correio eletrônico.
- Necessidade de interoperar com ecossistemas existentes que já falam um protocolo padronizado.

## Quando usar

- O domínio já possui protocolo consolidado (e-mail, streaming de mídia etc.) e há clientes e ferramentas que o utilizam.
- Os requisitos do domínio, como latência, fluxo contínuo ou semântica específica, não são bem atendidos por REST ou mensageria genérica.

### Quando evitar

- Existe protocolo genérico adequado, e a equipe ganharia mais com a familiaridade e as ferramentas de RPI ou Messaging.
- Seria necessário inventar um protocolo proprietário, com alto custo de manutenção e baixa interoperabilidade.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Semântica e desempenho ajustados ao domínio | Menor reaproveitamento de ferramentas e conhecimento genéricos da equipe |
| Interoperabilidade com clientes e servidores do ecossistema | Dependência de bibliotecas e infraestrutura específicas do protocolo |
| Evita adaptar um protocolo genérico a um uso para o qual não foi desenhado | Observabilidade, segurança e resiliência podem exigir soluções próprias |

## Diagrama

```mermaid
flowchart LR
    C["Cliente de domínio (ex.: player ou cliente de e-mail)"] -->|"protocolo do domínio (ex.: HLS, SMTP/IMAP)"| S["Serviço do domínio"]
    S -->|"respostas e fluxos no mesmo protocolo"| C
```

Cliente e serviço conversam diretamente usando um protocolo estabelecido para o domínio, sem camada genérica de RPI ou de mensageria.

## Padrões relacionados

- [Remote Procedure Invocation](./remote-procedure-invocation.md) — alternativa genérica de requisição/resposta síncrona.
- [Messaging](./messaging.md) — alternativa genérica de comunicação assíncrona por mensagens.

## Referência

- [Página do padrão no microservices.io](https://microservices.io/patterns/communication-style/domain-specific.html)
