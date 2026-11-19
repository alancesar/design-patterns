---
title: Blue-Green Deployment
pattern_slug: blue-green-deployment
category: Release
tags:
  - Reliability
  - Operational Excellence
source: https://martinfowler.com/bliki/BlueGreenDeployment.html
sidebar_label: "Blue-Green Deployment"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/blue-green-deployment.mdx';

# Blue-Green Deployment

## Descrição

Blue-Green Deployment mantém dois ambientes de produção idênticos, chamados *blue* e *green*, e só um deles recebe tráfego de cada vez. A nova versão é implantada e testada no ambiente ocioso e, quando está pronta, o roteador passa todo o tráfego para ele de uma vez. O ambiente anterior continua de pé, com a versão antiga, e serve de rollback imediato.

A troca acontece em um único ponto, como um load balancer, um `Service` do Kubernetes ou um registro de DNS, e por isso é rápida e reversível. Depois que a nova versão se prova estável, o ambiente antigo vira o ocioso e recebe o próximo release. Martin Fowler descreveu a técnica a partir do trabalho de Dan North e Jez Humble em *Continuous Delivery*.

## Problemas que resolve

- Indisponibilidade durante o deploy, quando o serviço precisa parar para trocar de versão.
- Rollback lento e arriscado, que exige reimplantar a versão anterior às pressas.
- Falta de um lugar para testar a nova versão na infraestrutura real de produção antes de expô-la aos clientes.

## Quando usar

- Serviços que exigem deploy sem indisponibilidade e rollback em segundos.
- Releases que precisam de um teste de fumaça em produção antes de receber tráfego.
- Quando a infraestrutura permite dobrar a capacidade durante a troca.

## Quando evitar

- Quando manter dois ambientes completos é caro demais: prefira [Rolling Deployment](/architecture/microservices/release/rolling-deployment).
- Quando a mudança é arriscada para o negócio e precisa ser exposta aos poucos: prefira [Canary Release](/architecture/microservices/release/canary-release).
- Mudanças de esquema que a versão antiga não suporta, porque o rollback deixa de ser seguro.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Deploy sem indisponibilidade | Dobro da capacidade durante a troca |
| Rollback imediato, trocando o roteamento de volta | O banco de dados costuma ser compartilhado pelos dois ambientes |
| Nova versão testada em produção antes de receber tráfego | Todos os clientes passam para a nova versão de uma vez |
| Troca simples, em um único ponto | Sessões e conexões longas precisam ser drenadas na troca |

- **Banco compartilhado:** como blue e green usam o mesmo banco, mudanças de esquema devem ser compatíveis com as duas versões. Separe a migração em etapas: primeiro adicione colunas e tabelas, depois troque o tráfego e só no release seguinte remova o que ficou obsoleto.
- **Exposição total:** um bug que só aparece com tráfego real atinge todos os clientes ao mesmo tempo; o rollback é rápido, mas não evita o impacto.
- **Mensageria:** consumidores de fila do ambiente ocioso também precisam ficar parados, ou as duas versões vão disputar as mesmas mensagens.

## Diagrama

<Diagram />

O `pix-service` v2 sobe no ambiente green, passa pelos testes de fumaça e recebe o tráfego quando o load balancer é reapontado. Se algo der errado, o roteamento volta para o blue.

## Padrões relacionados

- [Canary Release](/architecture/microservices/release/canary-release) — expõe a nova versão a uma parcela do tráfego em vez de trocar tudo de uma vez.
- [Rolling Deployment](/architecture/microservices/release/rolling-deployment) — alternativa que não exige dobrar a capacidade.
- [Feature Toggle](/architecture/microservices/release/feature-toggle) — separa a ativação da funcionalidade da troca de versão.
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — mostra como montar Blue-Green com `Deployment` e `Service` no Kubernetes.
- [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring) — confirma que o ambiente ocioso está saudável antes da troca.
- [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) — plataforma que automatiza a troca de roteamento.

## Referência

- [Martin Fowler — BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
