---
title: "Design Patterns (GoF and classics)"
sidebar_label: "GoF"
---

# Design Patterns (GoF and classics)

Personal catalog based on the [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet). Each pattern has a description, the problems it solves, when to use it, trade-offs, a Mermaid class diagram, and a code example. The tags indicate the design goal; the `origin` field indicates whether the pattern is one of the 23 from the *Design Patterns* (GoF) book or a complementary classic pattern.

Total: 28 patterns in 3 groups. Tags: Design goal.

## Groups

- [Creational](#creational) (8)
- [Structural](#structural) (8)
- [Behavioral](#behavioral) (12)

## Creational (8) {#creational}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [Abstract Factory](/coding/gof/creational/abstract-factory) | Abstract Factory provides an interface for creating families of related or dependent objects without specifying their concrete classes. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Builder](/coding/gof/creational/builder) | Builder separates the construction of a complex object from its representation, allowing the same construction process to produce different representations. | [`Encapsulation`](/tags/encapsulation) [`Simplicity`](/tags/simplicity) | GoF |
| [Factory Method](/coding/gof/creational/factory-method) | Factory Method defines an interface for creating an object, but lets subclasses decide which concrete class to instantiate. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Prototype](/coding/gof/creational/prototype) | Prototype specifies the kinds of objects to create using a prototypical instance, and creates new objects by copying (cloning) that prototype. | [`Resource Efficiency`](/tags/resource-efficiency) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Singleton](/coding/gof/creational/singleton) | Singleton ensures that a class has **a single instance** for the life of the application and provides a **global access point** to it. | [`Resource Efficiency`](/tags/resource-efficiency) | GoF |
| [Factory](/coding/gof/creational/factory) | Factory (also called Simple Factory) centralizes object creation at a single point: a class or method that receives a parameter (a type, a configuration, a string) and decides which concrete implementation to instantiate, returning it through a common interface or base class. | [`Decoupling`](/tags/decoupling) [`Encapsulation`](/tags/encapsulation) | Classic |
| [Object Pool](/coding/gof/creational/object-pool) | Object Pool keeps a set of objects that are already initialized and ready to use, instead of creating and destroying them on demand. | [`Resource Efficiency`](/tags/resource-efficiency) | Classic |
| [Telescoping Constructor](/coding/gof/creational/telescoping-constructor) | Telescoping Constructor is an object-creation technique in which a class offers a sequence of overloaded constructors, each accepting one more parameter than the previous one. | [`Simplicity`](/tags/simplicity) | Classic |

## Structural (8) {#structural}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [Adapter](/coding/gof/structural/adapter) | The Adapter (also known as Wrapper) converts the interface of a class into another interface the client expects. | [`Decoupling`](/tags/decoupling) | GoF |
| [Bridge](/coding/gof/structural/bridge) | The Bridge decouples an abstraction from its implementation so that the two can vary independently. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Composite](/coding/gof/structural/composite) | The Composite composes objects into tree structures to represent part-whole hierarchies. | [`Simplicity`](/tags/simplicity) [`Extensibility`](/tags/extensibility) | GoF |
| [Decorator](/coding/gof/structural/decorator) | The Decorator lets you add responsibilities to an object dynamically, at runtime, without changing its class and without resorting to inheritance. | [`Extensibility`](/tags/extensibility) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Facade](/coding/gof/structural/facade) | The Facade provides a single, simplified interface to a set of interfaces in a subsystem. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) | GoF |
| [Flyweight](/coding/gof/structural/flyweight) | The Flyweight reduces memory consumption when an application needs to hold a very large number of similar objects. | [`Resource Efficiency`](/tags/resource-efficiency) | GoF |
| [Proxy](/coding/gof/structural/proxy) | The Proxy provides a substitute (or stand-in) for another object, controlling access to it. | [`Encapsulation`](/tags/encapsulation) [`Resource Efficiency`](/tags/resource-efficiency) | GoF |
| [Private Class Data](/coding/gof/structural/private-class-data) | The Private Class Data restricts access to and modification of a class's attributes by separating them into a data object of their own (the `Data` class). | [`Encapsulation`](/tags/encapsulation) | Classic |

## Behavioral (12) {#behavioral}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility) | Chain of Responsibility avoids coupling the sender of a request to its receiver by giving more than one object a chance to handle it. | [`Decoupling`](/tags/decoupling) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Command](/coding/gof/behavioral/command) | Command encapsulates a request as an object, containing everything needed to execute it: the action, the object that performs it (the receiver), and the parameters. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Interpreter](/coding/gof/behavioral/interpreter) | Interpreter defines a representation for the grammar of a simple language and an interpreter that uses that representation to evaluate sentences in the language. | [`Extensibility`](/tags/extensibility) | GoF |
| [Iterator](/coding/gof/behavioral/iterator) | Iterator provides a way to access the elements of a collection (aggregate) sequentially without exposing its internal representation. | [`Encapsulation`](/tags/encapsulation) [`Simplicity`](/tags/simplicity) | GoF |
| [Mediator](/coding/gof/behavioral/mediator) | Mediator defines an object that encapsulates how a set of objects interact. | [`Decoupling`](/tags/decoupling) | GoF |
| [Memento](/coding/gof/behavioral/memento) | Memento captures and externalizes an object's internal state, without violating its encapsulation, so that the object can be restored to that state later. | [`Encapsulation`](/tags/encapsulation) | GoF |
| [Observer](/coding/gof/behavioral/observer) | Observer defines a one-to-many dependency between objects, so that when one object (the *subject*) changes state, all its dependents (the *observers*) are notified and updated automatically. | [`Decoupling`](/tags/decoupling) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [State](/coding/gof/behavioral/state) | State lets an object alter its behavior when its internal state changes, giving the impression that the object changed class. | [`Extensibility`](/tags/extensibility) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Strategy](/coding/gof/behavioral/strategy) | Strategy (also known as Policy) defines a family of algorithms, encapsulates each one in its own object, and makes them interchangeable. | [`Runtime Flexibility`](/tags/runtime-flexibility) [`Extensibility`](/tags/extensibility) | GoF |
| [Template Method](/coding/gof/behavioral/template-method) | Template Method defines the skeleton of an algorithm in an operation of a base class, deferring some steps to subclasses. | [`Extensibility`](/tags/extensibility) | GoF |
| [Visitor](/coding/gof/behavioral/visitor) | Visitor represents an operation to be performed on the elements of an object structure. | [`Extensibility`](/tags/extensibility) | GoF |
| [Null Object](/coding/gof/behavioral/null-object) | Null Object replaces null references with an object that implements the same interface the client expects, but whose behavior is neutral, that is, "do nothing". | [`Simplicity`](/tags/simplicity) | Classic |

## By tag

### Decoupling (10)

[Abstract Factory](/coding/gof/creational/abstract-factory), [Factory Method](/coding/gof/creational/factory-method), [Factory](/coding/gof/creational/factory), [Adapter](/coding/gof/structural/adapter), [Bridge](/coding/gof/structural/bridge), [Facade](/coding/gof/structural/facade), [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility), [Command](/coding/gof/behavioral/command), [Mediator](/coding/gof/behavioral/mediator), [Observer](/coding/gof/behavioral/observer)

### Extensibility (11)

[Abstract Factory](/coding/gof/creational/abstract-factory), [Factory Method](/coding/gof/creational/factory-method), [Bridge](/coding/gof/structural/bridge), [Composite](/coding/gof/structural/composite), [Decorator](/coding/gof/structural/decorator), [Command](/coding/gof/behavioral/command), [Interpreter](/coding/gof/behavioral/interpreter), [State](/coding/gof/behavioral/state), [Strategy](/coding/gof/behavioral/strategy), [Template Method](/coding/gof/behavioral/template-method), [Visitor](/coding/gof/behavioral/visitor)

### Runtime Flexibility (6)

[Prototype](/coding/gof/creational/prototype), [Decorator](/coding/gof/structural/decorator), [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility), [Observer](/coding/gof/behavioral/observer), [State](/coding/gof/behavioral/state), [Strategy](/coding/gof/behavioral/strategy)

### Encapsulation (6)

[Builder](/coding/gof/creational/builder), [Factory](/coding/gof/creational/factory), [Proxy](/coding/gof/structural/proxy), [Private Class Data](/coding/gof/structural/private-class-data), [Iterator](/coding/gof/behavioral/iterator), [Memento](/coding/gof/behavioral/memento)

### Resource Efficiency (5)

[Prototype](/coding/gof/creational/prototype), [Singleton](/coding/gof/creational/singleton), [Object Pool](/coding/gof/creational/object-pool), [Flyweight](/coding/gof/structural/flyweight), [Proxy](/coding/gof/structural/proxy)

### Simplicity (6)

[Builder](/coding/gof/creational/builder), [Telescoping Constructor](/coding/gof/creational/telescoping-constructor), [Composite](/coding/gof/structural/composite), [Facade](/coding/gof/structural/facade), [Iterator](/coding/gof/behavioral/iterator), [Null Object](/coding/gof/behavioral/null-object)
