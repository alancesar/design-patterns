---
title: Class Table Inheritance
pattern_slug: class-table-inheritance
category: Object-Relational Structural
tags:
  - Consistency
  - Extensibility
source: https://martinfowler.com/eaaCatalog/classTableInheritance.html
sidebar_label: "Class Table Inheritance"
---

# Class Table Inheritance

## Descrição

O Class Table Inheritance representa uma hierarquia de herança com uma tabela por classe. Cada tabela guarda apenas os campos declarados na própria classe, e as subclasses se ligam à tabela da superclasse por chave primária compartilhada.

Para carregar um objeto completo, o mapeador junta (join) as tabelas ao longo da cadeia de herança. Para saber o tipo concreto, usa-se um discriminador ou o resultado dos joins.

O esquema espelha o modelo de objetos, mantém o banco normalizado e permite `NOT NULL` nos campos de cada classe.

## Problemas que resolve

- Mapear herança com esquema normalizado e sem colunas nulas.
- Manter a relação direta entre classes do domínio e tabelas.
- Aplicar restrições de integridade por subclasse.

## Quando usar

- Quando as subclasses têm muitos campos próprios.
- Quando a integridade do esquema é prioridade.
- Quando referências para a superclasse (chave estrangeira) devem funcionar para qualquer subtipo.

## Quando evitar

- Quando o número de joins por consulta prejudica o desempenho.
- Quando a hierarquia muda de forma frequente, movendo campos entre tabelas.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Esquema normalizado, espelha o modelo | Joins em toda carga de objeto |
| `NOT NULL` por subclasse | Refatorar a hierarquia exige alterar tabelas |
| Chave estrangeira para a superclasse funciona | Hierarquias profundas geram consultas pesadas |

- **Desempenho:** custo cresce com a profundidade da hierarquia.
- **Manutenção:** uma alteração em uma classe toca a tabela correspondente.

## Diagrama

```mermaid
erDiagram
    PAYMENT_INSTRUCTION ||--o| PIX_TRANSFER : e
    PAYMENT_INSTRUCTION ||--o| TED_TRANSFER : e
    PAYMENT_INSTRUCTION {
        bigint id PK
        bigint amount_cents
        varchar status
    }
    PIX_TRANSFER {
        bigint id PK
        varchar pix_key
        varchar end_to_end_id
    }
    TED_TRANSFER {
        bigint id PK
        varchar bank_code
        varchar branch
        varchar account_number
    }
```

`PAYMENT_INSTRUCTION` guarda os campos comuns; `PIX_TRANSFER` e `TED_TRANSFER` guardam os específicos, compartilhando a mesma chave primária. A fonte do Fowler ilustra o padrão com a hierarquia `Player`; aqui ela é substituída por `PaymentInstruction`, a mesma nos quatro padrões de herança.

## Exemplo

Cada classe tem a própria tabela; o JPA une as tabelas com `JOINED`.

```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class PaymentInstruction {
    @Id @GeneratedValue
    private Long id;
    private long amountCents;
    private String status;
}

@Entity
public class PixTransfer extends PaymentInstruction {
    @Column(nullable = false)
    private String pixKey;
    private String endToEndId;
}

@Entity
public class TedTransfer extends PaymentInstruction {
    private String bankCode;
    private String branch;
    private String accountNumber;
}
```

No EF Core, é o Table-per-Type (TPT).

## Padrões relacionados

- [Single Table Inheritance](/design/poeaa/object-relational-structural/single-table-inheritance) — alternativa com uma tabela só.
- [Concrete Table Inheritance](/design/poeaa/object-relational-structural/concrete-table-inheritance) — alternativa com uma tabela por classe concreta.
- [Inheritance Mappers](/design/poeaa/object-relational-structural/inheritance-mappers) — organiza os mapeadores da hierarquia.
- [Foreign Key Mapping](/design/poeaa/object-relational-structural/foreign-key-mapping) — a ligação entre tabelas usa o mesmo princípio.
- [Identity Field](/design/poeaa/object-relational-structural/identity-field) — a chave compartilhada entre as tabelas.

## Referência

- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/classTableInheritance.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
