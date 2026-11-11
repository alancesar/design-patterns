---
title: Value Object
pattern_slug: value-object
category: Base
tags:
  - Consistency
  - Simplicity
  - Testability
also_in:
  - application/ddd/building-blocks
source: https://martinfowler.com/eaaCatalog/valueObject.html
sidebar_label: "Value Object"
---

# Value Object

## Descrição

O Value Object é um objeto pequeno e simples, como um valor monetário ou um intervalo de datas, cuja igualdade não se baseia em identidade. Dois Value Objects com os mesmos valores são intercambiáveis: o que importa é o valor, não qual instância específica está em uso.

Isso o diferencia dos objetos de referência (entidades), identificados por uma chave ou por identidade de objeto. O Value Object se parece com os tipos primitivos das linguagens, só que modelando conceitos do domínio, como `Money`, `DateRange`, `Email` ou `Address`.

Na prática, um bom Value Object é imutável, compara por valor (implementando igualdade e hash a partir dos campos) e concentra a validação e o comportamento do conceito que representa. No Domain-Driven Design, o Value Object é um bloco de construção do modelo, ao lado de [Entity](/design/ddd/building-blocks/entity) e de [Aggregate](/design/ddd/building-blocks/aggregate). Evans recomenda preferir Value Objects sempre que o conceito não exigir identidade, pois são mais simples de raciocinar, testar e compartilhar. Dentro de um Aggregate, eles descrevem a raiz e as entidades internas e podem ser copiados ou substituídos livremente, sem cuidado com ciclo de vida.

## Problemas que resolve

- "Obsessão por primitivos": strings e números soltos representando conceitos do domínio, sem validação ou comportamento.
- Aliasing: duas partes do código compartilhando e alterando o mesmo objeto sem perceber.
- Comparações incorretas por identidade de objeto quando se queria comparar valores.
- Regras de validação e formatação duplicadas em vários lugares.

## Quando usar

- Quando o conceito é definido apenas por seus atributos (valor monetário, intervalo, coordenada, e-mail, CEP).
- Quando se quer garantir invariantes na construção, de forma que o objeto seja sempre válido.
- Quando se quer imutabilidade para evitar efeitos colaterais e facilitar concorrência.
- Em conjunto com [Embedded Value](/design/poeaa/object-relational-structural/embedded-value) para persisti-lo dentro da linha do dono.

## Quando evitar

- Quando o objeto tem ciclo de vida e identidade próprios, que precisam ser rastreados (use uma entidade com [Identity Field](/design/poeaa/object-relational-structural/identity-field)).
- Quando o conceito muda com frequência e a imutabilidade geraria muita criação de objetos sem benefício.
- Quando o valor é realmente trivial e o encapsulamento acrescentaria apenas cerimônia.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Elimina aliasing e efeitos colaterais, graças à imutabilidade | Mais objetos criados (custo de alocação) |
| Validação e comportamento concentrados no conceito | Mais classes pequenas para escrever e manter |
| Igualdade por valor, simples de comparar e testar | Mapeamento para banco exige atenção (Embedded Value, colunas) |
| Código mais expressivo que primitivos soltos | Linguagens sem suporte nativo exigem implementar igualdade e hash à mão |

- **Consistência:** invariantes garantidas na construção.
- **Testabilidade:** objetos puros, sem dependências, são triviais de testar.
- **Concorrência:** imutáveis são seguros para compartilhar entre threads.

## Diagrama

```mermaid
classDiagram
    class Account {
        +id
    }
    class PixKey {
        +type
        +value
        +equals(other)
    }
    Account --> PixKey
```

A entidade `Account` possui uma `PixKey`. A `PixKey` não tem identidade: é comparada e substituída por valor.

## Exemplo

Uma conta digital representa a chave Pix como um Value Object imutável que valida o próprio formato.

```python
import re
from dataclasses import dataclass

_PATTERNS = {
    "cpf": r"\d{11}",
    "email": r"[^@\s]+@[^@\s]+\.[^@\s]+",
    "phone": r"\+55\d{10,11}",
    "random": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
}

@dataclass(frozen=True)
class PixKey:
    key_type: str
    value: str

    def __post_init__(self):
        pattern = _PATTERNS.get(self.key_type)
        if pattern is None:
            raise ValueError("tipo de chave desconhecido")
        if not re.fullmatch(pattern, self.value):
            raise ValueError("formato inválido para o tipo de chave")

a = PixKey("email", "ana@example.com")
b = PixKey("email", "ana@example.com")
assert a == b  # igualdade por valor
```

Records do Java e do C#, `dataclass(frozen=True)` no Python e `Struct` no Ruby são formas idiomáticas de declarar Value Objects.

## Padrões relacionados

- [Money](/design/poeaa/base/money) — o exemplo clássico de Value Object.
- [Embedded Value](/design/poeaa/object-relational-structural/embedded-value) — mapeia um Value Object para colunas da tabela do objeto dono.
- [Serialized LOB](/design/poeaa/object-relational-structural/serialized-lob) — alternativa para persistir um Value Object complexo como bloco serializado.
- [Special Case](/design/poeaa/base/special-case) — um valor especial (como "sem desconto") pode ser modelado como Value Object ou como Special Case.
- [Entity](/design/ddd/building-blocks/entity) — contraparte do DDD, definida por identidade e não por valor.
- [Aggregate](/design/ddd/building-blocks/aggregate) — Value Objects compõem os agregados e descrevem a raiz.
- [Domain Model](/design/poeaa/domain-logic/domain-model) — Value Objects compõem o modelo de domínio ao lado das entidades.
- [Flyweight](/coding/gof/structural/flyweight) — objetos imutáveis podem ser compartilhados com segurança, o que viabiliza o Flyweight.
- [Data Transfer Object](/design/poeaa/distribution/data-transfer-object) — também é um objeto de dados, mas sem comportamento nem invariantes, voltado à transferência.

## Referência

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/valueObject.html)
- [Value Object (bliki)](https://martinfowler.com/bliki/ValueObject.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
