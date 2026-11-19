---
title: Public API
pattern_slug: public-api
category: Foundations
tags:
  - Security
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Public API"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/foundations/public-api.mdx';

# Public API

## Descrição

O padrão Public API disponibiliza uma API na internet pública, acompanhada de uma descrição detalhada de suas propriedades funcionais e não funcionais, para um número ilimitado ou desconhecido de clientes fora da organização. O público-alvo não é limitado, embora o acesso costume ser controlado por chaves de API.

Como os consumidores podem estar em qualquer lugar e nem conhecer o provedor, a API precisa de um desenho completo: endpoints, operações, representações das mensagens, garantias de qualidade de serviço e um modelo de suporte ao ciclo de vida. Isso inclui escolher padrões de responsabilidade e de evolução, como marcar a API como um Processing Resource, adotar Version Identifiers e Semantic Versioning.

Segurança e confiabilidade ganham peso: use API Keys ou outros mecanismos, endureça a API e invista em documentação e suporte. Do ponto de vista da economia de APIs, defina um Pricing Plan, gerencie assinaturas e cobrança, e considere Rate Limits para planos gratuitos. Os termos de uso, incluindo uso justo e responsabilidades, entram em um Service Level Agreement que o consumidor aceita para usar a API. Por terem valor jurídico, esses documentos devem ser escritos ou revisados por especialistas.

## Problemas que resolve

- Atender clientes desconhecidos, distribuídos por regiões e organizações diferentes
- Permitir que terceiros construam produtos sobre as capacidades da organização
- Controlar acesso, consumo e cobrança sem conhecer cada consumidor de antemão
- Comunicar garantias, limites e termos de uso a quem nunca conversou com o provedor

## Quando usar

- Quando a fintech oferece uma API de cobranças Pix e consulta de extrato para lojistas e desenvolvedores externos
- Quando o objetivo é construir um ecossistema de parceiros e integradores
- Quando a API é parte do produto e pode ter planos e cobrança
- Quando se aceita assumir compromissos de estabilidade e de disponibilidade com o público

## Quando evitar

- Quando o público é um grupo fechado de organizações: prefira a [Community API](/architecture/api-patterns/foundations/community-api)
- Quando só serviços da própria aplicação a usam: uma [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) basta e custa menos
- Quando a organização não pode sustentar suporte, documentação e estabilidade a longo prazo
- Para operações sensíveis sem uma estratégia sólida de autenticação, autorização e limitação de uso

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Alcance amplo e possibilidade de ecossistema e receita | Superfície de ataque exposta à internet inteira |
| Consumidores independentes, sem acordo individual | Mudanças quebram clientes que você não conhece |
| Contrato e termos explícitos criam expectativas claras | Compromisso de suporte, documentação e disponibilidade |
| Modelos de negócio com planos e limites | Exige gestão de assinaturas, cobrança e revisão jurídica |

- **Estabilidade:** quanto mais público o contrato, mais caro mudá-lo; planeje versionamento e política de descontinuação desde o início.
- **Segurança:** chaves de API são um mínimo; considere ainda autenticação forte, limites e monitoramento de abuso.
- **Erros:** como provedor e cliente podem não se conhecer, as respostas de erro precisam ser autoexplicativas.

## Diagrama

<Diagram />

Clientes de qualquer origem acessam o mesmo ponto público, acompanhado de documentação, plano de preços, limites e acordo de nível de serviço.

## Exemplo

A fintech publica uma API de cobranças Pix para lojistas. O consumidor se identifica por uma chave de API, e o provedor aplica limites e informa o consumo restante.

```http
POST /v1/pix-charges HTTP/1.1
Host: api.fintech.example
X-Api-Key: pk_live_4f9c1a7e
Content-Type: application/json

{ "amountCents": 15990, "currency": "BRL", "description": "Pedido 4821" }

HTTP/1.1 201 Created
Content-Type: application/json
X-RateLimit-Remaining: 97

{ "id": "pc-5521", "status": "PENDING", "amountCents": 15990, "currency": "BRL" }
```

O prefixo `/v1` e os cabeçalhos de limite mostram os compromissos que uma API pública costuma assumir: versão explícita e consumo transparente.

## Padrões relacionados

- [Community API](/architecture/api-patterns/foundations/community-api) — visibilidade restrita a um grupo fechado de organizações, com traços de Public API
- [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) — o oposto: acessível somente dentro da aplicação
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — identifica e controla o acesso dos consumidores; difere do [Access Token](/architecture/microservices/security/access-token), que carrega a identidade e as permissões de uma requisição
- [API Description](/architecture/api-patterns/documentation/api-description) — contrato legível por máquina e por pessoas
- [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan), [Rate Limit](/architecture/api-patterns/documentation/rate-limit) e [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — o lado comercial e operacional da API pública
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) e [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning) — gestão da evolução sem surpreender consumidores
- [Throttling](/architecture/cloud-design-patterns/resiliency/throttling) e [Rate Limiting](/architecture/cloud-design-patterns/resiliency/rate-limiting-pattern) — o mecanismo de proteção que sustenta os limites declarados
- [API Gateway](/architecture/microservices/external-api/api-gateway) — ponto de entrada comum que aplica autenticação e limites

## Referência

- [Patterns for API Design, capítulo 4: Public API](https://api-patterns.org/)
