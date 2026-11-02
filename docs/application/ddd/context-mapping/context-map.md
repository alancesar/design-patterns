---
title: Context Map
pattern_slug: context-map
category: Context Mapping
tags:
  - Shared Understanding
  - Strategic Focus
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Context Map"
---

# Context Map

## Descrição

O Context Map é uma visão global dos Bounded Contexts de um projeto e dos relacionamentos reais entre eles. Ele registra quais contextos existem, onde passam as fronteiras, quem depende de quem (upstream e downstream) e que tipo de relação existe em cada ponto de integração, como Shared Kernel, Customer/Supplier ou Anticorruption Layer.

O mapa descreve a situação como ela é hoje, e não como se gostaria que fosse. Pode ser um diagrama, uma tabela ou um texto, desde que seja compartilhado e mantido pelos times. Cada contexto recebe um nome, que passa a fazer parte da linguagem comum da equipe, e cada relação deixa claro onde é necessário traduzir modelos ou coordenar mudanças.

Para Evans, o Context Map é o artefato central da modelagem estratégica: ele expõe as fricções entre times e modelos e guia decisões sobre onde investir em integração, onde isolar e onde aceitar a dependência.

## Problemas que resolve

- Fronteiras entre modelos implícitas, o que faz conceitos com o mesmo nome terem significados diferentes sem que ninguém perceba.
- Times que não sabem de quem dependem nem quem depende deles, descobrindo impactos só em produção.
- Integrações ad hoc, sem uma política clara de tradução ou de coordenação.
- Dificuldade de planejar mudanças que atravessam contextos e de dimensionar o esforço de integração.

## Quando usar

- Sempre que mais de um Bounded Context ou mais de um time participam do mesmo sistema ou ecossistema.
- Em iniciativas de modernização, para decidir onde isolar o legado e onde extrair novos serviços.
- Ao integrar com sistemas externos ou de terceiros, para tornar explícitas as dependências.

### Quando evitar

- Sistemas de contexto único, com um só time e um só modelo, em que o mapa seria cerimônia sem valor.
- Quando o mapa é desenhado como ideal futuro e nunca confrontado com a realidade; ele passa a enganar em vez de informar.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Visão compartilhada das fronteiras e dependências | Precisa ser mantido; mapas desatualizados são piores que nenhum |
| Expõe relações de poder e fricções entre times | Pode revelar conflitos organizacionais incômodos |
| Base para decisões de integração e de investimento | Esforço de levantamento inicial e de consenso |
| Vocabulário comum para falar de relações entre contextos | Risco de virar documento burocrático desligado do código |

- **Honestidade:** mapeie o que existe, inclusive relações ruins; a melhoria vem depois.
- **Granularidade:** comece com poucos contextos e refine; uma Big Ball of Mud pode aparecer como um único contexto no mapa.
- **Evolução:** revise o mapa quando times, produtos ou integrações mudarem.

## Diagrama

```mermaid
flowchart LR
    V["Sales"] -->|"Open-host Service + Published Language"| F["Billing"]
    V -->|"Customer/Supplier"| E["Inventory"]
    L["Legacy System"] -->|"Conformist"| E
    F -->|"Anticorruption Layer"| L
    P["Payments (third party)"] -->|"Open-host Service"| F
```

Cada aresta liga um contexto upstream ao seu downstream e é rotulada com o padrão de relacionamento que de fato vigora entre eles.

## Exemplo

Uma varejista tem os contextos Vendas, Estoque, Faturamento, um ERP legado e um gateway de pagamento de terceiro. Ao desenhar o mapa, o time descobre que Estoque simplesmente adota o modelo do ERP (Conformist), que Faturamento precisa de uma camada de tradução para conversar com o ERP (Anticorruption Layer) e que Vendas expõe uma API estável para vários consumidores (Open-host Service).

Com isso, o time decide priorizar a reunião quinzenal entre Vendas e Estoque (Customer/Supplier) e planejar a retirada gradual do ERP, usando o mapa como referência de onde as traduções são necessárias.

## Padrões relacionados

- [Bounded Context](../model-in-practice/bounded-context.md) — os nós do mapa; sem fronteiras explícitas não há o que mapear.
- [Shared Kernel](./shared-kernel.md) — um dos relacionamentos que o mapa registra.
- [Customer/Supplier Development](./customer-supplier-development.md) — relação upstream/downstream com negociação.
- [Conformist](./conformist.md) — downstream que adota o modelo do upstream.
- [Anticorruption Layer](../../../cloud/cloud-design-patterns/integration-and-modernization/anti-corruption-layer.md) — tradução defensiva no lado downstream.
- [Open-host Service](./open-host-service.md) — protocolo aberto para muitos consumidores.
- [Published Language](./published-language.md) — linguagem comum de troca entre contextos.
- [Separate Ways](./separate-ways.md) — decisão explícita de não integrar.
- [Partnership](./partnership.md) — times com sucesso interdependente.
- [Big Ball of Mud](./big-ball-of-mud.md) — região do mapa onde os modelos estão misturados.
- [Decompose by Subdomain](../../../architecture/microservices/service-boundaries/decompose-by-subdomain.md) — usa subdomínios do DDD para definir serviços.

## Referência

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003), cap. 14
- [DDD Crew: Context Mapping](https://github.com/ddd-crew/context-mapping)
