---
title: Null Object
pattern_slug: null-object
category: Behavioral
tags:
  - Simplicity
origin: Classic
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Null Object"
---

# Null Object

## Descrição

O Null Object substitui referências nulas por um objeto que implementa a mesma interface esperada pelo cliente, mas cujo comportamento é neutro, ou seja, "não fazer nada". Assim o cliente pode chamar métodos sem antes verificar se a referência existe.

O padrão define uma abstração (interface ou classe abstrata), uma ou mais implementações reais e uma implementação nula. A implementação nula devolve valores padrão seguros (lista vazia, zero, string vazia) ou simplesmente ignora a chamada. Como ela não guarda estado, costuma ser compartilhada como uma instância única.

Na prática, o padrão troca o tratamento condicional espalhado pelo código (`if (x != null)`) por polimorfismo: a decisão sobre o que fazer na ausência de um objeto fica concentrada em uma única classe.

## Problemas que resolve

- Verificações de nulo repetidas em vários pontos do código, que poluem a lógica e são fáceis de esquecer
- Falhas em tempo de execução (`NullPointerException`, `TypeError`) causadas por referências ausentes
- Dependências opcionais (logger, notificador, cache) que exigem lógica condicional sempre que são usadas
- Ausência de um comportamento padrão bem definido quando um colaborador não está disponível

## Quando usar

- O cliente precisa de um colaborador que pode estar ausente, e "não fazer nada" é uma reação aceitável
- Há muitos pontos de verificação de nulo para a mesma abstração
- Você quer fornecer um valor padrão seguro para dependências opcionais (por exemplo, um `NullLogger` em testes)
- O comportamento neutro pode ser expresso de forma clara e previsível

### Quando evitar

- A ausência do objeto é um erro que precisa ser detectado e reportado; o Null Object esconderia a falha
- O cliente precisa reagir de forma diferente quando o objeto não existe (nesse caso, prefira `Optional`/`Maybe` ou verificação explícita)
- Não existe um comportamento neutro razoável (por exemplo, um método que precisa devolver um identificador válido)
- A linguagem já oferece mecanismos adequados, como operadores de navegação segura, e a abstração extra não se paga

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Elimina verificações de nulo espalhadas pelo código | Pode mascarar erros reais, adiando a descoberta de bugs |
| Código cliente mais simples e legível | Uma classe extra para cada abstração que precisa de versão nula |
| Comportamento padrão centralizado em um único lugar | Toda mudança na interface exige atualizar também a implementação nula |
| Facilita testes ao substituir dependências opcionais | O "não fazer nada" pode não ser óbvio para quem lê o código |

- **Acoplamento:** o cliente depende apenas da abstração, sem conhecer a implementação nula.
- **Testabilidade:** objetos nulos funcionam como dublês simples para dependências que não interessam ao teste.
- **Desempenho:** a implementação nula costuma ser um Singleton sem estado, com custo desprezível.
- **Semântica:** documente bem o comportamento neutro para não surpreender quem consome a interface.

## Diagrama

```mermaid
classDiagram
    class Client
    class AbstractObject {
        <<interface>>
        +request()
    }
    class RealObject {
        +request()
    }
    class NullObject {
        +request()
    }
    Client --> AbstractObject : usa
    AbstractObject <|.. RealObject
    AbstractObject <|.. NullObject
```

`Client` depende apenas de `AbstractObject`. `RealObject` executa o comportamento de fato, enquanto `NullObject` implementa a mesma interface com um comportamento neutro, permitindo que o cliente o use sem verificar nulos.

## Exemplo

Um serviço de pedidos recebe um logger opcional. Em vez de testar se o logger existe a cada chamada, o serviço recebe um `NullLogger` quando nenhum logger é configurado.

```typescript
interface Logger {
  info(message: string): void;
}

class ConsoleLogger implements Logger {
  info(message: string): void {
    console.log(`[INFO] ${message}`);
  }
}

class NullLogger implements Logger {
  static readonly instance = new NullLogger();
  info(_message: string): void {
    // não faz nada
  }
}

class OrderService {
  constructor(private readonly logger: Logger = NullLogger.instance) {}

  placeOrder(id: string): void {
    // ... regras de negócio
    this.logger.info(`Pedido ${id} criado`); // sem if (logger != null)
  }
}

new OrderService(new ConsoleLogger()).placeOrder("42"); // registra log
new OrderService().placeOrder("43");                    // silencioso
```

## Padrões relacionados

- [Strategy](/coding/gof/behavioral/strategy) — o Null Object pode ser visto como uma estratégia que não faz nada
- [State](/coding/gof/behavioral/state) — um estado "nulo" ou inicial pode ser modelado como Null Object
- [Singleton](/coding/gof/creational/singleton) — como não tem estado, o objeto nulo costuma ser uma instância única compartilhada
- [Flyweight](/coding/gof/structural/flyweight) — a instância nula pode ser compartilhada como um flyweight sem estado intrínseco
- [Proxy](/coding/gof/structural/proxy) — ambos se colocam no lugar do objeto real, mas o Proxy controla acesso a ele e o Null Object o substitui
- [Iterator](/coding/gof/behavioral/iterator) — um iterador vazio é um caso clássico de Null Object
- [Command](/coding/gof/behavioral/command) — um comando "no-op" é usado como valor padrão em vez de comando nulo

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Null Object no SourceMaking](https://sourcemaking.com/design_patterns/null_object)
