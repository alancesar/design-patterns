---
title: Blue-Green Deployment
pattern_slug: blue-green-deployment
category: Release
tags:
  - Reliability
  - Operational Excellence
source: https://martinfowler.com/bliki/BlueGreenDeployment.html
sidebar_label: "Blue-Green Deployment"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/blue-green-deployment.mdx';

# Blue-Green Deployment

## Description

Blue-Green Deployment keeps two identical production environments, called *blue* and *green*, and only one of them receives traffic at a time. The new version is deployed and tested in the idle environment and, when it is ready, the router moves all traffic to it at once. The previous environment stays up, running the old version, and serves as an immediate rollback.

The switch happens at a single point, such as a load balancer, a Kubernetes `Service` or a DNS record, so it is fast and reversible. Once the new version proves stable, the old environment becomes the idle one and receives the next release. Martin Fowler described the technique based on the work of Dan North and Jez Humble in *Continuous Delivery*.

## Problems it solves

- Downtime during deployment, when the service has to stop to switch versions.
- Slow and risky rollback, which requires redeploying the previous version in a hurry.
- No place to test the new version on real production infrastructure before exposing it to customers.

## When to use

- Services that require zero-downtime deployment and rollback in seconds.
- Releases that need a smoke test in production before receiving traffic.
- When the infrastructure can double its capacity during the switch.

## When to avoid

- When keeping two full environments is too expensive: prefer [Rolling Deployment](/architecture/microservices/release/rolling-deployment).
- When the change is risky for the business and must be exposed gradually: prefer [Canary Release](/architecture/microservices/release/canary-release).
- Schema changes the old version cannot handle, because rollback stops being safe.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Zero-downtime deployment | Double the capacity during the switch |
| Immediate rollback by switching routing back | The database is usually shared by both environments |
| New version tested in production before receiving traffic | All customers move to the new version at once |
| Simple switch, at a single point | Sessions and long-lived connections must be drained at the switch |

- **Shared database:** since blue and green use the same database, schema changes must be compatible with both versions. Split the migration into steps: first add columns and tables, then switch traffic, and only in the next release remove what became obsolete.
- **Full exposure:** a bug that only shows up under real traffic hits every customer at the same time; rollback is fast, but it does not prevent the impact.
- **Messaging:** queue consumers in the idle environment must also stay stopped, or both versions will compete for the same messages.

## Diagram

<Diagram />

`pix-service` v2 starts in the green environment, passes the smoke tests and receives traffic when the load balancer is repointed. If something goes wrong, routing goes back to blue.

## Related patterns

- [Canary Release](/architecture/microservices/release/canary-release) — exposes the new version to a share of the traffic instead of switching everything at once.
- [Rolling Deployment](/architecture/microservices/release/rolling-deployment) — an alternative that does not require doubling capacity.
- [Feature Toggle](/architecture/microservices/release/feature-toggle) — separates turning a feature on from switching versions.
- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — shows how to build Blue-Green with a `Deployment` and a `Service` in Kubernetes.
- [Health Check API](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring) — confirms the idle environment is healthy before the switch.
- [Service Deployment Platform](/architecture/microservices/deployment/service-deployment-platform) — a platform that automates the routing switch.

## Reference

- [Martin Fowler — BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
