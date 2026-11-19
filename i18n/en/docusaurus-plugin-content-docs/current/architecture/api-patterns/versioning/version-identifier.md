---
title: Version Identifier
pattern_slug: version-identifier
category: Versioning
tags:
  - Evolvability
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Version Identifier"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/versioning/version-identifier.mdx';

# Version Identifier

## Description

The Version Identifier pattern introduces an explicit version indicator in the API and in the messages exchanged, so that provider and clients know which contract they are using and reject what they do not understand instead of misreading it.

The identifier is usually a number showing how far the API has evolved. It can live in the address (`/v2/...`), in a protocol header, in the negotiated media type (`Accept`) or in a field of the message body, that is, it acts as a [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element). It should also appear in the [API Description](/architecture/api-patterns/documentation/api-description). The practical rule is that it appears in a single place in each message exchange, to avoid inconsistencies between copies.

A receiver that gets a message with an unknown or incompatible version can abort interpretation and return a clear error, instead of carrying on with wrongly read data. Since the provider can also see which versions each client uses, it can plan the retirement of old versions. Note that the API version and the implementation version evolve at different paces, and that dependencies (such as the database schema) must keep up with the versioning.

## Problems it solves

- Clients breaking because of incompatible changes nobody noticed, such as a field whose semantics change without warning
- No way to identify exactly which contract a client expects and which one the provider offers
- Inability to know how many clients still depend on an old version before retiring it
- Hidden maintenance cost on clients, which must follow changes that add no business value

## When to use

- In APIs published in production, whose clients evolve on different cycles from the provider
- When incompatible changes are expected and must coexist with the previous version during migration
- When the provider needs to measure the use of each version to decide when to shut one down
- As the basis for other life-cycle patterns, such as [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production)

## When to avoid

- In a [Solution-Internal API](/architecture/api-patterns/foundations/solution-internal-api) maintained by the same team as the client, with automated tests and joint deployment, where an opportunistic approach is enough
- When the API only evolves compatibly and clients tolerate new fields, so an explicit version would carry no useful information
- When the provider cannot (or does not intend to) keep old versions and prefers [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence) with advance notice
- If the identifier is repeated in several places of the same message without need, creating conflicts

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Identifiable contract: clients and provider know what they refer to | One more element to specify, carry and validate in every message |
| Safe rejection of unknown versions, with no silent breakage | Clients may stay stuck on old versions and delay migration |
| Traceability of each version's use to plan retirement | Keeping several versions in production raises testing and operating cost |
| Basis for life-cycle and compatibility policies | Choosing where to put the identifier (URL, header, body) has pros and cons and divides opinions |

- **A single place:** put the version in one position of each message exchange, unless some client or intermediary requires more.
- **API version vs implementation version:** they are different things; the implementation can change more often without altering the contract.
- **Dependencies:** the database schema and other internal components must keep up with the versions in production; a facade that isolates the implementation from API versioning helps.
- **Structure:** combining the identifier with [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning) makes it possible to tell compatible changes from incompatible ones.

## Diagram

<Diagram />

The client declares the version it expects. The provider serves it if it knows the version and otherwise answers with an explicit error, instead of risking a wrong interpretation.

## Example

A fintech's Pix charge API has two versions in production. The client states the desired version in the media type, and the provider rejects versions it does not know. This message is common to all languages:

```http
GET /pix-charges/7c1f HTTP/1.1
Accept: application/vnd.fintech.pix-charge+json; version=2

HTTP/1.1 200 OK
Content-Type: application/vnd.fintech.pix-charge+json; version=2

{"id": "7c1f", "amountCents": 15000, "currency": "BRL", "status": "PENDING"}
```

In code, the provider validates the version before processing the request:

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.Set;

public class VersionGate {
    private static final Set<Integer> SUPPORTED = Set.of(1, 2);

    static String handle(int version) {
        if (!SUPPORTED.contains(version)) {
            return "406 unsupported version " + version;
        }
        return "200 PixCharge v" + version;
    }

    public static void main(String[] args) {
        System.out.println(handle(2)); // 200 PixCharge v2
        System.out.println(handle(3)); // 406 unsupported version 3
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
SUPPORTED = {1, 2}


def handle(version: int) -> str:
    if version not in SUPPORTED:
        return f"406 unsupported version {version}"
    return f"200 PixCharge v{version}"


print(handle(2))  # 200 PixCharge v2
print(handle(3))  # 406 unsupported version 3
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import "fmt"

var supported = map[int]bool{1: true, 2: true}

func handle(version int) string {
	if !supported[version] {
		return fmt.Sprintf("406 unsupported version %d", version)
	}
	return fmt.Sprintf("200 PixCharge v%d", version)
}

func main() {
	fmt.Println(handle(2)) // 200 PixCharge v2
	fmt.Println(handle(3)) // 406 unsupported version 3
}
```

</TabItem>
</Tabs>

## Related patterns

- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — the Version Identifier is a special kind of message metadata
- [Semantic Versioning](/architecture/api-patterns/versioning/semantic-versioning) — structures the identifier in three parts that indicate the impact of a change
- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) — requires explicit versioning to keep two versions at the same time
- [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence) — can use the identifier to flag what will be shut down
- [API Description](/architecture/api-patterns/documentation/api-description) — publishes the versions and the features of each one
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — the natural format to report an incompatible version
- [Format Indicator](/architecture/eip/message-construction/format-indicator) — the analogous indicator in messaging, for the format or version of a message

## Reference

- [Patterns for API Design, chapter 8: Version Identifier](https://api-patterns.org/)
