---
title: Feature Toggle
pattern_slug: feature-toggle
category: Release
tags:
  - Operational Excellence
  - Reliability
source: https://martinfowler.com/articles/feature-toggles.html
sidebar_label: "Feature Toggle"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/feature-toggle.mdx';

# Feature Toggle

## Description

Feature Toggle, also called Feature Flag, wraps a feature in a condition that can be turned on or off at runtime, without a new deployment. The new code ships to production switched off, and the decision to turn it on, for everyone or for a group of users, becomes a configuration change. Deploying a version and launching a feature stop being the same event.

Pete Hodgson classifies toggles by purpose and lifetime: *release toggles* hide unfinished work and last days or weeks; *experiment toggles* support A/B tests; *ops toggles* act as a *kill switch* to turn off a misbehaving feature; and *permissioning toggles* unlock features for specific groups of customers. The decision usually lives at a single point, which reads a configuration store and evaluates rules such as an allowlist of accounts or a percentage of users.

## Problems it solves

- Deployment coupled to launch, which forces deciding at deploy time whether the feature should already be visible.
- Long-lived branches to hide unfinished work, with painful merges at the end.
- No quick way to turn off a broken feature without reverting the deployment.
- Launching to everyone at once, without testing with a small group of customers.

## When to use

- Continuous integration with unfinished features on the main trunk.
- Gradual launches per feature, per customer group or by percentage.
- A/B tests and product experiments.
- A *kill switch* for risky features, such as a new payment method.

## When to avoid

- Small, low-risk changes, where the toggle only adds complexity.
- As a permanent replacement for configuration or permission rules, with no removal date.
- Schema or infrastructure changes that cannot be switched off by a condition in code.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Deployment independent from launch | Forgotten toggles become technical debt |
| Immediate switch-off, without a new deployment | Toggle combinations multiply the paths to test |
| Gradual launch per customer or percentage | Configuration becomes a critical part of production |
| A/B experiments with the same code | Scattered conditional logic hurts readability |

- **Planned removal:** every release toggle should be born with a deadline and an owner for its removal. Some teams cap how many active toggles each service may have.
- **Decision at one point:** centralize evaluation in a service or library and pass the decision along, instead of scattering `if` statements through the code.
- **Tests:** test both states of each toggle that goes to production, not every possible combination.
- **Sticky assignment:** in percentage rollouts, use a hash of the customer identifier so the same account always lands in the same group.

## Diagram

<Diagram />

The same artifact runs in production with both paths. The configuration decides which one each account sees.

## Example

The fintech's digital account is about to launch Pix installments. The code is already in production, but checkout only shows the new option to the accounts the `pix-installments` toggle lets through: an allowlist of internal accounts and 30% of the rest, chosen by a stable hash of the identifier. If something goes wrong, the team turns the toggle off and everyone goes back to seeing only single-payment Pix.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

record Toggle(boolean enabled, int rolloutPercent, Set<String> allowlist) {}

class FeatureToggles {
    private final Map<String, Toggle> toggles = new HashMap<>();

    void define(String name, Toggle toggle) {
        toggles.put(name, toggle);
    }

    boolean isEnabled(String name, String accountId) {
        Toggle t = toggles.get(name);
        if (t == null || !t.enabled()) {
            return false; // unknown or switched-off toggle: current behavior
        }
        if (t.allowlist().contains(accountId)) {
            return true;
        }
        return bucket(name + ":" + accountId) < t.rolloutPercent();
    }

    // 32-bit FNV-1a: the same account always lands in the same bucket (0 to 99)
    static int bucket(String key) {
        int hash = 0x811c9dc5;
        for (byte b : key.getBytes(StandardCharsets.UTF_8)) {
            hash ^= (b & 0xff);
            hash *= 0x01000193;
        }
        return (int) (Integer.toUnsignedLong(hash) % 100);
    }
}

class PixCheckout {
    private final FeatureToggles toggles;

    PixCheckout(FeatureToggles toggles) {
        this.toggles = toggles;
    }

    List<String> paymentOptions(String accountId) {
        if (toggles.isEnabled("pix-installments", accountId)) {
            return List.of("pix", "pix-installments");
        }
        return List.of("pix");
    }
}

public class FeatureToggleDemo {
    public static void main(String[] args) {
        FeatureToggles toggles = new FeatureToggles();
        toggles.define("pix-installments", new Toggle(true, 30, Set.of("acc-001")));
        PixCheckout checkout = new PixCheckout(toggles);

        for (String id : List.of("acc-001", "acc-002", "acc-003", "acc-004", "acc-005")) {
            System.out.println(id + ": " + String.join(", ", checkout.paymentOptions(id)));
        }

        // kill switch: turns the feature off without a new deployment
        toggles.define("pix-installments", new Toggle(false, 30, Set.of("acc-001")));
        System.out.println("acc-001: " + String.join(", ", checkout.paymentOptions("acc-001")));
    }
}

// acc-001: pix, pix-installments
// acc-002: pix
// acc-003: pix
// acc-004: pix, pix-installments
// acc-005: pix
// acc-001: pix
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List


@dataclass(frozen=True)
class Toggle:
    enabled: bool
    rollout_percent: int
    allowlist: FrozenSet[str] = field(default_factory=frozenset)


class FeatureToggles:
    def __init__(self) -> None:
        self._toggles: Dict[str, Toggle] = {}

    def define(self, name: str, toggle: Toggle) -> None:
        self._toggles[name] = toggle

    def is_enabled(self, name: str, account_id: str) -> bool:
        t = self._toggles.get(name)
        if t is None or not t.enabled:
            return False  # unknown or switched-off toggle: current behavior
        if account_id in t.allowlist:
            return True
        return bucket(f"{name}:{account_id}") < t.rollout_percent


def bucket(key: str) -> int:
    # 32-bit FNV-1a: the same account always lands in the same bucket (0 to 99)
    h = 0x811C9DC5
    for b in key.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h % 100


class PixCheckout:
    def __init__(self, toggles: FeatureToggles) -> None:
        self._toggles = toggles

    def payment_options(self, account_id: str) -> List[str]:
        if self._toggles.is_enabled("pix-installments", account_id):
            return ["pix", "pix-installments"]
        return ["pix"]


toggles = FeatureToggles()
toggles.define("pix-installments", Toggle(True, 30, frozenset({"acc-001"})))
checkout = PixCheckout(toggles)

for account_id in ["acc-001", "acc-002", "acc-003", "acc-004", "acc-005"]:
    print(f"{account_id}: {', '.join(checkout.payment_options(account_id))}")

# kill switch: turns the feature off without a new deployment
toggles.define("pix-installments", Toggle(False, 30, frozenset({"acc-001"})))
print(f"acc-001: {', '.join(checkout.payment_options('acc-001'))}")
# acc-001: pix, pix-installments
# acc-002: pix
# acc-003: pix
# acc-004: pix, pix-installments
# acc-005: pix
# acc-001: pix
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"hash/fnv"
	"strings"
)

type Toggle struct {
	Enabled        bool
	RolloutPercent uint32
	Allowlist      map[string]bool
}

type FeatureToggles struct {
	toggles map[string]Toggle
}

func NewFeatureToggles() *FeatureToggles {
	return &FeatureToggles{toggles: map[string]Toggle{}}
}

func (f *FeatureToggles) Define(name string, t Toggle) {
	f.toggles[name] = t
}

func (f *FeatureToggles) IsEnabled(name, accountID string) bool {
	t, ok := f.toggles[name]
	if !ok || !t.Enabled {
		return false // unknown or switched-off toggle: current behavior
	}
	if t.Allowlist[accountID] {
		return true
	}
	return bucket(name+":"+accountID) < t.RolloutPercent
}

// 32-bit FNV-1a: the same account always lands in the same bucket (0 to 99)
func bucket(key string) uint32 {
	h := fnv.New32a()
	h.Write([]byte(key))
	return h.Sum32() % 100
}

type PixCheckout struct {
	toggles *FeatureToggles
}

func (c PixCheckout) PaymentOptions(accountID string) []string {
	if c.toggles.IsEnabled("pix-installments", accountID) {
		return []string{"pix", "pix-installments"}
	}
	return []string{"pix"}
}

func main() {
	toggles := NewFeatureToggles()
	toggles.Define("pix-installments", Toggle{Enabled: true, RolloutPercent: 30, Allowlist: map[string]bool{"acc-001": true}})
	checkout := PixCheckout{toggles: toggles}

	for _, id := range []string{"acc-001", "acc-002", "acc-003", "acc-004", "acc-005"} {
		fmt.Printf("%s: %s\n", id, strings.Join(checkout.PaymentOptions(id), ", "))
	}

	// kill switch: turns the feature off without a new deployment
	toggles.Define("pix-installments", Toggle{Enabled: false, RolloutPercent: 30, Allowlist: map[string]bool{"acc-001": true}})
	fmt.Printf("acc-001: %s\n", strings.Join(checkout.PaymentOptions("acc-001"), ", "))
}

// acc-001: pix, pix-installments
// acc-002: pix
// acc-003: pix
// acc-004: pix, pix-installments
// acc-005: pix
// acc-001: pix
```

</TabItem>
</Tabs>

## Related patterns

- [Canary Release](/architecture/microservices/release/canary-release) — gradual rollout per service version, instead of per feature.
- [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment) — version switch without downtime; the toggle decides when the feature shows up.
- [Externalized Configuration](/architecture/cloud-design-patterns/deployment-and-topology/external-configuration-store) — the store toggles are read from at runtime.
- [Log Deployments and Changes](/architecture/microservices/observability/log-deployments-and-changes) — logging toggle changes helps correlate incidents.
- [Strategy](/coding/gof/behavioral/strategy) — swaps the behavior behind the toggle without scattering conditionals.

## Reference

- [Pete Hodgson — Feature Toggles (aka Feature Flags), martinfowler.com](https://martinfowler.com/articles/feature-toggles.html)
