---
title: Linked Information Holder
pattern_slug: linked-information-holder
category: Message Granularity
tags:
  - Performance
  - Decoupling
source: https://api-patterns.org/
sidebar_label: "Linked Information Holder"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/message-granularity/linked-information-holder.mdx';

# Linked Information Holder

## Descrição

O padrão Linked Information Holder mantém as mensagens pequenas ao substituir os dados relacionados por links para endpoints que os expõem, deixando o cliente buscar cada parte somente quando precisar dela.

Em vez de copiar o conteúdo do outro lado de uma relação, a mensagem leva um [Link Element](/architecture/api-patterns/element-stereotypes/link-element) que aponta para um [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) separado. O link pode vir acompanhado de um [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) que descreve o tipo da relação, o método HTTP a usar ou o formato esperado. Quando a relação é de muitos para muitos, pode-se criar um endpoint próprio que representa a relação, com operações para listar origens, destinos e para achar a outra ponta de uma relação conhecida.

O padrão faz uma promessa implícita ao receptor: o link pode ser seguido. O provedor precisa decidir por quanto tempo a cumpre, e os clientes devem tolerar redirecionamentos. Diferente do Embedded Entity, ciclos nos dados são menos problemáticos, porque a responsabilidade de evitar laços infinitos passa do emissor para o receptor.

## Problemas que resolve

- Mensagens grandes que sobrecarregam rede e processamento quando a maioria dos clientes usa só parte dos dados
- Acoplamento entre os consumidores de dados que não têm as mesmas necessidades, ao forçar todos a receber o conjunto completo
- Dados que mudam em velocidades diferentes, retransmitidos juntos mesmo quando só um deles mudou
- Dados com proteção diferente, que se beneficiam de endpoints com controles de acesso próprios

## Quando usar

- Quando há vários clientes com casos de uso diferentes e nem todos precisam do dado completo
- Quando o dado referenciado é rico e serve a vários cenários, como cadastros e dados mestres referenciados por dados operacionais
- Quando os dados relacionados têm ritmos de mudança ou classificações de segurança distintos, e vale cachear cada um separadamente
- Quando o modelo de domínio é complexo e entregar tudo de uma vez resultaria em mensagens muito pesadas

## Quando evitar

- Quando quase todo cliente sempre segue os links: o custo de várias chamadas supera o de uma mensagem maior
- Quando a rede tem alta latência e o número de requisições de acompanhamento é o gargalo
- Quando é preciso um retrato consistente de um instante, pois os alvos dos links podem mudar entre uma chamada e outra
- Quando o provedor não quer ou não consegue manter os links estáveis ao longo do tempo

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Mensagens menores, com menos uso de banda e de processamento por chamada | Mais requisições para obter o conjunto completo, o que pode aumentar a latência total |
| Cache independente para cada parte, conforme a velocidade de mudança | Endpoints adicionais para construir, operar e proteger |
| Controles de acesso próprios para dados sensíveis | Links podem quebrar se os dados forem movidos ou removidos |
| Design modular em que cada cliente pega só o que usa | A API passa a ter dependências entre endpoints que precisam ser gerenciadas |

- **Promessa de links:** defina por quanto tempo os links valem e como o cliente deve reagir a redirecionamentos; um [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) ajuda a manter os links consistentes.
- **Método e formato:** se a API não documenta que `GET` é o padrão para seguir links, inclua o método em metadados.
- **Medição:** só troque entre embutir e referenciar com base em medições de desempenho, não em palpites.
- **Evolução:** é possível migrar nos dois sentidos ao longo do tempo, inclusive mantendo as duas formas em paralelo com [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production).

## Diagrama

<Diagram />

A primeira resposta é leve; os dados relacionados vêm em chamadas separadas, sob demanda.

## Exemplo

A resposta da conta (`Account`) da fintech traz o saldo e o estado, e referencia lançamentos (`LedgerEntry`) e cartões (`Card`) por links. Um app que só mostra o saldo não paga pelo extrato inteiro.

```http
GET /accounts/acc-7f3a HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "acc-7f3a",
  "status": "ACTIVE",
  "balance": { "amountCents": 534210, "currency": "BRL" },
  "links": [
    { "rel": "entries", "href": "/accounts/acc-7f3a/entries" },
    { "rel": "cards", "href": "/accounts/acc-7f3a/cards" }
  ]
}
```

O provedor monta essa representação em cada linguagem (a saída é o JSON acima, em uma linha):

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.List;
import java.util.stream.Collectors;

record Money(long cents, String currency) {
    String json() { return "{\"amountCents\":" + cents + ",\"currency\":\"" + currency + "\"}"; }
}
record Account(String id, String status, Money balance) {}
record Link(String rel, String href) {}

public class Main {
    // A representação traz só o resumo e links para as partes que o cliente pode buscar depois.
    static String accountJson(Account a) {
        List<Link> links = List.of(
            new Link("entries", "/accounts/" + a.id() + "/entries"),
            new Link("cards", "/accounts/" + a.id() + "/cards"));
        String items = links.stream()
            .map(l -> "{\"rel\":\"" + l.rel() + "\",\"href\":\"" + l.href() + "\"}")
            .collect(Collectors.joining(","));
        return "{\"id\":\"" + a.id() + "\",\"status\":\"" + a.status() + "\",\"balance\":" + a.balance().json()
            + ",\"links\":[" + items + "]}";
    }

    public static void main(String[] args) {
        System.out.println(accountJson(new Account("acc-7f3a", "ACTIVE", new Money(534_210, "BRL"))));
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
import json
from dataclasses import dataclass, asdict


@dataclass
class Money:
    amountCents: int
    currency: str


@dataclass
class Account:
    id: str
    status: str
    balance: Money


# A representação traz só o resumo e links para as partes que o cliente pode buscar depois.
def account_json(account: Account) -> str:
    body = asdict(account)
    body["links"] = [
        {"rel": "entries", "href": "/accounts/%s/entries" % account.id},
        {"rel": "cards", "href": "/accounts/%s/cards" % account.id},
    ]
    return json.dumps(body, separators=(",", ":"))


print(account_json(Account("acc-7f3a", "ACTIVE", Money(534_210, "BRL"))))
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"encoding/json"
	"fmt"
)

type Money struct {
	AmountCents int64  `json:"amountCents"`
	Currency    string `json:"currency"`
}

type Link struct {
	Rel  string `json:"rel"`
	Href string `json:"href"`
}

type AccountView struct {
	ID      string `json:"id"`
	Status  string `json:"status"`
	Balance Money  `json:"balance"`
	Links   []Link `json:"links"`
}

// A representação traz só o resumo e links para as partes que o cliente pode buscar depois.
func accountView(id, status string, balance Money) AccountView {
	return AccountView{id, status, balance, []Link{
		{"entries", "/accounts/" + id + "/entries"},
		{"cards", "/accounts/" + id + "/cards"},
	}}
}

func main() {
	out, _ := json.Marshal(accountView("acc-7f3a", "ACTIVE", Money{534_210, "BRL"}))
	fmt.Println(string(out))
}
```

</TabItem>
</Tabs>

O cliente decide se segue cada link: por padrão, `GET`, o que a descrição da API deve documentar.

## Padrões relacionados

- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) — a solução oposta: copia o dado relacionado para dentro da mensagem em vez de referenciá-lo
- [Link Element](/architecture/api-patterns/element-stereotypes/link-element) — o elemento que carrega o endereço do dado referenciado
- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — o tipo de endpoint para o qual os links costumam apontar
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — mantém os links estáveis e ajuda a lidar com links quebrados
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) e [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — dados operacionais referenciam dados mestres, de forma achatada (Embedded Entity) ou progressiva (links)
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request), [Wish List](/architecture/api-patterns/response-shaping/wish-list), [Wish Template](/architecture/api-patterns/response-shaping/wish-template) e [Pagination](/architecture/api-patterns/response-shaping/pagination) — outras formas de reduzir o volume de dados trafegado
- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) — permite oferecer as duas formas de granularidade durante uma migração
- [Lazy Load](/design/poeaa/object-relational-behavioral/lazy-load) — a ideia análoga dentro do objeto: o dado relacionado só é carregado quando acessado
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — um DTO parcial, com links para o resto, é a variante em memória da mesma decisão

## Referência

- [Patterns for API Design, capítulo 7: Linked Information Holder](https://api-patterns.org/)
