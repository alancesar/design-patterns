---
title: Private Class Data
pattern_slug: private-class-data
category: Structural
tags:
  - Encapsulation
origin: Classic
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Private Class Data"
---

# Private Class Data

## Descrição

O Private Class Data restringe o acesso e a modificação dos atributos de uma classe ao separá-los em um objeto de dados próprio (a classe `Data`). A classe principal deixa de expor ou manipular diretamente seus campos e passa a guardar uma referência a esse objeto, que só oferece leitura, ou leitura e alterações controladas.

Normalmente os dados são passados no construtor da classe de dados e ficam imutáveis depois disso. Assim, nem os próprios métodos da classe principal conseguem alterar por engano valores que deveriam ser fixados uma única vez, como na inicialização. O padrão reduz a superfície de escrita do estado e deixa claro quais atributos são estáveis e quais variam.

Não é um dos 23 padrões do livro do Gang of Four. Ele aparece em catálogos complementares como uma técnica de encapsulamento, e em várias linguagens modernas se resume ao uso de campos `final`/`readonly`, records ou value objects.

## Problemas que resolve

- Atributos que deveriam ser definidos só na construção acabam sendo alterados por métodos da própria classe.
- Classes com muitos campos mutáveis, nas quais é difícil saber quem altera o quê e quando.
- Exposição desnecessária do estado interno por getters e setters genéricos.
- Dificuldade de manter invariantes quando qualquer método pode reatribuir campos.

## Quando usar

- Quando um conjunto de atributos deve ser imutável depois da inicialização.
- Quando se quer separar dados (estado) de comportamento, deixando explícito o que é somente leitura.
- Quando a linguagem não oferece bons recursos nativos de imutabilidade (`final`, `readonly`, `const`).
- Quando o objeto é compartilhado entre threads e precisa de estado seguro para leitura concorrente.

### Quando evitar

- Quando a linguagem já oferece imutabilidade simples (records, `readonly`, `data class`, `frozen dataclass`) que resolve o problema sem uma classe extra.
- Em classes pequenas, com poucos campos, nas quais a indireção só acrescenta código.
- Quando os dados precisam mudar com frequência; a imutabilidade obrigaria a recriar objetos o tempo todo.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Encapsulamento mais forte e menos escrita acidental do estado | Mais uma classe e uma indireção no acesso aos dados |
| Invariantes garantidas desde a construção | Alterar um valor exige criar um novo objeto de dados |
| Estado imutável, seguro para compartilhar entre threads | Pode duplicar o que a linguagem já oferece nativamente |
| Separação clara entre dados e comportamento | Risco de virar um "saco de getters" sem significado de domínio |

- **Acoplamento:** a classe principal depende só da interface de leitura da classe de dados.
- **Testabilidade:** objetos de dados imutáveis são fáceis de criar e comparar nos testes.
- **Desempenho:** recriar objetos de dados a cada alteração pode gerar alocações extras em caminhos críticos.

## Diagrama

```mermaid
classDiagram
    class Client
    class MainClass {
        -data: DataClass
        +MainClass(attr1, attr2)
        +operation()
    }
    class DataClass {
        -attribute1
        -attribute2
        +DataClass(attr1, attr2)
        +getAttribute1()
        +getAttribute2()
    }
    Client --> MainClass
    MainClass *-- DataClass
```

O `Client` usa a `MainClass`, que compõe internamente uma `DataClass`. A `DataClass` recebe os valores no construtor e expõe apenas métodos de leitura, de modo que a `MainClass` usa os dados sem poder reatribuí-los.

## Exemplo

Uma classe `Circle` recebe raio, cor e origem na criação, e esses valores não podem mudar depois. Os dados ficam em `CircleData`, que só permite leitura.

```java
public final class CircleData {
    private final double radius;
    private final String color;
    private final Point origin;

    public CircleData(double radius, String color, Point origin) {
        this.radius = radius;
        this.color = color;
        this.origin = origin;
    }

    public double getRadius() { return radius; }
    public String getColor() { return color; }
    public Point getOrigin() { return origin; }
}

public class Circle {
    private final CircleData data;

    public Circle(double radius, String color, Point origin) {
        this.data = new CircleData(radius, color, origin);
    }

    public double circumference() { return 2 * Math.PI * data.getRadius(); }
    public double area() { return Math.PI * data.getRadius() * data.getRadius(); }
    public void draw() { System.out.println("Desenhando círculo " + data.getColor()); }
}
```

## Padrões relacionados

- [Proxy](./proxy.md) — também controla o acesso a um objeto, mas por meio de um substituto, e não pela separação do estado.
- [Facade](./facade.md) — ambos reduzem o que é exposto aos clientes; a Facade simplifica um subsistema, o Private Class Data protege os atributos.
- [Builder](../creational/builder.md) — costuma montar objetos de dados imutáveis quando há muitos parâmetros de inicialização.
- [Telescoping Constructor](../creational/telescoping-constructor.md) — problema que aparece quando a classe de dados recebe muitos atributos no construtor.
- [Memento](../behavioral/memento.md) — também guarda o estado em um objeto separado e opaco, mas para salvá-lo e restaurá-lo depois.
- [Flyweight](./flyweight.md) — o estado intrínseco compartilhado precisa ser imutável, que é justamente o que o Private Class Data garante.

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Private Class Data no SourceMaking](https://sourcemaking.com/design_patterns/private_class_data)
