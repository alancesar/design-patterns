---
title: Retrieval Operation
pattern_slug: retrieval-operation
category: Operation Responsibilities
tags:
  - Performance
  - Decoupling
source: https://api-patterns.org/
sidebar_label: "Retrieval Operation"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/operation-responsibilities/retrieval-operation.mdx';

# Retrieval Operation

## Descrição

O padrão Retrieval Operation é uma operação de API somente leitura que devolve ao cliente uma representação legível por máquina de informações mantidas pelo provedor, com recursos de busca, filtro e formatação. Ela acessa o estado do provedor, mas não o altera: o único efeito colateral aceitável é o de infraestrutura, como registros de acesso.

A operação serve a necessidades de informação ad hoc ou periódicas, como o extrato de um mês, e muitas vezes devolve os dados em uma estrutura diferente da do modelo de domínio interno. Consultas simples usam parâmetros atômicos e devolvem uma árvore de parâmetros; cenários mais ricos recorrem a uma linguagem de consulta declarativa. Variantes conhecidas são o Status Check (consulta de progresso), o Time-Bound Report (relatório por período) e o Business Rule Validator (validação de uma regra contra o estado existente).

## Problemas que resolve

- Consumidores que precisam consultar dados do provedor sem copiar o banco inteiro para si
- Dados em um formato interno que não serve às necessidades de informação dos clientes
- Necessidade de delimitar escopo, critérios e período de um relatório
- Cargas de leitura que precisam escalar de forma independente das escritas

## Quando usar

- Para extratos, listagens, buscas e relatórios sobre dados de um endpoint
- Para consultar o andamento de um processo em execução (status check)
- Para relatórios de um intervalo de tempo, como o extrato mensal de uma conta
- Quando se deseja separar o modelo de leitura do de escrita, como em CQRS

## Quando evitar

- Quando a chamada precisa alterar estado: use uma [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) ou uma [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation)
- Quando o resultado depende só da entrada e não do estado: uma [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) é mais simples
- Para fluxos contínuos de alta velocidade, em que um modelo de streaming é mais adequado que repetidas consultas
- Quando as consultas exigem agregações tão pesadas que deveriam ser pré-calculadas em uma réplica analítica

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Leitura sem efeitos colaterais, fácil de escalar replicando dados | Pode virar gargalo se as consultas pedidas não combinarem com a forma como os dados são guardados |
| Clientes obtêm só o que precisam, com filtros e formatos | Quanto mais flexível a consulta, mais difícil proteger, otimizar e documentar |
| Fácil de cachear e de expor como API pública de dados | Respostas podem conter dados sensíveis e exigem controle de acesso |
| Separa o modelo de leitura do de escrita | Réplicas de leitura podem estar defasadas em relação à escrita |

- **Volume:** use [Pagination](/architecture/api-patterns/response-shaping/pagination) quando o resultado puder ser grande.
- **Tamanho das respostas:** um [Wish List](/architecture/api-patterns/response-shaping/wish-list) ou [Wish Template](/architecture/api-patterns/response-shaping/wish-template) deixa o cliente moldar a resposta.
- **Interpretação:** [Metadata Elements](/architecture/api-patterns/element-stereotypes/metadata-element) evitam leituras equivocadas dos dados.
- **Segurança:** em APIs públicas, combine com [API Key](/architecture/api-patterns/special-purpose-representations/api-key) e [Rate Limit](/architecture/api-patterns/documentation/rate-limit).

## Diagrama

<Diagram />

A consulta chega com os critérios de busca, o provedor lê o estado sem escrever e devolve um relatório com o recorte pedido.

## Exemplo

O aplicativo da fintech mostra o extrato de uma conta em um período. A operação filtra os lançamentos por data e nunca altera o razão.

```http
GET /accounts/acc-42/ledger-entries?from=2026-11-01&to=2026-11-15&limit=50 HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "accountId": "acc-42",
  "from": "2026-11-01",
  "to": "2026-11-15",
  "entries": [
    { "id": "le-2", "bookedOn": "2026-11-03", "amountCents": 250000, "description": "Pix recebido" },
    { "id": "le-3", "bookedOn": "2026-11-10", "amountCents": -12000, "description": "Compra no cartão" }
  ]
}
```

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;
import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        StatementService service = new StatementService(List.of(
                new LedgerEntry("le-1", LocalDate.parse("2026-10-28"), -4_990, "Boleto de energia"),
                new LedgerEntry("le-2", LocalDate.parse("2026-11-03"), 250_000, "Pix recebido"),
                new LedgerEntry("le-3", LocalDate.parse("2026-11-10"), -12_000, "Compra no cartão"),
                new LedgerEntry("le-4", LocalDate.parse("2026-11-20"), -3_000, "Tarifa")));
        List<LedgerEntry> page = service.findByPeriod(
                LocalDate.parse("2026-11-01"), LocalDate.parse("2026-11-15"));
        page.forEach(e -> System.out.println(e.id())); // le-2, le-3
    }
}

record LedgerEntry(String id, LocalDate bookedOn, long amountCents, String description) {}

class StatementService {
    private final List<LedgerEntry> ledger;

    StatementService(List<LedgerEntry> ledger) { this.ledger = ledger; }

    // Somente leitura: filtra o razão sem alterá-lo.
    List<LedgerEntry> findByPeriod(LocalDate from, LocalDate to) {
        return ledger.stream()
                .filter(e -> !e.bookedOn().isBefore(from) && !e.bookedOn().isAfter(to))
                .toList();
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass(frozen=True)
class LedgerEntry:
    id: str
    booked_on: date
    amount_cents: int
    description: str

class StatementService:
    def __init__(self, ledger: List[LedgerEntry]) -> None:
        self._ledger = ledger

    # Somente leitura: filtra o razão sem alterá-lo.
    def find_by_period(self, start: date, end: date) -> List[LedgerEntry]:
        return [e for e in self._ledger if start <= e.booked_on <= end]

service = StatementService([
    LedgerEntry("le-1", date(2026, 10, 28), -4_990, "Boleto de energia"),
    LedgerEntry("le-2", date(2026, 11, 3), 250_000, "Pix recebido"),
    LedgerEntry("le-3", date(2026, 11, 10), -12_000, "Compra no cartão"),
    LedgerEntry("le-4", date(2026, 11, 20), -3_000, "Tarifa"),
])
for entry in service.find_by_period(date(2026, 11, 1), date(2026, 11, 15)):
    print(entry.id)  # le-2, le-3
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
)

type LedgerEntry struct {
	ID          string
	BookedOn    string // formato ISO (AAAA-MM-DD), comparável como texto
	AmountCents int64
	Description string
}

type StatementService struct {
	ledger []LedgerEntry
}

// Somente leitura: filtra o razão sem alterá-lo.
func (s *StatementService) FindByPeriod(from, to string) []LedgerEntry {
	var result []LedgerEntry
	for _, e := range s.ledger {
		if e.BookedOn >= from && e.BookedOn <= to {
			result = append(result, e)
		}
	}
	return result
}

func main() {
	service := &StatementService{ledger: []LedgerEntry{
		{"le-1", "2026-10-28", -4_990, "Boleto de energia"},
		{"le-2", "2026-11-03", 250_000, "Pix recebido"},
		{"le-3", "2026-11-10", -12_000, "Compra no cartão"},
		{"le-4", "2026-11-20", -3_000, "Tarifa"},
	}}
	for _, e := range service.FindByPeriod("2026-11-01", "2026-11-15") {
		fmt.Println(e.ID) // le-2, le-3
	}
}
```

</TabItem>
</Tabs>

## Padrões relacionados

- [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) — empurra dados para o provedor; a Retrieval Operation os puxa
- [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) — lê e também escreve o estado
- [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) — não acessa o estado; uma Retrieval Operation sempre o lê
- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — o endpoint que mais expõe essas operações
- [Pagination](/architecture/api-patterns/response-shaping/pagination), [Wish List](/architecture/api-patterns/response-shaping/wish-list) e [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — controlam volume e forma das respostas
- [Repository](/design/poeaa/object-relational-metadata-mapping/repository) — abstração interna de consulta; a Retrieval Operation é a sua contraparte exposta pela API
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request) — evita reenviar dados que o cliente já tem

## Referência

- [Patterns for API Design, capítulo 5: Retrieval Operation](https://api-patterns.org/)
