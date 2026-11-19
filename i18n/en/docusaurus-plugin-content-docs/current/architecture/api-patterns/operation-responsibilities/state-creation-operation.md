---
title: State Creation Operation
pattern_slug: state-creation-operation
category: Operation Responsibilities
tags:
  - Decoupling
  - Performance
source: https://api-patterns.org/
sidebar_label: "State Creation Operation"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/operation-responsibilities/state-creation-operation.mdx';

# State Creation Operation

## Description

The State Creation Operation pattern is a write-only API operation with which the client tells the provider that something has happened, expecting nothing back except an acknowledgment. In terms of state, it writes (creates or appends data) on the provider side, but does not depend on reading that state to answer.

The operation represents a single business incident: a payment received, an order completed, a batch load finished. The provider may simply store the report or trigger later processing, and the client receives just a "received" or an identifier to query later. Because reports can arrive duplicated, out of order or get lost, each incident should carry a unique identifier and, preferably, the time at which it happened according to the client's clock, so that the provider can detect repeats and the operation appears idempotent.

A common variant is the Event Notification Operation, which just stores the event as it came (in line with event sourcing); another is the Bulk Report, in which several incidents travel together in a [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle).

## Problems it solves

- Clients that need to tell the provider about something that happened without coupling to the internal processing it triggers
- Mixing operations that write and operations that only compute in the same endpoint, which complicates load balancing and deployment
- Duplicate or resent reports after network failures, which create repeated entries
- Implicit assumptions about effects on state that stop holding without anyone noticing

## When to use

- To notify events that already happened on the client or in another system (a Pix received, a purchase approved)
- To start a long-running process by just registering the request, such as opening a credit application
- To report the completion of a batch load or the ingestion of a set of events into a data lake
- When the provider needs to scale writes and avoid reading state on every call

## When to avoid

- When the client needs a result computed from the current state: use a read or transition operation
- When complex invariants must be validated against existing state before accepting, since the operation deliberately avoids those reads
- When the change depends on a prior state identified in the request: prefer a [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation)
- To merely compute something without storing anything: use a [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function)

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Loose coupling: client and provider do not share application state | Consistency checks on the provider are hard, since the operation avoids reading state |
| Simple writes that are easy to scale and to deploy apart from reads | Contradictory or out-of-order reports require an explicit handling policy |
| Fast response, often just an acknowledgment | Without an acknowledgment or identifier, the client does not know whether to resend |
| Clear contract about the call's effect on state | Resends require unique identifiers and deduplication to remain idempotent |

- **Idempotency:** the incident identifier lets you discard repeats without creating duplicate entries.
- **Time:** the client's time and the arrival time can diverge; record both when order matters.
- **Consistency:** define whether the report is only stored, processed later, or changes the behavior of other operations.
- **Security:** when exposed in a [Public API](/architecture/api-patterns/foundations/public-api), protect it with an [API Key](/architecture/api-patterns/special-purpose-representations/api-key) and a [Rate Limit](/architecture/api-patterns/documentation/rate-limit).

## Diagram

<Diagram />

The provider only writes and acknowledges. If the same incident arrives again, the identifier lets it answer without creating another record.

## Example

The partner that processes Pix settlements tells the fintech that a Pix was received in an account. The fintech just records the event, and the balance and the corresponding `LedgerEntry` are produced later, asynchronously.

```http
POST /pix-events HTTP/1.1
Content-Type: application/json

{
  "eventId": "evt-501",
  "type": "PixReceived",
  "accountId": "acc-42",
  "amountCents": 15000,
  "occurredAt": "2026-11-03T14:21:07-03:00"
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{ "eventId": "evt-501", "status": "RECEIVED" }
```

A resend with the same `eventId` returns `"status": "ALREADY_RECEIVED"` and stores nothing new. The code below shows the core of the operation.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        PixEventProcessor processor = new PixEventProcessor();
        PixReceivedEvent event = new PixReceivedEvent("evt-501", "acc-42", 15_000);
        System.out.println(processor.informAbout(event)); // RECEIVED
        System.out.println(processor.informAbout(event)); // ALREADY_RECEIVED
    }
}

record PixReceivedEvent(String eventId, String accountId, long amountCents) {}

class PixEventProcessor {
    private final Map<String, PixReceivedEvent> store = new LinkedHashMap<>();

    // Only writes, without reading business state. Repeating the eventId is harmless.
    String informAbout(PixReceivedEvent event) {
        return store.putIfAbsent(event.eventId(), event) == null
                ? "RECEIVED" : "ALREADY_RECEIVED";
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PixReceivedEvent:
    event_id: str
    account_id: str
    amount_cents: int

class PixEventProcessor:
    def __init__(self) -> None:
        self._store = {}

    # Only writes, without reading business state. Repeating the event_id is harmless.
    def inform_about(self, event: PixReceivedEvent) -> str:
        if event.event_id in self._store:
            return "ALREADY_RECEIVED"
        self._store[event.event_id] = event
        return "RECEIVED"

processor = PixEventProcessor()
event = PixReceivedEvent("evt-501", "acc-42", 15_000)
print(processor.inform_about(event))  # RECEIVED
print(processor.inform_about(event))  # ALREADY_RECEIVED
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
)

type PixReceivedEvent struct {
	EventID     string
	AccountID   string
	AmountCents int64
}

type PixEventProcessor struct {
	store map[string]PixReceivedEvent
}

// Only writes, without reading business state. Repeating the EventID is harmless.
func (p *PixEventProcessor) InformAbout(event PixReceivedEvent) string {
	if _, seen := p.store[event.EventID]; seen {
		return "ALREADY_RECEIVED"
	}
	p.store[event.EventID] = event
	return "RECEIVED"
}

func main() {
	processor := &PixEventProcessor{store: map[string]PixReceivedEvent{}}
	event := PixReceivedEvent{"evt-501", "acc-42", 15_000}
	fmt.Println(processor.InformAbout(event)) // RECEIVED
	fmt.Println(processor.InformAbout(event)) // ALREADY_RECEIVED
}
```

</TabItem>
</Tabs>

## Related patterns

- [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) — reads and writes state and usually identifies the element to change; the State Creation Operation only writes
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — the opposite: reads state without writing, pulling data instead of pushing it
- [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) — neither reads nor writes state
- [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) and [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the endpoints that usually host the operation
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — the event identifier and the one returned in the acknowledgment
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — common format for the response when the report is rejected
- [Domain Event](/architecture/microservices/service-collaboration/domain-event) — helps identify these operations, especially in the event notification variant
- [Event Message](/architecture/eip/message-construction/event-message) — the EIP event message that the Event Notification Operation variant exposes through an API
- [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer) — technique to process the same report more than once safely

## Reference

- [Patterns for API Design, chapter 5: State Creation Operation](https://api-patterns.org/)
