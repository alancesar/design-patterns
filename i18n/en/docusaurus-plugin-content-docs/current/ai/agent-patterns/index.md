---
title: "AI Agent Design Patterns"
sidebar_label: "Agent Patterns"
---

# AI Agent Design Patterns

Personal catalog that brings together two sources: the [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) guide from the Azure Architecture Center and the [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) guide from the Google Cloud Architecture Center. It covers agentic system patterns, from a single agent to multi-agent systems, grouped by workflow type: deterministic, with dynamic orchestration, with iteration, or with special requirements. Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (orchestration goals), and a Mermaid diagram.

The Origin column shows which source each pattern comes from, and the Reference section of each page links to the original source. Three patterns appear in both sources under different names: Sequential Orchestration (*Multi-Agent Sequential* at Google), Concurrent Orchestration (*Multi-Agent Parallel*), and Maker-Checker Loop (*Multi-Agent Review and Critique*).

Total: 15 patterns in 4 groups. Tags: Orchestration goal.

## Groups

- [Deterministic Workflows](#deterministic-workflows) (2)
- [Dynamic Orchestration](#dynamic-orchestration) (7)
- [Iteration](#iteration) (4)
- [Special Requirements](#special-requirements) (2)

## Deterministic Workflows (2) {#deterministic-workflows}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [Sequential Orchestration](/ai/agent-patterns/deterministic-workflows/sequential-orchestration) | Sequential Orchestration chains AI agents in a predefined linear order. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) | Azure, Google |
| [Concurrent Orchestration](/ai/agent-patterns/deterministic-workflows/concurrent-orchestration) | Concurrent Orchestration runs several AI agents at the same time on the same task, so that each one brings an independent analysis from its own perspective or specialty. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) | Azure, Google |

## Dynamic Orchestration (7) {#dynamic-orchestration}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [Single Agent](/ai/agent-patterns/dynamic-orchestration/single-agent) | A single model, a defined set of tools, and a detailed system prompt handle the user's request autonomously. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) | Google |
| [Multi-Agent Coordinator](/ai/agent-patterns/dynamic-orchestration/multi-agent-coordinator) | A central coordinator agent analyzes the user's request, splits it into subtasks, and dispatches each one to a specialized agent (for example, one that queries a database or calls an API). | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) | Google |
| [Multi-Agent Hierarchical Task Decomposition](/ai/agent-patterns/dynamic-orchestration/multi-agent-hierarchical-task-decomposition) | Agents are organized in a multi-level hierarchy. | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) | Google |
| [Multi-Agent Swarm](/ai/agent-patterns/dynamic-orchestration/multi-agent-swarm) | Specialized agents communicate with one another in every direction (all-to-all) and iteratively refine a solution to a complex problem. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) | Google |
| [Group Chat Orchestration](/ai/agent-patterns/dynamic-orchestration/group-chat-orchestration) | Several AI agents solve a problem, make a decision, or validate work by taking part in a single shared conversation. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) | Azure |
| [Handoff Orchestration](/ai/agent-patterns/dynamic-orchestration/handoff-orchestration) | Dynamic delegation of tasks between specialized agents. | [`Specialization`](/tags/specialization) [`Adaptability`](/tags/adaptability) | Azure |
| [Magentic Orchestration](/ai/agent-patterns/dynamic-orchestration/magentic-orchestration) | Designed for open-ended, complex problems with no predetermined plan of approach. | [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) | Azure |

## Iteration (4) {#iteration}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [ReAct](/ai/agent-patterns/iteration/react) | A single model-driven agent repeats a three-step cycle: it reasons about the task (*thought*), chooses between calling a tool or giving the final answer (*action*), and records the tool's result in the context (*observation*). | [`Adaptability`](/tags/adaptability) | Google |
| [Multi-Agent Loop](/ai/agent-patterns/iteration/multi-agent-loop) | A loop agent runs a sequence of subagents and then checks an exit condition. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) | Google |
| [Maker-Checker Loop](/ai/agent-patterns/iteration/maker-checker-loop) | One agent, the **maker**, creates or proposes something, and another agent, the **checker**, evaluates the result against defined criteria. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) | Azure, Google |
| [Multi-Agent Iterative Refinement](/ai/agent-patterns/iteration/multi-agent-iterative-refinement) | One or more agents work in a loop, changing a result stored in the session state on each pass. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) | Google |

## Special Requirements (2) {#special-requirements}

| Pattern | Summary | Tags | Origin |
| --- | --- | --- | --- |
| [Human-in-the-Loop](/ai/agent-patterns/special-requirements/human-in-the-loop) | The agent runs the flow up to a predefined checkpoint, where it pauses and calls an external system so a person can review the work. | [`Human Oversight`](/tags/human-oversight) [`Output Quality`](/tags/output-quality) | Google |
| [Custom Logic](/ai/agent-patterns/special-requirements/custom-logic) | The orchestration is written in code, with conditionals, loops, and branches, instead of using a predefined pattern. | [`Adaptability`](/tags/adaptability) [`Predictability`](/tags/predictability) | Google |

## By tag

### Predictability (6)

[Sequential Orchestration](/ai/agent-patterns/deterministic-workflows/sequential-orchestration), [Single Agent](/ai/agent-patterns/dynamic-orchestration/single-agent), [Multi-Agent Loop](/ai/agent-patterns/iteration/multi-agent-loop), [Maker-Checker Loop](/ai/agent-patterns/iteration/maker-checker-loop), [Multi-Agent Iterative Refinement](/ai/agent-patterns/iteration/multi-agent-iterative-refinement), [Custom Logic](/ai/agent-patterns/special-requirements/custom-logic)

### Specialization (6)

[Sequential Orchestration](/ai/agent-patterns/deterministic-workflows/sequential-orchestration), [Concurrent Orchestration](/ai/agent-patterns/deterministic-workflows/concurrent-orchestration), [Single Agent](/ai/agent-patterns/dynamic-orchestration/single-agent), [Multi-Agent Coordinator](/ai/agent-patterns/dynamic-orchestration/multi-agent-coordinator), [Multi-Agent Hierarchical Task Decomposition](/ai/agent-patterns/dynamic-orchestration/multi-agent-hierarchical-task-decomposition), [Handoff Orchestration](/ai/agent-patterns/dynamic-orchestration/handoff-orchestration)

### Parallelism (1)

[Concurrent Orchestration](/ai/agent-patterns/deterministic-workflows/concurrent-orchestration)

### Output Quality (7)

[Concurrent Orchestration](/ai/agent-patterns/deterministic-workflows/concurrent-orchestration), [Multi-Agent Swarm](/ai/agent-patterns/dynamic-orchestration/multi-agent-swarm), [Group Chat Orchestration](/ai/agent-patterns/dynamic-orchestration/group-chat-orchestration), [Multi-Agent Loop](/ai/agent-patterns/iteration/multi-agent-loop), [Maker-Checker Loop](/ai/agent-patterns/iteration/maker-checker-loop), [Multi-Agent Iterative Refinement](/ai/agent-patterns/iteration/multi-agent-iterative-refinement), [Human-in-the-Loop](/ai/agent-patterns/special-requirements/human-in-the-loop)

### Adaptability (8)

[Multi-Agent Coordinator](/ai/agent-patterns/dynamic-orchestration/multi-agent-coordinator), [Multi-Agent Hierarchical Task Decomposition](/ai/agent-patterns/dynamic-orchestration/multi-agent-hierarchical-task-decomposition), [Multi-Agent Swarm](/ai/agent-patterns/dynamic-orchestration/multi-agent-swarm), [Group Chat Orchestration](/ai/agent-patterns/dynamic-orchestration/group-chat-orchestration), [Handoff Orchestration](/ai/agent-patterns/dynamic-orchestration/handoff-orchestration), [Magentic Orchestration](/ai/agent-patterns/dynamic-orchestration/magentic-orchestration), [ReAct](/ai/agent-patterns/iteration/react), [Custom Logic](/ai/agent-patterns/special-requirements/custom-logic)

### Human Oversight (4)

[Group Chat Orchestration](/ai/agent-patterns/dynamic-orchestration/group-chat-orchestration), [Magentic Orchestration](/ai/agent-patterns/dynamic-orchestration/magentic-orchestration), [Maker-Checker Loop](/ai/agent-patterns/iteration/maker-checker-loop), [Human-in-the-Loop](/ai/agent-patterns/special-requirements/human-in-the-loop)
