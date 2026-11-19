---
title: Experimental Preview
pattern_slug: experimental-preview
category: Life-Cycle Management
tags:
  - Evolvability
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Experimental Preview"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/life-cycle-management/experimental-preview.mdx';

# Experimental Preview

## Description

The Experimental Preview pattern makes an API available on a best-effort basis, with no commitment to functionality, stability or lifetime, and states this lack of maturity explicitly so that clients adjust their expectations.

The provider publishes a still-unstable version outside the normal management process, for example in a sandbox with no service level agreement and a draft API description. Clients join voluntarily, knowing the preview may change in incompatible ways, disappear without notice or run for a short, fixed period only. In return they get early access: they can estimate the integration effort and get a head start while the final API is still being designed. The preview can be open to any client or restricted to a closed group, (for example with specific [API Keys](/architecture/api-patterns/special-purpose-representations/api-key)), which limits the support and communication effort. It usually runs in a nonproduction environment tied to the version under development, with very lax service levels; whoever prefers stability stays on the official version. It is the weakest support commitment a provider can offer, similar to a beta program, and the provider may grant a grace period when the preview is promoted.

## Problems it solves

- Launching a new API without knowing whether the design meets the real needs of clients
- Preventing the incompatible changes still expected during development from breaking production integrations
- Giving interested clients a way to test and give opinions before the API is frozen
- Not taking on, too early, the guarantees and support cost of a stable API
- The alternative of waiting for the final version keeps clients from starting to integrate for months, and releasing frequent incompatible versions overloads governance and makes tracking hard

## When to use

- When a new feature or a major redesign is still in the discovery phase
- When the provider wants feedback from key clients before fixing contracts and versions
- When performance, security or usability must be validated at a smaller scale
- As a stage before delivering the API to production, combined with [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) or [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee)

## When to avoid

- When clients already depend on the feature in production and cannot tolerate breaking changes
- When the API is regulated or critical and needs formal guarantees from day one
- When there is no team to collect and act on feedback: the preview becomes an unstable API with no purpose
- When the warning about instability will not clearly reach the clients

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Early feedback from the people who will use the API | Clients may use the preview in production despite the warning |
| Freedom to change the design without versioning | Relationships may suffer if changes are too frequent |
| Lower support and governance cost | The lack of guarantees must be communicated clearly |
| Early integration for interested clients | Client work may be thrown away when the preview changes or goes away |

- **Expectations:** put the status in the URL, in the documentation and in the responses, so nobody mistakes it for the stable API.
- **Deadline:** a preview with no end date tends to become the de facto API; define when it ends or gets promoted.
- **Audience:** a closed group reduces support but also reduces the volume of feedback.
- **Extra environment:** operating and securing one more environment and access channel takes effort, and development becomes transparent, with mistakes that will not be part of the final API.
- **Attractiveness:** the lack of a long-term commitment may make the API look immature and put clients off.
- **Promotion:** once stable, publish the final version with the identifier and guarantees of the chosen life-cycle pattern.

## Diagram

<Diagram />

The beta versions change and may disappear without notice; only the version promoted to production takes on compatibility and lifetime guarantees.

## Example

A fintech wants to open an installment Pix charge API (automatic Pix) to partners. Before fixing the contract, it publishes a preview on a separate host, with an explicit warning in the responses.

```http
POST /v2beta1/pix-charges HTTP/1.1
Host: sandbox.api.fintech.example
Content-Type: application/json

{"accountId": "acc-4821", "amountCents": 125000, "currency": "BRL", "installments": 3}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json
Warning: 299 - "Experimental Preview: no guarantees of stability or availability"

{
  "id": "pix-9f3a",
  "status": "PENDING",
  "amountCents": 125000,
  "currency": "BRL",
  "installments": 3,
  "preview": {"stage": "beta1", "mayChangeWithoutNotice": true, "endsOn": "2027-02-28"}
}
```

The `beta1` suffix, the sandbox host, the `Warning` header and the `preview` object make it clear there are no guarantees, and `endsOn` sets the end of the preview.

## Related patterns

- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) — governs the production API's life cycle once the preview ends; in the N in Production variant, the preview can coexist with the other versions
- [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee) — the guarantee the final API offers, unlike the preview
- [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence) — removes parts of a stable API with advance notice, while the preview offers not even that
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — can restrict preview access to selected clients
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — identifies the beta versions and the final version, although the preview is not required to have one
- [API Description](/architecture/api-patterns/documentation/api-description) — the preview usually has a draft description
- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — the preview is normally not covered by an SLA
- [Strangler Fig](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig) — gradually moves functionality to a new system; here the goal is to test a new API with volunteer clients

## Reference

- [Patterns for API Design, chapter 8: Experimental Preview](https://api-patterns.org/)
