---
title: Metadata Element
pattern_slug: metadata-element
category: Element Stereotypes
tags:
  - Shared Understanding
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Metadata Element"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/element-stereotypes/metadata-element.mdx';

# Metadata Element

## Descrição

O padrão Metadata Element acrescenta às mensagens de uma API elementos que explicam e enriquecem os demais, para que o receptor interprete o conteúdo corretamente sem fixar no código suposições sobre o significado dos dados. A moeda de um valor, o total de itens de uma lista, a versão de um documento ou o autor de uma alteração são exemplos típicos.

Muitos Metadata Elements são [Atomic Parameters](/architecture/api-patterns/basic-structure/atomic-parameter) simples, mas podem também formar uma [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree). Um jeito flexível, porém sujeito a erros, é usar pares chave-valor de texto que o receptor converte. Eles passam a fazer parte da [API Description](/architecture/api-patterns/documentation/api-description) e precisam ser mantidos atualizados; convém definir a atualidade esperada (por exemplo, quando um contador expira) e se o valor é imutável.

Existem três variantes: os metadados de **controle** (identificadores, flags, filtros, links, informação de segurança, somas de verificação) conduzem o processamento; os **agregados** resumem ou analisam outros elementos (contadores, estatísticas, totais de paginação); e os de **proveniência** revelam a origem dos dados (autor, sistema de origem, data de criação, versão).

Um mesmo elemento pode realizar mais de uma variante: um código de região, por exemplo, indica proveniência e também controla o processamento. Os `ETag` do HTTP são metadados de controle e de proveniência (veja [Conditional Request](/architecture/api-patterns/message-exchange-optimization/conditional-request)). Uma alternativa a incluir metadados em cada mensagem é uma operação dedicada que os devolve para um elemento identificado por um [Id Element](/architecture/api-patterns/element-stereotypes/id-element) ou [Link Element](/architecture/api-patterns/element-stereotypes/link-element).

## Problemas que resolve

- Receptores que precisam adivinhar a unidade, a moeda ou o formato de um valor
- Ambiguidade entre campo ausente, vazio e não aplicável
- Clientes com regras de interpretação fixas no código que quebram quando a API evolui
- Falta de rastreabilidade sobre a origem e a versão dos dados recebidos

## Quando usar

- Quando um valor só faz sentido acompanhado de um qualificador, como moeda, unidade ou fuso
- Quando o cliente precisa de totais, contadores ou indicadores para tomar decisões em tempo de execução
- Quando a origem, a versão ou a data de um dado importam para auditoria
- Quando se quer reduzir o acoplamento a convenções escritas só na documentação

## Quando evitar

- Quando a informação é estática e já está completa e acessível na documentação do contrato
- Em APIs sensíveis ao tamanho da mensagem, em que cada byte extra tem custo relevante
- Quando o provedor não consegue manter os metadados corretos e atualizados, pois metadado errado é pior que ausente
- Quando os metadados expõem detalhes internos que o cliente não deveria conhecer

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Elimina ambiguidades sintáticas e semânticas entre as partes | Aumenta o tamanho das mensagens e o custo de processamento |
| Deixa o conhecimento compartilhado explícito em tempo de execução | Exige manter os metadados corretos e frescos enquanto a API evolui |
| Permite decisões dinâmicas do cliente com base nos dados recebidos | Mais elementos para testar, documentar e versionar |
| Facilita auditoria e rastreabilidade de origem | Pares chave-valor genéricos são flexíveis, porém frágeis e sem tipagem |

- **Interoperabilidade:** qualificadores explícitos, como a moeda ao lado do valor, evitam leituras erradas.
- **Acoplamento:** o conhecimento sai do contrato estático e vai para o conteúdo da mensagem, o que pode tanto aumentar quanto reduzir o acoplamento.
- **Eficiência:** inclua apenas os metadados que o receptor realmente usa.
- **Atualidade:** defina quando cada metadado deixa de ser válido, como contadores de paginação.
- **Dependência:** o cliente deve depender dos metadados só quando necessário; nos demais casos, trate-os como conveniência opcional, e a API deve funcionar sem eles. Metadados de controle, como links de paginação, criam dependência assim que são introduzidos.
- **Excesso:** metadados demais incham a interface e dificultam a evolução e o versionamento.

## Diagrama

<Diagram />

Os três tipos de Metadata Elements acompanham os Data Elements na mesma mensagem e explicam seu conteúdo.

## Exemplo

O extrato da conta da fintech devolve os lançamentos e, ao lado deles, metadados que descrevem o resultado. Os valores são inteiros em centavos.

```json
{
  "entries": [
    { "id": "le_9001", "type": "PIX_IN", "amountCents": 25000 },
    { "id": "le_9002", "type": "BOLETO_OUT", "amountCents": -8990 }
  ],
  "meta": {
    "currency": "BRL",
    "totalCount": 137,
    "nextPage": "/accounts/acc_7f3a91/entries?cursor=c2",
    "generatedAt": "2026-11-17T09:30:00Z",
    "source": "ledger-service"
  }
}
```

Com `currency` o cliente não presume a moeda, `totalCount` e `nextPage` guiam a navegação e `generatedAt` e `source` dão rastreabilidade.

## Padrões relacionados

- [Data Element](/architecture/api-patterns/element-stereotypes/data-element) — os dados que os metadados explicam
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) e [Link Element](/architecture/api-patterns/element-stereotypes/link-element) — formam metadados de controle
- [Pagination](/architecture/api-patterns/response-shaping/pagination) — usa contadores e cursores como metadados agregados e de controle
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — agrupa metadados de contexto em um bloco próprio da mensagem
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — metadado de segurança que identifica o cliente
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — metadado que indica a versão do contrato
- [Envelope Wrapper](/architecture/eip/message-transformation/envelope-wrapper) — embrulha a carga com cabeçalhos, em outro nível de mensagem
- [Format Indicator](/architecture/eip/message-construction/format-indicator) — metadado que declara o formato do conteúdo

## Referência

- [Patterns for API Design, capítulo 6: Metadata Element](https://api-patterns.org/)
