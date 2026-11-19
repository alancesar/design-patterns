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

## Description

The Linked Information Holder pattern keeps messages small by replacing related data with links to endpoints that expose it, letting the client fetch each part only when it needs it.

Instead of copying the content from the other end of a relation, the message carries a [Link Element](/architecture/api-patterns/element-stereotypes/link-element) that points to a separate [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource). The link can come with a [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) that describes the relation type, the HTTP method to use or the expected format. When the relation is many-to-many, a dedicated endpoint can represent the relation itself, with operations to list sources, targets and to find the other end of a known relation.

The pattern makes an implicit promise to the receiver: the link can be followed. The provider must decide for how long it keeps that promise, and clients should tolerate redirects. Unlike Embedded Entity, cycles in the data are less of a problem, because the responsibility for avoiding infinite loops moves from the sender to the receiver.

## Problems it solves

- Large messages that overload the network and processing when most clients use only part of the data
- Coupling between data consumers with different needs, by forcing all of them to receive the complete set
- Data that changes at different speeds, retransmitted together even when only one part changed
- Data with different protection levels, which benefits from endpoints with their own access controls

## When to use

- When there are several clients with different use cases and not all of them need the complete data
- When the referenced data is rich and serves several scenarios, such as registries and master data referenced by operational data
- When the related data has distinct change rhythms or security classifications, and each is worth caching separately
- When the domain model is complex and delivering everything at once would result in very heavy messages

## When to avoid

- When nearly every client always follows the links: the cost of several calls exceeds that of one larger message
- When the network has high latency and the number of follow-up requests is the bottleneck
- When a consistent picture of one instant is required, since link targets can change between calls
- When the provider does not want to, or cannot, keep links stable over time

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Smaller messages, with less bandwidth and processing per call | More requests to obtain the complete set, which can increase total latency |
| Independent caching for each part, according to its rate of change | Additional endpoints to build, operate and protect |
| Own access controls for sensitive data | Links can break if data is moved or removed |
| Modular design where each client takes only what it uses | The API gains dependencies between endpoints that must be managed |

- **Link promise:** define how long links are valid and how the client should react to redirects; a [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) helps keep links consistent.
- **Method and format:** if the API does not document that `GET` is the default for following links, include the method in metadata.
- **Measurement:** only switch between embedding and referencing based on performance measurements, not guesses.
- **Evolution:** it is possible to migrate in both directions over time, even keeping both forms in parallel with [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production).

## Diagram

<Diagram />

The first response is light; the related data comes in separate calls, on demand.

## Example

The fintech account (`Account`) response carries the balance and status, and references ledger entries (`LedgerEntry`) and cards (`Card`) through links. An app that only shows the balance does not pay for the whole statement.

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

The provider builds this representation in each language (the output is the JSON above, on one line):

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
    // The representation carries only the summary and links to the parts the client can fetch later.
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


# The representation carries only the summary and links to the parts the client can fetch later.
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

// The representation carries only the summary and links to the parts the client can fetch later.
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

The client decides whether to follow each link: by default with `GET`, which the API description should document.

## Related patterns

- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) — the opposite solution: copies the related data into the message instead of referencing it
- [Link Element](/architecture/api-patterns/element-stereotypes/link-element) — the element that carries the address of the referenced data
- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the kind of endpoint the links usually point to
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — keeps links stable and helps deal with broken links
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) and [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — operational data references master data, either flattened (Embedded Entity) or progressively (links)
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request), [Wish List](/architecture/api-patterns/response-shaping/wish-list), [Wish Template](/architecture/api-patterns/response-shaping/wish-template) and [Pagination](/architecture/api-patterns/response-shaping/pagination) — other ways to reduce the volume of data exchanged
- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) — allows offering both granularity forms during a migration
- [Lazy Load](/design/poeaa/object-relational-behavioral/lazy-load) — the analogous idea inside the object: related data is loaded only when accessed
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — a partial DTO, with links to the rest, is the in-memory variant of the same decision

## Reference

- [Patterns for API Design, chapter 7: Linked Information Holder](https://api-patterns.org/)
