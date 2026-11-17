---
title: "Kubernetes Patterns"
sidebar_label: "Kubernetes Patterns"
---

# Kubernetes Patterns

Personal catalog based on the book [*Kubernetes Patterns*](https://k8spatterns.com/), by Bilgin Ibryam and Roland Huß (O'Reilly, 1st edition, 2019), which describes reusable elements for designing cloud-native applications on Kubernetes. Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (Well-Architected Framework pillars), a Mermaid diagram and, where it helps, an example YAML manifest.

Patterns marked with ★ are shared with another catalog: this catalog points to the original document, revised with content from this source.

Total: 24 patterns in 5 groups. Tags: Well-Architected Framework pillars.

## Groups

- [Foundational](#foundational) (5)
- [Behavioral](#behavioral) (7)
- [Structural](#structural) (4)
- [Configuration](#configuration) (4)
- [Advanced](#advanced) (4)

## Foundational (5) {#foundational}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) | The Predictable Demands pattern consists of declaring, in each workload manifest, the runtime dependencies and the resource profile of its containers, so that Kubernetes knows where to place them and how to treat them when the cluster is under pressure. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) | The Declarative Deployment pattern describes the desired version of an application in a `Deployment` resource and lets Kubernetes execute, on the server side, all the steps to go from the current version to it, in a repeatable way and with the ability to roll back. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) | The Health Probe pattern makes the application expose signals about its own state to Kubernetes, through probes that the kubelet runs periodically, so that the platform decides whether to restart the container or stop sending it traffic. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle) | The Managed Lifecycle pattern makes the application listen and react to the lifecycle events emitted by Kubernetes, such as termination signals and start and stop hooks, so it can start and finish cleanly, without losing work in progress. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement) | The Automated Placement pattern delegates to the Kubernetes scheduler the decision of which node each Pod will run on, considering the requested resources and the declared placement rules, and allows influencing that decision without choosing nodes manually. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |

## Behavioral (7) {#behavioral}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) | The Batch Job pattern runs a finite, isolated unit of work in short-lived Pods, using the Kubernetes Job resource to make sure it finishes successfully even when containers or nodes fail. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) |
| [Periodic Job](/architecture/kubernetes-patterns/behavioral/periodic-job) | The Periodic Job pattern triggers the execution of a Batch Job from a temporal event, using the Kubernetes CronJob resource to schedule the creation of Jobs in cron format. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Daemon Service](/architecture/kubernetes-patterns/behavioral/daemon-service) | The Daemon Service pattern runs an infrastructure Pod on every node of the cluster, or on a chosen subset of nodes, using the DaemonSet resource to extend the platform's capabilities. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) | The Singleton Service pattern guarantees that only one active instance of a service runs at a time, either through external control by the platform or through a leadership contest inside the application itself. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) | The Stateful Service pattern runs stateful applications using the StatefulSet resource, which gives each Pod a stable identity, its own persistent storage and a predictable order of creation, update and removal. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery) | The Service Discovery pattern gives a set of Pods a stable access point, with a fixed name and address, using the Kubernetes Service resource so that consumers find producers without knowing their dynamic addresses. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness) | The Self Awareness pattern lets an application learn information about itself and the environment it runs in, using the Kubernetes Downward API to inject Pod metadata through environment variables or files. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |

## Structural (4) {#structural}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Init Container](/architecture/kubernetes-patterns/structural/init-container) | The Init Container pattern separates a Pod's initialization tasks from the application containers, running them beforehand, in sequence, and with their own lifecycle. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) ★ | The Sidecar pattern deploys an application's helper components in a separate process or container that runs alongside the main application. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Adapter](/architecture/kubernetes-patterns/structural/adapter) | The Adapter pattern uses a helper container in the same Pod to make a heterogeneous system expose a uniform, normalized interface that can be consumed from outside the Pod. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador) ★ | The Ambassador pattern creates helper services that send network requests on behalf of a consumer application or service. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) |

## Configuration (4) {#configuration}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration) | The EnvVar Configuration pattern externalizes an application's configuration into environment variables, the simplest and most universally supported way to change a container's behavior without rebuilding the image. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |
| [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource) | The Configuration Resource pattern keeps an application's configuration in native Kubernetes resources, ConfigMap for regular data and Secret for confidential data, decoupling the configuration lifecycle from the application lifecycle. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |
| [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration) | The Immutable Configuration pattern packages an environment's configuration data into a passive, versioned container image that is linked to the application only at runtime. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Configuration Template](/architecture/kubernetes-patterns/configuration/configuration-template) | The Configuration Template pattern generates, at application startup, large and complex configuration files from a single template and a small set of environment-specific parameters. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |

## Advanced (4) {#advanced}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Controller](/architecture/kubernetes-patterns/advanced/controller) | The Controller pattern is a process that continuously watches a set of Kubernetes resources and acts to bring the actual state closer to the desired state declared in them. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Operator](/architecture/kubernetes-patterns/advanced/operator) | The Operator pattern is a Controller that uses a CustomResourceDefinition (CRD) to encapsulate the operational knowledge of a specific application in an algorithmic, automated form. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale) | The Elastic Scale pattern makes an application's capacity follow the load automatically, scaling in several dimensions: horizontally (number of Pod replicas), vertically (requests and limits of each Pod) and at the cluster level (number of nodes). | [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) [`Reliability`](/tags/reliability) |
| [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder) | The Image Builder pattern builds container images inside the Kubernetes cluster itself, using the platform's scheduler and resources to run the builds instead of an external build system. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |

## By tag

### Reliability (18)

[Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands), [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment), [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe), [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle), [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement), [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job), [Periodic Job](/architecture/kubernetes-patterns/behavioral/periodic-job), [Daemon Service](/architecture/kubernetes-patterns/behavioral/daemon-service), [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service), [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service), [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery), [Init Container](/architecture/kubernetes-patterns/structural/init-container), [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador), [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration), [Configuration Template](/architecture/kubernetes-patterns/configuration/configuration-template), [Controller](/architecture/kubernetes-patterns/advanced/controller), [Operator](/architecture/kubernetes-patterns/advanced/operator), [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale)

### Cost Optimization (4)

[Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands), [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement), [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job), [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale)

### Performance Efficiency (7)

[Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands), [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement), [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service), [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery), [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness), [Adapter](/architecture/kubernetes-patterns/structural/adapter), [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale)

### Operational Excellence (17)

[Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment), [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe), [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle), [Periodic Job](/architecture/kubernetes-patterns/behavioral/periodic-job), [Daemon Service](/architecture/kubernetes-patterns/behavioral/daemon-service), [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service), [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness), [Init Container](/architecture/kubernetes-patterns/structural/init-container), [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar), [Adapter](/architecture/kubernetes-patterns/structural/adapter), [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration), [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource), [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration), [Configuration Template](/architecture/kubernetes-patterns/configuration/configuration-template), [Controller](/architecture/kubernetes-patterns/advanced/controller), [Operator](/architecture/kubernetes-patterns/advanced/operator), [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder)

### Security (5)

[Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar), [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador), [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration), [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource), [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder)
