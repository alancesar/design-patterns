---
title: Daemon Service
pattern_slug: daemon-service
category: Behavioral
tags:
  - Operational Excellence
  - Reliability
source: https://k8spatterns.com/
sidebar_label: "Daemon Service"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/behavioral/daemon-service.mdx';

# Daemon Service

## Descrição

O padrão Daemon Service executa um Pod de infraestrutura em cada nó do cluster, ou em um subconjunto escolhido de nós, usando o recurso DaemonSet para ampliar as capacidades da plataforma. Diferente de um ReplicaSet, cujo número de réplicas segue a demanda da aplicação, o DaemonSet não se orienta pela carga: o objetivo é manter exatamente um Pod por nó elegível, e novos nós recebem o Pod automaticamente.

É o modelo típico para coletores de logs, agentes de monitoramento, plugins de rede e de armazenamento e componentes de segurança que precisam estar junto ao nó. O Pod pode ser restrito com `nodeSelector` ou afinidade, tolerar taints para rodar em nós dedicados e usar prioridade alta para não ser despejado antes das aplicações. Como esses Pods costumam acessar recursos do nó, como o sistema de arquivos ou a rede do host, a configuração de privilégios merece atenção. Atualizações usam `updateStrategy`, em geral `RollingUpdate` com limite de indisponibilidade.

Outras diferenças em relação ao ReplicaSet: os Pods do DaemonSet já nascem com `nodeName` definido, então não dependem do scheduler e podem rodar antes dele, o que permite usar o DaemonSet para os próprios componentes do Kubernetes; por isso o campo `unschedulable` do nó não é respeitado; e esses Pods são tratados com prioridade maior por outros controladores, como o descheduler, que evita despejá-los, e o cluster autoscaler, que os gerencia à parte.

## Problemas que resolve

- Funções de plataforma que precisam rodar em todos os nós, como coleta de logs e métricas
- Agentes que dependem de recursos locais do nó, como discos, dispositivos e a rede do host
- Garantir cobertura automática quando o cluster ganha ou perde nós, sem intervenção manual
- Componentes de infraestrutura que devem ter prioridade sobre as cargas de aplicação

## Quando usar

- Para agentes de observabilidade, coletores de logs e exportadores de métricas por nó
- Para componentes de rede, de armazenamento e de segurança que operam no nível do nó
- Quando um recurso existe só em alguns nós, como hardware especial, e o Pod deve acompanhá-lo
- Quando a quantidade de Pods deve acompanhar o número de nós, e não a carga da aplicação

## Quando evitar

- Para cargas de aplicação comuns, cuja escala deve seguir a demanda: use um Deployment
- Quando um único Pod por nó é desperdício e poucas instâncias bastam
- Quando o trabalho é finito: use um [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job)
- Quando a funcionalidade pode ser entregue por um [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) ao lado de cada aplicação, sem acesso ao nó

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Cobertura automática de todos os nós, inclusive os novos | Consumo de CPU e memória em cada nó, descontado da capacidade das aplicações |
| Acesso direto a recursos locais do nó | Privilégios elevados ampliam a superfície de ataque |
| Prioridade e tolerâncias para rodar em nós dedicados | Um agente defeituoso afeta todos os nós de uma vez |
| Modelo declarativo, sem scripts de instalação por máquina | Atualizações em todos os nós exigem estratégia e limite de indisponibilidade |

- **Recursos:** declare requests e limits, pois o agente compete com as aplicações pela capacidade do nó.
- **Tolerâncias:** sem `tolerations`, o Pod não roda em nós com taints, como os do plano de controle ou de hardware dedicado.
- **Prioridade:** use uma `priorityClassName` alta para que agentes essenciais não sejam despejados por pressão de recursos.
- **Segurança:** conceda apenas as capacidades e os volumes do host de fato necessários.
- **Atualização:** ajuste `maxUnavailable` para limitar quantos nós ficam temporariamente sem o agente.
- **Acesso aos Pods:** há quatro formas: um Service com o mesmo seletor (balanceado para um nó qualquer), um Service headless que devolve os IPs de todos os Pods, `hostPort` no IP do nó (o que limita onde o Pod cabe) ou o próprio Pod enviando dados a um destino conhecido (push).
- **Static Pods:** o kubelet também pode executar Pods definidos em um diretório local, sem controlador nem health checks; o DaemonSet é mais integrado à plataforma e é o recomendado.

## Diagrama

<Diagram />

O DaemonSet mantém um Pod do agente em cada nó, e cada agente encaminha os logs dos Pods daquele nó, como os de `pix-service` e `ledger-service`, para o coletor central.

## Exemplo

Um agente de logs da fintech em todos os nós, inclusive os com taints de carga dedicada, com prioridade alta e leitura dos logs do host.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-agent
  namespace: fintech
spec:
  selector:
    matchLabels:
      app: log-agent
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: log-agent
    spec:
      priorityClassName: system-node-critical
      tolerations:
        - operator: Exists
          effect: NoSchedule
      containers:
        - name: agent
          image: registry.fintech.example/log-agent:2.3.0
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
          volumeMounts:
            - name: varlog
              mountPath: /var/log
              readOnly: true
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

O volume `hostPath` é somente leitura e a atualização troca um nó por vez, o que limita o impacto de uma versão com defeito.

## Padrões relacionados

- [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) — entrega capacidades junto a cada aplicação, enquanto o DaemonSet as entrega junto a cada nó
- [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement) — seletores, afinidades e taints determinam em quais nós o DaemonSet roda
- [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) — requests e limits evitam que o agente prejudique as aplicações do nó
- [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) — contraste entre processos contínuos por nó e tarefas finitas
- [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) — o extremo oposto, com uma única instância em todo o cluster

## Referência

- [Kubernetes Patterns, capítulo 9: Daemon Service](https://k8spatterns.com/)
- [DaemonSet na documentação do Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
