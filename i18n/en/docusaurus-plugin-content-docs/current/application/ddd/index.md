---
title: "Domain-Driven Design"
sidebar_label: "DDD"
---

# Domain-Driven Design

Personal catalog based on Eric Evans's [DDD Reference](https://www.domainlanguage.com/ddd/reference/), the official summary of the *Domain-Driven Design* book (2003) with three later patterns (Domain Event, Partnership, and Big Ball of Mud). Each pattern has a description, the problems it solves, when to use it, trade-offs, tags, a Mermaid diagram, and an example (code or scenario).

Patterns marked with ★ are shared with another catalog: this catalog points to the original document, revised with content from this source.

Total: 45 patterns in 6 groups. Tags: Modeling goal.

## Groups

- [Putting the Model to Work](#model-in-practice) (6)
- [Building Blocks](#building-blocks) (9)
- [Supple Design](#supple-design) (8)
- [Context Mapping](#context-mapping) (10)
- [Distillation](#distillation) (7)
- [Large-scale Structure](#large-scale-structure) (5)

## Putting the Model to Work (6) {#model-in-practice}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Bounded Context](/application/ddd/model-in-practice/bounded-context) | A Bounded Context explicitly defines the boundary within which a specific domain model applies. | [`Consistency`](/tags/consistency) [`Team Autonomy`](/tags/team-autonomy) [`Decoupling`](/tags/decoupling) |
| [Ubiquitous Language](/application/ddd/model-in-practice/ubiquitous-language) | The Ubiquitous Language is a language structured around the domain model and used by every team member, business experts and developers alike, in all activities: conversations, documents, tests, and code. | [`Shared Understanding`](/tags/shared-understanding) |
| [Continuous Integration](/application/ddd/model-in-practice/continuous-integration) | In DDD, Continuous Integration is the process of continuously integrating all the work done within a Bounded Context, so the model stays cohesive and every team member understands it the same way. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Model-Driven Design](/application/ddd/model-in-practice/model-driven-design) | Model-Driven Design is the idea that the domain model and the code design must be closely tied: the code is an expression of the model, and a change in the code is a change in the model. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Hands-on Modelers](/application/ddd/model-in-practice/hands-on-modelers) | Hands-on Modelers is the principle that everyone who contributes to the model should also have contact with the code, and everyone who changes the code should take part in the conversation about the model. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Refactoring Toward Deeper Insight](/application/ddd/model-in-practice/refactoring-toward-deeper-insight) | Refactoring Toward Deeper Insight is the practice of refactoring the model and the code not just to clean up the implementation, but to incorporate new understanding of the domain. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |

## Building Blocks (9) {#building-blocks}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Layered Architecture](/application/ddd/building-blocks/layered-architecture) | Layered Architecture divides the system into cohesive layers, each with a well-defined responsibility and dependencies pointing in a single direction. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Entity](/application/ddd/building-blocks/entity) | An Entity is a model object defined primarily by its identity rather than its attributes. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Value Object](/application/poeaa/base/value-object) ★ | A Value Object is a small, simple object, such as a monetary amount or a date range, whose equality isn't based on identity. | [`Consistency`](/tags/consistency) [`Simplicity`](/tags/simplicity) [`Testability`](/tags/testability) |
| [Domain Event](/architecture/microservices/service-collaboration/domain-event) ★ | A *Domain Event*, a concept from Domain-Driven Design, is a business-relevant fact that occurred in the domain, such as `OrderCreated` or `CreditReserved`. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Domain Service](/application/ddd/building-blocks/domain-service) | A Domain Service (called "Services" in Evans's book) represents a significant domain operation that doesn't naturally belong to any entity or Value Object. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Module](/application/ddd/building-blocks/module) | A Module (package or namespace) groups model concepts that are cohesive with one another, reducing the cognitive load on whoever reads the code. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Aggregate](/application/ddd/building-blocks/aggregate) | An Aggregate is a group of entities and Value Objects treated as a single unit for purposes of data change. | [`Consistency`](/tags/consistency) [`Decoupling`](/tags/decoupling) |
| [Repository](/application/poeaa/object-relational-metadata-mapping/repository) ★ | A Repository sits between the domain and the data mapping layer and presents persisted objects through an interface similar to an in-memory collection. | [`Decoupling`](/tags/decoupling) [`Testability`](/tags/testability) |
| [Factory](/application/ddd/building-blocks/factory) | In DDD, a Factory encapsulates the knowledge needed to create complex objects or entire aggregates, keeping that responsibility out of the main model. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |

## Supple Design (8) {#supple-design}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Intention-Revealing Interfaces](/application/ddd/supple-design/intention-revealing-interfaces) | Intention-Revealing Interfaces means naming classes, methods, and arguments so that they express the purpose and the observable effect, not how the result is obtained. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) |
| [Side-Effect-Free Functions](/application/ddd/supple-design/side-effect-free-functions) | Side-Effect-Free Functions proposes separating operations into two categories: commands, which modify state, and queries, which only return a result. | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Assertions](/application/ddd/supple-design/assertions) | Assertions means explicitly declaring the postconditions of operations and the invariants of classes and Aggregates. | [`Consistency`](/tags/consistency) [`Shared Understanding`](/tags/shared-understanding) |
| [Standalone Classes](/application/ddd/supple-design/standalone-classes) | Standalone Classes proposes reducing each class's dependencies to a minimum, until it can be understood and tested on its own, without referencing other classes beyond primitive types and the language's basic libraries. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Closure of Operations](/application/ddd/supple-design/closure-of-operations) | Closure of Operations means defining operations whose return type is the same as the type of their arguments. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Declarative Design](/application/ddd/supple-design/declarative-design) | Declarative Design is a style in which the software's behavior is controlled by an executable specification that describes the domain's properties and rules instead of step-by-step instructions. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Drawing on Established Formalisms](/application/ddd/supple-design/drawing-on-established-formalisms) | Drawing on Established Formalisms means reusing, in the domain model, a mature and well-understood conceptual system, such as accounting, algebra, set theory, logic, date calculation, or tax rules. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Conceptual Contours](/application/ddd/supple-design/conceptual-contours) | Conceptual Contours means decomposing the design into cohesive units (operations, interfaces, classes, and Aggregates) aligned with the natural contours of the domain. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |

## Context Mapping (10) {#context-mapping}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Context Map](/application/ddd/context-mapping/context-map) | The Context Map is a global view of a project's Bounded Contexts and the actual relationships between them. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Partnership](/application/ddd/context-mapping/partnership) | Partnership is a relationship between two Bounded Contexts, and between the teams that maintain them, in which the success of one depends on the success of the other. | [`Team Autonomy`](/tags/team-autonomy) [`Shared Understanding`](/tags/shared-understanding) |
| [Shared Kernel](/application/ddd/context-mapping/shared-kernel) | A Shared Kernel is a subset of the domain model, and of the associated code or data schema, that two or more teams agree to share. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Customer/Supplier Development](/application/ddd/context-mapping/customer-supplier-development) | In Customer/Supplier Development, two contexts have an upstream/downstream relationship in which the upstream team (the supplier) serves the needs of the downstream team (the customer). | [`Team Autonomy`](/tags/team-autonomy) [`Shared Understanding`](/tags/shared-understanding) |
| [Conformist](/application/ddd/context-mapping/conformist) | In Conformist, the downstream team decides to fully adopt the upstream context's model, with no translation. | [`Simplicity`](/tags/simplicity) [`Shared Understanding`](/tags/shared-understanding) |
| [Anti-Corruption Layer](/cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) ★ | The Anti-Corruption Layer is a facade or adapter layer placed between subsystems that don't share the same semantics. | [`Operational Excellence`](/tags/operational-excellence) |
| [Open-host Service](/application/ddd/context-mapping/open-host-service) | Open-host Service defines a protocol that gives access to your subsystem as a set of services. | [`Decoupling`](/tags/decoupling) [`Simplicity`](/tags/simplicity) |
| [Published Language](/application/ddd/context-mapping/published-language) | A Published Language is a well-documented, shared language capable of expressing the necessary domain, used as a common means of communication between contexts. | [`Shared Understanding`](/tags/shared-understanding) [`Decoupling`](/tags/decoupling) |
| [Separate Ways](/application/ddd/context-mapping/separate-ways) | In Separate Ways, two contexts explicitly decide not to integrate. | [`Team Autonomy`](/tags/team-autonomy) [`Simplicity`](/tags/simplicity) |
| [Big Ball of Mud](/application/ddd/context-mapping/big-ball-of-mud) | Big Ball of Mud is the name, coined by Brian Foote and Joseph Yoder, for a system with no discernible structure: mixed models, inconsistent boundaries, dependencies in every direction. | [`Consistency`](/tags/consistency) [`Strategic Focus`](/tags/strategic-focus) |

## Distillation (7) {#distillation}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Core Domain](/application/ddd/distillation/core-domain) | The Core Domain is the part of the model that is most central to the business's success: what sets the organization apart from its competitors and justifies the software's existence. | [`Strategic Focus`](/tags/strategic-focus) [`Simplicity`](/tags/simplicity) |
| [Generic Subdomains](/application/ddd/distillation/generic-subdomains) | Generic Subdomains are parts of the model that are neither the business's differentiator nor specific to it: problems that many organizations share, such as accounting, access control, scheduling, or notifications. | [`Strategic Focus`](/tags/strategic-focus) [`Simplicity`](/tags/simplicity) |
| [Domain Vision Statement](/application/ddd/distillation/domain-vision-statement) | The Domain Vision Statement is a short document, a page or less, that describes the [Core Domain](/application/ddd/distillation/core-domain) and the value it delivers, without getting into technical details. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Highlighted Core](/application/ddd/distillation/highlighted-core) | The Highlighted Core makes the [Core Domain](/application/ddd/distillation/core-domain) easy to find within a large model, without changing the structure of the code. | [`Shared Understanding`](/tags/shared-understanding) [`Strategic Focus`](/tags/strategic-focus) |
| [Cohesive Mechanisms](/application/ddd/distillation/cohesive-mechanisms) | Cohesive Mechanisms are complex computational mechanisms, such as graph algorithms, rules engines, or constraint solving, that creep into the domain model and fill it with procedural detail. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |
| [Segregated Core](/application/ddd/distillation/segregated-core) | The Segregated Core is a restructuring of the model to physically separate the [Core Domain](/application/ddd/distillation/core-domain) from the other elements, so that the core is cohesive and has few dependencies. | [`Decoupling`](/tags/decoupling) [`Strategic Focus`](/tags/strategic-focus) |
| [Abstract Core](/application/ddd/distillation/abstract-core) | The Abstract Core is a separate module that holds the most fundamental concepts of the model, expressed as abstract classes and interfaces. | [`Shared Understanding`](/tags/shared-understanding) [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) |

## Large-scale Structure (5) {#large-scale-structure}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Evolving Order](/application/ddd/large-scale-structure/evolving-order) | Evolving Order is the principle that guides all of DDD's large-scale structures: a system's overall structure shouldn't be imposed top-down at the start of the project, but left to evolve along with the application. | [`Simplicity`](/tags/simplicity) [`Strategic Focus`](/tags/strategic-focus) |
| [System Metaphor](/application/ddd/large-scale-structure/system-metaphor) | System Metaphor is a large-scale structure in which a concrete, easy-to-understand analogy comes to organize the design of the whole system. | [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Responsibility Layers](/application/ddd/large-scale-structure/responsibility-layers) | Responsibility Layers is a large-scale structure in which the whole domain is organized into a few conceptual layers, each with a broad, well-defined responsibility. | [`Decoupling`](/tags/decoupling) [`Shared Understanding`](/tags/shared-understanding) [`Consistency`](/tags/consistency) |
| [Knowledge Level](/application/ddd/large-scale-structure/knowledge-level) | Knowledge Level is a large-scale structure that splits the model into two groups of objects: the operational level, which represents everyday things (accounts, orders, loans), and the knowledge level, a set of objects that describes and constrains the structure and behavior of the first (account types, product rules, policies). | [`Simplicity`](/tags/simplicity) [`Consistency`](/tags/consistency) |
| [Pluggable Component Framework](/application/ddd/large-scale-structure/pluggable-component-framework) | Pluggable Component Framework is a large-scale structure that emerges when a mature domain has several applications or groups of components that need to interoperate. | [`Decoupling`](/tags/decoupling) [`Team Autonomy`](/tags/team-autonomy) |

## By tag

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
