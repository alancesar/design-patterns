---
title: Information Holder Resource
pattern_slug: information-holder-resource
category: Endpoint Roles
tags:
  - Shared Understanding
  - Decoupling
source: https://api-patterns.org/
sidebar_label: "Information Holder Resource"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/information-holder-resource.mdx';

# Information Holder Resource

## Descrição

O padrão Information Holder Resource expõe um endpoint que representa uma entidade de dados identificável e oferece operações para criá-la, lê-la e mantê-la, escondendo como ela é armazenada.

O endpoint é modelado em torno de um conceito do domínio (conta, cartão, contrato de crédito) e trata os dados como o centro do contrato. Os clientes consultam e alteram a informação por operações de leitura e escrita, enquanto a estrutura interna do banco, as tabelas e os serviços que a sustentam permanecem privados. A entidade ganha um identificador estável, usado para referenciá-la em outras mensagens.

Cada operação do recurso tem uma única responsabilidade: criar a entidade, recuperá-la (inclusive buscas filtradas) ou transicioná-la, o que inclui atualizar e remover. O provedor define pré e pós-condições e invariantes, decide se o componente é com ou sem estado e coordena o acesso concorrente (bloqueio otimista ou pessimista, consistência forte ou eventual).

O padrão é o papel genérico para endpoints centrados em dados e tem cinco refinamentos. Três diferem pela mutabilidade, pelas relações e pela vida útil dos dados: [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder), [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) e [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder). O [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) guarda apenas referências a outros endpoints, e o [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) guarda dados temporários compartilhados, que pertencem aos clientes.

## Problemas que resolve

- Expor dados do domínio para vários clientes sem acoplá-los ao esquema físico do banco
- Dar a cada entidade de negócio um ponto de acesso identificável, referenciável por outros recursos
- Evitar que cada cliente reimplemente regras de acesso, validação e consistência sobre os mesmos dados
- Permitir que a estrutura de armazenamento evolua sem forçar mudanças nos consumidores
- Evitar os dois extremos: esconder todos os dados atrás de operações de processamento (muitas chamadas pequenas ou dados duplicados) e expor o banco diretamente (acoplamento total ao esquema e riscos de segurança)

## Quando usar

- A atividade principal do cliente é consultar ou manter entidades, como contas, cartões e contratos
- Os dados precisam ser compartilhados entre vários clientes com uma visão consistente
- Existe uma identidade clara para cada entidade, que pode virar parte da URL
- A API deve ser fácil de entender porque espelha o vocabulário do domínio

## Quando evitar

- Quando a necessidade é executar uma atividade de negócio: prefira um [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource)
- Quando a API apenas espelha as tabelas do banco, expondo detalhes internos e criando acoplamento forte
- Quando o endpoint mistura dados de ciclos de vida muito distintos, o que pede dividi-lo em papéis mais específicos
- Quando a consistência entre várias entidades exige uma transação que o cliente não conseguiria coordenar

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Contrato fácil de entender, alinhado ao vocabulário do domínio | Risco de refletir o modelo interno e vazar o esquema do banco |
| Armazenamento escondido atrás de uma interface estável | Cliente pode precisar de várias chamadas para montar uma visão completa |
| Dados compartilhados com um único ponto de verdade | Mudar a estrutura da entidade afeta todos os consumidores |
| Facilita cache e identificação com URLs e identificadores | Expor escrita demais convida a violar invariantes do domínio |

- **Granularidade:** decida o tamanho da entidade exposta; muito pequena gera conversa excessiva, muito grande carrega dados que o cliente não usa.
- **Especialização:** classifique o endpoint como operacional, mestre ou de referência para definir frequência de mudança, cache e quem pode escrever.
- **Identidade:** use identificadores opacos e estáveis, sem expor chaves internas do banco.
- **Evolução:** versione e evolua a estrutura do recurso com cuidado, pois os dados são compartilhados.
- **Acoplamento:** um desenho centrado em dados costuma empurrar o processamento para os consumidores e gerar operações CRUD que aumentam o acoplamento semântico e operacional; há quem trate o recurso de dados puro como antipadrão ("entity service"), então use-o de forma consciente e esconda certos dados atrás de um Processing Resource.
- **Segurança e consistência:** nem todo cliente deve ler ou escrever da mesma forma (chaves de API, RBAC/ABAC), e é preciso definir como tratar atraso de dados, cache e indisponibilidade temporária.
- **Muitos recursos pequenos:** vários Information Holders de granularidade fina exigem muitas chamadas e espalham a responsabilidade pela qualidade dos dados.

## Diagrama

<Diagram />

Vários clientes acessam a mesma entidade pelo contrato; o armazenamento e as chaves internas permanecem escondidos.

## Exemplo

A API de contas da fintech trata a conta digital como um Information Holder Resource. O cliente lê e atualiza a conta pelo identificador, sem saber como os saldos e os lançamentos são guardados.

```http
GET /accounts/acc-1001 HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "acc-1001",
  "holderName": "Maria Souza",
  "status": "ACTIVE",
  "balance": { "cents": 250000, "currency": "BRL" }
}
```

```http
PATCH /accounts/acc-1001 HTTP/1.1
Content-Type: application/json

{ "notificationEmail": "maria@example.com" }
```

O saldo é um valor monetário em centavos inteiros, nunca um número de ponto flutuante. Alterações no saldo não são feitas por escrita direta: elas decorrem de novos lançamentos (`LedgerEntry`) gerados por outras operações.

## Padrões relacionados

- [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) — o papel complementar, focado em ações em vez de dados
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) — especialização para dados de vida curta e alta taxa de mudança
- [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — especialização para dados de vida longa referenciados por muitos
- [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) — especialização para dados estáveis, somente leitura
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — guarda só referências para outros recursos
- [Data Transfer Resource](/architecture/api-patterns/endpoint-roles/data-transfer-resource) — espaço compartilhado de dados temporários, de propriedade dos clientes
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) e [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) — as operações típicas, que modelam a semântica CRUD
- [Repository](/design/poeaa/object-relational-metadata-mapping/repository) — o equivalente local: o Information Holder Resource é a sua contraparte de API
- [Aggregate](/design/ddd/building-blocks/aggregate) — costuma ser a base de implementação, sem correspondência de um para um
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — identificador usado para endereçar a entidade
- [Entity](/design/ddd/building-blocks/entity) — o conceito de domínio que costuma ser exposto por esse tipo de endpoint

## Referência

- [Patterns for API Design, capítulo 5: Information Holder Resource](https://api-patterns.org/)
