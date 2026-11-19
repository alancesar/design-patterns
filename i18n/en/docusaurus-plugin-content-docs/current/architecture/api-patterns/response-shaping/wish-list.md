---
title: Wish List
pattern_slug: wish-list
category: Response Shaping
tags:
  - Performance
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Wish List"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/response-shaping/wish-list.mdx';

# Wish List

## Description

The Wish List pattern lets the client enumerate, in the request itself, the data elements it wants, and the provider returns only those elements in the response. It is the simplest way to shape the response (response shaping) to the needs of each consumer.

The list is usually an [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) or a flat [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree), such as `fields=a,b,c` in the query string. A special case is a single [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) for the level of detail (`minimal`, `medium`, `full`). On the provider, a list evaluator can translate the list into a filter on the data source (for example, the columns of a `SELECT`) or fetch everything and select the fields when assembling the response. Common variants: **expansion**, where the first response is lean and points to fields that can be requested later, and the use of **wildcards**, such as `*` or `holder.*`.

## Problems it solves

- Clients with different information needs consuming the same operation
- Responses bloated with fields most clients ignore, wasting network and processing
- Proliferation of specialized operations, one for each combination of fields
- Unnecessary load on the data source when only part of the attributes is used

## When to use

- When the network is limited (mobile apps) and clients usually need only a subset of the data
- When the resource has many attributes and there are very distinct consumption profiles
- When you want to honor the principle of data parsimony (Datensparsamkeit)
- When the response structure is simple enough to be described by field names

## When to avoid

- When clients almost always use everything, and the list would only add complexity
- When the response has a nested structure that must be selected by levels: prefer the [Wish Template](/architecture/api-patterns/response-shaping/wish-template)
- When exposing field names would couple clients too tightly to the internal data model
- When the team cannot afford the extra testing and maintenance

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Less data on the network and less load on the data source | The provider gains extra logic in the service and data access layers |
| A single contract serves clients with different needs | Field names expose the data model and increase coupling |
| Avoids operations tailored to each client | More test surface, with many field combinations |
| Easy to understand and document, because it is flat | Typos may be silently ignored, hiding the problem |

- **Unknown fields:** decide between rejecting with an [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) or ignoring; ignoring hides spelling mistakes and renames.
- **Evolution:** renaming an attribute breaks clients that list it, so the list becomes part of the contract.
- **Security:** validate the list and apply per-field authorization, since the client chooses what comes out.
- **Default value:** with no list, return a default set and document it.
- **Variants:** expansion and wildcards help, but are harder to build and to understand.

## Diagram

<Diagram />

The evaluator reads the wish list from the request and restricts the query or the response assembly to the enumerated fields.

## Example

In the fintech's digital account API, `Account` has several attributes, but a balance screen needs only two. The client builds the list in the query string. Amounts in cents.

```http
GET /accounts/acc-123?fields=accountId,balanceCents
```

```json
{ "accountId": "acc-123", "balanceCents": 152340 }
```

The selection on the provider, rejecting unknown fields:

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;

public class Main {
    static final Map<String, Object> ACCOUNT = Map.of(
            "accountId", "acc-123", "holder", "Maria Silva",
            "balanceCents", 152340, "currency", "BRL", "status", "ACTIVE");

    static Map<String, Object> shape(String fields) {
        Map<String, Object> out = new LinkedHashMap<>();
        for (String f : fields.split(",")) {
            if (!ACCOUNT.containsKey(f)) {
                throw new IllegalArgumentException("unknown field: " + f);
            }
            out.put(f, ACCOUNT.get(f));
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(shape("accountId,balanceCents")); // {accountId=acc-123, balanceCents=152340}
        try {
            shape("accountId,saldo");
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage()); // unknown field: saldo
        }
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from typing import Any, Dict

ACCOUNT = {"accountId": "acc-123", "holder": "Maria Silva",
           "balanceCents": 152340, "currency": "BRL", "status": "ACTIVE"}

def shape(fields: str) -> Dict[str, Any]:
    out = {}
    for f in fields.split(","):
        if f not in ACCOUNT:
            raise ValueError("unknown field: " + f)
        out[f] = ACCOUNT[f]
    return out

out = shape("accountId,balanceCents")
print("{" + ", ".join(f"{k}={v}" for k, v in out.items()) + "}")  # {accountId=acc-123, balanceCents=152340}
try:
    shape("accountId,saldo")
except ValueError as e:
    print(e)  # unknown field: saldo
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"strings"
)

var account = map[string]any{
	"accountId": "acc-123", "holder": "Maria Silva",
	"balanceCents": 152340, "currency": "BRL", "status": "ACTIVE",
}

// Go: the error is a return value, not an exception.
func shape(fields string) (map[string]any, error) {
	out := map[string]any{}
	for _, f := range strings.Split(fields, ",") {
		v, ok := account[f]
		if !ok {
			return nil, fmt.Errorf("unknown field: %s", f)
		}
		out[f] = v
	}
	return out, nil
}

func main() {
	fields := "accountId,balanceCents"
	out, _ := shape(fields)
	parts := []string{}
	for _, f := range strings.Split(fields, ",") {
		parts = append(parts, fmt.Sprintf("%s=%v", f, out[f]))
	}
	fmt.Println("{" + strings.Join(parts, ", ") + "}") // {accountId=acc-123, balanceCents=152340}
	if _, err := shape("accountId,saldo"); err != nil {
		fmt.Println(err) // unknown field: saldo
	}
}
```

</TabItem>
</Tabs>

## Related patterns

- [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — same problem, but with a nested structure instead of a flat list
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — reduces the response by splitting collections into pages; combines well with the Wish List
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request) — avoids resending what the client already has; can be added to cut transfer even further
- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — less data per response helps respect the quota
- [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) — the typical form of the wish list
- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) and [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — field expansion decides, per request, between embedding and linking
- [Backends for Frontends](/architecture/cloud-design-patterns/gateways-and-edge/backends-for-frontends) — another answer to the problem of different clients, with one backend per client instead of a configurable contract

## Reference

- [Patterns for API Design, chapter 7: Wish List](https://api-patterns.org/)
