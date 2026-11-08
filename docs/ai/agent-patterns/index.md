---
title: "AI Agent Design Patterns"
sidebar_label: "Agent Patterns"
---

# AI Agent Design Patterns

Catálogo pessoal que reúne duas fontes: o guia [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), do Azure Architecture Center, e o guia [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system), do Google Cloud Architecture Center. Cobre os padrões de sistemas agênticos, de um agente só a sistemas multiagente, agrupados pelo tipo de workflow: determinístico, com orquestração dinâmica, com iteração ou com requisitos especiais. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (objetivos de orquestração) e um diagrama Mermaid.

A coluna Origem indica de qual fonte vem cada padrão, e a seção Referência de cada página aponta para a fonte original. Três padrões aparecem nas duas fontes com nomes diferentes: Sequential Orchestration (*Multi-Agent Sequential* no Google), Concurrent Orchestration (*Multi-Agent Parallel*) e Maker-Checker Loop (*Multi-Agent Review and Critique*).

Total: 15 padrões em 4 grupos. Etiquetas: Objetivo de orquestração.

## Grupos

- [Deterministic Workflows](#deterministic-workflows) (2)
- [Dynamic Orchestration](#dynamic-orchestration) (7)
- [Iteration](#iteration) (4)
- [Special Requirements](#special-requirements) (2)

## Deterministic Workflows (2) {#deterministic-workflows}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [Sequential Orchestration](/ai/agent-patterns/deterministic-workflows/sequential-orchestration) | O Sequential Orchestration encadeia agentes de IA numa ordem linear predefinida. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) | Azure, Google |
| [Concurrent Orchestration](/ai/agent-patterns/deterministic-workflows/concurrent-orchestration) | O Concurrent Orchestration executa vários agentes de IA ao mesmo tempo sobre a mesma tarefa, de modo que cada um traga uma análise independente a partir da sua perspectiva ou especialização. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) | Azure, Google |

## Dynamic Orchestration (7) {#dynamic-orchestration}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [Single Agent](/ai/agent-patterns/dynamic-orchestration/single-agent) | Um único modelo, um conjunto definido de ferramentas e um prompt de sistema detalhado tratam o pedido do usuário de forma autônoma. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) | Google |
| [Multi-Agent Coordinator](/ai/agent-patterns/dynamic-orchestration/multi-agent-coordinator) | Um agente coordenador central analisa o pedido do usuário, divide-o em subtarefas e despacha cada uma para um agente especializado (por exemplo, um que consulta um banco de dados ou chama uma API). | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) | Google |
| [Multi-Agent Hierarchical Task Decomposition](/ai/agent-patterns/dynamic-orchestration/multi-agent-hierarchical-task-decomposition) | Os agentes se organizam em uma hierarquia de vários níveis. | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) | Google |
| [Multi-Agent Swarm](/ai/agent-patterns/dynamic-orchestration/multi-agent-swarm) | Agentes especializados se comunicam entre si em todas as direções (all-to-all) e refinam iterativamente uma solução para um problema complexo. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) | Google |
| [Group Chat Orchestration](/ai/agent-patterns/dynamic-orchestration/group-chat-orchestration) | Vários agentes de IA resolvem um problema, tomam uma decisão ou validam um trabalho participando de uma única conversa compartilhada. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) | Azure |
| [Handoff Orchestration](/ai/agent-patterns/dynamic-orchestration/handoff-orchestration) | Delegação dinâmica de tarefas entre agentes especializados. | [`Specialization`](/tags/specialization) [`Adaptability`](/tags/adaptability) | Azure |
| [Magentic Orchestration](/ai/agent-patterns/dynamic-orchestration/magentic-orchestration) | Voltado a problemas abertos e complexos, sem plano de abordagem predeterminado. | [`Adaptability`](/tags/adaptability) [`Human Oversight`](/tags/human-oversight) | Azure |

## Iteration (4) {#iteration}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [ReAct](/ai/agent-patterns/iteration/react) | Um único agente, conduzido por um modelo, repete um ciclo de três passos: raciocina sobre a tarefa (*thought*), escolhe entre chamar uma ferramenta ou dar a resposta final (*action*) e registra o resultado da ferramenta no contexto (*observation*). | [`Adaptability`](/tags/adaptability) | Google |
| [Multi-Agent Loop](/ai/agent-patterns/iteration/multi-agent-loop) | Um agente de loop executa uma sequência de subagentes e, em seguida, verifica uma condição de saída. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) | Google |
| [Maker-Checker Loop](/ai/agent-patterns/iteration/maker-checker-loop) | Um agente, o **maker**, cria ou propõe algo, e outro agente, o **checker**, avalia o resultado contra critérios definidos. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) | Azure, Google |
| [Multi-Agent Iterative Refinement](/ai/agent-patterns/iteration/multi-agent-iterative-refinement) | Um ou mais agentes trabalham em loop, alterando a cada passada um resultado guardado no estado da sessão. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) | Google |

## Special Requirements (2) {#special-requirements}

| Padrão | Resumo | Etiquetas | Origem |
| --- | --- | --- | --- |
| [Human-in-the-Loop](/ai/agent-patterns/special-requirements/human-in-the-loop) | O agente executa o fluxo até um checkpoint predefinido e, ali, pausa e chama um sistema externo para que uma pessoa revise o trabalho. | [`Human Oversight`](/tags/human-oversight) [`Output Quality`](/tags/output-quality) | Google |
| [Custom Logic](/ai/agent-patterns/special-requirements/custom-logic) | A orquestração é escrita em código, com instruções condicionais, laços e ramificações, em vez de usar um padrão predefinido. | [`Adaptability`](/tags/adaptability) [`Predictability`](/tags/predictability) | Google |

## Por etiqueta

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
