---
title: Request Bundle
pattern_slug: request-bundle
category: Message Exchange Optimization
tags:
  - Performance
source: https://api-patterns.org/
sidebar_label: "Request Bundle"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/message-exchange-optimization/request-bundle.mdx';

# Request Bundle

## Description

The Request Bundle pattern groups several independent requests into a single request message, to reduce the number of calls and responses exchanged between client and provider.

The message is a container with metadata, such as the identifier of each bundle element and an element counter. It is usually structured as a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) or a [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest). The response can take two forms: **a single bundled response**, where a container mirrors the received bundle, or **multiple responses** to one request, where the provider returns the results as each element is processed, for example through long polling.

The provider must split the bundle and assemble the response, and the client must split the bundled response back into individual results. Errors are handled at both levels: a report for the whole bundle and individual reports per element, found through the identifier.

## Problems it solves

- "Chatty" interactions, with many small independent requests that hurt scalability and throughput
- Latency accumulated by several round trips on high-latency networks
- Overhead of sending and receiving many messages for batch or bulk processing
- Client complexity in tracking several ongoing requests

## When to use

- When clients do batch processing, such as periodic loads or registration updates
- When the elements are logically independent and can be processed in any order
- When the network has high latency and the cost of each call dominates
- When the transport protocol cannot handle several requests at once

## When to avoid

- When the elements depend on each other or need a guaranteed execution order
- When the elements are all of the same kind and can be fetched with [Pagination](/architecture/api-patterns/response-shaping/pagination)
- When access control is per element and hard to communicate to the client in partial responses
- When the client needs the first response as early as possible, since the bundle only returns results after processing

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Fewer messages and round trips, with more throughput | The client waits longer for the first result |
| Fewer ongoing requests for the client to track | Provider and client must split and reassemble the bundle |
| Useful when the protocol does not support several requests together | More complex payload, with data from several sources in one message |
| Fewer calls counted by a [Rate Limit](/architecture/api-patterns/documentation/rate-limit) per invocation | May make the provider stateful, which hinders horizontal scaling |

- **Order:** the elements are independent and may run in parallel; document in the [API Description](/architecture/api-patterns/documentation/api-description) that the client must not assume an order. Guaranteeing order costs extra work.
- **Errors:** return success or failure per element with an [Error Report](/architecture/api-patterns/special-purpose-representations/error-report), not only for the whole bundle.
- **Size:** define a limit of elements per bundle to protect the provider.
- **Scaling unit:** it is not obvious whether the bundle or the element should be the unit of scaling; avoid state between calls.

## Diagram

<Diagram />

The endpoint splits the bundle into independent elements, processes each one and assembles a single response that mirrors the bundle. In the multiple-responses variant, the assembler is replaced by individual replies.

## Example

A fintech partner needs to generate several Pix charges at once, at the end of the day. Instead of one call per `PixCharge`, it sends a bundle; each element has a correlation identifier, and the result of each is returned individually, so an invalid amount does not block the other charges. The HTTP messages:

```http
POST /pix-charges/bundle HTTP/1.1
Content-Type: application/json

{
  "elements": [
    {"id": "1", "amountCents": 15000},
    {"id": "2", "amountCents": 0},
    {"id": "3", "amountCents": 4990}
  ]
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "results": [
    {"id": "1", "status": "CREATED", "detail": "charge-1"},
    {"id": "2", "status": "REJECTED", "detail": "amount must be positive"},
    {"id": "3", "status": "CREATED", "detail": "charge-3"}
  ]
}
```

In code, the provider validates the bundle size and processes each element independently, with amounts in cents:

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;

public class Main {
    record PixChargeRequest(String id, long amountCents) {}
    record ElementResult(String id, String status, String detail) {}

    static final int MAX_ELEMENTS = 100;

    // The elements are independent: one error does not bring down the others.
    static List<ElementResult> createCharges(List<PixChargeRequest> bundle) {
        if (bundle.size() > MAX_ELEMENTS) {
            throw new IllegalArgumentException("bundle exceeds " + MAX_ELEMENTS + " elements");
        }
        List<ElementResult> results = new ArrayList<>();
        for (PixChargeRequest element : bundle) {
            if (element.amountCents() <= 0) {
                results.add(new ElementResult(element.id(), "REJECTED", "amount must be positive"));
            } else {
                results.add(new ElementResult(element.id(), "CREATED", "charge-" + element.id()));
            }
        }
        return results;
    }

    public static void main(String[] args) {
        List<PixChargeRequest> bundle = List.of(
                new PixChargeRequest("1", 15000),
                new PixChargeRequest("2", 0),
                new PixChargeRequest("3", 4990));
        for (ElementResult r : createCharges(bundle)) {
            System.out.println(r.id() + " " + r.status() + " " + r.detail());
        }
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import List

MAX_ELEMENTS = 100


@dataclass
class PixChargeRequest:
    id: str
    amount_cents: int


@dataclass
class ElementResult:
    id: str
    status: str
    detail: str


# The elements are independent: one error does not bring down the others.
def create_charges(bundle: List[PixChargeRequest]) -> List[ElementResult]:
    if len(bundle) > MAX_ELEMENTS:
        raise ValueError(f"bundle exceeds {MAX_ELEMENTS} elements")
    results = []
    for element in bundle:
        if element.amount_cents <= 0:
            results.append(ElementResult(element.id, "REJECTED", "amount must be positive"))
        else:
            results.append(ElementResult(element.id, "CREATED", "charge-" + element.id))
    return results


bundle = [
    PixChargeRequest("1", 15000),
    PixChargeRequest("2", 0),
    PixChargeRequest("3", 4990),
]
for r in create_charges(bundle):
    print(r.id, r.status, r.detail)
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"errors"
	"fmt"
)

const maxElements = 100

type PixChargeRequest struct {
	ID          string
	AmountCents int64
}

type ElementResult struct {
	ID     string
	Status string
	Detail string
}

// The elements are independent: one error does not bring down the others.
func CreateCharges(bundle []PixChargeRequest) ([]ElementResult, error) {
	if len(bundle) > maxElements {
		return nil, errors.New("bundle exceeds the element limit")
	}
	results := make([]ElementResult, 0, len(bundle))
	for _, element := range bundle {
		if element.AmountCents <= 0 {
			results = append(results, ElementResult{element.ID, "REJECTED", "amount must be positive"})
		} else {
			results = append(results, ElementResult{element.ID, "CREATED", "charge-" + element.ID})
		}
	}
	return results, nil
}

func main() {
	bundle := []PixChargeRequest{{"1", 15000}, {"2", 0}, {"3", 4990}}
	results, err := CreateCharges(bundle)
	if err != nil {
		panic(err)
	}
	for _, r := range results {
		fmt.Println(r.ID, r.Status, r.Detail)
	}
}
```

</TabItem>
</Tabs>

## Related patterns

- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) and [Parameter Forest](/architecture/api-patterns/basic-structure/parameter-forest) — structure the request and response messages of the bundle
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) and [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — identify each element and describe the bundle
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — reports success or failure per element
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request), [Wish List](/architecture/api-patterns/response-shaping/wish-list) and [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — can be combined, as long as the gain justifies the complexity
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — alternative when the requested elements are of the same kind
- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — bundles help stay within limits that count invocations
- [Request Batch](/architecture/distributed-systems/node-communication/request-batch) — also groups requests to reduce messages, but between nodes of a distributed system; here the focus is the contract of an API between client and provider
- [Correlation Identifier](/architecture/eip/message-construction/correlation-identifier) — the element identifiers play this role, tying each result to its originating request
- [Command Message](/architecture/eip/message-construction/command-message) — each request in the bundle can be seen as a command

## Reference

- [Patterns for API Design, chapter 7: Request Bundle](https://api-patterns.org/)
