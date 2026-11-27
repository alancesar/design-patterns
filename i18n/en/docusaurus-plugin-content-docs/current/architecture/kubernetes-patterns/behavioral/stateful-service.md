---
title: Stateful Service
pattern_slug: stateful-service
category: Behavioral
tags:
  - Reliability
  - Performance Efficiency
source: https://k8spatterns.com/
sidebar_label: "Stateful Service"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/behavioral/stateful-service.mdx';

# Stateful Service

## Description

The Stateful Service pattern runs stateful applications using the StatefulSet resource, which gives each Pod a stable identity, its own persistent storage and a predictable order of creation, update and removal. It is the foundation for databases, queues and consensus systems, where each instance must be recognized by the others and keep its data across restarts.

In a ReplicaSet, Pods are interchangeable and disposable, with arbitrary names and disks. The StatefulSet changes this on four fronts. For **identity**, each Pod gets a name with a fixed ordinal index, such as `ledger-db-0`, which is kept when it is recreated. For **storage**, `volumeClaimTemplates` creates one PersistentVolumeClaim per replica, and the volume survives the replacement of the Pod. For **networking**, a headless Service provides a stable DNS name per Pod, allowing peers to find each other. For **ordering**, the default is to start Pods in ascending sequence and remove them in reverse, with a parallel mode available when order does not matter. There is also an at-most-one guarantee per identity and staged updates with `partition`. Without the StatefulSet, the alternatives are manual: a ReplicaSet with several replicas and one PVC would make them all share the same volume, and one ReplicaSet per instance, each with its own PVC and Service, offers no single abstraction to manage the set. Requirements beyond this, such as quorum and tolerance to duplicates, vary case by case and lead to CustomResourceDefinitions and Operators.

## Problems it solves

- Applications in which each instance needs a stable name and address to form a cluster
- Data that must remain bound to a specific replica after restarts and rescheduling
- Systems that require startup order, such as electing a primary before starting the replicas
- Preventing two instances with the same identity from writing to the same data

## When to use

- For databases, search engines, message brokers and consensus systems
- When each replica has its own non-shared persistent storage
- When peers need to address each other individually, for example for replication
- When strict uniqueness of the instance matters more than immediate availability

## When to avoid

- For applications with no local state, which scale better and more simply in a Deployment
- When using a managed data service is viable, instead of operating your own
- When the state can live in external storage and the application stays disposable
- When the team cannot operate backup, restore and replication: an Operator may be more suitable

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Stable identity and data across restarts | Slower and more careful scaling and updates than a Deployment |
| Individual discovery of peers through DNS | Requires a headless Service and cluster-formation logic in the application |
| Predictable order of creation, update and removal | A faulty Pod can block the following ones in an ordered update |
| At-most-one guarantee per identity | A node failure may leave the replica unavailable until the node returns or is removed |

- **Storage:** the StatefulSet creates PVCs but does not manage PersistentVolumes, which must be provisioned in advance or on demand by a storage class; scaling down removes the Pods and keeps the PVCs, on purpose, to avoid data loss, and removal is manual.
- **Governing Service:** `serviceName` is mandatory and the headless Service must exist before the StatefulSet; other load-balanced Services over the same Pods can also be created.
- **Breaking the guarantee:** force-deleting a Pod or deleting from the API Server the object of a node that is still running can create duplicates; do this only when certain the process has stopped.
- **Backup:** the StatefulSet does not do backup or replication; that is left to the application or to an [Operator](/architecture/kubernetes-patterns/advanced/operator).
- **Management mode:** `OrderedReady` serializes operations, and `Parallel` speeds things up when order is irrelevant.
- **Staged update:** `partition` allows updating only the Pods with a higher index and validating before continuing.
- **Sizing:** requests, limits and the storage class affect the performance and cost of each replica.

## Diagram

<Diagram />

Each Pod has a fixed name, its own volume and an individual DNS record through the headless Service, so `ledger-service` and the peers themselves can address specific replicas.

## Example

The fintech's ledger database with three replicas, one volume per replica and a headless Service for peer discovery.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ledger-db
  namespace: fintech
spec:
  clusterIP: None
  selector:
    app: ledger-db
  ports:
    - name: sql
      port: 5432
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ledger-db
  namespace: fintech
spec:
  serviceName: ledger-db
  replicas: 3
  selector:
    matchLabels:
      app: ledger-db
  template:
    metadata:
      labels:
        app: ledger-db
    spec:
      containers:
        - name: db
          image: registry.fintech.example/ledger-db:15.4
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/db
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
```

`clusterIP: None` creates the headless Service, and `volumeClaimTemplates` generates the volumes `data-ledger-db-0`, `data-ledger-db-1` and `data-ledger-db-2`, which follow each Pod.

## Related patterns

- [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) — uses the StatefulSet's at-most-one guarantee with a single replica
- [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery) — the headless Service exposes each Pod through its own DNS name
- [Operator](/architecture/kubernetes-patterns/advanced/operator) — automates backup, failover and upgrades that the StatefulSet alone does not solve
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — readiness defines when the next ordered Pod can start
- [Leader Election](/architecture/cloud-design-patterns/distributed-coordination/leader-election) — replicated databases elect a primary among the StatefulSet's Pods

## Reference

- [Kubernetes Patterns, chapter 12: Stateful Service](https://k8spatterns.com/)
- [StatefulSets in the Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Persistent volumes in the Kubernetes documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
