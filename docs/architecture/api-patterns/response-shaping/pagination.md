---
title: Pagination
pattern_slug: pagination
category: Response Shaping
tags:
  - Performance
  - Security
source: https://api-patterns.org/
sidebar_label: "Pagination"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/response-shaping/pagination.mdx';

# Pagination

## Descrição

O padrão Pagination divide um conjunto grande de dados em partes menores, as páginas, e entrega uma página por mensagem de resposta, com informações para o cliente pedir as seguintes. Assim o provedor não precisa montar, e o cliente não precisa consumir, uma coleção inteira de uma só vez.

O tamanho da página pode ser fixo no contrato ou escolhido pelo cliente com um teto definido pelo provedor. Cada resposta traz, além dos itens, [Metadata Elements](/architecture/api-patterns/element-stereotypes/metadata-element) (tamanho da página, total, posição) e, de preferência, um [Link Element](/architecture/api-patterns/element-stereotypes/link-element) para a próxima página. O livro descreve quatro variantes: por **página** (o cliente pede o índice da página), por **offset** (o cliente pede quantos itens pular e quantos ler), por **cursor** (o cliente devolve um identificador opaco do último item visto) e por **tempo** (parecida com o cursor, mas com marcas de tempo). As duas primeiras são equivalentes entre si e ficam inconsistentes se a coleção muda entre as requisições, pois um item pode ser pulado ou repetido. O cursor não depende da posição absoluta e resolve esse problema, mas em geral não permite saltar para uma página arbitrária.

## Problemas que resolve

- Respostas enormes que esgotam memória e rede, no provedor ou no cliente, quando a coleção cresce
- Tempos de resposta altos para quem só precisa dos primeiros itens (por exemplo, as últimas transações de um extrato)
- Consultas sem limite que viram vetor de negação de serviço
- Falta de um modo padronizado de navegar por uma coleção grande, item a item ou página a página

## Quando usar

- Em endpoints que devolvem coleções cujo tamanho é grande ou desconhecido, como extratos, listas de boletos e histórico de Pix
- Quando o consumidor (pessoa ou aplicação) lê os dados de forma sequencial e raramente precisa de tudo
- Em replicações em lote entre sistemas, em que a transferência precisa ser retomável
- Quando a coleção muda enquanto é lida e a leitura precisa ser estável (use a variante por cursor)

## Quando evitar

- Quando a resposta não é um conjunto de itens e não pode ser fatiada
- Quando as coleções são pequenas e limitadas, e uma única mensagem é mais simples
- Quando o cliente precisa do conjunto completo de uma vez, por exemplo para ordenar ou buscar no próprio lado; nesse caso considere um [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource)
- Quando o acesso aleatório a páginas é requisito central e o cursor opaco não atende

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Respostas pequenas e previsíveis, com menos memória e latência | Uma chamada vira uma conversa, com mais mensagens e mais código no cliente |
| Limita o dano de consultas abusivas, se o tamanho máximo da página for imposto | O provedor pode ainda carregar tudo na memória por descuido e perder o ganho |
| O cliente processa os dados aos poucos e pode parar a qualquer momento | Mudanças em itens de páginas já lidas passam despercebidas |
| O cursor dá leitura estável mesmo com inserções concorrentes | O cursor opaco impede o acesso aleatório e deve ser tratado como contrato |

- **Ordenação:** a ordem dos itens não pode mudar durante a paginação, e alterá-la numa nova versão da API pode quebrar clientes sem aviso.
- **Tamanho da página:** páginas pequenas aumentam o número de chamadas; defina um padrão e um máximo.
- **Estado:** decida por quanto tempo valem os cursores ou resultados intermediários e se as requisições precisam ser idempotentes.
- **Filtros:** filtre antes de paginar, e não o contrário, para reduzir o trabalho.
- **Consistência:** a paginação lida com itens novos, mas raramente com alterações em itens já entregues.

## Diagrama

<Diagram />

O cliente segue o link `next` até ele deixar de aparecer. O cursor guarda o último item visto, então inserções no início do extrato não deslocam as páginas seguintes.

## Exemplo

Um extrato da conta digital da fintech devolve lançamentos (`LedgerEntry`) por cursor, com no máximo 100 itens por página. Valores em centavos.

```http
GET /accounts/acc-123/entries?pageSize=2
```

```json
{
  "pageSize": 2,
  "entries": [
    { "id": 1, "amountCents": 15000 },
    { "id": 2, "amountCents": -4290 }
  ],
  "_links": { "next": { "href": "/accounts/acc-123/entries?pageSize=2&cursor=2" } }
}
```

A paginação em si, no lado do provedor e no laço do cliente:

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.List;

record LedgerEntry(long id, long amountCents) {}
record Page(List<LedgerEntry> items, Long nextCursor) {}

public class Main {
    static Page page(List<LedgerEntry> all, Long after, int size) {
        int max = Math.min(size, 100);
        List<LedgerEntry> rest = all.stream()
                .filter(e -> after == null || e.id() > after).toList();
        List<LedgerEntry> items = rest.subList(0, Math.min(max, rest.size()));
        Long next = rest.size() > max ? items.get(items.size() - 1).id() : null;
        return new Page(items, next);
    }

    public static void main(String[] args) {
        List<LedgerEntry> entries = List.of(new LedgerEntry(1, 15000), new LedgerEntry(2, -4290),
                new LedgerEntry(3, 800), new LedgerEntry(4, -12000), new LedgerEntry(5, 50000));
        Long cursor = null;
        do {
            Page p = page(entries, cursor, 2);
            System.out.println(p.items().stream().map(LedgerEntry::id).toList()
                    + " next=" + (p.nextCursor() == null ? "end" : p.nextCursor()));
            cursor = p.nextCursor();
        } while (cursor != null);
        // [1, 2] next=2 / [3, 4] next=4 / [5] next=end
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class LedgerEntry:
    id: int
    amount_cents: int

def page(entries: List[LedgerEntry], after: Optional[int], size: int) -> Tuple[List[LedgerEntry], Optional[int]]:
    size = min(size, 100)
    rest = [e for e in entries if after is None or e.id > after]
    items = rest[:size]
    next_cursor = items[-1].id if len(rest) > size else None
    return items, next_cursor

entries = [LedgerEntry(1, 15000), LedgerEntry(2, -4290), LedgerEntry(3, 800),
           LedgerEntry(4, -12000), LedgerEntry(5, 50000)]
cursor = None
while True:
    items, cursor = page(entries, cursor, 2)
    print([e.id for e in items], "next=" + ("end" if cursor is None else str(cursor)))
    if cursor is None:
        break
# [1, 2] next=2 / [3, 4] next=4 / [5] next=end
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"strings"
)

type LedgerEntry struct {
	ID          int64
	AmountCents int64
}

// next é nil na última página; o cursor é o id do último item visto.
func page(entries []LedgerEntry, after *int64, size int) (items []LedgerEntry, next *int64) {
	if size > 100 {
		size = 100
	}
	var rest []LedgerEntry
	for _, e := range entries {
		if after == nil || e.ID > *after {
			rest = append(rest, e)
		}
	}
	if len(rest) > size {
		items = rest[:size]
		last := items[size-1].ID
		next = &last
		return
	}
	return rest, nil
}

func main() {
	entries := []LedgerEntry{{1, 15000}, {2, -4290}, {3, 800}, {4, -12000}, {5, 50000}}
	var cursor *int64
	for {
		items, next := page(entries, cursor, 2)
		parts := []string{}
		for _, e := range items {
			parts = append(parts, fmt.Sprint(e.ID))
		}
		ids := "[" + strings.Join(parts, ", ") + "]"
		if next == nil {
			fmt.Println(ids, "next=end")
			break
		}
		fmt.Println(ids, fmt.Sprintf("next=%d", *next))
		cursor = next
	}
	// [1 2] next=2 / [3 4] next=4 / [5] next=end
}
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Wish List](/architecture/api-patterns/response-shaping/wish-list) e [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — reduzem o tamanho de cada item; a paginação reduz o número de itens por mensagem, e os dois podem ser combinados
- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) e [Link Element](/architecture/api-patterns/element-stereotypes/link-element) — carregam o tamanho, a posição e o link para a próxima página
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — a operação de leitura que costuma ser paginada
- [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) — alternativa quando o cliente precisa do conjunto inteiro, trocado como um recurso próprio
- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — páginas maiores e menos chamadas ajudam a ficar dentro da cota
- [Request Batch](/architecture/distributed-systems/node-communication/request-batch) — agrupa várias requisições em uma; a paginação fatia uma resposta em várias
- [Lazy Load](/design/poeaa/object-relational-behavioral/lazy-load) — mesma ideia de trazer os dados só quando necessários, dentro do acesso a dados

## Referência

- [Patterns for API Design, capítulo 7: Pagination](https://api-patterns.org/)
