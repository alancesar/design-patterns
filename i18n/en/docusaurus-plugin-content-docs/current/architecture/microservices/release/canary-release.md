---
title: Canary Release
pattern_slug: canary-release
category: Release
tags:
  - Reliability
  - Operational Excellence
source: https://martinfowler.com/bliki/CanaryRelease.html
sidebar_label: "Canary Release"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/canary-release.mdx';

# Canary Release

## Description

Canary Release rolls out the new version of a service to a small share of users before taking it to everyone. The new version runs alongside the current one, the router diverts a slice of the traffic to it, such as 1% or 5%, and the team compares errors, latency and business metrics between the two. If the numbers hold, the slice grows in steps up to 100%; if they get worse, traffic goes back to the current version.

The name comes from the canaries miners carried to detect toxic gases: a small group is exposed first to protect everyone else. The group can be chosen at random, by region, by customer type, or start with internal users.

## Problems it solves

- Bugs and performance regressions that only show up with real traffic and data.
- Releases that expose every customer to the same risk at once.
- No objective criterion to decide whether a version is ready for everyone.

## When to use

- Changes with higher business risk, such as a new billing or credit analysis rule.
- Services with enough traffic for a small slice to produce reliable metrics.
- When observability can split metrics by version.

## When to avoid

- Low-traffic services, where 1% of requests produces no statistical signal.
- Changes where two versions cannot coexist, such as incompatible contracts or schemas.
- When there is no way to route traffic by percentage or by user group.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Problems hit a small share of customers | Two versions in production at the same time |
| Decision to proceed based on real metrics | Requires percentage routing and per-version metrics |
| Fast rollback by reducing the slice to zero | Slower release, in several steps |
| Does not require doubling the infrastructure | Users may flip between versions if routing is not sticky |

- **Criteria set in advance:** the thresholds that move the release forward or back, such as error rate and p99 latency, should be decided before the launch and, ideally, checked automatically.
- **Sticky routing:** tie the customer to one version (by account, session or header) so they do not see different behavior on each request.
- **Compatibility:** since the versions coexist for hours or days, schema and contract changes must be backward compatible.

## Diagram

<Diagram />

The gateway sends 5% of Pix charges to v2. If v2 metrics stay within the threshold, the slice goes up to 25%, 50% and 100%; if not, it goes back to zero.

## Related patterns

- [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment) — switches all traffic at once, with no gradual exposure.
- [Rolling Deployment](/architecture/microservices/release/rolling-deployment) — also mixes versions, but without control over who gets the new one.
- [Feature Toggle](/architecture/microservices/release/feature-toggle) — does the gradual rollout in code, per feature, instead of per version.
- [Gateway Routing](/architecture/cloud-design-patterns/gateways-and-edge/gateway-routing) — the weighted routing that splits traffic between versions.
- [Application Metrics](/architecture/microservices/observability/application-metrics) — the metrics that decide whether the canary moves forward.
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — shows how to build a canary with replicas in Kubernetes.

## Reference

- [Martin Fowler — CanaryRelease](https://martinfowler.com/bliki/CanaryRelease.html)
