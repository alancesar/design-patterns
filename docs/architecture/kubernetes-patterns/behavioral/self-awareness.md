---
title: Self Awareness
pattern_slug: self-awareness
category: Behavioral
tags:
  - Operational Excellence
  - Performance Efficiency
source: https://k8spatterns.com/
sidebar_label: "Self Awareness"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/behavioral/self-awareness.mdx';

# Self Awareness

## Descrição

O padrão Self Awareness permite que uma aplicação conheça informações sobre si mesma e sobre o ambiente em que roda, usando a Downward API do Kubernetes para injetar metadados do Pod por variáveis de ambiente ou arquivos. A aplicação lê esses valores localmente, sem precisar de um cliente da API do Kubernetes e sem depender da plataforma.

Mesmo aplicações sem estado e descartáveis às vezes precisam saber coisas que só existem em tempo de execução: nome e IP do Pod, nome do nó, namespace e conta de serviço. Outras informações vêm da definição do Pod, como requests e limits de CPU e memória, usadas para ajustar o tamanho de pools de threads ou do heap. Há ainda dados que podem mudar com o Pod em execução, como labels e annotations. Com `fieldRef` e `resourceFieldRef`, o desenvolvedor escolhe as chaves de interesse e o Kubernetes preenche os valores. Variáveis de ambiente são fixadas na criação do contêiner; já um volume `downwardAPI` expõe arquivos que são atualizados quando labels e annotations mudam. Para necessidades além disso, como listar outros Pods, a aplicação precisa consultar a API do Kubernetes diretamente, com as permissões de RBAC adequadas.

## Problemas que resolve

- Identificar a instância em logs, métricas e traços, com o nome do Pod e do nó
- Ajustar o comportamento ao que foi reservado, como o tamanho de pools e de memória conforme os limits
- Acessar labels e annotations que mudam durante a execução, sem reiniciar
- Evitar acoplamento da aplicação ao cliente da API do Kubernetes só para ler dados básicos

## Quando usar

- Quando a aplicação precisa do nome, do IP, do namespace ou do nó para logs, métricas ou registro em serviços externos
- Para dimensionar a JVM, pools de conexões ou de threads com base em requests e limits do contêiner
- Quando labels e annotations alteram o comportamento e devem ser lidos em tempo de execução
- Para manter a aplicação agnóstica ao Kubernetes, com os dados chegando por ambiente e arquivos

## Quando evitar

- Quando a informação é configuração da aplicação: use [ConfigMap e Secret](/architecture/kubernetes-patterns/configuration/configuration-resource)
- Quando a aplicação precisa de dados do cluster além do próprio Pod, como outros recursos: acesse a API com RBAC apropriado
- Quando o valor deve mudar em variáveis de ambiente após a criação, o que não acontece
- Quando expor metadados pode vazar informações sensíveis, como nomes internos, a quem não deveria vê-las

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Aplicação independente do cliente da API do Kubernetes | Cobre só metadados do próprio Pod, não o estado do cluster |
| Dados corretos e dinâmicos sem configurá-los manualmente | Variáveis de ambiente não se atualizam após o início do contêiner |
| Mesmo mecanismo de variáveis e arquivos usado para configuração | Conjunto limitado de campos disponíveis |
| Dimensionamento automático conforme os limits do Pod | Valores de recursos precisam ser interpretados na unidade correta |

- **Variáveis versus volume:** use variáveis para dados estáveis e o volume `downwardAPI` para labels e annotations que mudam.
- **Unidades:** `resourceFieldRef` aceita `divisor` para entregar CPU e memória em milicores ou megabytes, conforme o que a aplicação espera.
- **Recarga:** quem lê arquivos precisa observá-los para perceber atualizações de labels e annotations; sem isso, pode ser necessário reiniciar o Pod.
- **Chaves fixas:** `fieldRef` cobre nome, namespace, IPs, nó, conta de serviço, uid, labels e annotations, e `resourceFieldRef` cobre requests e limits de CPU e memória do contêiner; qualquer outro dado exige consultar a API do Kubernetes, como fazem aplicações que descobrem Pods com certas labels para formar um cluster ou para monitorá-los.
- **Segurança:** não exponha nada além do necessário, pois annotations podem conter dados internos.

## Diagrama

<Diagram />

O kubelet preenche variáveis e arquivos com os metadados do Pod, e a aplicação os usa para identificar a instância e ajustar seu comportamento sem consultar a API do Kubernetes.

## Exemplo

Um Pod do `card-service` que recebe nome, namespace, IP e o limite de memória por variáveis, além de labels e annotations por arquivo.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: card-service-demo
  namespace: fintech
  labels:
    app: card-service
    tier: backend
  annotations:
    team: cards
spec:
  containers:
    - name: card-service
      image: registry.fintech.example/card-service:1.4.2
      env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: MEMORY_LIMIT_MB
          valueFrom:
            resourceFieldRef:
              containerName: card-service
              resource: limits.memory
              divisor: 1Mi
      resources:
        limits:
          memory: 512Mi
      volumeMounts:
        - name: podinfo
          mountPath: /etc/podinfo
  volumes:
    - name: podinfo
      downwardAPI:
        items:
          - path: labels
            fieldRef:
              fieldPath: metadata.labels
          - path: annotations
            fieldRef:
              fieldPath: metadata.annotations
```

As variáveis valem desde o início do contêiner, e os arquivos em `/etc/podinfo` são atualizados quando labels e annotations mudam.

## Padrões relacionados

- [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) — os requests e limits declarados são justamente os valores que a aplicação pode ler
- [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration) — usa o mesmo mecanismo de variáveis de ambiente, mas para configuração definida pelo usuário
- [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource) — ConfigMap e Secret entregam configuração, enquanto a Downward API entrega metadados gerados pela plataforma
- [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery) — nome e namespace do Pod ajudam a montar nomes DNS e registros
- [Controller](/architecture/kubernetes-patterns/advanced/controller) — quando a aplicação precisa observar e reagir ao estado do cluster, o caminho é a API do Kubernetes

## Referência

- [Kubernetes Patterns, capítulo 14: Self Awareness](https://k8spatterns.com/)
- [Expor informações do Pod por variáveis de ambiente](https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/)
- [Expor informações do Pod por arquivos](https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/)
