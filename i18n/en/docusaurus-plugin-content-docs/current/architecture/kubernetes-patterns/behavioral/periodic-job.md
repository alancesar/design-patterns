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

## Description

The Periodic Job pattern triggers the execution of a Batch Job from a temporal event, using the Kubernetes CronJob resource to schedule the creation of Jobs in cron format. Each trigger produces a new Job with its Pods, so the business logic stays in the container and the scheduling is left to the platform.

Without it, scheduling tasks requires a cron on a single server, which is hard to maintain and becomes a single point of failure, or a scheduler embedded in the application, which forces you to run several instances and elect a leader so that only one triggers the work. The CronJob removes that problem: the cluster controller creates the Job at the time given by `schedule`. Fields such as `concurrencyPolicy`, `startingDeadlineSeconds`, `suspend` and the history limits control overlap, delays, pausing and retention.

## Problems it solves

- Recurring maintenance and business tasks, such as cleanup, archiving, report delivery and file-based integrations
- Cron-based schedulers on a single server, which are single points of failure
- Scheduling embedded in the application, which requires high availability and leader election just to run a simple task
- Lack of visibility and of automatic reruns for scheduled tasks that fail

## When to use

- In routines with a defined time or interval, such as daily closing, statement issuance and purging of old data
- When you want to reuse the Job model (parallelism, retries, limits) with time-based triggering
- When the task can be run by a dedicated container, separate from the main application
- When the platform should handle scheduling, with no scheduler code in the application

## When to avoid

- For work that must react to events in real time: prefer queues or messaging
- For second or sub-second precision, since triggering has a tolerance and may be delayed
- When one execution must never overlap another and the task was not prepared for that
- For flows with dependencies between steps, which call for a workflow orchestrator

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Scheduling managed by the platform, with no single point of failure | A trigger may be delayed, missed or run twice |
| Reuse of every Job feature: retries, parallelism and limits | Executions may overlap if the work lasts longer than the interval |
| Business logic isolated from the scheduling mechanism | Time zone and daylight saving time need attention in the cron expression |
| Job history for auditing and diagnosis | Many old Jobs accumulate resources if history is not limited |

- **Overlap:** `concurrencyPolicy` is `Allow` by default (creates the new Job even with the previous one still running); `Forbid` skips the next trigger and `Replace` cancels the running Job and starts another.
- **Corner cases:** the application must handle duplicate, missing, parallel or canceled runs, since the CronJob does not eliminate them.
- **Delays:** `startingDeadlineSeconds` defines until when a missed trigger can still be started; it applies when the result of a late run would already be useless, because the data became obsolete.
- **Pausing:** `suspend: true` stops new triggers without deleting the CronJob, useful in maintenance windows.
- **History:** configure `successfulJobsHistoryLimit` and `failedJobsHistoryLimit` to balance diagnosis and resource usage.

## Diagram

<Diagram />

The CronJob creates a new Job on every trigger, and each Job runs its own Pods, following the retry and parallelism rules of the Batch Job pattern.

## Example

A daily statement closing at 02:00, with no simultaneous executions and a short history.

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

The `jobTemplate` uses the same specification as a regular Job, and `concurrencyPolicy: Forbid` prevents the day's closing from starting before the previous one finishes.

## Related patterns

- [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) — the CronJob creates Jobs, and all execution behavior comes from that pattern
- [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) — alternative when you need a single continuous instance rather than one-off executions
- [Leader Election](/architecture/cloud-design-patterns/distributed-coordination/leader-election) — the problem the CronJob avoids by scheduling tasks without leader election in the application
- [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle) — the Job's Pod must react to the termination signal and exit with the correct code
- [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) — requests and limits allow planning the capacity of the execution windows

## Reference

- [Kubernetes Patterns, chapter 8: Periodic Job](https://k8spatterns.com/)
- [CronJob in the Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
