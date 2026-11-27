---
title: Semantic Versioning
pattern_slug: semantic-versioning
category: Versioning
tags:
  - Evolvability
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Semantic Versioning"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/versioning/semantic-versioning.mdx';

# Semantic Versioning

## Descrição

O padrão Semantic Versioning estrutura o identificador de versão em três números (`MAJOR.MINOR.PATCH`) cujas partes indicam, por si só, se uma nova versão é compatível com a anterior.

Um número único de versão não diz quão grande foi a mudança, e cada cliente teria de ler a documentação ou rodar testes para descobrir o impacto. Com três partes, a regra fica clara: incrementa-se o `MAJOR` quando há mudanças incompatíveis, o `MINOR` quando se acrescentam funcionalidades de modo compatível, e o `PATCH` quando se corrigem erros sem alterar o contrato. Ao aumentar um número, os da direita voltam a zero.

Assim, clientes e provedor comparam duas versões e concluem imediatamente se podem trocar uma pela outra ou se precisam planejar uma migração. O padrão ajuda a separar mudanças com impacto diferente, mas depende da disciplina do provedor: o número só vale se a classificação das mudanças for feita com rigor, e há casos de fronteira em que decidir o que é "incompatível" não é óbvio.

## Problemas que resolve

- Incerteza sobre o impacto de uma atualização, que obriga cada cliente a analisar a mudança por conta própria
- Dificuldade de planejar o esforço e o risco de migração para uma nova versão
- Mistura, em um mesmo número, de correções, novidades e quebras de contrato
- Falta de uma linguagem comum entre equipes para falar de compatibilidade

## Quando usar

- Em APIs com vários clientes que precisam decidir sozinhos se uma nova versão é segura de adotar
- Quando o provedor publica versões com frequência e quer comunicar o impacto de cada uma
- Quando o identificador também aparece na [API Description](/architecture/api-patterns/documentation/api-description) e em ferramentas de automação que comparam versões
- Em conjunto com o [Version Identifier](/architecture/api-patterns/versioning/version-identifier), para dar estrutura ao número

## Quando evitar

- Quando a API é interna e evolui junto com seu único cliente, de modo que a distinção entre tipos de mudança tem pouco valor
- Se o provedor não consegue ou não quer avaliar a compatibilidade de cada mudança com rigor, pois um número que mente é pior que nenhum
- Quando o contexto exige apenas a versão principal, como em URLs `/v1` e `/v2`, e as partes menores seriam ruído para o cliente
- Em APIs experimentais, sem garantias, cobertas pelo [Experimental Preview](/architecture/api-patterns/life-cycle-management/experimental-preview)

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Compatibilidade legível a partir do número, sem análise manual | Exige disciplina para classificar corretamente cada mudança |
| Separação clara entre correção, novidade e quebra | Casos de fronteira, como mudar a semântica de um campo, podem ser mal classificados |
| Planejamento de migração com esforço e risco conhecidos | Mais versões de `MINOR` e `PATCH` para publicar e documentar |
| Linguagem comum entre provedor, clientes e ferramentas | Clientes podem confiar demais no número e pular testes de integração |

- **Regra de incremento:** `MAJOR` para quebra, `MINOR` para novidade compatível, `PATCH` para correção; os números à direita são zerados.
- **Onde expor:** na [API Description](/architecture/api-patterns/documentation/api-description) e em um único ponto das mensagens, como no [Version Identifier](/architecture/api-patterns/versioning/version-identifier).
- **Nem tudo vira versão:** apenas a versão `MAJOR` costuma aparecer na URL; as demais ficam na descrição ou em cabeçalhos informativos.
- **Compatibilidade tem dois lados:** adicionar campos pode ser seguro para quem lê, mas quebrar quem valida o esquema de forma rígida.

## Diagrama

<Diagram />

Dada a versão atual, o tipo de incremento já diz ao cliente se ele pode atualizar direto ou se precisa planejar uma migração.

## Exemplo

A API de contas de uma fintech publica versões de `Account`. Um cliente usa a regra de compatibilidade para decidir se atualiza sozinho. Os números abaixo são ilustrativos e o resultado é o mesmo em todas as linguagens. O provedor devolve a versão em um cabeçalho informativo:

```http
GET /accounts/9021 HTTP/1.1

HTTP/1.1 200 OK
X-Api-Version: 2.4.1

{"id": "9021", "balanceCents": 250000, "currency": "BRL"}
```

O cliente compara a versão atual com a anunciada:

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
public class SemVer {
    static int[] parse(String version) {
        String[] parts = version.split("\\.");
        return new int[] {
            Integer.parseInt(parts[0]),
            Integer.parseInt(parts[1]),
            Integer.parseInt(parts[2])
        };
    }

    static String classify(String from, String to) {
        int[] a = parse(from);
        int[] b = parse(to);
        if (b[0] != a[0]) return "breaking";
        if (b[1] != a[1]) return "compatible feature";
        if (b[2] != a[2]) return "compatible fix";
        return "same";
    }

    public static void main(String[] args) {
        System.out.println(classify("2.4.1", "3.0.0")); // breaking
        System.out.println(classify("2.4.1", "2.5.0")); // compatible feature
        System.out.println(classify("2.4.1", "2.4.2")); // compatible fix
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from typing import Tuple


def parse(version: str) -> Tuple[int, int, int]:
    major, minor, patch = (int(p) for p in version.split("."))
    return major, minor, patch


def classify(current: str, new: str) -> str:
    a, b = parse(current), parse(new)
    if b[0] != a[0]:
        return "breaking"
    if b[1] != a[1]:
        return "compatible feature"
    if b[2] != a[2]:
        return "compatible fix"
    return "same"


print(classify("2.4.1", "3.0.0"))  # breaking
print(classify("2.4.1", "2.5.0"))  # compatible feature
print(classify("2.4.1", "2.4.2"))  # compatible fix
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func parse(version string) [3]int {
	var v [3]int
	for i, p := range strings.Split(version, ".") {
		v[i], _ = strconv.Atoi(p)
	}
	return v
}

func classify(from, to string) string {
	a, b := parse(from), parse(to)
	switch {
	case a[0] != b[0]:
		return "breaking"
	case a[1] != b[1]:
		return "compatible feature"
	case a[2] != b[2]:
		return "compatible fix"
	}
	return "same"
}

func main() {
	fmt.Println(classify("2.4.1", "3.0.0")) // breaking
	fmt.Println(classify("2.4.1", "2.5.0")) // compatible feature
	fmt.Println(classify("2.4.1", "2.4.2")) // compatible fix
}
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — define onde o número vai; o Semantic Versioning define como compô-lo
- [API Description](/architecture/api-patterns/documentation/api-description) — documenta as versões e o que mudou em cada uma
- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) — duas versões `MAJOR` convivem enquanto os clientes migram
- [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee) — a garantia de suporte costuma ser dada por versão `MAJOR`
- [Consumer-Driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test) — verifica na prática se uma versão `MINOR` ou `PATCH` realmente preservou o contrato

## Referência

- [Patterns for API Design, capítulo 8: Semantic Versioning](https://api-patterns.org/)
- [Semantic Versioning 2.0.0](https://semver.org/)
