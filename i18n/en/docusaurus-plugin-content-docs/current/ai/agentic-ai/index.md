---
title: "Agentic AI Design Patterns"
sidebar_label: "Agentic AI"
---

# Agentic AI Design Patterns

Personal catalog based on the [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) guide from the Google Cloud Architecture Center. It covers patterns for agentic systems (from a single agent to multi-agent systems), grouped by workflow type: deterministic, with dynamic orchestration, with iteration, or with special requirements. Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (orchestration goals), and a Mermaid diagram.

Patterns marked with ★ are shared with another catalog: this catalog points to the original document, revised with content from this source.

Total: 12 patterns in 4 groups. Tags: Orchestration goal.

## Groups

- [Deterministic Workflows](#deterministic-workflows) (2)
- [Dynamic Orchestration](#dynamic-orchestration) (4)
- [Iteration](#iteration) (4)
- [Special Requirements](#special-requirements) (2)

## Deterministic Workflows (2) {#deterministic-workflows}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Multi-Agent Sequential](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration) ★ | Sequential Orchestration chains AI agents in a predefined linear order. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Parallel](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration) ★ | Concurrent Orchestration runs several AI agents at the same time on the same task, so that each one brings an independent analysis from its own perspective or specialty. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) |

## Dynamic Orchestration (4) {#dynamic-orchestration}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Single Agent](/ai/agentic-ai/dynamic-orchestration/single-agent) | A single model, a defined set of tools, and a detailed system prompt handle the user's request autonomously. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Coordinator](/ai/agentic-ai/dynamic-orchestration/multi-agent-coordinator) | A central coordinator agent analyzes the user's request, splits it into subtasks, and dispatches each one to a specialized agent (for example, one that queries a database or calls an API). | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Hierarchical Task Decomposition](/ai/agentic-ai/dynamic-orchestration/multi-agent-hierarchical-task-decomposition) | Agents are organized in a multi-level hierarchy. | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Swarm](/ai/agentic-ai/dynamic-orchestration/multi-agent-swarm) | Specialized agents communicate with one another in every direction (all-to-all) and iteratively refine a solution to a complex problem. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) |

## Iteration (4) {#iteration}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [ReAct](/ai/agentic-ai/iteration/react) | A single model-driven agent repeats a three-step cycle: it reasons about the task (*thought*), chooses between calling a tool or giving the final answer (*action*), and records the tool's result in the context (*observation*). | [`Adaptability`](/tags/adaptability) |
| [Multi-Agent Loop](/ai/agentic-ai/iteration/multi-agent-loop) | A loop agent runs a sequence of subagents and then checks an exit condition. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) |
| [Multi-Agent Review and Critique](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop) ★ | One agent, the **maker**, creates or proposes something, and another agent, the **checker**, evaluates the result against defined criteria. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) |
| [Multi-Agent Iterative Refinement](/ai/agentic-ai/iteration/multi-agent-iterative-refinement) | One or more agents work in a loop, changing a result stored in the session state on each pass. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) |

## Special Requirements (2) {#special-requirements}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Human-in-the-Loop](/ai/agentic-ai/special-requirements/human-in-the-loop) | The agent runs the flow up to a predefined checkpoint, where it pauses and calls an external system so a person can review the work. | [`Human Oversight`](/tags/human-oversight) [`Output Quality`](/tags/output-quality) |
| [Custom Logic](/ai/agentic-ai/special-requirements/custom-logic) | The orchestration is written in code, with conditionals, loops, and branches, instead of using a predefined pattern. | [`Adaptability`](/tags/adaptability) [`Predictability`](/tags/predictability) |

## By tag

### Predictability (6)

[Multi-Agent Sequential](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration), [Single Agent](/ai/agentic-ai/dynamic-orchestration/single-agent), [Multi-Agent Loop](/ai/agentic-ai/iteration/multi-agent-loop), [Multi-Agent Review and Critique](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop), [Multi-Agent Iterative Refinement](/ai/agentic-ai/iteration/multi-agent-iterative-refinement), [Custom Logic](/ai/agentic-ai/special-requirements/custom-logic)

### Parallelism (1)

[Multi-Agent Parallel](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration)

### Specialization (5)

[Multi-Agent Sequential](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration), [Multi-Agent Parallel](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration), [Single Agent](/ai/agentic-ai/dynamic-orchestration/single-agent), [Multi-Agent Coordinator](/ai/agentic-ai/dynamic-orchestration/multi-agent-coordinator), [Multi-Agent Hierarchical Task Decomposition](/ai/agentic-ai/dynamic-orchestration/multi-agent-hierarchical-task-decomposition)

### Output Quality (6)

[Multi-Agent Parallel](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration), [Multi-Agent Swarm](/ai/agentic-ai/dynamic-orchestration/multi-agent-swarm), [Multi-Agent Loop](/ai/agentic-ai/iteration/multi-agent-loop), [Multi-Agent Review and Critique](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop), [Multi-Agent Iterative Refinement](/ai/agentic-ai/iteration/multi-agent-iterative-refinement), [Human-in-the-Loop](/ai/agentic-ai/special-requirements/human-in-the-loop)

### Adaptability (5)

[Multi-Agent Coordinator](/ai/agentic-ai/dynamic-orchestration/multi-agent-coordinator), [Multi-Agent Hierarchical Task Decomposition](/ai/agentic-ai/dynamic-orchestration/multi-agent-hierarchical-task-decomposition), [Multi-Agent Swarm](/ai/agentic-ai/dynamic-orchestration/multi-agent-swarm), [ReAct](/ai/agentic-ai/iteration/react), [Custom Logic](/ai/agentic-ai/special-requirements/custom-logic)

### Human Oversight (2)

[Multi-Agent Review and Critique](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop), [Human-in-the-Loop](/ai/agentic-ai/special-requirements/human-in-the-loop)
