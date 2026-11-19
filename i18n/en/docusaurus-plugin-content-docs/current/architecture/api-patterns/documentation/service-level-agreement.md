---
title: Service Level Agreement
pattern_slug: service-level-agreement
category: Documentation
tags:
  - Shared Understanding
  - Performance
source: https://api-patterns.org/
sidebar_label: "Service Level Agreement"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/documentation/service-level-agreement.mdx';

# Service Level Agreement

## Description

The Service Level Agreement (SLA) pattern defines, in measurable terms, the quality-of-service characteristics that an API provider guarantees and the consequences of failing to meet them.

An SLA gathers one or more service level objectives (SLOs). Each SLO tied to a quality attribute, such as latency or availability, carries a threshold value with its unit of measurement, a guarantee (the fraction of time or requests in which the threshold will be met), a penalty or compensation if it fails, and reporting procedures: who notices and reports the violation, the client or the provider. The SLA must say which operations it applies to and how measurement is performed and interpreted, for example over which time window the percentage is calculated and where the clock starts and stops.

SLOs derive from quality requirements gathered during analysis and design, and also from regulations, such as personal data protection rules. Typical categories are performance, security, data management and personal data protection. The main audience is the API product owner, and the drafting should involve legal, security and executive areas early. One variant is the internal SLA, where the provider measures its own performance without sharing it with external clients.

## Problems it solves

- Clients whose business depends on the API and cannot know what availability and latency to expect
- Informal and ambiguous terms that lead to misunderstandings and disputes
- The lack of a measurable criterion to compare equivalent providers
- Legal obligations, such as data location, without a documented guarantee

## When to use

- When API usage is critical to the client's business and the risk of unavailability is not tolerable
- When clients require, and pay for, formal guarantees (for example, partners who offer the service to third parties)
- When the provider wants to signal maturity and confidence to stand out
- As an internal SLA, to measure the team's own quality, even if it is not published

## When to avoid

- In free, experimental or low-impact APIs, where best effort is enough
- When the provider can neither measure nor meet what it would promise: a legally binding SLA without backing is pure risk
- When aspects that are hard to formalize, such as security, would force unrealistic promises; in those cases prefer a "commercially reasonable efforts" commitment

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Clear, measurable expectations for clients and provider | Takes effort to define, instrument, monitor and report |
| Trust and a competitive edge against offerings with no guarantees | Legal and financial accountability if the SLA is breached |
| An objective basis for handling incidents and compensation | Internal resistance to formal commitment and to the possibility of failing |
| Alignment between technical, legal and business areas | Lengthy negotiation, with many review rounds |

- **Risk limitation:** restricting the penalty to service credits limits the provider's financial exposure.
- **Measurement precision:** state where latency is measured and over which window the percentage is calculated, to avoid different readings.
- **Scope:** some SLOs apply to the whole service (data protection); others to specific operations (backup frequency).
- **Operational cost:** meeting an SLA requires on-call staff and mitigation mechanisms, which is expensive.

## Diagram

<Diagram />

The SLA aggregates measurable objectives, each with a threshold, unit, guarantee and compensation, plus the reporting rules.

## Example

The fintech offers partners an API for creating Pix charges and publishes the following SLA, with illustrative values. The latency SLO applies to the `POST /v2/pix-charges` operation:

```yaml
sla: pix-charges-api
operations: [POST /v2/pix-charges, GET /v2/pix-charges/{id}]
objectives:
  - name: latency
    unit: milliseconds
    threshold: 500
    guarantee: 99%            # of requests, over a 30-day window
    measured: from the request arriving at the endpoint to the response being sent
    penalty: 10% credit on the period's invoice
  - name: availability
    unit: percent-uptime
    threshold: 99.9
    window: 30 days
    penalty: 25% credit on the period's invoice
reporting:
  detection: provider publishes the status dashboard
  claim: client sends the credit request to support, with the dates and times of the incident
```

For the client, this translates into a verifiable sentence: in 99% of requests, over 30 days, the response goes out in under 500 ms, and if it does not, the next invoice gets a 10% discount.

## Related patterns

- [API Description](/architecture/api-patterns/documentation/api-description) — the SLA accompanies the technical contract and is referenced by it
- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — details of the usage limit can be included in the SLA
- [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan) — plan tiers usually come with different SLAs
- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) and [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee) — life-cycle guarantees the SLA can record
- [Health Endpoint Monitoring](/architecture/cloud-design-patterns/resiliency/health-endpoint-monitoring) — provides the availability measurement used to verify the SLO

## Reference

- [Patterns for API Design, chapter 9: Service Level Agreement](https://api-patterns.org/)
- [Site Reliability Engineering: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
