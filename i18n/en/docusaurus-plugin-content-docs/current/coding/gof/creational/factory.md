---
title: Factory
pattern_slug: factory
category: Creational
tags:
  - Decoupling
  - Encapsulation
origin: Classic
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Factory"
mdx:
  format: mdx
---

# Factory

## Description

Factory (also called Simple Factory) centralizes object creation at a single point: a class or method that receives a parameter (a type, a configuration, a string) and decides which concrete implementation to instantiate, returning it through a common interface or base class. The client asks for "a product of type X" without knowing the constructor or the concrete class.

Unlike the patterns in the book "Design Patterns" (Gang of Four), Simple Factory isn't among the 23 cataloged patterns, and its status as a formal pattern is debated: many authors consider it merely a programming idiom or a good encapsulation practice. Even so, it's probably the most common form of "factory" found in real code and is usually the first step before evolving to Factory Method or Abstract Factory.

The decision logic is usually a `switch`/`if` or a registry map (type → constructor). There's no hierarchy of factories or subclasses deciding creation: there's a single concrete factory, often with a static method.

## Problems it solves

- Logic for selecting concrete classes (`if type == ...`) scattered and duplicated across many places in client code
- Client coupled to concrete classes and to construction details (parameters, dependencies, configuration)
- Difficulty adding or swapping implementations without changing every place that instantiates them
- The need to create objects from run-time data (configuration, user input, messages)

## When to use

- There's a family of classes with a common interface and the choice of implementation depends on a simple parameter
- Object creation involves logic that shouldn't live in the client
- You want a single point to change how objects are created (for example, for caching, logging, or dependency injection)
- The number of variants is small and relatively stable

## When to avoid

- There's only one implementation and no prospect of variation — a direct constructor is simpler
- New variants appear frequently and changing the central `switch` violates the open/closed principle; consider Factory Method or an extensible registry
- You need to create families of related objects that must be consistent with each other — use Abstract Factory
- Construction is complex and done in steps — use Builder

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Client decoupled from concrete classes | The factory comes to know every concrete class |
| Centralized creation logic with no duplication | Adding a type requires modifying the factory (violates open/closed) |
| Easy to understand and implement | Can grow into a giant `switch` that's hard to maintain |
| Single point for swapping implementations | Static methods make substitution in tests harder |

- **Coupling:** reduces the client's coupling, but concentrates dependencies in the factory.
- **Testability:** prefer an injectable factory (an instance with an interface) over a static method to make mocking easier.
- **Extensibility:** a registry map (type → constructor) mitigates the growing `switch` problem.
- **Complexity:** low; it's the lightest way to encapsulate object creation.

## Diagram

```mermaid
classDiagram
    class Client
    class PaymentMethodFactory {
        +create(type) PaymentMethod
    }
    class PaymentMethod {
        <<interface>>
        +charge(amountCents)
    }
    class PixPayment {
        +charge(amountCents)
    }
    class BoletoPayment {
        +charge(amountCents)
    }
    class CardPayment {
        +charge(amountCents)
    }
    Client --> PaymentMethodFactory : uses
    Client --> PaymentMethod : uses
    PaymentMethodFactory ..> PaymentMethod : creates
    PaymentMethodFactory ..> PixPayment : instantiates
    PaymentMethodFactory ..> BoletoPayment : instantiates
    PaymentMethodFactory ..> CardPayment : instantiates
    PaymentMethod <|.. PixPayment
    PaymentMethod <|.. BoletoPayment
    PaymentMethod <|.. CardPayment
```

The `Client` requests an object from the `PaymentMethodFactory`, specifying the desired type; the factory decides which concrete class (`PixPayment`, `BoletoPayment` or `CardPayment`) to instantiate and returns it as a `PaymentMethod`. The client works only with the interface.

## Example

At checkout, the buyer chooses to pay with Pix, boleto or card. The factory translates that choice into the right `PaymentMethod`, and the rest of the code only calls `charge()`.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
interface PaymentMethod {
    void charge(long amountCents);
}

class PixPayment implements PaymentMethod {
    public void charge(long amountCents) { /* generates the Pix QR code */ }
}

class BoletoPayment implements PaymentMethod {
    public void charge(long amountCents) { /* issues the boleto */ }
}

class CardPayment implements PaymentMethod {
    public void charge(long amountCents) { /* authorizes the card purchase */ }
}

class PaymentMethodFactory {
    static PaymentMethod create(String type) {
        return switch (type) {
            case "pix"    -> new PixPayment();
            case "boleto" -> new BoletoPayment();
            case "card"   -> new CardPayment();
            default -> throw new IllegalArgumentException("Unknown payment method: " + type);
        };
    }
}

// Client
PaymentMethod method = PaymentMethodFactory.create(checkout.selectedMethod());
method.charge(checkout.totalCents());
```

</TabItem>
<TabItem value="python" label="Python">

```python
from typing import Protocol

class PaymentMethod(Protocol):
    def charge(self, amount_cents: int) -> None: ...

class PixPayment:
    def charge(self, amount_cents: int) -> None:
        ...  # generates the Pix QR code

class BoletoPayment:
    def charge(self, amount_cents: int) -> None:
        ...  # issues the boleto

class CardPayment:
    def charge(self, amount_cents: int) -> None:
        ...  # authorizes the card purchase

class PaymentMethodFactory:
    _methods = {"pix": PixPayment, "boleto": BoletoPayment, "card": CardPayment}

    @classmethod
    def create(cls, type: str) -> PaymentMethod:
        try:
            return cls._methods[type]()
        except KeyError:
            raise ValueError(f"Unknown payment method: {type}") from None

# Client
method = PaymentMethodFactory.create(checkout.selected_method)
method.charge(checkout.total_cents)
```

</TabItem>
<TabItem value="go" label="Go">

```go
type PaymentMethod interface {
	Charge(amountCents int64)
}

type PixPayment struct{}

func (PixPayment) Charge(amountCents int64) { /* generates the Pix QR code */ }

type BoletoPayment struct{}

func (BoletoPayment) Charge(amountCents int64) { /* issues the boleto */ }

type CardPayment struct{}

func (CardPayment) Charge(amountCents int64) { /* authorizes the card purchase */ }

func NewPaymentMethod(kind string) (PaymentMethod, error) {
	switch kind {
	case "pix":
		return PixPayment{}, nil
	case "boleto":
		return BoletoPayment{}, nil
	case "card":
		return CardPayment{}, nil
	default:
		return nil, fmt.Errorf("unknown payment method: %s", kind)
	}
}

func main() {
	// Client
	method, err := NewPaymentMethod(checkout.SelectedMethod)
	if err != nil {
		return
	}
	method.Charge(checkout.TotalCents)
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface PaymentMethod {
  charge(amountCents: number): void;
}

class PixPayment implements PaymentMethod {
  charge(amountCents: number) { /* generates the Pix QR code */ }
}

class BoletoPayment implements PaymentMethod {
  charge(amountCents: number) { /* issues the boleto */ }
}

class CardPayment implements PaymentMethod {
  charge(amountCents: number) { /* authorizes the card purchase */ }
}

class PaymentMethodFactory {
  static create(type: "pix" | "boleto" | "card"): PaymentMethod {
    switch (type) {
      case "pix":    return new PixPayment();
      case "boleto": return new BoletoPayment();
      case "card":   return new CardPayment();
      default: throw new Error(`Unknown payment method: ${type}`);
    }
  }
}

// Client
const method = PaymentMethodFactory.create(checkout.selectedMethod);
method.charge(checkout.totalCents);
```

</TabItem>
</Tabs>

## Related patterns

- [Factory Method](/coding/gof/creational/factory-method) — instead of a single factory with a conditional, it defines a creation method that subclasses override; the decision about the concrete class is made through inheritance/polymorphism, not by parameter. It's the natural evolution when the Simple Factory needs to be extended without modification.
- [Abstract Factory](/coding/gof/creational/abstract-factory) — provides an interface for creating *families* of related objects, with several interchangeable concrete factories; the Simple Factory creates a single product type and has only one concrete factory.
- [Builder](/coding/gof/creational/builder) — focuses on building a complex object step by step, whereas Factory returns the finished object in a single call.
- [Singleton](/coding/gof/creational/singleton) — the factory is often exposed as a single instance or through static methods.
- [Prototype](/coding/gof/creational/prototype) — a factory can create objects by cloning registered prototypes instead of calling constructors.
- [Object Pool](/coding/gof/creational/object-pool) — the factory can reuse instances from a pool instead of creating new ones on every call.
- [Strategy](/coding/gof/behavioral/strategy) — factories are frequently used to select the concrete strategy based on configuration.

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
