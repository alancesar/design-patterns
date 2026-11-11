---
title: Service Layer
pattern_slug: service-layer
category: Domain Logic
tags:
  - Decoupling
  - Consistency
  - Testability
source: https://martinfowler.com/eaaCatalog/serviceLayer.html
sidebar_label: "Service Layer"
---

# Service Layer

## Descrição

O Service Layer define a fronteira de uma aplicação como um conjunto de serviços que expõem as operações disponíveis e coordenam as respostas. Ele fica entre os clientes (interface web, API, carga de dados, mensageria) e a lógica de domínio.

Aplicações corporativas têm várias interfaces para os mesmos dados e regras, e todas precisam das mesmas interações, que podem envolver várias transações e recursos. Sem uma camada comum, essa orquestração é duplicada em cada interface.

O Service Layer encapsula a coordenação do caso de uso, controla transações e segurança, e delega as regras de negócio ao domínio. Pode ser fino (apenas orquestra) ou carregar parte da lógica de aplicação, mas as regras centrais ficam no Domain Model.

## Problemas que resolve

- Lógica de coordenação duplicada entre interfaces diferentes (web, API, jobs).
- Controle de transação e segurança espalhado pelos controladores.
- Clientes acoplados diretamente ao modelo de domínio e à persistência.
- Dificuldade de testar casos de uso sem passar pela interface.

## Quando usar

- Quando a aplicação tem mais de um tipo de cliente que executa as mesmas operações.
- Quando casos de uso envolvem várias etapas, transações ou recursos.
- Quando se quer um ponto único para transação, autorização e eventos.

## Quando evitar

- Aplicações simples com um único cliente e lógica trivial, em que a camada só repassa chamadas.
- Quando serviços acumulam regras de negócio e esvaziam o domínio (modelo anêmico).
- Quando a camada vira um "god object" de operações não relacionadas.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Orquestração em um só lugar, reutilizada por todos os clientes | Camada extra que pode ser só indireção |
| Fronteira transacional clara | Risco de concentrar regras e gerar modelo anêmico |
| Domínio isolado de interfaces e persistência | Serviços podem crescer demais |
| Casos de uso testáveis sem interface | Exige disciplina para manter a camada fina |

- **Consistência:** a transação por operação garante que o caso de uso seja atômico.
- **Acoplamento:** os clientes dependem dos serviços, não do modelo.
- **Variantes:** a camada pode ser de domain facade (fina) ou de operation script (com lógica de aplicação).

## Diagrama

```mermaid
sequenceDiagram
    participant UI as Cliente (API do app, job de agendadas)
    participant S as PixTransferService
    participant D as Domain Model
    participant R as Repositorio
    UI->>S: transfer(comando)
    S->>S: abre transacao
    S->>R: carrega Account
    S->>D: account.sendPix(pixKey, amount)
    S->>R: salva PixTransfer
    S->>S: confirma transacao
    S-->>UI: resultado
```

O serviço abre a transação, carrega objetos, delega a regra ao domínio, persiste o resultado e devolve a resposta ao cliente.

## Exemplo

Um `PixTransferService` é usado tanto pela API do app quanto pelo job de transferências agendadas, concentrando transação e orquestração.

```java
@Service
public class PixTransferService {
    private final AccountRepository accounts;
    private final PixTransferRepository transfers;
    private final SpiGateway spi;

    @Transactional
    public PixTransferId transfer(SendPixCommand cmd) {
        Account account = accounts.get(cmd.accountId());
        PixTransfer transfer = account.sendPix(cmd.pixKey(), cmd.amount());   // regra no domínio
        transfers.save(transfer);
        // em produção, o envio ao SPI acontece após o commit (por exemplo, via outbox)
        spi.submit(transfer.endToEndId(), transfer.amount());
        return transfer.id();
    }
}
```

No Spring, serviços anotados com `@Service` e `@Transactional` são a forma comum desse padrão.

## Padrões relacionados

- [Domain Model](/design/poeaa/domain-logic/domain-model) — o Service Layer coordena o modelo, que contém as regras.
- [Transaction Script](/design/poeaa/domain-logic/transaction-script) — pode ser a implementação dos serviços quando a lógica é simples.
- [Table Module](/design/poeaa/domain-logic/table-module) — também pode ficar atrás da camada de serviço.
- [Remote Facade](/design/poeaa/distribution/remote-facade) — fachada de granularidade grossa para acesso remoto, geralmente sobre o Service Layer.
- [Repository](/design/poeaa/object-relational-metadata-mapping/repository) — usado pelos serviços para obter e salvar agregados.
- [Facade](/coding/gof/structural/facade) — o Service Layer é uma fachada para as operações da aplicação.

## Referência

- [Página do padrão no catálogo do Fowler](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- *Patterns of Enterprise Application Architecture*, Martin Fowler (Addison-Wesley, 2002)
