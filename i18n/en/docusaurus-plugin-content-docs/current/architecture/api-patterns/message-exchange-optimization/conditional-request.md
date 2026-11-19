---
title: Conditional Request
pattern_slug: conditional-request
category: Message Exchange Optimization
tags:
  - Performance
source: https://api-patterns.org/
sidebar_label: "Conditional Request"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/message-exchange-optimization/conditional-request.mdx';

# Conditional Request

## Description

The Conditional Request pattern makes a request conditional by adding metadata that describes the version of the data the client already holds, so the provider returns the full representation only if it has changed.

The client keeps the previous response together with a version marker and sends it back on the next call. If the condition is not met, that is, nothing has changed, the provider answers with a special status code and no body, and the client reuses the copy it has. There are two variants: the **time-based** one, where the marker is the last-modified date, and the **fingerprint-based** one, where the provider tags the resource with a hash or a version number. In HTTP this maps to `Last-Modified` with `If-Modified-Since`, or to `ETag` with `If-None-Match`, and the empty answer is `304 Not Modified`.

The number of messages does not go down; what shrinks is the size of repeated responses. Because the client is the one remembering the version it saw, the provider does not need to keep per-client state.

## Problems it solves

- Clients that repeatedly query rarely changing data and re-download the same large response
- Server-side processing and bandwidth spent resending what the client already has
- Client work to reprocess a result identical to the previous one
- The need for a "preflight" query (ask whether it changed, then fetch), which doubles the number of requests

## When to use

- When responses are large or the network is limited, and the data changes less often than it is read
- When clients already keep a local copy and must decide when to refresh it
- When the provider can cheaply compute a version marker (version number, hash or modification date)
- For statements, product catalogs, rate tables and registration data queried frequently

## When to avoid

- When responses are already small and cheap to produce: the decision logic may cost more than it saves
- When the data changes on every request, so the condition almost never lets the copy be reused
- When the client cannot or should not keep a local cache
- When the version marker does not cover the metadata: if only the metadata changes, a condition based only on the data will hide the change

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Less bandwidth and fewer bytes processed on repeated responses | The number of messages stays the same |
| The provider keeps no state about which client saw which version | The client must store the copy and the version marker |
| Rereading locally is much faster than a new full call | Extra logic in the endpoint to evaluate conditions and errors |
| Often transparent to the implementation, if done in a filter | As a filter, the response is still computed and then discarded: it saves bandwidth, not processing |

- **Condition type:** the modification date is simple but needs reasonably synchronized clocks; the fingerprint is more precise and clock-independent.
- **Processing:** to also save computation, the check must happen before the response is built, for example with a server-side cache.
- **Limits and billing:** define whether a conditional response counts against the [Rate Limit](/architecture/api-patterns/documentation/rate-limit) and whether it gets special treatment in the [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan).
- **Pagination:** a page may be unchanged while the total number of pages grew; that metadata change must also enter the condition.

## Diagram

<Diagram />

The first reply carries the body and the `ETag`. While the data does not change, the condition holds and the provider returns only the `304`; when a new entry alters the state, the `ETag` changes and the full response comes back.

## Example

A fintech app queries the summary of an account statement. Since the balance only changes when a `LedgerEntry` arrives, the provider tags the response with an `ETag` and answers `304` when the client already has the current version. The HTTP messages:

```http
GET /accounts/acc-1/statement HTTP/1.1

HTTP/1.1 200 OK
ETag: "ledger-2"
Content-Type: application/json

{"accountId": "acc-1", "balanceCents": 15000, "currency": "BRL"}
```

```http
GET /accounts/acc-1/statement HTTP/1.1
If-None-Match: "ledger-2"

HTTP/1.1 304 Not Modified
ETag: "ledger-2"
```

In code, the service derives the `ETag` from the number of entries, and the client keeps the latest copy. The balance is always in cents, never a float.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;

public class Main {
    record LedgerEntry(String id, long amountCents) {}
    record Response(int status, String etag, Long balanceCents) {}

    static class StatementService {
        private final List<LedgerEntry> entries = new ArrayList<>();

        void post(LedgerEntry entry) { entries.add(entry); }

        // The ETag derives from the number of ledger entries: it changes with every new entry.
        Response get(String ifNoneMatch) {
            String etag = "\"ledger-" + entries.size() + "\"";
            if (etag.equals(ifNoneMatch)) {
                return new Response(304, etag, null);
            }
            long balance = entries.stream().mapToLong(LedgerEntry::amountCents).sum();
            return new Response(200, etag, balance);
        }
    }

    public static void main(String[] args) {
        StatementService service = new StatementService();
        service.post(new LedgerEntry("e1", 10000));
        service.post(new LedgerEntry("e2", 5000));

        String cachedEtag = null;
        long cachedBalance = 0;
        for (int i = 0; i < 3; i++) {
            if (i == 2) service.post(new LedgerEntry("e3", 2500));
            Response r = service.get(cachedEtag);
            if (r.status() == 200) {
                cachedEtag = r.etag();
                cachedBalance = r.balanceCents();
            }
            System.out.println(r.status() + " " + r.etag() + " balance=" + cachedBalance);
        }
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LedgerEntry:
    id: str
    amount_cents: int


@dataclass
class Response:
    status: int
    etag: str
    balance_cents: Optional[int] = None


class StatementService:
    def __init__(self) -> None:
        self.entries: List[LedgerEntry] = []

    def post(self, entry: LedgerEntry) -> None:
        self.entries.append(entry)

    # The ETag derives from the number of ledger entries: it changes with every new entry.
    def get(self, if_none_match: Optional[str]) -> Response:
        etag = '"ledger-%d"' % len(self.entries)
        if etag == if_none_match:
            return Response(304, etag)
        return Response(200, etag, sum(e.amount_cents for e in self.entries))


service = StatementService()
service.post(LedgerEntry("e1", 10000))
service.post(LedgerEntry("e2", 5000))

cached_etag, cached_balance = None, 0
for i in range(3):
    if i == 2:
        service.post(LedgerEntry("e3", 2500))
    r = service.get(cached_etag)
    if r.status == 200:
        cached_etag, cached_balance = r.etag, r.balance_cents
    print(f"{r.status} {r.etag} balance={cached_balance}")
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import "fmt"

type LedgerEntry struct {
	ID          string
	AmountCents int64
}

type Response struct {
	Status       int
	ETag         string
	BalanceCents int64
}

type StatementService struct {
	entries []LedgerEntry
}

func (s *StatementService) Post(e LedgerEntry) { s.entries = append(s.entries, e) }

// The ETag derives from the number of ledger entries: it changes with every new entry.
func (s *StatementService) Get(ifNoneMatch string) Response {
	etag := fmt.Sprintf("\"ledger-%d\"", len(s.entries))
	if etag == ifNoneMatch {
		return Response{Status: 304, ETag: etag}
	}
	var balance int64
	for _, e := range s.entries {
		balance += e.AmountCents
	}
	return Response{Status: 200, ETag: etag, BalanceCents: balance}
}

func main() {
	service := &StatementService{}
	service.Post(LedgerEntry{"e1", 10000})
	service.Post(LedgerEntry{"e2", 5000})

	cachedETag := ""
	var cachedBalance int64
	for i := 0; i < 3; i++ {
		if i == 2 {
			service.Post(LedgerEntry{"e3", 2500})
		}
		r := service.Get(cachedETag)
		if r.Status == 200 {
			cachedETag, cachedBalance = r.ETag, r.BalanceCents
		}
		fmt.Printf("%d %s balance=%d\n", r.Status, r.ETag, cachedBalance)
	}
}
```

</TabItem>
</Tabs>

The second cycle ends in `304` and the client keeps the cached balance; the third, after a new entry, receives an updated `ETag` and balance.

## Related patterns

- [Wish List](/architecture/api-patterns/response-shaping/wish-list) and [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — combine well: they indicate which data to send when the condition holds and the response must be resent
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — can be combined, with care for changes in the total number of pages
- [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle) — a bundle of requests can also be delivered conditionally
- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — carries the condition (date or fingerprint) in the message
- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — conditional responses reduce the transferred data volume, which helps when the limit counts bytes
- [Cache-Aside](/architecture/cloud-design-patterns/data-management/cache-aside) — the cache sits on the data consumer's side and the client decides when to refresh; here the condition is part of the API's own contract, and the cache is just the copy the client reuses

## Reference

- [Patterns for API Design, chapter 7: Conditional Request](https://api-patterns.org/)
- [RFC 7232: Conditional Requests (HTTP/1.1)](https://datatracker.ietf.org/doc/html/rfc7232)
