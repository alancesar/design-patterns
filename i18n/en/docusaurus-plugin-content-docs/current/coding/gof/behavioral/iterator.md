---
title: Iterator
pattern_slug: iterator
category: Behavioral
tags:
  - Encapsulation
  - Simplicity
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Iterator"
mdx:
  format: mdx
---

# Iterator

## Description

Iterator provides a way to access the elements of a collection (aggregate) sequentially without exposing its internal representation. Instead of the client knowing whether the data lives in an array, a linked list, a tree, or a paginated source, it talks only to a uniform iteration interface, with operations such as `hasNext()` and `next()`.

The responsibility for traversing the collection moves out of the aggregate and into a separate iterator object, which holds the traversal state (current position, stack of visited nodes, page cursor, and so on). This way, the same collection can have several active iterators at once and offer different traversal strategies (in order, reverse, filtered, breadth-first, depth-first).

The aggregate acts as an iterator factory through a method such as `createIterator()`. Many languages build the pattern in natively (`Iterable`/`Iterator` in Java, `IEnumerable` in C#, the iteration protocol in Python and JavaScript, generators with `yield`).

## Problems it solves

- Client code gets coupled to the collection's internal structure (indexes, node pointers, cursors) and breaks when it changes.
- Different collections require different loops, which prevents generic algorithms that work over any structure.
- You need to support multiple ways of traversing the same collection without bloating its interface with traversal methods.
- Several simultaneous, independent traversals over the same collection need to keep their own state.
- Traversing large volumes of data (streams, paginated results) without loading everything into memory.

## When to use

- The collection has a complex structure (tree, graph, composition) and you want to hide that complexity from clients.
- You need a uniform interface to traverse heterogeneous collections (polymorphic iteration).
- You need multiple traversal strategies or lazy iteration over external sources.
- You want to reduce duplication of traversal code scattered across the application.

## When to avoid

- The collection is simple (a native array or list) and the language already offers adequate iteration; creating your own iterators only adds ceremony.
- Random access by index is the main use case, and sequential iteration is slower or less expressive.
- The collection is modified frequently during traversal and there's no clear policy for handling concurrent modifications.

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Encapsulates the collection's internal structure | More classes and interfaces to maintain |
| Allows multiple simultaneous, independent traversals | Iterators can become invalid if the collection changes during traversal |
| Supports several traversal strategies without changing the aggregate | Can be less efficient than direct access in specialized collections |
| Enables lazy iteration and iteration over infinite sources | Iteration state needs care in concurrent scenarios |
| Makes generic algorithms easier (Single Responsibility, Open/Closed) | Overkill for trivial collections |

- **Coupling:** the client depends only on the `Iterator` and `Aggregate` interfaces, not on the concrete classes.
- **Testability:** iterators can be tested in isolation and replaced by simple test doubles.
- **Robustness:** choose between *fail-fast* iterators (throw an error on concurrent modification) and snapshot-based ones.
- **Internal vs. external iterator:** external iterators give the client control; internal ones (e.g., `forEach` with a callback) are simpler but less flexible.

## Diagram

```mermaid
classDiagram
    class Iterator {
        <<interface>>
        +hasNext() bool
        +next() Object
    }
    class Aggregate {
        <<interface>>
        +createIterator() Iterator
    }
    class ConcreteIterator {
        -collection ConcreteAggregate
        -position int
        +hasNext() bool
        +next() Object
    }
    class ConcreteAggregate {
        -items List
        +createIterator() Iterator
    }
    class Client
    Iterator <|.. ConcreteIterator
    Aggregate <|.. ConcreteAggregate
    ConcreteAggregate ..> ConcreteIterator : creates
    ConcreteIterator --> ConcreteAggregate : traverses
    Client --> Aggregate
    Client --> Iterator
```

The `Client` obtains an `Iterator` from the `Aggregate` and walks the elements without knowing the internal structure. The `ConcreteAggregate` creates the `ConcreteIterator`, which keeps the current traversal position over the collection.

## Example

An account statement has thousands of entries and the API returns them in cursor-based pages. The consumer only calls `hasNext()` and `next()`: the `PagedStatementIterator` fetches the next page when the current one runs out, and the `ReverseStatementIterator` walks the same collection from the most recent entry to the oldest.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
record StatementEntry(String date, String description, long amountCents) {}

record Page(List<StatementEntry> entries, Integer nextCursor) {}

class Statement implements Iterable<StatementEntry> {
    private final List<StatementEntry> entries;
    private final int pageSize;

    Statement(List<StatementEntry> entries, int pageSize) { this.entries = entries; this.pageSize = pageSize; }

    // simulates the paginated API: returns one page and the cursor of the next
    Page fetchPage(int cursor) {
        int end = Math.min(cursor + pageSize, entries.size());
        return new Page(entries.subList(cursor, end), end < entries.size() ? end : null);
    }

    public Iterator<StatementEntry> iterator() { return new PagedStatementIterator(this); }

    Iterator<StatementEntry> reverseIterator() {
        return new ReverseStatementIterator(entries); // simplification: reads the entries already loaded
    }
}

class PagedStatementIterator implements Iterator<StatementEntry> {
    private final Statement statement;
    private List<StatementEntry> buffer = List.of();
    private int position = 0;
    private Integer cursor = 0;

    PagedStatementIterator(Statement statement) { this.statement = statement; }

    public boolean hasNext() { fill(); return position < buffer.size(); }
    public StatementEntry next() { fill(); return buffer.get(position++); }

    private void fill() {
        if (position < buffer.size() || cursor == null) return;
        Page page = statement.fetchPage(cursor); // only fetches when the current page is exhausted
        buffer = page.entries();
        position = 0;
        cursor = page.nextCursor();
    }
}

class ReverseStatementIterator implements Iterator<StatementEntry> {
    private final List<StatementEntry> entries;
    private int position;

    ReverseStatementIterator(List<StatementEntry> entries) { this.entries = entries; position = entries.size() - 1; }

    public boolean hasNext() { return position >= 0; }
    public StatementEntry next() { return entries.get(position--); }
}

Statement statement = new Statement(List.of(
    new StatementEntry("2026-03-01", "Pix received", 25_000),
    new StatementEntry("2026-03-02", "Boleto paid", -8_990),
    new StatementEntry("2026-03-03", "Card purchase", -4_550)), 2);

for (StatementEntry entry : statement) System.out.println(entry.description()); // Pix received, Boleto paid, Card purchase

Iterator<StatementEntry> recent = statement.reverseIterator();
System.out.println(recent.next().description());                                // Card purchase
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import Iterator, Optional

@dataclass(frozen=True)
class StatementEntry:
    date: str
    description: str
    amount_cents: int

@dataclass(frozen=True)
class Page:
    entries: list[StatementEntry]
    next_cursor: Optional[int]

class Statement:
    def __init__(self, entries: list[StatementEntry], page_size: int = 2) -> None:
        self._entries = entries
        self._page_size = page_size

    def fetch_page(self, cursor: int = 0) -> Page:
        """Simulates the paginated API: returns one page and the cursor of the next."""
        end = cursor + self._page_size
        return Page(self._entries[cursor:end], end if end < len(self._entries) else None)

    def __iter__(self) -> Iterator[StatementEntry]:
        return PagedStatementIterator(self)

    def __reversed__(self) -> Iterator[StatementEntry]:
        return ReverseStatementIterator(self._entries)  # simplification: reads the entries already loaded

class PagedStatementIterator:
    def __init__(self, statement: Statement) -> None:
        self._statement = statement
        self._buffer: list[StatementEntry] = []
        self._position = 0
        self._cursor: Optional[int] = 0

    def __iter__(self) -> Iterator[StatementEntry]:
        return self

    def __next__(self) -> StatementEntry:
        if self._position >= len(self._buffer):
            if self._cursor is None:
                raise StopIteration
            page = self._statement.fetch_page(self._cursor)  # only fetches when the current page is exhausted
            self._buffer, self._position, self._cursor = page.entries, 0, page.next_cursor
        entry = self._buffer[self._position]
        self._position += 1
        return entry

class ReverseStatementIterator:
    def __init__(self, entries: list[StatementEntry]) -> None:
        self._entries = entries
        self._position = len(entries) - 1

    def __iter__(self) -> Iterator[StatementEntry]:
        return self

    def __next__(self) -> StatementEntry:
        if self._position < 0:
            raise StopIteration
        entry = self._entries[self._position]
        self._position -= 1
        return entry

statement = Statement([
    StatementEntry("2026-03-01", "Pix received", 25_000),
    StatementEntry("2026-03-02", "Boleto paid", -8_990),
    StatementEntry("2026-03-03", "Card purchase", -4_550),
])

for entry in statement:
    print(entry.description)  # Pix received, Boleto paid, Card purchase

recent = reversed(statement)
print(next(recent).description)  # Card purchase
```

</TabItem>
<TabItem value="go" label="Go">

```go
type StatementEntry struct {
	Date        string
	Description string
	AmountCents int64
}

type Page struct {
	Entries    []StatementEntry
	NextCursor int // -1 when there is no next page
}

type Statement struct {
	entries  []StatementEntry
	pageSize int
}

// simulates the paginated API: returns one page and the cursor of the next
func (s *Statement) FetchPage(cursor int) Page {
	end := min(cursor+s.pageSize, len(s.entries))
	next := -1
	if end < len(s.entries) {
		next = end
	}
	return Page{s.entries[cursor:end], next}
}

// In Go, the iterator is an iter.Seq function, consumed with for range.
func (s *Statement) All() iter.Seq[StatementEntry] {
	return func(yield func(StatementEntry) bool) {
		for cursor := 0; cursor >= 0; {
			page := s.FetchPage(cursor) // only fetches when the current page is exhausted
			for _, entry := range page.Entries {
				if !yield(entry) {
					return
				}
			}
			cursor = page.NextCursor
		}
	}
}

func (s *Statement) Backward() iter.Seq[StatementEntry] {
	return func(yield func(StatementEntry) bool) {
		// simplification: reads the entries already loaded
		for i := len(s.entries) - 1; i >= 0; i-- {
			if !yield(s.entries[i]) {
				return
			}
		}
	}
}

func main() {
	statement := &Statement{pageSize: 2, entries: []StatementEntry{
		{"2026-03-01", "Pix received", 25_000},
		{"2026-03-02", "Boleto paid", -8_990},
		{"2026-03-03", "Card purchase", -4_550},
	}}

	for entry := range statement.All() {
		fmt.Println(entry.Description) // Pix received, Boleto paid, Card purchase
	}

	for entry := range statement.Backward() {
		fmt.Println(entry.Description) // Card purchase
		break
	}
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface StatementEntry {
  date: string;
  description: string;
  amountCents: number;
}

interface Page {
  entries: StatementEntry[];
  nextCursor?: number;
}

interface StatementIterator {
  hasNext(): boolean;
  next(): StatementEntry;
}

class Statement {
  constructor(private entries: StatementEntry[], private pageSize = 2) {}

  // simulates the paginated API: returns one page and the cursor of the next
  fetchPage(cursor = 0): Page {
    const end = cursor + this.pageSize;
    return {
      entries: this.entries.slice(cursor, end),
      nextCursor: end < this.entries.length ? end : undefined,
    };
  }

  createIterator(): StatementIterator {
    return new PagedStatementIterator(this);
  }

  createReverseIterator(): StatementIterator {
    return new ReverseStatementIterator(this.entries); // simplification: reads the entries already loaded
  }
}

class PagedStatementIterator implements StatementIterator {
  private buffer: StatementEntry[] = [];
  private position = 0;
  private cursor: number | undefined = 0;
  constructor(private statement: Statement) {}

  hasNext(): boolean { this.fill(); return this.position < this.buffer.length; }
  next(): StatementEntry { this.fill(); return this.buffer[this.position++]; }

  private fill(): void {
    if (this.position < this.buffer.length || this.cursor === undefined) return;
    const page = this.statement.fetchPage(this.cursor); // only fetches when the current page is exhausted
    this.buffer = page.entries;
    this.position = 0;
    this.cursor = page.nextCursor;
  }
}

class ReverseStatementIterator implements StatementIterator {
  private position: number;
  constructor(private entries: StatementEntry[]) {
    this.position = entries.length - 1;
  }

  hasNext(): boolean { return this.position >= 0; }
  next(): StatementEntry { return this.entries[this.position--]; }
}

const statement = new Statement([
  { date: "2026-03-01", description: "Pix received", amountCents: 25_000 },
  { date: "2026-03-02", description: "Boleto paid", amountCents: -8_990 },
  { date: "2026-03-03", description: "Card purchase", amountCents: -4_550 },
]);

const it = statement.createIterator();
while (it.hasNext()) console.log(it.next().description);  // Pix received, Boleto paid, Card purchase

const recent = statement.createReverseIterator();
console.log(recent.next().description);                   // Card purchase
```

</TabItem>
</Tabs>

## Related patterns

- [Composite](/coding/gof/structural/composite) — iterators are often used to traverse recursive Composite structures.
- [Factory Method](/coding/gof/creational/factory-method) — `createIterator()` is a Factory Method that lets each collection instantiate the appropriate iterator.
- [Memento](/coding/gof/behavioral/memento) — can capture the state of an iteration to resume or undo it later.
- [Visitor](/coding/gof/behavioral/visitor) — combines with Iterator: the iterator traverses the collection and the Visitor applies the operation to each element.
- [Null Object](/coding/gof/behavioral/null-object) — an empty iterator (Null Iterator) avoids null checks on collections with no elements.

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Iterator on Refactoring.Guru](https://refactoring.guru/design-patterns/iterator)
