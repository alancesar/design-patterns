---
title: Builder
pattern_slug: builder
category: Creational
tags:
  - Encapsulation
  - Simplicity
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Builder"
---

# Builder

## Descrição

O Builder separa a construção de um objeto complexo da sua representação, permitindo que o mesmo processo de construção produza representações diferentes. Em vez de montar o objeto de uma só vez por um construtor com muitos parâmetros, a criação é dividida em etapas nomeadas e explícitas.

Um `Builder` define as operações para criar cada parte do produto; implementações concretas (`ConcreteBuilder`) sabem como montar e guardar essas partes e expõem um método para obter o resultado final. Opcionalmente, um `Director` encapsula a ordem dos passos para receitas de construção recorrentes, de modo que o cliente só escolhe qual builder usar.

Na prática moderna, a variante mais comum é o builder fluente (métodos encadeados que retornam o próprio builder), usado para criar objetos imutáveis com muitos atributos opcionais e validar a consistência do objeto antes de entregá-lo.

## Problemas que resolve

- Construtores com longas listas de parâmetros, muitos deles opcionais, difíceis de ler e propensos a erros de ordem (o "telescoping constructor")
- Necessidade de montar um objeto passo a passo, às vezes com etapas condicionais ou repetidas
- Mesmo processo de construção precisando gerar representações diferentes (ex.: documento em HTML, Markdown ou PDF)
- Criação de objetos imutáveis cujo estado deve estar completo e válido no momento em que são entregues

## Quando usar

- O objeto tem muitos atributos, principalmente opcionais ou com valores padrão
- A construção envolve várias etapas, ordem relevante ou regras de validação entre campos
- Você quer reutilizar o mesmo algoritmo de montagem para produzir produtos diferentes
- Você precisa de objetos imutáveis, mas sem construtores gigantes
- Montagem de estruturas compostas (árvores, consultas SQL, requisições HTTP, mensagens)

## Quando evitar

- O objeto é simples, com poucos campos obrigatórios; um construtor ou factory resolve
- A linguagem já oferece parâmetros nomeados e valores padrão que eliminam o problema
- Os produtos não compartilham um processo de construção comum, tornando a abstração artificial
- O custo de manter um builder sincronizado com cada mudança na classe de produto não compensa

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Código cliente legível e autodocumentado (passos nomeados) | Mais classes e código a manter (um builder por produto) |
| Permite produtos imutáveis e validação centralizada em `build()` | Duplicação de campos entre builder e produto |
| Isola o código de construção da lógica de negócio do produto | Builder pode ficar desatualizado em relação ao produto |
| Mesmo processo gera representações diferentes | Erros de campos obrigatórios esquecidos só aparecem em tempo de execução (salvo builders tipados por etapa) |

- **Acoplamento:** o cliente depende do builder, não da representação interna do produto.
- **Testabilidade:** builders facilitam criar dados de teste ("test data builders") com valores padrão sensatos.
- **Complexidade:** o `Director` é opcional; muitas vezes adiciona camadas sem benefício real.
- **Concorrência:** builders são mutáveis e normalmente não devem ser compartilhados entre threads.

## Diagrama

```mermaid
classDiagram
    class Director {
        -builder: Builder
        +construct()
    }
    class Builder {
        <<interface>>
        +buildPartA()
        +buildPartB()
        +getResult() Product
    }
    class ConcreteBuilder {
        -product: Product
        +buildPartA()
        +buildPartB()
        +getResult() Product
    }
    class Product
    class Client
    Director o--> Builder
    Builder <|.. ConcreteBuilder
    ConcreteBuilder ..> Product : cria
    Client --> Director
    Client --> ConcreteBuilder
```

O `Client` cria um `ConcreteBuilder` e o entrega ao `Director`, que chama os passos de construção na ordem correta; ao final, o cliente obtém o `Product` montado a partir do próprio builder via `getResult()`.

## Exemplo

Uma aplicação monta requisições HTTP com URL obrigatória e vários cabeçalhos, timeout e corpo opcionais. Um builder fluente deixa a criação legível e garante que a requisição final seja imutável e válida.

```java
public final class HttpRequest {
    private final String url, method, body;
    private final Map<String, String> headers;
    private final int timeoutMs;

    private HttpRequest(Builder b) {
        url = b.url; method = b.method; body = b.body;
        headers = Map.copyOf(b.headers); timeoutMs = b.timeoutMs;
    }

    public static Builder builder(String url) { return new Builder(url); }

    public static final class Builder {
        private final String url;
        private String method = "GET", body;
        private final Map<String, String> headers = new HashMap<>();
        private int timeoutMs = 5000;

        private Builder(String url) { this.url = url; }
        public Builder method(String m) { this.method = m; return this; }
        public Builder header(String k, String v) { headers.put(k, v); return this; }
        public Builder body(String b) { this.body = b; return this; }
        public Builder timeout(int ms) { this.timeoutMs = ms; return this; }

        public HttpRequest build() {
            if (body != null && method.equals("GET"))
                throw new IllegalStateException("GET nao aceita corpo");
            return new HttpRequest(this);
        }
    }
}

// Uso
HttpRequest req = HttpRequest.builder("https://api.example.com/orders")
    .method("POST").header("Content-Type", "design/json")
    .body("{\"id\": 42}").timeout(2000).build();
```

## Padrões relacionados

- [Abstract Factory](/coding/gof/creational/abstract-factory) — também cria objetos complexos, mas retorna famílias de produtos de uma vez; o Builder foca em montar um produto passo a passo
- [Telescoping Constructor](/coding/gof/creational/telescoping-constructor) — antipadrão que o Builder normalmente substitui
- [Factory Method](/coding/gof/creational/factory-method) — alternativa mais simples quando a criação cabe em uma única chamada
- [Prototype](/coding/gof/creational/prototype) — outra forma de evitar construção complexa, clonando um objeto já configurado
- [Composite](/coding/gof/structural/composite) — o Builder é frequentemente usado para montar árvores Composite
- [Singleton](/coding/gof/creational/singleton) — um Director ou builder compartilhado às vezes é exposto como instância única

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Builder no Refactoring.Guru](https://refactoring.guru/design-patterns/builder)
