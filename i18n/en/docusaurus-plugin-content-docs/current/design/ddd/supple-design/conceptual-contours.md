---
title: Conceptual Contours
pattern_slug: conceptual-contours
category: Supple Design
tags:
  - Simplicity
  - Strategic Focus
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Conceptual Contours"
---

# Conceptual Contours

## Description

Conceptual Contours means decomposing the design into cohesive units (operations, interfaces, classes, and Aggregates) aligned with the natural contours of the domain. The division isn't arbitrary: it follows what changes together and what changes separately, so that each unit has a coherent responsibility.

When the contours are right, a requirement change tends to affect only one unit, and extensions use the existing pieces. When they're wrong, every change requires altering many parts at once, or you discover that separate concepts are mixed together in a single one.

Contours are rarely found on the first attempt. The team discovers them by refactoring, observing where change hurts, and testing the model against varied scenarios. The pattern guides the reflection: units that are too small fragment the concept, and units that are too large lose cohesion.

## Problems it solves

- Simple changes that require edits scattered across many classes.
- Classes that mix concepts that evolve at different paces.
- Concepts split into fragments that only make sense together.
- Interfaces that force the client to know the details of several pieces.

## When to use

- When you notice that small requirement changes cause large refactorings.
- When reviewing the model after new insights into the domain.
- In Aggregates and classes whose boundary seems arbitrary.

## When to avoid

- Before knowing the domain reasonably well: a division made early tends to be reworked.
- As an excuse for endless refactoring: apply it when there is concrete pain with change.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Changes localized in a few units | Discovering the contours takes iterations and refactoring |
| Reuse and composition of existing pieces | Excessive division fragments the concept |
| A model that reflects the domain's natural structure | The contours change when the domain changes |

- **Cohesion:** each unit expresses a whole concept.
- **Observation:** the change history shows where the real boundaries are.
- **Testing:** varied scenarios reveal whether the design accommodates extensions.

## Diagram

```mermaid
flowchart LR
    A["Before: installment with interest, IOF, and insurance"] -->|"IOF change affects everything"| B["Refactoring"]
    B --> C["Interest"]
    B --> D["Iof"]
    B --> E["Insurance"]
    C -.->|"change independently"| F["Localized changes"]
    D -.-> F
    E -.-> F
```

By separating interest, IOF, and insurance into units that change independently, each requirement change is confined to one of them.

## Example

The installment calculation of a `LoanContract` summed interest, IOF, and insurance in a single method. Because the interest policy changes by commercial decision, IOF by legislation, and insurance by contract with the insurer, every change meant touching the same class. The decomposition follows the contours of the domain. The rules and values are illustrative.

```java
public class InstallmentCalculator {
    private final InterestPolicy interest;
    private final IofPolicy iof;
    private final InsurancePolicy insurance;

    public InstallmentCalculator(InterestPolicy interest, IofPolicy iof, InsurancePolicy insurance) {
        this.interest = interest; this.iof = iof; this.insurance = insurance;
    }

    public Money amountFor(LoanContract contract) {
        Money principalPart = contract.principalPortion();
        return principalPart
            .plus(interest.interestOn(contract))
            .plus(iof.iofOn(contract))
            .plus(insurance.premiumFor(contract));
    }
}
// New IOF rule: only IofPolicy changes.
```

## Related patterns

- [Refactoring Toward Deeper Insight](/design/ddd/model-in-practice/refactoring-toward-deeper-insight) — the main means of discovering the contours.
- [Aggregate](/design/ddd/building-blocks/aggregate) — Aggregate boundaries follow the contours of consistency.
- [Standalone Classes](/design/ddd/supple-design/standalone-classes) — correct contours make independent classes easier.
- [Intention-Revealing Interfaces](/design/ddd/supple-design/intention-revealing-interfaces) — each unit has a name that expresses its concept.
- [Drawing on Established Formalisms](/design/ddd/supple-design/drawing-on-established-formalisms) — formalisms suggest natural divisions.
- [Core Domain](/design/ddd/distillation/core-domain) — the most important contours go where the business value is.
- [Strategy](/coding/gof/behavioral/strategy) (GoF) — encapsulates each policy that varies separately.

## Reference

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
