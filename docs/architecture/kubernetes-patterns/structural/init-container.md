---
title: Init Container
pattern_slug: init-container
category: Structural
tags:
  - Reliability
  - Operational Excellence
source: https://k8spatterns.com/
sidebar_label: "Init Container"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/structural/init-container.mdx';

# Init Container

## Descrição

O padrão Init Container separa as tarefas de inicialização de um Pod dos contêineres da aplicação, executando-as antes, em sequência e com ciclo de vida próprio. É o equivalente, no nível do Pod, ao construtor de uma classe: prepara o ambiente e valida pré-condições antes que o trabalho de verdade comece.

Os contêineres de um Pod se dividem em dois grupos. Os init containers rodam um por vez, na ordem declarada, e cada um precisa terminar com sucesso para que o próximo comece. Só depois do último é que os contêineres da aplicação sobem, em paralelo e sem ordem definida. Se um init container falha, o Pod é reiniciado (conforme a `restartPolicy`) e todos eles rodam de novo, por isso é boa prática torná-los idempotentes.

Como pertencem ao mesmo Pod, init containers e contêineres da aplicação compartilham volumes, rede e configurações de segurança e vão para o mesmo nó. Isso permite que uma equipe cuide da imagem da aplicação enquanto outra cuida de ferramentas de preparação (migrações, permissões, carga de dados) sem misturá-las na mesma imagem.

## Problemas que resolve

- Passos de preparação (schema de banco, permissões em arquivos, carga inicial de dados) misturados ao código ou à imagem da aplicação
- Ferramentas e bibliotecas de setup que não deveriam ir para a imagem final, aumentando tamanho e superfície de ataque
- Aplicação que precisa de permissões elevadas apenas na inicialização, mas não deveria mantê-las em execução
- Início da aplicação antes de uma dependência externa estar pronta, causando falhas em cascata na partida
- Falta de garantia de ordem entre etapas de inicialização quando tudo roda como contêineres paralelos

## Quando usar

- Quando a aplicação depende de uma preparação que precisa terminar antes do primeiro request, como migrar um schema ou baixar artefatos
- Quando as ferramentas de setup não devem fazer parte da imagem da aplicação
- Quando é preciso atrasar a partida até que uma dependência (banco, fila, serviço) responda
- Quando a inicialização exige privilégios que a aplicação em execução não deve ter
- Quando equipes diferentes mantêm a aplicação e a sua preparação

## Quando evitar

- Quando a tarefa precisa rodar continuamente ao lado da aplicação: use um Sidecar
- Quando a preparação pode ser feita pelo próprio processo da aplicação de forma simples e segura
- Quando o passo é lento e pesado e se repetiria a cada reinício do Pod; prefira um Job separado, executado uma vez por release
- Quando a lógica é de política do cluster (injetar valores padrão em todos os Pods): isso é papel de admission webhooks, mantidos por administradores

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Separação de responsabilidades entre inicialização e aplicação | Cada reinício do Pod repete todos os init containers |
| Ordem e sucesso de cada etapa garantidos antes da aplicação | Uma falha ou espera infinita impede o Pod de ficar pronto |
| Imagem da aplicação menor e com menos privilégios | Requests e limits do Pod consideram o maior init container, o que pode reservar recursos em excesso |
| Reuso de imagens de setup entre aplicações diferentes | Sem readiness probe nos init containers, o diagnóstico depende de logs e eventos |

- **Idempotência:** como o Pod pode reiniciar, cada init container deve produzir o mesmo resultado se executado mais de uma vez.
- **Recursos:** o valor efetivo de request e limit do Pod é o maior entre o init container mais exigente e a soma dos contêineres da aplicação; um init container pesado reserva capacidade que ninguém mais pode usar.
- **Dependências externas:** esperar por um serviço em um init container simplifica a partida, mas mascara problemas se não houver timeout e alerta.
- **Depuração:** trocar temporariamente o comando da aplicação por um `sleep` ajuda a inspecionar os volumes preenchidos pelo init container.
- **Combinação com Sidecar:** use os dois quando for preciso uma inicialização garantida e também atualização contínua dos dados.

## Diagrama

<Diagram />

Os init containers rodam em sequência: primeiro espera-se o banco responder, depois o schema é migrado. Só quando ambos terminam com sucesso o contêiner `ledger-service` é iniciado.

## Exemplo

O `ledger-service` só deve subir depois que o banco aceitar conexões e as migrações do razão tiverem sido aplicadas. A imagem de migração é mantida à parte da imagem da aplicação.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ledger-service
  namespace: fintech
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ledger-service
  template:
    metadata:
      labels:
        app: ledger-service
    spec:
      initContainers:
        - name: wait-for-db
          image: registry.fintech.example/tools/pg-isready:1.0.0
          args: ["--host=ledger-db", "--timeout=120"]
        - name: migrate-schema
          image: registry.fintech.example/ledger-migrations:1.4.2
          env:
            - name: DB_HOST
              value: ledger-db
      containers:
        - name: ledger-service
          image: registry.fintech.example/ledger-service:1.4.2
          ports:
            - containerPort: 8080
```

Os dois init containers rodam na ordem declarada e a migração é idempotente, então reiniciar o Pod é seguro.

## Padrões relacionados

- [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) — roda ao lado da aplicação durante toda a vida do Pod, enquanto o Init Container roda e termina antes dela.
- [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle) — complementa a inicialização com hooks de pós-início e pré-encerramento da aplicação.
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — depois que os init containers terminam, as probes indicam quando a aplicação está viva e pronta.
- [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) — requests e limits do Pod levam em conta o init container mais exigente.
- [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness) — um init container pode usar as informações do Pod para gerar configuração antes da partida.

## Referência

- [Kubernetes Patterns, capítulo 15: Init Container](https://k8spatterns.com/)
- [Init Containers (documentação do Kubernetes)](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
