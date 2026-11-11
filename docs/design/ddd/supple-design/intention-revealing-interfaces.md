---
title: Intention-Revealing Interfaces
pattern_slug: intention-revealing-interfaces
category: Supple Design
tags:
  - Shared Understanding
  - Simplicity
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Intention-Revealing Interfaces"
---

# Intention-Revealing Interfaces

## Descrição

Intention-Revealing Interfaces consiste em nomear classes, métodos e argumentos de modo que expressem o propósito e o efeito observável, e não o modo como o resultado é obtido. O nome vem da Ubiquitous Language: quem usa o componente entende o que ele faz sem precisar ler a implementação.

Na prática, o contrato é escrito primeiro, por exemplo com um teste que mostra como o cliente quer usar a operação. Depois a implementação é escrita por trás dessa interface. Se o desenvolvedor precisa abrir o código para saber o que um método faz, o encapsulamento foi perdido: o cliente passa a depender dos detalhes internos.

O padrão é a base do Supple Design. Interfaces que revelam intenção tornam as demais técnicas (funções sem efeito colateral, assertions, operações fechadas) mais fáceis de aplicar e de comunicar.

## Problemas que resolve

- Nomes genéricos (`process`, `handle`, `calculate`) que obrigam a ler a implementação para entender o efeito.
- Clientes acoplados ao mecanismo interno, e não ao propósito da operação.
- Desenvolvedores que reimplementam algo que já existe porque não perceberam o que o método fazia.
- Distância entre o vocabulário do negócio e o vocabulário do código.

## Quando usar

- Em qualquer classe ou método público do modelo de domínio.
- Quando especialistas do negócio e desenvolvedores precisam ler o mesmo código ou os mesmos testes.
- Ao refatorar métodos cujo nome descreve o "como" em vez do "quê".

## Quando evitar

- Em detalhes internos privados e voláteis, onde o nome prolixo traz pouco valor.
- Quando o conceito ainda não foi entendido: um nome "bonito" para um modelo errado só dá falsa confiança. Primeiro aprofunde o modelo.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Código legível por quem não conhece a implementação | Exige conhecer bem o domínio para dar bons nomes |
| Menos duplicação e menos leitura de código interno | Renomear APIs públicas pode afetar muitos clientes |
| Testes que servem como documentação | Nomes ruins mantidos por inércia perdem o benefício |

- **Linguagem compartilhada:** o vocabulário do código e o da conversa evoluem juntos.
- **Encapsulamento:** o cliente depende do contrato, não do mecanismo.
- **Manutenção:** nomes precisam ser revisados quando o entendimento do domínio muda.

## Diagrama

```mermaid
classDiagram
    class AccountBefore {
        +process(Money amount)
    }
    class AccountAfter {
        +placeHold(Money amount)
        +availableBalance() Money
    }
    note for AccountBefore "Nome nao revela se debita, credita ou reserva"
    note for AccountAfter "Nome revela o efeito: reserva saldo sem debitar"
```

Em `AccountBefore`, o método não diz o que acontece com o saldo; em `AccountAfter`, `placeHold` revela a intenção e o efeito. O livro ilustra o padrão com a mistura de tintas.

## Exemplo

Uma conta digital tinha o método `process(Money amount)`, que na verdade reservava o valor do saldo disponível, sem debitar. O cliente precisava ler o corpo do método para descobrir o efeito, e já houve quem o chamasse achando que movimentava o dinheiro. Renomeado para `placeHold`, o contrato fica claro e o teste diz o que se espera.

```java
public class Account {
    private Money balance;
    private final Money overdraftLimit;
    private Money held = Money.brl(0);

    public Account(Money balance, Money overdraftLimit) {
        this.balance = balance;
        this.overdraftLimit = overdraftLimit;
    }

    // Antes: public void process(Money amount)
    public void placeHold(Money amount) {
        held = held.plus(amount);
    }

    public Money balance() { return balance; }

    public Money availableBalance() {
        return balance.plus(overdraftLimit).minus(held);
    }
}

// O teste escreve o contrato antes da implementação
Account account = new Account(Money.brl(100_00), Money.brl(0));
account.placeHold(Money.brl(30_00));
assertEquals(Money.brl(70_00), account.availableBalance());
assertEquals(Money.brl(100_00), account.balance());
```

## Padrões relacionados

- [Side-Effect-Free Functions](/design/ddd/supple-design/side-effect-free-functions) — separa consultas de comandos, deixando o efeito explícito.
- [Assertions](/design/ddd/supple-design/assertions) — declaram os efeitos e invariantes que o nome apenas sugere.
- [Ubiquitous Language](/design/ddd/model-in-practice/ubiquitous-language) — fonte dos nomes usados nas interfaces.
- [Model-Driven Design](/design/ddd/model-in-practice/model-driven-design) — liga o modelo ao código por meio dessas interfaces.
- [Refactoring Toward Deeper Insight](/design/ddd/model-in-practice/refactoring-toward-deeper-insight) — novos entendimentos geram novos nomes.

## Referência

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
