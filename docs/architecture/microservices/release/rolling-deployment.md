---
title: Rolling Deployment
pattern_slug: rolling-deployment
category: Release
tags:
  - Reliability
  - Operational Excellence
  - Cost Optimization
source: https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/
sidebar_label: "Rolling Deployment"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/rolling-deployment.mdx';

# Rolling Deployment

## Descrição

Rolling Deployment substitui as instâncias da versão atual pelas da nova versão aos poucos, uma ou poucas de cada vez, sem dobrar o ambiente. Cada instância nova só entra no balanceamento depois de passar no health check, e só então uma instância antiga é removida. O ciclo se repete até que todas rodem a nova versão, mantendo sempre uma capacidade mínima no ar.

O ritmo é controlado por dois limites: quantas instâncias extras podem existir durante a troca e quantas podem ficar indisponíveis. É a estratégia padrão de orquestradores como o Kubernetes (`RollingUpdate`) e de grupos de auto scaling em nuvem.

## Problemas que resolve

- Indisponibilidade durante o deploy, sem o custo de manter um segundo ambiente completo.
- Trocas manuais de instância em clusters com muitas réplicas.
- Picos de carga causados por reiniciar todas as instâncias ao mesmo tempo.

## Quando usar

- Serviços sem estado, com várias réplicas atrás de um load balancer.
- Quando o custo de dobrar o ambiente, como no Blue-Green, não se justifica.
- Mudanças retrocompatíveis, em que duas versões podem atender ao mesmo tempo.

## Quando evitar

- Quando duas versões não podem coexistir, como em mudanças de contrato sem retrocompatibilidade: prefira parar e recriar, ou [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment).
- Quando é preciso controlar quais clientes veem a nova versão: prefira [Canary Release](/architecture/microservices/release/canary-release).
- Serviços com uma única instância, em que não há o que alternar.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Sem indisponibilidade e sem dobrar a infraestrutura | Duas versões atendem ao mesmo tempo durante a troca |
| Ritmo controlável por limites de excedente e indisponibilidade | Rollback lento, refazendo a troca no sentido contrário |
| Suporte nativo em orquestradores | Sem controle sobre quais clientes caem na nova versão |
| Capacidade mínima garantida o tempo todo | Um bug pode atingir boa parte do tráfego antes de ser detectado |

- **Health check é obrigatório:** sem uma verificação de prontidão confiável, o orquestrador avança a troca mesmo com instâncias novas quebradas.
- **Compatibilidade:** durante a janela de troca, requisições de um mesmo cliente podem cair em versões diferentes, então contratos e esquemas precisam funcionar com as duas.
- **Capacidade extra:** permitir uma instância excedente acelera a troca sem reduzir a capacidade; permitir indisponibilidade economiza recursos, mas reduz a folga durante o deploy.

## Diagrama

<Diagram />

O `pix-service` tem três réplicas e admite uma excedente. Uma réplica v2 sobe, passa no health check e substitui uma v1; o ciclo se repete até que só restem réplicas v2.

## Padrões relacionados

- [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment) — rollback imediato, ao custo de dobrar a capacidade.
- [Canary Release](/architecture/microservices/release/canary-release) — controla quem recebe a nova versão e por quanto tempo.
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — a estratégia `RollingUpdate` do Kubernetes, com `maxSurge` e `maxUnavailable`.
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — a verificação de prontidão que libera cada passo da troca.
- [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) — plataforma que executa a troca automaticamente.

## Referência

- [Kubernetes — Performing a Rolling Update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
