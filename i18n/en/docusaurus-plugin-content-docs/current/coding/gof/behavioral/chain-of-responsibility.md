---
title: Chain of Responsibility
pattern_slug: chain-of-responsibility
category: Behavioral
tags:
  - Decoupling
  - Runtime Flexibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Chain of Responsibility"
---

# Chain of Responsibility

## Description

Chain of Responsibility avoids coupling the sender of a request to its receiver by giving more than one object a chance to handle it. The receiving objects (handlers) are chained together, and the request is passed along the chain until one of them handles it, or until the chain ends.

Each handler implements a common interface and keeps a reference to the next element in the chain. When it receives the request, it decides whether to process it, pass it to its successor, or both (a common variation in middleware pipelines). The client only knows the first link and doesn't need to know which object will actually handle the request.

Because the chain is assembled at runtime, you can add, remove, or reorder handlers without changing the client code or the other handlers.

## Problems it solves

- A sender tightly coupled to a specific receiver, with long `if/else` or `switch` chains to decide who handles the request
- The need to apply a configurable sequence of checks (authentication, authorization, validation, rate limiting) before processing a request
- Tiered escalation of requests (for example, expense approval by authority level, or first-, second-, and third-level support)
- A set of handlers that must change dynamically without recompiling or modifying the client

## When to use

- More than one object can handle a request and the handler isn't known in advance
- You want to issue a request to one of several objects without explicitly specifying the receiver
- The set and order of handlers must be defined or changed dynamically
- Processing pipelines such as HTTP middleware, servlet filters, interceptors, and UI event handling (event bubbling)

## When to avoid

- There is exactly one known, stable handler: a direct call is simpler
- Every request must be handled and there's no default handler at the end of the chain
- The chain is very long and performance is critical, since each request may traverse many links
- The handler order creates implicit dependencies that are hard to understand and debug

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Decouples sender and receiver | There's no guarantee that the request will be handled |
| Flexibility to add, remove, and reorder handlers at runtime | Chain order becomes an implicit, fragile dependency |
| Each handler has a single responsibility (SRP) and follows the Open/Closed Principle | Harder debugging: the flow is spread across several objects |
| Handlers are reusable in different chains | Extra latency when the request crosses many links |

- **Coupling:** the client depends only on the `Handler` abstraction; each handler only knows the next one.
- **Testability:** handlers can be tested in isolation with a fake (mock) successor.
- **Complexity:** chain assembly should be centralized (for example, in a builder or in configuration) to avoid cycles and forgotten links.
- **Performance:** in long chains, consider putting the most likely handlers first.

## Diagram

```mermaid
classDiagram
    class Client
    class Handler {
        <<abstract>>
        -Handler next
        +setNext(Handler handler) Handler
        +handle(Request request)
    }
    class ConcreteHandlerA {
        +handle(Request request)
    }
    class ConcreteHandlerB {
        +handle(Request request)
    }
    class Request
    Client --> Handler : sends request
    Handler o--> Handler : next
    Handler <|-- ConcreteHandlerA
    Handler <|-- ConcreteHandlerB
    Handler ..> Request : processes
```

The `Client` sends the `Request` to the first `Handler` in the chain. Each `ConcreteHandler` decides whether to handle the request or pass it to the successor referenced by `next`, forming a linked list of handlers.

## Example

A personal loan proposal goes up through approval levels: the analyst approves up to R$ 5,000, the coordinator up to R$ 50,000 and the credit committee above that. The approval limits are illustrative.

```typescript
abstract class CreditApprover {
  private next?: CreditApprover;

  setNext(next: CreditApprover): CreditApprover {
    this.next = next;
    return next;
  }

  handle(proposal: CreditProposal): string {
    if (this.next) return this.next.handle(proposal);
    return `Proposal ${proposal.id} rejected: no approver`;
  }
}

class CreditProposal {
  constructor(readonly id: string, readonly amountCents: number) {}
}

class Analyst extends CreditApprover {
  handle(proposal: CreditProposal): string {
    return proposal.amountCents <= 500_000 ? `Analyst approved ${proposal.id}` : super.handle(proposal);
  }
}

class Coordinator extends CreditApprover {
  handle(proposal: CreditProposal): string {
    return proposal.amountCents <= 5_000_000 ? `Coordinator approved ${proposal.id}` : super.handle(proposal);
  }
}

class CreditCommittee extends CreditApprover {
  handle(proposal: CreditProposal): string {
    return `CreditCommittee approved ${proposal.id}`;
  }
}

const chain = new Analyst();
chain.setNext(new Coordinator()).setNext(new CreditCommittee());
console.log(chain.handle(new CreditProposal("P-101", 300_000)));   // Analyst approved P-101
console.log(chain.handle(new CreditProposal("P-102", 8_000_000))); // CreditCommittee approved P-102
```

## Related patterns

- [Composite](/coding/gof/structural/composite) — the chain often follows a Composite hierarchy, passing the request from child to parent (event bubbling)
- [Command](/coding/gof/behavioral/command) — requests can be encapsulated as Commands and passed along the chain
- [Decorator](/coding/gof/structural/decorator) — a similar recursive chaining structure, but a Decorator always delegates and adds behavior, while a handler can stop the chain
- [Mediator](/coding/gof/behavioral/mediator) — another way to decouple senders and receivers, but it centralizes communication instead of distributing it along a chain
- [Observer](/coding/gof/behavioral/observer) — also decouples senders and receivers, but notifies all interested parties instead of a single handler
- [Null Object](/coding/gof/behavioral/null-object) — can serve as the last link in the chain, eliminating null-successor checks

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Chain of Responsibility on Refactoring.Guru](https://refactoring.guru/design-patterns/chain-of-responsibility)
