---
title: Interpreter
pattern_slug: interpreter
category: Behavioral
tags:
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Interpreter"
mdx:
  format: mdx
---

# Interpreter

## Descrição

O Interpreter define uma representação para a gramática de uma linguagem simples e um interpretador que usa essa representação para avaliar sentenças da linguagem. Cada regra da gramática vira uma classe, e uma sentença é representada como uma árvore sintática abstrata (AST) composta por instâncias dessas classes.

A interface comum `AbstractExpression` declara a operação `interpret(context)`. Expressões terminais (como literais e variáveis) resolvem seu valor diretamente; expressões não terminais (como soma, `and`, `or`) combinam recursivamente os resultados de suas subexpressões. Um `Context` carrega informações globais necessárias à interpretação, como valores de variáveis.

O padrão não trata da análise sintática (parsing): ele assume que a árvore já foi construída, seja manualmente pelo cliente, seja por um parser separado.

## Problemas que resolve

- Avaliar repetidamente expressões de uma linguagem pequena e bem definida (regras de negócio, filtros, consultas simples)
- Evitar condicionais gigantes ao interpretar comandos ou expressões configuráveis pelo usuário
- Permitir estender a linguagem adicionando novas regras como novas classes
- Representar expressões como objetos que podem ser combinados, reutilizados e avaliados com contextos diferentes

## Quando usar

- A gramática é simples e relativamente estável
- Eficiência não é a preocupação principal
- É útil expressar o problema como sentenças de uma DSL (por exemplo, regras de validação, expressões booleanas, especificações de busca)
- As mesmas expressões precisam ser avaliadas contra vários contextos

## Quando evitar

- A gramática é grande ou complexa: o número de classes explode e a manutenção fica difícil; prefira geradores de parser ou bibliotecas de expressão
- O desempenho é crítico: interpretar uma AST recursivamente é mais lento que código compilado ou tabelas de estado
- Já existe uma linguagem ou motor de regras pronto que atende à necessidade

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Fácil mudar e estender a gramática (nova regra = nova classe) | Gramáticas grandes geram muitas classes difíceis de manter |
| Implementação direta de cada regra, isolada e testável | Avaliação recursiva pode ser lenta e consumir pilha em árvores profundas |
| Expressões combináveis e reutilizáveis | Não resolve o parsing; é preciso construir a AST de outra forma |
| Novas formas de interpretar podem ser adicionadas | Adicionar operações exige alterar todas as classes, a menos que se use Visitor |

- Acoplamento: cada classe conhece apenas sua regra e suas subexpressões.
- Testabilidade: expressões terminais e não terminais podem ser testadas isoladamente.
- Complexidade: cresce linearmente com o número de regras da gramática.
- Desempenho: considere cache de resultados ou compilação da AST quando houver avaliações frequentes.

## Diagrama

```mermaid
classDiagram
    class Client
    class Context {
        +lookup(name) Object
        +assign(name, value)
    }
    class AbstractExpression {
        <<interface>>
        +interpret(context) Object
    }
    class TerminalExpression {
        +interpret(context) Object
    }
    class NonterminalExpression {
        -children List~AbstractExpression~
        +interpret(context) Object
    }
    Client --> AbstractExpression
    Client --> Context
    AbstractExpression <|.. TerminalExpression
    AbstractExpression <|.. NonterminalExpression
    NonterminalExpression o-- AbstractExpression
    AbstractExpression ..> Context
```

O `Client` monta (ou recebe) a árvore de `AbstractExpression` e chama `interpret` passando um `Context`. `TerminalExpression` representa as folhas da gramática e `NonterminalExpression` agrega subexpressões, formando uma estrutura recursiva semelhante ao Composite.

## Exemplo

O antifraude avalia regras booleanas como `high_amount AND (new_device OR night_time)` contra os sinais de cada transação. O contexto é um mapa com os sinais, e cada regra é uma árvore de expressões.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
interface Expression {
    boolean interpret(Map<String, Boolean> ctx);
}

record Variable(String name) implements Expression {
    public boolean interpret(Map<String, Boolean> ctx) {
        return ctx.getOrDefault(name, false);
    }
}

record And(Expression left, Expression right) implements Expression {
    public boolean interpret(Map<String, Boolean> ctx) {
        return left.interpret(ctx) && right.interpret(ctx);
    }
}

record Or(Expression left, Expression right) implements Expression {
    public boolean interpret(Map<String, Boolean> ctx) {
        return left.interpret(ctx) || right.interpret(ctx);
    }
}

Expression rule = new And(
    new Variable("high_amount"),
    new Or(new Variable("new_device"), new Variable("night_time")));
Map<String, Boolean> ctx = Map.of("high_amount", true, "night_time", true);
System.out.println(rule.interpret(ctx)); // true

Map<String, Boolean> calm = Map.of("high_amount", true);
System.out.println(rule.interpret(calm)); // false
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import Protocol

class Expression(Protocol):
    def interpret(self, ctx: dict[str, bool]) -> bool: ...

@dataclass(frozen=True)
class Variable:
    name: str

    def interpret(self, ctx: dict[str, bool]) -> bool:
        return ctx.get(self.name, False)

@dataclass(frozen=True)
class And:
    left: Expression
    right: Expression

    def interpret(self, ctx: dict[str, bool]) -> bool:
        return self.left.interpret(ctx) and self.right.interpret(ctx)

@dataclass(frozen=True)
class Or:
    left: Expression
    right: Expression

    def interpret(self, ctx: dict[str, bool]) -> bool:
        return self.left.interpret(ctx) or self.right.interpret(ctx)

rule = And(Variable("high_amount"), Or(Variable("new_device"), Variable("night_time")))
ctx = {"high_amount": True, "night_time": True}
print(rule.interpret(ctx))  # True

calm = {"high_amount": True}
print(rule.interpret(calm))  # False
```

</TabItem>
<TabItem value="go" label="Go">

```go
type Expression interface {
	Interpret(ctx map[string]bool) bool
}

type Variable string

func (v Variable) Interpret(ctx map[string]bool) bool { return ctx[string(v)] }

type And struct{ Left, Right Expression }

func (e And) Interpret(ctx map[string]bool) bool {
	return e.Left.Interpret(ctx) && e.Right.Interpret(ctx)
}

type Or struct{ Left, Right Expression }

func (e Or) Interpret(ctx map[string]bool) bool {
	return e.Left.Interpret(ctx) || e.Right.Interpret(ctx)
}

func main() {
	rule := And{
		Variable("high_amount"),
		Or{Variable("new_device"), Variable("night_time")},
	}
	ctx := map[string]bool{"high_amount": true, "night_time": true}
	fmt.Println(rule.Interpret(ctx)) // true

	calm := map[string]bool{"high_amount": true}
	fmt.Println(rule.Interpret(calm)) // false
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface Expression {
  interpret(ctx: Map<string, boolean>): boolean;
}

class Variable implements Expression {
  constructor(private name: string) {}
  interpret(ctx: Map<string, boolean>): boolean {
    return ctx.get(this.name) ?? false;
  }
}

class And implements Expression {
  constructor(private left: Expression, private right: Expression) {}
  interpret(ctx: Map<string, boolean>): boolean {
    return this.left.interpret(ctx) && this.right.interpret(ctx);
  }
}

class Or implements Expression {
  constructor(private left: Expression, private right: Expression) {}
  interpret(ctx: Map<string, boolean>): boolean {
    return this.left.interpret(ctx) || this.right.interpret(ctx);
  }
}

const rule = new And(
  new Variable("high_amount"),
  new Or(new Variable("new_device"), new Variable("night_time")),
);
const ctx = new Map([["high_amount", true], ["night_time", true]]);
console.log(rule.interpret(ctx)); // true

const calm = new Map([["high_amount", true]]);
console.log(rule.interpret(calm)); // false
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Composite](/coding/gof/structural/composite) — a árvore sintática abstrata é uma instância do Composite
- [Flyweight](/coding/gof/structural/flyweight) — permite compartilhar símbolos terminais repetidos na AST
- [Iterator](/coding/gof/behavioral/iterator) — pode ser usado para percorrer a estrutura da árvore
- [Visitor](/coding/gof/behavioral/visitor) — concentra operações sobre os nós da AST em uma única classe, evitando alterar cada expressão

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Interpreter no SourceMaking](https://sourcemaking.com/design_patterns/interpreter)
