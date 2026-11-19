---
title: Link Element
pattern_slug: link-element
category: Element Stereotypes
tags:
  - Decoupling
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Link Element"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/element-stereotypes/link-element.mdx';

# Link Element

## Description

The Link Element pattern includes in request and response messages a human- and machine-readable, network-accessible pointer to other endpoints and operations, so the client can call them remotely. It is an Id Element that, besides naming the target, says where it can be called.

In HTTP, the Link Element is a URI, and the set of links lets the provider guide the client through the possible next steps (HATEOAS). Links can be [Atomic Parameters](/architecture/api-patterns/basic-structure/atomic-parameter), list entries or tree leaves. It helps to add [Metadata Elements](/architecture/api-patterns/element-stereotypes/metadata-element) that describe the relation: the role name of the link (`self`, `next`, `cancel`), the HTTP method accepted, the expected media type, and whether following the link is safe, reversible or compensable.

The client must handle broken links and network failures, and the provider must care about stability, security and authorization of the target, since the link only reveals what the caller can do.

The most common semantic link types are: **next** (next step of a process), **undo** (undo or compensate), **more** (more results, a horizontal move) and **details** (more information about the link source, a vertical move). Some types are registered and standardized, such as those from IANA, and the structure follows RFC 8288. In REST there is no distinction between an Id Element and a Link Element, which eases addressing but makes URLs hard to change.

## Problems it solves

- Clients that build URLs from identifiers and routing rules copied from the documentation
- Difficulty changing the address structure without breaking those who know it
- No indication, in the response, of which actions are available in the current state
- The need to point to other endpoints, including on other hosts, without coupling the client to them

## When to use

- In REST level 3 APIs that use hypermedia to guide the client
- For navigation in collections and pagination (`next`, `prev`)
- When a resource exposes the next steps of a process, such as pay or cancel
- When related resources live in other services or hosts

## When to avoid

- When a simple [Id Element](/architecture/api-patterns/element-stereotypes/id-element) is enough and clients already know the base address
- In APIs whose clients do not support or use hypermedia, where links only increase the payload
- When the transport layer has no accessible addresses, as in internal messaging
- When the provider cannot keep links stable, valid and protected by authorization

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Addresses and actions can change without altering the client | Larger messages and more elaborate clients to interpret links |
| The provider drives the flow and announces only the actions valid in the current state | Requires a shared convention (relations, methods, media types) for link semantics |
| References resources in other services globally | Links can break through network failures, target changes or expiry |
| Replaces manual URL construction | Absolute URLs expose hosts and internal structure if badly designed |

- **Stability:** provider-supplied links reduce coupling, but relation names become part of the contract.
- **Security:** do not include links to actions the user cannot perform, and validate authorization at the target.
- **Semantics:** document the effect of following each link, whether it is safe, whether it can be undone and which method to use.
- **Failures:** the client must handle unavailable, expired or broken links.
- **URI scheme:** the pattern solves global, timeless identification at the cost of a more complex client programming model; once published, changing the URI scheme is risky and costly.
- **Threats:** invalid URIs must not crash the server or open doors for attackers, so they belong in the security design and tests.

## Diagram

<Diagram />

The boleto response carries links with the valid actions, and the client picks one instead of building the URL itself.

## Example

When fetching a boleto, the fintech's API returns links to the actions possible in the current state. Since the boleto is pending, the response announces payment and cancellation, not reversal.

```http
GET /boletos/bol_5521 HTTP/1.1
Accept: application/json
```

```json
{
  "id": "bol_5521",
  "amountCents": 89990,
  "currency": "BRL",
  "dueDate": "2026-11-30",
  "status": "PENDING",
  "links": [
    { "rel": "self",   "href": "/boletos/bol_5521", "method": "GET" },
    { "rel": "pay",    "href": "/boletos/bol_5521/payment", "method": "POST" },
    { "rel": "cancel", "href": "/boletos/bol_5521/cancellation", "method": "POST" },
    { "rel": "account", "href": "/accounts/acc_7f3a91", "method": "GET" }
  ]
}
```

Once the boleto is paid, the `pay` and `cancel` links stop appearing, and the client adapts without any change.

## Related patterns

- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — identifies the target but does not say where to call it; the Link Element adds the address
- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — describes the relation and the method of each link
- [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — uses Link Elements to point to related data
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — endpoint that returns links to other resources
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — depends on links such as `next` and `prev` to navigate
- [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) — exposes the next steps of a process through links
- [Return Address](/architecture/eip/message-construction/return-address) — in messaging, tells the receiver where to send the reply

## Reference

- [Patterns for API Design, chapter 6: Link Element](https://api-patterns.org/)
- [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288)
