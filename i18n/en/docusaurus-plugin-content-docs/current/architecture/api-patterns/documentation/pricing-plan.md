---
title: Pricing Plan
pattern_slug: pricing-plan
category: Documentation
tags:
  - Shared Understanding
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Pricing Plan"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/documentation/pricing-plan.mdx';

# Pricing Plan

## Description

The Pricing Plan pattern attaches to the API description a pricing policy that defines how consumption is metered and charged to clients, advertisers or other parties, so that the provider funds the API and the client knows what it will pay.

An API is an asset with monetary and immaterial value, and building and running it costs money. The pricing plan makes costs and mutual obligations explicit (invoicing, payment, limits). It also defines the metrics to measure, such as calls per operation or the volume of data transferred.

Three variants are the most common. With **subscription-based pricing**, the client pays a recurring fee independent of usage, often combined with a [Rate Limit](/architecture/api-patterns/documentation/rate-limit) for fair use and with tiers among which the client chooses. With **usage-based pricing**, the client pays only for what it consumes, with prices that can vary per operation, or through prepaid packages of credits. With **market-based pricing**, the price follows demand and clients place bids. Plans can be combined: a free (freemium) tier for low usage, or a base subscription plus charges for overage.

## Problems it solves

- Funding the development and operation of an API without treating hobbyists and high-volume clients alike
- Giving the client predictability about cost and control over spending limits
- Metering consumption at a level of detail both sides accept
- Making billing auditable without exposing one client's data to another

## When to use

- When the API is a product or has a relevant cost that must be recovered
- When there are client segments with very different usage profiles (hobbyist, startup, large company)
- When you want to encourage adoption with a free tier and convert to paid plans
- When the provider needs to align technical and commercial limits in a single agreement

## When to avoid

- In internal APIs of a single organization, where cost is shared in another way
- When the cost of metering and charging exceeds the revenue charging would bring
- When the client cannot be reliably identified (see [API Key](/architecture/api-patterns/special-purpose-representations/api-key)): without identity there is no correct billing

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Revenue proportional to the value delivered and a clear agreement on costs | Setting fair prices requires knowing the clients' business and is hard to get right |
| Subscription is simple to run and predictable | Very low or very high usage ends up badly priced |
| Usage-based pricing is fair and follows consumption | Requires detailed metering, reports and dispute handling |
| Tiers combined with limits protect capacity | More plans mean more complexity to communicate and maintain |

- **Metering:** if the metering system goes down, the provider loses revenue; you must choose between pausing the API or serving it free during the outage.
- **Accuracy and performance:** counting every call exactly may cost latency; a daily aggregate lowers the cost but reduces transparency.
- **Security and privacy:** billing data is sensitive, and in multitenant environments one client must not see or infer another's usage.
- **Evolution:** start with a subscription and add usage-based pricing later if needed, since the former is much simpler to implement.

## Diagram

<Diagram />

The gateway identifies the client, meters usage and forwards the events to billing, which applies the tiers defined in the plan.

## Example

The fintech charges for access to the Pix charges API by monthly call tier, with a free level. Values are illustrative and always in cents. The table published in the documentation is:

```text
Calls per month (up to)   Price per month
1,000                     free
50,000                    R$ 299.00
500,000                   R$ 1,499.00
above that                contact sales
```

Code that computes a client's invoice from the month's total calls.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.List;

public class PricingPlanDemo {
    record Tier(long upToCalls, long priceCents) {}

    static class PricingPlan {
        private final List<Tier> tiers;

        PricingPlan(List<Tier> tiers) { this.tiers = tiers; }

        long monthlyChargeCents(long calls) {
            for (Tier tier : tiers) {
                if (calls <= tier.upToCalls()) {
                    return tier.priceCents();
                }
            }
            throw new IllegalArgumentException("above the highest tier: contact sales");
        }
    }

    public static void main(String[] args) {
        PricingPlan plan = new PricingPlan(List.of(
                new Tier(1_000, 0),
                new Tier(50_000, 29_900),
                new Tier(500_000, 149_900)));
        System.out.println(plan.monthlyChargeCents(800));     // 0
        System.out.println(plan.monthlyChargeCents(12_000));  // 29900
        System.out.println(plan.monthlyChargeCents(300_000)); // 149900
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Tier:
    up_to_calls: int
    price_cents: int


class PricingPlan:
    def __init__(self, tiers: List[Tier]) -> None:
        self.tiers = tiers

    def monthly_charge_cents(self, calls: int) -> int:
        for tier in self.tiers:
            if calls <= tier.up_to_calls:
                return tier.price_cents
        raise ValueError("above the highest tier: contact sales")


plan = PricingPlan([Tier(1_000, 0), Tier(50_000, 29_900), Tier(500_000, 149_900)])
print(plan.monthly_charge_cents(800))      # 0
print(plan.monthly_charge_cents(12_000))   # 29900
print(plan.monthly_charge_cents(300_000))  # 149900
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"errors"
	"fmt"
)

type Tier struct {
	UpToCalls  int64
	PriceCents int64
}

type PricingPlan struct {
	Tiers []Tier
}

// In Go, exceeding the tiers comes back as an error, not an exception.
func (p PricingPlan) MonthlyChargeCents(calls int64) (int64, error) {
	for _, tier := range p.Tiers {
		if calls <= tier.UpToCalls {
			return tier.PriceCents, nil
		}
	}
	return 0, errors.New("above the highest tier: contact sales")
}

func main() {
	plan := PricingPlan{Tiers: []Tier{
		{1_000, 0}, {50_000, 29_900}, {500_000, 149_900},
	}}
	for _, calls := range []int64{800, 12_000, 300_000} {
		charge, _ := plan.MonthlyChargeCents(calls)
		fmt.Println(charge) // 0, 29900, 149900
	}
}
```

</TabItem>
</Tabs>

## Related patterns

- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — enforces in practice the limits of each plan tier
- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — the plan should reference the SLA that goes with each tier
- [API Description](/architecture/api-patterns/documentation/api-description) — the API description is where the plan is attached
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — identifies the client whose usage is metered and charged
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) and [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — help the client reduce data volume when billing depends on it
- [API Gateway](/architecture/microservices/external-api/api-gateway) — the natural place to meter usage and apply the plan

## Reference

- [Patterns for API Design, chapter 9: Pricing Plan](https://api-patterns.org/)
