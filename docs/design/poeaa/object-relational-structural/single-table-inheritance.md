---
title: Single Table Inheritance
pattern_slug: single-table-inheritance
category: Object-Relational Structural
tags:
  - Simplicity
  - Performance
source: https://martinfowler.com/eaaCatalog/singleTableInheritance.html
sidebar_label: "Single Table Inheritance"
---

# Single Table Inheritance

## Descrição

O Single Table Inheritance representa uma hierarquia de classes como uma única tabela, com colunas para todos os campos de todas as classes. Cada linha guarda um objeto, e uma coluna discriminadora indica a qual classe concreta ela pertence.

Os campos que não se aplicam a uma subclasse ficam nulos. Ao carregar, o mapeador lê o discriminador para decidir qual classe instanciar.

É o esquema mais simples dos três de herança, e tem a vantagem de não exigir joins nem de a tabela ser alterada quando um campo sobe ou desce na hierarquia.

## Problemas que resolve

- Mapear herança com um esquema simples e sem joins.
- Consultar polimorficamente toda a hierarquia em uma única tabela.

## Quando usar

- Quando a hierarquia é pequena e as subclasses diferem em poucos campos.
- Quando o desempenho de leitura polimórfica importa.
- Quando refatorações movem campos pela hierarquia com frequência.

## Quando evitar

- Quando as subclasses têm muitos campos exclusivos, gerando uma tabela larga e esparsa.
- Quando é necessário `NOT NULL` nas colunas das subclasses.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Uma única tabela, sem joins | Colunas nulas desperdiçam espaço |
| Mover campos na hierarquia não muda o esquema | Sem `NOT NULL` nas colunas específicas |
| Consulta polimórfica simples | Tabela cresce e pode virar gargalo; nomes de coluna podem colidir |

- **Integridade:** restrições por subclasse só com `CHECK` condicionais.
- **Legibilidade:** a tabela mistura conceitos diferentes.

## Diagrama

```mermaid
classDiagram
    class PaymentInstruction {
        -Long id
        -long amountCents
        -String status
    }
    class PixTransfer {
        -String pixKey
        -String endToEndId
    }
    class TedTransfer {
        -String bankCode
        -String branch
        -String accountNumber
    }
    class PaymentInstructionsTable {
        <<table>>
        id
        type
        amount_cents
        status
        pix_key
        end_to_end_id
        bank_code
        branch
        account_number
    }
    PaymentInstruction <|-- PixTransfer
    PaymentInstruction <|-- TedTransfer
    PaymentInstruction ..> PaymentInstructionsTable
```

Toda a hierarquia fica em `PaymentInstructionsTable`; a coluna `type` identifica a subclasse e as colunas específicas ficam nulas nas demais. A fonte do Fowler ilustra o padrão com a hierarquia `Player`; aqui ela é substituída por `PaymentInstruction`, a mesma nos quatro padrões de herança.

## Exemplo

Uma hierarquia de instruções de pagamento é mapeada em uma só tabela, `payment_instructions`, com discriminador.

```java
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "type")
public abstract class PaymentInstruction {
    @Id @GeneratedValue
    private Long id;
    private long amountCents;
    private String status;
}

@Entity
@DiscriminatorValue("PIX")
public class PixTransfer extends PaymentInstruction {
    private String pixKey;
    private String endToEndId;
}

@Entity
@DiscriminatorValue("TED")
public class TedTransfer extends PaymentInstruction {
    private String bankCode;
    private String branch;
    private String accountNumber;
}
```

No EF Core, é o padrão Table-per-Hierarchy (TPH).
## Padrões relacionados

- [Class Table Inheritance](/design/poeaa/object-relational-structural/class-table-inheritance) — uma tabela por classe, com joins.
- [Concrete Table Inheritance](/design/poeaa/object-relational-structural/concrete-table-inheritance) — uma tabela por classe concreta, sem joins entre tipos.
- [Inheritance Mappers](/design/poeaa/object-relational-structural/inheritance-mappers) — estrutura de mapeadores usada com qualquer um dos três esquemas.
- [Embedded Value](/design/poeaa/object-relational-structural/embedded-value) — outro caso de colunas agrupadas na tabela do dono.

## Referência

- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/singleTableInheritance.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
- [Single Table Inheritance na Wikipedia](https://en.wikipedia.org/wiki/Single_Table_Inheritance)
