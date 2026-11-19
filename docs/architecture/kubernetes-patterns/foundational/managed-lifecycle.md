---
title: Managed Lifecycle
pattern_slug: managed-lifecycle
category: Foundational
tags:
  - Reliability
  - Operational Excellence
source: https://k8spatterns.com/
sidebar_label: "Managed Lifecycle"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/foundational/managed-lifecycle.mdx';

# Managed Lifecycle

## Descrição

O padrão Managed Lifecycle faz a aplicação escutar e reagir aos eventos de ciclo de vida emitidos pelo Kubernetes, como sinais de encerramento e hooks de início e fim, para iniciar e terminar de forma limpa, sem perder trabalho em andamento. Enquanto as sondas de saúde extraem informação da aplicação, este padrão é o canal inverso: a plataforma envia comandos e a aplicação decide como responder.

Ao encerrar um contêiner, seja por remoção do Pod, rolling update, eviction ou falha de liveness, o Kubernetes envia o sinal **SIGTERM** e espera um período de carência (30 segundos por padrão, ajustável com `terminationGracePeriodSeconds`) antes de enviar o **SIGKILL**, que mata o processo à força. A aplicação deve tratar o SIGTERM parando de aceitar novas requisições, concluindo as que estão em andamento, liberando conexões e fazendo flush de dados. Para isso, o processo principal precisa receber o sinal (cuidado com scripts de shell no entrypoint que não o repassam).

Há também hooks no nível do contêiner. O **postStart** roda logo após a criação do contêiner, em paralelo ao processo principal, e bloqueia o estado do contêiner até terminar. O **preStop** roda antes do envio do SIGTERM e permite iniciar o encerramento quando o processo não consegue tratar o sinal, ou apenas ganhar tempo, por exemplo para que o Pod saia do balanceamento antes de parar. Os hooks suportam `exec` e `httpGet`, e a execução deles deve ser idempotente, pois a garantia é de pelo menos uma vez. Para inicialização no nível do Pod, com garantias de ordem, usam-se init containers.

## Problemas que resolve

- Requisições em andamento interrompidas quando um Pod é removido durante um deploy ou um scale down
- Dados não persistidos ou transações pela metade quando o processo é morto de forma abrupta
- Conexões abertas que não são liberadas, deixando clientes e bancos com sessões penduradas
- Aplicações que precisam de uma preparação ou de um aquecimento logo após iniciar
- Tráfego ainda direcionado a um Pod que acabou de receber o sinal de encerramento

## Quando usar

- Em serviços que processam requisições longas ou operações financeiras, como o `ledger-service`, que não podem ser cortadas no meio
- Quando é preciso concluir ou devolver à fila o trabalho em andamento antes de encerrar
- Quando a aplicação mantém conexões, locks ou arquivos que devem ser liberados no encerramento
- Quando o Pod precisa de uma pausa curta para sair do balanceamento antes de parar de aceitar conexões

## Quando evitar

- Em lógica crítica dentro do `postStart`, pois não há garantia de ordem em relação ao processo principal
- Para tarefas longas de inicialização no nível do Pod, em que um init container oferece garantias melhores
- Com `terminationGracePeriodSeconds` muito altos sem necessidade, que atrasam rollouts e drenagem de nós
- Para depender do `preStop` como único mecanismo de limpeza, já que sua falha não impede a remoção do contêiner

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Encerramentos limpos, sem perder requisições em andamento | A aplicação precisa implementar o tratamento de sinais e a lógica de shutdown |
| Menos erros visíveis aos usuários durante deploys e escalonamento | Períodos de carência longos deixam rollouts e drenagem de nós mais lentos |
| Possibilidade de preparar a aplicação logo após iniciar | Hooks podem rodar mais de uma vez ou antes do processo principal estar pronto |
| Comportamento previsível e alinhado ao modelo de processos POSIX | Se o SIGKILL chega antes do fim, o trabalho restante é perdido de qualquer forma |

- **Tratamento de SIGTERM:** pare de aceitar conexões, conclua o que está em curso e saia dentro do período de carência.
- **Propagação do sinal:** garanta que o processo principal seja o PID 1 ou que o entrypoint repasse o sinal.
- **Corrida com o balanceamento:** a remoção dos endpoints e o SIGTERM ocorrem em paralelo; um `preStop` curto, com `sleep`, reduz erros por requisições ainda a caminho.
- **Idempotência:** os hooks têm semântica de pelo menos uma vez e devem tolerar execuções repetidas.

## Diagrama

<Diagram />

O Pod sai do balanceamento, passa pelo `preStop` e recebe o SIGTERM; a aplicação conclui o trabalho em curso e encerra, sob pena de ser morta à força ao fim do período de carência.

## Exemplo

O `ledger-service` recebe 45 segundos de carência para concluir lançamentos em andamento. O hook `preStop` faz uma pausa curta para dar tempo de o Pod sair do balanceamento antes de o SIGTERM chegar.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ledger-service
  namespace: fintech
  labels:
    app: ledger-service
spec:
  terminationGracePeriodSeconds: 45
  containers:
    - name: ledger-service
      image: registry.fintech.example/ledger-service:3.1.0
      ports:
        - containerPort: 8080
      lifecycle:
        preStop:
          exec:
            command: ["sleep", "5"]   # deixa o Pod sair do balanceamento
```

Após o `preStop`, o processo recebe o SIGTERM e deve finalizar os lançamentos pendentes (cada estorno continua sendo um novo lançamento) antes de encerrar.

## Padrões relacionados

- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — o canal oposto: as sondas leem o estado da aplicação, enquanto o ciclo de vida envia eventos a ela
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — rolling updates dependem de encerramentos limpos para não perder requisições
- [Init Container](/architecture/kubernetes-patterns/structural/init-container) — inicialização no nível do Pod, com ordem e término garantidos, em contraste com os hooks por contêiner
- [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) — a transição ordenada de instância ativa depende de encerramento correto da anterior
- [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) — contêineres auxiliares também seguem o ciclo de vida do Pod e precisam encerrar de forma coordenada

## Referência

- [Kubernetes Patterns, capítulo 5: Managed Lifecycle](https://k8spatterns.com/)
- [Container Lifecycle Hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)
- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
