---
title: Command
pattern_slug: command
category: Behavioral
tags:
  - Decoupling
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Command"
---

# Command

## Description

Command encapsulates a request as an object, containing everything needed to execute it: the action, the object that performs it (the receiver), and the parameters. This makes it possible to parameterize clients with different requests, queue them, log them, and support operations that can be undone.

The pattern separates whoever triggers the operation (the Invoker, such as a button or a scheduler) from whoever knows how to perform it (the Receiver). The Invoker only knows the `Command` interface with the `execute()` method; each concrete command delegates the work to the appropriate receiver. Optionally, the command stores the state needed to implement `undo()`.

Because commands are first-class objects, they can be stored in a history, composed into macros, serialized for later execution or execution in another process, and re-executed (for example, for recovery after failures).

## Problems it solves

- Direct coupling between the interface element (button, menu, shortcut) and the business logic it triggers
- The need to undo/redo operations while keeping a history of actions
- Queuing, scheduling, or running operations asynchronously or remotely
- Logging operations for auditing or to replay them after a failure
- Grouping several operations into a single composite action (macro or transaction)

## When to use

- When you need to parameterize objects with actions to perform (object-oriented callbacks)
- When requests must be specified, queued, and executed at different times
- When the system needs to support undo/redo
- When operations must be logged and replayable (journaling, simplified event sourcing)
- When different triggers (button, shortcut, menu, API) must fire the same operation

## When to avoid

- When the operation is simple, synchronous, and called from a single place: a direct method call or a function/lambda is enough
- When there's no need for history, queue, log, or decoupling between sender and receiver
- When the number of command classes would grow a lot without real reuse benefit

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| Decouples the invoker from the executor | Increases the number of classes (one per operation) |
| Enables undo/redo, queues, logs, and macros | Implementing `undo()` correctly requires storing state and can be complex |
| New commands are added without changing existing code (Open/Closed) | Extra indirection makes the execution flow harder to follow |
| Commands can be serialized and executed later or remotely | Serialized commands require versioning and care with missing receivers |

- **Coupling:** the Invoker depends only on the `Command` abstraction; coupling to the Receiver is concentrated in the concrete commands.
- **Testability:** commands are small, isolated units, easy to test with fake receivers.
- **Performance:** keeping unlimited undo history consumes memory; it's common to cap the size or use Memento for snapshots.
- **Modern languages:** in languages with first-class functions, closures can replace simple commands, but they lose undo and metadata.

## Diagram

```mermaid
classDiagram
    class Command {
        <<interface>>
        +execute()
        +undo()
    }
    class ConcreteCommand {
        -receiver: Receiver
        -state
        +execute()
        +undo()
    }
    class Receiver {
        +action()
    }
    class Invoker {
        -history: List~Command~
        +setCommand(command: Command)
        +executeCommand()
    }
    class Client
    Command <|.. ConcreteCommand
    ConcreteCommand --> Receiver
    Invoker o-- Command
    Client ..> ConcreteCommand : creates
    Client ..> Receiver : configures
```

The `Client` creates the `ConcreteCommand` and associates it with a `Receiver`; the `Invoker` stores commands and calls `execute()` without knowing the receiver. The `ConcreteCommand` translates the call into one or more actions on the `Receiver` and can store state for `undo()`.

## Example

Each movement in an account's ledger is a command with `execute()` and `undo()`, and the history lets you reverse the last operation. In accounting a reversal is a new entry: `undo()` posts the inverse entry and the original stays in the ledger.

```typescript
type EntryType = "DEBIT" | "CREDIT";

interface LedgerEntry {
  type: EntryType;
  amountCents: number;
  reversalOf?: number; // reverses the entry at the given index
}

class Account {                          // Receiver
  readonly entries: LedgerEntry[] = [];

  post(type: EntryType, amountCents: number, reversalOf?: number): number {
    this.entries.push({ type, amountCents, reversalOf });
    return this.entries.length - 1;      // the entry index serves as its identifier
  }

  get balanceCents(): number {
    return this.entries.reduce(
      (sum, e) => sum + (e.type === "CREDIT" ? e.amountCents : -e.amountCents), 0);
  }
}

interface LedgerCommand { execute(): void; undo(): void; }

class CreditCommand implements LedgerCommand {
  private entryId?: number;
  constructor(private account: Account, private amountCents: number) {}
  execute() { this.entryId = this.account.post("CREDIT", this.amountCents); }
  undo() { this.account.post("DEBIT", this.amountCents, this.entryId); }
}

class DebitCommand implements LedgerCommand {
  private entryId?: number;
  constructor(private account: Account, private amountCents: number) {}
  execute() { this.entryId = this.account.post("DEBIT", this.amountCents); }
  undo() { this.account.post("CREDIT", this.amountCents, this.entryId); }
}

class LedgerHistory {                    // Invoker
  private history: LedgerCommand[] = [];
  run(cmd: LedgerCommand) { cmd.execute(); this.history.push(cmd); }
  undo() { this.history.pop()?.undo(); }
}

const account = new Account();
const history = new LedgerHistory();
history.run(new CreditCommand(account, 100_000));
history.run(new DebitCommand(account, 30_000));
console.log(account.balanceCents);       // 70000
history.undo();                          // posts a reversal credit; the original debit stays in the ledger
console.log(account.balanceCents);       // 100000
console.log(account.entries.length);     // 3
```

## Related patterns

- [Memento](/coding/gof/behavioral/memento) — can store the receiver's state before execution to make `undo()` possible
- [Composite](/coding/gof/structural/composite) — allows building macros, commands made up of other commands
- [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility) — also decouples sender and receiver; handlers can be represented as commands
- [Strategy](/coding/gof/behavioral/strategy) — similar structure, but Strategy varies *how* something is done, while Command represents *what* to do as an object
- [Prototype](/coding/gof/creational/prototype) — useful for copying commands before putting them in the history
- [Observer](/coding/gof/behavioral/observer) — commands can notify observers or be triggered by events

## Reference

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Command on Refactoring.Guru](https://refactoring.guru/design-patterns/command)
