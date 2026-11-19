---
title: Id Element
pattern_slug: id-element
category: Element Stereotypes
tags:
  - Shared Understanding
  - Decoupling
source: https://api-patterns.org/
sidebar_label: "Id Element"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/element-stereotypes/id-element.mdx';

# Id Element

## Descrição

O padrão Id Element introduz um tipo especial de Data Element, o identificador único, para distinguir endpoints, operações e elementos de mensagem que precisam ser diferenciados em tempo de projeto e de execução. O mesmo identificador deve ser usado de forma consistente na descrição e na implementação da API.

É preciso decidir o esquema de nomes e documentá-lo na [API Description](/architecture/api-patterns/documentation/api-description). Abordagens populares são os UUIDs (identificadores de 128 bits que bibliotecas padrão geram), textos legíveis gerados pelo provedor e chaves substitutas atribuídas por camadas inferiores, como a chave primária de um banco. Também é preciso definir o escopo: um identificador local só vale dentro de um endpoint ou API, enquanto um global é único entre sistemas e dura mais, ao custo de coordenar o espaço de nomes.

Id Elements normalmente trafegam como [Atomic Parameters](/architecture/api-patterns/basic-structure/atomic-parameter), entradas de listas ou folhas de árvores de parâmetros. Em DDD, identificam elementos da Published Language, como entidades e agregados.

Os identificadores podem ser legíveis por pessoas e por máquinas: se usuários precisam digitá-los, prefira nomes curtos e fáceis de pronunciar; caso contrário, UUIDs numéricos. URIs são globalmente únicas, mas podem ser reatribuídas ao longo do tempo e apontar para alvos inesperados; URNs, com prefixo hierárquico, são uma alternativa. O escopo também pode ser limitado no tempo, como um cursor de paginação válido só durante a sessão.

## Problemas que resolve

- Ambiguidade ao referenciar entidades que vivem em endpoints ou serviços diferentes
- Necessidade de seguir relacionamentos sem embutir todos os dados relacionados na resposta
- Conflitos de nomes quando identificadores locais são usados fora do seu contexto
- Identificadores previsíveis que permitem enumerar ou adivinhar recursos alheios

## Quando usar

- Quando o modelo é dividido em vários recursos ou serviços que se referenciam
- Quando o cliente precisa apontar de forma inequívoca para uma instância específica
- Quando se quer correlacionar chamadas, auditorias e eventos sobre a mesma entidade
- Quando as entidades têm ciclo de vida longo e o identificador precisa se manter estável

## Quando evitar

- Quando os dados relacionados cabem na resposta e o cliente sempre os usa: considere o [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity)
- Quando o cliente precisa de um endereço acessível pela rede, não só de um nome: use um [Link Element](/architecture/api-patterns/element-stereotypes/link-element)
- Para identificar objetos efêmeros que nunca são referenciados depois
- Expondo chaves de banco sequenciais em contextos nos quais a previsibilidade seja um risco

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Referência curta e inequívoca a qualquer elemento da API | Identificadores globais exigem coordenação e manutenção do espaço de nomes |
| Mensagens menores que embutir a entidade inteira | O cliente precisa de chamadas extras para obter os detalhes |
| Permite seguir relacionamentos entre endpoints | Identificadores locais podem colidir se usados fora do contexto original |
| Base para correlação, auditoria e idempotência | Exposição de chaves previsíveis facilita enumeração |

- **Esforço versus estabilidade:** nomes locais são fáceis de criar, mas globais duram mais.
- **Legibilidade:** identificadores longos e estruturados ajudam pessoas; curtos e opacos servem às máquinas.
- **Segurança:** quando adivinhar um identificador for um risco, use valores aleatórios e confira a autorização em cada acesso.
- **Escopo e vida útil:** documente onde o identificador é único e por quanto tempo a unicidade é garantida.
- **Contadores:** números autoincrementais vazam informação e são difíceis de manter únicos em ambientes distribuídos; ideal é todos os identificadores de um tipo seguirem o mesmo esquema, o que facilita monitoramento e correlação de eventos.
- **Autorização:** mesmo com identificadores aleatórios, proteja o acesso ao elemento identificado com autorização por objeto, para evitar o ataque de autorização quebrada em nível de objeto.

## Diagrama

<Diagram />

Duas mensagens distintas referenciam a mesma conta pelo mesmo Id Element, o que permite ao cliente relacioná-las e buscar os detalhes quando precisar.

## Exemplo

Na fintech, uma cobrança Pix e o lançamento gerado por ela se referenciam por identificadores opacos, com prefixo que indica o tipo. Eles são gerados pelo provedor e não revelam a ordem de criação.

```json
{
  "id": "pix_01HZX4Q8M2",
  "accountId": "acc_7f3a91",
  "amountCents": 25000,
  "currency": "BRL",
  "status": "PAID",
  "ledgerEntryId": "le_9001"
}
```

O cliente guarda `id` para consultar ou conciliar a cobrança e usa `accountId` e `ledgerEntryId` para navegar até os outros recursos.

## Padrões relacionados

- [Data Element](/architecture/api-patterns/element-stereotypes/data-element) — o Id Element é uma especialização dele
- [Link Element](/architecture/api-patterns/element-stereotypes/link-element) — vai além, ao tornar a referência um endereço acessível pela rede
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) e [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — tipos particulares de identificadores
- [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) e [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) — recursos cujas instâncias exigem identificação robusta
- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) — alternativa que evita o identificador ao embutir os dados
- [Identity Field](/design/poeaa/object-relational-structural/identity-field) — mantém a identidade do banco no objeto; o Id Element a expõe na API
- [Entity](/design/ddd/building-blocks/entity) — objeto de domínio definido por sua identidade, que o Id Element representa na mensagem
- [Correlation Identifier](/architecture/eip/message-construction/correlation-identifier) — identificador que associa uma resposta à sua requisição em mensageria

## Referência

- [Patterns for API Design, capítulo 6: Id Element](https://api-patterns.org/)
- [RFC 4122: A UUID URN Namespace](https://www.rfc-editor.org/rfc/rfc4122)
