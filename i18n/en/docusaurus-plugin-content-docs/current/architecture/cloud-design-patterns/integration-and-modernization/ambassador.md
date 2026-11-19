---
title: Ambassador
pattern_slug: ambassador
category: Integration and Modernization
tags:
  - Reliability
  - Security
also_in:
  - architecture/kubernetes-patterns/structural
source: https://learn.microsoft.com/en-us/azure/architecture/patterns/ambassador
sidebar_label: "Ambassador"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/cloud-design-patterns/integration-and-modernization/ambassador.mdx';

# Ambassador

## Description

The Ambassador pattern creates helper services that send network requests on behalf of a consumer application or service. The ambassador acts as an out-of-process proxy deployed alongside the application (on the same host, VM, or pod), so the application talks only to this local proxy instead of calling remote services directly.

This moves cross-cutting client connectivity tasks, such as monitoring, logging, routing, encryption (TLS/mTLS), authentication, and resiliency patterns (retry, circuit breaker), out of the application code and into a language-independent component. The ambassador can be updated, configured, and operated separately, often by teams specialized in networking, security, or platform.

The ambassador can be deployed as a sidecar that follows the application's lifecycle, as a daemon or system service shared by several processes on the same host, or, in containerized environments, as a separate container next to the application container.

In Kubernetes, the ambassador is a container in the same Pod that listens on a localhost port; the application talks to it as if it were the final service, and it hides the complexity of reaching dependencies outside the Pod, such as client-side service discovery, balancing across cache shards, or protection against unreliable protocols. Since the application only knows the local address, the ambassador can be swapped by reconfiguring the Pod, without touching the main container: for example, an in-memory cache in development and a distributed cache in production.

## Problems it solves

- Legacy or hard-to-modify applications that need modern connectivity features (circuit breaking, routing, metrics, network configuration updates).
- Repeated connection, authentication, and authorization setup across multiple applications written in different languages and frameworks.
- The risk of a central network or security team having to change code in applications it doesn't know.
- Lack of standardized instrumentation (latency, resource usage, tracing) on outbound calls.
- The need to apply security controls (encryption, mutual authentication) that the client can't implement directly.

## When to use

- When you need to build a common set of client connectivity features for multiple languages or frameworks.
- When cross-cutting connectivity concerns should be delegated to infrastructure or other specialized teams.
- When a legacy or hard-to-change application needs to meet cloud or cluster connectivity requirements.
- When you need to support protocols or connectivity patterns that API gateways, service meshes, or standard ingress and egress controls don't handle easily.

## When to avoid

- When network request latency is critical and even the small overhead of the proxy is unacceptable.
- When the connectivity features are consumed by a single language; a client library distributed as a package tends to be simpler.
- When the connectivity features can't be generalized and require deep integration with the application logic.
- When the platform already offers ready-made solutions, such as a service mesh, for mTLS, traffic management, and policies; prefer them over a custom ambassador.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Resiliency (retry, circuit breaker, buffering) applied without changing the application | Added latency on every call because of the extra proxy hop |
| Network security (TLS/mTLS, authentication) centralized and language-independent | One more component to package, deploy, version, and monitor |
| Specialized teams evolve networking and security without touching application code | Generic retries can be dangerous if operations aren't idempotent |
| Standardized instrumentation and telemetry on outbound calls | A shared instance becomes a single point of failure and contention; a per-client instance consumes more resources |

- **Context between client and proxy:** define a mechanism for the application to pass instructions to the ambassador, for example headers that disable retry or limit the number of attempts.
- **Deployment model:** choose between one instance per client (sidecar) or one instance shared per host, weighing isolation against resource consumption.
- **Idempotency:** only enable automatic retries for operations that can be safely repeated.
- **Observability:** the ambassador is a natural place to measure latency, log calls, and propagate tracing information.
- **Local scope:** the ambassador's port is reachable only inside the Pod, which simplifies security but makes each replica carry its own instance.
- **Operational complexity:** the proxy's lifecycle (updates, configuration, health) must be managed together with the application's.

## Diagram

<Diagram />

The application sends its requests to the ambassador colocated on the same host, which resolves the destination, applies resiliency and security, forwards the call to the remote service, and returns the response, recording metrics such as latency. As a specific example, on Azure Kubernetes Service the ambassador usually runs as a sidecar container in the same pod as the application.

## Related patterns

- [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) — the ambassador is a specialization of the sidecar focused on outbound connectivity and is often deployed that way.
- [Adapter (Kubernetes Patterns)](/architecture/kubernetes-patterns/structural/adapter) — the other sidecar specialization: it exposes the application uniformly instead of mediating access to external services.
- [Init Container](/architecture/kubernetes-patterns/structural/init-container) — can prepare the configuration the ambassador will use before the Pod starts serving.
- [Circuit Breaker](/architecture/cloud-design-patterns/resiliency/circuit-breaker) — one of the most common resiliency features to implement inside the ambassador.
- [Retry](/architecture/cloud-design-patterns/resiliency/retry) — the ambassador can apply retries transparently, as long as the operations are idempotent.
- [Gateway Offloading](/architecture/cloud-design-patterns/gateways-and-edge/gateway-offloading) — also offloads cross-cutting concerns, but centrally on the server side rather than next to the client.
- [Anti-Corruption Layer](/architecture/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) — also sits between the application and external systems, but to translate semantics rather than handle connectivity.

## Reference

- [Azure Architecture Center documentation](https://learn.microsoft.com/en-us/azure/architecture/patterns/ambassador)
- [Kubernetes Patterns, chapter 18: Ambassador](https://k8spatterns.com/)
