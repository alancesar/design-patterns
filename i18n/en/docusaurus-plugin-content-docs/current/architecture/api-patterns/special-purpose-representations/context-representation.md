---
title: Context Representation
pattern_slug: context-representation
category: Special-Purpose Representations
tags:
  - Decoupling
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Context Representation"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/special-purpose-representations/context-representation.mdx';

# Context Representation

## Description

The Context Representation pattern groups the context information exchanged between client and provider (identity, preferences, quality of service, correlation) into a dedicated, recognizable element inside the message body, instead of scattering it across the headers of the communication protocol.

The element is usually a [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) of low or medium complexity, made of [Metadata Elements](/architecture/api-patterns/element-stereotypes/metadata-element) such as correlation and session identifiers, priority, language, location, client version or credentials such as an [API Key](/architecture/api-patterns/special-purpose-representations/api-key). When there are only numbers or enumerations, an [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) is enough. Because it lives in the payload, the context crosses gateways, queues and protocol switches without depending on how each of them treats headers, and it stays under the API designer's control.

The pattern has two variants. The **global context** is valid for a whole conversation (several calls, a business process, nested calls in which the provider also acts as a client) and is handed over from operation to operation, like the correlation identifier or the user's token. The **local context** is valid only for the current message, like the message identifier or its time to live. Separating them in the structure makes clear who processes them: the global one is usually handled by gateways and shared libraries; the local one, by the operation's implementation.

## Problems it solves

- Control information (language, priority, correlation, credentials) that gets lost when crossing intermediaries or switching protocols
- Dependence on protocol-specific headers, which complicate migrating from HTTP to another transport
- Lack of a single, predictable place for metadata, which mixes it with business data
- Tracing and auditing a conversation that goes through several calls and services

## When to use

- When messages may cross gateways, buses or different protocols and the context must arrive intact
- When an operation depends on conversation metadata, such as correlation, session or token, handed over in chained calls
- When the API must be independent of the communication protocol
- When several operations share the same metadata and it is worth standardizing where it goes

## When to avoid

- When a single protocol is guaranteed and its standard headers (such as `Authorization` or `Accept-Language` in HTTP) already cover the need, with support from frameworks and infrastructure
- When the context is minimal, one or two values, and an [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) solves it
- When the infrastructure (caches, load balancers) needs to see the value without reading the body
- When each operation would have a different context, which removes the benefit of standardization

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Independence from the protocol and from intermediaries' headers | Ready-made support from frameworks and infrastructure for standard headers is lost |
| A single, recognizable place for metadata, under the API's control | Client and provider must implement, document and test the handling |
| Global context propagated across conversations and nested calls | The context grows over time and may become a dumping ground for loose data |
| End-to-end traceability and auditing | Each message gets slightly bigger, and the body must be read to extract the context |

- **Consistency:** use the same structure and the same place in all operations; if the context varies a lot, model an abstraction-refinement hierarchy or optional fields with default values.
- **Scope:** separate global from local context, to know what must be handed on and what is valid only for the message.
- **Security:** credentials and tokens in the context require a protected channel and care not to leak into logs.
- **Chaining:** in nested calls, the provider acting as a client hands over the global context and generates a new local one.

## Diagram

<Diagram />

Request and response carry a context element in the body, split into a global part, which follows the conversation, and a local one, which is valid only for the message.

## Example

The fintech's payments API receives, together with a `PixCharge`, a `context` element in the body. The `correlationId` and the language are global; the `messageId` and the time to live are local:

```http
POST /v1/pix-charges/charge-881/payments HTTP/1.1
Content-Type: application/json

{
  "context": {
    "global": {"correlationId": "corr-9d2e", "locale": "pt-BR"},
    "local": {"messageId": "msg-1", "ttlSeconds": 30}
  },
  "amountCents": 25000
}
```

When calling the ledger service (`LedgerEntry`), the provider hands over the global context and generates a new local one.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
record GlobalContext(String correlationId, String locale) {}

record LocalContext(String messageId, int ttlSeconds) {}

record RequestContext(GlobalContext global, LocalContext local) {
    // Nested call: the global context follows, the local one is new.
    RequestContext next(String messageId) {
        return new RequestContext(global, new LocalContext(messageId, local.ttlSeconds()));
    }

    String toJson() {
        return String.format(
            "{\"global\":{\"correlationId\":\"%s\",\"locale\":\"%s\"},"
                + "\"local\":{\"messageId\":\"%s\",\"ttlSeconds\":%d}}",
            global.correlationId(), global.locale(), local.messageId(), local.ttlSeconds());
    }
}

public class Main {
    public static void main(String[] args) {
        RequestContext incoming = new RequestContext(
            new GlobalContext("corr-9d2e", "pt-BR"), new LocalContext("msg-1", 30));
        System.out.println(incoming.toJson());
        System.out.println(incoming.next("msg-2").toJson());
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
import json
from dataclasses import asdict, dataclass, replace


@dataclass(frozen=True)
class GlobalContext:
    correlationId: str
    locale: str


@dataclass(frozen=True)
class LocalContext:
    messageId: str
    ttlSeconds: int


@dataclass(frozen=True)
class RequestContext:
    glob: GlobalContext  # "global" is a reserved word in Python
    local: LocalContext

    def next(self, message_id: str) -> "RequestContext":
        # Nested call: the global context follows, the local one is new.
        return RequestContext(self.glob, replace(self.local, messageId=message_id))

    def to_json(self) -> str:
        data = asdict(self)
        return json.dumps({"global": data["glob"], "local": data["local"]}, separators=(",", ":"))


incoming = RequestContext(GlobalContext("corr-9d2e", "pt-BR"), LocalContext("msg-1", 30))
print(incoming.to_json())
print(incoming.next("msg-2").to_json())
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"encoding/json"
	"fmt"
)

type GlobalContext struct {
	CorrelationID string `json:"correlationId"`
	Locale        string `json:"locale"`
}

type LocalContext struct {
	MessageID  string `json:"messageId"`
	TTLSeconds int    `json:"ttlSeconds"`
}

type RequestContext struct {
	Global GlobalContext `json:"global"`
	Local  LocalContext  `json:"local"`
}

// Nested call: the global context follows, the local one is new.
// In Go the struct is copied by value, so the original does not change.
func (c RequestContext) Next(messageID string) RequestContext {
	c.Local.MessageID = messageID
	return c
}

func main() {
	incoming := RequestContext{
		Global: GlobalContext{CorrelationID: "corr-9d2e", Locale: "pt-BR"},
		Local:  LocalContext{MessageID: "msg-1", TTLSeconds: 30},
	}
	for _, ctx := range []RequestContext{incoming, incoming.Next("msg-2")} {
		body, _ := json.Marshal(ctx)
		fmt.Println(string(body))
	}
}
```

</TabItem>
</Tabs>

Output:

```text
{"global":{"correlationId":"corr-9d2e","locale":"pt-BR"},"local":{"messageId":"msg-1","ttlSeconds":30}}
{"global":{"correlationId":"corr-9d2e","locale":"pt-BR"},"local":{"messageId":"msg-2","ttlSeconds":30}}
```

## Related patterns

- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — the items that make up the context
- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — the usual structure of the context element
- [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) — an alternative when the context has only simple values
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — a credential that can travel in the context
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — can be part of the response context
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) — client preferences can be carried in the context
- [Envelope Wrapper](/architecture/eip/message-transformation/envelope-wrapper) — also separates metadata from the payload, but at the messaging layer, for the infrastructure; here the context is part of the API contract
- [Correlation Identifier](/architecture/eip/message-construction/correlation-identifier) — the correlation identifier is the most common item of the global context

## Reference

- [Patterns for API Design, chapter 6: Context Representation](https://api-patterns.org/)
