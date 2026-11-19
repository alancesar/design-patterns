---
title: Operational Data Holder
pattern_slug: operational-data-holder
category: Endpoint Roles
tags:
  - Performance
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Operational Data Holder"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/operational-data-holder.mdx';

# Operational Data Holder

## Descrição

O padrão Operational Data Holder expõe um endpoint de dados de vida curta e alta taxa de mudança, que os clientes podem criar, ler, atualizar e apagar com frequência.

Os dados operacionais são o resultado do trabalho do dia a dia do sistema: pedidos em andamento, cobranças abertas, sessões, lançamentos recentes. Têm vida curta ou média e costumam ter muitas referências de saída, apontando para dados mestres e para outros dados operacionais, enquanto quase nada aponta para eles. Tendem a ser arquivados quando o processo termina. O endpoint oferece operações completas de manutenção, e por isso carrega a responsabilidade de manter consistência e de lidar com acesso concorrente.

Por serem alterados com frequência, esses dados são pouco indicados para cache agressivo ou para referência de longo prazo. A fronteira entre dado operacional e mestre é subjetiva e depende do contexto: o que é passageiro para um aplicativo pode ser um ativo central para outro. Já os dados que sobrevivem a muitos ciclos e são apontados por vários outros ficam melhor em um [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder).

## Problemas que resolve

- Clientes que precisam registrar e atualizar rapidamente o estado de trabalhos em andamento
- Manutenção de dados transitórios sem pagar o custo de governança dos dados de longa vida
- Acesso eficiente a informações que mudam o tempo todo, com baixa latência
- Expor um CRUD simples para entidades cujo ciclo de vida acompanha um processo de negócio

## Quando usar

- Os dados nascem, mudam e terminam dentro de um processo, como uma cobrança Pix pendente
- Há muitas escritas e leituras, e a frescura da informação importa
- As entidades apontam para dados de vida mais longa, e quase nada aponta para elas
- É preciso velocidade de leitura e escrita e flexibilidade para mudar o esquema
- Os clientes precisam de operações de criação, atualização e remoção expostas diretamente

## Quando evitar

- Quando os dados vivem por anos e são referenciados por muitos outros: use um [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder)
- Quando os dados quase não mudam e o ideal é cache forte: use um [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder)
- Quando a regra de negócio exige executar uma atividade, e não só manter dados: use um [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource)
- Quando a consistência entre várias entidades operacionais depende de transações distribuídas difíceis de sustentar

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Modelo simples de manutenção direta dos dados em andamento | Cache e replicação têm eficácia limitada, pois os dados mudam depressa |
| Dados frescos, adequados a processos de negócio ativos | Escritas concorrentes exigem tratamento de conflitos |
| Baixo custo de governança por serem dados transitórios | Integridade referencial com outros recursos é difícil de garantir |
| Operações completas disponíveis para o cliente | Expor remoção e atualização amplas aumenta o risco de corrupção de estado |

- **Concorrência:** use versão ou ETag para detectar atualizações simultâneas e evitar sobrescritas perdidas.
- **Ciclo de vida:** defina quando o dado é arquivado ou removido, para que o endpoint não acumule histórico indevido.
- **Consistência:** as referências para dados operacionais devem tolerar que o alvo tenha desaparecido.
- **Transações:** com vários clientes simultâneos, ofereça isolamento e atomicidade, reverta ao último estado consistente após falhas e elimine duplicatas em repetições que não são idempotentes.
- **Relações:** não embuta dados mestres nas mensagens sem necessidade; prefira referenciá-los por link, e mantenha juntos os holders operacionais estreitamente relacionados.
- **Histórico:** são bons candidatos a event sourcing, que expõe todas as mudanças de estado, ao custo de mais complexidade para quem consulta instantâneos antigos.
- **Evolução:** vida curta e poucos dependentes facilitam mudar ou até reescrever o recurso, e relaxar a consistência para eventual pode melhorar a disponibilidade.
- **Desempenho:** índices e paginação importam, pois o volume é alto e a leitura é frequente.

## Diagrama

<Diagram />

O cliente mantém as cobranças enquanto o processo está ativo; ao terminar, o dado sai do conjunto operacional.

## Exemplo

As cobranças Pix pendentes da fintech são dados operacionais: nascem quando o lojista gera o QR code, mudam de estado quando o pagamento chega e expiram em minutos.

```http
POST /pix-charges HTTP/1.1
Content-Type: application/json

{
  "receiverAccountId": "acc-2040",
  "amount": { "cents": 8990, "currency": "BRL" },
  "expiresInSeconds": 900
}
```

```http
HTTP/1.1 201 Created
Location: /pix-charges/chg-5581
ETag: "1"
Content-Type: application/json

{ "id": "chg-5581", "status": "PENDING", "amount": { "cents": 8990, "currency": "BRL" } }
```

```http
PATCH /pix-charges/chg-5581 HTTP/1.1
If-Match: "1"
Content-Type: application/json

{ "status": "CANCELLED" }
```

O `If-Match` faz a atualização falhar com `412 Precondition Failed` se a cobrança tiver sido paga entre a leitura e a escrita. Taxas e limites são ilustrativos.

## Padrões relacionados

- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — o papel geral do qual este é uma especialização
- [Master Data Holder](/architecture/api-patterns/endpoint-roles/master-data-holder) — dados de vida longa e muito referenciados
- [Reference Data Holder](/architecture/api-patterns/endpoint-roles/reference-data-holder) — dados estáveis e somente leitura
- [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request) — evita sobrescritas concorrentes com `If-Match`
- [Embedded Entity](/architecture/api-patterns/message-granularity/embedded-entity) e [Linked Information Holder](/architecture/api-patterns/message-granularity/linked-information-holder) — embutir dados operacionais relacionados ou apontar por link para os mestres
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — controla o volume ao listar muitas entidades
- [Entity](/design/ddd/building-blocks/entity) — conceito de domínio que costuma estar por trás dos dados operacionais

## Referência

- [Patterns for API Design, capítulo 5: Operational Data Holder](https://api-patterns.org/)
