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

## Description

The Stateless Service pattern runs applications made of identical, ephemeral, replaceable replicas that keep nothing future requests depend on, using Deployment, ReplicaSet and Service. It is the ideal shape for APIs and message consumers that need to scale and recover quickly in dynamic cloud environments.

A container is stateless when it holds no information critical for serving future requests in memory or on temporary disk: whatever must be remembered goes to a database, a queue, a mounted filesystem or another external store reachable by all instances. A good thought experiment is to imagine the instances on different nodes, with a load balancer spreading requests at random and without session affinity: if the service still does its job, it is stateless. In Kubernetes, the **ReplicaSet** keeps the desired number of identical Pods, but the recommended resource for day-to-day use is the **Deployment**, which creates and manages ReplicaSets and also controls updates and rollbacks. Because every replaced Pod gets a new name and a new IP, the **Service** offers a fixed address and balances load only across ready Pods. When files are needed, a PersistentVolumeClaim can be referenced in the Pod template, but all replicas of a ReplicaSet share the same claim, unlike in a [StatefulSet](/architecture/kubernetes-patterns/behavioral/stateful-service).

## Problems it solves

- Applications that must be created, scaled and destroyed without side effects
- Replicas lost to node failure or eviction that must be replaced automatically
- Pod addresses that change on every restart and break their consumers
- Version updates that cannot interrupt service

## When to use

- For APIs and request/response services that keep their state in an external database, queue or cache
- When any replica can serve any request, with no session affinity
- When you want to scale horizontally, quickly and cheaply
- For message consumers that only open outbound connections and do not need a Service

## When to avoid

- When each instance needs an identity, a stable name or its own volume: use a [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service)
- When the service depends on local memory that cannot be lost on a restart
- When only one instance may write to a piece of data: consider a [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service)
- When each replica would need a distinct volume, since in a ReplicaSet all of them share the same claim

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Fast scaling and recovery, with no dependencies among instances | State moves to external systems, which must be operated and can become a bottleneck |
| Automatic updates and rollbacks through the Deployment | The application must be designed to be disposable and tolerate restarts at any time |
| Stable address and traffic only to ready Pods through the Service | The Service and the Deployment do not know each other: whoever defines the resources must align selectors and probes |
| Interchangeable replicas simplify operations | Pod names and IPs change, so nothing can depend on them |

- **Direct ReplicaSet:** only worthwhile when the Deployment update strategies do not fit or when no control over the update is wanted; a ReplicaSet also adopts bare Pods whose labels match its selector, and may delete them if they exceed the total.
- **Access modes:** `ReadWriteOnce` allows mounting on a single node, but several Pods on that node can write; `ReadWriteMany` and `ReadOnlyMany` accept several nodes; `ReadWriteOncePod` guarantees a single Pod, but in practice prevents scaling out.
- **Shared volume:** all replicas point to the same PVC, unlike the StatefulSet, which creates one per replica.
- **Optional Service:** a workload that only opens outbound connections, such as a queue consumer, does not need a Service.
- **Combining the pieces:** Kubernetes enforces no relationship among Pod, ReplicaSet, Deployment, Service and PVC; understanding liveness, readiness and the storage policy is up to whoever assembles the whole.
- **Beyond the basics:** to scale to zero or by events, you can combine it with tools such as Knative and KEDA, covered in [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale).

## Diagram

<Diagram />

The three replicas are identical and disposable: the Service spreads the requests, the Deployment and the ReplicaSet replace whatever fails, and all state lives in the external database.

## Example

The fintech's `pix-service` API, with three interchangeable replicas, a gradual update with no downtime and a readiness probe, exposed inside the cluster by a Service.

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

The Deployment keeps three identical Pods and replaces them one by one without reducing capacity; the Service uses the same `app: pix-service` label to find the Pods and sends traffic only to those that passed readiness.

## Related patterns

- [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) — the counterpoint: stable identity and own storage per replica
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — defines how the Deployment updates and rolls back the replicas
- [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery) — the Service gives a fixed address to the ephemeral replicas
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — readiness decides which Pods receive traffic
- [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale) — scales the replicas according to load, including down to zero

## Reference

- [Kubernetes Patterns, chapter 11: Stateless Service](https://k8spatterns.com/)
- [Deployments in the Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ReplicaSet in the Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
