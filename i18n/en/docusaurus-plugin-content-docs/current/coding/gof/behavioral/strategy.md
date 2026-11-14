---
title: Strategy
pattern_slug: strategy
category: Behavioral
tags:
  - Runtime Flexibility
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Strategy"
mdx:
  format: mdx
---

# Strategy

## Description

Strategy (also known as Policy) defines a family of algorithms, encapsulates each one in its own object, and makes them interchangeable. This way, the algorithm can vary independently of the clients that use it.

The object that uses the algorithm, called the context (`Context`), holds a reference to a `Strategy` interface and delegates the work to it, without knowing the concrete implementation. Each `ConcreteStrategy` implements the same interface with a variation of the behavior (for example, different ways to amortize a loan, sort data, or compress files).

The strategy is normally chosen by the client and injected into the context — via constructor or setter — and can be swapped at runtime. This replaces scattered conditionals with composition, keeping each algorithm isolated, testable, and extensible without changing the context.

## Problems it solves

- Classes with long `if/else` or `switch` blocks that select among variations of the same algorithm
- The need to change an object's behavior at runtime (by configuration, user profile, or context)
- A proliferation of subclasses that differ only in how they perform one operation
- Algorithms with implementation details (data structures, dependencies) that shouldn't leak to the client

## When to use

- There are several related classes that differ only in behavior
- You need different variants of an algorithm (for example, with distinct memory and time trade-offs)
- The algorithm must be selected or replaced dynamically, including through dependency injection
- Variable business rules, such as pricing policies, discounts, tax calculation, retry/backoff, or load balancing

## When to avoid

- There are only one or two stable algorithms that rarely change — a simple conditional is more readable
- Clients shouldn't need to know the differences between strategies in order to pick one
- The language offers first-class functions and a lambda solves the problem without the ceremony of classes and interfaces
- The strategies would need very different interfaces, forcing parameters that some implementations ignore

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Eliminates conditionals and follows the Open/Closed Principle | Increases the number of classes/objects in the system |
| Algorithms are interchangeable at runtime | The client needs to know the available strategies to pick the right one |
| Each algorithm is isolated and individually testable | Communication overhead: the common interface may pass data that some strategies don't use |
| Composition instead of inheritance | Extra indirection can make the flow harder to read in simple cases |

- **Coupling:** the context depends only on the `Strategy` abstraction; the concrete implementations stay isolated.
- **Testability:** the context can be tested with a fake strategy, and each strategy can be tested without the context.
- **Complexity:** strategy selection usually lives in a factory, a registry map, or the DI container configuration.
- **Performance:** stateless strategies can be shared (including as Flyweights) to avoid repeated allocations.

## Diagram

```mermaid
classDiagram
    class Client
    class Context {
        -Strategy strategy
        +setStrategy(Strategy strategy)
        +executeStrategy(Data data) Result
    }
    class Strategy {
        <<interface>>
        +execute(Data data) Result
    }
    class ConcreteStrategyA {
        +execute(Data data) Result
    }
    class ConcreteStrategyB {
        +execute(Data data) Result
    }
    Client --> Context : configures
    Client ..> ConcreteStrategyA : chooses
    Context o--> Strategy : delegates
    Strategy <|.. ConcreteStrategyA
    Strategy <|.. ConcreteStrategyB
```

The `Client` chooses a `ConcreteStrategy` and hands it to the `Context`, which keeps a reference to the `Strategy` interface and delegates the execution of the algorithm to it. New strategies can be added by implementing the interface, without changing the `Context`.

## Example

A fintech's credit simulator calculates the installments of a loan using the amortization system the customer chose: SAC, with decreasing installments, or Price, with fixed installments. The rate is illustrative.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
interface AmortizationStrategy {
    // Returns the amount of each installment, in cents.
    long[] schedule(long principalCents, double monthlyRate, int months);
}

class SacAmortization implements AmortizationStrategy {
    public long[] schedule(long principalCents, double monthlyRate, int months) {
        double amortization = (double) principalCents / months;
        long[] installments = new long[months];
        for (int i = 0; i < months; i++) {
            double balance = principalCents - amortization * i;
            installments[i] = Math.round(amortization + balance * monthlyRate);
        }
        return installments;
    }
}

class PriceAmortization implements AmortizationStrategy {
    public long[] schedule(long principalCents, double monthlyRate, int months) {
        double factor = monthlyRate / (1 - Math.pow(1 + monthlyRate, -months));
        long[] installments = new long[months];
        Arrays.fill(installments, Math.round(principalCents * factor));
        return installments;
    }
}

class LoanSimulator {
    private AmortizationStrategy amortization;

    LoanSimulator(AmortizationStrategy amortization) { this.amortization = amortization; }

    void setAmortization(AmortizationStrategy amortization) { this.amortization = amortization; }

    long[] simulate(long principalCents, double monthlyRate, int months) {
        return amortization.schedule(principalCents, monthlyRate, months);
    }
}

// R$ 10,000.00 at 2% per month, in 10 installments
LoanSimulator simulator = new LoanSimulator(new SacAmortization());
long[] sac = simulator.simulate(1_000_000, 0.02, 10);
System.out.println(sac[0] + " " + sac[9]); // 120000 102000

simulator.setAmortization(new PriceAmortization());
long[] price = simulator.simulate(1_000_000, 0.02, 10);
System.out.println(price[0] + " " + price[9]); // 111327 111327
```

</TabItem>
<TabItem value="python" label="Python">

```python
from typing import Protocol

class AmortizationStrategy(Protocol):
    def schedule(self, principal_cents: int, monthly_rate: float, months: int) -> list[int]:
        """Returns the amount of each installment, in cents."""
        ...

class SacAmortization:
    def schedule(self, principal_cents: int, monthly_rate: float, months: int) -> list[int]:
        amortization = principal_cents / months
        return [
            round(amortization + (principal_cents - amortization * i) * monthly_rate)
            for i in range(months)
        ]

class PriceAmortization:
    def schedule(self, principal_cents: int, monthly_rate: float, months: int) -> list[int]:
        factor = monthly_rate / (1 - (1 + monthly_rate) ** -months)
        return [round(principal_cents * factor)] * months

class LoanSimulator:
    def __init__(self, amortization: AmortizationStrategy) -> None:
        self.amortization = amortization

    def simulate(self, principal_cents: int, monthly_rate: float, months: int) -> list[int]:
        return self.amortization.schedule(principal_cents, monthly_rate, months)

# R$ 10,000.00 at 2% per month, in 10 installments
simulator = LoanSimulator(SacAmortization())
sac = simulator.simulate(1_000_000, 0.02, 10)
print(sac[0], sac[9])  # 120000 102000

simulator.amortization = PriceAmortization()
price = simulator.simulate(1_000_000, 0.02, 10)
print(price[0], price[9])  # 111327 111327
```

</TabItem>
<TabItem value="go" label="Go">

```go
type AmortizationStrategy interface {
	// Returns the amount of each installment, in cents.
	Schedule(principalCents int64, monthlyRate float64, months int) []int64
}

type SacAmortization struct{}

func (SacAmortization) Schedule(principalCents int64, monthlyRate float64, months int) []int64 {
	amortization := float64(principalCents) / float64(months)
	installments := make([]int64, months)
	for i := range installments {
		balance := float64(principalCents) - amortization*float64(i)
		installments[i] = int64(math.Round(amortization + balance*monthlyRate))
	}
	return installments
}

type PriceAmortization struct{}

func (PriceAmortization) Schedule(principalCents int64, monthlyRate float64, months int) []int64 {
	factor := monthlyRate / (1 - math.Pow(1+monthlyRate, float64(-months)))
	installments := make([]int64, months)
	for i := range installments {
		installments[i] = int64(math.Round(float64(principalCents) * factor))
	}
	return installments
}

type LoanSimulator struct {
	Amortization AmortizationStrategy
}

func (s *LoanSimulator) Simulate(principalCents int64, monthlyRate float64, months int) []int64 {
	return s.Amortization.Schedule(principalCents, monthlyRate, months)
}

func main() {
	// R$ 10,000.00 at 2% per month, in 10 installments
	simulator := &LoanSimulator{Amortization: SacAmortization{}}
	sac := simulator.Simulate(1_000_000, 0.02, 10)
	fmt.Println(sac[0], sac[9]) // 120000 102000

	simulator.Amortization = PriceAmortization{}
	price := simulator.Simulate(1_000_000, 0.02, 10)
	fmt.Println(price[0], price[9]) // 111327 111327
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface AmortizationStrategy {
  // Returns the amount of each installment, in cents.
  schedule(principalCents: number, monthlyRate: number, months: number): number[];
}

class SacAmortization implements AmortizationStrategy {
  schedule(principalCents: number, monthlyRate: number, months: number): number[] {
    const amortization = principalCents / months;
    return Array.from({ length: months }, (_, i) => {
      const balance = principalCents - amortization * i;
      return Math.round(amortization + balance * monthlyRate);
    });
  }
}

class PriceAmortization implements AmortizationStrategy {
  schedule(principalCents: number, monthlyRate: number, months: number): number[] {
    const factor = monthlyRate / (1 - Math.pow(1 + monthlyRate, -months));
    const installment = Math.round(principalCents * factor);
    return Array.from({ length: months }, () => installment);
  }
}

class LoanSimulator {
  constructor(private amortization: AmortizationStrategy) {}

  setAmortization(amortization: AmortizationStrategy): void {
    this.amortization = amortization;
  }

  simulate(principalCents: number, monthlyRate: number, months: number): number[] {
    return this.amortization.schedule(principalCents, monthlyRate, months);
  }
}

// R$ 10,000.00 at 2% per month, in 10 installments
const simulator = new LoanSimulator(new SacAmortization());
const sac = simulator.simulate(1_000_000, 0.02, 10);
console.log(sac[0], sac[9]); // 120000 102000

simulator.setAmortization(new PriceAmortization());
const price = simulator.simulate(1_000_000, 0.02, 10);
console.log(price[0], price[9]); // 111327 111327
```

</TabItem>
</Tabs>

## Related patterns

- [State](/coding/gof/behavioral/state) — almost identical structure, but in State the states swap themselves according to the lifecycle, while in Strategy the choice usually comes from the client
- [Template Method](/coding/gof/behavioral/template-method) — varies parts of an algorithm through inheritance, while Strategy varies the whole algorithm through composition
- [Decorator](/coding/gof/structural/decorator) — Decorator changes an object's "skin"; Strategy changes its "guts"
- [Bridge](/coding/gof/structural/bridge) — similar structure of delegating to an implementation, but aimed at separating abstraction and implementation into independent hierarchies
- [Command](/coding/gof/behavioral/command) — both encapsulate behavior in objects; Command represents an action to perform, Strategy a way of doing something
- [Flyweight](/coding/gof/structural/flyweight) — stateless strategies can be shared as flyweights
- [Factory Method](/coding/gof/creational/factory-method) — often used to create the appropriate strategy from configuration or user input
- [Null Object](/coding/gof/behavioral/null-object) — can act as a default strategy that does nothing, avoiding null checks in the context

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Strategy on Refactoring.Guru](https://refactoring.guru/design-patterns/strategy)
