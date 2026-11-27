---
title: Rolling Deployment
pattern_slug: rolling-deployment
category: Release
tags:
  - Reliability
  - Operational Excellence
  - Cost Optimization
source: https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/
sidebar_label: "Rolling Deployment"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/rolling-deployment.mdx';

# Rolling Deployment

## Description

Rolling Deployment replaces the instances of the current version with those of the new version gradually, one or a few at a time, without doubling the environment. Each new instance only joins the load balancer after passing the health check, and only then is an old instance removed. The cycle repeats until all of them run the new version, always keeping a minimum capacity online.

The pace is controlled by two limits: how many extra instances may exist during the switch and how many may be unavailable. It is the default strategy of orchestrators such as Kubernetes (`RollingUpdate`) and of cloud auto scaling groups.

## Problems it solves

- Downtime during deployment, without the cost of keeping a second full environment.
- Manual instance swaps in clusters with many replicas.
- Load spikes caused by restarting every instance at the same time.

## When to use

- Stateless services with several replicas behind a load balancer.
- When the cost of doubling the environment, as in Blue-Green, is not justified.
- Backward-compatible changes, where two versions can serve at the same time.

## When to avoid

- When two versions cannot coexist, as in contract changes without backward compatibility: prefer stopping and recreating, or [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment).
- When you need to control which customers see the new version: prefer [Canary Release](/architecture/microservices/release/canary-release).
- Single-instance services, where there is nothing to alternate.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| No downtime and no doubled infrastructure | Two versions serve at the same time during the switch |
| Pace controllable through surge and unavailability limits | Slow rollback, redoing the switch in reverse |
| Native support in orchestrators | No control over which customers land on the new version |
| Minimum capacity guaranteed at all times | A bug can reach a large share of traffic before it is detected |

- **Health check is mandatory:** without a reliable readiness check, the orchestrator moves the switch forward even with broken new instances.
- **Compatibility:** during the switch window, requests from the same customer may land on different versions, so contracts and schemas must work with both.
- **Extra capacity:** allowing one surge instance speeds up the switch without reducing capacity; allowing unavailability saves resources, but reduces headroom during the deployment.

## Diagram

<Diagram />

`pix-service` has three replicas and allows one surge replica. A v2 replica starts, passes the health check and replaces a v1; the cycle repeats until only v2 replicas remain.

## Related patterns

- [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment) — immediate rollback, at the cost of doubling capacity.
- [Canary Release](/architecture/microservices/release/canary-release) — controls who gets the new version and for how long.
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — the Kubernetes `RollingUpdate` strategy, with `maxSurge` and `maxUnavailable`.
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — the readiness check that releases each step of the switch.
- [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) — a platform that runs the switch automatically.

## Reference

- [Kubernetes — Performing a Rolling Update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
