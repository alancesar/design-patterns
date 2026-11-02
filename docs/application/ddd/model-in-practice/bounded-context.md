---
title: Bounded Context
pattern_slug: bounded-context
category: Putting the Model to Work
tags:
  - Consistency
  - Team Autonomy
  - Decoupling
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Bounded Context"
---

# Bounded Context

## Descrição

Um Bounded Context define explicitamente a fronteira dentro da qual um modelo de domínio específico se aplica. Dentro dessa fronteira, cada termo tem um único significado e o modelo é internamente consistente; fora dela, o mesmo termo pode significar outra coisa, e isso é aceito.

A fronteira é definida em termos práticos: organização dos times, partes da aplicação, base de código e esquema do banco de dados. Em vez de perseguir um modelo único e universal para toda a empresa, o DDD aceita vários modelos, cada um com seu contexto, e trata o relacionamento entre eles de forma explícita por meio do Context Map.

O Bounded Context é o alicerce do design estratégico: é nele que a Ubiquitous Language ganha significado preciso e é a partir dele que se decide onde investir esforço de modelagem.

## Problemas que resolve

- Conceitos ambíguos, como "Cliente" ou "Produto", com significados conflitantes em áreas diferentes do negócio.
- Modelo "unificado" que tenta agradar a todos e acaba inconsistente e confuso.
- Times pisando no código uns dos outros por falta de fronteiras claras.
- Vazamento de conceitos de um modelo para outro, corrompendo ambos.

## Quando usar

- Quando o mesmo termo tem significados diferentes para áreas distintas do negócio.
- Quando mais de um time contribui para o mesmo sistema e o modelo começa a ficar incoerente.
- Ao desenhar a decomposição de um sistema grande, seja em módulos ou em serviços.

### Quando evitar

- Sistemas pequenos, mantidos por um único time, em que um único modelo coeso é suficiente.
- Quando a fronteira é traçada só por critério técnico (camadas, tecnologia) e ignora o significado do domínio.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Modelo consistente e vocabulário preciso dentro da fronteira | Duplicação de conceitos entre contextos |
| Times com autonomia para evoluir seu modelo | Necessidade de tradução e integração nas fronteiras |
| Base para decompor em módulos ou serviços | Fronteiras mal traçadas são caras de corrigir depois |

- **Integração:** os relacionamentos entre contextos precisam ser mapeados e gerenciados, em geral com um Context Map.
- **Fronteira organizacional:** o contexto costuma coincidir com a fronteira de um time; a Lei de Conway atua a favor ou contra.
- **Consistência:** a consistência do modelo vale só dentro do contexto; entre contextos ela é negociada.

## Diagrama

```mermaid
flowchart LR
    subgraph Vendas ["Contexto de Vendas"]
        V1["Cliente = comprador com carrinho e pedidos"]
    end
    subgraph Suporte ["Contexto de Suporte"]
        S1["Cliente = solicitante de chamados"]
    end
    subgraph Cobranca ["Contexto de Cobrança"]
        C1["Cliente = pagador com contrato e fatura"]
    end
    Vendas -->|"traduz"| Cobranca
    Suporte -->|"traduz"| Vendas
```

O termo "Cliente" tem um modelo próprio em cada contexto, e as setas indicam pontos de tradução entre eles.

## Exemplo

Uma empresa de telecomunicações tinha uma única classe `Customer` com mais de cem atributos, alterada por vendas, cobrança e suporte. Cada mudança de um time quebrava outro. A equipe separou três Bounded Contexts: em Vendas, o cliente é um lead com propostas e planos; em Cobrança, é o titular de um contrato com faturas e inadimplência; em Suporte, é quem abre chamados e tem um histórico de atendimento.

Cada contexto passou a ter seu modelo, seu código e seu esquema de banco, com um identificador de cliente compartilhado como única ligação. As integrações passaram por uma camada de tradução, e o vocabulário de cada time ficou preciso dentro do seu contexto.

## Padrões relacionados

- [Ubiquitous Language](./ubiquitous-language.md) — a linguagem vale dentro de um Bounded Context.
- [Continuous Integration](./continuous-integration.md) — mantém o modelo coeso dentro da fronteira.
- [Context Map](../context-mapping/context-map.md) — descreve os relacionamentos entre Bounded Contexts.
- [Anticorruption Layer](../../../cloud/azure/integration-and-modernization/anti-corruption-layer.md) — protege o modelo de influências externas.
- [Shared Kernel](../context-mapping/shared-kernel.md) — subconjunto do modelo compartilhado entre contextos.
- [Decompose by Subdomain](../../../architecture/microservices/service-boundaries/decompose-by-subdomain.md) — Bounded Contexts costumam guiar a divisão em microsserviços.
- [Database per Service](../../../architecture/microservices/service-collaboration/database-per-service.md) — reforça a fronteira do modelo no armazenamento.

## Referência

- [BoundedContext, bliki de Martin Fowler](https://martinfowler.com/bliki/BoundedContext.html)
- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
