---
title: Community API
pattern_slug: community-api
category: Foundations
tags:
  - Security
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Community API"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/foundations/community-api.mdx';

# Community API

## Descrição

O padrão Community API restringe a visibilidade e o acesso de uma API a um grupo fechado de usuários que pertence a várias entidades jurídicas, como empresas, organizações sem fins lucrativos e governos. A API e seus recursos de implementação ficam implantados em um local de acesso restrito, por exemplo uma extranet, e a descrição da API é compartilhada apenas com o público autorizado.

Ela combina elementos das vizinhas Public API e Solution-Internal API. Como uma API pública, pode ter um modelo de preços próprio da comunidade e exige contrato, segurança e confiabilidade bem cuidados. Como uma API interna, pode manter os endpoints próximos de suas implementações. O desenho segue o mesmo roteiro da Public API: endpoints, operações, representações, qualidade de serviço e ciclo de vida.

O que a distingue é a governança coletiva: nomeia-se um responsável pela API em nível de comunidade, busca-se financiamento compartilhado e organiza-se o suporte entre os membros.

## Problemas que resolve

- Compartilhar uma API entre organizações diferentes sem torná-la pública
- Restringir quem enxerga a API e sua documentação a um grupo conhecido
- Dar a esse grupo um ponto de integração com regras e custos acordados em conjunto
- Evitar a duplicação de integrações bilaterais entre cada par de membros

## Quando usar

- Quando um consórcio de instituições financeiras compartilha uma API de conciliação ou de consulta de participantes
- Quando existe uma rede fechada, como extranet, para os membros da comunidade
- Quando as regras de uso, o financiamento e o suporte são decididos coletivamente
- Quando a confiança entre os membros é maior que na internet aberta, mas ainda não é a de uma mesma organização

## Quando evitar

- Quando qualquer parte interessada deveria poder usar a API: escolha a [Public API](/architecture/api-patterns/foundations/public-api)
- Quando só componentes de uma mesma aplicação a consomem: use a [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api)
- Quando não há um responsável nem financiamento comum para sustentar a API
- Quando a comunidade é pequena demais para justificar a governança de um contrato compartilhado

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Integração única para todos os membros, no lugar de acordos bilaterais | Exige governança, dono comum e financiamento compartilhado |
| Acesso e documentação restritos ao público certo | Infraestrutura de rede e de segurança para a extranet |
| Regras e custos adequados à comunidade | Decisões de mudança dependem de consenso entre organizações |
| Menor exposição que uma API pública | Menos escala de uso e menos retorno para amortizar o investimento |

- **Governança:** defina quem decide a evolução do contrato e como mudanças são comunicadas aos membros.
- **Segurança:** a rede restrita ajuda, mas não substitui autenticação e autorização por membro.
- **Suporte:** parte do suporte pode vir dos próprios membros, o que precisa ser combinado.

## Diagrama

<Diagram />

Somente os membros da comunidade alcançam a API, que fica em uma rede de acesso restrito.

## Exemplo

Um consórcio de cooperativas de crédito usa uma API comum para consultar se um CPF já tem contrato ativo em outro membro. Só instituições cadastradas, dentro da extranet, chamam o endpoint, e cada chamada se identifica pelo membro.

```http
POST /consortium/v1/loan-contracts/lookup HTTP/1.1
Host: api.consortium.example
X-Member-Id: coop-042
Content-Type: application/json

{ "taxId": "123.456.789-09" }

HTTP/1.1 200 OK
Content-Type: application/json

{ "activeContracts": 1, "totalOutstanding": { "amountCents": 1850000, "currency": "BRL" } }
```

O documento que descreve esse endpoint é distribuído apenas aos membros, não publicado na internet.

## Padrões relacionados

- [Public API](/architecture/api-patterns/foundations/public-api) — o irmão aberto; a Community API herda dela boa parte das práticas de contrato, documentação e suporte
- [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) — o irmão fechado dentro de uma aplicação, do qual a Community API pode tomar a proximidade com a implementação
- [Backend Integration](/architecture/api-patterns/foundations/backend-integration) e [Frontend Integration](/architecture/api-patterns/foundations/frontend-integration) — os tipos de integração que a API de comunidade pode servir
- [API Description](/architecture/api-patterns/documentation/api-description) — compartilhada apenas com o público restrito
- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) e [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan) — acordos e custos definidos em conjunto pela comunidade
- [Open Host Service](/design/ddd/context-mapping/open-host-service) e [Published Language](/design/ddd/context-mapping/published-language) — relação de contexto em que um protocolo comum é oferecido a vários consumidores

## Referência

- [Patterns for API Design, capítulo 4: Community API](https://api-patterns.org/)
