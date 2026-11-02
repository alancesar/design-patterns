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
| [Bounded Context](./model-in-practice/bounded-context.md) | Um Bounded Context define explicitamente a fronteira dentro da qual um modelo de domínio específico se aplica. | [`Consistency`](/tags/consistency) [`Team Autonomy`](/tags/team-autonomy) [`Decoupling`](/tags/decoupling) |
| [Ubiquitous Language](./model-in-practice/ubiquitous-language.md) | A Ubiquitous Language é uma linguagem estruturada em torno do modelo de domínio e usada por todos os membros do time, especialistas de negócio e desenvolvedores, em todas as atividades: conversas, documentos, testes e código. | [`Shared Understanding`](/tags/shared-understanding) |
| [Continuous Integration](./model-in-practice/continuous-integration.md) | No DDD, Continuous Integration é o processo de integrar continuamente todo o trabalho feito dentro de um Bounded Context, para que o modelo permaneça coeso e todos os membros do time o entendam da mesma forma. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Model-Driven Design](./model-in-practice/model-driven-design.md) | Model-Driven Design é a ideia de que o modelo de domínio e o design do código devem estar intimamente ligados: o código é uma expressão do modelo, e uma mudança no código é uma mudança no modelo. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Hands-on Modelers](./model-in-practice/hands-on-modelers.md) | Hands-on Modelers é o princípio de que toda pessoa que contribui com o modelo deve também ter contato com o código, e toda pessoa que altera o código deve participar da conversa sobre o modelo. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Refactoring Toward Deeper Insight](./model-in-practice/refactoring-toward-deeper-insight.md) | Refactoring Toward Deeper Insight é a prática de refatorar o modelo e o código não apenas para limpar a implementação, mas para incorporar novo entendimento do domínio. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |

## Building Blocks (9) {#building-blocks}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Layered Architecture](./building-blocks/layered-architecture.md) | A Layered Architecture divide o sistema em camadas coesas, cada uma com uma responsabilidade bem definida e dependências que apontam em uma única direção. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Entity](./building-blocks/entity.md) | Uma Entity é um objeto do modelo definido principalmente por sua identidade, e não por seus atributos. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Value Object](../poeaa/base/value-object.md) ★ | O Value Object é um objeto pequeno e simples, como um valor monetário ou um intervalo de datas, cuja igualdade não se baseia em identidade. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Domain Event](../../architecture/microservices/service-collaboration/domain-event.md) ★ | Um evento de domínio (*Domain Event*), conceito vindo do Domain-Driven Design, é um fato relevante para o negócio que ocorreu no domínio, como `PedidoCriado` ou `CreditoReservado`. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Domain Service](./building-blocks/domain-service.md) | Um Domain Service (chamado de "Services" no livro de Evans) representa uma operação significativa do domínio que não pertence naturalmente a nenhuma entidade ou Value Object. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Module](./building-blocks/module.md) | Um Module (pacote ou namespace) agrupa conceitos do modelo que são coesos entre si, reduzindo a carga cognitiva de quem lê o código. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Aggregate](./building-blocks/aggregate.md) | Um Aggregate é um grupo de entidades e Value Objects tratado como uma unidade para fins de mudança de dados. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |
| [Repository](../poeaa/object-relational-metadata-mapping/repository.md) ★ | O Repository fica entre o domínio e a camada de mapeamento de dados e apresenta os objetos persistidos por meio de uma interface semelhante à de uma coleção em memória. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Factory](./building-blocks/factory.md) | No DDD, uma Factory encapsula o conhecimento necessário para criar objetos complexos ou agregados inteiros, mantendo essa responsabilidade fora do modelo principal. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |

## Supple Design (8) {#supple-design}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Intention-Revealing Interfaces](./supple-design/intention-revealing-interfaces.md) | Intention-Revealing Interfaces consiste em nomear classes, métodos e argumentos de modo que expressem o propósito e o efeito observável, e não o modo como o resultado é obtido. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) |
| [Side-Effect-Free Functions](./supple-design/side-effect-free-functions.md) | Side-Effect-Free Functions propõe separar as operações em duas categorias: comandos, que modificam o estado, e consultas, que apenas devolvem um resultado. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Assertions](./supple-design/assertions.md) | Assertions consiste em declarar explicitamente as pós-condições das operações e os invariantes das classes e dos Aggregates. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Standalone Classes](./supple-design/standalone-classes.md) | Standalone Classes propõe reduzir ao mínimo as dependências de cada classe, até que ela possa ser entendida e testada sozinha, sem referenciar outras classes além de tipos primitivos e de bibliotecas básicas da linguagem. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Closure of Operations](./supple-design/closure-of-operations.md) | Closure of Operations consiste em definir operações cujo tipo de retorno é o mesmo tipo de seus argumentos. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Declarative Design](./supple-design/declarative-design.md) | Declarative Design é um estilo em que o comportamento do software é controlado por uma especificação executável, que descreve propriedades e regras do domínio em vez de instruções passo a passo. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Drawing on Established Formalisms](./supple-design/drawing-on-established-formalisms.md) | Drawing on Established Formalisms consiste em reaproveitar, no modelo de domínio, um sistema conceitual maduro e bem compreendido, como contabilidade, álgebra, teoria dos conjuntos, lógica, cálculo de datas ou regras tributárias. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Conceptual Contours](./supple-design/conceptual-contours.md) | Conceptual Contours consiste em decompor o design em unidades coesas (operações, interfaces, classes e Aggregates) alinhadas aos contornos naturais do domínio. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |

## Context Mapping (10) {#context-mapping}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Context Map](./context-mapping/context-map.md) | O Context Map é uma visão global dos Bounded Contexts de um projeto e dos relacionamentos reais entre eles. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Partnership](./context-mapping/partnership.md) | Partnership é um relacionamento entre dois Bounded Contexts, e entre os times que os mantêm, em que o sucesso de um depende do sucesso do outro. | [`Team Autonomy`](/tags/team-autonomy) [`Shared Understanding`](/tags/shared-understanding) |
| [Shared Kernel](./context-mapping/shared-kernel.md) | O Shared Kernel é um subconjunto do modelo de domínio, e do código ou do esquema de dados associado, que dois ou mais times concordam em compartilhar. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Customer/Supplier Development](./context-mapping/customer-supplier-development.md) | No Customer/Supplier Development, dois contextos têm uma relação upstream/downstream em que o time upstream (fornecedor, supplier) atende às necessidades do time downstream (cliente, customer). | [`Team Autonomy`](/tags/team-autonomy) [`Shared Understanding`](/tags/shared-understanding) |
| [Conformist](./context-mapping/conformist.md) | No Conformist, o time downstream decide adotar integralmente o modelo do contexto upstream, sem tradução. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Anti-Corruption Layer](../../cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer.md) ★ | O Anti-Corruption Layer (camada anticorrupção) é uma fachada ou camada de adaptação colocada entre subsistemas que não compartilham a mesma semântica. | [`Operational Excellence`](/tags/operational-excellence) |
| [Open-host Service](./context-mapping/open-host-service.md) | O Open-host Service define um protocolo que dá acesso ao seu subsistema como um conjunto de serviços. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Published Language](./context-mapping/published-language.md) | A Published Language é uma linguagem bem documentada, compartilhada e capaz de expressar o domínio necessário, usada como meio de comunicação comum entre contextos. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Separate Ways](./context-mapping/separate-ways.md) | No Separate Ways, dois contextos decidem de forma explícita não se integrar. | [`Team Autonomy`](/tags/team-autonomy) [`Simplicity`](/tags/simplicity) |
| [Big Ball of Mud](./context-mapping/big-ball-of-mud.md) | Big Ball of Mud é o nome, cunhado por Brian Foote e Joseph Yoder, para um sistema sem estrutura perceptível: modelos misturados, fronteiras inconsistentes, dependências em todas as direções. | [`Consistency`](/tags/consistency) [`Strategic Focus`](/tags/strategic-focus) |

## Distillation (7) {#distillation}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Core Domain](./distillation/core-domain.md) | O Core Domain é a parte do modelo que é mais central para o sucesso do negócio: aquilo que diferencia a organização dos concorrentes e justifica a existência do software. | [`Strategic Focus`](/tags/strategic-focus) [`Simplicity`](/tags/simplicity) |
| [Generic Subdomains](./distillation/generic-subdomains.md) | Generic Subdomains são partes do modelo que não são o diferencial do negócio e nem são específicas dele: problemas que muitas organizações compartilham, como contabilidade, controle de acesso, agendamento ou notificações. | [`Strategic Focus`](/tags/strategic-focus) [`Simplicity`](/tags/simplicity) |
| [Domain Vision Statement](./distillation/domain-vision-statement.md) | O Domain Vision Statement é um documento curto, de uma página ou menos, que descreve o Core Domain e o valor que ele entrega, sem entrar em detalhes técnicos. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Highlighted Core](./distillation/highlighted-core.md) | O Highlighted Core torna o Core Domain fácil de encontrar dentro de um modelo grande, sem alterar a estrutura do código. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Cohesive Mechanisms](./distillation/cohesive-mechanisms.md) | Cohesive Mechanisms são mecanismos computacionais complexos, como algoritmos de grafos, motores de regras ou resolução de restrições, que se infiltram no modelo de domínio e o enchem de detalhes procedimentais. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Segregated Core](./distillation/segregated-core.md) | O Segregated Core é a reestruturação do modelo para separar fisicamente o Core Domain dos demais elementos, de modo que o core fique coeso e com poucas dependências. | [`Decoupling`](/tags/decoupling) [`Strategic Focus`](/tags/strategic-focus) |
| [Abstract Core](./distillation/abstract-core.md) | O Abstract Core é um módulo separado que contém os conceitos mais fundamentais do modelo, expressos como classes abstratas e interfaces. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |

## Large-scale Structure (5) {#large-scale-structure}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Evolving Order](./large-scale-structure/evolving-order.md) | Evolving Order é o princípio que guia todas as estruturas de larga escala do DDD: a estrutura global de um sistema não deve ser imposta de cima para baixo no início do projeto, e sim deixada evoluir junto com a aplicação. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |
| [System Metaphor](./large-scale-structure/system-metaphor.md) | System Metaphor é uma estrutura de larga escala em que uma analogia concreta e fácil de entender passa a organizar o design do sistema inteiro. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Responsibility Layers](./large-scale-structure/responsibility-layers.md) | Responsibility Layers é uma estrutura de larga escala em que o domínio inteiro é organizado em poucas camadas conceituais, cada uma com uma responsabilidade ampla e bem definida. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Knowledge Level](./large-scale-structure/knowledge-level.md) | Knowledge Level é uma estrutura de larga escala que separa o modelo em dois grupos de objetos: o nível operacional, que representa as coisas do dia a dia (contas, pedidos, empréstimos), e o nível de conhecimento, um conjunto de objetos que descreve e restringe a estrutura e o comportamento do primeiro (tipos de conta, regras de produto, políticas). | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Pluggable Component Framework](./large-scale-structure/pluggable-component-framework.md) | Pluggable Component Framework é uma estrutura de larga escala que surge quando um domínio maduro tem várias aplicações ou grupos de componentes que precisam interoperar. | [`Decoupling`](/tags/decoupling) [`Team Autonomy`](/tags/team-autonomy) |

## Por etiqueta

### Shared Understanding (22)

[Ubiquitous Language](./model-in-practice/ubiquitous-language.md), [Continuous Integration](./model-in-practice/continuous-integration.md), [Model-Driven Design](./model-in-practice/model-driven-design.md), [Hands-on Modelers](./model-in-practice/hands-on-modelers.md), [Entity](./building-blocks/entity.md), [Domain Service](./building-blocks/domain-service.md), [Module](./building-blocks/module.md), [Intention-Revealing Interfaces](./supple-design/intention-revealing-interfaces.md), [Assertions](./supple-design/assertions.md), [Declarative Design](./supple-design/declarative-design.md), [Drawing on Established Formalisms](./supple-design/drawing-on-established-formalisms.md), [Context Map](./context-mapping/context-map.md), [Partnership](./context-mapping/partnership.md), [Shared Kernel](./context-mapping/shared-kernel.md), [Customer/Supplier Development](./context-mapping/customer-supplier-development.md), [Conformist](./context-mapping/conformist.md), [Published Language](./context-mapping/published-language.md), [Domain Vision Statement](./distillation/domain-vision-statement.md), [Highlighted Core](./distillation/highlighted-core.md), [Abstract Core](./distillation/abstract-core.md), [System Metaphor](./large-scale-structure/system-metaphor.md), [Responsibility Layers](./large-scale-structure/responsibility-layers.md)

### Decoupling (13)

[Bounded Context](./model-in-practice/bounded-context.md), [Layered Architecture](./building-blocks/layered-architecture.md), [Aggregate](./building-blocks/aggregate.md), [Repository](../poeaa/object-relational-metadata-mapping/repository.md), [Standalone Classes](./supple-design/standalone-classes.md), [Closure of Operations](./supple-design/closure-of-operations.md), [Open-host Service](./context-mapping/open-host-service.md), [Published Language](./context-mapping/published-language.md), [Cohesive Mechanisms](./distillation/cohesive-mechanisms.md), [Segregated Core](./distillation/segregated-core.md), [Abstract Core](./distillation/abstract-core.md), [Responsibility Layers](./large-scale-structure/responsibility-layers.md), [Pluggable Component Framework](./large-scale-structure/pluggable-component-framework.md)

### Consistency (16)

[Bounded Context](./model-in-practice/bounded-context.md), [Continuous Integration](./model-in-practice/continuous-integration.md), [Model-Driven Design](./model-in-practice/model-driven-design.md), [Hands-on Modelers](./model-in-practice/hands-on-modelers.md), [Entity](./building-blocks/entity.md), [Value Object](../poeaa/base/value-object.md), [Aggregate](./building-blocks/aggregate.md), [Factory](./building-blocks/factory.md), [Side-Effect-Free Functions](./supple-design/side-effect-free-functions.md), [Assertions](./supple-design/assertions.md), [Drawing on Established Formalisms](./supple-design/drawing-on-established-formalisms.md), [Shared Kernel](./context-mapping/shared-kernel.md), [Big Ball of Mud](./context-mapping/big-ball-of-mud.md), [System Metaphor](./large-scale-structure/system-metaphor.md), [Responsibility Layers](./large-scale-structure/responsibility-layers.md), [Knowledge Level](./large-scale-structure/knowledge-level.md)

### Simplicity (21)

[Refactoring Toward Deeper Insight](./model-in-practice/refactoring-toward-deeper-insight.md), [Layered Architecture](./building-blocks/layered-architecture.md), [Value Object](../poeaa/base/value-object.md), [Domain Service](./building-blocks/domain-service.md), [Module](./building-blocks/module.md), [Factory](./building-blocks/factory.md), [Intention-Revealing Interfaces](./supple-design/intention-revealing-interfaces.md), [Side-Effect-Free Functions](./supple-design/side-effect-free-functions.md), [Standalone Classes](./supple-design/standalone-classes.md), [Closure of Operations](./supple-design/closure-of-operations.md), [Declarative Design](./supple-design/declarative-design.md), [Conceptual Contours](./supple-design/conceptual-contours.md), [Conformist](./context-mapping/conformist.md), [Open-host Service](./context-mapping/open-host-service.md), [Separate Ways](./context-mapping/separate-ways.md), [Core Domain](./distillation/core-domain.md), [Generic Subdomains](./distillation/generic-subdomains.md), [Cohesive Mechanisms](./distillation/cohesive-mechanisms.md), [Abstract Core](./distillation/abstract-core.md), [Evolving Order](./large-scale-structure/evolving-order.md), [Knowledge Level](./large-scale-structure/knowledge-level.md)

### Team Autonomy (5)

[Bounded Context](./model-in-practice/bounded-context.md), [Partnership](./context-mapping/partnership.md), [Customer/Supplier Development](./context-mapping/customer-supplier-development.md), [Separate Ways](./context-mapping/separate-ways.md), [Pluggable Component Framework](./large-scale-structure/pluggable-component-framework.md)

### Strategic Focus (10)

[Refactoring Toward Deeper Insight](./model-in-practice/refactoring-toward-deeper-insight.md), [Conceptual Contours](./supple-design/conceptual-contours.md), [Context Map](./context-mapping/context-map.md), [Big Ball of Mud](./context-mapping/big-ball-of-mud.md), [Core Domain](./distillation/core-domain.md), [Generic Subdomains](./distillation/generic-subdomains.md), [Domain Vision Statement](./distillation/domain-vision-statement.md), [Highlighted Core](./distillation/highlighted-core.md), [Segregated Core](./distillation/segregated-core.md), [Evolving Order](./large-scale-structure/evolving-order.md)

### Testability (2)

[Value Object](../poeaa/base/value-object.md), [Repository](../poeaa/object-relational-metadata-mapping/repository.md)

### Reliability (1)

[Domain Event](../../architecture/microservices/service-collaboration/domain-event.md)

### Operational Excellence (2)

[Domain Event](../../architecture/microservices/service-collaboration/domain-event.md), [Anti-Corruption Layer](../../cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer.md)
