---
title: Bridge
pattern_slug: bridge
category: Structural
tags:
  - Decoupling
  - Extensibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Bridge"
---

# Bridge

## Descrição

O Bridge desacopla uma abstração da sua implementação para que ambas possam variar de forma independente. Em vez de criar uma hierarquia única que combina todas as variações (por exemplo, `WindowsCircle`, `LinuxCircle`, `WindowsSquare`...), o padrão separa o problema em duas hierarquias: a da **abstração** (o que o cliente usa) e a do **implementador** (como o trabalho de baixo nível é feito).

A abstração mantém uma referência para um objeto implementador e delega a ele as operações primitivas. Novas abstrações refinadas e novas implementações concretas podem ser adicionadas sem que uma afete a outra, e a implementação pode até ser trocada em tempo de execução.

Na prática, o Bridge troca herança por composição: a "ponte" é justamente a referência da abstração para a interface do implementador.

## Problemas que resolve

- Explosão combinatória de subclasses quando duas dimensões de variação (ex.: forma e plataforma de renderização) são modeladas em uma única hierarquia.
- Acoplamento permanente entre a abstração e uma implementação específica definido em tempo de compilação.
- Mudanças na implementação que forçam recompilação ou alteração do código cliente.
- Dificuldade de compartilhar uma mesma implementação entre várias abstrações.

## Quando usar

- Quando uma classe varia em duas (ou mais) dimensões ortogonais que devem evoluir de forma independente.
- Quando é necessário escolher ou trocar a implementação em tempo de execução (ex.: driver, backend de armazenamento, canal de envio).
- Quando se quer esconder detalhes de implementação dependentes de plataforma do código cliente.
- Ao projetar bibliotecas multiplataforma ou drivers (JDBC, renderizadores gráficos, provedores de nuvem).

### Quando evitar

- Quando existe apenas uma implementação e não há perspectiva real de outras; a indireção vira complexidade gratuita.
- Quando as duas dimensões não são de fato independentes e a abstração precisa conhecer detalhes de cada implementação.
- Em código pequeno e estável, onde uma hierarquia simples ou um Strategy pontual resolve.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Abstração e implementação evoluem independentemente | Mais classes e interfaces para entender |
| Evita explosão de subclasses (N + M em vez de N x M) | Indireção extra a cada chamada delegada |
| Implementação trocável em tempo de execução | Exige identificar as dimensões corretas logo no design |
| Respeita Open/Closed e Single Responsibility | A interface do implementador pode ficar genérica demais (menor denominador comum) |

- **Acoplamento:** o cliente depende apenas da abstração; implementações ficam isoladas.
- **Testabilidade:** o implementador pode ser substituído por um dublê de teste facilmente.
- **Complexidade:** costuma ser decidido no início do projeto; aplicá-lo depois exige refatoração significativa.
- **Desempenho:** custo de uma chamada indireta, normalmente desprezível.

## Diagrama

```mermaid
classDiagram
    class Abstraction {
        -Implementor impl
        +operation()
    }
    class RefinedAbstraction {
        +operation()
    }
    class Implementor {
        <<interface>>
        +operationImpl()
    }
    class ConcreteImplementorA {
        +operationImpl()
    }
    class ConcreteImplementorB {
        +operationImpl()
    }
    class Client
    Client --> Abstraction
    Abstraction <|-- RefinedAbstraction
    Abstraction o-- Implementor : impl
    Implementor <|.. ConcreteImplementorA
    Implementor <|.. ConcreteImplementorB
```

`Abstraction` define a interface usada pelo `Client` e mantém uma referência para um `Implementor`; `RefinedAbstraction` estende essa interface. `Implementor` declara as operações primitivas, realizadas por `ConcreteImplementorA` e `ConcreteImplementorB`.

## Exemplo

Um sistema de notificações tem tipos de mensagem (alerta, lembrete) e canais de envio (e-mail, SMS). Com Bridge, cada tipo de mensagem delega o envio a um canal, evitando classes como `EmailAlert` e `SmsReminder`.

```typescript
interface MessageSender {
  send(to: string, body: string): void;
}

class EmailSender implements MessageSender {
  send(to: string, body: string) { console.log(`Email to ${to}: ${body}`); }
}

class SmsSender implements MessageSender {
  send(to: string, body: string) { console.log(`SMS to ${to}: ${body}`); }
}

abstract class Notification {
  constructor(protected sender: MessageSender) {}
  abstract notify(to: string, text: string): void;
}

class AlertNotification extends Notification {
  notify(to: string, text: string) { this.sender.send(to, `[ALERT] ${text}`); }
}

class ReminderNotification extends Notification {
  notify(to: string, text: string) { this.sender.send(to, `Reminder: ${text}`); }
}

new AlertNotification(new SmsSender()).notify("+5511999999999", "CPU at 95%");
new ReminderNotification(new EmailSender()).notify("ana@example.com", "Meeting at 3pm");
```

## Padrões relacionados

- [Adapter](/coding/gof/structural/adapter) — também envolve indireção entre interfaces, mas o Adapter é aplicado depois para compatibilizar classes existentes; o Bridge é planejado de antemão.
- [Abstract Factory](/coding/gof/creational/abstract-factory) — pode criar e configurar o par abstração/implementador adequado, escondendo a escolha da implementação concreta.
- [Strategy](/coding/gof/behavioral/strategy) — estrutura semelhante (composição + delegação), mas o Strategy foca em trocar algoritmos, enquanto o Bridge separa duas hierarquias estruturais.
- [State](/coding/gof/behavioral/state) — também delega comportamento a um objeto composto, porém a troca é dirigida pelo estado interno.
- [Builder](/coding/gof/creational/builder) — pode ser combinado com Bridge: o diretor atua como abstração e os builders como implementações.

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Bridge no Refactoring.Guru](https://refactoring.guru/design-patterns/bridge)
