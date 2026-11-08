---
title: "Microservices Patterns"
sidebar_label: "Microservices"
---

# Microservices Patterns

Personal catalog based on Chris Richardson's [microservices.io](https://microservices.io/patterns/). Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (Well-Architected Framework pillars), and a Mermaid diagram.

Patterns marked with ★ are shared with another catalog: this catalog points to the original document, revised with content from this source.

Total: 53 patterns in 15 groups. Tags: Well-Architected Framework pillars.

## Groups

- [Architectural Style](#architectural-style) (2)
- [Service Boundaries](#service-boundaries) (4)
- [Refactoring to Services](#refactoring-to-services) (2)
- [Service Collaboration](#service-collaboration) (8)
- [Transactional Messaging](#transactional-messaging) (3)
- [Testing](#testing) (3)
- [Deployment](#deployment) (6)
- [Cross-cutting Concerns](#cross-cutting-concerns) (3)
- [Communication Styles](#communication-styles) (4)
- [External API](#external-api) (2)
- [Service Discovery](#service-discovery) (5)
- [Reliability](#reliability) (1)
- [Security](#security) (1)
- [Observability](#observability) (7)
- [UI Design](#ui-design) (2)

## Architectural Style (2) {#architectural-style}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Monolithic Architecture](/architecture/microservices/architectural-style/monolithic-architecture) | Monolithic Architecture structures the application as a single deployable component backed by a single database. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |
| [Microservice Architecture](/architecture/microservices/architectural-style/microservice-architecture) | Microservice Architecture structures the application as two or more independently deployable, loosely coupled services. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Security`](/tags/security) |

## Service Boundaries (4) {#service-boundaries}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Decompose by Business Capability](/architecture/microservices/service-boundaries/decompose-by-business-capability) | Decompose by Business Capability defines services from business capabilities, that is, the things the organization does to generate value, such as order management, catalog, inventory, or delivery. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Decompose by Subdomain](/architecture/microservices/service-boundaries/decompose-by-subdomain) | Decompose by Subdomain defines services from Domain-Driven Design (DDD) subdomains, which represent the distinct areas of the business. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Self-contained Service](/architecture/microservices/service-boundaries/self-contained-service) | Self-contained Service designs a service to respond to a synchronous request without having to wait for any other service. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service per Team](/architecture/microservices/service-boundaries/service-per-team) | Service per Team establishes that each service belongs to exactly one team, which has sole responsibility for changing it. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |

## Refactoring to Services (2) {#refactoring-to-services}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Strangler Application](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig) ★ | The Strangler Fig pattern incrementally migrates a legacy system by replacing specific pieces of functionality, one by one, with new applications and services. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Anti-Corruption Layer](/architecture/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) ★ | The Anti-Corruption Layer is a facade or adapter layer placed between subsystems that don't share the same semantics. | [`Operational Excellence`](/tags/operational-excellence) |

## Service Collaboration (8) {#service-collaboration}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Database per Service](/architecture/microservices/service-collaboration/database-per-service) | In the Database per Service pattern, each service's persistent data is private to it and can only be accessed through its API. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Shared Database](/architecture/microservices/service-collaboration/shared-database) | In the Shared Database pattern, all services use a single database. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Saga](/architecture/cloud-design-patterns/distributed-coordination/saga) ★ | The Saga pattern maintains data consistency in distributed systems by splitting a business operation that spans several services into a sequence of **local transactions**. | [`Reliability`](/tags/reliability) |
| [Command-side Replica](/architecture/microservices/service-collaboration/command-side-replica) | In an architecture with Database per Service, a service that executes a command often needs data that belongs to another service. | [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [API Composition](/architecture/microservices/service-collaboration/api-composition) | In an application with microservices and Database per Service, the data is spread across private databases, and queries that combine information from several services are no longer a simple *join*. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [CQRS](/architecture/cloud-design-patterns/data-management/cqrs) ★ | CQRS (Command Query Responsibility Segregation) separates the operations that change data (*commands*) from the operations that read data (*queries*), using distinct models for each side. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [Domain Event](/architecture/microservices/service-collaboration/domain-event) | A *Domain Event*, a concept from Domain-Driven Design, is a business-relevant fact that occurred in the domain, such as `OrderCreated` or `CreditReserved`. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Event Sourcing](/architecture/cloud-design-patterns/data-management/event-sourcing) ★ | Instead of storing only the current state of the data and overwriting it on every change (the CRUD model), Event Sourcing records the entire sequence of actions applied to an entity as immutable events in an append-only store, the **event store**. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Transactional Messaging (3) {#transactional-messaging}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Transactional Outbox](/architecture/microservices/transactional-messaging/transactional-outbox) | Transactional Outbox solves the problem of updating a service's database and, at the same time, sending a message or event to a message broker atomically. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Transaction Log Tailing](/architecture/microservices/transactional-messaging/transaction-log-tailing) | Transaction Log Tailing is one way to implement the message relay of the Transactional Outbox. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Polling Publisher](/architecture/microservices/transactional-messaging/polling-publisher) | Polling Publisher is one way to implement the message relay of the Transactional Outbox. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |

## Testing (3) {#testing}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Consumer-driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test) | In Consumer-driven Contract Test, the developers of each consumer service write a set of tests (contracts) describing what they expect from a provider service's API. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Consumer-side Contract Test](/architecture/microservices/testing/consumer-side-contract-test) | Consumer-side Contract Test verifies that a service's client can communicate with it. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Component Test](/architecture/microservices/testing/service-component-test) | Service Component Test is a set of tests that exercises a single service in isolation, treating it as a black box accessed through its API. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Cost Optimization`](/tags/cost-optimization) |

## Deployment (6) {#deployment}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Multiple Service Instances per Host](/architecture/microservices/deployment/multiple-service-instances-per-host) | In this pattern, instances of different services run on the same host, which can be physical or virtual. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per Host](/architecture/microservices/deployment/service-instance-per-host) | Each service instance is deployed on its own host, which can be a physical or virtual machine. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per VM](/architecture/microservices/deployment/service-instance-per-vm) | The service is packaged as a virtual machine image and each instance is deployed as a separate VM. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per Container](/architecture/microservices/deployment/service-instance-per-container) | The service is packaged as a container image (for example, Docker) and each instance runs as a container. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |
| [Serverless Deployment](/architecture/microservices/deployment/serverless-deployment) | The service is deployed on infrastructure that hides any concept of a server, whether physical, virtual, or container. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) | The pattern proposes using a deployment platform, that is, automated infrastructure for deploying applications. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) |

## Cross-cutting Concerns (3) {#cross-cutting-concerns}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Microservice Chassis](/architecture/microservices/cross-cutting-concerns/microservice-chassis) | The Microservice Chassis is a shared framework that serves as the foundation for all of an organization's services. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Security`](/tags/security) |
| [Externalized Configuration](/architecture/cloud-design-patterns/deployment-and-topology/external-configuration-store) ★ | The External Configuration Store pattern moves configuration information out of the application deployment package and into a centralized repository. | [`Operational Excellence`](/tags/operational-excellence) |
| [Service Template](/architecture/microservices/cross-cutting-concerns/service-template) | The Service Template is a source-code template that developers copy to start a new service. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |

## Communication Styles (4) {#communication-styles}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation) | Remote Procedure Invocation (RPI) is the communication style in which a client sends a request to a service using a synchronous request/response protocol, as if it were invoking a remote procedure. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Messaging](/architecture/microservices/communication-styles/messaging) | In the Messaging pattern, services communicate asynchronously by exchanging messages over message channels. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Domain-specific Protocol](/architecture/microservices/communication-styles/domain-specific-protocol) | The Domain-specific Protocol pattern proposes that communication between services, or between clients and services, use a protocol native to the problem domain instead of a generic request/response or messaging protocol. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer) ★ | The Idempotent Consumer pattern designs message consumers so that processing the same message more than once has exactly the same effect as processing it a single time. | [`Reliability`](/tags/reliability) |

## External API (2) {#external-api}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [API Gateway](/architecture/microservices/external-api/api-gateway) | The API Gateway is the single entry point between clients and an application's microservices. | [`Performance Efficiency`](/tags/performance-efficiency) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Backend for Front-end](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) ★ | The Backends for Frontends (BFF) pattern proposes creating a separate backend service for each frontend interface (for example, web application, mobile app, embedded devices), instead of using a single general-purpose backend for all of them. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |

## Service Discovery (5) {#service-discovery}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Client-side Discovery](/architecture/microservices/service-discovery/client-side-discovery) | In Client-side Discovery, the client of a service (another service or an API gateway) is responsible for finding where the available instances are. | [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [Server-side Discovery](/architecture/microservices/service-discovery/server-side-discovery) | In Server-side Discovery, the client sends its requests to a router (also called a load balancer) at a well-known address. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Registry](/architecture/microservices/service-discovery/service-registry) | The Service Registry is a database of services, their instances, and their locations. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Self Registration](/architecture/microservices/service-discovery/self-registration) | In Self Registration, each service instance is responsible for registering itself in the Service Registry, supplying its host and IP address at startup. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [3rd Party Registration](/architecture/microservices/service-discovery/3rd-party-registration) | In 3rd Party Registration, a separate component, the registrar, takes care of registering each instance in the Service Registry when it starts and removing it when it shuts down. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |

## Reliability (1) {#reliability}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Circuit Breaker](/architecture/cloud-design-patterns/resiliency/circuit-breaker) ★ | The Circuit Breaker temporarily blocks access to a remote service or resource when failures exceed a threshold. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Security (1) {#security}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Access Token](/architecture/microservices/security/access-token) | Access Token is the pattern in which the identity of the requester is carried by a secure token, instead of each service re-authenticating the client. | [`Security`](/tags/security) [`Reliability`](/tags/reliability) |

## Observability (7) {#observability}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Log Aggregation](/architecture/microservices/observability/log-aggregation) | In a microservices architecture, each service instance writes its own logs (errors, warnings, info, and debug) in a standardized format. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Application Metrics](/architecture/microservices/observability/application-metrics) | Each service is instrumented to collect statistics about its individual operations, such as request counts, error rates, latencies, and resource usage. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Audit Logging](/architecture/microservices/observability/audit-logging) | The pattern records user actions (who did what, when, and on which resource) in a dedicated data store, such as a database. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Distributed Tracing](/architecture/microservices/observability/distributed-tracing) | In microservices, a single external request often passes through several services, each performing operations such as database queries or publishing messages. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [Exception Tracking](/architecture/microservices/observability/exception-tracking) | When a request fails, a service instance throws an exception with an error message and a stack trace. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring) ★ | The application exposes health endpoints (for example, `/health` over HTTPS or gRPC's standard health checking protocol) that external tools query at regular intervals. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Log Deployments and Changes](/architecture/microservices/observability/log-deployments-and-changes) | Problems in production often appear right after a change. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |

## UI Design (2) {#ui-design}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Server-side Page Fragment Composition](/architecture/microservices/ui-design/server-side-page-fragment-composition) | In a microservices architecture with teams organized by business capability or subdomain, each team also owns the user experience related to its service. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Client-side UI Composition](/architecture/microservices/ui-design/client-side-ui-composition) | In a microservices architecture with teams organized by business capability or subdomain, each team is also responsible for the user experience of its service. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |

## By tag

### Reliability (38)

[Microservice Architecture](/architecture/microservices/architectural-style/microservice-architecture), [Decompose by Business Capability](/architecture/microservices/service-boundaries/decompose-by-business-capability), [Decompose by Subdomain](/architecture/microservices/service-boundaries/decompose-by-subdomain), [Self-contained Service](/architecture/microservices/service-boundaries/self-contained-service), [Strangler Application](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig), [Database per Service](/architecture/microservices/service-collaboration/database-per-service), [Shared Database](/architecture/microservices/service-collaboration/shared-database), [Saga](/architecture/cloud-design-patterns/distributed-coordination/saga), [Command-side Replica](/architecture/microservices/service-collaboration/command-side-replica), [Domain Event](/architecture/microservices/service-collaboration/domain-event), [Event Sourcing](/architecture/cloud-design-patterns/data-management/event-sourcing), [Transactional Outbox](/architecture/microservices/transactional-messaging/transactional-outbox), [Transaction Log Tailing](/architecture/microservices/transactional-messaging/transaction-log-tailing), [Polling Publisher](/architecture/microservices/transactional-messaging/polling-publisher), [Consumer-driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test), [Consumer-side Contract Test](/architecture/microservices/testing/consumer-side-contract-test), [Service Component Test](/architecture/microservices/testing/service-component-test), [Service Instance per Host](/architecture/microservices/deployment/service-instance-per-host), [Service Instance per VM](/architecture/microservices/deployment/service-instance-per-vm), [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform), [Microservice Chassis](/architecture/microservices/cross-cutting-concerns/microservice-chassis), [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation), [Messaging](/architecture/microservices/communication-styles/messaging), [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer), [Backend for Front-end](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends), [Client-side Discovery](/architecture/microservices/service-discovery/client-side-discovery), [Server-side Discovery](/architecture/microservices/service-discovery/server-side-discovery), [Service Registry](/architecture/microservices/service-discovery/service-registry), [Self Registration](/architecture/microservices/service-discovery/self-registration), [3rd Party Registration](/architecture/microservices/service-discovery/3rd-party-registration), [Circuit Breaker](/architecture/cloud-design-patterns/resiliency/circuit-breaker), [Access Token](/architecture/microservices/security/access-token), [Log Aggregation](/architecture/microservices/observability/log-aggregation), [Application Metrics](/architecture/microservices/observability/application-metrics), [Distributed Tracing](/architecture/microservices/observability/distributed-tracing), [Exception Tracking](/architecture/microservices/observability/exception-tracking), [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring), [Log Deployments and Changes](/architecture/microservices/observability/log-deployments-and-changes)

### Security (9)

[Microservice Architecture](/architecture/microservices/architectural-style/microservice-architecture), [Service Instance per Host](/architecture/microservices/deployment/service-instance-per-host), [Service Instance per VM](/architecture/microservices/deployment/service-instance-per-vm), [Microservice Chassis](/architecture/microservices/cross-cutting-concerns/microservice-chassis), [Service Template](/architecture/microservices/cross-cutting-concerns/service-template), [API Gateway](/architecture/microservices/external-api/api-gateway), [Backend for Front-end](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends), [Access Token](/architecture/microservices/security/access-token), [Audit Logging](/architecture/microservices/observability/audit-logging)

### Cost Optimization (7)

[Monolithic Architecture](/architecture/microservices/architectural-style/monolithic-architecture), [Strangler Application](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig), [Service Component Test](/architecture/microservices/testing/service-component-test), [Multiple Service Instances per Host](/architecture/microservices/deployment/multiple-service-instances-per-host), [Service Instance per Container](/architecture/microservices/deployment/service-instance-per-container), [Serverless Deployment](/architecture/microservices/deployment/serverless-deployment), [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform)

### Operational Excellence (41)

[Monolithic Architecture](/architecture/microservices/architectural-style/monolithic-architecture), [Microservice Architecture](/architecture/microservices/architectural-style/microservice-architecture), [Decompose by Business Capability](/architecture/microservices/service-boundaries/decompose-by-business-capability), [Decompose by Subdomain](/architecture/microservices/service-boundaries/decompose-by-subdomain), [Service per Team](/architecture/microservices/service-boundaries/service-per-team), [Strangler Application](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig), [Anti-Corruption Layer](/architecture/cloud-design-patterns/integration-and-modernization/anti-corruption-layer), [Database per Service](/architecture/microservices/service-collaboration/database-per-service), [Shared Database](/architecture/microservices/service-collaboration/shared-database), [Domain Event](/architecture/microservices/service-collaboration/domain-event), [Transactional Outbox](/architecture/microservices/transactional-messaging/transactional-outbox), [Polling Publisher](/architecture/microservices/transactional-messaging/polling-publisher), [Consumer-driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test), [Consumer-side Contract Test](/architecture/microservices/testing/consumer-side-contract-test), [Service Component Test](/architecture/microservices/testing/service-component-test), [Multiple Service Instances per Host](/architecture/microservices/deployment/multiple-service-instances-per-host), [Service Instance per Host](/architecture/microservices/deployment/service-instance-per-host), [Service Instance per VM](/architecture/microservices/deployment/service-instance-per-vm), [Service Instance per Container](/architecture/microservices/deployment/service-instance-per-container), [Serverless Deployment](/architecture/microservices/deployment/serverless-deployment), [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform), [Microservice Chassis](/architecture/microservices/cross-cutting-concerns/microservice-chassis), [Externalized Configuration](/architecture/cloud-design-patterns/deployment-and-topology/external-configuration-store), [Service Template](/architecture/microservices/cross-cutting-concerns/service-template), [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation), [Messaging](/architecture/microservices/communication-styles/messaging), [Domain-specific Protocol](/architecture/microservices/communication-styles/domain-specific-protocol), [API Gateway](/architecture/microservices/external-api/api-gateway), [Server-side Discovery](/architecture/microservices/service-discovery/server-side-discovery), [Service Registry](/architecture/microservices/service-discovery/service-registry), [Self Registration](/architecture/microservices/service-discovery/self-registration), [3rd Party Registration](/architecture/microservices/service-discovery/3rd-party-registration), [Log Aggregation](/architecture/microservices/observability/log-aggregation), [Application Metrics](/architecture/microservices/observability/application-metrics), [Audit Logging](/architecture/microservices/observability/audit-logging), [Distributed Tracing](/architecture/microservices/observability/distributed-tracing), [Exception Tracking](/architecture/microservices/observability/exception-tracking), [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring), [Log Deployments and Changes](/architecture/microservices/observability/log-deployments-and-changes), [Server-side Page Fragment Composition](/architecture/microservices/ui-design/server-side-page-fragment-composition), [Client-side UI Composition](/architecture/microservices/ui-design/client-side-ui-composition)

### Performance Efficiency (24)

[Monolithic Architecture](/architecture/microservices/architectural-style/monolithic-architecture), [Microservice Architecture](/architecture/microservices/architectural-style/microservice-architecture), [Self-contained Service](/architecture/microservices/service-boundaries/self-contained-service), [Service per Team](/architecture/microservices/service-boundaries/service-per-team), [Database per Service](/architecture/microservices/service-collaboration/database-per-service), [Command-side Replica](/architecture/microservices/service-collaboration/command-side-replica), [API Composition](/architecture/microservices/service-collaboration/api-composition), [CQRS](/architecture/cloud-design-patterns/data-management/cqrs), [Event Sourcing](/architecture/cloud-design-patterns/data-management/event-sourcing), [Transaction Log Tailing](/architecture/microservices/transactional-messaging/transaction-log-tailing), [Service Instance per Container](/architecture/microservices/deployment/service-instance-per-container), [Serverless Deployment](/architecture/microservices/deployment/serverless-deployment), [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation), [Messaging](/architecture/microservices/communication-styles/messaging), [Domain-specific Protocol](/architecture/microservices/communication-styles/domain-specific-protocol), [API Gateway](/architecture/microservices/external-api/api-gateway), [Backend for Front-end](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends), [Client-side Discovery](/architecture/microservices/service-discovery/client-side-discovery), [Circuit Breaker](/architecture/cloud-design-patterns/resiliency/circuit-breaker), [Application Metrics](/architecture/microservices/observability/application-metrics), [Distributed Tracing](/architecture/microservices/observability/distributed-tracing), [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring), [Server-side Page Fragment Composition](/architecture/microservices/ui-design/server-side-page-fragment-composition), [Client-side UI Composition](/architecture/microservices/ui-design/client-side-ui-composition)
