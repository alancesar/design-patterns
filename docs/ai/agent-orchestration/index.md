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
| [Sequential Orchestration](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration) | O Sequential Orchestration encadeia agentes de IA numa ordem linear predefinida. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Concurrent Orchestration](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration) | O Concurrent Orchestration executa vários agentes de IA ao mesmo tempo sobre a mesma tarefa, de modo que cada um traga uma análise independente a partir da sua perspectiva ou especialização. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) |

## Dynamic Orchestration (4) {#dynamic-orchestration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Group Chat Orchestration](/ai/agent-orchestration/dynamic-orchestration/group-chat-orchestration) | Vários agentes de IA resolvem um problema, tomam uma decisão ou validam um trabalho participando de uma única conversa compartilhada. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) |
| [Maker-Checker Loop](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop) | Um agente, o **maker**, cria ou propõe algo, e outro agente, o **checker**, avalia o resultado contra critérios definidos. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) |
| [Handoff Orchestration](/ai/agent-orchestration/dynamic-orchestration/handoff-orchestration) | Delegação dinâmica de tarefas entre agentes especializados. | [`Specialization`](/tags/specialization) [`Adaptability`](/tags/adaptability) |
| [Magentic Orchestration](/ai/agent-orchestration/dynamic-orchestration/magentic-orchestration) | Voltado a problemas abertos e complexos, sem plano de abordagem predeterminado. | [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) |

## Por etiqueta

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
