---
title: Transaction Script
pattern_slug: transaction-script
category: Domain Logic
tags:
  - Simplicity
  - Performance
source: https://martinfowler.com/eaaCatalog/transactionScript.html
sidebar_label: "Transaction Script"
---

# Transaction Script

## Descrição

O Transaction Script organiza a lógica de negócio como procedimentos, com um procedimento para cada requisição vinda da camada de apresentação. Cada script recebe a entrada, valida, calcula, acessa o banco de dados (diretamente ou por um gateway fino) e devolve o resultado.

Uma aplicação corporativa pode ser vista como uma série de transações: algumas apenas exibem dados, outras os alteram. Cada transação ganha seu próprio script, que roda do começo ao fim de forma linear. Passos comuns podem ser extraídos para subprocedimentos, e vários scripts relacionados costumam ser agrupados em uma mesma classe.

É a forma mais direta de estruturar lógica de domínio e funciona bem enquanto as regras são simples. Quando a lógica cresce, a duplicação entre scripts tende a aumentar.

## Problemas que resolve

- Necessidade de implementar rapidamente casos de uso simples sem montar uma infraestrutura de objetos e mapeamento.
- Equipes sem experiência com modelagem de objetos que precisam de um estilo fácil de entender.
- Operações que se resumem a ler, calcular e gravar, onde cada requisição tem fluxo bem definido.

## Quando usar

- Lógica de negócio simples, com poucas regras e poucas interações entre elas.
- Aplicações que precisam de controle fino sobre as consultas SQL e sobre o desempenho.
- Sistemas pequenos, protótipos ou módulos de relatório e importação.

## Quando evitar

- Quando as regras são complexas e se repetem entre vários casos de uso: a duplicação entre scripts se acumula.
- Quando o domínio tem muitas variações de comportamento que se beneficiam de polimorfismo.
- Quando a aplicação deve crescer por muito tempo e a lógica espalhada em procedimentos ficará difícil de manter.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Simples de entender e de implementar | Lógica duplicada entre scripts à medida que o sistema cresce |
| Sem camada de mapeamento objeto-relacional; fácil controlar o SQL | Difícil de refatorar para um modelo mais rico depois |
| Limites de transação claros: um script, uma transação | Regras de negócio acopladas à estrutura das tabelas |
| Bom desempenho previsível | Testes dependem do banco ou de gateways simulados |

- **Complexidade:** cresce de forma não linear; o que começa simples vira um emaranhado de procedimentos.
- **Testabilidade:** boa para scripts pequenos, mas depende da separação entre lógica e acesso a dados.
- **Evolução:** a migração para Domain Model costuma ser custosa.

## Diagrama

```mermaid
classDiagram
    class Presentation
    class PaymentScripts {
        +payBoleto(accountId, barcode, amountCents)
        +reversePayment(paymentId)
        +reconcileSettlements(fileId)
    }
    class Gateway {
        +find(id)
        +insert(row)
        +update(row)
    }
    class Database
    Presentation --> PaymentScripts
    PaymentScripts --> Gateway
    Gateway --> Database
```

A camada de apresentação chama um script por requisição. Os scripts, agrupados em `PaymentScripts`, usam um gateway fino para acessar o `Database`.

## Exemplo

O app da fintech precisa pagar um boleto: validar o saldo, debitar a conta e gravar o pagamento. Um único procedimento faz todo o trabalho, em uma só transação.

```python
class PaymentScripts:
    def __init__(self, db):
        self.db = db

    def pay_boleto(self, account_id: int, barcode: str, amount_cents: int) -> int:
        with self.db.transaction():
            account = self.db.fetch_one(
                "SELECT balance_cents FROM accounts WHERE id = %s FOR UPDATE",
                account_id,
            )
            if account["balance_cents"] < amount_cents:
                raise ValueError("Saldo insuficiente")
            self.db.execute(
                "UPDATE accounts SET balance_cents = balance_cents - %s WHERE id = %s",
                amount_cents, account_id,
            )
            return self.db.insert(
                "INSERT INTO boleto_payments (account_id, barcode, amount_cents) "
                "VALUES (%s, %s, %s)",
                account_id, barcode, amount_cents,
            )
```

## Padrões relacionados

- [Domain Model](/design/poeaa/domain-logic/domain-model) — alternativa para lógica complexa, com objetos que combinam dados e comportamento.
- [Table Module](/design/poeaa/domain-logic/table-module) — organiza a lógica por tabela, em vez de por requisição.
- [Service Layer](/design/poeaa/domain-logic/service-layer) — pode ser implementado com scripts de transação como fronteira da aplicação.
- [Table Data Gateway](/design/poeaa/data-source-architectural/table-data-gateway) — gateway fino frequentemente usado pelos scripts para acessar o banco.
- [Command](/coding/gof/behavioral/command) — scripts podem ser organizados como objetos de comando, um por transação.

## Referência

- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/transactionScript.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
