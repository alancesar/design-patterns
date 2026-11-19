---
title: Data Element
pattern_slug: data-element
category: Element Stereotypes
tags:
  - Decoupling
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Data Element"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/element-stereotypes/data-element.mdx';

# Data Element

## Descrição

O padrão Data Element define um vocabulário dedicado de elementos de dados para as mensagens de requisição e resposta de uma API, que embrulha e mapeia as partes relevantes do modelo interno do provedor sem expor suas definições internas. É o estereótipo mais geral entre os elementos de representação: descreve o papel de qualquer parâmetro que carrega informação de domínio ou de aplicação.

Um Data Element pode ser um [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) simples, uma [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) ou uma folha de uma [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree); os mais ricos costumam conter um [Id Element](/architecture/api-patterns/element-stereotypes/id-element) e vários atributos do domínio. Várias instâncias transferidas juntas formam uma coleção de elementos. O esquema da mensagem deve ser explícito e documentado, e o mapeamento entre o modelo interno (tabelas, entidades, agregados) e esse vocabulário público fica sob responsabilidade do provedor, de modo que o cliente nunca precise saber como os dados são gravados.

Em termos de DDD, o vocabulário de Data Elements funciona como uma Published Language que protege agregados, entidades e objetos de valor da camada de domínio.

Há duas variantes dignas de nota: o **Entity Element**, que contém um identificador e indica um ciclo de vida de objeto na Published Language, e o **Query Parameter**, que não representa entidades da API, e sim uma expressão usada para selecionar um subconjunto delas em uma [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation). Os elementos podem ser fortemente tipados, com esquema rico, ou genéricos, como listas de pares chave-valor, que são flexíveis, mas pouco validáveis. Padrões do DDD não devem ser traduzidos um a um para a API; o provedor deve desenhar sua linguagem pública para minimizar o acoplamento indesejado.

## Problemas que resolve

- Vazamento de tabelas, colunas ou classes internas do provedor para o contrato da API
- Acoplamento entre cliente e provedor por strings livres interpretadas por convenção implícita
- Dificuldade de evoluir o modelo interno sem quebrar os consumidores
- Falta de um vocabulário comum que torne a API compreensível e documentável

## Quando usar

- Ao definir as mensagens de qualquer operação que troque informação de negócio
- Quando o modelo interno muda em ritmo diferente do contrato público
- Quando vários clientes, com necessidades distintas, consomem a mesma API
- Quando se quer um contrato descrito por esquema, testável e versionável

## Quando evitar

- Para mensagens triviais com um único valor, em que um parâmetro atômico já basta
- Quando cliente e provedor compartilham o mesmo modelo e equipe e o mapeamento extra só traz cerimônia
- Para expor referências remotas a objetos ou stubs, que tornam a comunicação com estado
- Quando o vocabulário público espelharia o modelo interno campo a campo, sem ganho de isolamento

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Desacopla o contrato da API do modelo de dados interno | Exige código de mapeamento entre o modelo interno e o vocabulário público |
| Vocabulário explícito que facilita documentação e compreensão | Mais elementos a documentar, testar e manter à medida que a API evolui |
| Liberdade para refatorar o modelo interno sem quebrar clientes | Decidir o que expor é uma escolha difícil e afeta compatibilidade futura |
| Esquemas verificáveis melhoram a interoperabilidade | Flexibilidade excessiva (campos opcionais, variações) aumenta o custo de testes |

- **Funcionalidade versus simplicidade:** quanto mais dados e comportamento expostos, mais opções de uso e mais risco de inconsistência e de documentação extensa.
- **Segurança e privacidade:** expor menos detalhes reduz a superfície de ataque, mas pode exigir configuração extra.
- **Manutenção versus flexibilidade:** cada campo novo precisa de análise de compatibilidade e suporte enquanto houver clientes que o usem.
- **Nomes e tipos:** escolha nomes do domínio de negócio, não nomes de colunas, e valores monetários como inteiros em centavos.
- **Granularidade:** uma linguagem rica e profunda é expressiva, mas difícil de proteger e manter; uma simples é fácil de ensinar, mas pode não representar as particularidades do domínio. Na dúvida, deixe o elemento de fora.

## Diagrama

<Diagram />

O cliente troca apenas Data Elements com o endpoint; o mapeamento traduz esse vocabulário para o modelo interno, que permanece invisível.

## Exemplo

A API de contas da fintech devolve uma conta como um conjunto de Data Elements do domínio, e não as colunas da tabela `tb_acct`. Os valores monetários são inteiros em centavos.

```http
GET /accounts/acc_7f3a91 HTTP/1.1
Accept: application/json
```

```json
{
  "id": "acc_7f3a91",
  "holderName": "Maria Souza",
  "status": "ACTIVE",
  "balance": { "amountCents": 1523050, "currency": "BRL" },
  "openedOn": "2024-03-12"
}
```

O provedor pode renomear colunas, dividir tabelas ou trocar de banco sem alterar esse contrato.

## Padrões relacionados

- [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) e [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — estruturas que dão forma aos Data Elements
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — Data Element especializado que identifica as demais entidades
- [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) — complementa os dados com informação que explica seu significado
- [Published Language](/design/ddd/context-mapping/published-language) — o vocabulário público compartilhado, na visão do DDD
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — objeto de transferência que carrega Data Elements entre as camadas
- [Anti-Corruption Layer](/architecture/cloud-design-patterns/integration-and-modernization/anti-corruption-layer) — protege o próprio modelo do de terceiros, enquanto o Data Element protege o modelo do provedor dos clientes

## Referência

- [Patterns for API Design, capítulo 6: Data Element](https://api-patterns.org/)
