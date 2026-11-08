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
| [Monolithic Architecture](/architecture/microservices/architectural-style/monolithic-architecture) | Monolithic Architecture estrutura a aplicação como um único componente implantável, apoiado por um único banco de dados. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |
| [Microservice Architecture](/architecture/microservices/architectural-style/microservice-architecture) | Microservice Architecture estrutura a aplicação como dois ou mais serviços implantáveis de forma independente e fracamente acoplados. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Security`](/tags/security) |

## Service Boundaries (4) {#service-boundaries}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Decompose by Business Capability](/architecture/microservices/service-boundaries/decompose-by-business-capability) | Decompose by Business Capability define os serviços a partir das capacidades de negócio, isto é, das coisas que a organização faz para gerar valor, como gestão de pedidos, catálogo, estoque ou entrega. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Decompose by Subdomain](/architecture/microservices/service-boundaries/decompose-by-subdomain) | Decompose by Subdomain define os serviços a partir dos subdomínios do Domain-Driven Design (DDD), que representam as áreas distintas do negócio. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Self-contained Service](/architecture/microservices/service-boundaries/self-contained-service) | Self-contained Service projeta um serviço para responder a uma requisição síncrona sem precisar esperar por nenhum outro serviço. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service per Team](/architecture/microservices/service-boundaries/service-per-team) | Service per Team estabelece que cada serviço pertence a exatamente uma equipe, que tem a responsabilidade exclusiva de alterá-lo. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |

## Refactoring to Services (2) {#refactoring-to-services}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Strangler Application](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig) ★ | O padrão Strangler Fig migra um sistema legado de forma incremental, substituindo funcionalidades específicas, uma a uma, por novas aplicações e serviços. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Anti-Corruption Layer](/architecture/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) ★ | O Anti-Corruption Layer (camada anticorrupção) é uma fachada ou camada de adaptação colocada entre subsistemas que não compartilham a mesma semântica. | [`Operational Excellence`](/tags/operational-excellence) |

## Service Collaboration (8) {#service-collaboration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Database per Service](/architecture/microservices/service-collaboration/database-per-service) | No padrão Database per Service, os dados persistentes de cada serviço são privados a ele e só podem ser acessados por meio da sua API. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Shared Database](/architecture/microservices/service-collaboration/shared-database) | No padrão Shared Database, todos os serviços utilizam um único banco de dados. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Saga](/architecture/cloud-design-patterns/distributed-coordination/saga) ★ | O padrão Saga mantém a consistência de dados em sistemas distribuídos ao dividir uma operação de negócio que envolve vários serviços em uma sequência de **transações locais**. | [`Reliability`](/tags/reliability) |
| [Command-side Replica](/architecture/microservices/service-collaboration/command-side-replica) | Em uma arquitetura com Database per Service, um serviço que executa um comando muitas vezes precisa de dados que pertencem a outro serviço. | [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [API Composition](/architecture/microservices/service-collaboration/api-composition) | Em uma aplicação com microsserviços e Database per Service, os dados estão espalhados em bancos privados, e consultas que combinam informações de vários serviços deixam de ser um simples *join*. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [CQRS](/architecture/cloud-design-patterns/data-management/cqrs) ★ | O CQRS (Command Query Responsibility Segregation) separa as operações que alteram dados (*commands*) das operações que leem dados (*queries*), usando modelos distintos para cada lado. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [Domain Event](/architecture/microservices/service-collaboration/domain-event) | Um evento de domínio (*Domain Event*), conceito vindo do Domain-Driven Design, é um fato relevante para o negócio que ocorreu no domínio, como `PedidoCriado` ou `CreditoReservado`. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Event Sourcing](/architecture/cloud-design-patterns/data-management/event-sourcing) ★ | Em vez de guardar apenas o estado atual dos dados e sobrescrevê-lo a cada alteração (modelo CRUD), o Event Sourcing registra toda a sequência de ações aplicadas a uma entidade como eventos imutáveis em um armazenamento somente de acréscimo (*append-only*), o **event store**. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Transactional Messaging (3) {#transactional-messaging}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Transactional Outbox](/architecture/microservices/transactional-messaging/transactional-outbox) | O Transactional Outbox resolve o problema de atualizar o banco de dados de um serviço e, ao mesmo tempo, enviar uma mensagem ou evento a um message broker de forma atômica. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Transaction Log Tailing](/architecture/microservices/transactional-messaging/transaction-log-tailing) | O Transaction Log Tailing é uma forma de implementar o message relay do Transactional Outbox. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Polling Publisher](/architecture/microservices/transactional-messaging/polling-publisher) | O Polling Publisher é uma forma de implementar o message relay do Transactional Outbox. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |

## Testing (3) {#testing}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Consumer-driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test) | No Consumer-driven Contract Test, os desenvolvedores de cada serviço consumidor escrevem um conjunto de testes (contratos) que descreve o que esperam da API de um serviço provedor. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Consumer-side Contract Test](/architecture/microservices/testing/consumer-side-contract-test) | O Consumer-side Contract Test verifica que o cliente de um serviço consegue se comunicar com ele. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Component Test](/architecture/microservices/testing/service-component-test) | O Service Component Test é um conjunto de testes que exercita um único serviço em isolamento, tratando-o como uma caixa-preta acessada por sua API. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Cost Optimization`](/tags/cost-optimization) |

## Deployment (6) {#deployment}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Multiple Service Instances per Host](/architecture/microservices/deployment/multiple-service-instances-per-host) | Neste padrão, instâncias de serviços diferentes são executadas no mesmo host, que pode ser físico ou virtual. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per Host](/architecture/microservices/deployment/service-instance-per-host) | Cada instância de serviço é implantada em seu próprio host, que pode ser uma máquina física ou virtual. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per VM](/architecture/microservices/deployment/service-instance-per-vm) | O serviço é empacotado como uma imagem de máquina virtual e cada instância é implantada como uma VM separada. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Instance per Container](/architecture/microservices/deployment/service-instance-per-container) | O serviço é empacotado como uma imagem de contêiner (por exemplo, Docker) e cada instância é executada como um contêiner. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |
| [Serverless Deployment](/architecture/microservices/deployment/serverless-deployment) | O serviço é implantado em uma infraestrutura que esconde qualquer conceito de servidor, seja físico, virtual ou contêiner. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) | O padrão propõe usar uma plataforma de implantação, isto é, uma infraestrutura automatizada para implantar aplicações. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) |

## Cross-cutting Concerns (3) {#cross-cutting-concerns}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Microservice Chassis](/architecture/microservices/cross-cutting-concerns/microservice-chassis) | O Microservice Chassis é um framework compartilhado que serve de fundação para todos os serviços de uma organização. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Security`](/tags/security) |
| [Externalized Configuration](/architecture/cloud-design-patterns/deployment-and-topology/external-configuration-store) ★ | O padrão External Configuration Store move as informações de configuração para fora do pacote de implantação da aplicação, levando-as para um repositório centralizado. | [`Operational Excellence`](/tags/operational-excellence) |
| [Service Template](/architecture/microservices/cross-cutting-concerns/service-template) | O Service Template é um modelo de código-fonte que os desenvolvedores copiam para iniciar um novo serviço. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |

## Communication Styles (4) {#communication-styles}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Remote Procedure Invocation](/architecture/microservices/communication-styles/remote-procedure-invocation) | Remote Procedure Invocation (RPI) é o estilo de comunicação em que um cliente envia uma requisição a um serviço usando um protocolo síncrono de requisição/resposta, como se estivesse invocando um procedimento remoto. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Messaging](/architecture/microservices/communication-styles/messaging) | No padrão Messaging, os serviços se comunicam trocando mensagens por canais de mensagens, de forma assíncrona. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Domain-specific Protocol](/architecture/microservices/communication-styles/domain-specific-protocol) | O padrão Domain-specific Protocol propõe que a comunicação entre serviços, ou entre clientes e serviços, use um protocolo próprio do domínio do problema, em vez de um protocolo genérico de requisição/resposta ou de mensageria. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer) ★ | O padrão Idempotent Consumer projeta consumidores de mensagens de forma que processar a mesma mensagem mais de uma vez produza exatamente o mesmo efeito que processá-la uma única vez. | [`Reliability`](/tags/reliability) |

## External API (2) {#external-api}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [API Gateway](/architecture/microservices/external-api/api-gateway) | O API Gateway é o ponto de entrada único entre os clientes e os microsserviços de uma aplicação. | [`Performance Efficiency`](/tags/performance-efficiency) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Backend for Front-end](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) ★ | O padrão Backends for Frontends (BFF) propõe criar um serviço de backend separado para cada interface de frontend (por exemplo, aplicação web, app mobile, dispositivos embarcados), em vez de usar um único backend de propósito geral para todas elas. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |

## Service Discovery (5) {#service-discovery}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Client-side Discovery](/architecture/microservices/service-discovery/client-side-discovery) | No Client-side Discovery, o cliente de um serviço (outro serviço ou um API gateway) é responsável por descobrir onde estão as instâncias disponíveis. | [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [Server-side Discovery](/architecture/microservices/service-discovery/server-side-discovery) | No Server-side Discovery, o cliente envia suas requisições a um roteador (também chamado de load balancer) em um endereço bem conhecido. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Service Registry](/architecture/microservices/service-discovery/service-registry) | O Service Registry é um banco de dados de serviços, suas instâncias e suas localizações. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Self Registration](/architecture/microservices/service-discovery/self-registration) | No Self Registration, cada instância de serviço é responsável por se registrar no Service Registry, informando seu host e endereço IP ao iniciar. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [3rd Party Registration](/architecture/microservices/service-discovery/3rd-party-registration) | No 3rd Party Registration, um componente separado, o registrador (registrar), cuida de registrar cada instância no Service Registry quando ela inicia e de removê-la quando desliga. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |

## Reliability (1) {#reliability}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Circuit Breaker](/architecture/cloud-design-patterns/resiliency/circuit-breaker) ★ | O Circuit Breaker bloqueia temporariamente o acesso a um serviço ou recurso remoto quando as falhas passam de um limite. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Security (1) {#security}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Access Token](/architecture/microservices/security/access-token) | Access Token é o padrão em que a identidade de quem faz a requisição é transportada por um token seguro, em vez de cada serviço reautenticar o cliente. | [`Security`](/tags/security) [`Reliability`](/tags/reliability) |

## Observability (7) {#observability}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Log Aggregation](/architecture/microservices/observability/log-aggregation) | Em uma arquitetura de microsserviços, cada instância de serviço escreve seus próprios logs (erros, avisos, informações e depuração) em um formato padronizado. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Application Metrics](/architecture/microservices/observability/application-metrics) | Cada serviço é instrumentado para coletar estatísticas sobre suas operações individuais, como contagem de requisições, taxa de erros, latências e uso de recursos. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Audit Logging](/architecture/microservices/observability/audit-logging) | O padrão registra as ações dos usuários (quem fez o quê, quando e sobre qual recurso) em um armazenamento de dados próprio, como um banco de dados. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Distributed Tracing](/architecture/microservices/observability/distributed-tracing) | Em microsserviços, uma única requisição externa costuma percorrer vários serviços, cada um executando operações como consultas a banco de dados ou publicação de mensagens. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) [`Reliability`](/tags/reliability) |
| [Exception Tracking](/architecture/microservices/observability/exception-tracking) | Quando uma requisição falha, uma instância de serviço lança uma exceção com mensagem de erro e stack trace. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring) ★ | A aplicação expõe endpoints de saúde (por exemplo, `/health` via HTTPS ou o protocolo padrão de health checking do gRPC) que ferramentas externas consultam em intervalos regulares. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Log Deployments and Changes](/architecture/microservices/observability/log-deployments-and-changes) | Problemas em produção costumam surgir logo depois de uma mudança. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |

## UI Design (2) {#ui-design}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Server-side Page Fragment Composition](/architecture/microservices/ui-design/server-side-page-fragment-composition) | Em uma arquitetura de microsserviços com equipes organizadas por capacidade de negócio ou subdomínio, cada equipe também é dona da experiência do usuário relacionada ao seu serviço. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |
| [Client-side UI Composition](/architecture/microservices/ui-design/client-side-ui-composition) | Em uma arquitetura de microsserviços com equipes organizadas por capacidade de negócio ou subdomínio, cada equipe também é responsável pela experiência do usuário do seu serviço. | [`Performance Efficiency`](/tags/performance-efficiency) [`Operational Excellence`](/tags/operational-excellence) |

## Por etiqueta

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
