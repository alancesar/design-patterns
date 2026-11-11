---
title: Factory
pattern_slug: factory
category: Building Blocks
tags:
  - Simplicity
  - Consistency
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Factory"
---

# Factory

## Descrição

No DDD, uma Factory encapsula o conhecimento necessário para criar objetos complexos ou agregados inteiros, mantendo essa responsabilidade fora do modelo principal. Ela garante que o objeto nasça completo e com todas as invariantes satisfeitas.

A criação é atômica: o cliente obtém o agregado inteiro em um estado consistente, ou a criação falha. A Factory pode ser um Factory Method na raiz de um agregado, uma classe própria ou um método estático, dependendo da complexidade. O cliente depende só da interface, sem conhecer o tipo concreto nem os detalhes da montagem.

Não se deve confundir com os padrões Factory Method e Abstract Factory do GoF, que são soluções de design de classes. A Factory do DDD é um conceito de domínio ligado ao ciclo de vida: ela cria e reconstitui objetos, enquanto o Repository os persiste e recupera.

## Problemas que resolve

- Construtores complexos que misturam regras de negócio e montagem.
- Clientes que precisam conhecer a estrutura interna de um agregado para criá-lo.
- Objetos criados em estado inválido ou parcial.
- Reconstituição de objetos a partir de dados persistidos sem passar pelas regras de criação.

## Quando usar

- Quando a criação envolve várias etapas, regras ou objetos relacionados.
- Quando se quer garantir invariantes desde o nascimento do objeto.
- Quando o cliente não deve conhecer a classe concreta.

## Quando evitar

- Quando um construtor simples basta.
- Quando a Factory seria apenas uma camada extra sem lógica de criação.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Invariantes garantidas na criação | Mais uma classe para manter |
| Clientes desacoplados dos detalhes de montagem | Risco de duplicar a lógica do construtor |
| Modelo principal mais limpo | Pode esconder complexidade que mereceria simplificação |

- **Atomicidade:** o objeto criado deve ser consistente por inteiro.
- **Reconstituição:** a criação a partir de dados persistidos segue regras diferentes da criação nova.

## Diagrama

```mermaid
classDiagram
    class LoanContractFactory {
        +create(customer, proposal) LoanContract
    }
    class LoanContract {
        <<aggregate root>>
    }
    class Installment
    class Customer
    LoanContractFactory ..> LoanContract : cria
    LoanContractFactory ..> Customer
    LoanContract "1" *-- "*" Installment
```

`LoanContractFactory` monta o `LoanContract` com o cronograma de `Installment` e garante que o agregado seja válido ao ser entregue.

## Exemplo

A fábrica entrega o contrato de crédito já com o cronograma de parcelas, e recusa a criação para cliente com restrição.

```java
public class LoanContractFactory {
    public LoanContract create(Customer customer, CreditProposal proposal) {
        if (customer.hasRestriction()) {
            throw new IllegalStateException("Cliente com restrição");
        }
        LoanContract contract = new LoanContract(ContractId.next(), customer.id(), proposal.principal());
        List<Installment> schedule = proposal.amortization()
                .schedule(proposal.principal(), proposal.monthlyRate(), proposal.months());
        schedule.forEach(contract::addInstallment);
        return contract;
    }
}
```

## Padrões relacionados

- [Aggregate](/design/ddd/building-blocks/aggregate) — a fábrica cria o agregado inteiro e suas invariantes.
- [Entity](/design/ddd/building-blocks/entity) — cria entidades com identidade válida.
- [Value Object](/design/poeaa/base/value-object) — também pode ser criado por fábricas.
- [Repository](/design/poeaa/object-relational-metadata-mapping/repository) — recupera objetos já existentes, enquanto a fábrica cria novos.
- [Factory](/coding/gof/creational/factory) — a fábrica simples do acervo GoF, com escopo de design de classes.
- [Factory Method](/coding/gof/creational/factory-method) — padrão GoF que pode ser usado na implementação.
- [Abstract Factory](/coding/gof/creational/abstract-factory) — padrão GoF para famílias de objetos, distinto da Factory do DDD.

## Referência

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
