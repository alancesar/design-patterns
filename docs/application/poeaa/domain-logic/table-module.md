---
title: Table Module
pattern_slug: table-module
category: Domain Logic
tags:
  - Simplicity
  - Performance
source: https://martinfowler.com/eaaCatalog/tableModule.html
sidebar_label: "Table Module"
---

# Table Module

## Descrição

O Table Module é uma única instância que trata a lógica de negócio de todas as linhas de uma tabela ou view do banco de dados. Há uma classe por tabela, e seus métodos recebem ou operam sobre um conjunto de dados tabular.

Diferente do Domain Model, que cria um objeto por registro (um objeto para cada pedido), o Table Module tem um único objeto `Orders` que processa todos os pedidos. Para identificar uma linha, o cliente passa uma chave ou o método recebe o registro como argumento.

O padrão funciona muito bem com Record Set, estruturas tabulares em memória fornecidas por plataformas como .NET (DataSet), que o integram a ferramentas de interface e de acesso a dados.

## Problemas que resolve

- Evitar o custo e a complexidade do mapeamento objeto-relacional de um Domain Model.
- Organizar a lógica em um lugar previsível, em vez de espalhá-la em scripts.
- Aproveitar plataformas e ferramentas orientadas a dados tabulares.

## Quando usar

- Quando a plataforma oferece suporte forte a Record Set e a controles de interface ligados a dados.
- Lógica de complexidade moderada, organizada em torno de tabelas.
- Quando se quer mais estrutura que o Transaction Script, sem o custo de um Domain Model.

### Quando evitar

- Quando as regras exigem polimorfismo, herança e relacionamentos ricos entre entidades.
- Quando a lógica cresce e se espalha entre muitos módulos de tabelas que precisam se chamar.
- Quando o suporte a Record Set da plataforma é fraco.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Estrutura mais clara que scripts soltos | Sem polimorfismo nem identidade por objeto |
| Dispensa mapeamento objeto-relacional | Acoplado ao formato tabular dos dados |
| Integra bem com ferramentas orientadas a dados | Lógica complexa fica difícil de expressar |
| Poucas consultas e operações em lote eficientes | Difícil migrar para Domain Model depois |

- **Desempenho:** processar muitas linhas de uma vez costuma ser eficiente.
- **Testabilidade:** exige montar Record Sets em memória, mas dispensa banco.
- **Evolução:** relações entre tabelas se tornam chamadas entre módulos.

## Diagrama

```mermaid
classDiagram
    class Client
    class OrdersModule {
        +total(orderId) decimal
        +applyDiscount(orderId)
    }
    class OrderItemsModule {
        +subtotal(orderId) decimal
    }
    class RecordSet
    class TableDataGateway
    Client --> OrdersModule
    OrdersModule --> OrderItemsModule
    OrdersModule --> RecordSet
    OrderItemsModule --> RecordSet
    TableDataGateway --> RecordSet
```

Cada tabela tem um módulo (`OrdersModule`, `OrderItemsModule`) que opera sobre um `RecordSet` carregado por um gateway de tabela.

## Exemplo

Um módulo `Orders` calcula o total de um pedido a partir do conjunto de itens carregado.

```csharp
public class OrderItems
{
    private readonly DataTable table;
    public OrderItems(DataTable table) { this.table = table; }

    public decimal Subtotal(int orderId) =>
        table.AsEnumerable()
             .Where(r => r.Field<int>("OrderId") == orderId)
             .Sum(r => r.Field<decimal>("Price") * r.Field<int>("Qty"));
}

public class Orders
{
    private readonly DataTable table;
    private readonly OrderItems items;
    public Orders(DataTable table, OrderItems items) { this.table = table; this.items = items; }

    public decimal Total(int orderId)
    {
        var row = table.AsEnumerable().Single(r => r.Field<int>("Id") == orderId);
        var subtotal = items.Subtotal(orderId);
        return row.Field<bool>("Vip") ? subtotal * 0.9m : subtotal;
    }
}
```

## Padrões relacionados

- [Transaction Script](./transaction-script.md) — organiza por requisição em vez de por tabela.
- [Domain Model](./domain-model.md) — um objeto por registro, em vez de um por tabela.
- [Record Set](../base/record-set.md) — estrutura tabular em memória na qual o Table Module opera.
- [Table Data Gateway](../data-source-architectural/table-data-gateway.md) — carrega os dados da tabela para o módulo.
- [Service Layer](./service-layer.md) — pode servir de fronteira sobre os módulos.

## Referência

- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/tableModule.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
