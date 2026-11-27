---
title: Periodic Job
pattern_slug: periodic-job
category: Behavioral
tags:
  - Reliability
  - Operational Excellence
source: https://k8spatterns.com/
sidebar_label: "Periodic Job"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/behavioral/periodic-job.mdx';

# Periodic Job

## Descrição

O padrão Periodic Job dispara a execução de um Batch Job por um evento temporal, usando o recurso CronJob do Kubernetes para agendar a criação de Jobs no formato cron. Cada disparo gera um novo Job com seus Pods, de modo que a lógica de negócio fica no contêiner e o agendamento fica por conta da plataforma.

Sem isso, agendar tarefas exige um cron em um único servidor, que é difícil de manter e vira ponto único de falha, ou um agendador embutido na aplicação, que obriga a rodar várias instâncias e eleger um líder para que só uma dispare o trabalho. O CronJob elimina esse problema: o controlador do cluster cria o Job no horário indicado por `schedule`. Campos como `concurrencyPolicy`, `startingDeadlineSeconds`, `suspend` e os limites de histórico controlam sobreposição, atrasos, pausa e retenção.

## Problemas que resolve

- Tarefas recorrentes de manutenção e de negócio, como limpeza, arquivamento, envio de relatórios e integrações por arquivo
- Agendadores baseados em cron de um único servidor, que são pontos únicos de falha
- Agendamento embutido na aplicação, que exige alta disponibilidade e eleição de líder só para rodar uma tarefa simples
- Falta de visibilidade e de reexecução automática de tarefas agendadas que falham

## Quando usar

- Em rotinas com horário ou intervalo definido, como fechamento diário, emissão de extratos e expurgo de dados antigos
- Quando se quer reaproveitar o modelo de Jobs (paralelismo, tentativas, limites) com disparo por tempo
- Quando a tarefa pode ser executada por um contêiner dedicado, separado da aplicação principal
- Quando a plataforma deve cuidar do agendamento, sem código de scheduler na aplicação

## Quando evitar

- Para trabalho que deve reagir a eventos em tempo real: prefira filas ou mensageria
- Para precisão de segundos ou subsegundos, pois o disparo tem tolerância e pode atrasar
- Quando uma execução nunca pode se sobrepor a outra e a tarefa não foi preparada para isso
- Para fluxos com dependências entre etapas, que pedem um orquestrador de workflows

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Agendamento gerenciado pela plataforma, sem ponto único de falha | O disparo pode atrasar, falhar ou ser executado duas vezes |
| Reuso de todos os recursos de Job: tentativas, paralelismo e limites | Execuções podem se sobrepor se o trabalho durar mais que o intervalo |
| Lógica de negócio isolada do mecanismo de agendamento | Fuso horário e horário de verão exigem atenção na expressão cron |
| Histórico de Jobs para auditoria e diagnóstico | Muitos Jobs antigos acumulam recursos se o histórico não for limitado |

- **Sobreposição:** `concurrencyPolicy` é `Allow` por padrão (cria o novo Job mesmo com o anterior em andamento); `Forbid` pula o disparo seguinte e `Replace` cancela o Job em execução e inicia outro.
- **Casos de borda:** a aplicação deve tratar execuções duplicadas, ausentes, paralelas ou canceladas, pois o CronJob não as elimina.
- **Atrasos:** `startingDeadlineSeconds` define até quando um disparo perdido ainda pode ser iniciado; vale quando o resultado de uma execução tardia já seria inútil, porque os dados ficaram obsoletos.
- **Pausa:** `suspend: true` interrompe novos disparos sem apagar o CronJob, útil em janelas de manutenção.
- **Histórico:** configure `successfulJobsHistoryLimit` e `failedJobsHistoryLimit` para equilibrar diagnóstico e consumo de recursos.

## Diagrama

<Diagram />

O CronJob cria um novo Job a cada disparo, e cada Job executa seus próprios Pods, seguindo as regras de tentativas e paralelismo do padrão Batch Job.

## Exemplo

Um fechamento diário de extratos às 02h00, sem permitir execuções simultâneas e mantendo um histórico curto.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-statement-close
  namespace: fintech
spec:
  schedule: "0 2 * * *"
  timeZone: "America/Sao_Paulo"
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 600
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        metadata:
          labels:
            app: statement-service
        spec:
          restartPolicy: OnFailure
          containers:
            - name: closer
              image: registry.fintech.example/statement-service:1.4.2
              args: ["close-statements", "--period=daily"]
```

O `jobTemplate` usa a mesma especificação de um Job comum, e `concurrencyPolicy: Forbid` evita que o fechamento do dia comece antes de o anterior terminar.

## Padrões relacionados

- [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) — o CronJob cria Jobs, e todo o comportamento de execução vem desse padrão
- [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) — alternativa quando é preciso uma instância única contínua, e não execuções pontuais
- [Leader Election](/architecture/cloud-design-patterns/distributed-coordination/leader-election) — o problema que o CronJob evita ao agendar tarefas sem eleição de líder na aplicação
- [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle) — o Pod do Job deve reagir ao sinal de término e sair com o código correto
- [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) — requests e limits permitem planejar a capacidade das janelas de execução

## Referência

- [Kubernetes Patterns, capítulo 8: Periodic Job](https://k8spatterns.com/)
- [CronJob na documentação do Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
