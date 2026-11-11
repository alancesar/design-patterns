---
title: Iterator
pattern_slug: iterator
category: Behavioral
tags:
  - Encapsulation
  - Simplicity
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Iterator"
---

# Iterator

## Descrição

O Iterator fornece uma forma de acessar sequencialmente os elementos de uma coleção (agregado) sem expor sua representação interna. Em vez de o cliente conhecer se os dados estão em um array, uma lista ligada, uma árvore ou uma fonte paginada, ele conversa apenas com uma interface de iteração uniforme, com operações como `hasNext()` e `next()`.

A responsabilidade de percorrer a coleção sai do agregado e passa para um objeto iterador separado, que guarda o estado da travessia (posição atual, pilha de nós visitados, cursor de página etc.). Assim, a mesma coleção pode ter vários iteradores ativos ao mesmo tempo e oferecer diferentes estratégias de percurso (em ordem, reversa, filtrada, em largura, em profundidade).

O agregado atua como fábrica de iteradores por meio de um método como `createIterator()`. Muitas linguagens incorporam o padrão nativamente (`Iterable`/`Iterator` em Java, `IEnumerable` em C#, protocolo de iteração em Python e JavaScript, geradores com `yield`).

## Problemas que resolve

- O código cliente fica acoplado à estrutura interna da coleção (índices, ponteiros de nós, cursores) e quebra quando ela muda.
- Diferentes coleções exigem laços diferentes, impedindo algoritmos genéricos que funcionem sobre qualquer estrutura.
- É preciso suportar múltiplas formas de percorrer a mesma coleção sem inchar sua interface com métodos de travessia.
- Várias travessias simultâneas e independentes sobre a mesma coleção precisam manter seu próprio estado.
- Percorrer grandes volumes de dados (streams, resultados paginados) sem carregar tudo em memória.

## Quando usar

- A coleção tem estrutura complexa (árvore, grafo, composição) e você quer esconder essa complexidade dos clientes.
- Você precisa de uma interface uniforme para percorrer coleções heterogêneas (iteração polimórfica).
- Há necessidade de várias estratégias de percurso ou de iteração preguiçosa (lazy) sobre fontes externas.
- Você quer reduzir duplicação de código de travessia espalhado pela aplicação.

## Quando evitar

- A coleção é simples (um array ou lista nativa) e a linguagem já oferece iteração adequada; criar iteradores próprios só adiciona cerimônia.
- O acesso aleatório por índice é o caso de uso principal, e a iteração sequencial é mais lenta ou menos expressiva.
- A coleção é modificada com frequência durante a travessia e não há uma política clara para lidar com modificações concorrentes.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Encapsula a estrutura interna da coleção | Mais classes e interfaces para manter |
| Permite múltiplas travessias simultâneas e independentes | Iteradores podem ficar inválidos se a coleção mudar durante o percurso |
| Suporta várias estratégias de percurso sem alterar o agregado | Pode ser menos eficiente que acesso direto em coleções especializadas |
| Habilita iteração preguiçosa e sobre fontes infinitas | Estado da iteração precisa de cuidado em cenários concorrentes |
| Facilita algoritmos genéricos (Single Responsibility, Open/Closed) | Overkill para coleções triviais |

- **Acoplamento:** o cliente depende apenas das interfaces `Iterator` e `Aggregate`, não das classes concretas.
- **Testabilidade:** iteradores podem ser testados isoladamente e substituídos por dublês simples.
- **Robustez:** decida entre iteradores *fail-fast* (lançam erro em modificação concorrente) ou baseados em snapshot.
- **Iterador interno vs. externo:** iteradores externos dão controle ao cliente; internos (ex.: `forEach` com callback) são mais simples, porém menos flexíveis.

## Diagrama

```mermaid
classDiagram
    class Iterator {
        <<interface>>
        +hasNext() bool
        +next() Object
    }
    class Aggregate {
        <<interface>>
        +createIterator() Iterator
    }
    class ConcreteIterator {
        -collection ConcreteAggregate
        -position int
        +hasNext() bool
        +next() Object
    }
    class ConcreteAggregate {
        -items List
        +createIterator() Iterator
    }
    class Client
    Iterator <|.. ConcreteIterator
    Aggregate <|.. ConcreteAggregate
    ConcreteAggregate ..> ConcreteIterator : cria
    ConcreteIterator --> ConcreteAggregate : percorre
    Client --> Aggregate
    Client --> Iterator
```

O `Client` obtém um `Iterator` a partir do `Aggregate` e percorre os elementos sem conhecer a estrutura interna. O `ConcreteAggregate` cria o `ConcreteIterator`, que mantém a posição atual da travessia sobre a coleção.

## Exemplo

O extrato de uma conta tem milhares de lançamentos e a API os devolve em páginas com cursor. O consumidor só chama `hasNext()` e `next()`: o `PagedStatementIterator` busca a próxima página quando a atual acaba, e o `ReverseStatementIterator` percorre a mesma coleção do lançamento mais recente para o mais antigo.

```typescript
interface StatementEntry {
  date: string;
  description: string;
  amountCents: number;
}

interface Page {
  entries: StatementEntry[];
  nextCursor?: number;
}

interface StatementIterator {
  hasNext(): boolean;
  next(): StatementEntry;
}

class Statement {
  constructor(private entries: StatementEntry[], private pageSize = 2) {}

  // simula a API paginada: devolve uma página e o cursor da próxima
  fetchPage(cursor = 0): Page {
    const end = cursor + this.pageSize;
    return {
      entries: this.entries.slice(cursor, end),
      nextCursor: end < this.entries.length ? end : undefined,
    };
  }

  createIterator(): StatementIterator {
    return new PagedStatementIterator(this);
  }

  createReverseIterator(): StatementIterator {
    return new ReverseStatementIterator(this.entries);
  }
}

class PagedStatementIterator implements StatementIterator {
  private buffer: StatementEntry[] = [];
  private position = 0;
  private cursor: number | undefined = 0;
  constructor(private statement: Statement) {}

  hasNext(): boolean { this.fill(); return this.position < this.buffer.length; }
  next(): StatementEntry { this.fill(); return this.buffer[this.position++]; }

  private fill(): void {
    if (this.position < this.buffer.length || this.cursor === undefined) return;
    const page = this.statement.fetchPage(this.cursor); // só busca quando a página atual acabou
    this.buffer = page.entries;
    this.position = 0;
    this.cursor = page.nextCursor;
  }
}

class ReverseStatementIterator implements StatementIterator {
  private position: number;
  constructor(private entries: StatementEntry[]) {
    this.position = entries.length - 1;
  }

  hasNext(): boolean { return this.position >= 0; }
  next(): StatementEntry { return this.entries[this.position--]; }
}

const statement = new Statement([
  { date: "2026-03-01", description: "Pix recebido", amountCents: 25_000 },
  { date: "2026-03-02", description: "Boleto pago", amountCents: -8_990 },
  { date: "2026-03-03", description: "Compra no cartão", amountCents: -4_550 },
]);

const it = statement.createIterator();
while (it.hasNext()) console.log(it.next().description);  // Pix recebido, Boleto pago, Compra no cartão

const recent = statement.createReverseIterator();
console.log(recent.next().description);                   // Compra no cartão
```

## Padrões relacionados

- [Composite](/coding/gof/structural/composite) — iteradores são frequentemente usados para percorrer estruturas recursivas de Composite.
- [Factory Method](/coding/gof/creational/factory-method) — `createIterator()` é um Factory Method que permite a cada coleção instanciar o iterador adequado.
- [Memento](/coding/gof/behavioral/memento) — pode capturar o estado de uma iteração para retomá-la ou desfazê-la depois.
- [Visitor](/coding/gof/behavioral/visitor) — combina-se com Iterator: o iterador percorre a coleção e o Visitor aplica a operação a cada elemento.
- [Null Object](/coding/gof/behavioral/null-object) — um iterador vazio (Null Iterator) evita verificações de nulo em coleções sem elementos.

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Iterator no Refactoring.Guru](https://refactoring.guru/design-patterns/iterator)
