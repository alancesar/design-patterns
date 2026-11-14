---
title: Facade
pattern_slug: facade
category: Structural
tags:
  - Simplicity
  - Decoupling
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Facade"
mdx:
  format: mdx
---

# Facade

## Description

The Facade provides a single, simplified interface to a set of interfaces in a subsystem. Instead of the client knowing about and coordinating several internal classes, it talks to a single facade object that exposes high-level operations.

The facade knows which subsystem classes are responsible for each request and delegates the work to them, in the correct order. The subsystem classes keep working independently and don't know about the facade; advanced clients can still access them directly when they need more control.

The result is a layer that reduces the coupling between clients and implementation details, making the subsystem easier to use, maintain, and evolve.

## Problems it solves

- Clients need to orchestrate many low-level classes (libraries, frameworks, legacy APIs) to perform a simple task.
- Internal changes in a subsystem propagate to all the code that uses it.
- Complex dependencies between layers make it hard to understand a module's entry point.
- Integration code repeated in several places to perform the same sequence of calls.

## When to use

- When you want to provide a simple interface to a complex subsystem.
- To structure a system into layers, defining an entry point for each one.
- To isolate client code from third-party libraries or legacy systems, making them easier to replace.
- When there are many dependencies between clients and implementation classes and you want to decouple them.

## When to avoid

- When the subsystem is already simple; the facade would only add an unnecessary layer.
- When clients need the full power and flexibility of the subsystem and the facade would end up replicating its entire API.
- When the facade tends to become a "god object", accumulating unrelated responsibilities.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Simple, easy-to-use interface | May hide useful functionality or limit advanced use cases |
| Less coupling between clients and the subsystem | One more layer of indirection to maintain |
| Internal changes are isolated behind the facade | Risk of the facade growing too large and becoming a "god object" |
| Clear entry point for layers and modules | May mask design problems in the subsystem instead of solving them |

- **Coupling:** the client depends only on the facade, but the facade is coupled to several subsystem classes.
- **Testability:** clients are easy to test with a facade double; the facade itself requires integration tests or mocks of the components.
- **Complexity:** low; the pattern requires neither inheritance nor special interfaces.
- **Performance:** negligible impact, just one extra delegation call.

## Diagram

```mermaid
classDiagram
    class Client
    class Facade {
        +operation()
    }
    class SubsystemA {
        +operationA()
    }
    class SubsystemB {
        +operationB()
    }
    class SubsystemC {
        +operationC()
    }
    Client --> Facade
    Facade --> SubsystemA
    Facade --> SubsystemB
    Facade --> SubsystemC
```

The `Client` interacts only with the `Facade`, which delegates calls to `SubsystemA`, `SubsystemB`, and `SubsystemC` in the proper order. The subsystem classes don't know about the facade.

## Example

Sending a Pix requires resolving the key in DICT, passing the fraud check, debiting the ledger and sending the message to SPI. Instead of each controller coordinating these four services, a `PixTransferFacade` exposes a single `send` operation.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
record PixDestination(String ispb, String account) {}

class DictClient {
    PixDestination resolve(String pixKey) { return new PixDestination("00000000", "12345-6"); }
}

class FraudService {
    boolean approve(String accountId, long amountCents) { return true; }
}

class LedgerService {
    String debit(String accountId, long amountCents) { return "entry-123"; }
}

class SpiClient {
    String submit(PixDestination destination, long amountCents, String entryId) {
        return "E00000000202603101030abcdef12345"; // endToEndId
    }
}

class PixTransferFacade {
    private final DictClient dict = new DictClient();
    private final FraudService fraud = new FraudService();
    private final LedgerService ledger = new LedgerService();
    private final SpiClient spi = new SpiClient();

    String send(String accountId, String pixKey, long amountCents) {
        PixDestination destination = dict.resolve(pixKey);
        if (!fraud.approve(accountId, amountCents)) {
            throw new IllegalStateException("Transfer rejected by fraud check");
        }
        String entryId = ledger.debit(accountId, amountCents);
        return spi.submit(destination, amountCents, entryId);
    }
}

// Client
String endToEndId = new PixTransferFacade().send("acc-1", "ana@example.com", 19_990);
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PixDestination:
    ispb: str
    account: str

class DictClient:
    def resolve(self, pix_key: str) -> PixDestination:
        return PixDestination("00000000", "12345-6")

class FraudService:
    def approve(self, account_id: str, amount_cents: int) -> bool:
        return True

class LedgerService:
    def debit(self, account_id: str, amount_cents: int) -> str:
        return "entry-123"

class SpiClient:
    def submit(self, destination: PixDestination, amount_cents: int, entry_id: str) -> str:
        return "E00000000202603101030abcdef12345"  # endToEndId

class PixTransferFacade:
    def __init__(self) -> None:
        self._dict = DictClient()
        self._fraud = FraudService()
        self._ledger = LedgerService()
        self._spi = SpiClient()

    def send(self, account_id: str, pix_key: str, amount_cents: int) -> str:
        destination = self._dict.resolve(pix_key)
        if not self._fraud.approve(account_id, amount_cents):
            raise PermissionError("Transfer rejected by fraud check")
        entry_id = self._ledger.debit(account_id, amount_cents)
        return self._spi.submit(destination, amount_cents, entry_id)

# Client
end_to_end_id = PixTransferFacade().send("acc-1", "ana@example.com", 19_990)
```

</TabItem>
<TabItem value="go" label="Go">

```go
type PixDestination struct{ ISPB, Account string }

type DictClient struct{}

func (DictClient) Resolve(pixKey string) PixDestination {
	return PixDestination{ISPB: "00000000", Account: "12345-6"}
}

type FraudService struct{}

func (FraudService) Approve(accountID string, amountCents int64) bool { return true }

type LedgerService struct{}

func (LedgerService) Debit(accountID string, amountCents int64) string { return "entry-123" }

type SpiClient struct{}

func (SpiClient) Submit(destination PixDestination, amountCents int64, entryID string) string {
	return "E00000000202603101030abcdef12345" // endToEndId
}

type PixTransferFacade struct {
	dict   DictClient
	fraud  FraudService
	ledger LedgerService
	spi    SpiClient
}

func (f PixTransferFacade) Send(accountID, pixKey string, amountCents int64) (string, error) {
	destination := f.dict.Resolve(pixKey)
	if !f.fraud.Approve(accountID, amountCents) {
		return "", errors.New("transfer rejected by fraud check")
	}
	entryID := f.ledger.Debit(accountID, amountCents)
	return f.spi.Submit(destination, amountCents, entryID), nil
}

func main() {
	// Client
	endToEndID, err := PixTransferFacade{}.Send("acc-1", "ana@example.com", 19_990)
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface PixDestination { ispb: string; account: string; }

class DictClient {
  resolve(pixKey: string): PixDestination { return { ispb: "00000000", account: "12345-6" }; }
}

class FraudService {
  approve(accountId: string, amountCents: number): boolean { return true; }
}

class LedgerService {
  debit(accountId: string, amountCents: number): string { return "entry-123"; }
}

class SpiClient {
  submit(destination: PixDestination, amountCents: number, entryId: string): string {
    return "E00000000202603101030abcdef12345"; // endToEndId
  }
}

class PixTransferFacade {
  constructor(
    private dict = new DictClient(),
    private fraud = new FraudService(),
    private ledger = new LedgerService(),
    private spi = new SpiClient(),
  ) {}

  send(accountId: string, pixKey: string, amountCents: number): string {
    const destination = this.dict.resolve(pixKey);
    if (!this.fraud.approve(accountId, amountCents)) {
      throw new Error("Transfer rejected by fraud check");
    }
    const entryId = this.ledger.debit(accountId, amountCents);
    return this.spi.submit(destination, amountCents, entryId);
  }
}

// Client
const endToEndId = new PixTransferFacade().send("acc-1", "ana@example.com", 19_990);
```

</TabItem>
</Tabs>

## Related patterns

- [Adapter](/coding/gof/structural/adapter) — the Adapter converts an existing interface into another one that's expected; the Facade creates a new, simpler interface for a set of classes.
- [Mediator](/coding/gof/behavioral/mediator) — both centralize communication, but the Mediator coordinates colleagues that know about it, while the Facade is transparent to the subsystem.
- [Abstract Factory](/coding/gof/creational/abstract-factory) — can be used together with the Facade to create the subsystem's objects in a platform-independent way.
- [Singleton](/coding/gof/creational/singleton) — often a single instance of the facade is enough.
- [Proxy](/coding/gof/structural/proxy) — also sits between the client and the real object, but keeps the same interface instead of simplifying it.

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Facade on Refactoring.Guru](https://refactoring.guru/design-patterns/facade)
