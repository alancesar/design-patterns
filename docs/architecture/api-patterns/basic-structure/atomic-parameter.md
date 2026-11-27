---
title: Atomic Parameter
pattern_slug: atomic-parameter
category: Basic Structure
tags:
  - Simplicity
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Atomic Parameter"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/basic-structure/atomic-parameter.mdx';

# Atomic Parameter

## Descrição

O padrão Atomic Parameter define um único parâmetro ou elemento de corpo de mensagem, de um tipo básico do formato de troca escolhido (número, texto, booleano ou bloco binário), como a menor unidade de dados transmitida entre cliente e provedor de uma API. É a base de toda a estrutura de mensagens: aparece em caminhos, consultas, cabeçalhos e corpos, e é a folha de qualquer estrutura maior.

O projetista escolhe o tipo, dá ao átomo um nome do vocabulário do domínio quando o receptor precisa identificá-lo, e documenta tipo, cardinalidade (um, opcional, vários) e obrigatoriedade na [API Description](/architecture/api-patterns/documentation/api-description). Também vale explicar o significado informalmente, incluindo a unidade de medida, e restringir os valores aceitos (faixa, formato) em um esquema como JSON Schema ou Protocol Buffers. Dados binários costumam exigir codificação, como Base64. Um átomo pode ter estrutura interna, como um texto que segue uma expressão regular, mas essa estrutura é responsabilidade das aplicações, não da serialização.

## Problemas que resolve

- Trocar um dado simples e sem estrutura (número, texto, flag, bytes) entre cliente e provedor
- Tornar explícito o significado, a unidade e a faixa de valores de cada dado transmitido
- Manter a mensagem mínima quando o cliente precisa de apenas um valor
- Dar a cada elemento um nome que desenvolvedores e pessoas de negócio entendam

## Quando usar

- Em operações cuja entrada ou saída é um único valor, como um identificador, um saldo ou uma confirmação
- Como bloco de construção de listas e árvores de parâmetros
- Quando o dado tem significado completo sozinho e não precisa de metadados agrupados

## Quando evitar

- Quando vários valores só fazem sentido juntos: use um [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list)
- Quando há relações de contêiner e conteúdo: use um [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree)
- Para "esconder" uma estrutura dentro de um texto (por exemplo, JSON serializado em string), o que contorna as ferramentas de serialização e traz riscos técnicos e de segurança

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Contrato simples, fácil de entender e de testar | Uma operação com muitos átomos soltos vira uma assinatura longa e frágil |
| Mapeia para qualquer formato e tecnologia | O significado e a unidade dependem de documentação, pois o tipo básico não os expressa |
| Mínimo de dados trafegados | Regras de validação ficam no nível da implementação, não do contrato de interoperabilidade |

- **Nomes:** use termos do domínio e seja consistente entre operações.
- **Unidade e faixa:** declare-as no esquema ou nos metadados; um valor monetário, por exemplo, deve ser inteiro em centavos, nunca um número de ponto flutuante.
- **Cardinalidade:** decida se o átomo é obrigatório, opcional ou múltiplo, e registre isso na descrição da API.
- **Tunelamento:** evite empacotar estruturas em strings opacas.

## Diagrama

<Diagram />

Uma única mensagem de requisição carrega um parâmetro e a resposta devolve outro, ambos de tipo básico.

## Exemplo

Consulta do saldo de uma conta da fintech. O identificador no caminho e o saldo da resposta são átomos; o saldo vem em centavos, como inteiro.

```http
GET /accounts/acc-7f3a/balance HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ "balanceCents": 1523075 }
```

Um átomo múltiplo seria, por exemplo, `{ "tags": ["salary", "rent"] }`, com cardinalidade "zero ou mais" documentada.

## Padrões relacionados

- [Atomic Parameter List](/architecture/api-patterns/basic-structure/atomic-parameter-list) — agrupa vários átomos relacionados em um único elemento
- [Parameter Tree](/architecture/api-patterns/basic-structure/parameter-tree) — usa átomos como folhas de uma hierarquia
- [Data Element](/architecture/api-patterns/element-stereotypes/data-element) — papel semântico que um átomo costuma assumir, assim como [Id Element](/architecture/api-patterns/element-stereotypes/id-element), [Metadata Element](/architecture/api-patterns/element-stereotypes/metadata-element) e [Link Element](/architecture/api-patterns/element-stereotypes/link-element)
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — normalmente é um átomo
- [API Description](/architecture/api-patterns/documentation/api-description) — onde nome, tipo e cardinalidade são registrados
- [Value Object](/design/poeaa/base/value-object) — no domínio, valores como `Money` encapsulam o átomo e suas regras; na API, ele trafega como tipo básico

## Referência

- [Patterns for API Design, capítulo 4: Atomic Parameter](https://api-patterns.org/)
