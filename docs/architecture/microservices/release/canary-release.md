---
title: Canary Release
pattern_slug: canary-release
category: Release
tags:
  - Reliability
  - Operational Excellence
source: https://martinfowler.com/bliki/CanaryRelease.html
sidebar_label: "Canary Release"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/canary-release.mdx';

# Canary Release

## Descrição

Canary Release libera a nova versão de um serviço para uma pequena parcela dos usuários antes de levá-la a todos. A nova versão roda ao lado da atual, o roteador desvia para ela uma fatia do tráfego, como 1% ou 5%, e a equipe compara erros, latência e métricas de negócio entre as duas. Se os números se mantêm, a fatia cresce em etapas até 100%; se pioram, o tráfego volta para a versão atual.

O nome vem dos canários que mineiros levavam para detectar gases tóxicos: um grupo pequeno é exposto primeiro para proteger os demais. A seleção do grupo pode ser aleatória, por região, por tipo de cliente ou começar por usuários internos.

## Problemas que resolve

- Bugs e regressões de desempenho que só aparecem com tráfego e dados reais.
- Releases que expõem todos os clientes ao mesmo risco de uma vez.
- Falta de critério objetivo para decidir se uma versão está pronta para todos.

## Quando usar

- Mudanças de maior risco para o negócio, como uma nova regra de cobrança ou de análise de crédito.
- Serviços com tráfego suficiente para que uma fatia pequena gere métricas confiáveis.
- Quando existe observabilidade que separa métricas por versão.

## Quando evitar

- Serviços com pouco tráfego, em que 1% das requisições não gera sinal estatístico.
- Mudanças em que duas versões não podem coexistir, como contratos ou esquemas incompatíveis.
- Quando não há como rotear tráfego por porcentagem ou por grupo de usuários.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Problemas atingem uma parcela pequena dos clientes | Duas versões em produção ao mesmo tempo |
| Decisão de avançar baseada em métricas reais | Exige roteamento por porcentagem e métricas por versão |
| Rollback rápido, reduzindo a fatia a zero | Release mais lento, em várias etapas |
| Não exige dobrar a infraestrutura | Usuários podem alternar entre versões se o roteamento não for estável |

- **Critérios definidos antes:** os limites que fazem o release avançar ou voltar, como taxa de erro e latência no p99, devem ser decididos antes do lançamento e, de preferência, verificados automaticamente.
- **Roteamento estável:** associe o cliente a uma versão (por conta, sessão ou cabeçalho) para que ele não veja comportamentos diferentes a cada requisição.
- **Compatibilidade:** como as versões convivem por horas ou dias, mudanças de esquema e de contrato precisam ser retrocompatíveis.

## Diagrama

<Diagram />

O gateway envia 5% das cobranças Pix para a v2. Se as métricas da v2 ficam dentro do limite, a fatia sobe para 25%, 50% e 100%; se não, volta a zero.

## Padrões relacionados

- [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment) — troca todo o tráfego de uma vez, sem exposição gradual.
- [Rolling Deployment](/architecture/microservices/release/rolling-deployment) — também mistura versões, mas sem controle sobre quem recebe a nova.
- [Feature Toggle](/architecture/microservices/release/feature-toggle) — faz a liberação gradual no código, por funcionalidade, em vez de por versão.
- [Gateway Routing](/architecture/cloud-design-patterns/gateways-and-edge/gateway-routing) — o roteamento por peso que divide o tráfego entre as versões.
- [Application Metrics](/architecture/microservices/observability/application-metrics) — as métricas que decidem se o canário avança.
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — mostra como montar um canário com réplicas no Kubernetes.

## Referência

- [Martin Fowler — CanaryRelease](https://martinfowler.com/bliki/CanaryRelease.html)
