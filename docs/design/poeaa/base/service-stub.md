---
title: Service Stub
pattern_slug: service-stub
category: Base
tags:
  - Testability
  - Decoupling
source: https://martinfowler.com/eaaCatalog/serviceStub.html
sidebar_label: "Service Stub"
---

# Service Stub

## Descrição

O Service Stub remove a dependência de serviços problemáticos durante os testes. Aplicações corporativas costumam depender de serviços fora do controle da equipe, como consulta de crédito, cálculo de impostos ou motores de preço. Esses serviços podem estar atrasados, instáveis, lentos ou simplesmente indisponíveis no ambiente de desenvolvimento.

A solução é substituir o serviço real, durante os testes, por uma implementação local e em memória que devolve respostas previsíveis. O stub é rápido, determinístico e não depende da disponibilidade do sistema externo. Em geral ele é plugado no lugar de um [Gateway](/design/poeaa/base/gateway) por meio de um [Separated Interface](/design/poeaa/base/separated-interface) e escolhido por configuração, com o [Plugin](/design/poeaa/base/plugin).

O padrão foi proposto por David Rice no PoEAA e é a base do que hoje se chama de fakes e stubs em testes automatizados.

## Problemas que resolve

- Testes dependentes de serviços remotos lentos ou instáveis.
- Desenvolvimento bloqueado porque o serviço externo ainda não foi entregue.
- Testes que não conseguem rodar sem rede ou credenciais.
- Gambiarras no código de produção para contornar um serviço ausente.

## Quando usar

- Quando a aplicação depende de serviços de terceiros ou remotos fora do controle da equipe.
- Quando se quer testes rápidos e repetíveis no fluxo de desenvolvimento e na integração contínua.
- Quando é preciso simular cenários difíceis de provocar no serviço real (erros, lentidão, dados específicos).

## Quando evitar

- Quando o serviço real é barato, rápido e estável, e testá-lo diretamente é viável.
- Como única forma de teste: o stub não garante que o contrato real continua válido (use também testes de contrato ou de integração).
- Quando o stub ficaria tão complexo que passaria a reimplementar o serviço.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Testes rápidos, previsíveis e independentes de rede | O stub pode divergir do comportamento do serviço real |
| Desenvolvimento destravado mesmo sem o serviço pronto | Mais código de apoio a manter |
| Permite simular falhas e casos de borda | Falsa sensação de segurança se o contrato não for verificado |
| Código de produção sem desvios para testes | Exige uma interface bem definida para trocar a implementação |

- **Acoplamento:** exige que o cliente dependa de uma interface, não de uma classe concreta.
- **Testabilidade:** é o principal ganho do padrão.
- **Complexidade:** baixa, desde que o stub seja apenas uma tabela de respostas em memória.

## Diagrama

```mermaid
classDiagram
    class TaxService {
        <<interface>>
        +rateFor(region)
    }
    class RemoteTaxService {
        +rateFor(region)
    }
    class TaxServiceStub {
        +rateFor(region)
    }
    class CheckoutService
    CheckoutService --> TaxService
    TaxService <|.. RemoteTaxService
    TaxService <|.. TaxServiceStub
```

O `CheckoutService` depende da interface `TaxService`. Em produção usa o `RemoteTaxService`; nos testes, o `TaxServiceStub`, que responde em memória.

## Exemplo

Um checkout calcula imposto consultando um serviço remoto. Nos testes, um stub devolve alíquotas fixas.

```java
interface TaxService {
    java.math.BigDecimal rateFor(String region);
}

class TaxServiceStub implements TaxService {
    private final java.util.Map<String, java.math.BigDecimal> rates = java.util.Map.of(
        "SP", new java.math.BigDecimal("0.18"),
        "RJ", new java.math.BigDecimal("0.20"));

    public java.math.BigDecimal rateFor(String region) {
        return rates.getOrDefault(region, java.math.BigDecimal.ZERO);
    }
}

class CheckoutService {
    private final TaxService taxService;
    CheckoutService(TaxService taxService) { this.taxService = taxService; }

    java.math.BigDecimal total(java.math.BigDecimal net, String region) {
        return net.add(net.multiply(taxService.rateFor(region)));
    }
}

// Teste
var checkout = new CheckoutService(new TaxServiceStub());
// checkout.total(new BigDecimal("100"), "SP") -> 118.00
```

Ferramentas como WireMock, MockServer e bibliotecas de mock produzem stubs sem escrevê-los à mão.

## Padrões relacionados

- [Gateway](/design/poeaa/base/gateway) — o Gateway encapsula o serviço externo; o Service Stub é a implementação de teste desse Gateway.
- [Separated Interface](/design/poeaa/base/separated-interface) — fornece a interface que permite trocar o serviço real pelo stub.
- [Plugin](/design/poeaa/base/plugin) — escolhe, por configuração, entre o serviço real e o stub conforme o ambiente.
- [Null Object](/coding/gof/behavioral/null-object) — também é uma implementação alternativa de uma interface, mas voltada a representar ausência, e não a simular um serviço em testes.
- [Proxy](/coding/gof/structural/proxy) — o stub ocupa o lugar do serviço real, mas sem delegar a ele.
- [Consumer-Driven Contract Test](/architecture/microservices/testing/consumer-driven-contract-test) — complementa o stub, verificando que ele continua fiel ao contrato real.

## Referência

- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/serviceStub.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
