---
title: Elastic Scale
pattern_slug: elastic-scale
category: Advanced
tags:
  - Performance Efficiency
  - Cost Optimization
  - Reliability
source: https://k8spatterns.com/
sidebar_label: "Elastic Scale"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/advanced/elastic-scale.mdx';

# Elastic Scale

## Descrição

O padrão Elastic Scale faz a capacidade de uma aplicação acompanhar a carga automaticamente, escalando em várias dimensões: horizontalmente (número de réplicas de Pod), verticalmente (requests e limits de cada Pod) e no nível do cluster (número de nós). Em vez de um humano observar a carga e decidir quanto escalar, o Kubernetes mede o uso real e ajusta o estado desejado.

A forma mais direta é o **HorizontalPodAutoscaler (HPA)**, que lê métricas (CPU e memória, métricas customizadas de Pod ou de objeto e métricas externas, como a profundidade de uma fila) e calcula as réplicas necessárias, proporcionais à razão entre o valor atual e o alvo. O **Vertical Pod Autoscaler (VPA)** recomenda ou aplica requests e limits ajustados ao consumo real, e o **Cluster Autoscaler** adiciona ou remove nós quando há Pods que não cabem ou nós ociosos. A escala manual, imperativa ou declarativa, continua válida para cargas previsíveis.

O HPA não reduz a zero Pods, e acordar uma aplicação parada exige um gatilho. Dois complementos preenchem essa lacuna e podem ser usados juntos. O **Knative** (Serving) escala aplicações HTTP sem estado com o Knative Pod Autoscaler, baseado em requisições concorrentes por Pod, e usa um Activator que segura as requisições enquanto a aplicação sai de zero. O **KEDA** é orientado a eventos e baseado em pull: um `ScaledObject` liga o alvo a um gatilho externo (fila ou tópico, por exemplo), o operador faz a ativação de 0 para 1 e o HPA, alimentado pelo serviço de métricas do KEDA, cuida de 1 a n. O `ScaledJob` do KEDA, por sua vez, inicia Jobs em vez de réplicas.
Os níveis são complementares e independentes: ajustar a própria aplicação, definir requests corretos (VPA), variar o número de Pods (HPA) e variar o número de nós (Cluster Autoscaler). Os autoscalers dependem de que os [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) estejam declarados, já que as porcentagens são calculadas sobre os requests.

## Problemas que resolve

- Cargas sazonais ou imprevisíveis, em que um número fixo de réplicas ou fica pequeno demais ou desperdiça recursos
- Dificuldade de dimensionar com precisão quantas réplicas e quantos recursos cada contêiner precisa
- Intervenção manual lenta e propensa a erro durante picos de tráfego
- Custo de infraestrutura pago em horários de baixa demanda
- Aplicações ociosas que continuam consumindo recursos, pois o HPA sozinho não escala a zero

## Quando usar

- Quando a carga varia ao longo do dia, da semana ou do mês, como em dias de pagamento de boletos ou de grandes campanhas
- Em serviços sem estado, que escalam bem horizontalmente
- Quando há uma métrica correlacionada ao número de Pods, como CPU, requisições por segundo ou tamanho da fila
- Quando o cluster roda em uma nuvem capaz de provisionar e remover nós sob demanda
- Com consumidores de fila ou tópico, ou cargas esporádicas que devem escalar a zero, usando KEDA; com serviços HTTP de tráfego em rajadas, usando Knative

## Quando evitar

- Quando a métrica escolhida não cai ao adicionar Pods (memória em aplicações que não liberam dados é o caso clássico), pois o HPA escalaria até o máximo
- Em aplicações com estado difícil de redistribuir, em que escalar horizontalmente é complexo ou arriscado
- Quando a carga é estável e previsível: um número fixo de réplicas é mais simples
- Quando os requests não foram definidos, já que as porcentagens de uso não têm referência
- Sem cuidado, quando HPA e VPA agem sobre as mesmas métricas de CPU e memória, que podem gerar escala dupla
- Quando a latência de partida a frio (cold start) após escalar a zero é inaceitável, como em um caminho crítico de pagamento

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Capacidade acompanha a demanda sem intervenção humana | Reação com atraso: coleta de métricas, ciclo do HPA e inicialização dos Pods |
| Menos custo, pois só se paga o que é preciso | Métricas mal escolhidas causam escala excessiva ou oscilação (thrashing) |
| Maior disponibilidade em picos de tráfego | VPA reinicia Pods para aplicar novos requests, o que pode causar interrupções |
| Escala em vários níveis, de Pods a nós | Configuração e ajuste fino são trabalhosos e dependem de experimentação |
| Escala a zero com Knative ou KEDA, sem custo quando ocioso | Complementos extras para instalar e operar, e partida a frio ao sair de zero |

- **Escolha da métrica:** prefira uma métrica correlacionada, de preferência linear, ao número de Pods, como CPU ou requisições por segundo.
- **Estabilização:** use janelas de estabilização e políticas de escala para evitar oscilações, principalmente na redução.
- **Limites:** defina mínimo e máximo de réplicas, para ter capacidade em picos e proteger o orçamento e as dependências, como o banco de dados.
- **Aplicar o HPA ao Deployment:** aplicá-lo a um ReplicaSet gerenciado perde a configuração a cada atualização.
- **Prontidão:** réplicas novas só devem receber tráfego quando prontas; combine com [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) e com um encerramento gracioso.
- **VPA no modo de recomendação:** começar com o modo que apenas sugere valores ajuda a ajustar requests sem disrupção.
- **Escolha entre HPA, Knative e KEDA:** o HPA usa métricas de recursos e não escala a zero; o Knative serve tráfego HTTP (push) e o KEDA, métricas externas como backlog de filas (pull). Não são excludentes.
- **Escala a zero:** defina um mínimo de réplicas maior que zero (por exemplo, `min-scale` no Knative) para caminhos sensíveis à latência.

## Diagrama

<Diagram />

O HPA compara o uso medido com o alvo e ajusta as réplicas do Deployment; se faltar espaço para os novos Pods, o Cluster Autoscaler aumenta o número de nós.

## Exemplo

O `pix-service` recebe picos nos horários de pagamento. Este HorizontalPodAutoscaler (`autoscaling/v2`) mantém a CPU média em 60% dos requests, entre 3 e 20 réplicas, sobe rápido e reduz devagar para evitar oscilações. O Deployment precisa declarar `resources.requests.cpu` e o cluster precisa ter o metrics-server.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pix-service
  namespace: fintech
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pix-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300 # espera 5 minutos antes de reduzir
```

## Padrões relacionados

- [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) — requests e limits declarados são a base dos cálculos de HPA, VPA e Cluster Autoscaler
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — o HPA deve ser aplicado ao Deployment, que preserva a escala nas atualizações
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — garante que réplicas recém-criadas só recebam tráfego quando estiverem prontas
- [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement) — define em quais nós os novos Pods são agendados, e dispara o Cluster Autoscaler quando não há espaço
- [Queue-Based Load Leveling](/architecture/cloud-design-patterns/messaging/queue-based-load-leveling) — a profundidade da fila é uma métrica externa útil para escalar consumidores, por exemplo com KEDA
- [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) — um Job também escala pelo paralelismo, e o `ScaledJob` do KEDA inicia Jobs conforme o trabalho externo
- [Competing Consumers](/architecture/cloud-design-patterns/messaging/competing-consumers) — escalar réplicas de consumidores aumenta o paralelismo sobre a mesma fila

## Referência

- [Kubernetes Patterns, capítulo 29: Elastic Scale](https://k8spatterns.com/)
- [Horizontal Pod Autoscaling (documentação do Kubernetes)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Node Autoscaling (documentação do Kubernetes)](https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/)
