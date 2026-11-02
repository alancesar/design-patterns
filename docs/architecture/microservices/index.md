---
title: "Microservices Patterns"
sidebar_label: "Microservices"
---

# Microservices Patterns

Catálogo pessoal baseado no [microservices.io](https://microservices.io/patterns/), de Chris Richardson. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (pilares do Well-Architected Framework) e um diagrama Mermaid.

Padrões marcados com ★ são compartilhados com outro catálogo: este catálogo aponta para o documento original, revisado com o conteúdo desta fonte.

Total: 53 padrões em 15 grupos. Etiquetas: Pilares do Well-Architected Framework.

## Grupos

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

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Monolithic Architecture](./architectural-style/monolithic-architecture.md) | Monolithic Architecture estrutura a aplicação como um único componente implantável, apoiado por um único banco de dados. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |
| [Microservice Architecture](./architectural-style/microservice-architecture.md) | Microservice Architecture estrutura a aplicação como dois ou mais serviços implantáveis de forma independente e fracamente acoplados. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Security`](/tags/security) |

## Service Boundaries (4) {#service-boundaries}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Decompose by Business Capability](./service-boundaries/decompose-by-business-capability.md) | Decompose by Business Capability define os serviços a partir das capacidades de negócio, isto é, das coisas que a organização faz para gerar valor, como gestão de pedidos, catálogo, estoque ou entrega. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Decompose by Subdomain](./service-boundaries/decompose-by-subdomain.md) | Decompose by Subdomain define os serviços a partir dos subdomínios do Domain-Driven Design (DDD), que representam as áreas distintas do negócio. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Self-contained Service](./service-boundaries/self-contained-service.md) | Self-contained Service projeta um serviço para responder a uma requisição síncrona sem precisar esperar por nenhum outro serviço. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service per Team](./service-boundaries/service-per-team.md) | Service per Team estabelece que cada serviço pertence a exatamente uma equipe, que tem a responsabilidade exclusiva de alterá-lo. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |

## Refactoring to Services (2) {#refactoring-to-services}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Strangler Application](../../cloud/cloud-design-patterns/integration-and-modernization/strangler-fig.md) ★ | O padrão Strangler Fig migra um sistema legado de forma incremental, substituindo funcionalidades específicas, uma a uma, por novas aplicações e serviços. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Anti-Corruption Layer](../../cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer.md) ★ | O Anti-Corruption Layer (camada anticorrupção) é uma fachada ou camada de adaptação colocada entre subsistemas que não compartilham a mesma semântica. | [`Operational Excellence`](/tags/operational-excellence) |

## Service Collaboration (8) {#service-collaboration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Database per Service](./service-collaboration/database-per-service.md) | No padrão Database per Service, os dados persistentes de cada serviço são privados a ele e só podem ser acessados por meio da sua API. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Shared Database](./service-collaboration/shared-database.md) | No padrão Shared Database, todos os serviços utilizam um único banco de dados. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Saga](../../cloud/cloud-design-patterns/distributed-coordination/saga.md) ★ | O padrão Saga mantém a consistência de dados em sistemas distribuídos ao dividir uma operação de negócio que envolve vários serviços em uma sequência de **transações locais**. | [`Reliability`](/tags/reliability) |
| [Command-side Replica](./service-collaboration/command-side-replica.md) | Em uma arquitetura com Database per Service, um serviço que executa um comando muitas vezes precisa de dados que pertencem a outro serviço. | [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [API Composition](./service-collaboration/api-composition.md) | Em uma aplicação com microsserviços e Database per Service, os dados estão espalhados em bancos privados, e consultas que combinam informações de vários serviços deixam de ser um simples *join*. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [CQRS](../../cloud/cloud-design-patterns/data-management/cqrs.md) ★ | O CQRS (Command Query Responsibility Segregation) separa as operações que alteram dados (*commands*) das operações que leem dados (*queries*), usando modelos distintos para cada lado. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [Domain Event](./service-collaboration/domain-event.md) | Um evento de domínio (*Domain Event*), conceito vindo do Domain-Driven Design, é um fato relevante para o negócio que ocorreu no domínio, como `PedidoCriado` ou `CreditoReservado`. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Event Sourcing](../../cloud/cloud-design-patterns/data-management/event-sourcing.md) ★ | Em vez de guardar apenas o estado atual dos dados e sobrescrevê-lo a cada alteração (modelo CRUD), o Event Sourcing registra toda a sequência de ações aplicadas a uma entidade como eventos imutáveis em um armazenamento somente de acréscimo (*append-only*), o **event store**. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Transactional Messaging (3) {#transactional-messaging}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Transactional Outbox](./transactional-messaging/transactional-outbox.md) | O Transactional Outbox resolve o problema de atualizar o banco de dados de um serviço e, ao mesmo tempo, enviar uma mensagem ou evento a um message broker de forma atômica. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Transaction Log Tailing](./transactional-messaging/transaction-log-tailing.md) | O Transaction Log Tailing é uma forma de implementar o message relay do Transactional Outbox. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Polling Publisher](./transactional-messaging/polling-publisher.md) | O Polling Publisher é uma forma de implementar o message relay do Transactional Outbox. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |

## Testing (3) {#testing}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Consumer-driven Contract Test](./testing/consumer-driven-contract-test.md) | No Consumer-driven Contract Test, os desenvolvedores de cada serviço consumidor escrevem um conjunto de testes (contratos) que descreve o que esperam da API de um serviço provedor. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Consumer-side Contract Test](./testing/consumer-side-contract-test.md) | O Consumer-side Contract Test verifica que o cliente de um serviço consegue se comunicar com ele. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Component Test](./testing/service-component-test.md) | O Service Component Test é um conjunto de testes que exercita um único serviço em isolamento, tratando-o como uma caixa-preta acessada por sua API. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Cost Optimization`](/tags/cost-optimization) |

## Deployment (6) {#deployment}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Multiple Service Instances per Host](./deployment/multiple-service-instances-per-host.md) | Neste padrão, instâncias de serviços diferentes são executadas no mesmo host, que pode ser físico ou virtual. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per Host](./deployment/service-instance-per-host.md) | Cada instância de serviço é implantada em seu próprio host, que pode ser uma máquina física ou virtual. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per VM](./deployment/service-instance-per-vm.md) | O serviço é empacotado como uma imagem de máquina virtual e cada instância é implantada como uma VM separada. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per Container](./deployment/service-instance-per-container.md) | O serviço é empacotado como uma imagem de contêiner (por exemplo, Docker) e cada instância é executada como um contêiner. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |
| [Serverless Deployment](./deployment/serverless-deployment.md) | O serviço é implantado em uma infraestrutura que esconde qualquer conceito de servidor, seja físico, virtual ou contêiner. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service Deployment Platform](./deployment/service-deployment-platform.md) | O padrão propõe usar uma plataforma de implantação, isto é, uma infraestrutura automatizada para implantar aplicações. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) |

## Cross-cutting Concerns (3) {#cross-cutting-concerns}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Microservice Chassis](./cross-cutting-concerns/microservice-chassis.md) | O Microservice Chassis é um framework compartilhado que serve de fundação para todos os serviços de uma organização. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Security`](/tags/security) |
| [Externalized Configuration](../../cloud/cloud-design-patterns/deployment-and-topology/external-configuration-store.md) ★ | O padrão External Configuration Store move as informações de configuração para fora do pacote de implantação da aplicação, levando-as para um repositório centralizado. | [`Operational Excellence`](/tags/operational-excellence) |
| [Service Template](./cross-cutting-concerns/service-template.md) | O Service Template é um modelo de código-fonte que os desenvolvedores copiam para iniciar um novo serviço. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |

## Communication Styles (4) {#communication-styles}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Remote Procedure Invocation](./communication-styles/remote-procedure-invocation.md) | Remote Procedure Invocation (RPI) é o estilo de comunicação em que um cliente envia uma requisição a um serviço usando um protocolo síncrono de requisição/resposta, como se estivesse invocando um procedimento remoto. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Messaging](./communication-styles/messaging.md) | No padrão Messaging, os serviços se comunicam trocando mensagens por canais de mensagens, de forma assíncrona. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Domain-specific Protocol](./communication-styles/domain-specific-protocol.md) | O padrão Domain-specific Protocol propõe que a comunicação entre serviços, ou entre clientes e serviços, use um protocolo próprio do domínio do problema, em vez de um protocolo genérico de requisição/resposta ou de mensageria. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Idempotent Consumer](../../cloud/cloud-design-patterns/messaging/idempotent-consumer.md) ★ | O padrão Idempotent Consumer projeta consumidores de mensagens de forma que processar a mesma mensagem mais de uma vez produza exatamente o mesmo efeito que processá-la uma única vez. | [`Reliability`](/tags/reliability) |

## External API (2) {#external-api}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [API Gateway](./external-api/api-gateway.md) | O API Gateway é o ponto de entrada único entre os clientes e os microsserviços de uma aplicação. | [`Performance Efficiency`](/tags/performance-efficiency) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Backend for Front-end](../../cloud/cloud-design-patterns/gateways-and-edge/backends-for-frontends.md) ★ | O padrão Backends for Frontends (BFF) propõe criar um serviço de backend separado para cada interface de frontend (por exemplo, aplicação web, app mobile, dispositivos embarcados), em vez de usar um único backend de propósito geral para todas elas. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |

## Service Discovery (5) {#service-discovery}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Client-side Discovery](./service-discovery/client-side-discovery.md) | No Client-side Discovery, o cliente de um serviço (outro serviço ou um API gateway) é responsável por descobrir onde estão as instâncias disponíveis. | [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [Server-side Discovery](./service-discovery/server-side-discovery.md) | No Server-side Discovery, o cliente envia suas requisições a um roteador (também chamado de load balancer) em um endereço bem conhecido. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Registry](./service-discovery/service-registry.md) | O Service Registry é um banco de dados de serviços, suas instâncias e suas localizações. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Self Registration](./service-discovery/self-registration.md) | No Self Registration, cada instância de serviço é responsável por se registrar no Service Registry, informando seu host e endereço IP ao iniciar. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [3rd Party Registration](./service-discovery/3rd-party-registration.md) | No 3rd Party Registration, um componente separado, o registrador (registrar), cuida de registrar cada instância no Service Registry quando ela inicia e de removê-la quando desliga. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |

## Reliability (1) {#reliability}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Circuit Breaker](../../cloud/cloud-design-patterns/resiliency/circuit-breaker.md) ★ | O Circuit Breaker bloqueia temporariamente o acesso a um serviço ou recurso remoto quando as falhas passam de um limite. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Security (1) {#security}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Access Token](./security/access-token.md) | Access Token é o padrão em que a identidade de quem faz a requisição é transportada por um token seguro, em vez de cada serviço reautenticar o cliente. | [`Security`](/tags/security) [`Reliability`](/tags/reliability) |

## Observability (7) {#observability}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Log Aggregation](./observability/log-aggregation.md) | Em uma arquitetura de microsserviços, cada instância de serviço escreve seus próprios logs (erros, avisos, informações e depuração) em um formato padronizado. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Application Metrics](./observability/application-metrics.md) | Cada serviço é instrumentado para coletar estatísticas sobre suas operações individuais, como contagem de requisições, taxa de erros, latências e uso de recursos. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Audit Logging](./observability/audit-logging.md) | O padrão registra as ações dos usuários (quem fez o quê, quando e sobre qual recurso) em um armazenamento de dados próprio, como um banco de dados. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Distributed Tracing](./observability/distributed-tracing.md) | Em microsserviços, uma única requisição externa costuma percorrer vários serviços, cada um executando operações como consultas a banco de dados ou publicação de mensagens. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [Exception Tracking](./observability/exception-tracking.md) | Quando uma requisição falha, uma instância de serviço lança uma exceção com mensagem de erro e stack trace. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Health Check API](../../cloud/cloud-design-patterns/resiliency/health-endpoint-monitoring.md) ★ | A aplicação expõe endpoints de saúde (por exemplo, `/health` via HTTPS ou o protocolo padrão de health checking do gRPC) que ferramentas externas consultam em intervalos regulares. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Log Deployments and Changes](./observability/log-deployments-and-changes.md) | Problemas em produção costumam surgir logo depois de uma mudança. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |

## UI Design (2) {#ui-design}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Server-side Page Fragment Composition](./ui-design/server-side-page-fragment-composition.md) | Em uma arquitetura de microsserviços com equipes organizadas por capacidade de negócio ou subdomínio, cada equipe também é dona da experiência do usuário relacionada ao seu serviço. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Client-side UI Composition](./ui-design/client-side-ui-composition.md) | Em uma arquitetura de microsserviços com equipes organizadas por capacidade de negócio ou subdomínio, cada equipe também é responsável pela experiência do usuário do seu serviço. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |

## Por etiqueta

### Reliability (38)

[Microservice Architecture](./architectural-style/microservice-architecture.md), [Decompose by Business Capability](./service-boundaries/decompose-by-business-capability.md), [Decompose by Subdomain](./service-boundaries/decompose-by-subdomain.md), [Self-contained Service](./service-boundaries/self-contained-service.md), [Strangler Application](../../cloud/cloud-design-patterns/integration-and-modernization/strangler-fig.md), [Database per Service](./service-collaboration/database-per-service.md), [Shared Database](./service-collaboration/shared-database.md), [Saga](../../cloud/cloud-design-patterns/distributed-coordination/saga.md), [Command-side Replica](./service-collaboration/command-side-replica.md), [Domain Event](./service-collaboration/domain-event.md), [Event Sourcing](../../cloud/cloud-design-patterns/data-management/event-sourcing.md), [Transactional Outbox](./transactional-messaging/transactional-outbox.md), [Transaction Log Tailing](./transactional-messaging/transaction-log-tailing.md), [Polling Publisher](./transactional-messaging/polling-publisher.md), [Consumer-driven Contract Test](./testing/consumer-driven-contract-test.md), [Consumer-side Contract Test](./testing/consumer-side-contract-test.md), [Service Component Test](./testing/service-component-test.md), [Service Instance per Host](./deployment/service-instance-per-host.md), [Service Instance per VM](./deployment/service-instance-per-vm.md), [Service Deployment Platform](./deployment/service-deployment-platform.md), [Microservice Chassis](./cross-cutting-concerns/microservice-chassis.md), [Remote Procedure Invocation](./communication-styles/remote-procedure-invocation.md), [Messaging](./communication-styles/messaging.md), [Idempotent Consumer](../../cloud/cloud-design-patterns/messaging/idempotent-consumer.md), [Backend for Front-end](../../cloud/cloud-design-patterns/gateways-and-edge/backends-for-frontends.md), [Client-side Discovery](./service-discovery/client-side-discovery.md), [Server-side Discovery](./service-discovery/server-side-discovery.md), [Service Registry](./service-discovery/service-registry.md), [Self Registration](./service-discovery/self-registration.md), [3rd Party Registration](./service-discovery/3rd-party-registration.md), [Circuit Breaker](../../cloud/cloud-design-patterns/resiliency/circuit-breaker.md), [Access Token](./security/access-token.md), [Log Aggregation](./observability/log-aggregation.md), [Application Metrics](./observability/application-metrics.md), [Distributed Tracing](./observability/distributed-tracing.md), [Exception Tracking](./observability/exception-tracking.md), [Health Check API](../../cloud/cloud-design-patterns/resiliency/health-endpoint-monitoring.md), [Log Deployments and Changes](./observability/log-deployments-and-changes.md)

### Security (9)

[Microservice Architecture](./architectural-style/microservice-architecture.md), [Service Instance per Host](./deployment/service-instance-per-host.md), [Service Instance per VM](./deployment/service-instance-per-vm.md), [Microservice Chassis](./cross-cutting-concerns/microservice-chassis.md), [Service Template](./cross-cutting-concerns/service-template.md), [API Gateway](./external-api/api-gateway.md), [Backend for Front-end](../../cloud/cloud-design-patterns/gateways-and-edge/backends-for-frontends.md), [Access Token](./security/access-token.md), [Audit Logging](./observability/audit-logging.md)

### Cost Optimization (7)

[Monolithic Architecture](./architectural-style/monolithic-architecture.md), [Strangler Application](../../cloud/cloud-design-patterns/integration-and-modernization/strangler-fig.md), [Service Component Test](./testing/service-component-test.md), [Multiple Service Instances per Host](./deployment/multiple-service-instances-per-host.md), [Service Instance per Container](./deployment/service-instance-per-container.md), [Serverless Deployment](./deployment/serverless-deployment.md), [Service Deployment Platform](./deployment/service-deployment-platform.md)

### Operational Excellence (41)

[Monolithic Architecture](./architectural-style/monolithic-architecture.md), [Microservice Architecture](./architectural-style/microservice-architecture.md), [Decompose by Business Capability](./service-boundaries/decompose-by-business-capability.md), [Decompose by Subdomain](./service-boundaries/decompose-by-subdomain.md), [Service per Team](./service-boundaries/service-per-team.md), [Strangler Application](../../cloud/cloud-design-patterns/integration-and-modernization/strangler-fig.md), [Anti-Corruption Layer](../../cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer.md), [Database per Service](./service-collaboration/database-per-service.md), [Shared Database](./service-collaboration/shared-database.md), [Domain Event](./service-collaboration/domain-event.md), [Transactional Outbox](./transactional-messaging/transactional-outbox.md), [Polling Publisher](./transactional-messaging/polling-publisher.md), [Consumer-driven Contract Test](./testing/consumer-driven-contract-test.md), [Consumer-side Contract Test](./testing/consumer-side-contract-test.md), [Service Component Test](./testing/service-component-test.md), [Multiple Service Instances per Host](./deployment/multiple-service-instances-per-host.md), [Service Instance per Host](./deployment/service-instance-per-host.md), [Service Instance per VM](./deployment/service-instance-per-vm.md), [Service Instance per Container](./deployment/service-instance-per-container.md), [Serverless Deployment](./deployment/serverless-deployment.md), [Service Deployment Platform](./deployment/service-deployment-platform.md), [Microservice Chassis](./cross-cutting-concerns/microservice-chassis.md), [Externalized Configuration](../../cloud/cloud-design-patterns/deployment-and-topology/external-configuration-store.md), [Service Template](./cross-cutting-concerns/service-template.md), [Remote Procedure Invocation](./communication-styles/remote-procedure-invocation.md), [Messaging](./communication-styles/messaging.md), [Domain-specific Protocol](./communication-styles/domain-specific-protocol.md), [API Gateway](./external-api/api-gateway.md), [Server-side Discovery](./service-discovery/server-side-discovery.md), [Service Registry](./service-discovery/service-registry.md), [Self Registration](./service-discovery/self-registration.md), [3rd Party Registration](./service-discovery/3rd-party-registration.md), [Log Aggregation](./observability/log-aggregation.md), [Application Metrics](./observability/application-metrics.md), [Audit Logging](./observability/audit-logging.md), [Distributed Tracing](./observability/distributed-tracing.md), [Exception Tracking](./observability/exception-tracking.md), [Health Check API](../../cloud/cloud-design-patterns/resiliency/health-endpoint-monitoring.md), [Log Deployments and Changes](./observability/log-deployments-and-changes.md), [Server-side Page Fragment Composition](./ui-design/server-side-page-fragment-composition.md), [Client-side UI Composition](./ui-design/client-side-ui-composition.md)

### Performance Efficiency (24)

[Monolithic Architecture](./architectural-style/monolithic-architecture.md), [Microservice Architecture](./architectural-style/microservice-architecture.md), [Self-contained Service](./service-boundaries/self-contained-service.md), [Service per Team](./service-boundaries/service-per-team.md), [Database per Service](./service-collaboration/database-per-service.md), [Command-side Replica](./service-collaboration/command-side-replica.md), [API Composition](./service-collaboration/api-composition.md), [CQRS](../../cloud/cloud-design-patterns/data-management/cqrs.md), [Event Sourcing](../../cloud/cloud-design-patterns/data-management/event-sourcing.md), [Transaction Log Tailing](./transactional-messaging/transaction-log-tailing.md), [Service Instance per Container](./deployment/service-instance-per-container.md), [Serverless Deployment](./deployment/serverless-deployment.md), [Remote Procedure Invocation](./communication-styles/remote-procedure-invocation.md), [Messaging](./communication-styles/messaging.md), [Domain-specific Protocol](./communication-styles/domain-specific-protocol.md), [API Gateway](./external-api/api-gateway.md), [Backend for Front-end](../../cloud/cloud-design-patterns/gateways-and-edge/backends-for-frontends.md), [Client-side Discovery](./service-discovery/client-side-discovery.md), [Circuit Breaker](../../cloud/cloud-design-patterns/resiliency/circuit-breaker.md), [Application Metrics](./observability/application-metrics.md), [Distributed Tracing](./observability/distributed-tracing.md), [Health Check API](../../cloud/cloud-design-patterns/resiliency/health-endpoint-monitoring.md), [Server-side Page Fragment Composition](./ui-design/server-side-page-fragment-composition.md), [Client-side UI Composition](./ui-design/client-side-ui-composition.md)
