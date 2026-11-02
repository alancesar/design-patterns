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
| [Transaction Script](./domain-logic/transaction-script.md) | O Transaction Script organiza a lógica de negócio como procedimentos, com um procedimento para cada requisição vinda da camada de apresentação. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Domain Model](./domain-logic/domain-model.md) | O Domain Model é um modelo de objetos do domínio de negócio que incorpora tanto o comportamento quanto os dados. | [`Extensibility`](/tags/extensibility) [`Testability`](/tags/testability) |
| [Table Module](./domain-logic/table-module.md) | O Table Module é uma única instância que trata a lógica de negócio de todas as linhas de uma tabela ou view do banco de dados. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Service Layer](./domain-logic/service-layer.md) | O Service Layer define a fronteira de uma aplicação como um conjunto de serviços que expõem as operações disponíveis e coordenam as respostas. | [`Decoupling`](/tags/decoupling) [`Consistency`](/tags/consistency) [`Testability`](/tags/testability) |

## Data Source Architectural (4) {#data-source-architectural}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Table Data Gateway](./data-source-architectural/table-data-gateway.md) | O Table Data Gateway é um objeto que atua como gateway para uma tabela (ou view) do banco de dados. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Row Data Gateway](./data-source-architectural/row-data-gateway.md) | O Row Data Gateway é um objeto que atua como gateway para um único registro de uma fonte de dados, com uma instância por linha. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Active Record](./data-source-architectural/active-record.md) | O Active Record é um objeto que envolve uma linha de uma tabela ou view, encapsula o acesso ao banco e adiciona lógica de domínio sobre esses dados. | [`Simplicity`](/tags/simplicity) |
| [Data Mapper](./data-source-architectural/data-mapper.md) | O Data Mapper é uma camada de acesso a dados que transfere dados entre objetos em memória e o banco, mantendo ambos independentes entre si e do próprio mapper. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) [`Extensibility`](/tags/extensibility) |

## Object-Relational Behavioral (3) {#object-relational-behavioral}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Unit of Work](./object-relational-behavioral/unit-of-work.md) | O Unit of Work mantém uma lista dos objetos afetados por uma transação de negócio e coordena a escrita das mudanças no banco de dados, além da resolução de problemas de concorrência. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Identity Map](./object-relational-behavioral/identity-map.md) | O Identity Map garante que cada objeto seja carregado do banco de dados uma única vez por sessão, mantendo um mapa de objetos já lidos indexado pela chave primária. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Lazy Load](./object-relational-behavioral/lazy-load.md) | O Lazy Load é um objeto que não contém todos os dados de que precisa, mas sabe como obtê-los quando forem necessários. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Object-Relational Structural (10) {#object-relational-structural}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Identity Field](./object-relational-structural/identity-field.md) | O Identity Field guarda no objeto a chave primária da linha do banco de dados, para manter a identidade entre o objeto em memória e a linha correspondente. | [`Consistency`](/tags/consistency) |
| [Inheritance Mappers](./object-relational-structural/inheritance-mappers.md) | O Inheritance Mappers organiza os mapeadores de uma hierarquia de herança para que a lógica de mapeamento comum fique em um lugar e a específica de cada classe em outro. | [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) |
| [Foreign Key Mapping](./object-relational-structural/foreign-key-mapping.md) | O Foreign Key Mapping mapeia uma associação entre objetos para uma chave estrangeira entre tabelas. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Association Table Mapping](./object-relational-structural/association-table-mapping.md) | O Association Table Mapping salva uma associação como uma tabela com chaves estrangeiras para as tabelas ligadas pela associação. | [`Consistency`](/tags/consistency) |
| [Dependent Mapping](./object-relational-structural/dependent-mapping.md) | O Dependent Mapping faz uma classe ser responsável por salvar e carregar os filhos que dependem dela. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Embedded Value](./object-relational-structural/embedded-value.md) | O Embedded Value mapeia um objeto para vários campos da tabela de outro objeto. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Serialized LOB](./object-relational-structural/serialized-lob.md) | O Serialized LOB salva um grafo de objetos serializando-o e gravando o resultado em um campo grande (LOB) de uma única coluna. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Single Table Inheritance](./object-relational-structural/single-table-inheritance.md) | O Single Table Inheritance representa uma hierarquia de classes como uma única tabela, com colunas para todos os campos de todas as classes. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Class Table Inheritance](./object-relational-structural/class-table-inheritance.md) | O Class Table Inheritance representa uma hierarquia de herança com uma tabela por classe. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) |
| [Concrete Table Inheritance](./object-relational-structural/concrete-table-inheritance.md) | O Concrete Table Inheritance representa uma hierarquia com uma tabela por classe concreta. | [`Performance`](/tags/performance) [`Simplicity`](/tags/simplicity) |

## Object-Relational Metadata Mapping (3) {#object-relational-metadata-mapping}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Metadata Mapping](./object-relational-metadata-mapping/metadata-mapping.md) | O Metadata Mapping mantém os detalhes do mapeamento objeto-relacional em metadados, em vez de espalhá-los em código escrito à mão. | [`Simplicity`](/tags/simplicity) [`Extensibility`](/tags/extensibility) |
| [Query Object](./object-relational-metadata-mapping/query-object.md) | O Query Object é um objeto que representa uma consulta ao banco de dados. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) |
| [Repository](./object-relational-metadata-mapping/repository.md) | O Repository fica entre o domínio e a camada de mapeamento de dados e apresenta os objetos persistidos por meio de uma interface semelhante à de uma coleção em memória. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |

## Web Presentation (7) {#web-presentation}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Model View Controller](./web-presentation/model-view-controller.md) | O Model View Controller (MVC) divide a interação com o usuário em três papéis. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) [`Extensibility`](/tags/extensibility) |
| [Page Controller](./web-presentation/page-controller.md) | O Page Controller é um objeto que trata a requisição de uma página ou ação específica de um site. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Front Controller](./web-presentation/front-controller.md) | O Front Controller é um único controller que trata todas as requisições de um site. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) |
| [Template View](./web-presentation/template-view.md) | O Template View renderiza informação em HTML incorporando marcadores em uma página estática. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Transform View](./web-presentation/transform-view.md) | O Transform View é uma view que processa dados de domínio elemento por elemento e os transforma em HTML (ou outro formato). | [`Testability`](/tags/testability) [`Decoupling`](/tags/decoupling) |
| [Two Step View](./web-presentation/two-step-view.md) | O Two Step View transforma dados de domínio em HTML em duas etapas. | [`Consistency`](/tags/consistency) [`Extensibility`](/tags/extensibility) |
| [Application Controller](./web-presentation/application-controller.md) | O Application Controller é um ponto central para tratar a navegação entre telas e o fluxo da aplicação. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) [`Testability`](/tags/testability) |

## Distribution (2) {#distribution}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Remote Facade](./distribution/remote-facade.md) | O Remote Facade oferece uma interface de granularidade grossa sobre objetos de granularidade fina, para tornar eficiente o acesso por rede. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Data Transfer Object](./distribution/data-transfer-object.md) | O Data Transfer Object (DTO) é um objeto que carrega dados entre processos para reduzir o número de chamadas. | [`Performance`](/tags/performance) [`Decoupling`](/tags/decoupling) |

## Offline Concurrency (4) {#offline-concurrency}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Optimistic Offline Lock](./offline-concurrency/optimistic-offline-lock.md) | O Optimistic Offline Lock evita conflitos entre transações de negócio concorrentes validando, no momento do commit, que ninguém alterou os dados que a sessão leu. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Pessimistic Offline Lock](./offline-concurrency/pessimistic-offline-lock.md) | O Pessimistic Offline Lock previne conflitos entre transações de negócio concorrentes permitindo que apenas uma sessão por vez edite um dado. | [`Consistency`](/tags/consistency) |
| [Coarse-Grained Lock](./offline-concurrency/coarse-grained-lock.md) | O Coarse-Grained Lock bloqueia um conjunto de objetos relacionados com um único bloqueio. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Implicit Lock](./offline-concurrency/implicit-lock.md) | O Implicit Lock permite que código de framework ou de um supertipo de camada adquira bloqueios offline automaticamente, em vez de depender de o desenvolvedor lembrar de fazê-lo em cada ponto de uso. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |

## Session State (3) {#session-state}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Client Session State](./session-state/client-session-state.md) | O Client Session State armazena o estado da sessão no cliente. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Server Session State](./session-state/server-session-state.md) | O Server Session State mantém o estado da sessão no servidor, em forma serializada ou como objetos em memória. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Database Session State](./session-state/database-session-state.md) | O Database Session State armazena os dados da sessão como dados confirmados (committed) no banco de dados. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |

## Base (11) {#base}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Gateway](./base/gateway.md) | O Gateway é um objeto que encapsula o acesso a um sistema ou recurso externo, como um banco de dados, um serviço de pagamento, uma fila ou um arquivo XML. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Service Stub](./base/service-stub.md) | O Service Stub remove a dependência de serviços problemáticos durante os testes. | [`Testability`](/tags/testability) [`Decoupling`](/tags/decoupling) |
| [Record Set](./base/record-set.md) | O Record Set é uma representação em memória de dados tabulares. | [`Simplicity`](/tags/simplicity) [`Performance`](/tags/performance) |
| [Mapper](./base/mapper.md) | O Mapper é um objeto que estabelece a comunicação entre dois objetos ou subsistemas independentes. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) |
| [Layer Supertype](./base/layer-supertype.md) | O Layer Supertype é um tipo que atua como supertipo de todos os tipos de uma camada. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Separated Interface](./base/separated-interface.md) | O Separated Interface coloca uma interface em um pacote diferente do pacote da sua implementação. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Registry](./base/registry.md) | O Registry é um objeto bem conhecido que outros objetos usam para encontrar objetos e serviços comuns. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Value Object](./base/value-object.md) | O Value Object é um objeto pequeno e simples, como um valor monetário ou um intervalo de datas, cuja igualdade não se baseia em identidade. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Money](./base/money.md) | O Money representa um valor monetário. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) |
| [Special Case](./base/special-case.md) | O Special Case é uma subclasse que fornece comportamento especial para casos particulares. | [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Plugin](./base/plugin.md) | O Plugin liga classes durante a configuração, e não durante a compilação. | [`Extensibility`](/tags/extensibility) [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |

## Por etiqueta

### Decoupling (24)

[Service Layer](./domain-logic/service-layer.md), [Table Data Gateway](./data-source-architectural/table-data-gateway.md), [Row Data Gateway](./data-source-architectural/row-data-gateway.md), [Data Mapper](./data-source-architectural/data-mapper.md), [Lazy Load](./object-relational-behavioral/lazy-load.md), [Inheritance Mappers](./object-relational-structural/inheritance-mappers.md), [Dependent Mapping](./object-relational-structural/dependent-mapping.md), [Query Object](./object-relational-metadata-mapping/query-object.md), [Repository](./object-relational-metadata-mapping/repository.md), [Model View Controller](./web-presentation/model-view-controller.md), [Front Controller](./web-presentation/front-controller.md), [Template View](./web-presentation/template-view.md), [Transform View](./web-presentation/transform-view.md), [Application Controller](./web-presentation/application-controller.md), [Remote Facade](./distribution/remote-facade.md), [Data Transfer Object](./distribution/data-transfer-object.md), [Implicit Lock](./offline-concurrency/implicit-lock.md), [Client Session State](./session-state/client-session-state.md), [Database Session State](./session-state/database-session-state.md), [Gateway](./base/gateway.md), [Service Stub](./base/service-stub.md), [Mapper](./base/mapper.md), [Separated Interface](./base/separated-interface.md), [Plugin](./base/plugin.md)

### Simplicity (23)

[Transaction Script](./domain-logic/transaction-script.md), [Table Module](./domain-logic/table-module.md), [Table Data Gateway](./data-source-architectural/table-data-gateway.md), [Active Record](./data-source-architectural/active-record.md), [Foreign Key Mapping](./object-relational-structural/foreign-key-mapping.md), [Dependent Mapping](./object-relational-structural/dependent-mapping.md), [Embedded Value](./object-relational-structural/embedded-value.md), [Serialized LOB](./object-relational-structural/serialized-lob.md), [Single Table Inheritance](./object-relational-structural/single-table-inheritance.md), [Concrete Table Inheritance](./object-relational-structural/concrete-table-inheritance.md), [Metadata Mapping](./object-relational-metadata-mapping/metadata-mapping.md), [Page Controller](./web-presentation/page-controller.md), [Template View](./web-presentation/template-view.md), [Remote Facade](./distribution/remote-facade.md), [Coarse-Grained Lock](./offline-concurrency/coarse-grained-lock.md), [Client Session State](./session-state/client-session-state.md), [Server Session State](./session-state/server-session-state.md), [Record Set](./base/record-set.md), [Layer Supertype](./base/layer-supertype.md), [Registry](./base/registry.md), [Value Object](./base/value-object.md), [Money](./base/money.md), [Special Case](./base/special-case.md)

### Extensibility (12)

[Domain Model](./domain-logic/domain-model.md), [Data Mapper](./data-source-architectural/data-mapper.md), [Inheritance Mappers](./object-relational-structural/inheritance-mappers.md), [Class Table Inheritance](./object-relational-structural/class-table-inheritance.md), [Metadata Mapping](./object-relational-metadata-mapping/metadata-mapping.md), [Query Object](./object-relational-metadata-mapping/query-object.md), [Model View Controller](./web-presentation/model-view-controller.md), [Front Controller](./web-presentation/front-controller.md), [Two Step View](./web-presentation/two-step-view.md), [Application Controller](./web-presentation/application-controller.md), [Mapper](./base/mapper.md), [Plugin](./base/plugin.md)

### Performance (14)

[Transaction Script](./domain-logic/transaction-script.md), [Table Module](./domain-logic/table-module.md), [Unit of Work](./object-relational-behavioral/unit-of-work.md), [Identity Map](./object-relational-behavioral/identity-map.md), [Lazy Load](./object-relational-behavioral/lazy-load.md), [Embedded Value](./object-relational-structural/embedded-value.md), [Serialized LOB](./object-relational-structural/serialized-lob.md), [Single Table Inheritance](./object-relational-structural/single-table-inheritance.md), [Concrete Table Inheritance](./object-relational-structural/concrete-table-inheritance.md), [Remote Facade](./distribution/remote-facade.md), [Data Transfer Object](./distribution/data-transfer-object.md), [Optimistic Offline Lock](./offline-concurrency/optimistic-offline-lock.md), [Server Session State](./session-state/server-session-state.md), [Record Set](./base/record-set.md)

### Consistency (17)

[Service Layer](./domain-logic/service-layer.md), [Unit of Work](./object-relational-behavioral/unit-of-work.md), [Identity Map](./object-relational-behavioral/identity-map.md), [Identity Field](./object-relational-structural/identity-field.md), [Foreign Key Mapping](./object-relational-structural/foreign-key-mapping.md), [Association Table Mapping](./object-relational-structural/association-table-mapping.md), [Class Table Inheritance](./object-relational-structural/class-table-inheritance.md), [Front Controller](./web-presentation/front-controller.md), [Two Step View](./web-presentation/two-step-view.md), [Optimistic Offline Lock](./offline-concurrency/optimistic-offline-lock.md), [Pessimistic Offline Lock](./offline-concurrency/pessimistic-offline-lock.md), [Coarse-Grained Lock](./offline-concurrency/coarse-grained-lock.md), [Implicit Lock](./offline-concurrency/implicit-lock.md), [Database Session State](./session-state/database-session-state.md), [Layer Supertype](./base/layer-supertype.md), [Value Object](./base/value-object.md), [Money](./base/money.md)

### Testability (16)

[Domain Model](./domain-logic/domain-model.md), [Service Layer](./domain-logic/service-layer.md), [Row Data Gateway](./data-source-architectural/row-data-gateway.md), [Data Mapper](./data-source-architectural/data-mapper.md), [Repository](./object-relational-metadata-mapping/repository.md), [Model View Controller](./web-presentation/model-view-controller.md), [Page Controller](./web-presentation/page-controller.md), [Transform View](./web-presentation/transform-view.md), [Application Controller](./web-presentation/application-controller.md), [Gateway](./base/gateway.md), [Service Stub](./base/service-stub.md), [Separated Interface](./base/separated-interface.md), [Registry](./base/registry.md), [Value Object](./base/value-object.md), [Special Case](./base/special-case.md), [Plugin](./base/plugin.md)
