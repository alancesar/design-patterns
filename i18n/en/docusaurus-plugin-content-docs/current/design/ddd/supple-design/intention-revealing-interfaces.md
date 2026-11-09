---
title: Intention-Revealing Interfaces
pattern_slug: intention-revealing-interfaces
category: Supple Design
tags:
  - Shared Understanding
  - Simplicity
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Intention-Revealing Interfaces"
---

# Intention-Revealing Interfaces

## Description

Intention-Revealing Interfaces means naming classes, methods, and arguments so that they express the purpose and the observable effect, not how the result is obtained. The name comes from the Ubiquitous Language: whoever uses the component understands what it does without having to read the implementation.

In practice, the contract is written first, for example with a test that shows how the client wants to use the operation. Then the implementation is written behind that interface. If the developer has to open the code to find out what a method does, encapsulation has been lost: the client now depends on the internal details.

The pattern is the foundation of Supple Design. Interfaces that reveal intention make the other techniques (side-effect-free functions, assertions, closed operations) easier to apply and to communicate.

## Problems it solves

- Generic names (`process`, `handle`, `calculate`) that force you to read the implementation to understand the effect.
- Clients coupled to the internal mechanism rather than to the purpose of the operation.
- Developers who reimplement something that already exists because they didn't realize what the method did.
- Distance between the business vocabulary and the code vocabulary.

## When to use

- In any public class or method of the domain model.
- When business experts and developers need to read the same code or the same tests.
- When refactoring methods whose name describes the "how" instead of the "what".

## When to avoid

- In private, volatile internal details, where a wordy name adds little value.
- When the concept hasn't been understood yet: a "nice" name for a wrong model only gives false confidence. Deepen the model first.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Code readable by people who don't know the implementation | Requires knowing the domain well to choose good names |
| Less duplication and less reading of internal code | Renaming public APIs can affect many clients |
| Tests that serve as documentation | Bad names kept out of inertia lose the benefit |

- **Shared language:** the code's vocabulary and the conversation's vocabulary evolve together.
- **Encapsulation:** the client depends on the contract, not the mechanism.
- **Maintenance:** names need to be revisited when the understanding of the domain changes.

## Diagram

```mermaid
classDiagram
    class PaintBefore {
        +paint(Paint other)
    }
    class PaintAfter {
        +mixIn(Paint other)
        +volume() int
    }
    note for PaintBefore "Name does not reveal whether it mixes, replaces, or adds"
    note for PaintAfter "Name reveals the effect: the paint receives the mix"
```

In `PaintBefore`, the method doesn't say what happens to the paint; in `PaintAfter`, `mixIn` reveals the intention and the effect.

## Example

A paint module had a method `paint(Paint other)` that actually mixed the other paint into the current volume. The client had to read the method body to find out the effect. Renamed to `mixIn`, the contract is clear and the test says what's expected.

```java
public class Paint {
    private int volume;
    private PigmentColor color;

    // Before: public void paint(Paint other)
    public void mixIn(Paint other) {
        color = color.mixedWith(other.color, volume, other.volume);
        volume += other.volume;
    }

    public int volume() { return volume; }
}

// The test writes the contract before the implementation
Paint blue = new Paint(100, PigmentColor.BLUE);
blue.mixIn(new Paint(50, PigmentColor.YELLOW));
assertEquals(150, blue.volume());
```

## Related patterns

- [Side-Effect-Free Functions](/design/ddd/supple-design/side-effect-free-functions) — separates queries from commands, making the effect explicit.
- [Assertions](/design/ddd/supple-design/assertions) — declare the effects and invariants that the name only suggests.
- [Ubiquitous Language](/design/ddd/model-in-practice/ubiquitous-language) — the source of the names used in the interfaces.
- [Model-Driven Design](/design/ddd/model-in-practice/model-driven-design) — ties the model to the code through these interfaces.
- [Refactoring Toward Deeper Insight](/design/ddd/model-in-practice/refactoring-toward-deeper-insight) — new insights produce new names.

## Reference

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
