---
title: "Patterns of Enterprise Application Architecture"
sidebar_label: "PoEAA"
---

# Patterns of Enterprise Application Architecture

Catálogo pessoal baseado no [Catalog of Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/), de Martin Fowler. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (objetivos de design), um diagrama Mermaid e um exemplo de código.

Total: 51 padrões em 10 grupos. Etiquetas: Objetivo de design.

## Grupos

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

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Transaction Script](/design/poeaa/domain-logic/transaction-script) | O Transaction Script organiza a lógica de negócio como procedimentos, com um procedimento para cada requisição vinda da camada de apresentação. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Domain Model](/design/poeaa/domain-logic/domain-model) | O Domain Model é um modelo de objetos do domínio de negócio que incorpora tanto o comportamento quanto os dados. | [`Extensibility`](/tags/extensibility) [`Testability`](/tags/testability) |
| [Table Module](/design/poeaa/domain-logic/table-module) | O Table Module é uma única instância que trata a lógica de negócio de todas as linhas de uma tabela ou view do banco de dados. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Service Layer](/design/poeaa/domain-logic/service-layer) | O Service Layer define a fronteira de uma aplicação como um conjunto de serviços que expõem as operações disponíveis e coordenam as respostas. | [`Decoupling`](/tags/decoupling) [`Consistency`](/tags/consistency) [`Testability`](/tags/testability) |

## Data Source Architectural (4) {#data-source-architectural}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Table Data Gateway](/design/poeaa/data-source-architectural/table-data-gateway) | O Table Data Gateway é um objeto que atua como gateway para uma tabela (ou view) do banco de dados. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Row Data Gateway](/design/poeaa/data-source-architectural/row-data-gateway) | O Row Data Gateway é um objeto que atua como gateway para um único registro de uma fonte de dados, com uma instância por linha. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Active Record](/design/poeaa/data-source-architectural/active-record) | O Active Record é um objeto que envolve uma linha de uma tabela ou view, encapsula o acesso ao banco e adiciona lógica de domínio sobre esses dados. | [`Simplicity`](/tags/simplicity) |
| [Data Mapper](/design/poeaa/data-source-architectural/data-mapper) | O Data Mapper é uma camada de acesso a dados que transfere dados entre objetos em memória e o banco, mantendo ambos independentes entre si e do próprio mapper. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) [`Extensibility`](/tags/extensibility) |

## Object-Relational Behavioral (3) {#object-relational-behavioral}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Unit of Work](/design/poeaa/object-relational-behavioral/unit-of-work) | O Unit of Work mantém uma lista dos objetos afetados por uma transação de negócio e coordena a escrita das mudanças no banco de dados, além da resolução de problemas de concorrência. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Identity Map](/design/poeaa/object-relational-behavioral/identity-map) | O Identity Map garante que cada objeto seja carregado do banco de dados uma única vez por sessão, mantendo um mapa de objetos já lidos indexado pela chave primária. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Lazy Load](/design/poeaa/object-relational-behavioral/lazy-load) | O Lazy Load é um objeto que não contém todos os dados de que precisa, mas sabe como obtê-los quando forem necessários. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Object-Relational Structural (10) {#object-relational-structural}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Identity Field](/design/poeaa/object-relational-structural/identity-field) | O Identity Field guarda no objeto a chave primária da linha do banco de dados, para manter a identidade entre o objeto em memória e a linha correspondente. | [`Consistency`](/tags/consistency) |
| [Inheritance Mappers](/design/poeaa/object-relational-structural/inheritance-mappers) | O Inheritance Mappers organiza os mapeadores de uma hierarquia de herança para que a lógica de mapeamento comum fique em um lugar e a específica de cada classe em outro. | [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) |
| [Foreign Key Mapping](/design/poeaa/object-relational-structural/foreign-key-mapping) | O Foreign Key Mapping mapeia uma associação entre objetos para uma chave estrangeira entre tabelas. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Association Table Mapping](/design/poeaa/object-relational-structural/association-table-mapping) | O Association Table Mapping salva uma associação como uma tabela com chaves estrangeiras para as tabelas ligadas pela associação. | [`Consistency`](/tags/consistency) |
| [Dependent Mapping](/design/poeaa/object-relational-structural/dependent-mapping) | O Dependent Mapping faz uma classe ser responsável por salvar e carregar os filhos que dependem dela. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Embedded Value](/design/poeaa/object-relational-structural/embedded-value) | O Embedded Value mapeia um objeto para vários campos da tabela de outro objeto. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Serialized LOB](/design/poeaa/object-relational-structural/serialized-lob) | O Serialized LOB salva um grafo de objetos serializando-o e gravando o resultado em um campo grande (LOB) de uma única coluna. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Single Table Inheritance](/design/poeaa/object-relational-structural/single-table-inheritance) | O Single Table Inheritance representa uma hierarquia de classes como uma única tabela, com colunas para todos os campos de todas as classes. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Class Table Inheritance](/design/poeaa/object-relational-structural/class-table-inheritance) | O Class Table Inheritance representa uma hierarquia de herança com uma tabela por classe. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) |
| [Concrete Table Inheritance](/design/poeaa/object-relational-structural/concrete-table-inheritance) | O Concrete Table Inheritance representa uma hierarquia com uma tabela por classe concreta. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |

## Object-Relational Metadata Mapping (3) {#object-relational-metadata-mapping}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Metadata Mapping](/design/poeaa/object-relational-metadata-mapping/metadata-mapping) | O Metadata Mapping mantém os detalhes do mapeamento objeto-relacional em metadados, em vez de espalhá-los em código escrito à mão. | [`Simplicity`](/tags/simplicity) [`Extensibility`](/tags/extensibility) |
| [Query Object](/design/poeaa/object-relational-metadata-mapping/query-object) | O Query Object é um objeto que representa uma consulta ao banco de dados. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) |
| [Repository](/design/poeaa/object-relational-metadata-mapping/repository) | O Repository fica entre o domínio e a camada de mapeamento de dados e apresenta os objetos persistidos por meio de uma interface semelhante à de uma coleção em memória. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |

## Web Presentation (7) {#web-presentation}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Model View Controller](/design/poeaa/web-presentation/model-view-controller) | O Model View Controller (MVC) divide a interação com o usuário em três papéis. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) [`Extensibility`](/tags/extensibility) |
| [Page Controller](/design/poeaa/web-presentation/page-controller) | O Page Controller é um objeto que trata a requisição de uma página ou ação específica de um site. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Front Controller](/design/poeaa/web-presentation/front-controller) | O Front Controller é um único controller que trata todas as requisições de um site. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) |
| [Template View](/design/poeaa/web-presentation/template-view) | O Template View renderiza informação em HTML incorporando marcadores em uma página estática. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Transform View](/design/poeaa/web-presentation/transform-view) | O Transform View é uma view que processa dados de domínio elemento por elemento e os transforma em HTML (ou outro formato). | [`Testability`](/tags/testability) [`Decoupling`](/tags/decoupling) |
| [Two Step View](/design/poeaa/web-presentation/two-step-view) | O Two Step View transforma dados de domínio em HTML em duas etapas. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) |
| [Application Controller](/design/poeaa/web-presentation/application-controller) | O Application Controller é um ponto central para tratar a navegação entre telas e o fluxo da aplicação. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) [`Testability`](/tags/testability) |

## Distribution (2) {#distribution}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Remote Facade](/design/poeaa/distribution/remote-facade) | O Remote Facade oferece uma interface de granularidade grossa sobre objetos de granularidade fina, para tornar eficiente o acesso por rede. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) | O Data Transfer Object (DTO) é um objeto que carrega dados entre processos para reduzir o número de chamadas. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Offline Concurrency (4) {#offline-concurrency}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Optimistic Offline Lock](/design/poeaa/offline-concurrency/optimistic-offline-lock) | O Optimistic Offline Lock evita conflitos entre transações de negócio concorrentes validando, no momento do commit, que ninguém alterou os dados que a sessão leu. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Pessimistic Offline Lock](/design/poeaa/offline-concurrency/pessimistic-offline-lock) | O Pessimistic Offline Lock previne conflitos entre transações de negócio concorrentes permitindo que apenas uma sessão por vez edite um dado. | [`Consistency`](/tags/consistency) |
| [Coarse-Grained Lock](/design/poeaa/offline-concurrency/coarse-grained-lock) | O Coarse-Grained Lock bloqueia um conjunto de objetos relacionados com um único bloqueio. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Implicit Lock](/design/poeaa/offline-concurrency/implicit-lock) | O Implicit Lock permite que código de framework ou de um supertipo de camada adquira bloqueios offline automaticamente, em vez de depender de o desenvolvedor lembrar de fazê-lo em cada ponto de uso. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |

## Session State (3) {#session-state}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Client Session State](/design/poeaa/session-state/client-session-state) | O Client Session State armazena o estado da sessão no cliente. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Server Session State](/design/poeaa/session-state/server-session-state) | O Server Session State mantém o estado da sessão no servidor, em forma serializada ou como objetos em memória. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Database Session State](/design/poeaa/session-state/database-session-state) | O Database Session State armazena os dados da sessão como dados confirmados (committed) no banco de dados. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |

## Base (11) {#base}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Gateway](/design/poeaa/base/gateway) | O Gateway é um objeto que encapsula o acesso a um sistema ou recurso externo, como um banco de dados, um serviço de pagamento, uma fila ou um arquivo XML. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Service Stub](/design/poeaa/base/service-stub) | O Service Stub remove a dependência de serviços problemáticos durante os testes. | [`Testability`](/tags/testability) [`Decoupling`](/tags/decoupling) |
| [Record Set](/design/poeaa/base/record-set) | O Record Set é uma representação em memória de dados tabulares. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Mapper](/design/poeaa/base/mapper) | O Mapper é um objeto que estabelece a comunicação entre dois objetos ou subsistemas independentes. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) |
| [Layer Supertype](/design/poeaa/base/layer-supertype) | O Layer Supertype é um tipo que atua como supertipo de todos os tipos de uma camada. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Separated Interface](/design/poeaa/base/separated-interface) | O Separated Interface coloca uma interface em um pacote diferente do pacote da sua implementação. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Registry](/design/poeaa/base/registry) | O Registry é um objeto bem conhecido que outros objetos usam para encontrar objetos e serviços comuns. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Value Object](/design/poeaa/base/value-object) | O Value Object é um objeto pequeno e simples, como um valor monetário ou um intervalo de datas, cuja igualdade não se baseia em identidade. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Money](/design/poeaa/base/money) | O Money representa um valor monetário. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Special Case](/design/poeaa/base/special-case) | O Special Case é uma subclasse que fornece comportamento especial para casos particulares. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Plugin](/design/poeaa/base/plugin) | O Plugin liga classes durante a configuração, e não durante a compilação. | [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |

## Por etiqueta

### Decoupling (24)

[Service Layer](/design/poeaa/domain-logic/service-layer), [Table Data Gateway](/design/poeaa/data-source-architectural/table-data-gateway), [Row Data Gateway](/design/poeaa/data-source-architectural/row-data-gateway), [Data Mapper](/design/poeaa/data-source-architectural/data-mapper), [Lazy Load](/design/poeaa/object-relational-behavioral/lazy-load), [Inheritance Mappers](/design/poeaa/object-relational-structural/inheritance-mappers), [Dependent Mapping](/design/poeaa/object-relational-structural/dependent-mapping), [Query Object](/design/poeaa/object-relational-metadata-mapping/query-object), [Repository](/design/poeaa/object-relational-metadata-mapping/repository), [Model View Controller](/design/poeaa/web-presentation/model-view-controller), [Front Controller](/design/poeaa/web-presentation/front-controller), [Template View](/design/poeaa/web-presentation/template-view), [Transform View](/design/poeaa/web-presentation/transform-view), [Application Controller](/design/poeaa/web-presentation/application-controller), [Remote Facade](/design/poeaa/distribution/remote-facade), [Data Transfer Object](/design/poeaa/distribution/data-transfer-object), [Implicit Lock](/design/poeaa/offline-concurrency/implicit-lock), [Client Session State](/design/poeaa/session-state/client-session-state), [Database Session State](/design/poeaa/session-state/database-session-state), [Gateway](/design/poeaa/base/gateway), [Service Stub](/design/poeaa/base/service-stub), [Mapper](/design/poeaa/base/mapper), [Separated Interface](/design/poeaa/base/separated-interface), [Plugin](/design/poeaa/base/plugin)

### Simplicity (23)

[Transaction Script](/design/poeaa/domain-logic/transaction-script), [Table Module](/design/poeaa/domain-logic/table-module), [Table Data Gateway](/design/poeaa/data-source-architectural/table-data-gateway), [Active Record](/design/poeaa/data-source-architectural/active-record), [Foreign Key Mapping](/design/poeaa/object-relational-structural/foreign-key-mapping), [Dependent Mapping](/design/poeaa/object-relational-structural/dependent-mapping), [Embedded Value](/design/poeaa/object-relational-structural/embedded-value), [Serialized LOB](/design/poeaa/object-relational-structural/serialized-lob), [Single Table Inheritance](/design/poeaa/object-relational-structural/single-table-inheritance), [Concrete Table Inheritance](/design/poeaa/object-relational-structural/concrete-table-inheritance), [Metadata Mapping](/design/poeaa/object-relational-metadata-mapping/metadata-mapping), [Page Controller](/design/poeaa/web-presentation/page-controller), [Template View](/design/poeaa/web-presentation/template-view), [Remote Facade](/design/poeaa/distribution/remote-facade), [Coarse-Grained Lock](/design/poeaa/offline-concurrency/coarse-grained-lock), [Client Session State](/design/poeaa/session-state/client-session-state), [Server Session State](/design/poeaa/session-state/server-session-state), [Record Set](/design/poeaa/base/record-set), [Layer Supertype](/design/poeaa/base/layer-supertype), [Registry](/design/poeaa/base/registry), [Value Object](/design/poeaa/base/value-object), [Money](/design/poeaa/base/money), [Special Case](/design/poeaa/base/special-case)

### Extensibility (12)

[Domain Model](/design/poeaa/domain-logic/domain-model), [Data Mapper](/design/poeaa/data-source-architectural/data-mapper), [Inheritance Mappers](/design/poeaa/object-relational-structural/inheritance-mappers), [Class Table Inheritance](/design/poeaa/object-relational-structural/class-table-inheritance), [Metadata Mapping](/design/poeaa/object-relational-metadata-mapping/metadata-mapping), [Query Object](/design/poeaa/object-relational-metadata-mapping/query-object), [Model View Controller](/design/poeaa/web-presentation/model-view-controller), [Front Controller](/design/poeaa/web-presentation/front-controller), [Two Step View](/design/poeaa/web-presentation/two-step-view), [Application Controller](/design/poeaa/web-presentation/application-controller), [Mapper](/design/poeaa/base/mapper), [Plugin](/design/poeaa/base/plugin)

### Performance (14)

[Transaction Script](/design/poeaa/domain-logic/transaction-script), [Table Module](/design/poeaa/domain-logic/table-module), [Unit of Work](/design/poeaa/object-relational-behavioral/unit-of-work), [Identity Map](/design/poeaa/object-relational-behavioral/identity-map), [Lazy Load](/design/poeaa/object-relational-behavioral/lazy-load), [Embedded Value](/design/poeaa/object-relational-structural/embedded-value), [Serialized LOB](/design/poeaa/object-relational-structural/serialized-lob), [Single Table Inheritance](/design/poeaa/object-relational-structural/single-table-inheritance), [Concrete Table Inheritance](/design/poeaa/object-relational-structural/concrete-table-inheritance), [Remote Facade](/design/poeaa/distribution/remote-facade), [Data Transfer Object](/design/poeaa/distribution/data-transfer-object), [Optimistic Offline Lock](/design/poeaa/offline-concurrency/optimistic-offline-lock), [Server Session State](/design/poeaa/session-state/server-session-state), [Record Set](/design/poeaa/base/record-set)

### Consistency (17)

[Service Layer](/design/poeaa/domain-logic/service-layer), [Unit of Work](/design/poeaa/object-relational-behavioral/unit-of-work), [Identity Map](/design/poeaa/object-relational-behavioral/identity-map), [Identity Field](/design/poeaa/object-relational-structural/identity-field), [Foreign Key Mapping](/design/poeaa/object-relational-structural/foreign-key-mapping), [Association Table Mapping](/design/poeaa/object-relational-structural/association-table-mapping), [Class Table Inheritance](/design/poeaa/object-relational-structural/class-table-inheritance), [Front Controller](/design/poeaa/web-presentation/front-controller), [Two Step View](/design/poeaa/web-presentation/two-step-view), [Optimistic Offline Lock](/design/poeaa/offline-concurrency/optimistic-offline-lock), [Pessimistic Offline Lock](/design/poeaa/offline-concurrency/pessimistic-offline-lock), [Coarse-Grained Lock](/design/poeaa/offline-concurrency/coarse-grained-lock), [Implicit Lock](/design/poeaa/offline-concurrency/implicit-lock), [Database Session State](/design/poeaa/session-state/database-session-state), [Layer Supertype](/design/poeaa/base/layer-supertype), [Value Object](/design/poeaa/base/value-object), [Money](/design/poeaa/base/money)

### Testability (16)

[Domain Model](/design/poeaa/domain-logic/domain-model), [Service Layer](/design/poeaa/domain-logic/service-layer), [Row Data Gateway](/design/poeaa/data-source-architectural/row-data-gateway), [Data Mapper](/design/poeaa/data-source-architectural/data-mapper), [Repository](/design/poeaa/object-relational-metadata-mapping/repository), [Model View Controller](/design/poeaa/web-presentation/model-view-controller), [Page Controller](/design/poeaa/web-presentation/page-controller), [Transform View](/design/poeaa/web-presentation/transform-view), [Application Controller](/design/poeaa/web-presentation/application-controller), [Gateway](/design/poeaa/base/gateway), [Service Stub](/design/poeaa/base/service-stub), [Separated Interface](/design/poeaa/base/separated-interface), [Registry](/design/poeaa/base/registry), [Value Object](/design/poeaa/base/value-object), [Special Case](/design/poeaa/base/special-case), [Plugin](/design/poeaa/base/plugin)
