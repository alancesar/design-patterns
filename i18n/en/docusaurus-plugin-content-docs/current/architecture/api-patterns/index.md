---
title: "Patterns for API Design"
sidebar_label: "Patterns for API Design"
---

# Patterns for API Design

Personal catalog based on the book [*Patterns for API Design: Simplifying Integration with Loosely Coupled Message Exchanges*](https://api-patterns.org/), by Olaf Zimmermann, Mirko Stocker, Daniel Lübke, Uwe Zdun and Cesare Pautasso (Addison-Wesley, 2022), which collects patterns for designing and evolving remote APIs: visibility and integration type, endpoint and operation roles, message structure, quality, evolution and contracts. Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (design goals), a Mermaid diagram and, where it helps, an example.

Total: 44 patterns in 12 groups. Tags: Design goal.

## Groups

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

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Frontend Integration](/architecture/api-patterns/foundations/frontend-integration) | The Frontend Integration pattern exposes the services of a distributed application's backend to one or more frontends through a message-based remote API. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) |
| [Backend Integration](/architecture/api-patterns/foundations/backend-integration) | The Backend Integration pattern integrates the backend of a distributed application with other backends, of the same or other applications, by exposing its services through a message-based remote API. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |
| [Public API](/architecture/api-patterns/foundations/public-api) | The Public API pattern makes an API available on the public internet, together with a detailed description of its functional and non-functional properties, for an unlimited or unknown number of clients outside the organization. | [`Security`](/tags/security) [`Evolvability`](/tags/evolvability) |
| [Community API](/architecture/api-patterns/foundations/community-api) | The Community API pattern restricts the visibility of and access to an API to a closed group of users who belong to several legal entities, such as companies, non-profit organizations and governments. | [`Security`](/tags/security) [`Shared Understanding`](/tags/shared-understanding) |
| [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) | The Solution-Internal API pattern limits access to and use of an API to a single application, logically decomposing it into components that expose local or remote APIs only to their internal communication partners. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |

## Basic Structure (4) {#basic-structure}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) | The Atomic Parameter pattern defines a single parameter or message body element, of a basic type of the chosen exchange format (number, text, boolean or binary block), as the smallest unit of data transmitted between an API client and provider. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) | The Atomic Parameter List pattern groups two or more related atomic parameters into a single cohesive representation element, keeping each item simple while making the link between them explicit in the API description and in the exchanged messages. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) | The Parameter Tree pattern defines a hierarchical structure with a root node and one or more child nodes, each being an atomic parameter, a list of atomic parameters or another tree, to express containment relationships in API messages. | [`Shared Understanding`](/tags/shared-understanding) [`Performance`](/tags/performance) |
| [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest) | The Parameter Forest pattern gathers two or more parameter trees at the top level of a message header or body, located by position or by name. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |

## Endpoint Roles (7) {#endpoint-roles}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) | The Processing Resource pattern exposes an endpoint whose job is to carry out a business action rather than to hold data, offering one or more operations that the client invokes to trigger processing on the provider. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |
| [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) | The Information Holder Resource pattern exposes an endpoint that represents an identifiable data entity and offers operations to create, read and maintain it, hiding how it is stored. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) | The Operational Data Holder pattern exposes an endpoint for short-lived, fast-changing data that clients can create, read, update and delete frequently. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) | The Master Data Holder pattern exposes an endpoint for master data, which is long-lived and widely referenced by other data, and offers careful access with clear maintenance rules to preserve its quality and consistency. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) | The Reference Data Holder pattern exposes an endpoint for reference data, stable and read-oriented, that serves as shared lookup and rarely changes. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) | The Link Lookup Resource pattern exposes an endpoint that resolves references, returning to the client the current addresses of other resources instead of the data itself. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |
| [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) | The Data Transfer Resource pattern exposes a shared endpoint that serves as an intermediate area for exchanging data between partners that do not need to be available at the same time or to know each other directly. | [`Decoupling`](/tags/decoupling) [`Performance`](/tags/performance) |

## Operation Responsibilities (4) {#operation-responsibilities}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) | The State Creation Operation pattern is a write-only API operation with which the client tells the provider that something has happened, expecting nothing back except an acknowledgment. | [`Decoupling`](/tags/decoupling) [`Performance`](/tags/performance) |
| [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) | The Retrieval Operation pattern is a read-only API operation that returns to the client a machine-readable representation of information held by the provider, with search, filter and formatting capabilities. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |
| [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) | The State Transition Operation pattern is an API operation that combines the client's input with the provider's current state to cause a state change, reading and writing provider-side storage. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) | The Computation Function pattern is a stateless, side-effect-free API operation that receives data from the client, computes a result that depends exclusively on that input and returns it in the response. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |

## Element Stereotypes (4) {#element-stereotypes}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Data Element](/architecture/api-patterns/element-stereotypes/data-element) | The Data Element pattern defines a dedicated vocabulary of data elements for an API's request and response messages, wrapping and mapping the relevant parts of the provider's internal model without exposing its internal definitions. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) |
| [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) | The Metadata Element pattern adds to an API's messages elements that explain and enrich the other ones, so the receiver interprets the content correctly without hardcoding assumptions about the meaning of the data. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Id Element](/architecture/api-patterns/element-stereotypes/id-element) | The Id Element pattern introduces a special kind of Data Element, the unique identifier, to tell apart endpoints, operations and message elements that must be distinguished at design time and at runtime. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Link Element](/architecture/api-patterns/element-stereotypes/link-element) | The Link Element pattern includes in request and response messages a human- and machine-readable, network-accessible pointer to other endpoints and operations, so the client can call them remotely. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |

## Special-Purpose Representations (3) {#special-purpose-representations}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [API Key](/architecture/api-patterns/special-purpose-representations/api-key) | The API Key pattern identifies an API client through a unique, hard-to-guess token issued by the provider and sent with every request as a plain string. | [`Security`](/tags/security) [`Simplicity`](/tags/simplicity) |
| [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) | The Error Report pattern tells a client that a request failed through a representation inside the response message itself, with a machine-readable error code and a textual description for people, independent of the transport protocol. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) | The Context Representation pattern groups the context information exchanged between client and provider (identity, preferences, quality of service, correlation) into a dedicated, recognizable element inside the message body, instead of scattering it across the headers of the communication protocol. | [`Decoupling`](/tags/decoupling) [`Evolvability`](/tags/evolvability) |

## Message Granularity (2) {#message-granularity}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) | The Embedded Entity pattern includes, inside the representation of a data element, the full data of the elements related to it, so that the receiver gets everything in a single message. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) | The Linked Information Holder pattern keeps messages small by replacing related data with links to endpoints that expose it, letting the client fetch each part only when it needs it. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Response Shaping (3) {#response-shaping}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Pagination](/architecture/api-patterns/response-shaping/pagination) | The Pagination pattern splits a large data set into smaller parts, the pages, and delivers one page per response message, with information the client uses to request the next ones. | [`Performance`](/tags/performance) [`Security`](/tags/security) |
| [Wish List](/architecture/api-patterns/response-shaping/wish-list) | The Wish List pattern lets the client enumerate, in the request itself, the data elements it wants, and the provider returns only those elements in the response. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |
| [Wish Template](/architecture/api-patterns/response-shaping/wish-template) | The Wish Template pattern lets the client describe, in the request, a structure that mirrors the shape of the desired response, marking which elements, including nested ones, it wants. | [`Performance`](/tags/performance) [`Evolvability`](/tags/evolvability) |

## Message Exchange Optimization (2) {#message-exchange-optimization}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request) | The Conditional Request pattern makes a request conditional by adding metadata that describes the version of the data the client already holds, so the provider returns the full representation only if it has changed. | [`Performance`](/tags/performance) |
| [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle) | The Request Bundle pattern groups several independent requests into a single request message, to reduce the number of calls and responses exchanged between client and provider. | [`Performance`](/tags/performance) |

## Versioning (2) {#versioning}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Version Identifier](/architecture/api-patterns/versioning/version-identifier) | The Version Identifier pattern introduces an explicit version indicator in the API and in the messages exchanged, so that provider and clients know which contract they are using and reject what they do not understand instead of misreading it. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |
| [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning) | The Semantic Versioning pattern structures the version identifier in three numbers (`MAJOR.MINOR.PATCH`) whose parts indicate, on their own, whether a new version is compatible with the previous one. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |

## Life-Cycle Management (4) {#life-cycle-management}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Experimental Preview](/architecture/api-patterns/life-cycle-management/experimental-preview) | The Experimental Preview pattern makes an API available on a best-effort basis, with no commitment to functionality, stability or lifetime, and states this lack of maturity explicitly so that clients adjust their expectations. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |
| [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence) | The Aggressive Obsolescence pattern announces, as early as possible, a decommissioning date for the whole API or its obsolete parts, keeps those parts available but discouraged for a short period and removes them as soon as the date passes. | [`Evolvability`](/tags/evolvability) [`Simplicity`](/tags/simplicity) |
| [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee) | The Limited Lifetime Guarantee pattern guarantees that the published API will not be broken for a fixed period, and labels each version with an expiration date known from the moment of release. | [`Evolvability`](/tags/evolvability) [`Shared Understanding`](/tags/shared-understanding) |
| [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) | The Two in Production pattern keeps two versions of an endpoint and its operations in production at the same time, without requiring compatibility between them, and updates and decommissions them in a sliding, overlapping window. | [`Evolvability`](/tags/evolvability) [`Decoupling`](/tags/decoupling) |

## Documentation (4) {#documentation}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [API Description](/architecture/api-patterns/documentation/api-description) | The API Description pattern defines, in a human- and machine-readable form, the technical and semantic contract of an API: endpoints, operations, structure and meaning of messages, errors and any other knowledge that provider and clients must share to interact successfully. | [`Shared Understanding`](/tags/shared-understanding) [`Evolvability`](/tags/evolvability) |
| [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan) | The Pricing Plan pattern attaches to the API description a pricing policy that defines how consumption is metered and charged to clients, advertisers or other parties, so that the provider funds the API and the client knows what it will pay. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) |
| [Rate Limit](/architecture/api-patterns/documentation/rate-limit) | The Rate Limit pattern protects an API against excessive use by defining and communicating a maximum number of requests each client may make in a time window, rejecting, postponing or degrading those beyond the limit. | [`Performance`](/tags/performance) [`Security`](/tags/security) |
| [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) | The Service Level Agreement (SLA) pattern defines, in measurable terms, the quality-of-service characteristics that an API provider guarantees and the consequences of failing to meet them. | [`Shared Understanding`](/tags/shared-understanding) [`Performance`](/tags/performance) |

## By tag

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
