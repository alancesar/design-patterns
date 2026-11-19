---
title: Stateless Service
pattern_slug: stateless-service
category: Behavioral
tags:
  - Reliability
  - Performance Efficiency
  - Operational Excellence
source: https://k8spatterns.com/
sidebar_label: "Stateless Service"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/behavioral/stateless-service.mdx';

# Stateless Service

## Descrição

O padrão Stateless Service executa aplicações compostas por réplicas idênticas, efêmeras e substituíveis, que não guardam nada de que as próximas requisições dependam, usando Deployment, ReplicaSet e Service. É o formato ideal para APIs e consumidores de mensagens que precisam escalar e se recuperar rapidamente em ambientes dinâmicos de nuvem.

Um contêiner é sem estado quando não mantém, em memória ou no disco temporário, informação crítica para atender requisições futuras: o que precisa ser lembrado vai para um banco, uma fila, um sistema de arquivos montado ou outro armazenamento externo acessível a todas as instâncias. Um bom teste mental é imaginar as instâncias em nós diferentes, com um balanceador distribuindo as requisições ao acaso e sem afinidade de sessão: se o serviço cumpre seu papel assim, ele é sem estado. No Kubernetes, o **ReplicaSet** mantém o número desejado de Pods idênticos, mas o recurso recomendado para o uso diário é o **Deployment**, que cria e gerencia os ReplicaSets e ainda controla atualização e reversão. Como cada Pod substituído ganha novo nome e novo IP, o **Service** oferece um endereço fixo e balanceia a carga apenas entre os Pods prontos. Quando há necessidade de arquivos, um PersistentVolumeClaim pode ser referenciado no template do Pod, mas todas as réplicas de um ReplicaSet compartilham o mesmo claim, diferente do que acontece em um [StatefulSet](/architecture/kubernetes-patterns/behavioral/stateful-service).

## Problemas que resolve

- Aplicações que precisam ser criadas, escaladas e destruídas sem efeitos colaterais
- Réplicas perdidas por falha de nó ou despejo que precisam ser repostas automaticamente
- Endereços de Pods que mudam a cada reinício e quebram quem os consome
- Atualizações de versão que não podem interromper o atendimento

## Quando usar

- Para APIs e serviços de requisição e resposta que guardam o estado em um banco, uma fila ou um cache externo
- Quando qualquer réplica pode atender qualquer requisição, sem afinidade de sessão
- Quando se quer escalar horizontalmente de forma rápida e barata
- Para consumidores de mensagens que só abrem conexões de saída e dispensam um Service

## Quando evitar

- Quando cada instância precisa de identidade, nome estável ou volume próprio: use um [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service)
- Quando o serviço depende de memória local que não pode ser perdida em um reinício
- Quando só uma instância pode escrever em um dado: considere um [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service)
- Quando cada réplica precisaria de um volume distinto, pois em um ReplicaSet todas compartilham o mesmo claim

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Escala e recuperação rápidas, sem dependência entre instâncias | O estado vai para sistemas externos, que precisam ser operados e podem virar gargalo |
| Atualizações e reversões automáticas pelo Deployment | A aplicação deve ser projetada para ser descartável e tolerar reinícios a qualquer momento |
| Endereço estável e tráfego só para Pods prontos pelo Service | O Service e o Deployment não se conhecem: cabe a quem define os recursos alinhar seletores e probes |
| Réplicas intercambiáveis simplificam a operação | Nomes e IPs dos Pods mudam, então nada pode depender deles |

- **ReplicaSet direto:** só vale quando as estratégias de atualização do Deployment não servem ou quando não se quer controle algum sobre a atualização; um ReplicaSet também adota Pods avulsos cujos rótulos casem com o seletor, e pode apagá-los se passarem do total.
- **Modos de acesso:** `ReadWriteOnce` permite montagem em um único nó, mas vários Pods desse nó podem escrever; `ReadWriteMany` e `ReadOnlyMany` aceitam vários nós; `ReadWriteOncePod` garante um único Pod, mas na prática impede escalar.
- **Volume compartilhado:** todas as réplicas apontam para o mesmo PVC, ao contrário do StatefulSet, que cria um por réplica.
- **Service opcional:** quem só abre conexões de saída, como um consumidor de filas, não precisa de Service.
- **Combinação de peças:** o Kubernetes não impõe relação entre Pod, ReplicaSet, Deployment, Service e PVC; entender liveness, readiness e a política de armazenamento é responsabilidade de quem monta o conjunto.
- **Além do básico:** para escalar a zero ou por eventos, é possível combinar com ferramentas como Knative e KEDA, tratadas em [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale).

## Diagrama

<Diagram />

As três réplicas são idênticas e descartáveis: o Service distribui as requisições, o Deployment e o ReplicaSet repõem quem falhar, e todo o estado fica no banco externo.

## Exemplo

A API `pix-service` da fintech, com três réplicas intercambiáveis, atualização gradual sem indisponibilidade e probe de prontidão, exposta dentro do cluster por um Service.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pix-service
  namespace: fintech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pix-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    metadata:
      labels:
        app: pix-service
    spec:
      containers:
        - name: pix-service
          image: registry.fintech.example/pix-service:1.4.2
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: pix-service
  namespace: fintech
spec:
  selector:
    app: pix-service
  ports:
    - port: 80
      targetPort: 8080
```

O Deployment mantém três Pods idênticos e os troca um a um sem reduzir a capacidade; o Service usa o mesmo rótulo `app: pix-service` para encontrar os Pods e envia tráfego só aos que passaram na prontidão.

## Padrões relacionados

- [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) — o contraponto: identidade estável e armazenamento próprio por réplica
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — define como o Deployment atualiza e reverte as réplicas
- [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery) — o Service dá um endereço fixo às réplicas efêmeras
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — a prontidão decide quais Pods recebem tráfego
- [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale) — escala as réplicas de acordo com a carga, inclusive até zero

## Referência

- [Kubernetes Patterns, capítulo 11: Stateless Service](https://k8spatterns.com/)
- [Deployments na documentação do Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ReplicaSet na documentação do Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
