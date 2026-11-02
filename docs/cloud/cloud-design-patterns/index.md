---
title: "Cloud Design Patterns"
sidebar_label: "Cloud Design Patterns"
---

# Cloud Design Patterns

Catálogo pessoal baseado no [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/), que mantém o catálogo publicado originalmente no livro *Cloud Design Patterns* (Microsoft patterns & practices, 2014). Os padrões são independentes de provedor; o Azure aparece só nas notas de implementação. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (pilares do Well-Architected Framework) e um diagrama Mermaid.

Total: 44 padrões em 8 grupos. Etiquetas: Pilares do Well-Architected Framework.

## Grupos

- [Messaging](#messaging) (10)
- [Data Management](#data-management) (6)
- [Resiliency](#resiliency) (6)
- [Distributed Coordination](#distributed-coordination) (5)
- [Deployment and Topology](#deployment-and-topology) (5)
- [Gateways and Edge](#gateways-and-edge) (4)
- [Security and Access](#security-and-access) (4)
- [Integration and Modernization](#integration-and-modernization) (4)

## Messaging (10) {#messaging}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Asynchronous Request-Reply](./messaging/asynchronous-request-reply.md) | O padrão Asynchronous Request-Reply desacopla o processamento no back-end do host de front-end quando o trabalho precisa ser executado de forma assíncrona, mas o cliente ainda precisa de uma resposta clara. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [Claim Check](./messaging/claim-check.md) | O padrão Claim Check separa o armazenamento do conteúdo (payload) da entrega da mensagem. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Competing Consumers](./messaging/competing-consumers.md) | O padrão Competing Consumers permite que várias instâncias consumidoras processem, de forma concorrente, mensagens recebidas pelo mesmo canal de mensageria. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Idempotent Consumer](./messaging/idempotent-consumer.md) | O padrão Idempotent Consumer projeta consumidores de mensagens de forma que processar a mesma mensagem mais de uma vez produza exatamente o mesmo efeito que processá-la uma única vez. | [`Reliability`](/tags/reliability) |
| [Messaging Bridge](./messaging/messaging-bridge.md) | O Messaging Bridge conecta sistemas que usam infraestruturas de mensageria diferentes (por exemplo, um broker legado on-premises e um serviço de filas na nuvem) e repassa mensagens entre elas. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |
| [Pipes and Filters](./messaging/pipes-and-filters.md) | O padrão Pipes and Filters decompõe uma tarefa de processamento complexa em uma sequência de etapas independentes e reutilizáveis. | [`Reliability`](/tags/reliability) |
| [Priority Queue](./messaging/priority-queue.md) | O padrão Priority Queue prioriza as requisições enviadas a um serviço para que as de maior prioridade sejam recebidas e processadas antes das de menor prioridade. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Publisher-Subscriber](./messaging/publisher-subscriber.md) | O padrão Publisher-Subscriber (pub/sub) permite que uma aplicação anuncie eventos de forma assíncrona a vários consumidores interessados, sem conhecer quem são eles. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Queue-Based Load Leveling](./messaging/queue-based-load-leveling.md) | O padrão Queue-Based Load Leveling coloca uma fila entre as tarefas que geram trabalho (produtores) e o serviço que executa esse trabalho (consumidor). | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Sequential Convoy](./messaging/sequential-convoy.md) | O Sequential Convoy agrupa mensagens relacionadas por uma chave de categoria (por exemplo, o ID de um pedido) e processa cada grupo de forma sequencial, uma mensagem por vez, enquanto grupos diferentes são processados em paralelo. | [`Reliability`](/tags/reliability) |

## Data Management (6) {#data-management}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Cache-Aside](./data-management/cache-aside.md) | O Cache-Aside carrega dados no cache sob demanda a partir do armazenamento de dados de origem. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [CQRS](./data-management/cqrs.md) | O CQRS (Command Query Responsibility Segregation) separa as operações que alteram dados (*commands*) das operações que leem dados (*queries*), usando modelos distintos para cada lado. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [Event Sourcing](./data-management/event-sourcing.md) | Em vez de guardar apenas o estado atual dos dados e sobrescrevê-lo a cada alteração (modelo CRUD), o Event Sourcing registra toda a sequência de ações aplicadas a uma entidade como eventos imutáveis em um armazenamento somente de acréscimo (*append-only*), o **event store**. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Index Table](./data-management/index-table.md) | Muitos armazenamentos de dados organizam as entidades apenas pela chave primária (ou pela chave de partição/shard). | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Materialized View](./data-management/materialized-view.md) | O padrão Materialized View gera, com antecedência, visões pré-populadas sobre os dados de um ou mais armazenamentos quando esses dados não estão no formato ideal para as consultas necessárias. | [`Performance Efficiency`](/tags/performance-efficiency) |
| [Sharding](./data-management/sharding.md) | O padrão Sharding divide um armazenamento de dados em partições horizontais, chamadas *shards*. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) |

## Resiliency (6) {#resiliency}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Bulkhead](./resiliency/bulkhead.md) | O padrão Bulkhead isola os elementos de uma aplicação em pools independentes, de modo que, se um deles falhar, os demais continuem funcionando. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Circuit Breaker](./resiliency/circuit-breaker.md) | O Circuit Breaker bloqueia temporariamente o acesso a um serviço ou recurso remoto quando as falhas passam de um limite. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Health Endpoint Monitoring](./resiliency/health-endpoint-monitoring.md) | A aplicação expõe endpoints de saúde (por exemplo, `/health` via HTTPS ou o protocolo padrão de health checking do gRPC) que ferramentas externas consultam em intervalos regulares. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Rate Limiting](./resiliency/rate-limiting-pattern.md) | O padrão Rate Limiting faz com que uma aplicação **controle a taxa com que ela mesma envia requisições** a um serviço que impõe limites de uso. | [`Reliability`](/tags/reliability) |
| [Retry](./resiliency/retry.md) | O padrão Retry permite que uma aplicação lide com falhas transitórias ao se conectar a um serviço ou recurso remoto, repetindo de forma transparente uma operação que falhou. | [`Reliability`](/tags/reliability) |
| [Throttling](./resiliency/throttling.md) | O padrão Throttling limita os recursos que uma instância da aplicação, um tenant ou um serviço inteiro pode consumir. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |

## Distributed Coordination (5) {#distributed-coordination}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Choreography](./distributed-coordination/choreography.md) | O padrão Choreography distribui a lógica de um fluxo de negócio entre os próprios serviços que participam dele, em vez de concentrá-la em um orquestrador central. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Compensating Transaction](./distributed-coordination/compensating-transaction.md) | O padrão Compensating Transaction desfaz o trabalho já realizado quando uma ou mais etapas de uma operação com consistência eventual falham. | [`Reliability`](/tags/reliability) |
| [Leader Election](./distributed-coordination/leader-election.md) | O padrão Leader Election coordena as ações de um conjunto de instâncias colaborativas de uma aplicação distribuída elegendo uma delas como líder. | [`Reliability`](/tags/reliability) |
| [Saga](./distributed-coordination/saga.md) | O padrão Saga mantém a consistência de dados em sistemas distribuídos ao dividir uma operação de negócio que envolve vários serviços em uma sequência de **transações locais**. | [`Reliability`](/tags/reliability) |
| [Scheduler Agent Supervisor](./distributed-coordination/scheduler-agent-supervisor.md) | O padrão Scheduler Agent Supervisor coordena um conjunto de ações distribuídas como uma única operação lógica: ou a operação inteira é concluída com sucesso, ou o trabalho já feito é desfeito. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |

## Deployment and Topology (5) {#deployment-and-topology}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Compute Resource Consolidation](./deployment-and-topology/compute-resource-consolidation.md) | O padrão Compute Resource Consolidation agrupa várias tarefas ou operações em uma única unidade computacional (uma máquina virtual, um contêiner, um plano de hospedagem ou um pool de nós), em vez de manter cada uma em uma unidade dedicada. | [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Deployment Stamps](./deployment-and-topology/deployment-stamp.md) | O padrão Deployment Stamps consiste em implantar várias cópias independentes dos componentes de uma aplicação, incluindo os armazenamentos de dados, como um único grupo de recursos. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [External Configuration Store](./deployment-and-topology/external-configuration-store.md) | O padrão External Configuration Store move as informações de configuração para fora do pacote de implantação da aplicação, levando-as para um repositório centralizado. | [`Operational Excellence`](/tags/operational-excellence) |
| [Geode](./deployment-and-topology/geodes.md) | O padrão Geode (de **ge**ographical n**ode**) consiste em implantar o mesmo conjunto de serviços de backend em vários nós geográficos espalhados pelo mundo, em que cada nó consegue atender qualquer requisição de qualquer cliente, em qualquer região. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Static Content Hosting](./deployment-and-topology/static-content-hosting.md) | O padrão Static Content Hosting consiste em publicar o conteúdo estático de uma aplicação (páginas HTML, imagens, folhas de estilo, JavaScript do lado do cliente, documentos, pacotes de software) em um serviço de armazenamento em nuvem capaz de entregá-lo diretamente ao cliente via HTTP(S), sem passar pelos servidores de aplicação. | [`Cost Optimization`](/tags/cost-optimization) |

## Gateways and Edge (4) {#gateways-and-edge}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Backends for Frontends](./gateways-and-edge/backends-for-frontends.md) | O padrão Backends for Frontends (BFF) propõe criar um serviço de backend separado para cada interface de frontend (por exemplo, aplicação web, app mobile, dispositivos embarcados), em vez de usar um único backend de propósito geral para todas elas. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Gateway Aggregation](./gateways-and-edge/gateway-aggregation.md) | O padrão Gateway Aggregation usa um gateway para agregar várias requisições individuais em uma única requisição. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Gateway Offloading](./gateways-and-edge/gateway-offloading.md) | O padrão Gateway Offloading transfere para um gateway (proxy reverso) funcionalidades compartilhadas ou especializadas que, de outra forma, precisariam ser implementadas e mantidas em cada serviço de backend. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Gateway Routing](./gateways-and-edge/gateway-routing.md) | O padrão Gateway Routing coloca um gateway na frente de um conjunto de aplicações, serviços ou implantações e expõe tudo por um único endpoint. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |

## Security and Access (4) {#security-and-access}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Federated Identity](./security-and-access/federated-identity.md) | O padrão Federated Identity delega a autenticação de usuários (e de cargas de trabalho) a um provedor de identidade (IdP) externo e confiável, em vez de implementá-la no código da aplicação. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Gatekeeper](./security-and-access/gatekeeper.md) | O padrão Gatekeeper protege aplicações e serviços colocando um componente dedicado entre os clientes e o sistema. | [`Security`](/tags/security) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Quarantine](./security-and-access/quarantine.md) | O padrão Quarantine garante que artefatos de software de terceiros (imagens de contêiner, pacotes de bibliotecas, módulos de infraestrutura como código, imagens de sistema operacional, instaladores de fornecedores) só sejam consumidos pela carga de trabalho depois de verificados e marcados como confiáveis por um processo bem definido. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Valet Key](./security-and-access/valet-key.md) | O padrão Valet Key ("chave de manobrista") entrega ao cliente um token ou chave que dá acesso direto, mas restrito, a um recurso específico, como um arquivo num armazenamento de objetos ou uma fila. | [`Security`](/tags/security) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |

## Integration and Modernization (4) {#integration-and-modernization}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Ambassador](./integration-and-modernization/ambassador.md) | O padrão Ambassador cria serviços auxiliares que enviam requisições de rede em nome de uma aplicação ou serviço consumidor. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) |
| [Anti-Corruption Layer](./integration-and-modernization/anti-corruption-layer.md) | O Anti-Corruption Layer (camada anticorrupção) é uma fachada ou camada de adaptação colocada entre subsistemas que não compartilham a mesma semântica. | [`Operational Excellence`](/tags/operational-excellence) |
| [Sidecar](./integration-and-modernization/sidecar.md) | O padrão Sidecar implanta componentes auxiliares de uma aplicação em um processo ou contêiner separado, executado ao lado da aplicação principal. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Strangler Fig](./integration-and-modernization/strangler-fig.md) | O padrão Strangler Fig migra um sistema legado de forma incremental, substituindo funcionalidades específicas, uma a uma, por novas aplicações e serviços. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Operational Excellence`](/tags/operational-excellence) |

## Por etiqueta

### Reliability (30)

[Claim Check](./messaging/claim-check.md), [Competing Consumers](./messaging/competing-consumers.md), [Idempotent Consumer](./messaging/idempotent-consumer.md), [Pipes and Filters](./messaging/pipes-and-filters.md), [Priority Queue](./messaging/priority-queue.md), [Publisher-Subscriber](./messaging/publisher-subscriber.md), [Queue-Based Load Leveling](./messaging/queue-based-load-leveling.md), [Sequential Convoy](./messaging/sequential-convoy.md), [Cache-Aside](./data-management/cache-aside.md), [Event Sourcing](./data-management/event-sourcing.md), [Index Table](./data-management/index-table.md), [Sharding](./data-management/sharding.md), [Bulkhead](./resiliency/bulkhead.md), [Circuit Breaker](./resiliency/circuit-breaker.md), [Health Endpoint Monitoring](./resiliency/health-endpoint-monitoring.md), [Rate Limiting](./resiliency/rate-limiting-pattern.md), [Retry](./resiliency/retry.md), [Throttling](./resiliency/throttling.md), [Compensating Transaction](./distributed-coordination/compensating-transaction.md), [Leader Election](./distributed-coordination/leader-election.md), [Saga](./distributed-coordination/saga.md), [Scheduler Agent Supervisor](./distributed-coordination/scheduler-agent-supervisor.md), [Geode](./deployment-and-topology/geodes.md), [Backends for Frontends](./gateways-and-edge/backends-for-frontends.md), [Gateway Aggregation](./gateways-and-edge/gateway-aggregation.md), [Gateway Offloading](./gateways-and-edge/gateway-offloading.md), [Gateway Routing](./gateways-and-edge/gateway-routing.md), [Federated Identity](./security-and-access/federated-identity.md), [Ambassador](./integration-and-modernization/ambassador.md), [Strangler Fig](./integration-and-modernization/strangler-fig.md)

### Security (13)

[Claim Check](./messaging/claim-check.md), [Publisher-Subscriber](./messaging/publisher-subscriber.md), [Bulkhead](./resiliency/bulkhead.md), [Throttling](./resiliency/throttling.md), [Backends for Frontends](./gateways-and-edge/backends-for-frontends.md), [Gateway Aggregation](./gateways-and-edge/gateway-aggregation.md), [Gateway Offloading](./gateways-and-edge/gateway-offloading.md), [Federated Identity](./security-and-access/federated-identity.md), [Gatekeeper](./security-and-access/gatekeeper.md), [Quarantine](./security-and-access/quarantine.md), [Valet Key](./security-and-access/valet-key.md), [Ambassador](./integration-and-modernization/ambassador.md), [Sidecar](./integration-and-modernization/sidecar.md)

### Cost Optimization (12)

[Claim Check](./messaging/claim-check.md), [Competing Consumers](./messaging/competing-consumers.md), [Messaging Bridge](./messaging/messaging-bridge.md), [Publisher-Subscriber](./messaging/publisher-subscriber.md), [Queue-Based Load Leveling](./messaging/queue-based-load-leveling.md), [Sharding](./data-management/sharding.md), [Throttling](./resiliency/throttling.md), [Compute Resource Consolidation](./deployment-and-topology/compute-resource-consolidation.md), [Static Content Hosting](./deployment-and-topology/static-content-hosting.md), [Gateway Offloading](./gateways-and-edge/gateway-offloading.md), [Valet Key](./security-and-access/valet-key.md), [Strangler Fig](./integration-and-modernization/strangler-fig.md)

### Operational Excellence (14)

[Messaging Bridge](./messaging/messaging-bridge.md), [Publisher-Subscriber](./messaging/publisher-subscriber.md), [Health Endpoint Monitoring](./resiliency/health-endpoint-monitoring.md), [Choreography](./distributed-coordination/choreography.md), [Compute Resource Consolidation](./deployment-and-topology/compute-resource-consolidation.md), [Deployment Stamps](./deployment-and-topology/deployment-stamp.md), [External Configuration Store](./deployment-and-topology/external-configuration-store.md), [Gateway Aggregation](./gateways-and-edge/gateway-aggregation.md), [Gateway Offloading](./gateways-and-edge/gateway-offloading.md), [Gateway Routing](./gateways-and-edge/gateway-routing.md), [Quarantine](./security-and-access/quarantine.md), [Anti-Corruption Layer](./integration-and-modernization/anti-corruption-layer.md), [Sidecar](./integration-and-modernization/sidecar.md), [Strangler Fig](./integration-and-modernization/strangler-fig.md)

### Performance Efficiency (27)

[Asynchronous Request-Reply](./messaging/asynchronous-request-reply.md), [Claim Check](./messaging/claim-check.md), [Competing Consumers](./messaging/competing-consumers.md), [Priority Queue](./messaging/priority-queue.md), [Publisher-Subscriber](./messaging/publisher-subscriber.md), [Queue-Based Load Leveling](./messaging/queue-based-load-leveling.md), [Cache-Aside](./data-management/cache-aside.md), [CQRS](./data-management/cqrs.md), [Event Sourcing](./data-management/event-sourcing.md), [Index Table](./data-management/index-table.md), [Materialized View](./data-management/materialized-view.md), [Bulkhead](./resiliency/bulkhead.md), [Circuit Breaker](./resiliency/circuit-breaker.md), [Health Endpoint Monitoring](./resiliency/health-endpoint-monitoring.md), [Throttling](./resiliency/throttling.md), [Choreography](./distributed-coordination/choreography.md), [Scheduler Agent Supervisor](./distributed-coordination/scheduler-agent-supervisor.md), [Compute Resource Consolidation](./deployment-and-topology/compute-resource-consolidation.md), [Deployment Stamps](./deployment-and-topology/deployment-stamp.md), [Geode](./deployment-and-topology/geodes.md), [Backends for Frontends](./gateways-and-edge/backends-for-frontends.md), [Gateway Aggregation](./gateways-and-edge/gateway-aggregation.md), [Gateway Offloading](./gateways-and-edge/gateway-offloading.md), [Gateway Routing](./gateways-and-edge/gateway-routing.md), [Federated Identity](./security-and-access/federated-identity.md), [Gatekeeper](./security-and-access/gatekeeper.md), [Valet Key](./security-and-access/valet-key.md)
