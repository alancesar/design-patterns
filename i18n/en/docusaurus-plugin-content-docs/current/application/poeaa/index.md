---
title: "Patterns of Enterprise Application Architecture"
sidebar_label: "PoEAA"
---

# Patterns of Enterprise Application Architecture

Personal catalog based on Martin Fowler's [Catalog of Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/). Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (design goals), a Mermaid diagram, and a code example.

Total: 51 patterns in 10 groups. Tags: Design goal.

## Groups

- [Domain Logic](#domain-logic) (4)
- [Data Source Architectural](#data-source-architectural) (4)
- [Object-Relational Behavioral](#object-relational-behavioral) (3)
- [Object-Relational Structural](#object-relational-structural) (10)
- [Object-Relational Metadata Mapping](#object-relational-metadata-mapping) (3)
- [Web Presentation](#web-presentation) (7)
- [Distribution](#distribution) (2)
- [Offline Concurrency](#offline-concurrency) (4)
- [Session State](#session-state) (3)
- [Base](#base) (11)

## Domain Logic (4) {#domain-logic}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Transaction Script](/application/poeaa/domain-logic/transaction-script) | Transaction Script organizes business logic as procedures, with one procedure for each request coming from the presentation layer. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Domain Model](/application/poeaa/domain-logic/domain-model) | Domain Model is an object model of the business domain that incorporates both behavior and data. | [`Extensibility`](/tags/extensibility) [`Testability`](/tags/testability) |
| [Table Module](/application/poeaa/domain-logic/table-module) | Table Module is a single instance that handles the business logic for all the rows in a database table or view. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Service Layer](/application/poeaa/domain-logic/service-layer) | Service Layer defines an application's boundary as a set of services that expose the available operations and coordinate the responses. | [`Decoupling`](/tags/decoupling) [`Consistency`](/tags/consistency) [`Testability`](/tags/testability) |

## Data Source Architectural (4) {#data-source-architectural}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Table Data Gateway](/application/poeaa/data-source-architectural/table-data-gateway) | Table Data Gateway is an object that acts as a gateway to a database table (or view). | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Row Data Gateway](/application/poeaa/data-source-architectural/row-data-gateway) | Row Data Gateway is an object that acts as a gateway to a single record in a data source, with one instance per row. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Active Record](/application/poeaa/data-source-architectural/active-record) | Active Record is an object that wraps a row in a table or view, encapsulates database access, and adds domain logic on top of that data. | [`Simplicity`](/tags/simplicity) |
| [Data Mapper](/application/poeaa/data-source-architectural/data-mapper) | Data Mapper is a data access layer that moves data between in-memory objects and the database, keeping the two independent of each other and of the mapper itself. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) [`Extensibility`](/tags/extensibility) |

## Object-Relational Behavioral (3) {#object-relational-behavioral}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Unit of Work](/application/poeaa/object-relational-behavioral/unit-of-work) | Unit of Work keeps a list of the objects affected by a business transaction and coordinates writing the changes to the database, as well as resolving concurrency problems. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Identity Map](/application/poeaa/object-relational-behavioral/identity-map) | Identity Map ensures that each object is loaded from the database only once per session by keeping a map of already-read objects, indexed by primary key. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Lazy Load](/application/poeaa/object-relational-behavioral/lazy-load) | Lazy Load is an object that doesn't contain all the data it needs, but knows how to get it when it's required. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Object-Relational Structural (10) {#object-relational-structural}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Identity Field](/application/poeaa/object-relational-structural/identity-field) | Identity Field stores the database row's primary key in the object, to maintain identity between the in-memory object and the corresponding row. | [`Consistency`](/tags/consistency) |
| [Inheritance Mappers](/application/poeaa/object-relational-structural/inheritance-mappers) | Inheritance Mappers organizes the mappers of an inheritance hierarchy so that common mapping logic lives in one place and class-specific logic in another. | [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) |
| [Foreign Key Mapping](/application/poeaa/object-relational-structural/foreign-key-mapping) | Foreign Key Mapping maps an association between objects to a foreign key between tables. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Association Table Mapping](/application/poeaa/object-relational-structural/association-table-mapping) | Association Table Mapping saves an association as a table with foreign keys to the tables linked by the association. | [`Consistency`](/tags/consistency) |
| [Dependent Mapping](/application/poeaa/object-relational-structural/dependent-mapping) | Dependent Mapping makes one class responsible for saving and loading the children that depend on it. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Embedded Value](/application/poeaa/object-relational-structural/embedded-value) | Embedded Value maps an object into several fields of another object's table. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Serialized LOB](/application/poeaa/object-relational-structural/serialized-lob) | Serialized LOB saves an object graph by serializing it and writing the result into a large object (LOB) field in a single column. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Single Table Inheritance](/application/poeaa/object-relational-structural/single-table-inheritance) | Single Table Inheritance represents a class hierarchy as a single table, with columns for all the fields of all the classes. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Class Table Inheritance](/application/poeaa/object-relational-structural/class-table-inheritance) | Class Table Inheritance represents an inheritance hierarchy with one table per class. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) |
| [Concrete Table Inheritance](/application/poeaa/object-relational-structural/concrete-table-inheritance) | Concrete Table Inheritance represents a hierarchy with one table per concrete class. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |

## Object-Relational Metadata Mapping (3) {#object-relational-metadata-mapping}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Metadata Mapping](/application/poeaa/object-relational-metadata-mapping/metadata-mapping) | Metadata Mapping keeps the details of the object-relational mapping in metadata instead of scattering them across hand-written code. | [`Simplicity`](/tags/simplicity) [`Extensibility`](/tags/extensibility) |
| [Query Object](/application/poeaa/object-relational-metadata-mapping/query-object) | A Query Object is an object that represents a database query. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) |
| [Repository](/application/poeaa/object-relational-metadata-mapping/repository) | A Repository sits between the domain and the data mapping layer and presents persisted objects through an interface similar to an in-memory collection. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |

## Web Presentation (7) {#web-presentation}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Model View Controller](/application/poeaa/web-presentation/model-view-controller) | Model View Controller (MVC) splits user interaction into three roles. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) [`Extensibility`](/tags/extensibility) |
| [Page Controller](/application/poeaa/web-presentation/page-controller) | Page Controller is an object that handles the request for a specific page or action of a website. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Front Controller](/application/poeaa/web-presentation/front-controller) | Front Controller is a single controller that handles all requests for a website. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) |
| [Template View](/application/poeaa/web-presentation/template-view) | Template View renders information as HTML by embedding markers in a static page. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Transform View](/application/poeaa/web-presentation/transform-view) | Transform View is a view that processes domain data element by element and transforms it into HTML (or another format). | [`Testability`](/tags/testability) [`Decoupling`](/tags/decoupling) |
| [Two Step View](/application/poeaa/web-presentation/two-step-view) | Two Step View transforms domain data into HTML in two steps. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) |
| [Application Controller](/application/poeaa/web-presentation/application-controller) | Application Controller is a central point for handling navigation between screens and the application's flow. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) [`Testability`](/tags/testability) |

## Distribution (2) {#distribution}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Remote Facade](/application/poeaa/distribution/remote-facade) | The Remote Facade provides a coarse-grained interface over fine-grained objects to make network access efficient. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Data Transfer Object](/application/poeaa/distribution/data-transfer-object) | The Data Transfer Object (DTO) is an object that carries data between processes to reduce the number of calls. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Offline Concurrency (4) {#offline-concurrency}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Optimistic Offline Lock](/application/poeaa/offline-concurrency/optimistic-offline-lock) | Optimistic Offline Lock prevents conflicts between concurrent business transactions by validating, at commit time, that nobody has changed the data the session read. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Pessimistic Offline Lock](/application/poeaa/offline-concurrency/pessimistic-offline-lock) | Pessimistic Offline Lock prevents conflicts between concurrent business transactions by allowing only one session at a time to edit a piece of data. | [`Consistency`](/tags/consistency) |
| [Coarse-Grained Lock](/application/poeaa/offline-concurrency/coarse-grained-lock) | Coarse-Grained Lock locks a set of related objects with a single lock. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Implicit Lock](/application/poeaa/offline-concurrency/implicit-lock) | Implicit Lock lets framework code or a layer supertype acquire offline locks automatically, instead of relying on the developer to remember to do so at every point of use. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |

## Session State (3) {#session-state}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Client Session State](/application/poeaa/session-state/client-session-state) | Client Session State stores session state on the client. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Server Session State](/application/poeaa/session-state/server-session-state) | Server Session State keeps session state on the server, in serialized form or as in-memory objects. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Database Session State](/application/poeaa/session-state/database-session-state) | Database Session State stores session data as committed data in the database. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |

## Base (11) {#base}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Gateway](/application/poeaa/base/gateway) | A Gateway is an object that encapsulates access to an external system or resource, such as a database, a payment service, a queue, or an XML file. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Service Stub](/application/poeaa/base/service-stub) | A Service Stub removes dependence on problematic services during testing. | [`Testability`](/tags/testability) [`Decoupling`](/tags/decoupling) |
| [Record Set](/application/poeaa/base/record-set) | A Record Set is an in-memory representation of tabular data. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Mapper](/application/poeaa/base/mapper) | A Mapper is an object that sets up communication between two independent objects or subsystems. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) |
| [Layer Supertype](/application/poeaa/base/layer-supertype) | A Layer Supertype is a type that acts as the supertype for all the types in a layer. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Separated Interface](/application/poeaa/base/separated-interface) | A Separated Interface puts an interface in a different package from its implementation. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Registry](/application/poeaa/base/registry) | A Registry is a well-known object that other objects use to find common objects and services. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Value Object](/application/poeaa/base/value-object) | A Value Object is a small, simple object, such as a monetary amount or a date range, whose equality isn't based on identity. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Money](/application/poeaa/base/money) | Money represents a monetary value. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Special Case](/application/poeaa/base/special-case) | A Special Case is a subclass that provides special behavior for particular cases. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Plugin](/application/poeaa/base/plugin) | A Plugin links classes at configuration time, not at compile time. | [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |

## By tag

### Decoupling (24)

[Service Layer](/application/poeaa/domain-logic/service-layer), [Table Data Gateway](/application/poeaa/data-source-architectural/table-data-gateway), [Row Data Gateway](/application/poeaa/data-source-architectural/row-data-gateway), [Data Mapper](/application/poeaa/data-source-architectural/data-mapper), [Lazy Load](/application/poeaa/object-relational-behavioral/lazy-load), [Inheritance Mappers](/application/poeaa/object-relational-structural/inheritance-mappers), [Dependent Mapping](/application/poeaa/object-relational-structural/dependent-mapping), [Query Object](/application/poeaa/object-relational-metadata-mapping/query-object), [Repository](/application/poeaa/object-relational-metadata-mapping/repository), [Model View Controller](/application/poeaa/web-presentation/model-view-controller), [Front Controller](/application/poeaa/web-presentation/front-controller), [Template View](/application/poeaa/web-presentation/template-view), [Transform View](/application/poeaa/web-presentation/transform-view), [Application Controller](/application/poeaa/web-presentation/application-controller), [Remote Facade](/application/poeaa/distribution/remote-facade), [Data Transfer Object](/application/poeaa/distribution/data-transfer-object), [Implicit Lock](/application/poeaa/offline-concurrency/implicit-lock), [Client Session State](/application/poeaa/session-state/client-session-state), [Database Session State](/application/poeaa/session-state/database-session-state), [Gateway](/application/poeaa/base/gateway), [Service Stub](/application/poeaa/base/service-stub), [Mapper](/application/poeaa/base/mapper), [Separated Interface](/application/poeaa/base/separated-interface), [Plugin](/application/poeaa/base/plugin)

### Simplicity (23)

[Transaction Script](/application/poeaa/domain-logic/transaction-script), [Table Module](/application/poeaa/domain-logic/table-module), [Table Data Gateway](/application/poeaa/data-source-architectural/table-data-gateway), [Active Record](/application/poeaa/data-source-architectural/active-record), [Foreign Key Mapping](/application/poeaa/object-relational-structural/foreign-key-mapping), [Dependent Mapping](/application/poeaa/object-relational-structural/dependent-mapping), [Embedded Value](/application/poeaa/object-relational-structural/embedded-value), [Serialized LOB](/application/poeaa/object-relational-structural/serialized-lob), [Single Table Inheritance](/application/poeaa/object-relational-structural/single-table-inheritance), [Concrete Table Inheritance](/application/poeaa/object-relational-structural/concrete-table-inheritance), [Metadata Mapping](/application/poeaa/object-relational-metadata-mapping/metadata-mapping), [Page Controller](/application/poeaa/web-presentation/page-controller), [Template View](/application/poeaa/web-presentation/template-view), [Remote Facade](/application/poeaa/distribution/remote-facade), [Coarse-Grained Lock](/application/poeaa/offline-concurrency/coarse-grained-lock), [Client Session State](/application/poeaa/session-state/client-session-state), [Server Session State](/application/poeaa/session-state/server-session-state), [Record Set](/application/poeaa/base/record-set), [Layer Supertype](/application/poeaa/base/layer-supertype), [Registry](/application/poeaa/base/registry), [Value Object](/application/poeaa/base/value-object), [Money](/application/poeaa/base/money), [Special Case](/application/poeaa/base/special-case)

### Extensibility (12)

[Domain Model](/application/poeaa/domain-logic/domain-model), [Data Mapper](/application/poeaa/data-source-architectural/data-mapper), [Inheritance Mappers](/application/poeaa/object-relational-structural/inheritance-mappers), [Class Table Inheritance](/application/poeaa/object-relational-structural/class-table-inheritance), [Metadata Mapping](/application/poeaa/object-relational-metadata-mapping/metadata-mapping), [Query Object](/application/poeaa/object-relational-metadata-mapping/query-object), [Model View Controller](/application/poeaa/web-presentation/model-view-controller), [Front Controller](/application/poeaa/web-presentation/front-controller), [Two Step View](/application/poeaa/web-presentation/two-step-view), [Application Controller](/application/poeaa/web-presentation/application-controller), [Mapper](/application/poeaa/base/mapper), [Plugin](/application/poeaa/base/plugin)

### Performance (14)

[Transaction Script](/application/poeaa/domain-logic/transaction-script), [Table Module](/application/poeaa/domain-logic/table-module), [Unit of Work](/application/poeaa/object-relational-behavioral/unit-of-work), [Identity Map](/application/poeaa/object-relational-behavioral/identity-map), [Lazy Load](/application/poeaa/object-relational-behavioral/lazy-load), [Embedded Value](/application/poeaa/object-relational-structural/embedded-value), [Serialized LOB](/application/poeaa/object-relational-structural/serialized-lob), [Single Table Inheritance](/application/poeaa/object-relational-structural/single-table-inheritance), [Concrete Table Inheritance](/application/poeaa/object-relational-structural/concrete-table-inheritance), [Remote Facade](/application/poeaa/distribution/remote-facade), [Data Transfer Object](/application/poeaa/distribution/data-transfer-object), [Optimistic Offline Lock](/application/poeaa/offline-concurrency/optimistic-offline-lock), [Server Session State](/application/poeaa/session-state/server-session-state), [Record Set](/application/poeaa/base/record-set)

### Consistency (17)

[Service Layer](/application/poeaa/domain-logic/service-layer), [Unit of Work](/application/poeaa/object-relational-behavioral/unit-of-work), [Identity Map](/application/poeaa/object-relational-behavioral/identity-map), [Identity Field](/application/poeaa/object-relational-structural/identity-field), [Foreign Key Mapping](/application/poeaa/object-relational-structural/foreign-key-mapping), [Association Table Mapping](/application/poeaa/object-relational-structural/association-table-mapping), [Class Table Inheritance](/application/poeaa/object-relational-structural/class-table-inheritance), [Front Controller](/application/poeaa/web-presentation/front-controller), [Two Step View](/application/poeaa/web-presentation/two-step-view), [Optimistic Offline Lock](/application/poeaa/offline-concurrency/optimistic-offline-lock), [Pessimistic Offline Lock](/application/poeaa/offline-concurrency/pessimistic-offline-lock), [Coarse-Grained Lock](/application/poeaa/offline-concurrency/coarse-grained-lock), [Implicit Lock](/application/poeaa/offline-concurrency/implicit-lock), [Database Session State](/application/poeaa/session-state/database-session-state), [Layer Supertype](/application/poeaa/base/layer-supertype), [Value Object](/application/poeaa/base/value-object), [Money](/application/poeaa/base/money)

### Testability (16)

[Domain Model](/application/poeaa/domain-logic/domain-model), [Service Layer](/application/poeaa/domain-logic/service-layer), [Row Data Gateway](/application/poeaa/data-source-architectural/row-data-gateway), [Data Mapper](/application/poeaa/data-source-architectural/data-mapper), [Repository](/application/poeaa/object-relational-metadata-mapping/repository), [Model View Controller](/application/poeaa/web-presentation/model-view-controller), [Page Controller](/application/poeaa/web-presentation/page-controller), [Transform View](/application/poeaa/web-presentation/transform-view), [Application Controller](/application/poeaa/web-presentation/application-controller), [Gateway](/application/poeaa/base/gateway), [Service Stub](/application/poeaa/base/service-stub), [Separated Interface](/application/poeaa/base/separated-interface), [Registry](/application/poeaa/base/registry), [Value Object](/application/poeaa/base/value-object), [Special Case](/application/poeaa/base/special-case), [Plugin](/application/poeaa/base/plugin)
