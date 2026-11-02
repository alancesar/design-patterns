---
title: "Agentic AI Design Patterns"
sidebar_label: "Agentic AI"
---

# Agentic AI Design Patterns

Catálogo pessoal baseado no guia [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system), do Google Cloud Architecture Center. Cobre os padrões de sistemas agênticos (de um agente só a sistemas multiagente), agrupados pelo tipo de workflow: determinístico, com orquestração dinâmica, com iteração ou com requisitos especiais. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (objetivos de orquestração) e um diagrama Mermaid.

Padrões marcados com ★ são compartilhados com outro catálogo: este catálogo aponta para o documento original, revisado com o conteúdo desta fonte.

Total: 12 padrões em 4 grupos. Etiquetas: Objetivo de orquestração.

## Grupos

- [Deterministic Workflows](#deterministic-workflows) (2)
- [Dynamic Orchestration](#dynamic-orchestration) (4)
- [Iteration](#iteration) (4)
- [Special Requirements](#special-requirements) (2)

## Deterministic Workflows (2) {#deterministic-workflows}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Multi-Agent Sequential](/ai/agent-orchestration/deterministic-workflows/sequential-orchestration) ★ | O Sequential Orchestration encadeia agentes de IA numa ordem linear predefinida. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Parallel](/ai/agent-orchestration/deterministic-workflows/concurrent-orchestration) ★ | O Concurrent Orchestration executa vários agentes de IA ao mesmo tempo sobre a mesma tarefa, de modo que cada um traga uma análise independente a partir da sua perspectiva ou especialização. | [`Parallelism`](/tags/parallelism) [`Specialization`](/tags/specialization) [`Output Quality`](/tags/output-quality) |

## Dynamic Orchestration (4) {#dynamic-orchestration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Single Agent](/ai/agentic-ai/dynamic-orchestration/single-agent) | Um único modelo, um conjunto definido de ferramentas e um prompt de sistema detalhado tratam o pedido do usuário de forma autônoma. | [`Predictability`](/tags/predictability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Coordinator](/ai/agentic-ai/dynamic-orchestration/multi-agent-coordinator) | Um agente coordenador central analisa o pedido do usuário, divide-o em subtarefas e despacha cada uma para um agente especializado (por exemplo, um que consulta um banco de dados ou chama uma API). | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Hierarchical Task Decomposition](/ai/agentic-ai/dynamic-orchestration/multi-agent-hierarchical-task-decomposition) | Os agentes se organizam em uma hierarquia de vários níveis. | [`Adaptability`](/tags/adaptability) [`Specialization`](/tags/specialization) |
| [Multi-Agent Swarm](/ai/agentic-ai/dynamic-orchestration/multi-agent-swarm) | Agentes especializados se comunicam entre si em todas as direções (all-to-all) e refinam iterativamente uma solução para um problema complexo. | [`Output Quality`](/tags/output-quality) [`Adaptability`](/tags/adaptability) |

## Iteration (4) {#iteration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [ReAct](/ai/agentic-ai/iteration/react) | Um único agente, conduzido por um modelo, repete um ciclo de três passos: raciocina sobre a tarefa (*thought*), escolhe entre chamar uma ferramenta ou dar a resposta final (*action*) e registra o resultado da ferramenta no contexto (*observation*). | [`Adaptability`](/tags/adaptability) |
| [Multi-Agent Loop](/ai/agentic-ai/iteration/multi-agent-loop) | Um agente de loop executa uma sequência de subagentes e, em seguida, verifica uma condição de saída. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) |
| [Multi-Agent Review and Critique](/ai/agent-orchestration/dynamic-orchestration/maker-checker-loop) ★ | Um agente, o **maker**, cria ou propõe algo, e outro agente, o **checker**, avalia o resultado contra critérios definidos. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) [`Human Oversight`](/tags/human-oversight) |
| [Multi-Agent Iterative Refinement](/ai/agentic-ai/iteration/multi-agent-iterative-refinement) | Um ou mais agentes trabalham em loop, alterando a cada passada um resultado guardado no estado da sessão. | [`Predictability`](/tags/predictability) [`Output Quality`](/tags/output-quality) |

## Special Requirements (2) {#special-requirements}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Human-in-the-Loop](/ai/agentic-ai/special-requirements/human-in-the-loop) | O agente executa o fluxo até um checkpoint predefinido e, ali, pausa e chama um sistema externo para que uma pessoa revise o trabalho. | [`Human Oversight`](/tags/human-oversight) [`Output Quality`](/tags/output-quality) |
| [Custom Logic](/ai/agentic-ai/special-requirements/custom-logic) | A orquestração é escrita em código, com instruções condicionais, laços e ramificações, em vez de usar um padrão predefinido. | [`Adaptability`](/tags/adaptability) [`Predictability`](/tags/predictability) |

## Por etiqueta

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
