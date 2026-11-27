---
title: State Transition Operation
pattern_slug: state-transition-operation
category: Operation Responsibilities
tags:
  - Shared Understanding
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "State Transition Operation"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/operation-responsibilities/state-transition-operation.mdx';

# State Transition Operation

## Description

The State Transition Operation pattern is an API operation that combines the client's input with the provider's current state to cause a state change, reading and writing provider-side storage. The provider models the valid transitions and checks, on every call, whether the request is allowed in the state the resource is in.

The operation can represent an isolated business activity (approve, cancel), an update of an entity (full replacement or partial change) or even the execution of an entire process. It is the basis for splitting business process responsibilities between client and provider, so that progress is visible in the API and the client can advance, track or cancel it.

The Business Activity Processor variant exposes the states and primitives of an activity (prepare, start, suspend, resume, complete, fail, cancel, undo, restart and cleanup) as a documented state machine. Internally, each call should have a transaction boundary equal to the operation's (an ACID transaction or a saga) and appear idempotent, for instance by preferring absolute values over increments.

## Problems it solves

- Long-running business processes that need to advance step by step through distinct calls
- Activities that may only happen in certain states and must not run out of order
- Clients and provider that need to agree on who owns the process state
- Invalid or fraudulent flows, which must be rejected at runtime

## When to use

- For activities with a life cycle, such as approving, disbursing or canceling a credit contract
- For entity updates that depend on the current state (partial change, increments, status change)
- When the client needs to track, cancel or undo an activity in progress
- When there is auditing of which transitions occurred and by whom

## When to avoid

- When the operation only reports a fact and does not depend on state: a [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) is enough
- When the endpoint must be fully stateless, to scale or to run as a serverless function
- When all state can be carried by the client on every call, with the security risks that brings
- When the flow is a simple read or computation: use a [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) or a [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function)

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Valid transitions verified on the provider, with process auditing | Stateful operations are hard to scale and to move between nodes |
| Client tracks and controls the progress of long processes | Requests may be denied because the client has an outdated view of the state |
| Explicit contract, with pre and postconditions per state | Complex pre and postconditions must be documented and tested |
| Can use absolute, idempotent updates | Incremental updates are not idempotent and corrupt data if repeated |

- **Granularity:** decide whether each activity, each subprocess or the entire process becomes an operation.
- **Consistency:** the transaction boundary matches the operation; long processes call for sagas, not a single transaction.
- **Conflicts:** other calls, events and jobs may change the same state; validate the transition and handle the refusal.
- **Idempotency:** prefer "set the value to n" over "add one"; an [Id Element](/architecture/api-patterns/element-stereotypes/id-element) identifies the resource and the activity.
- **Security:** only authorized clients should trigger certain transitions; protect with an [API Key](/architecture/api-patterns/special-purpose-representations/api-key) or a stronger token.

## Diagram

<Diagram />

Each operation moves the contract from one state to another. Requests that do not follow one of the arrows, such as canceling an already disbursed contract, are rejected.

## Example

A personal credit `LoanContract` goes through the requested, approved and disbursed states, and can be canceled while the money has not been disbursed. Each transition is a call that checks the current state.

```http
POST /loan-contracts/loan-77/approve HTTP/1.1
Content-Type: application/json

{ "approvedBy": "analyst-9" }
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ "id": "loan-77", "status": "APPROVED" }
```

An attempt to cancel an already disbursed contract is refused:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{ "error": "INVALID_TRANSITION", "message": "DISBURSED -> CANCELED" }
```

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        LoanContract contract = new LoanContract("loan-77");
        contract.transitionTo(LoanStatus.APPROVED);
        System.out.println(contract.status); // APPROVED
        contract.transitionTo(LoanStatus.DISBURSED);
        System.out.println(contract.status); // DISBURSED
        try {
            contract.transitionTo(LoanStatus.CANCELED);
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage()); // DISBURSED -> CANCELED
        }
    }
}

enum LoanStatus { REQUESTED, APPROVED, DISBURSED, CANCELED }

class LoanContract {
    private static final Map<LoanStatus, Set<LoanStatus>> ALLOWED = Map.of(
            LoanStatus.REQUESTED, Set.of(LoanStatus.APPROVED, LoanStatus.CANCELED),
            LoanStatus.APPROVED, Set.of(LoanStatus.DISBURSED, LoanStatus.CANCELED),
            LoanStatus.DISBURSED, Set.of(),
            LoanStatus.CANCELED, Set.of());

    final String id;
    LoanStatus status = LoanStatus.REQUESTED;

    LoanContract(String id) { this.id = id; }

    // Reads the current state and only writes if the transition is valid.
    void transitionTo(LoanStatus target) {
        if (!ALLOWED.get(status).contains(target)) {
            throw new IllegalStateException(status + " -> " + target);
        }
        status = target;
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from enum import Enum

class LoanStatus(Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    DISBURSED = "DISBURSED"
    CANCELED = "CANCELED"

ALLOWED = {
    LoanStatus.REQUESTED: {LoanStatus.APPROVED, LoanStatus.CANCELED},
    LoanStatus.APPROVED: {LoanStatus.DISBURSED, LoanStatus.CANCELED},
    LoanStatus.DISBURSED: set(),
    LoanStatus.CANCELED: set(),
}

class LoanContract:
    def __init__(self, id: str) -> None:
        self.id = id
        self.status = LoanStatus.REQUESTED

    # Reads the current state and only writes if the transition is valid.
    def transition_to(self, target: LoanStatus) -> None:
        if target not in ALLOWED[self.status]:
            raise ValueError(f"{self.status.value} -> {target.value}")
        self.status = target

contract = LoanContract("loan-77")
contract.transition_to(LoanStatus.APPROVED)
print(contract.status.value)  # APPROVED
contract.transition_to(LoanStatus.DISBURSED)
print(contract.status.value)  # DISBURSED
try:
    contract.transition_to(LoanStatus.CANCELED)
except ValueError as e:
    print(e)  # DISBURSED -> CANCELED
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
)

type LoanStatus string

const (
	Requested LoanStatus = "REQUESTED"
	Approved  LoanStatus = "APPROVED"
	Disbursed LoanStatus = "DISBURSED"
	Canceled  LoanStatus = "CANCELED"
)

var allowed = map[LoanStatus][]LoanStatus{
	Requested: {Approved, Canceled},
	Approved:  {Disbursed, Canceled},
	Disbursed: {},
	Canceled:  {},
}

type LoanContract struct {
	ID     string
	Status LoanStatus
}

// Reads the current state and only writes if the transition is valid.
// In Go, an invalid transition comes back as an error, not an exception.
func (c *LoanContract) TransitionTo(target LoanStatus) error {
	for _, next := range allowed[c.Status] {
		if next == target {
			c.Status = target
			return nil
		}
	}
	return fmt.Errorf("%s -> %s", c.Status, target)
}

func main() {
	contract := &LoanContract{ID: "loan-77", Status: Requested}
	_ = contract.TransitionTo(Approved)
	fmt.Println(contract.Status) // APPROVED
	_ = contract.TransitionTo(Disbursed)
	fmt.Println(contract.Status) // DISBURSED
	if err := contract.TransitionTo(Canceled); err != nil {
		fmt.Println(err) // DISBURSED -> CANCELED
	}
}
```

</TabItem>
</Tabs>

## Related patterns

- [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) — only writes and usually does not identify an existing element; the State Transition Operation reads and writes
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — queries the progress of the process without changing it
- [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) — can validate a step before the transition is requested
- [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) and [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — the endpoints that host the operation
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — propagates context for logging and debugging in long conversations
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — describes the refusal of an invalid transition
- [Command Message](/architecture/eip/message-construction/command-message) and [Document Message](/architecture/eip/message-construction/document-message) — the request usually combines a command with a document
- [Aggregate](/design/ddd/building-blocks/aggregate) — consistency boundary that normally holds the transition rules behind the operation
- [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer) — helps tolerate repeated transition requests
- [Asynchronous Request-Reply](/architecture/cloud-design-patterns/messaging/asynchronous-request-reply) — conversation pattern for slow activities that the client follows

## Reference

- [Patterns for API Design, chapter 5: State Transition Operation](https://api-patterns.org/)
