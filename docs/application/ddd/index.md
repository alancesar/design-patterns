---
title: "Domain-Driven Design"
sidebar_label: "DDD"
---

# Domain-Driven Design

Catálogo pessoal baseado no [DDD Reference](https://www.domainlanguage.com/ddd/reference/), de Eric Evans, resumo oficial do livro *Domain-Driven Design* (2003) com três padrões posteriores (Domain Event, Partnership e Big Ball of Mud). Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas, um diagrama Mermaid e um exemplo (código ou cenário).

Padrões marcados com ★ são compartilhados com outro catálogo: este catálogo aponta para o documento original, revisado com o conteúdo desta fonte.

Total: 45 padrões em 6 grupos. Etiquetas: Objetivo de modelagem.

## Grupos

- [Putting the Model to Work](#model-in-practice) (6)
- [Building Blocks](#building-blocks) (9)
- [Supple Design](#supple-design) (8)
- [Context Mapping](#context-mapping) (10)
- [Distillation](#distillation) (7)
- [Large-scale Structure](#large-scale-structure) (5)

## Putting the Model to Work (6) {#model-in-practice}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Bounded Context](/application/ddd/model-in-practice/bounded-context) | Um Bounded Context define explicitamente a fronteira dentro da qual um modelo de domínio específico se aplica. | [`Consistency`](/tags/consistency) [`Team Autonomy`](/tags/team-autonomy) [`Decoupling`](/tags/decoupling) |
| [Ubiquitous Language](/application/ddd/model-in-practice/ubiquitous-language) | A Ubiquitous Language é uma linguagem estruturada em torno do modelo de domínio e usada por todos os membros do time, especialistas de negócio e desenvolvedores, em todas as atividades: conversas, documentos, testes e código. | [`Shared Understanding`](/tags/shared-understanding) |
| [Continuous Integration](/application/ddd/model-in-practice/continuous-integration) | No DDD, Continuous Integration é o processo de integrar continuamente todo o trabalho feito dentro de um Bounded Context, para que o modelo permaneça coeso e todos os membros do time o entendam da mesma forma. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Model-Driven Design](/application/ddd/model-in-practice/model-driven-design) | Model-Driven Design é a ideia de que o modelo de domínio e o design do código devem estar intimamente ligados: o código é uma expressão do modelo, e uma mudança no código é uma mudança no modelo. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Hands-on Modelers](/application/ddd/model-in-practice/hands-on-modelers) | Hands-on Modelers é o princípio de que toda pessoa que contribui com o modelo deve também ter contato com o código, e toda pessoa que altera o código deve participar da conversa sobre o modelo. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Refactoring Toward Deeper Insight](/application/ddd/model-in-practice/refactoring-toward-deeper-insight) | Refactoring Toward Deeper Insight é a prática de refatorar o modelo e o código não apenas para limpar a implementação, mas para incorporar novo entendimento do domínio. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |

## Building Blocks (9) {#building-blocks}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Layered Architecture](/application/ddd/building-blocks/layered-architecture) | A Layered Architecture divide o sistema em camadas coesas, cada uma com uma responsabilidade bem definida e dependências que apontam em uma única direção. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Entity](/application/ddd/building-blocks/entity) | Uma Entity é um objeto do modelo definido principalmente por sua identidade, e não por seus atributos. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Value Object](/application/poeaa/base/value-object) ★ | O Value Object é um objeto pequeno e simples, como um valor monetário ou um intervalo de datas, cuja igualdade não se baseia em identidade. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Domain Event](/architecture/microservices/service-collaboration/domain-event) ★ | Um evento de domínio (*Domain Event*), conceito vindo do Domain-Driven Design, é um fato relevante para o negócio que ocorreu no domínio, como `PedidoCriado` ou `CreditoReservado`. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Domain Service](/application/ddd/building-blocks/domain-service) | Um Domain Service (chamado de "Services" no livro de Evans) representa uma operação significativa do domínio que não pertence naturalmente a nenhuma entidade ou Value Object. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Module](/application/ddd/building-blocks/module) | Um Module (pacote ou namespace) agrupa conceitos do modelo que são coesos entre si, reduzindo a carga cognitiva de quem lê o código. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Aggregate](/application/ddd/building-blocks/aggregate) | Um Aggregate é um grupo de entidades e Value Objects tratado como uma unidade para fins de mudança de dados. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |
| [Repository](/application/poeaa/object-relational-metadata-mapping/repository) ★ | O Repository fica entre o domínio e a camada de mapeamento de dados e apresenta os objetos persistidos por meio de uma interface semelhante à de uma coleção em memória. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Factory](/application/ddd/building-blocks/factory) | No DDD, uma Factory encapsula o conhecimento necessário para criar objetos complexos ou agregados inteiros, mantendo essa responsabilidade fora do modelo principal. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |

## Supple Design (8) {#supple-design}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Intention-Revealing Interfaces](/application/ddd/supple-design/intention-revealing-interfaces) | Intention-Revealing Interfaces consiste em nomear classes, métodos e argumentos de modo que expressem o propósito e o efeito observável, e não o modo como o resultado é obtido. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) |
| [Side-Effect-Free Functions](/application/ddd/supple-design/side-effect-free-functions) | Side-Effect-Free Functions propõe separar as operações em duas categorias: comandos, que modificam o estado, e consultas, que apenas devolvem um resultado. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Assertions](/application/ddd/supple-design/assertions) | Assertions consiste em declarar explicitamente as pós-condições das operações e os invariantes das classes e dos Aggregates. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Standalone Classes](/application/ddd/supple-design/standalone-classes) | Standalone Classes propõe reduzir ao mínimo as dependências de cada classe, até que ela possa ser entendida e testada sozinha, sem referenciar outras classes além de tipos primitivos e de bibliotecas básicas da linguagem. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Closure of Operations](/application/ddd/supple-design/closure-of-operations) | Closure of Operations consiste em definir operações cujo tipo de retorno é o mesmo tipo de seus argumentos. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Declarative Design](/application/ddd/supple-design/declarative-design) | Declarative Design é um estilo em que o comportamento do software é controlado por uma especificação executável, que descreve propriedades e regras do domínio em vez de instruções passo a passo. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Drawing on Established Formalisms](/application/ddd/supple-design/drawing-on-established-formalisms) | Drawing on Established Formalisms consiste em reaproveitar, no modelo de domínio, um sistema conceitual maduro e bem compreendido, como contabilidade, álgebra, teoria dos conjuntos, lógica, cálculo de datas ou regras tributárias. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Conceptual Contours](/application/ddd/supple-design/conceptual-contours) | Conceptual Contours consiste em decompor o design em unidades coesas (operações, interfaces, classes e Aggregates) alinhadas aos contornos naturais do domínio. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |

## Context Mapping (10) {#context-mapping}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Context Map](/application/ddd/context-mapping/context-map) | O Context Map é uma visão global dos Bounded Contexts de um projeto e dos relacionamentos reais entre eles. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Partnership](/application/ddd/context-mapping/partnership) | Partnership é um relacionamento entre dois Bounded Contexts, e entre os times que os mantêm, em que o sucesso de um depende do sucesso do outro. | [`Team Autonomy`](/tags/team-autonomy) [`Shared Understanding`](/tags/shared-understanding) |
| [Shared Kernel](/application/ddd/context-mapping/shared-kernel) | O Shared Kernel é um subconjunto do modelo de domínio, e do código ou do esquema de dados associado, que dois ou mais times concordam em compartilhar. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Customer/Supplier Development](/application/ddd/context-mapping/customer-supplier-development) | No Customer/Supplier Development, dois contextos têm uma relação upstream/downstream em que o time upstream (fornecedor, supplier) atende às necessidades do time downstream (cliente, customer). | [`Team Autonomy`](/tags/team-autonomy) [`Shared Understanding`](/tags/shared-understanding) |
| [Conformist](/application/ddd/context-mapping/conformist) | No Conformist, o time downstream decide adotar integralmente o modelo do contexto upstream, sem tradução. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Anti-Corruption Layer](/cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) ★ | O Anti-Corruption Layer (camada anticorrupção) é uma fachada ou camada de adaptação colocada entre subsistemas que não compartilham a mesma semântica. | [`Operational Excellence`](/tags/operational-excellence) |
| [Open-host Service](/application/ddd/context-mapping/open-host-service) | O Open-host Service define um protocolo que dá acesso ao seu subsistema como um conjunto de serviços. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Published Language](/application/ddd/context-mapping/published-language) | A Published Language é uma linguagem bem documentada, compartilhada e capaz de expressar o domínio necessário, usada como meio de comunicação comum entre contextos. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Separate Ways](/application/ddd/context-mapping/separate-ways) | No Separate Ways, dois contextos decidem de forma explícita não se integrar. | [`Team Autonomy`](/tags/team-autonomy) [`Simplicity`](/tags/simplicity) |
| [Big Ball of Mud](/application/ddd/context-mapping/big-ball-of-mud) | Big Ball of Mud é o nome, cunhado por Brian Foote e Joseph Yoder, para um sistema sem estrutura perceptível: modelos misturados, fronteiras inconsistentes, dependências em todas as direções. | [`Consistency`](/tags/consistency) [`Strategic Focus`](/tags/strategic-focus) |

## Distillation (7) {#distillation}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Core Domain](/application/ddd/distillation/core-domain) | O Core Domain é a parte do modelo que é mais central para o sucesso do negócio: aquilo que diferencia a organização dos concorrentes e justifica a existência do software. | [`Strategic Focus`](/tags/strategic-focus) [`Simplicity`](/tags/simplicity) |
| [Generic Subdomains](/application/ddd/distillation/generic-subdomains) | Generic Subdomains são partes do modelo que não são o diferencial do negócio e nem são específicas dele: problemas que muitas organizações compartilham, como contabilidade, controle de acesso, agendamento ou notificações. | [`Strategic Focus`](/tags/strategic-focus) [`Simplicity`](/tags/simplicity) |
| [Domain Vision Statement](/application/ddd/distillation/domain-vision-statement) | O Domain Vision Statement é um documento curto, de uma página ou menos, que descreve o Core Domain e o valor que ele entrega, sem entrar em detalhes técnicos. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Highlighted Core](/application/ddd/distillation/highlighted-core) | O Highlighted Core torna o Core Domain fácil de encontrar dentro de um modelo grande, sem alterar a estrutura do código. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Cohesive Mechanisms](/application/ddd/distillation/cohesive-mechanisms) | Cohesive Mechanisms são mecanismos computacionais complexos, como algoritmos de grafos, motores de regras ou resolução de restrições, que se infiltram no modelo de domínio e o enchem de detalhes procedimentais. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Segregated Core](/application/ddd/distillation/segregated-core) | O Segregated Core é a reestruturação do modelo para separar fisicamente o Core Domain dos demais elementos, de modo que o core fique coeso e com poucas dependências. | [`Decoupling`](/tags/decoupling) [`Strategic Focus`](/tags/strategic-focus) |
| [Abstract Core](/application/ddd/distillation/abstract-core) | O Abstract Core é um módulo separado que contém os conceitos mais fundamentais do modelo, expressos como classes abstratas e interfaces. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |

## Large-scale Structure (5) {#large-scale-structure}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Evolving Order](/application/ddd/large-scale-structure/evolving-order) | Evolving Order é o princípio que guia todas as estruturas de larga escala do DDD: a estrutura global de um sistema não deve ser imposta de cima para baixo no início do projeto, e sim deixada evoluir junto com a aplicação. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |
| [System Metaphor](/application/ddd/large-scale-structure/system-metaphor) | System Metaphor é uma estrutura de larga escala em que uma analogia concreta e fácil de entender passa a organizar o design do sistema inteiro. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Responsibility Layers](/application/ddd/large-scale-structure/responsibility-layers) | Responsibility Layers é uma estrutura de larga escala em que o domínio inteiro é organizado em poucas camadas conceituais, cada uma com uma responsabilidade ampla e bem definida. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Knowledge Level](/application/ddd/large-scale-structure/knowledge-level) | Knowledge Level é uma estrutura de larga escala que separa o modelo em dois grupos de objetos: o nível operacional, que representa as coisas do dia a dia (contas, pedidos, empréstimos), e o nível de conhecimento, um conjunto de objetos que descreve e restringe a estrutura e o comportamento do primeiro (tipos de conta, regras de produto, políticas). | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Pluggable Component Framework](/application/ddd/large-scale-structure/pluggable-component-framework) | Pluggable Component Framework é uma estrutura de larga escala que surge quando um domínio maduro tem várias aplicações ou grupos de componentes que precisam interoperar. | [`Decoupling`](/tags/decoupling) [`Team Autonomy`](/tags/team-autonomy) |

## Por etiqueta

### Shared Understanding (22)

[Ubiquitous Language](/application/ddd/model-in-practice/ubiquitous-language), [Continuous Integration](/application/ddd/model-in-practice/continuous-integration), [Model-Driven Design](/application/ddd/model-in-practice/model-driven-design), [Hands-on Modelers](/application/ddd/model-in-practice/hands-on-modelers), [Entity](/application/ddd/building-blocks/entity), [Domain Service](/application/ddd/building-blocks/domain-service), [Module](/application/ddd/building-blocks/module), [Intention-Revealing Interfaces](/application/ddd/supple-design/intention-revealing-interfaces), [Assertions](/application/ddd/supple-design/assertions), [Declarative Design](/application/ddd/supple-design/declarative-design), [Drawing on Established Formalisms](/application/ddd/supple-design/drawing-on-established-formalisms), [Context Map](/application/ddd/context-mapping/context-map), [Partnership](/application/ddd/context-mapping/partnership), [Shared Kernel](/application/ddd/context-mapping/shared-kernel), [Customer/Supplier Development](/application/ddd/context-mapping/customer-supplier-development), [Conformist](/application/ddd/context-mapping/conformist), [Published Language](/application/ddd/context-mapping/published-language), [Domain Vision Statement](/application/ddd/distillation/domain-vision-statement), [Highlighted Core](/application/ddd/distillation/highlighted-core), [Abstract Core](/application/ddd/distillation/abstract-core), [System Metaphor](/application/ddd/large-scale-structure/system-metaphor), [Responsibility Layers](/application/ddd/large-scale-structure/responsibility-layers)

### Decoupling (13)

[Bounded Context](/application/ddd/model-in-practice/bounded-context), [Layered Architecture](/application/ddd/building-blocks/layered-architecture), [Aggregate](/application/ddd/building-blocks/aggregate), [Repository](/application/poeaa/object-relational-metadata-mapping/repository), [Standalone Classes](/application/ddd/supple-design/standalone-classes), [Closure of Operations](/application/ddd/supple-design/closure-of-operations), [Open-host Service](/application/ddd/context-mapping/open-host-service), [Published Language](/application/ddd/context-mapping/published-language), [Cohesive Mechanisms](/application/ddd/distillation/cohesive-mechanisms), [Segregated Core](/application/ddd/distillation/segregated-core), [Abstract Core](/application/ddd/distillation/abstract-core), [Responsibility Layers](/application/ddd/large-scale-structure/responsibility-layers), [Pluggable Component Framework](/application/ddd/large-scale-structure/pluggable-component-framework)

### Consistency (16)

[Bounded Context](/application/ddd/model-in-practice/bounded-context), [Continuous Integration](/application/ddd/model-in-practice/continuous-integration), [Model-Driven Design](/application/ddd/model-in-practice/model-driven-design), [Hands-on Modelers](/application/ddd/model-in-practice/hands-on-modelers), [Entity](/application/ddd/building-blocks/entity), [Value Object](/application/poeaa/base/value-object), [Aggregate](/application/ddd/building-blocks/aggregate), [Factory](/application/ddd/building-blocks/factory), [Side-Effect-Free Functions](/application/ddd/supple-design/side-effect-free-functions), [Assertions](/application/ddd/supple-design/assertions), [Drawing on Established Formalisms](/application/ddd/supple-design/drawing-on-established-formalisms), [Shared Kernel](/application/ddd/context-mapping/shared-kernel), [Big Ball of Mud](/application/ddd/context-mapping/big-ball-of-mud), [System Metaphor](/application/ddd/large-scale-structure/system-metaphor), [Responsibility Layers](/application/ddd/large-scale-structure/responsibility-layers), [Knowledge Level](/application/ddd/large-scale-structure/knowledge-level)

### Simplicity (21)

[Refactoring Toward Deeper Insight](/application/ddd/model-in-practice/refactoring-toward-deeper-insight), [Layered Architecture](/application/ddd/building-blocks/layered-architecture), [Value Object](/application/poeaa/base/value-object), [Domain Service](/application/ddd/building-blocks/domain-service), [Module](/application/ddd/building-blocks/module), [Factory](/application/ddd/building-blocks/factory), [Intention-Revealing Interfaces](/application/ddd/supple-design/intention-revealing-interfaces), [Side-Effect-Free Functions](/application/ddd/supple-design/side-effect-free-functions), [Standalone Classes](/application/ddd/supple-design/standalone-classes), [Closure of Operations](/application/ddd/supple-design/closure-of-operations), [Declarative Design](/application/ddd/supple-design/declarative-design), [Conceptual Contours](/application/ddd/supple-design/conceptual-contours), [Conformist](/application/ddd/context-mapping/conformist), [Open-host Service](/application/ddd/context-mapping/open-host-service), [Separate Ways](/application/ddd/context-mapping/separate-ways), [Core Domain](/application/ddd/distillation/core-domain), [Generic Subdomains](/application/ddd/distillation/generic-subdomains), [Cohesive Mechanisms](/application/ddd/distillation/cohesive-mechanisms), [Abstract Core](/application/ddd/distillation/abstract-core), [Evolving Order](/application/ddd/large-scale-structure/evolving-order), [Knowledge Level](/application/ddd/large-scale-structure/knowledge-level)

### Team Autonomy (5)

[Bounded Context](/application/ddd/model-in-practice/bounded-context), [Partnership](/application/ddd/context-mapping/partnership), [Customer/Supplier Development](/application/ddd/context-mapping/customer-supplier-development), [Separate Ways](/application/ddd/context-mapping/separate-ways), [Pluggable Component Framework](/application/ddd/large-scale-structure/pluggable-component-framework)

### Strategic Focus (10)

[Refactoring Toward Deeper Insight](/application/ddd/model-in-practice/refactoring-toward-deeper-insight), [Conceptual Contours](/application/ddd/supple-design/conceptual-contours), [Context Map](/application/ddd/context-mapping/context-map), [Big Ball of Mud](/application/ddd/context-mapping/big-ball-of-mud), [Core Domain](/application/ddd/distillation/core-domain), [Generic Subdomains](/application/ddd/distillation/generic-subdomains), [Domain Vision Statement](/application/ddd/distillation/domain-vision-statement), [Highlighted Core](/application/ddd/distillation/highlighted-core), [Segregated Core](/application/ddd/distillation/segregated-core), [Evolving Order](/application/ddd/large-scale-structure/evolving-order)

### Testability (2)

[Value Object](/application/poeaa/base/value-object), [Repository](/application/poeaa/object-relational-metadata-mapping/repository)

### Reliability (1)

[Domain Event](/architecture/microservices/service-collaboration/domain-event)

### Operational Excellence (2)

[Domain Event](/architecture/microservices/service-collaboration/domain-event), [Anti-Corruption Layer](/cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer)
