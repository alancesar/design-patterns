---
title: "Design Patterns (GoF e clássicos)"
sidebar_label: "GoF"
---

# Design Patterns (GoF e clássicos)

Catálogo pessoal baseado no [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet). Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, diagrama de classes Mermaid e um exemplo de código. As etiquetas indicam o objetivo de design; o campo `origin` indica se o padrão é um dos 23 do livro *Design Patterns* (GoF) ou um padrão clássico complementar.

Total: 28 padrões em 3 grupos. Etiquetas: Objetivo de design.

## Grupos

- [Creational](#creational) (8)
- [Structural](#structural) (8)
- [Behavioral](#behavioral) (12)

## Creational (8) {#creational}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [Abstract Factory](/coding/gof/creational/abstract-factory) | O Abstract Factory fornece uma interface para criar famílias de objetos relacionados ou dependentes sem especificar suas classes concretas. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Builder](/coding/gof/creational/builder) | O Builder separa a construção de um objeto complexo da sua representação, permitindo que o mesmo processo de construção produza representações diferentes. | [`Encapsulation`](/tags/encapsulation) [`Simplicity`](/tags/simplicity) | GoF |
| [Factory Method](/coding/gof/creational/factory-method) | O Factory Method define uma interface para criar um objeto, mas deixa que as subclasses decidam qual classe concreta instanciar. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Prototype](/coding/gof/creational/prototype) | O Prototype especifica os tipos de objetos a serem criados por meio de uma instância-protótipo e cria novos objetos copiando (clonando) esse protótipo. | [`Resource Efficiency`](/tags/resource-efficiency) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Singleton](/coding/gof/creational/singleton) | O Singleton garante que uma classe tenha **uma única instância** durante a vida da aplicação e fornece um **ponto de acesso global** a ela. | [`Resource Efficiency`](/tags/resource-efficiency) | GoF |
| [Factory](/coding/gof/creational/factory) | O Factory (também chamado de Simple Factory) centraliza a criação de objetos em um único ponto: uma classe ou método que recebe um parâmetro (um tipo, uma configuração, uma string) e decide qual implementação concreta instanciar, devolvendo-a por meio de uma interface ou classe base comum. | [`Decoupling`](/tags/decoupling) [`Encapsulation`](/tags/encapsulation) | Classic |
| [Object Pool](/coding/gof/creational/object-pool) | O Object Pool mantém um conjunto de objetos já inicializados e prontos para uso, em vez de criá-los e destruí-los sob demanda. | [`Resource Efficiency`](/tags/resource-efficiency) | Classic |
| [Telescoping Constructor](/coding/gof/creational/telescoping-constructor) | O Telescoping Constructor é uma técnica de criação de objetos em que uma classe oferece uma sequência de construtores sobrecarregados, cada um aceitando um parâmetro a mais que o anterior. | [`Simplicity`](/tags/simplicity) | Classic |

## Structural (8) {#structural}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [Adapter](/coding/gof/structural/adapter) | O Adapter (também conhecido como Wrapper) converte a interface de uma classe em outra interface que o cliente espera. | [`Decoupling`](/tags/decoupling) | GoF |
| [Bridge](/coding/gof/structural/bridge) | O Bridge desacopla uma abstração da sua implementação para que ambas possam variar de forma independente. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Composite](/coding/gof/structural/composite) | O Composite compõe objetos em estruturas de árvore para representar hierarquias parte-todo. | [`Simplicity`](/tags/simplicity) [`Extensibility`](/tags/extensibility) | GoF |
| [Decorator](/coding/gof/structural/decorator) | O Decorator permite adicionar responsabilidades a um objeto de forma dinâmica, em tempo de execução, sem alterar sua classe e sem recorrer à herança. | [`Extensibility`](/tags/extensibility) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Facade](/coding/gof/structural/facade) | O Facade oferece uma interface única e simplificada para um conjunto de interfaces de um subsistema. | [`Simplicity`](/tags/simplicity) [`Decoupling`](/tags/decoupling) | GoF |
| [Flyweight](/coding/gof/structural/flyweight) | O Flyweight reduz o consumo de memória quando uma aplicação precisa manter um número muito grande de objetos parecidos. | [`Resource Efficiency`](/tags/resource-efficiency) | GoF |
| [Proxy](/coding/gof/structural/proxy) | O Proxy fornece um substituto (ou representante) para outro objeto, controlando o acesso a ele. | [`Encapsulation`](/tags/encapsulation) [`Resource Efficiency`](/tags/resource-efficiency) | GoF |
| [Private Class Data](/coding/gof/structural/private-class-data) | O Private Class Data restringe o acesso e a modificação dos atributos de uma classe ao separá-los em um objeto de dados próprio (a classe `Data`). | [`Encapsulation`](/tags/encapsulation) | Classic |

## Behavioral (12) {#behavioral}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility) | O Chain of Responsibility evita acoplar o remetente de uma requisição ao seu receptor, dando a mais de um objeto a chance de tratá-la. | [`Decoupling`](/tags/decoupling) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Command](/coding/gof/behavioral/command) | O Command encapsula uma solicitação como um objeto, contendo tudo o que é necessário para executá-la: a ação, o objeto que a realiza (o receptor) e os parâmetros. | [`Decoupling`](/tags/decoupling) [`Extensibility`](/tags/extensibility) | GoF |
| [Interpreter](/coding/gof/behavioral/interpreter) | O Interpreter define uma representação para a gramática de uma linguagem simples e um interpretador que usa essa representação para avaliar sentenças da linguagem. | [`Extensibility`](/tags/extensibility) | GoF |
| [Iterator](/coding/gof/behavioral/iterator) | O Iterator fornece uma forma de acessar sequencialmente os elementos de uma coleção (agregado) sem expor sua representação interna. | [`Encapsulation`](/tags/encapsulation) [`Simplicity`](/tags/simplicity) | GoF |
| [Mediator](/coding/gof/behavioral/mediator) | O Mediator define um objeto que encapsula a forma como um conjunto de objetos interage. | [`Decoupling`](/tags/decoupling) | GoF |
| [Memento](/coding/gof/behavioral/memento) | O Memento captura e externaliza o estado interno de um objeto, sem violar seu encapsulamento, para que esse objeto possa ser restaurado a esse estado mais tarde. | [`Encapsulation`](/tags/encapsulation) | GoF |
| [Observer](/coding/gof/behavioral/observer) | O Observer define uma dependência um-para-muitos entre objetos, de modo que, quando um objeto (o *subject*) muda de estado, todos os seus dependentes (os *observers*) são notificados e atualizados automaticamente. | [`Decoupling`](/tags/decoupling) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [State](/coding/gof/behavioral/state) | O State permite que um objeto altere seu comportamento quando seu estado interno muda, dando a impressão de que o objeto mudou de classe. | [`Extensibility`](/tags/extensibility) [`Runtime Flexibility`](/tags/runtime-flexibility) | GoF |
| [Strategy](/coding/gof/behavioral/strategy) | O Strategy (também conhecido como Policy) define uma família de algoritmos, encapsula cada um deles em um objeto próprio e os torna intercambiáveis. | [`Runtime Flexibility`](/tags/runtime-flexibility) [`Extensibility`](/tags/extensibility) | GoF |
| [Template Method](/coding/gof/behavioral/template-method) | O Template Method define o esqueleto de um algoritmo em uma operação de uma classe base, delegando alguns passos para as subclasses. | [`Extensibility`](/tags/extensibility) | GoF |
| [Visitor](/coding/gof/behavioral/visitor) | O Visitor representa uma operação a ser executada sobre os elementos de uma estrutura de objetos. | [`Extensibility`](/tags/extensibility) | GoF |
| [Null Object](/coding/gof/behavioral/null-object) | O Null Object substitui referências nulas por um objeto que implementa a mesma interface esperada pelo cliente, mas cujo comportamento é neutro, ou seja, "não fazer nada". | [`Simplicity`](/tags/simplicity) | Classic |

## Por etiqueta

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
