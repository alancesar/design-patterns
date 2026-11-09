---
title: Visitor
pattern_slug: visitor
category: Behavioral
tags:
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Visitor"
---

# Visitor

## Descrição

O Visitor representa uma operação a ser executada sobre os elementos de uma estrutura de objetos. Ele permite definir novas operações sem alterar as classes dos elementos sobre os quais opera, movendo cada operação para um objeto separado, o visitante.

Cada elemento da estrutura expõe um método `accept(visitor)`, que apenas chama de volta o método do visitante correspondente ao seu tipo concreto (por exemplo, `visitor.visitCircle(this)`). Essa técnica, chamada de *double dispatch*, faz com que o código executado dependa tanto do tipo do visitante quanto do tipo do elemento, sem `instanceof` nem `switch` sobre tipos.

Assim, cada nova operação vira uma nova classe `ConcreteVisitor` que reúne, em um só lugar, o comportamento para todos os tipos de elemento. O padrão é especialmente útil em hierarquias estáveis, como árvores sintáticas (AST), documentos e modelos de domínio, sobre as quais muitas operações diferentes são aplicadas.

## Problemas que resolve

- Necessidade de adicionar novas operações (exportação, validação, cálculo, renderização) a uma hierarquia de classes sem modificá-la a cada nova funcionalidade
- Lógica de uma mesma operação espalhada por várias classes de elementos, dificultando entendimento e manutenção
- Cadeias de `if/else` ou `switch` com verificações de tipo (`instanceof`) para decidir o que fazer com cada elemento
- Classes de domínio poluídas com responsabilidades não relacionadas ao seu propósito principal
- Acúmulo de estado ao percorrer uma estrutura heterogênea (por exemplo, somar totais ou coletar métricas de uma árvore)

## Quando usar

- A estrutura de objetos contém classes com interfaces diferentes e você precisa executar operações que dependem do tipo concreto de cada uma
- Muitas operações distintas e não relacionadas precisam ser aplicadas à estrutura e você não quer poluir as classes com elas
- A hierarquia de elementos raramente muda, mas novas operações são adicionadas com frequência
- Compiladores, interpretadores e ferramentas de análise que percorrem árvores sintáticas (type checking, otimização, geração de código, pretty printing)

## Quando evitar

- A hierarquia de elementos muda com frequência: cada novo tipo exige um novo método em todos os visitantes
- Há poucas operações e elas pertencem naturalmente aos próprios elementos
- A operação precisa de acesso a estado interno privado dos elementos, o que obrigaria a quebrar o encapsulamento
- A linguagem oferece pattern matching exaustivo sobre tipos selados (sealed classes, union types), que resolve o mesmo problema com menos cerimônia

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Novas operações sem alterar as classes dos elementos (Open/Closed para operações) | Adicionar um novo tipo de elemento exige alterar a interface `Visitor` e todos os visitantes concretos |
| Comportamento relacionado concentrado em um único visitante (SRP) | Pode forçar os elementos a expor estado interno via métodos públicos |
| Visitante pode acumular estado durante o percorrimento da estrutura | Double dispatch e callbacks tornam o fluxo menos intuitivo |
| Elimina verificações de tipo e `switch` sobre classes | Acoplamento cíclico entre `Visitor` e a hierarquia de elementos |

- **Acoplamento:** os visitantes conhecem todos os tipos concretos de elemento; os elementos conhecem apenas a interface `Visitor`.
- **Testabilidade:** cada operação pode ser testada isoladamente aplicando o visitante a estruturas pequenas e controladas.
- **Complexidade:** a responsabilidade de percorrer a estrutura (no elemento, no visitante ou em um Iterator) deve ser decidida e mantida de forma consistente.
- **Extensibilidade:** o padrão inverte o eixo de extensão: facilita novas operações e dificulta novos tipos (o chamado *expression problem*).

## Diagrama

```mermaid
classDiagram
    class Client
    class ObjectStructure {
        -List~Element~ elements
        +accept(Visitor visitor)
    }
    class Visitor {
        <<interface>>
        +visitConcreteElementA(ConcreteElementA element)
        +visitConcreteElementB(ConcreteElementB element)
    }
    class ConcreteVisitor1 {
        +visitConcreteElementA(ConcreteElementA element)
        +visitConcreteElementB(ConcreteElementB element)
    }
    class ConcreteVisitor2 {
        +visitConcreteElementA(ConcreteElementA element)
        +visitConcreteElementB(ConcreteElementB element)
    }
    class Element {
        <<interface>>
        +accept(Visitor visitor)
    }
    class ConcreteElementA {
        +accept(Visitor visitor)
        +operationA()
    }
    class ConcreteElementB {
        +accept(Visitor visitor)
        +operationB()
    }
    Client --> ObjectStructure
    Client --> Visitor
    ObjectStructure o--> Element : contem
    Visitor <|.. ConcreteVisitor1
    Visitor <|.. ConcreteVisitor2
    Element <|.. ConcreteElementA
    Element <|.. ConcreteElementB
    Element ..> Visitor : accept
    Visitor ..> ConcreteElementA : visita
    Visitor ..> ConcreteElementB : visita
```

O `Client` aplica um `ConcreteVisitor` à `ObjectStructure`, que repassa o visitante a cada `Element`. Cada `ConcreteElement` implementa `accept` chamando o método `visit` correspondente ao seu tipo, de modo que a operação executada depende do par visitante/elemento (double dispatch).

## Exemplo

Um editor gráfico possui formas estáveis (`Circle` e `Rectangle`) e precisa calcular a área total e exportar o desenho para JSON sem adicionar esses métodos às classes das formas.

```typescript
interface ShapeVisitor<R> {
  visitCircle(c: Circle): R;
  visitRectangle(r: Rectangle): R;
}

interface Shape { accept<R>(v: ShapeVisitor<R>): R; }

class Circle implements Shape {
  constructor(public radius: number) {}
  accept<R>(v: ShapeVisitor<R>): R { return v.visitCircle(this); }
}

class Rectangle implements Shape {
  constructor(public width: number, public height: number) {}
  accept<R>(v: ShapeVisitor<R>): R { return v.visitRectangle(this); }
}

class AreaVisitor implements ShapeVisitor<number> {
  visitCircle(c: Circle) { return Math.PI * c.radius ** 2; }
  visitRectangle(r: Rectangle) { return r.width * r.height; }
}

class JsonExportVisitor implements ShapeVisitor<string> {
  visitCircle(c: Circle) { return JSON.stringify({ type: "circle", r: c.radius }); }
  visitRectangle(r: Rectangle) { return JSON.stringify({ type: "rect", w: r.width, h: r.height }); }
}

const shapes: Shape[] = [new Circle(1), new Rectangle(2, 3)];
const total = shapes.reduce((sum, s) => sum + s.accept(new AreaVisitor()), 0);
const json = shapes.map((s) => s.accept(new JsonExportVisitor()));
```

## Padrões relacionados

- [Composite](/coding/gof/structural/composite) — o Visitor é frequentemente aplicado para executar operações sobre todos os nós de uma árvore Composite
- [Iterator](/coding/gof/behavioral/iterator) — pode ser usado para percorrer a estrutura de objetos enquanto o Visitor executa a operação em cada elemento
- [Interpreter](/coding/gof/behavioral/interpreter) — operações sobre a árvore sintática abstrata do Interpreter (avaliação, impressão, otimização) costumam ser implementadas como visitantes
- [Command](/coding/gof/behavioral/command) — ambos encapsulam operações em objetos; o Visitor pode ser visto como um Command poderoso que atua sobre vários tipos de elemento
- [Strategy](/coding/gof/behavioral/strategy) — também extrai comportamento para objetos separados, mas varia um algoritmo para um único contexto, sem double dispatch

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Visitor no Refactoring.Guru](https://refactoring.guru/design-patterns/visitor)
