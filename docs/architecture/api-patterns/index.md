---
title: "Patterns for API Design"
sidebar_label: "Patterns for API Design"
---

# Patterns for API Design

Catálogo pessoal baseado no livro [*Patterns for API Design: Simplifying Integration with Loosely Coupled Message Exchanges*](https://api-patterns.org/), de Olaf Zimmermann, Mirko Stocker, Daniel Lübke, Uwe Zdun e Cesare Pautasso (Addison-Wesley, 2022), que reúne padrões para projetar e evoluir APIs remotas: visibilidade e tipo de integração, papéis de endpoints e operações, estrutura das mensagens, qualidade, evolução e contratos. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (objetivos de design), um diagrama Mermaid e, quando ajuda, um exemplo.

Total: 44 padrões em 12 grupos. Etiquetas: Objetivo de design.

## Grupos

- [Foundations](#foundations) (5)
- [Basic Structure](#basic-structure) (4)
- [Endpoint Roles](#endpoint-roles) (7)
- [Operation Responsibilities](#operation-responsibilities) (4)
- [Element Stereotypes](#element-stereotypes) (4)
- [Special-Purpose Representations](#special-purpose-representations) (3)
- [Message Granularity](#message-granularity) (2)
- [Response Shaping](#response-shaping) (3)
- [Message Exchange Optimization](#message-exchange-optimization) (2)
- [Versioning](#versioning) (2)
- [Life-Cycle Management](#life-cycle-management) (4)
- [Documentation](#documentation) (4)

## Foundations (5) {#foundations}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Frontend Integration](/architecture/api-patterns/foundations/frontend-integration) | O padrão Frontend Integration expõe os serviços do backend de uma aplicação distribuída a um ou mais frontends por meio de uma API remota baseada em mensagens. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) |
| [Backend Integration](/architecture/api-patterns/foundations/backend-integration) | O padrão Backend Integration integra o backend de uma aplicação distribuída a outros backends, da mesma aplicação ou de outras, expondo seus serviços por meio de uma API remota baseada em mensagens. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |
| [Public API](/architecture/api-patterns/foundations/public-api) | O padrão Public API disponibiliza uma API na internet pública, acompanhada de uma descrição detalhada de suas propriedades funcionais e não funcionais, para um número ilimitado ou desconhecido de clientes fora da organização. | [`Security`](/tags/security) [`Evolvability`](/tags/evolvability) |
| [Community API](/architecture/api-patterns/foundations/community-api) | O padrão Community API restringe a visibilidade e o acesso de uma API a um grupo fechado de usuários que pertence a várias entidades jurídicas, como empresas, organizações sem fins lucrativos e governos. | [`Security`](/tags/security) [`Shared Understanding`](/tags/shared-understanding) |
| [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) | O padrão Solution-Internal API limita o acesso e o uso de uma API a uma única aplicação, decompondo-a logicamente em componentes que expõem APIs locais ou remotas apenas a seus parceiros internos de comunicação. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |

## Basic Structure (4) {#basic-structure}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) | O padrão Atomic Parameter define um único parâmetro ou elemento de corpo de mensagem, de um tipo básico do formato de troca escolhido (número, texto, booleano ou bloco binário), como a menor unidade de dados transmitida entre cliente e provedor de uma API. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) | O padrão Atomic Parameter List agrupa dois ou mais parâmetros atômicos relacionados em um único elemento coeso de representação, mantendo cada item simples e tornando explícita a ligação entre eles na descrição da API e nas mensagens trocadas. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) | O padrão Parameter Tree define uma estrutura hierárquica com um nó raiz e um ou mais nós filhos, cada um sendo um parâmetro atômico, uma lista de parâmetros atômicos ou outra árvore, para expressar relações de contenção em mensagens de API. | [`Shared Understanding`](/tags/shared-understanding) [`Performance`](/tags/performance) |
| [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest) | O padrão Parameter Forest reúne duas ou mais árvores de parâmetros no nível superior do cabeçalho ou do corpo de uma mensagem, localizadas por posição ou por nome. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |

## Endpoint Roles (7) {#endpoint-roles}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) | O padrão Processing Resource expõe um endpoint cuja função é executar uma ação de negócio, e não guardar dados, oferecendo uma ou mais operações que o cliente invoca para disparar processamento no provedor. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |
| [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) | O padrão Information Holder Resource expõe um endpoint que representa uma entidade de dados identificável e oferece operações para criá-la, lê-la e mantê-la, escondendo como ela é armazenada. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) | O padrão Operational Data Holder expõe um endpoint de dados de vida curta e alta taxa de mudança, que os clientes podem criar, ler, atualizar e apagar com frequência. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) | O padrão Master Data Holder expõe um endpoint de dados mestres, de vida longa e muito referenciados por outros dados, e oferece acesso cuidadoso, com regras claras de manutenção, para preservar sua qualidade e consistência. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) | O padrão Reference Data Holder expõe um endpoint de dados de referência, estáveis e de leitura, que servem de consulta compartilhada e mudam raramente. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) | O padrão Link Lookup Resource expõe um endpoint que resolve referências, devolvendo ao cliente os endereços atuais de outros recursos, em vez de os dados em si. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |
| [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) | O padrão Data Transfer Resource expõe um endpoint compartilhado que serve de área intermediária para trocar dados entre parceiros que não precisam estar disponíveis ao mesmo tempo nem se conhecer diretamente. | [`Decoupling`](/tags/decoupling) [`Performance`](/tags/performance) |

## Operation Responsibilities (4) {#operation-responsibilities}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) | O padrão State Creation Operation é uma operação de API de natureza somente escrita, com a qual o cliente informa ao provedor que algo aconteceu, sem esperar dele nada além de uma confirmação de recebimento. | [`Decoupling`](/tags/decoupling) [`Performance`](/tags/performance) |
| [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) | O padrão Retrieval Operation é uma operação de API somente leitura que devolve ao cliente uma representação legível por máquina de informações mantidas pelo provedor, com recursos de busca, filtro e formatação. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |
| [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) | O padrão State Transition Operation é uma operação de API que combina a entrada do cliente com o estado atual do provedor para provocar uma mudança de estado, lendo e escrevendo o armazenamento do lado do provedor. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) | O padrão Computation Function é uma operação de API sem estado e sem efeitos colaterais que recebe dados do cliente, calcula um resultado que depende exclusivamente dessa entrada e o devolve na resposta. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |

## Element Stereotypes (4) {#element-stereotypes}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Data Element](/architecture/api-patterns/element-stereotypes/data-element) | O padrão Data Element define um vocabulário dedicado de elementos de dados para as mensagens de requisição e resposta de uma API, que embrulha e mapeia as partes relevantes do modelo interno do provedor sem expor suas definições internas. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) |
| [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) | O padrão Metadata Element acrescenta às mensagens de uma API elementos que explicam e enriquecem os demais, para que o receptor interprete o conteúdo corretamente sem fixar no código suposições sobre o significado dos dados. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Id Element](/architecture/api-patterns/element-stereotypes/id-element) | O padrão Id Element introduz um tipo especial de Data Element, o identificador único, para distinguir endpoints, operações e elementos de mensagem que precisam ser diferenciados em tempo de projeto e de execução. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Link Element](/architecture/api-patterns/element-stereotypes/link-element) | O padrão Link Element inclui nas mensagens de requisição e resposta um ponteiro legível por pessoas e máquinas, acessível pela rede, para outros endpoints e operações, de modo que o cliente os chame remotamente. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |

## Special-Purpose Representations (3) {#special-purpose-representations}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [API Key](/architecture/api-patterns/special-purpose-representations/api-key) | O padrão API Key identifica o cliente de uma API por meio de um token único e difícil de adivinhar, emitido pelo provedor e enviado em cada requisição como um simples texto. | [`Security`](/tags/security) [`Simplicity`](/tags/simplicity) |
| [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) | O padrão Error Report informa ao cliente que uma requisição falhou por meio de uma representação na própria mensagem de resposta, com um código de erro legível por máquina e uma descrição textual para pessoas, independente do protocolo de transporte. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) | O padrão Context Representation agrupa as informações de contexto trocadas entre cliente e provedor (identidade, preferências, qualidade de serviço, correlação) em um elemento próprio e reconhecível dentro do corpo da mensagem, em vez de espalhá-las em cabeçalhos do protocolo de comunicação. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |

## Message Granularity (2) {#message-granularity}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) | O padrão Embedded Entity inclui, dentro da representação de um elemento de dados, os dados completos dos elementos relacionados a ele, para que o receptor obtenha tudo em uma única mensagem. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) | O padrão Linked Information Holder mantém as mensagens pequenas ao substituir os dados relacionados por links para endpoints que os expõem, deixando o cliente buscar cada parte somente quando precisar dela. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Response Shaping (3) {#response-shaping}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Pagination](/architecture/api-patterns/response-shaping/pagination) | O padrão Pagination divide um conjunto grande de dados em partes menores, as páginas, e entrega uma página por mensagem de resposta, com informações para o cliente pedir as seguintes. | [`Performance`](/tags/performance) [`Security`](/tags/security) |
| [Wish List](/architecture/api-patterns/response-shaping/wish-list) | O padrão Wish List permite que o cliente enumere, na própria requisição, os elementos de dados que deseja, e o provedor devolve apenas esses elementos na resposta. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Wish Template](/architecture/api-patterns/response-shaping/wish-template) | O padrão Wish Template permite que o cliente descreva, na requisição, uma estrutura que espelha a forma da resposta desejada, marcando quais elementos, inclusive aninhados, quer receber. | [`Performance`](/tags/performance) [`Evolvability`](/tags/evolvability) |

## Message Exchange Optimization (2) {#message-exchange-optimization}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request) | O padrão Conditional Request torna uma requisição condicional, acrescentando a ela metadados que descrevem a versão dos dados que o cliente já possui, de modo que o provedor só devolva a representação completa se ela tiver mudado. | [`Performance`](/tags/performance) |
| [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle) | O padrão Request Bundle agrupa várias requisições independentes em uma única mensagem de requisição, para reduzir o número de chamadas e de respostas trocadas entre cliente e provedor. | [`Performance`](/tags/performance) |

## Versioning (2) {#versioning}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Version Identifier](/architecture/api-patterns/versioning/version-identifier) | O padrão Version Identifier introduz um indicador explícito de versão na API e nas mensagens trocadas, para que provedor e clientes saibam qual contrato estão usando e rejeitem o que não entendem em vez de interpretá-lo errado. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |
| [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning) | O padrão Semantic Versioning estrutura o identificador de versão em três números (`MAJOR.MINOR.PATCH`) cujas partes indicam, por si só, se uma nova versão é compatível com a anterior. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |

## Life-Cycle Management (4) {#life-cycle-management}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Experimental Preview](/architecture/api-patterns/life-cycle-management/experimental-preview) | O padrão Experimental Preview disponibiliza uma API em regime de melhor esforço, sem compromisso com funcionalidade, estabilidade ou tempo de vida, e deixa essa falta de maturidade explícita para que os clientes ajustem suas expectativas. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |
| [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence) | O padrão Aggressive Obsolescence anuncia o mais cedo possível uma data de desativação para a API inteira ou para suas partes obsoletas, mantém essas partes disponíveis, porém desaconselhadas, durante um prazo curto e as remove assim que a data vence. | [`Evolvability`](/tags/evolvability) [`Simplicity`](/tags/simplicity) |
| [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee) | O padrão Limited Lifetime Guarantee garante que a API publicada não será quebrada durante um período fixo, e rotula cada versão com uma data de expiração conhecida desde o lançamento. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |
| [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) | O padrão Two in Production mantém duas versões de um endpoint e suas operações em produção ao mesmo tempo, sem exigir compatibilidade entre elas, e as atualiza e desativa em uma janela deslizante e sobreposta. | [`Evolvability`](/tags/evolvability) [`Decoupling`](/tags/decoupling) |

## Documentation (4) {#documentation}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [API Description](/architecture/api-patterns/documentation/api-description) | O padrão API Description define, de forma legível por pessoas e por máquinas, o contrato técnico e semântico de uma API: endpoints, operações, estrutura e significado das mensagens, erros e demais conhecimento que provedor e clientes precisam compartilhar para interagir com sucesso. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan) | O padrão Pricing Plan associa à descrição da API uma política de preços, que define como o consumo é medido e cobrado de clientes, anunciantes ou outras partes, de modo que o provedor financie a API e o cliente saiba quanto vai pagar. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) |
| [Rate Limit](/architecture/api-patterns/documentation/rate-limit) | O padrão Rate Limit protege uma API contra o uso excessivo ao definir e comunicar um número máximo de requisições que cada cliente pode fazer em uma janela de tempo, rejeitando, adiando ou degradando as que passarem do limite. | [`Performance`](/tags/performance) [`Security`](/tags/security) |
| [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) | O padrão Service Level Agreement (SLA) define, em termos mensuráveis, as características de qualidade de serviço que o provedor de uma API garante e as consequências de não cumpri-las. | [`Shared Understanding`](/tags/shared-understanding) [`Performance`](/tags/performance) |

## Por etiqueta

### Decoupling (16)

[Frontend Integration](/architecture/api-patterns/foundations/frontend-integration), [Backend Integration](/architecture/api-patterns/foundations/backend-integration), [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api), [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource), [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource), [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource), [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource), [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation), [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation), [Data Element](/architecture/api-patterns/element-stereotypes/data-element), [Id Element](/architecture/api-patterns/element-stereotypes/id-element), [Link Element](/architecture/api-patterns/element-stereotypes/link-element), [Error Report](/architecture/api-patterns/special-purpose-representations/error-report), [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation), [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder), [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production)

### Shared Understanding (20)

[Frontend Integration](/architecture/api-patterns/foundations/frontend-integration), [Community API](/architecture/api-patterns/foundations/community-api), [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter), [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list), [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree), [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest), [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource), [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder), [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation), [Data Element](/architecture/api-patterns/element-stereotypes/data-element), [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element), [Id Element](/architecture/api-patterns/element-stereotypes/id-element), [Error Report](/architecture/api-patterns/special-purpose-representations/error-report), [Version Identifier](/architecture/api-patterns/versioning/version-identifier), [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning), [Experimental Preview](/architecture/api-patterns/life-cycle-management/experimental-preview), [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee), [API Description](/architecture/api-patterns/documentation/api-description), [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan), [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement)

### Evolvability (17)

[Backend Integration](/architecture/api-patterns/foundations/backend-integration), [Public API](/architecture/api-patterns/foundations/public-api), [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource), [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder), [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource), [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation), [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element), [Link Element](/architecture/api-patterns/element-stereotypes/link-element), [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation), [Wish Template](/architecture/api-patterns/response-shaping/wish-template), [Version Identifier](/architecture/api-patterns/versioning/version-identifier), [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning), [Experimental Preview](/architecture/api-patterns/life-cycle-management/experimental-preview), [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence), [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee), [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production), [API Description](/architecture/api-patterns/documentation/api-description)

### Security (5)

[Public API](/architecture/api-patterns/foundations/public-api), [Community API](/architecture/api-patterns/foundations/community-api), [API Key](/architecture/api-patterns/special-purpose-representations/api-key), [Pagination](/architecture/api-patterns/response-shaping/pagination), [Rate Limit](/architecture/api-patterns/documentation/rate-limit)

### Simplicity (12)

[Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api), [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter), [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list), [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest), [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder), [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder), [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function), [API Key](/architecture/api-patterns/special-purpose-representations/api-key), [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity), [Wish List](/architecture/api-patterns/response-shaping/wish-list), [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence), [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan)

### Performance (16)

[Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree), [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder), [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder), [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource), [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation), [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation), [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function), [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity), [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder), [Pagination](/architecture/api-patterns/response-shaping/pagination), [Wish List](/architecture/api-patterns/response-shaping/wish-list), [Wish Template](/architecture/api-patterns/response-shaping/wish-template), [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request), [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle), [Rate Limit](/architecture/api-patterns/documentation/rate-limit), [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement)
