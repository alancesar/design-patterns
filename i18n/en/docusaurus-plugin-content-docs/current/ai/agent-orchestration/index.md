---
title: "AI Agent Orchestration Patterns"
sidebar_label: "Agent Orchestration"
---

# AI Agent Orchestration Patterns

Personal catalog based on the [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) guide from the Azure Architecture Center. It covers patterns for coordinating multiple AI agents, grouped by routing type (deterministic or dynamic). Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (orchestration goals), and a Mermaid diagram.

Total: 6 patterns in 2 groups. Tags: Orchestration goal.

## Groups

- [Deterministic Workflows](#deterministic-workflows) (2)
- [Dynamic Orchestration](#dynamic-orchestration) (4)

## Deterministic Workflows (2) {#deterministic-workflows}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Sequential Orchestration](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration) | Sequential Orchestration chains AI agents in a predefined linear order. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Concurrent Orchestration](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration) | Concurrent Orchestration runs several AI agents at the same time on the same task, so that each one brings an independent analysis from its own perspective or specialty. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) |

## Dynamic Orchestration (4) {#dynamic-orchestration}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Group Chat Orchestration](/ai/agent-orchestration/dynamic-orchestration/group-chat-orchestration) | Several AI agents solve a problem, make a decision, or validate work by taking part in a single shared conversation. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) |
| [Maker-Checker Loop](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop) | One agent, the **maker**, creates or proposes something, and another agent, the **checker**, evaluates the result against defined criteria. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) |
| [Handoff Orchestration](/ai/agent-orchestration/dynamic-orchestration/handoff-orchestration) | Dynamic delegation of tasks between specialized agents. | [`Specialization`](/tags/specialization) [`Adaptability`](/tags/adaptability) |
| [Magentic Orchestration](/ai/agent-orchestration/dynamic-orchestration/magentic-orchestration) | Designed for open-ended, complex problems with no predetermined plan of approach. | [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) |

## By tag

### Predictability (2)

[Sequential Orchestration](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration), [Maker-Checker Loop](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop)

### Parallelism (1)

[Concurrent Orchestration](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration)

### Specialization (3)

[Sequential Orchestration](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration), [Concurrent Orchestration](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration), [Handoff Orchestration](/ai/agent-orchestration/dynamic-orchestration/handoff-orchestration)

### Output Quality (3)

[Concurrent Orchestration](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration), [Group Chat Orchestration](/ai/agent-orchestration/dynamic-orchestration/group-chat-orchestration), [Maker-Checker Loop](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop)

### Adaptability (3)

[Group Chat Orchestration](/ai/agent-orchestration/dynamic-orchestration/group-chat-orchestration), [Handoff Orchestration](/ai/agent-orchestration/dynamic-orchestration/handoff-orchestration), [Magentic Orchestration](/ai/agent-orchestration/dynamic-orchestration/magentic-orchestration)

### Human Oversight (3)

[Group Chat Orchestration](/ai/agent-orchestration/dynamic-orchestration/group-chat-orchestration), [Maker-Checker Loop](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop), [Magentic Orchestration](/ai/agent-orchestration/dynamic-orchestration/magentic-orchestration)
