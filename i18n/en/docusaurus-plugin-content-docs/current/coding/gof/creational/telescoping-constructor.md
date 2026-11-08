---
title: Telescoping Constructor
pattern_slug: telescoping-constructor
category: Creational
tags:
  - Simplicity
origin: Classic
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Telescoping Constructor"
---

# Telescoping Constructor

## Description

Telescoping Constructor is an object-creation technique in which a class offers a sequence of overloaded constructors, each accepting one more parameter than the previous one. The smaller constructors delegate to the larger ones, filling in the missing parameters with default values, until reaching a "full" constructor that actually initializes the object. The name comes from the image of a telescope extending segment by segment.

It isn't one of the 23 patterns in the GoF catalog. In the literature (notably *Effective Java*, by Joshua Bloch) it's usually presented as an **anti-pattern**: it works well with few parameters, but scales poorly as the number of optional fields grows — calls become hard to read, argument order becomes a trap, and the number of constructors explodes. [Builder](/coding/gof/creational/builder) is the solution usually recommended in that scenario.

Still, the technique has real merits: it produces immutable, fully initialized objects in a single call, requires no helper classes, and is idiomatic in languages without named parameters. For objects with two or three optional parameters, it's often the simplest and most direct option. In languages with named parameters and default values (Kotlin, C#, Python), the problem practically disappears, since a single constructor replaces the whole chain.

## Problems it solves

- Allowing an object to be created by providing only the required parameters, using default values for the optional ones
- Centralizing initialization and validation logic in a single "full" constructor, avoiding duplication
- Ensuring the object is born in a valid state and can be immutable (`final`/`readonly` fields), without setters
- Offering default values in languages that don't support optional or named parameters

## When to use

- The class has few optional parameters (typically up to three or four)
- The optional parameters have a natural order of "importance", so it makes sense to add them progressively
- Immutability and atomic initialization are desirable and you don't want the cost of a Builder class
- The language offers neither named parameters nor default values

## When to avoid

- There are many optional parameters, or they grow frequently — prefer [Builder](/coding/gof/creational/builder)
- Several consecutive parameters have the same type (e.g., several `int` or `boolean`), which makes it easy to swap arguments without a compile error
- The client needs to combine optionals arbitrarily (skip the second and supply the third), which the linear chain doesn't allow
- The language already offers named parameters and default values, making the chain of overloads unnecessary

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Simple, with no helper classes | The number of constructors grows linearly (and combinations not covered are unreachable) |
| Immutable, valid object after a single call | Calls with many positional arguments are hard to read (`new Pizza(30, true, false, true)`) |
| Default values and validation centralized in the full constructor | Arguments of the same type can be silently swapped |
| Safe for concurrent use (no intermediate state) | Adding a new optional field requires a new constructor and changes the public API |

- **Readability:** the most criticized point; IDEs with parameter hints soften it but don't solve the problem in code review.
- **Maintenance:** each new optional extends the chain; inserting a parameter "in the middle" breaks the order and existing clients.
- **Alternatives:** Builder (readability and arbitrary combinations), JavaBeans/setters (readable, but loses immutability and allows inconsistent states), static factory methods with descriptive names, or named parameters when the language allows.

## Diagram

```mermaid
classDiagram
    class Client
    class NutritionFacts {
        -int servingSize
        -int servings
        -int calories
        -int fat
        -int sodium
        +NutritionFacts(servingSize, servings)
        +NutritionFacts(servingSize, servings, calories)
        +NutritionFacts(servingSize, servings, calories, fat)
        +NutritionFacts(servingSize, servings, calories, fat, sodium)
    }
    Client ..> NutritionFacts : new
```

The `Client` instantiates `NutritionFacts` by choosing the constructor with the number of arguments it needs. Each smaller constructor delegates (via `this(...)`) to the next one, passing a default value, until reaching the full constructor, which assigns all the fields.

## Example

A nutrition facts class requires a serving size and a number of servings, while calories, fat, and sodium are optional with a default of zero.

```java
public final class NutritionFacts {
    private final int servingSize; // required
    private final int servings;    // required
    private final int calories;    // optional
    private final int fat;         // optional
    private final int sodium;      // optional

    public NutritionFacts(int servingSize, int servings) {
        this(servingSize, servings, 0);
    }
    public NutritionFacts(int servingSize, int servings, int calories) {
        this(servingSize, servings, calories, 0);
    }
    public NutritionFacts(int servingSize, int servings, int calories, int fat) {
        this(servingSize, servings, calories, fat, 0);
    }
    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium) {
        if (servingSize <= 0 || servings <= 0) throw new IllegalArgumentException();
        this.servingSize = servingSize;
        this.servings = servings;
        this.calories = calories;
        this.fat = fat;
        this.sodium = sodium;
    }
}

// Usage: what does each number mean? Swapping fat and sodium compiles without error.
NutritionFacts cola = new NutritionFacts(240, 8, 100, 0, 35);
```

## Related patterns

- [Builder](/coding/gof/creational/builder) — the recommended alternative when there are many optional parameters; offers readable calls and arbitrary combinations while keeping immutability
- [Factory Method](/coding/gof/creational/factory-method) — creation methods with descriptive names can replace ambiguous constructor overloads
- [Factory](/coding/gof/creational/factory) — encapsulates the choice of default values and the creation, hiding the constructor chain from the client
- [Prototype](/coding/gof/creational/prototype) — another way to avoid long parameter lists: clone a pre-configured object and adjust only what's needed

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
