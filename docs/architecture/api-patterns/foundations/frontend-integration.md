---
title: Frontend Integration
pattern_slug: frontend-integration
category: Foundations
tags:
  - Decoupling
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Frontend Integration"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/foundations/frontend-integration.mdx';

# Frontend Integration

## Descrição

O padrão Frontend Integration expõe os serviços do backend de uma aplicação distribuída a um ou mais frontends por meio de uma API remota baseada em mensagens. É a API que conecta a interface do usuário, fisicamente separada da lógica de negócio e do armazenamento, ao processamento e aos dados que ela precisa exibir ou alterar.

O consumidor dessa API é sempre um cliente que atende pessoas: um aplicativo móvel, uma aplicação web ou o frontend de outro sistema. A porta de entrada natural no backend é a camada de lógica de negócio, que já concentra controle de acesso, transações e regras. Na prática, costuma ser uma API de recursos sobre HTTP, mas gRPC, WebSockets e GraphQL também servem. A API pode ter propósito geral, atendendo a todos os clientes, ou ser especializada por tipo de cliente, como nos Backends for Frontends.

Depois de escolher esse tipo de integração, ainda é preciso decidir a visibilidade da API (pública, de comunidade ou interna), montar as mensagens, definir os papéis dos endpoints, uma estratégia de versionamento e a descrição do contrato.

## Problemas que resolve

- Popular e atualizar a interface do usuário com resultados de processamento, buscas e detalhes de entidades que vivem no servidor
- Permitir que o frontend dispare atividades no backend ou envie dados a ele
- Manter a interface independente da lógica de negócio e do armazenamento, que mudam em ritmos diferentes
- Dar a clientes de tipos distintos (móvel, web, parceiros) um contrato estável de acesso

## Quando usar

- Quando um aplicativo móvel ou web precisa consultar saldo, extrato ou iniciar um Pix em um backend remoto
- Quando a interface e o backend são implantados e evoluem separadamente
- Quando vários frontends compartilham as mesmas capacidades do servidor
- Quando as mensagens precisam ser pensadas para a experiência do usuário, com menos idas e voltas e respostas moldadas à tela

## Quando evitar

- Para integrar dois sistemas de backend entre si: use [Backend Integration](/architecture/api-patterns/foundations/backend-integration), cujas necessidades de protocolo e de estrutura de mensagens são outras
- Quando a interface roda no mesmo processo da lógica e não há fronteira de rede
- Quando uma mesma API tentaria atender frontends e backends ao mesmo tempo, o que obriga a compromissos ou a opções que complicam o uso

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Interface desacoplada da lógica de negócio e do armazenamento | Cada chamada atravessa a rede, com latência e falhas parciais |
| Contrato claro entre quem constrói a tela e quem constrói o servidor | O contrato precisa ser versionado e documentado com cuidado |
| Possibilidade de moldar mensagens para as necessidades da experiência | Várias especializações por cliente multiplicam o que é preciso manter |
| Reuso das mesmas capacidades por diversos frontends | Uma API genérica pode servir mal a todos os clientes |

- **Visibilidade:** a mesma integração pode ser pública, de comunidade ou interna; a escolha muda as exigências de segurança e de estabilidade.
- **Tecnologia:** HTTP é a escolha natural, enquanto GraphQL promete reduzir busca em excesso ou insuficiente, ao custo de outra superfície a operar.
- **Generalista ou especializada:** uma API única simplifica a manutenção; uma por tipo de cliente aproxima a resposta do que cada tela precisa.

## Diagrama

<Diagram />

O frontend nunca toca a lógica ou os dados diretamente: tudo passa pela API remota exposta pelo backend.

## Exemplo

O aplicativo da fintech mostra o saldo e o extrato da conta e permite criar uma cobrança Pix. As mensagens são pensadas para a tela: o saldo vem pronto, com `Money` em centavos inteiros, nunca em ponto flutuante.

```http
GET /accounts/acc-7781/overview HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "accountId": "acc-7781",
  "balance": { "amountCents": 125090, "currency": "BRL" },
  "recentEntries": [
    { "id": "le-9001", "description": "Pix recebido", "amountCents": 5000, "currency": "BRL" },
    { "id": "le-9000", "description": "Boleto pago", "amountCents": -23000, "currency": "BRL" }
  ]
}
```

```http
POST /accounts/acc-7781/pix-charges HTTP/1.1
Content-Type: application/json

{ "amountCents": 5000, "currency": "BRL", "description": "Aluguel de novembro" }

HTTP/1.1 201 Created
Location: /pix-charges/pc-3310
```

Uma única chamada de visão geral evita que o aplicativo monte a tela com várias requisições separadas.

## Padrões relacionados

- [Backend Integration](/architecture/api-patterns/foundations/backend-integration) — o outro tipo de integração, entre backends em vez de entre interface e servidor
- [Public API](/architecture/api-patterns/foundations/public-api), [Community API](/architecture/api-patterns/foundations/community-api) e [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) — as visibilidades que a API de frontend pode assumir
- [Backends for Frontends](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) — especializa a API por tipo de cliente; é uma forma de organizar a Frontend Integration
- [Remote Facade](/design/poeaa/distribution/remote-facade) — fachada de granularidade grossa que costuma sustentar esse tipo de API
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) e [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — deixam o cliente moldar a resposta à tela
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — apoia a evolução do contrato sem quebrar clientes instalados

## Referência

- [Patterns for API Design, capítulo 4: Frontend Integration](https://api-patterns.org/)
