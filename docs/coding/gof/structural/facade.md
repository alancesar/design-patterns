---
title: Facade
pattern_slug: facade
category: Structural
tags:
  - Simplicity
  - Decoupling
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Facade"
---

# Facade

## Descrição

O Facade oferece uma interface única e simplificada para um conjunto de interfaces de um subsistema. Em vez de o cliente conhecer e coordenar várias classes internas, ele conversa com um único objeto de fachada que expõe operações de alto nível.

A fachada sabe quais classes do subsistema são responsáveis por cada pedido e delega o trabalho a elas, na ordem correta. As classes do subsistema continuam funcionando de forma independente e não conhecem a fachada; clientes avançados ainda podem acessá-las diretamente quando precisarem de mais controle.

O resultado é uma camada que reduz o acoplamento entre clientes e detalhes de implementação, facilitando o uso, a manutenção e a evolução do subsistema.

## Problemas que resolve

- Clientes precisam orquestrar muitas classes de baixo nível (bibliotecas, frameworks, APIs legadas) para executar uma tarefa simples.
- Mudanças internas em um subsistema se propagam para todo o código que o utiliza.
- Dependências complexas entre camadas dificultam entender o ponto de entrada de um módulo.
- Código de integração repetido em vários lugares para realizar a mesma sequência de chamadas.

## Quando usar

- Quando se quer fornecer uma interface simples para um subsistema complexo.
- Para estruturar um sistema em camadas, definindo um ponto de entrada para cada uma.
- Para isolar o código cliente de bibliotecas de terceiros ou sistemas legados, facilitando substituí-los.
- Quando há muitas dependências entre clientes e classes de implementação e se deseja desacoplá-los.

### Quando evitar

- Quando o subsistema já é simples; a fachada só adicionaria uma camada desnecessária.
- Quando os clientes precisam de todo o poder e flexibilidade do subsistema e a fachada acabaria replicando toda a sua API.
- Quando a fachada tende a virar um "god object", acumulando responsabilidades não relacionadas.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Interface simples e fácil de usar | Pode esconder funcionalidades úteis ou limitar casos avançados |
| Menor acoplamento entre clientes e subsistema | Mais uma camada de indireção para manter |
| Mudanças internas ficam isoladas atrás da fachada | Risco de a fachada crescer demais e virar um "god object" |
| Ponto de entrada claro para camadas e módulos | Pode mascarar problemas de design no subsistema em vez de resolvê-los |

- **Acoplamento:** o cliente depende apenas da fachada, mas a fachada fica acoplada a várias classes do subsistema.
- **Testabilidade:** clientes ficam fáceis de testar com um dublê da fachada; a própria fachada exige testes de integração ou mocks dos componentes.
- **Complexidade:** baixa; o padrão não exige herança nem interfaces especiais.
- **Desempenho:** impacto desprezível, apenas uma chamada a mais de delegação.

## Diagrama

```mermaid
classDiagram
    class Client
    class Facade {
        +operation()
    }
    class SubsystemA {
        +operationA()
    }
    class SubsystemB {
        +operationB()
    }
    class SubsystemC {
        +operationC()
    }
    Client --> Facade
    Facade --> SubsystemA
    Facade --> SubsystemB
    Facade --> SubsystemC
```

O `Client` interage apenas com a `Facade`, que delega as chamadas para `SubsystemA`, `SubsystemB` e `SubsystemC` na ordem adequada. As classes do subsistema não conhecem a fachada.

## Exemplo

Um e-commerce precisa finalizar pedidos verificando estoque, cobrando o pagamento e agendando a entrega. Em vez de cada controlador coordenar esses três serviços, um `OrderFacade` expõe uma única operação `placeOrder`.

```typescript
class InventoryService {
  reserve(sku: string, qty: number): void { /* ... */ }
}

class PaymentService {
  charge(customerId: string, amount: number): string { return "tx-123"; }
}

class ShippingService {
  schedule(customerId: string, sku: string): string { return "track-456"; }
}

class OrderFacade {
  constructor(
    private inventory = new InventoryService(),
    private payment = new PaymentService(),
    private shipping = new ShippingService(),
  ) {}

  placeOrder(customerId: string, sku: string, qty: number, amount: number): string {
    this.inventory.reserve(sku, qty);
    this.payment.charge(customerId, amount);
    return this.shipping.schedule(customerId, sku);
  }
}

// Cliente
const tracking = new OrderFacade().placeOrder("c-1", "SKU-9", 2, 199.9);
```

## Padrões relacionados

- [Adapter](./adapter.md) — o Adapter converte uma interface existente para outra esperada; o Facade cria uma interface nova e mais simples para um conjunto de classes.
- [Mediator](../behavioral/mediator.md) — ambos centralizam a comunicação, mas o Mediator coordena colegas que o conhecem, enquanto o Facade é transparente para o subsistema.
- [Abstract Factory](../creational/abstract-factory.md) — pode ser usado junto com o Facade para criar os objetos do subsistema de forma independente de plataforma.
- [Singleton](../creational/singleton.md) — frequentemente basta uma única instância da fachada.
- [Proxy](./proxy.md) — também se interpõe entre cliente e objeto real, mas mantém a mesma interface em vez de simplificá-la.

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Facade no Refactoring.Guru](https://refactoring.guru/design-patterns/facade)
