---
title: Parameter Forest
pattern_slug: parameter-forest
category: Basic Structure
tags:
  - Simplicity
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Parameter Forest"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/basic-structure/parameter-forest.mdx';

# Parameter Forest

## Descrição

O padrão Parameter Forest reúne duas ou mais árvores de parâmetros no nível superior do cabeçalho ou do corpo de uma mensagem, localizadas por posição ou por nome. Assim como átomos formam listas, árvores podem ser agrupadas, mas só no topo: uma floresta não contém outra floresta.

Na maioria dos mapeamentos tecnológicos, uma floresta equivale a uma [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) cujo primeiro nível são os membros da floresta, e a JSON resultante é praticamente idêntica. A diferença aparece na assinatura da operação: uma interface pode receber um único objeto contendo as duas árvores ou dois parâmetros separados. Em APIs HTTP, o conjunto de parâmetros de caminho, de consulta, de cookie e o corpo já forma uma floresta. Uma floresta vira árvore ao se introduzir uma raiz artificial, e o livro mantém os dois padrões para modelar com fidelidade tecnologias como HTTP, SOAP e gRPC.

## Problemas que resolve

- Expor várias estruturas independentes como carga útil de uma única operação
- Modelar fielmente tecnologias em que a operação recebe vários parâmetros de topo
- Evitar uma raiz artificial quando as partes não pertencem a um mesmo conceito

## Quando usar

- Quando uma operação recebe ou devolve conjuntos distintos de dados de negócio, como uma lista de contas e uma lista de cartões
- Ao descrever APIs HTTP que combinam caminho, consulta e corpo
- Quando a tecnologia da plataforma trata os parâmetros de topo como itens separados

## Quando evitar

- Quando as partes formam um único conceito: use uma [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) com raiz própria
- Quando só há uma estrutura: a floresta seria uma abstração sem ganho
- Quando o formato não distingue florestas de árvores e a diferença só confundiria o contrato

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Modela com precisão operações com vários parâmetros de topo | Em JSON é indistinguível de uma árvore, o que gera confusão |
| Mantém as partes independentes e nomeadas | Tem suporte limitado em algumas tecnologias (por exemplo, WSDL) |
| Permite evoluir cada árvore separadamente | Muitas árvores de topo tornam a operação pouco coesa |

- **Equivalência:** uma floresta sempre pode virar árvore com uma raiz artificial; escolha a forma que combina melhor com a plataforma.
- **Coesão:** se uma operação precisa de muitas árvores independentes, talvez ela faça coisas demais.
- **Localização:** identifique os membros por nome sempre que possível, pois a posição é frágil.

## Diagrama

<Diagram />

A mensagem carrega duas árvores no nível superior, sem uma raiz comum.

## Exemplo

Resposta de um resumo financeiro da fintech com duas árvores de topo, contas e cartões, localizadas por nome.

```http
GET /customers/cus-42/summary HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "accounts": [
    {
      "accountId": "acc-7f3a",
      "balanceCents": 1523075,
      "recentEntries": [
        { "entryId": "le-1001", "type": "PIX_IN", "amountCents": 25000 }
      ]
    }
  ],
  "cards": [
    { "cardId": "card-88", "limitCents": 500000, "usedCents": 120000 }
  ]
}
```

Em uma interface de serviço, isso pode ser um único objeto com os dois campos ou dois parâmetros separados, como `List<Account>` e `List<Card>`; a primeira forma é mais fácil de evoluir.

## Padrões relacionados

- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — cada membro da floresta é uma árvore, e a floresta equivale a uma árvore com raiz artificial
- [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) — o paralelo para átomos: uma lista agrupa átomos, uma floresta agrupa árvores
- [Atomic Parameter](/architecture/api-patterns/basic-structure/atomic-parameter) — o bloco de construção mais simples da família
- [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle) — também reúne várias partes em uma mensagem, mas agrupa requisições inteiras, não dados
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — o objeto que agrega as várias árvores em uma interface de serviço

## Referência

- [Patterns for API Design, capítulo 4: Parameter Forest](https://api-patterns.org/)
