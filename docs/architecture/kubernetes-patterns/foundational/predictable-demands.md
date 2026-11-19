---
title: Predictable Demands
pattern_slug: predictable-demands
category: Foundational
tags:
  - Reliability
  - Cost Optimization
  - Performance Efficiency
source: https://k8spatterns.com/
sidebar_label: "Predictable Demands"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/foundational/predictable-demands.mdx';

# Predictable Demands

## Descrição

O padrão Predictable Demands consiste em declarar, no manifesto de cada workload, as dependências de execução e o perfil de recursos de seus contêineres, para que o Kubernetes saiba onde colocá-los e como tratá-los quando o cluster fica sob pressão. Sem essa declaração, a plataforma enxerga cada contêiner como uma caixa-preta e só pode descartá-lo quando os nós ficam cheios.

Há dois tipos de demanda. As **dependências de execução** são recursos que precisam existir para o contêiner funcionar: volumes persistentes (`PersistentVolumeClaim`), `ConfigMap` e `Secret` consumidos como variáveis ou arquivos, ou portas fixas no host (`hostPort`). Elas restringem em quais nós o Pod pode rodar, ou até impedem que ele inicie. Os **perfis de recursos** são os `requests` (o mínimo de CPU e memória de que o contêiner precisa) e os `limits` (o teto que pode consumir). O scheduler usa apenas os `requests` para escolher o nó.

A combinação entre `requests` e `limits` define a classe de qualidade de serviço do Pod (Best-Effort, Burstable ou Guaranteed), que determina quem é removido primeiro quando um nó fica sem memória. CPU é um recurso compressível, e o contêiner é apenas limitado (throttled); memória é incompressível, e o contêiner que a excede é encerrado. Complementam o padrão `PriorityClass`, `ResourceQuota` e `LimitRange`, que organizam prioridades e limites por namespace.

## Problemas que resolve

- Pods colocados em nós sem capacidade real, causando lentidão, throttling ou falta de memória
- Contêineres encerrados sem aviso por consumirem memória acima do que o nó podia oferecer
- Planejamento de capacidade feito no escuro, sem saber quanto cada serviço precisa
- Um time ou serviço consumindo todos os recursos de um cluster compartilhado e afetando os demais
- Pods que ficam agendados, mas não iniciam, porque um `ConfigMap`, `Secret` ou volume esperado não existe

## Quando usar

- Em todo workload executado em um cluster compartilhado, como `requests` de CPU e memória para cada contêiner
- Quando o serviço precisa de armazenamento persistente, configuração externa ou portas específicas
- Quando há serviços críticos (como o processamento de Pix) que devem ser os últimos a sofrer eviction
- Para fazer o planejamento de capacidade e dimensionar os nós com base em perfis medidos em testes de carga

## Quando evitar

- Em experimentos descartáveis ou ambientes de desenvolvimento locais, em que a classe Best-Effort é aceitável
- Quando os valores seriam chutes sem medição: números inventados distorcem o scheduler e desperdiçam capacidade
- Para `hostPort`, salvo necessidade real, pois limita a um Pod por nó e reduz a flexibilidade de agendamento
- Para `limits` de CPU muito apertados em serviços sensíveis a latência, que sofrem throttling mesmo com o nó ocioso

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Agendamento previsível, com Pods em nós que realmente comportam sua demanda | Exige medir e revisar os perfis de recursos à medida que o serviço evolui |
| Prioridade clara entre workloads quando os nós ficam sob pressão | Valores altos demais desperdiçam capacidade e aumentam o custo de infraestrutura |
| Base concreta para capacidade e custo por ambiente | Valores baixos demais causam throttling de CPU ou encerramento por falta de memória |
| Isolamento entre times via `ResourceQuota` e `LimitRange` | Prioridades mal definidas podem causar preempção de Pods importantes de outros times |

- **Classe de QoS:** `requests` igual a `limits` coloca o Pod em Guaranteed, a mais protegida; use para serviços que não podem ser removidos, como o ledger.
- **Medição:** use testes de carga e métricas reais para escolher os valores, em vez de copiá-los de outro serviço.
- **Prioridade versus QoS:** a `PriorityClass` influencia a ordem de agendamento e a preempção, enquanto a QoS influencia a ordem de eviction no nó; são mecanismos independentes.
- **Governança:** `ResourceQuota` limita o total por namespace e `LimitRange` define valores mínimos, máximos e padrão por contêiner.

## Diagrama

<Diagram />

O scheduler usa os `requests` e as dependências declaradas para escolher um nó com capacidade; já os `limits` valem em tempo de execução, limitando a CPU e encerrando o contêiner que excede a memória.

## Exemplo

O `pix-service` declara que precisa de um `ConfigMap`, reserva 250 milicores e 256 MiB e aceita crescer até o dobro, e usa uma `PriorityClass` para ser agendado antes de workloads menos importantes.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: payments-critical
value: 100000
globalDefault: false
description: "Realtime payment services"
---
apiVersion: v1
kind: Pod
metadata:
  name: pix-service
  namespace: fintech
  labels:
    app: pix-service
spec:
  priorityClassName: payments-critical
  containers:
    - name: pix-service
      image: registry.fintech.example/pix-service:1.4.2
      envFrom:
        - configMapRef:
            name: pix-service-config   # dependência: precisa existir
      resources:
        requests:
          cpu: 250m
          memory: 256Mi
        limits:
          cpu: 500m
          memory: 512Mi
```

Como `requests` e `limits` diferem, o Pod é Burstable; para torná-lo Guaranteed, bastaria igualar os dois valores.

## Padrões relacionados

- [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement) — usa os perfis declarados aqui para decidir em qual nó cada Pod será executado
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — outro contrato entre a aplicação e a plataforma, voltado ao estado de saúde em vez dos recursos
- [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale) — os `requests` são a base de cálculo do autoscaling por utilização
- [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource) — `ConfigMap` e `Secret` são dependências de execução declaradas por este padrão
- [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) — a plataforma de execução que consome essas declarações para rodar os serviços

## Referência

- [Kubernetes Patterns, capítulo 2: Predictable Demands](https://k8spatterns.com/)
- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)
