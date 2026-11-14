---
title: Mediator
pattern_slug: mediator
category: Behavioral
tags:
  - Decoupling
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Mediator"
mdx:
  format: mdx
---

# Mediator

## Description

Mediator defines an object that encapsulates how a set of objects interact. Instead of the objects (called colleagues) referencing and calling each other directly, they communicate only through the mediator, which promotes loose coupling between them.

Each colleague only knows the `Mediator` abstraction and notifies it when something relevant happens. The concrete mediator concentrates the coordination logic: it decides which other colleagues should react and in what order. A many-to-many web of dependencies is thus turned into several one-to-many relationships centered on the mediator.

Since the collaborative behavior lives in a single place, you can change how the components interact by swapping or extending the mediator, without modifying the colleague classes, which become easier to reuse.

## Problems it solves

- Many objects referencing each other directly, forming a web of dependencies that's hard to understand and maintain
- Components that are hard to reuse because they depend on several other specific components
- Interaction logic spread across several classes, requiring changes in many of them to alter a flow
- Coordinating UI elements in forms (enabling buttons, validating fields, updating lists according to selections)
- Communication between participants of a system, such as users in a chat room or aircraft at a control tower

## When to use

- A set of objects communicates in well-defined but complex ways, and the resulting interdependencies are unstructured
- Reusing an object is difficult because it references and communicates with many others
- Behavior distributed across several classes should be customizable without creating many subclasses
- You want to centralize orchestration rules among components (for example, UI dialogs, workflows, command handlers in CQRS)

## When to avoid

- Few objects with simple interactions — direct calls are clearer
- The mediator tends to accumulate too many rules and become a hard-to-maintain "god object"
- Communication is essentially broadcast with no coordination logic — Observer is usually enough
- Performance is critical and the extra indirection in each interaction isn't justified

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Reduces coupling between colleagues | The mediator can become monolithic and complex (god object) |
| Centralizes interaction logic in a single place | Single point of failure and of change contention |
| Colleagues become simpler and more reusable | Indirect flow makes tracing interactions less obvious |
| Replaces many-to-many relationships with one-to-many | Concrete mediators are usually not very reusable across contexts |

- **Coupling:** colleagues depend only on the `Mediator` interface; coupling is concentrated in the concrete mediator.
- **Testability:** colleagues can be tested with a fake mediator; the mediator can be tested with simulated colleagues.
- **Complexity:** split large mediators by context or use case to keep them from growing indefinitely.
- **Performance:** indirection is cheap, but it can add up in flows with many chained notifications.

## Diagram

```mermaid
classDiagram
    class Mediator {
        <<interface>>
        +notify(Colleague sender, String event)
    }
    class ConcreteMediator {
        -ConcreteColleagueA colleagueA
        -ConcreteColleagueB colleagueB
        +notify(Colleague sender, String event)
    }
    class Colleague {
        <<abstract>>
        #Mediator mediator
        +setMediator(Mediator mediator)
    }
    class ConcreteColleagueA {
        +operationA()
    }
    class ConcreteColleagueB {
        +operationB()
    }
    Mediator <|.. ConcreteMediator
    Colleague <|-- ConcreteColleagueA
    Colleague <|-- ConcreteColleagueB
    Colleague --> Mediator : notifies
    ConcreteMediator --> ConcreteColleagueA : coordinates
    ConcreteMediator --> ConcreteColleagueB : coordinates
```

The `Mediator` defines the communication interface used by the colleagues. The `ConcreteMediator` knows the concrete colleagues and implements the coordination between them. Each `Colleague` keeps a reference to the mediator and notifies it instead of talking directly to the others.

## Example

Participant banks do not send payment orders directly to each other: the clearing house (mediator) receives the order and delivers it to the destination bank.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
record ClearingOrder(String from, String to, long amountCents) {}

interface ClearingHouse {
    void register(ParticipantBank bank);
    void send(ClearingOrder order);
}

class InstantPaymentClearing implements ClearingHouse {
    private final Map<String, ParticipantBank> banks = new HashMap<>();

    public void register(ParticipantBank bank) {
        banks.put(bank.code(), bank);
    }

    public void send(ClearingOrder order) {
        ParticipantBank destination = banks.get(order.to());
        if (destination == null)
            throw new IllegalArgumentException("Bank " + order.to() + " is not a clearing participant");
        destination.receive(order);
    }
}

class ParticipantBank {
    private final String code;
    private final ClearingHouse clearing;

    ParticipantBank(String code, ClearingHouse clearing) {
        this.code = code;
        this.clearing = clearing;
        clearing.register(this);
    }

    String code() { return code; }

    void pay(String to, long amountCents) {
        clearing.send(new ClearingOrder(code, to, amountCents));
    }

    void receive(ClearingOrder order) {
        System.out.println("[" + code + "] order from " + order.from() + ": " + order.amountCents() + " cents");
    }
}

ClearingHouse clearing = new InstantPaymentClearing();
ParticipantBank alpha = new ParticipantBank("001", clearing);
new ParticipantBank("237", clearing);
alpha.pay("237", 15_000); // [237] order from 001: 15000 cents
```

</TabItem>
<TabItem value="python" label="Python">

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ClearingOrder:
    sender: str
    to: str
    amount_cents: int

class ClearingHouse(Protocol):
    def register(self, bank: ParticipantBank) -> None: ...
    def send(self, order: ClearingOrder) -> None: ...

class InstantPaymentClearing:
    def __init__(self) -> None:
        self._banks: dict[str, ParticipantBank] = {}

    def register(self, bank: ParticipantBank) -> None:
        self._banks[bank.code] = bank

    def send(self, order: ClearingOrder) -> None:
        destination = self._banks.get(order.to)
        if destination is None:
            raise LookupError(f"Bank {order.to} is not a clearing participant")
        destination.receive(order)

class ParticipantBank:
    def __init__(self, code: str, clearing: ClearingHouse) -> None:
        self.code = code
        self._clearing = clearing
        clearing.register(self)

    def pay(self, to: str, amount_cents: int) -> None:
        self._clearing.send(ClearingOrder(self.code, to, amount_cents))

    def receive(self, order: ClearingOrder) -> None:
        print(f"[{self.code}] order from {order.sender}: {order.amount_cents} cents")

clearing = InstantPaymentClearing()
alpha = ParticipantBank("001", clearing)
ParticipantBank("237", clearing)
alpha.pay("237", 15_000)  # [237] order from 001: 15000 cents
```

</TabItem>
<TabItem value="go" label="Go">

```go
type ClearingOrder struct {
	From, To    string
	AmountCents int64
}

type ClearingHouse interface {
	Register(bank *ParticipantBank)
	Send(order ClearingOrder) error
}

type InstantPaymentClearing struct {
	banks map[string]*ParticipantBank
}

func (c *InstantPaymentClearing) Register(bank *ParticipantBank) {
	c.banks[bank.Code] = bank
}

func (c *InstantPaymentClearing) Send(order ClearingOrder) error {
	destination, ok := c.banks[order.To]
	if !ok {
		return fmt.Errorf("bank %s is not a clearing participant", order.To)
	}
	destination.Receive(order)
	return nil
}

type ParticipantBank struct {
	Code     string
	clearing ClearingHouse
}

func NewParticipantBank(code string, clearing ClearingHouse) *ParticipantBank {
	bank := &ParticipantBank{Code: code, clearing: clearing}
	clearing.Register(bank)
	return bank
}

func (b *ParticipantBank) Pay(to string, amountCents int64) error {
	return b.clearing.Send(ClearingOrder{From: b.Code, To: to, AmountCents: amountCents})
}

func (b *ParticipantBank) Receive(order ClearingOrder) {
	fmt.Printf("[%s] order from %s: %d cents\n", b.Code, order.From, order.AmountCents)
}

func main() {
	clearing := &InstantPaymentClearing{banks: map[string]*ParticipantBank{}}
	alpha := NewParticipantBank("001", clearing)
	NewParticipantBank("237", clearing)
	if err := alpha.Pay("237", 15_000); err != nil { // [237] order from 001: 15000 cents
		fmt.Println(err)
	}
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface ClearingHouse {
  register(bank: ParticipantBank): void;
  send(order: ClearingOrder): void;
}

interface ClearingOrder {
  from: string;
  to: string;
  amountCents: number;
}

class InstantPaymentClearing implements ClearingHouse {
  private banks = new Map<string, ParticipantBank>();

  register(bank: ParticipantBank): void {
    this.banks.set(bank.code, bank);
  }

  send(order: ClearingOrder): void {
    const destination = this.banks.get(order.to);
    if (!destination) throw new Error(`Bank ${order.to} is not a clearing participant`);
    destination.receive(order);
  }
}

class ParticipantBank {
  constructor(public code: string, private clearing: ClearingHouse) {
    clearing.register(this);
  }
  pay(to: string, amountCents: number): void {
    this.clearing.send({ from: this.code, to, amountCents });
  }
  receive(order: ClearingOrder): void {
    console.log(`[${this.code}] order from ${order.from}: ${order.amountCents} cents`);
  }
}

const clearing = new InstantPaymentClearing();
const alpha = new ParticipantBank("001", clearing);
new ParticipantBank("237", clearing);
alpha.pay("237", 15_000); // [237] order from 001: 15000 cents
```

</TabItem>
</Tabs>

## Related patterns

- [Observer](/coding/gof/behavioral/observer) — often used to implement communication between colleagues and mediator; Observer distributes the communication, while Mediator centralizes it
- [Facade](/coding/gof/structural/facade) — also simplifies interactions, but it's unidirectional and abstracts a subsystem; Mediator coordinates colleagues that know it and communicate through it
- [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility) — another way to decouple senders and receivers, passing the request along a chain instead of centralizing it
- [Command](/coding/gof/behavioral/command) — commands can be routed by a mediator to their handlers, as in mediator libraries for CQRS
- [Singleton](/coding/gof/creational/singleton) — the mediator usually has a single instance per context

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Mediator on Refactoring.Guru](https://refactoring.guru/design-patterns/mediator)
