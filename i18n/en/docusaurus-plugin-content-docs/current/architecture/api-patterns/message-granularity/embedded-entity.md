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

## Description

The Embedded Entity pattern includes, inside the representation of a data element, the full data of the elements related to it, so that the receiver gets everything in a single message.

For each relationship the receiver usually follows, the provider embeds in the message a [Data Element](/architecture/api-patterns/element-stereotypes/data-element) with the data from the other end of the relation, inside the representation of the source. The result is a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree): nested objects for containment hierarchies, lists for one-to-many relations. Metadata can indicate the type of each relation.

The analysis is repeated transitively: for each newly included element, it is assessed whether its relations are also worth including, until everything reachable has been included or excluded (and cycles are detected). If the answer is "rarely", the way out is to reference the data with a [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder). The [API Description](/architecture/api-patterns/documentation/api-description) must explain the existence, structure and meaning of the embedded elements.

## Problems it solves

- Clients that need several sequential calls to assemble a complete view, following references one by one
- Conversation state and request coordination that hurt scalability and availability when the data is scattered
- Inconsistency between reads made at different moments: a single snapshot is internally coherent, while links can break or point to data that has since changed
- Dedicated endpoints for each element that exist only to resolve references

## When to use

- When the related data is used together in most cases, such as a credit contract and its installments
- When there is a single consumer, or homogeneous consumers, and the required data set is known, as with a [Backend for Frontend](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends)
- When a consistent picture of a specific moment must be delivered, with no risk of a link target disappearing
- When the latency of several round trips is the main integration problem

## When to avoid

- When many different clients, possibly unknown, need distinct subsets of the data: the tendency is to include more than most of them use
- When the related elements change at very different speeds: the message can only be cached as a whole
- When the embedded data has stricter privacy classification or access control than its source
- When the relation graph is large or deep, producing heavy messages on slow or unreliable networks

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Fewer calls and less accumulated latency | Larger messages, which consume more bandwidth and transfer time |
| Consistent snapshot, with no broken links | Only the whole message can be cached, even if just one part changed |
| Fewer endpoints to build and operate | Hard to remove later: clients start depending on the embedded data |
| Uniform structure that simplifies client development | Risk of leaking restricted data, and of redundancy when the same entity appears in several places |

- **Cycles:** in bidirectional relationships, embed only one direction and use an [Id Element](/architecture/api-patterns/element-stereotypes/id-element) or [Link Element](/architecture/api-patterns/element-stereotypes/link-element) in the other, to avoid duplication and infinite loops.
- **Sizing:** measure message sizes and the real use of fields; if most of it is ignored, switch to referencing.
- **Evolution:** it is possible to switch between embedding and referencing over time, even offering both versions in parallel with [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production).
- **Hybrid:** embed what the interface displays immediately and reference the rest for on-demand retrieval.

## Diagram

<Diagram />

A single call returns the source element and the related elements, with no follow-up requests.

## Example

In the fintech, the personal credit contract (`LoanContract`) is almost always displayed together with the account (`Account`) that received the funds and with its installments. Instead of three calls, the response embeds both.

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

The same contract assembled on the provider, in each language (the output is the JSON above, on one line):

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
    // The Account and the installments are embedded in the contract representation.
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


# The Account and the installments are embedded in the contract representation.
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

// The Account and the installments are embedded in the contract representation.
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

Monetary values travel as integer cents plus currency, never as floating-point numbers.

## Related patterns

- [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — the opposite solution: instead of copying the related data, it sends a link to it
- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — the message structure that results from embedding entities
- [Data Element](/architecture/api-patterns/element-stereotypes/data-element) — the element type that carries the embedded data
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) and [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — let the client choose which parts to receive, tuning the embedded content
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) and [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — operational data usually references master data; references between holders of the same type tend to be embedded
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — the read operation that decides between embedding and referencing
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — also aggregates several objects to reduce remote calls; Embedded Entity describes the granularity decision for each relation inside it
- [Backends for Frontends](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) — with one specific consumer, embedding everything the screen needs is a reasonable strategy
- [API Description](/architecture/api-patterns/documentation/api-description) — must document the embedded elements

## Reference

- [Patterns for API Design, chapter 7: Embedded Entity](https://api-patterns.org/)
