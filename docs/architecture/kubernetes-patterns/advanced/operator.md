---
title: Operator
pattern_slug: operator
category: Advanced
tags:
  - Operational Excellence
  - Reliability
source: https://k8spatterns.com/
sidebar_label: "Operator"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/advanced/operator.mdx';

# Operator

## Descrição

O padrão Operator é um Controller que usa uma CustomResourceDefinition (CRD) para encapsular o conhecimento operacional de uma aplicação específica de forma algorítmica e automatizada. Ele estende a API do Kubernetes com novos tipos de recurso do domínio e roda um laço de reconciliação que os transforma em recursos nativos e em ações de operação.

Um Operator entende dois domínios: o Kubernetes e a aplicação que gerencia. Em vez de um humano executar o runbook de instalar, atualizar, fazer backup ou restaurar um banco de dados, o time declara um recurso como `LedgerDatabase` e o Operator faz o trabalho, relatando o resultado no campo `status`. Como o recurso customizado é servido pela API, ele funciona com `kubectl`, RBAC por tipo, namespaces, versionamento e validação por esquema OpenAPI.

Os CRDs costumam ser de dois tipos: de **instalação** (instalam e operam uma aplicação, como um banco de dados ou um Prometheus) e de **aplicação** (representam um conceito do domínio, como um monitor de serviço). Para casos que a CRD não alcança, existe ainda a agregação de API, com um servidor de API próprio, que dá mais liberdade ao custo de muito mais código. Três projetos principais ajudam a escrever Operators. O **Kubebuilder**, do SIG API Machinery, é um framework em Go que gera o esqueleto do projeto e tem arquitetura de plugins para outras linguagens. O **Operator Framework**, da CNCF, reúne o Operator SDK (construído sobre o Kubebuilder, com plugins para Ansible, Helm e Java), o Operator Lifecycle Manager (que instala operadores e suas CRDs em nome de usuários sem privilégio, por meio de um recurso `ClusterServiceVersion`) e o OperatorHub, um catálogo público. O **Metacontroller** delega a lógica a um webhook em qualquer linguagem que entenda HTTP e JSON, e ele cuida da reconciliação.

## Problemas que resolve

- Aplicações complexas ou com estado cuja operação (instalar, atualizar, escalar, backup, restauração) depende de conhecimento humano especializado
- Necessidade de novos conceitos de domínio na plataforma, descritos como recursos declarativos e não como scripts
- Falta de validação, versionamento e permissões por tipo quando a configuração mora em ConfigMaps
- Integração fraca com as ferramentas do ecossistema, como `kubectl`, GitOps e controle de acesso

## Quando usar

- Quando você quer integração forte com as ferramentas do Kubernetes e tratar o domínio como recursos de primeira classe
- Para automatizar o ciclo de vida de software com estado, como bancos de dados, filas e sistemas de mensageria
- Quando o domínio é declarativo e se encaixa na reconciliação reativa
- Quando você se beneficia de grupos de API, versões, namespaces e RBAC por tipo de recurso

## Quando evitar

- Quando um [Controller](/architecture/kubernetes-patterns/advanced/controller) simples sobre recursos padrão resolve, sem exigir permissão de administrador do cluster para registrar CRDs
- Quando o caso de uso não é declarativo ou os dados não cabem no modelo de recursos do Kubernetes: prefira uma API própria exposta por Service ou Ingress
- Quando um chart de Helm ou um Deployment bem escrito já atende, sem lógica operacional contínua
- Quando você precisa de mais flexibilidade de armazenamento do que a CRD oferece: considere um servidor de API agregado, ciente do custo

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Conhecimento operacional versionado, testável e repetível | Registrar CRDs exige permissão de administrador do cluster, já que são recursos globais |
| Recursos de domínio com `kubectl`, validação e RBAC por tipo | Mais código e mais um componente crítico para manter e atualizar |
| Menos erro humano em tarefas complexas como backup e restauração | Um bug no Operator pode afetar todas as instâncias gerenciadas |
| Comportamento reconciliado continuamente, com status visível | Evolução de esquema e versões da CRD exige estratégia de migração |

- **Esquema e status:** declare um esquema OpenAPI e a subresource `status` para que erros de configuração sejam detectados cedo e o resultado seja visível.
- **Escala:** a subresource `scale` permite que o recurso customizado seja usado com o HorizontalPodAutoscaler, desde que informe o seletor de rótulos.
- **Ciclo de vida do próprio Operator:** instalar e atualizar o Operator e suas CRDs também precisa de processo, por exemplo com um gerenciador dedicado.
- **Exagero:** o Kubernetes não é a solução para tudo; modele como CRD apenas o que de fato é declarativo.
- **Idempotência e falhas:** o laço pode ser reexecutado a qualquer momento e deve tolerar estados parciais.
- **Dados sensíveis:** operações como backup e restauração envolvem dados financeiros; limite as permissões do Operator ao necessário.

## Diagrama

<Diagram />

O time declara um `LedgerDatabase`; o Operator observa o recurso, cria os recursos nativos necessários, agenda os backups e atualiza o `status`, fechando o ciclo de reconciliação.

## Exemplo

O ledger da fintech roda em um banco com réplicas e backups. Em vez de um runbook, o time de plataforma define uma CRD `LedgerDatabase` (primeiro manifesto) e um Operator que a reconcilia. O segundo manifesto é uma instância do recurso customizado, que declara versão, réplicas e agenda de backup.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: ledgerdatabases.fintech.example
spec:
  group: fintech.example
  scope: Namespaced
  names:
    kind: LedgerDatabase
    singular: ledgerdatabase
    plural: ledgerdatabases
  versions:
    - name: v1
      served: true
      storage: true
      subresources:
        status: {}
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              required: [version, replicas]
              properties:
                version:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                backupSchedule:
                  type: string
            status:
              type: object
              properties:
                readyReplicas:
                  type: integer
                lastBackupTime:
                  type: string
```

```yaml
apiVersion: fintech.example/v1
kind: LedgerDatabase
metadata:
  name: ledger-db
  namespace: fintech
spec:
  version: "15.4"
  replicas: 3
  backupSchedule: "0 3 * * *" # todo dia às 3h
```

## Padrões relacionados

- [Controller](/architecture/kubernetes-patterns/advanced/controller) — a base do Operator: o mesmo laço de reconciliação, mas sobre recursos padrão
- [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) — Operators costumam automatizar a operação de aplicações com estado que usam StatefulSets
- [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) — o Operator roda como uma única instância ativa para não reconciliar em duplicidade
- [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource) — alternativa simples à CRD: um ConfigMap como descrição declarativa do domínio
- [Leader Election](/architecture/cloud-design-patterns/distributed-coordination/leader-election) — permite réplicas do Operator em espera, com apenas uma líder reconciliando

## Referência

- [Kubernetes Patterns, capítulo 28: Operator](https://k8spatterns.com/)
- [Operator pattern (documentação do Kubernetes)](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [Custom Resources (documentação do Kubernetes)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
