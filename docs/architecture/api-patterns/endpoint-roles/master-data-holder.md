---
title: Master Data Holder
pattern_slug: master-data-holder
category: Endpoint Roles
tags:
  - Shared Understanding
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Master Data Holder"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/master-data-holder.mdx';

# Master Data Holder

## Descrição

O padrão Master Data Holder expõe um endpoint de dados mestres, de vida longa e muito referenciados por outros dados, e oferece acesso cuidadoso, com regras claras de manutenção, para preservar sua qualidade e consistência.

Dados mestres descrevem as entidades centrais do negócio, como clientes, contas e produtos. Sobrevivem a muitos processos, mudam devagar em relação aos dados operacionais e são apontados por muitos outros registros e sistemas. Por isso, a manutenção é feita de forma controlada: criar e alterar exige validação, e remover costuma ser restrito ou substituído por uma marcação de inativo, para não quebrar referências.

O endpoint precisa pensar em identidade estável, versões e propagação de mudanças, já que vários clientes dependem da mesma fonte da verdade. Como esses dados são um ativo valioso, atraente para ataques e muitas vezes sob controle de um sistema ou de uma área externa, a proteção, a auditoria e a conformidade pesam mais do que em outros tipos de dado.

As atualizações podem ser de granularidade grossa, que substituem a maior parte dos atributos (como um PUT), ou parciais, que alteram poucos campos (como um PATCH). A remoção é tratada como um tipo especial de atualização: em geral o dado vai para um estado arquivado e imutável, preservando a trilha de auditoria. Os dados mestres têm muitas referências de entrada e podem ter referências de saída; os dados operacionais os referenciam, mas não o contrário.

## Problemas que resolve

- Vários sistemas mantendo cópias divergentes dos mesmos dados centrais do negócio
- Referências quebradas quando uma entidade importante é alterada ou apagada sem cuidado
- Falta de um ponto único e confiável para consultar e manter a identidade das entidades principais
- Mudanças em dados centrais que se propagam sem controle para quem depende deles

## Quando usar

- Os dados são centrais, duram anos e são referenciados por muitos outros recursos
- É necessária uma fonte única da verdade sobre clientes, contas ou produtos
- A manutenção precisa de validação, auditoria e regras explícitas de quem pode alterar
- Os consumidores toleram que as mudanças sejam menos frequentes e mais controladas

## Quando evitar

- Quando os dados são transitórios e mudam o tempo todo: use um [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder)
- Quando os dados são apenas uma tabela estável de consulta: use um [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder)
- Quando cada serviço deveria ser dono do seu próprio modelo e cópias locais são aceitáveis
- Quando o custo de governança supera o valor de centralizar a fonte

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Fonte única e consistente sobre as entidades centrais | Ponto central de dependência e possível gargalo de mudança |
| Referências estáveis entre sistemas e recursos | Alterar a estrutura afeta muitos consumidores ao mesmo tempo |
| Qualidade garantida por validação e regras de manutenção | Processo de mudança mais lento e burocrático |
| Boa candidata a cache, pois muda devagar | Cópias em cache podem ficar defasadas após uma alteração |

- **Remoção:** prefira arquivar ou inativar a apagar, para não deixar referências penduradas; se a exclusão for exigida por lei, oculte o dado dos consumidores sem destruí-lo, quando a regulação permitir.
- **Desenho do contrato:** não reduza o endpoint a CRUD sobre tabelas, que gera APIs tagarelas e acopladas; parta de raízes de agregado, capacidades ou processos de negócio, e dê operações semanticamente ricas (como validar e arquivar).
- **Controle externo:** sistemas de gestão de dados mestres, às vezes terceirizados, evoluem em outro ritmo e envolvem mais partes; concentrar o acesso em um único endpoint limita onde essa dependência aparece.
- **Evolução:** mudanças na estrutura exigem versionamento e comunicação cuidadosa com os consumidores.
- **Propriedade:** defina claramente quem é o dono dos dados e quem pode escrever.
- **Propagação:** considere publicar eventos de mudança para que os consumidores atualizem suas cópias.

## Diagrama

<Diagram />

Vários serviços referenciam e consultam a mesma fonte mestra, que concentra a validação e a manutenção.

## Exemplo

O cadastro de clientes da fintech é um dado mestre: contas, cartões e contratos de crédito apontam para ele. A alteração é validada e a remoção vira inativação.

```http
GET /customers/cus-9001 HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
ETag: "7"

{
  "id": "cus-9001",
  "legalName": "Maria Souza",
  "status": "ACTIVE",
  "accounts": ["acc-1001"]
}
```

```http
PATCH /customers/cus-9001 HTTP/1.1
If-Match: "7"
Content-Type: application/json

{ "status": "INACTIVE" }
```

O cliente nunca é apagado: ao ser inativado, os contratos e lançamentos (`LedgerEntry`) que o referenciam continuam válidos para consulta e auditoria.

## Padrões relacionados

- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — o papel geral do qual este é uma especialização
- [Operational Data Holder](/architecture/api-patterns/endpoint-roles/operational-data-holder) — o contraste: dados de vida curta e alta taxa de mudança
- [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) — dados estáveis, geralmente somente leitura
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — identificador estável que sustenta as referências
- [Bounded Context](/design/ddd/model-in-practice/bounded-context) — define de quem é o modelo dos dados mestres e onde as cópias divergem
- [Aggregate](/design/ddd/building-blocks/aggregate) — ponto de partida usual para identificar o endpoint, em vez de uma entidade por tabela
- [Domain Event](/architecture/microservices/service-collaboration/domain-event) — forma de propagar mudanças dos dados mestres para os consumidores

## Referência

- [Patterns for API Design, capítulo 5: Master Data Holder](https://api-patterns.org/)
