---
title: Declarative Deployment
pattern_slug: declarative-deployment
category: Foundational
tags:
  - Operational Excellence
  - Reliability
source: https://k8spatterns.com/
sidebar_label: "Declarative Deployment"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/foundational/declarative-deployment.mdx';

# Declarative Deployment

## Description

The Declarative Deployment pattern describes the desired version of an application in a `Deployment` resource and lets Kubernetes execute, on the server side, all the steps to go from the current version to it, in a repeatable way and with the ability to roll back. Instead of an operator running commands in sequence to start new Pods, wait for them to become ready and remove the old ones, the operator only changes the desired state, and a controller does the rest.

Behind the `Deployment`, each version is a `ReplicaSet`, and the `strategy` field defines how the switch happens. The **RollingUpdate** strategy (the default) replaces Pods gradually, controlled by `maxSurge` (how many extra Pods may exist) and `maxUnavailable` (how many may be missing), and avoids unavailability as long as there is a `readinessProbe`. The **Recreate** strategy terminates all old Pods before starting the new ones, accepting a window of unavailability in exchange for never having two versions at the same time.

On top of these primitives it is possible to build more elaborate release strategies, usually with a human decision: **Blue-Green**, in which two versions coexist in separate Deployments and traffic is switched by changing the `Service` selector, and **Canary**, in which a small share of the replicas runs the new version before the full replacement. The revision history allows pausing, resuming and undoing the update with `kubectl rollout`.

## Problems it solves

- Manual or scripted updates, prone to human error and hard to repeat across environments
- Unavailability while switching a service's version
- Difficulty knowing which version is actually running and how to return to the previous one
- A release process that becomes a bottleneck as the number of microservices grows
- Update orchestration logic scattered across clients and scripts, instead of centralized in the platform

## When to use

- In stateless services that must be updated frequently and without unavailability, such as the `pix-service`
- When you want the desired state versioned in Git and applied identically in every environment
- When you need to quickly roll back a faulty version
- As a basis for Blue-Green and Canary releases, combined with `Service` and traffic routing

## When to avoid

- For workloads with identity or storage of their own per replica, which call for a `StatefulSet` (see Stateful Service)
- With `RollingUpdate` when two simultaneous versions are incompatible, such as a contract change without backward compatibility: prefer `Recreate`
- To update Pod dependencies, such as `ConfigMap` and database schema, which the `Deployment` does not manage by itself
- When you need a fully automated rollout with metrics analysis, which requires additional tools

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Repeatable, versioned update executed by the server | Depends on `readinessProbe` and clean shutdown to be truly zero downtime |
| Simple rollback through the `ReplicaSet` history | Two versions coexist during the rolling update, requiring compatibility |
| Fine control of the pace with `maxSurge` and `maxUnavailable` | `Recreate` causes unavailability, and Blue-Green temporarily needs double the capacity |
| Basis for Blue-Green and Canary strategies | Blue-Green and Canary require manual steps or additional tools |

- **Compatibility between versions:** during the rolling update, `pix-service` v1 and v2 receive traffic together; API and schema changes must be made in stages.
- **Mandatory probes:** without a `readinessProbe`, Kubernetes considers the Pod ready too early and may take down the old replicas before time.
- **Extra capacity:** `maxSurge` consumes resources beyond the replica count; make sure the cluster has headroom.
- **Dependencies:** `ConfigMap`, `Secret` and database migrations need their own update and rollback strategy.

## Diagram

<Diagram />

The `Deployment` scales up the new `ReplicaSet` and scales down the old one in controlled steps; a Pod only receives traffic from the `Service` after it passes the `readinessProbe`.

## Example

The `pix-service` has four replicas and is updated with a rolling update without reducing capacity: it starts one extra Pod at a time and never leaves any unavailable. The `readinessProbe` ensures that the switch only advances when the new Pod is ready.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pix-service
  namespace: fintech
spec:
  replicas: 4
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: pix-service
  template:
    metadata:
      labels:
        app: pix-service
    spec:
      containers:
        - name: pix-service
          image: registry.fintech.example/pix-service:1.5.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
```

To return to the previous version, just run `kubectl rollout undo deployment/pix-service -n fintech`; the history kept by `revisionHistoryLimit` makes the rollback immediate.

## Related patterns

- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — the `readinessProbe` decides when the rolling update may advance to the next replica
- [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle) — handling SIGTERM lets old Pods shut down without losing in-flight requests
- [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) — alternative for workloads with their own identity and storage, whose update follows different rules
- [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) — Kubernetes is an implementation of this platform, and the `Deployment` is its release primitive
- [Controller](/architecture/kubernetes-patterns/advanced/controller) — the `Deployment` works because a controller continuously reconciles the current state with the desired one

## Reference

- [Kubernetes Patterns, chapter 3: Declarative Deployment](https://k8spatterns.com/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Performing a Rolling Update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
