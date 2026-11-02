---
title: "AI Agent Orchestration Patterns"
sidebar_label: "Agent Orchestration"
---

# AI Agent Orchestration Patterns

Catálogo pessoal baseado no guia [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), do Azure Architecture Center. Cobre os padrões de coordenação de vários agentes de IA, agrupados pelo tipo de roteamento (determinístico ou dinâmico). Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (objetivos de orquestração) e um diagrama Mermaid.

Total: 6 padrões em 2 grupos. Etiquetas: Objetivo de orquestração.

## Grupos

- [Deterministic Workflows](#deterministic-workflows) (2)
- [Dynamic Orchestration](#dynamic-orchestration) (4)

## Deterministic Workflows (2) {#deterministic-workflows}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Sequential Orchestration](./deterministic-workflows/sequential-orchestration.md) | O Sequential Orchestration encadeia agentes de IA numa ordem linear predefinida. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Concurrent Orchestration](./deterministic-workflows/concurrent-orchestration.md) | O Concurrent Orchestration executa vários agentes de IA ao mesmo tempo sobre a mesma tarefa, de modo que cada um traga uma análise independente a partir da sua perspectiva ou especialização. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) |

## Dynamic Orchestration (4) {#dynamic-orchestration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Group Chat Orchestration](./dynamic-orchestration/group-chat-orchestration.md) | Vários agentes de IA resolvem um problema, tomam uma decisão ou validam um trabalho participando de uma única conversa compartilhada. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) |
| [Maker-Checker Loop](./dynamic-orchestration/maker-checker-loop.md) | Um agente, o **maker**, cria ou propõe algo, e outro agente, o **checker**, avalia o resultado contra critérios definidos. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) |
| [Handoff Orchestration](./dynamic-orchestration/handoff-orchestration.md) | Delegação dinâmica de tarefas entre agentes especializados. | [`Specialization`](/tags/specialization) [`Adaptability`](/tags/adaptability) |
| [Magentic Orchestration](./dynamic-orchestration/magentic-orchestration.md) | Voltado a problemas abertos e complexos, sem plano de abordagem predeterminado. | [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) |

## Por etiqueta

### Predictability (2)

[Sequential Orchestration](./deterministic-workflows/sequential-orchestration.md), [Maker-Checker Loop](./dynamic-orchestration/maker-checker-loop.md)

### Parallelism (1)

[Concurrent Orchestration](./deterministic-workflows/concurrent-orchestration.md)

### Specialization (3)

[Sequential Orchestration](./deterministic-workflows/sequential-orchestration.md), [Concurrent Orchestration](./deterministic-workflows/concurrent-orchestration.md), [Handoff Orchestration](./dynamic-orchestration/handoff-orchestration.md)

### Output Quality (3)

[Concurrent Orchestration](./deterministic-workflows/concurrent-orchestration.md), [Group Chat Orchestration](./dynamic-orchestration/group-chat-orchestration.md), [Maker-Checker Loop](./dynamic-orchestration/maker-checker-loop.md)

### Adaptability (3)

[Group Chat Orchestration](./dynamic-orchestration/group-chat-orchestration.md), [Handoff Orchestration](./dynamic-orchestration/handoff-orchestration.md), [Magentic Orchestration](./dynamic-orchestration/magentic-orchestration.md)

### Human Oversight (3)

[Group Chat Orchestration](./dynamic-orchestration/group-chat-orchestration.md), [Maker-Checker Loop](./dynamic-orchestration/maker-checker-loop.md), [Magentic Orchestration](./dynamic-orchestration/magentic-orchestration.md)
