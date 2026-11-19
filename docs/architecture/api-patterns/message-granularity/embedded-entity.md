---
title: Embedded Entity
pattern_slug: embedded-entity
category: Message Granularity
tags:
  - Performance
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Embedded Entity"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/message-granularity/embedded-entity.mdx';

# Embedded Entity

## Descrição

O padrão Embedded Entity inclui, dentro da representação de um elemento de dados, os dados completos dos elementos relacionados a ele, para que o receptor obtenha tudo em uma única mensagem.

Para cada relacionamento que o receptor costuma seguir, o provedor embute na mensagem um [Data Element](/architecture/api-patterns/element-stereotypes/data-element) com os dados do outro lado da relação, dentro da representação da origem. O resultado é uma [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree): objetos aninhados para hierarquias de contenção, listas para relações de um para muitos. Metadados podem indicar o tipo de cada relação.

A análise é repetida de forma transitiva: a cada novo elemento incluído, avalia-se se suas relações também valem a pena, até que tudo o que é alcançável tenha sido incluído ou excluído (e ciclos sejam detectados). Se a resposta for "raramente", o caminho é referenciar o dado com um [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder). A [API Description](/architecture/api-patterns/documentation/api-description) precisa explicar a existência, a estrutura e o significado dos elementos embutidos.

## Problemas que resolve

- Clientes que precisam fazer várias chamadas em sequência para montar uma visão completa, seguindo referências uma a uma
- Estado de conversação e coordenação de requisições que prejudicam escalabilidade e disponibilidade quando os dados estão espalhados
- Inconsistência entre leituras feitas em momentos diferentes: um único snapshot é internamente coerente, enquanto links podem quebrar ou apontar para dados já alterados
- Endpoints dedicados a cada elemento que só existem para resolver referências

## Quando usar

- Quando os dados relacionados são usados juntos na maioria dos casos, como um contrato de crédito e suas parcelas
- Quando há um único consumidor, ou consumidores homogêneos, e o conjunto de dados necessário é conhecido, como em um [Backend for Frontend](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends)
- Quando é preciso entregar um retrato consistente de um momento específico, sem risco de o alvo de um link sumir
- Quando a latência de várias idas e voltas é o principal problema da integração

## Quando evitar

- Quando muitos clientes diferentes, possivelmente desconhecidos, precisam de subconjuntos distintos do dado: a tendência é incluir mais do que a maioria usa
- Quando os elementos relacionados mudam em velocidades muito diferentes: a mensagem só pode ser cacheada por inteiro
- Quando o dado embutido tem classificação de privacidade ou controle de acesso mais restritos do que o da origem
- Quando o grafo de relações é grande ou profundo, gerando mensagens pesadas em redes lentas ou instáveis

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Menos chamadas e menos latência acumulada | Mensagens maiores, que consomem mais banda e tempo de transferência |
| Snapshot consistente, sem links quebrados | Cache só da mensagem inteira, mesmo que só uma parte tenha mudado |
| Menos endpoints para construir e operar | Difícil de remover depois: clientes passam a depender do dado embutido |
| Estrutura uniforme que simplifica o desenvolvimento do cliente | Risco de vazar dado restrito, e de redundância quando a mesma entidade aparece em vários lugares |

- **Ciclos:** em relacionamentos bidirecionais, embuta apenas uma direção e use [Id Element](/architecture/api-patterns/element-stereotypes/id-element) ou [Link Element](/architecture/api-patterns/element-stereotypes/link-element) na outra, para evitar duplicação e laços infinitos.
- **Dimensionamento:** meça o tamanho das mensagens e o uso real dos campos; se a maior parte for ignorada, passe a referenciar.
- **Evolução:** é possível alternar entre embutir e referenciar ao longo do tempo, inclusive oferecendo as duas versões em paralelo com [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production).
- **Híbrido:** embuta o que a interface exibe de imediato e referencie o resto para busca sob demanda.

## Diagrama

<Diagram />

Uma única chamada devolve o elemento de origem e os elementos relacionados, sem requisições de acompanhamento.

## Exemplo

Na fintech, o contrato de crédito pessoal (`LoanContract`) é quase sempre exibido junto com a conta (`Account`) que recebeu o valor e com as parcelas. Em vez de três chamadas, a resposta embute os dois.

```http
GET /loan-contracts/loan-2041 HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "loan-2041",
  "status": "ACTIVE",
  "principal": { "amountCents": 1200000, "currency": "BRL" },
  "account": { "id": "acc-7f3a", "holder": "Marina Souza" },
  "installments": [
    { "number": 1, "dueDate": "2026-12-10", "amountCents": 112500 },
    { "number": 2, "dueDate": "2027-01-10", "amountCents": 112500 }
  ]
}
```

O mesmo contrato montado no provedor, em cada linguagem (a saída é o JSON acima, em uma linha):

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.List;
import java.util.stream.Collectors;

record Money(long cents, String currency) {
    String json() { return "{\"amountCents\":" + cents + ",\"currency\":\"" + currency + "\"}"; }
}
record Account(String id, String holder) {}
record Installment(int number, String dueDate, long cents) {}
record LoanContract(String id, String status, Money principal, Account account, List<Installment> installments) {}

public class Main {
    // O Account e as parcelas vão embutidos na representação do contrato.
    static String loanJson(LoanContract l) {
        String items = l.installments().stream()
            .map(i -> "{\"number\":" + i.number() + ",\"dueDate\":\"" + i.dueDate() + "\",\"amountCents\":" + i.cents() + "}")
            .collect(Collectors.joining(","));
        return "{\"id\":\"" + l.id() + "\",\"status\":\"" + l.status() + "\",\"principal\":" + l.principal().json()
            + ",\"account\":{\"id\":\"" + l.account().id() + "\",\"holder\":\"" + l.account().holder() + "\"}"
            + ",\"installments\":[" + items + "]}";
    }

    public static void main(String[] args) {
        var loan = new LoanContract("loan-2041", "ACTIVE", new Money(1_200_000, "BRL"),
            new Account("acc-7f3a", "Marina Souza"),
            List.of(new Installment(1, "2026-12-10", 112_500), new Installment(2, "2027-01-10", 112_500)));
        System.out.println(loanJson(loan));
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Money:
    amountCents: int
    currency: str


@dataclass
class Account:
    id: str
    holder: str


@dataclass
class Installment:
    number: int
    dueDate: str
    amountCents: int


@dataclass
class LoanContract:
    id: str
    status: str
    principal: Money
    account: Account
    installments: List[Installment]


# O Account e as parcelas vão embutidos na representação do contrato.
def loan_json(loan: LoanContract) -> str:
    return json.dumps(asdict(loan), separators=(",", ":"))


loan = LoanContract("loan-2041", "ACTIVE", Money(1_200_000, "BRL"), Account("acc-7f3a", "Marina Souza"),
                    [Installment(1, "2026-12-10", 112_500), Installment(2, "2027-01-10", 112_500)])
print(loan_json(loan))
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

type Account struct {
	ID     string `json:"id"`
	Holder string `json:"holder"`
}

type Installment struct {
	Number      int    `json:"number"`
	DueDate     string `json:"dueDate"`
	AmountCents int64  `json:"amountCents"`
}

type LoanContract struct {
	ID           string        `json:"id"`
	Status       string        `json:"status"`
	Principal    Money         `json:"principal"`
	Account      Account       `json:"account"`
	Installments []Installment `json:"installments"`
}

// O Account e as parcelas vão embutidos na representação do contrato.
func loanJSON(l LoanContract) (string, error) {
	b, err := json.Marshal(l)
	return string(b), err
}

func main() {
	loan := LoanContract{"loan-2041", "ACTIVE", Money{1_200_000, "BRL"}, Account{"acc-7f3a", "Marina Souza"},
		[]Installment{{1, "2026-12-10", 112_500}, {2, "2027-01-10", 112_500}}}
	out, _ := loanJSON(loan)
	fmt.Println(out)
}
```

</TabItem>
</Tabs>

Os valores monetários trafegam como centavos inteiros e moeda, nunca como número de ponto flutuante.

## Padrões relacionados

- [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — a solução oposta: em vez de copiar o dado relacionado, envia um link para ele
- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — a estrutura de mensagem que resulta de embutir entidades
- [Data Element](/architecture/api-patterns/element-stereotypes/data-element) — o tipo de elemento que carrega o dado embutido
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) e [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — deixam o cliente escolher quais partes receber, ajustando o conteúdo embutido
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) e [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — dados operacionais costumam referenciar dados mestres; referências entre holders do mesmo tipo tendem a ser embutidas
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — a operação de leitura que decide entre embutir e referenciar
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — também agrega vários objetos para reduzir chamadas remotas; o Embedded Entity descreve a decisão de granularidade de cada relação dentro dele
- [Backends for Frontends](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) — com um consumidor específico, embutir tudo o que a tela precisa é uma estratégia razoável
- [API Description](/architecture/api-patterns/documentation/api-description) — deve documentar os elementos embutidos

## Referência

- [Patterns for API Design, capítulo 7: Embedded Entity](https://api-patterns.org/)
