---
title: Decorator
pattern_slug: decorator
category: Structural
tags:
  - Extensibility
  - Runtime Flexibility
origin: GoF
source: https://iretha.github.io/design-patterns/cheat-sheet
sidebar_label: "Decorator"
mdx:
  format: mdx
---

# Decorator

## Descrição

O Decorator permite adicionar responsabilidades a um objeto de forma dinâmica, em tempo de execução, sem alterar sua classe e sem recorrer à herança. Ele oferece uma alternativa flexível à criação de subclasses para estender funcionalidades.

A ideia é "embrulhar" o objeto original em outro objeto (o decorador) que implementa a mesma interface. O decorador mantém uma referência ao componente embrulhado, delega a ele as chamadas e acrescenta comportamento antes ou depois dessa delegação. Como o decorador tem a mesma interface do componente, o cliente não percebe a diferença.

Decoradores podem ser empilhados: cada camada adiciona um comportamento, e a ordem de composição determina o resultado final. Isso permite combinar funcionalidades livremente, em vez de criar uma subclasse para cada combinação possível.

## Problemas que resolve

- Explosão de subclasses para representar todas as combinações de funcionalidades opcionais (ex.: `CompressedEncryptedBufferedStream`).
- Necessidade de adicionar ou remover comportamento de objetos individuais em tempo de execução, sem afetar outras instâncias da mesma classe.
- Estender classes que não podem ser modificadas ou herdadas (ex.: classes `final`/`sealed` ou de bibliotecas de terceiros).
- Separar preocupações transversais (log, cache, métricas, retry) da lógica principal.

## Quando usar

- Quando é preciso adicionar responsabilidades a objetos de forma transparente e dinâmica.
- Quando as extensões são opcionais e combináveis entre si.
- Quando a herança é impraticável, seja por gerar muitas subclasses, seja por a classe não permitir extensão.
- Para aplicar comportamentos transversais (logging, cache, autorização, compressão) mantendo o Single Responsibility Principle.

## Quando evitar

- Quando o cliente depende da identidade ou do tipo concreto do objeto (o decorador é um objeto diferente do componente embrulhado).
- Quando a interface do componente é muito extensa, obrigando cada decorador a delegar dezenas de métodos.
- Quando há apenas uma extensão fixa e estável, em que uma subclasse simples ou uma alteração direta é mais clara.
- Quando a ordem dos decoradores importa muito e é difícil de controlar, gerando comportamentos inesperados.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Estende comportamento sem modificar a classe original (Open/Closed) | Muitos objetos pequenos e parecidos, dificultando a leitura |
| Combina funcionalidades em tempo de execução | A ordem de empilhamento afeta o resultado e pode gerar bugs sutis |
| Evita explosão de subclasses | Comparações de identidade e checagens de tipo deixam de funcionar |
| Cada decorador tem uma única responsabilidade | Depuração mais difícil por causa das várias camadas de delegação |

- **Acoplamento:** baixo; decoradores dependem apenas da interface do componente.
- **Testabilidade:** alta; cada decorador pode ser testado isoladamente com um componente falso.
- **Complexidade:** a montagem da cadeia costuma ser delegada a uma factory ou a um container de injeção de dependência.
- **Desempenho:** cada camada acrescenta uma chamada indireta, geralmente com custo desprezível.

## Diagrama

```mermaid
classDiagram
    class Component {
        <<interface>>
        +operation()
    }
    class ConcreteComponent {
        +operation()
    }
    class Decorator {
        <<abstract>>
        -component: Component
        +operation()
    }
    class ConcreteDecoratorA {
        +operation()
        +addedBehavior()
    }
    class ConcreteDecoratorB {
        -addedState
        +operation()
    }
    class Client
    Component <|.. ConcreteComponent
    Component <|.. Decorator
    Decorator o-- Component : wraps
    Decorator <|-- ConcreteDecoratorA
    Decorator <|-- ConcreteDecoratorB
    Client --> Component
```

`Component` define a interface comum; `ConcreteComponent` é o objeto base. `Decorator` implementa a mesma interface e guarda uma referência a um `Component`, delegando a ele as chamadas; `ConcreteDecoratorA` e `ConcreteDecoratorB` acrescentam comportamento antes ou depois dessa delegação. O `Client` trabalha apenas com `Component`.

## Exemplo

O serviço de transferência básico só movimenta o dinheiro. Antifraude, limite noturno e trilha de auditoria são camadas empilhadas conforme o tipo de conta, em vez de uma subclasse para cada combinação. Os limites são ilustrativos.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
record TransferRequest(String fromAccountId, String toKey, long amountCents, LocalDateTime at) {}

interface TransferService {
    void transfer(TransferRequest request);
}

class BasicTransferService implements TransferService {
    public void transfer(TransferRequest request) {
        System.out.println("Transferindo " + request.amountCents() + " -> " + request.toKey());
    }
}

abstract class TransferDecorator implements TransferService {
    protected final TransferService wrapped;

    TransferDecorator(TransferService wrapped) { this.wrapped = wrapped; }

    public void transfer(TransferRequest request) {
        wrapped.transfer(request);
    }
}

class FraudCheckDecorator extends TransferDecorator {
    FraudCheckDecorator(TransferService wrapped) { super(wrapped); }

    @Override
    public void transfer(TransferRequest request) {
        if (request.amountCents() > 5_000_000) throw new IllegalStateException("Bloqueado pelo antifraude");
        super.transfer(request);
    }
}

class NightLimitDecorator extends TransferDecorator {
    NightLimitDecorator(TransferService wrapped) { super(wrapped); }

    @Override
    public void transfer(TransferRequest request) {
        int hour = request.at().getHour();
        boolean isNight = hour >= 20 || hour < 6;
        if (isNight && request.amountCents() > 100_000) throw new IllegalStateException("Limite noturno excedido");
        super.transfer(request);
    }
}

class AuditDecorator extends TransferDecorator {
    AuditDecorator(TransferService wrapped) { super(wrapped); }

    @Override
    public void transfer(TransferRequest request) {
        System.out.println("Audit: " + request.fromAccountId() + " transfere " + request.amountCents());
        super.transfer(request);
    }
}

TransferService service = new AuditDecorator(
    new NightLimitDecorator(new FraudCheckDecorator(new BasicTransferService())));
service.transfer(new TransferRequest(
    "acc-1", "ana@example.com", 50_000, LocalDateTime.of(2026, 3, 10, 23, 30)));
// auditoria, limite noturno e antifraude aprovam; R$ 500,00 transferidos
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

@dataclass(frozen=True)
class TransferRequest:
    from_account_id: str
    to_key: str
    amount_cents: int
    at: datetime

class TransferService(Protocol):
    def transfer(self, request: TransferRequest) -> None: ...

class BasicTransferService:
    def transfer(self, request: TransferRequest) -> None:
        print(f"Transferindo {request.amount_cents} -> {request.to_key}")

class TransferDecorator:
    def __init__(self, wrapped: TransferService) -> None:
        self._wrapped = wrapped

    def transfer(self, request: TransferRequest) -> None:
        self._wrapped.transfer(request)

class FraudCheckDecorator(TransferDecorator):
    def transfer(self, request: TransferRequest) -> None:
        if request.amount_cents > 5_000_000:
            raise PermissionError("Bloqueado pelo antifraude")
        super().transfer(request)

class NightLimitDecorator(TransferDecorator):
    def transfer(self, request: TransferRequest) -> None:
        is_night = request.at.hour >= 20 or request.at.hour < 6
        if is_night and request.amount_cents > 100_000:
            raise PermissionError("Limite noturno excedido")
        super().transfer(request)

class AuditDecorator(TransferDecorator):
    def transfer(self, request: TransferRequest) -> None:
        print(f"Audit: {request.from_account_id} transfere {request.amount_cents}")
        super().transfer(request)

service: TransferService = AuditDecorator(
    NightLimitDecorator(FraudCheckDecorator(BasicTransferService()))
)
service.transfer(TransferRequest("acc-1", "ana@example.com", 50_000, datetime(2026, 3, 10, 23, 30)))
# auditoria, limite noturno e antifraude aprovam; R$ 500,00 transferidos
```

</TabItem>
<TabItem value="go" label="Go">

```go
type TransferRequest struct {
	FromAccountID string
	ToKey         string
	AmountCents   int64
	At            time.Time
}

type TransferService interface {
	Transfer(request TransferRequest) error
}

type BasicTransferService struct{}

func (BasicTransferService) Transfer(request TransferRequest) error {
	fmt.Printf("Transferindo %d -> %s\n", request.AmountCents, request.ToKey)
	return nil
}

// Cada decorador implementa TransferService e embrulha outro TransferService.
type FraudCheckDecorator struct{ Wrapped TransferService }

func (d FraudCheckDecorator) Transfer(request TransferRequest) error {
	if request.AmountCents > 5_000_000 {
		return errors.New("bloqueado pelo antifraude")
	}
	return d.Wrapped.Transfer(request)
}

type NightLimitDecorator struct{ Wrapped TransferService }

func (d NightLimitDecorator) Transfer(request TransferRequest) error {
	hour := request.At.Hour()
	isNight := hour >= 20 || hour < 6
	if isNight && request.AmountCents > 100_000 {
		return errors.New("limite noturno excedido")
	}
	return d.Wrapped.Transfer(request)
}

type AuditDecorator struct{ Wrapped TransferService }

func (d AuditDecorator) Transfer(request TransferRequest) error {
	fmt.Printf("Audit: %s transfere %d\n", request.FromAccountID, request.AmountCents)
	return d.Wrapped.Transfer(request)
}

func main() {
	var service TransferService = AuditDecorator{
		NightLimitDecorator{FraudCheckDecorator{BasicTransferService{}}},
	}
	err := service.Transfer(TransferRequest{
		FromAccountID: "acc-1",
		ToKey:         "ana@example.com",
		AmountCents:   50_000,
		At:            time.Date(2026, 3, 10, 23, 30, 0, 0, time.Local),
	}) // auditoria, limite noturno e antifraude aprovam; R$ 500,00 transferidos
	if err != nil {
		fmt.Println(err)
	}
}
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
interface TransferRequest {
  fromAccountId: string;
  toKey: string;
  amountCents: number;
  at: Date;
}

interface TransferService {
  transfer(request: TransferRequest): void;
}

class BasicTransferService implements TransferService {
  transfer(request: TransferRequest): void {
    console.log(`Transferindo ${request.amountCents} -> ${request.toKey}`);
  }
}

abstract class TransferDecorator implements TransferService {
  constructor(protected wrapped: TransferService) {}
  transfer(request: TransferRequest): void {
    this.wrapped.transfer(request);
  }
}

class FraudCheckDecorator extends TransferDecorator {
  transfer(request: TransferRequest): void {
    if (request.amountCents > 5_000_000) throw new Error("Bloqueado pelo antifraude");
    super.transfer(request);
  }
}

class NightLimitDecorator extends TransferDecorator {
  transfer(request: TransferRequest): void {
    const hour = request.at.getHours();
    const isNight = hour >= 20 || hour < 6;
    if (isNight && request.amountCents > 100_000) throw new Error("Limite noturno excedido");
    super.transfer(request);
  }
}

class AuditDecorator extends TransferDecorator {
  transfer(request: TransferRequest): void {
    console.log(`Audit: ${request.fromAccountId} transfere ${request.amountCents}`);
    super.transfer(request);
  }
}

const service: TransferService = new AuditDecorator(
  new NightLimitDecorator(new FraudCheckDecorator(new BasicTransferService())),
);
service.transfer({
  fromAccountId: "acc-1",
  toKey: "ana@example.com",
  amountCents: 50_000,
  at: new Date("2026-03-10T23:30:00"),
}); // auditoria, limite noturno e antifraude aprovam; R$ 500,00 transferidos
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Adapter](/coding/gof/structural/adapter) — o Adapter altera a interface de um objeto; o Decorator mantém a interface e acrescenta responsabilidades.
- [Composite](/coding/gof/structural/composite) — estrutura semelhante (composição recursiva), mas o Decorator tem um único filho e foca em adicionar comportamento, não em agregar resultados.
- [Proxy](/coding/gof/structural/proxy) — mesma estrutura de embrulho, mas o Proxy controla o acesso ao objeto e normalmente gerencia seu ciclo de vida, enquanto o Decorator é composto pelo cliente para estender comportamento.
- [Strategy](/coding/gof/behavioral/strategy) — o Decorator muda a "casca" do objeto; o Strategy muda suas "entranhas", trocando o algoritmo interno.
- [Chain of Responsibility](/coding/gof/behavioral/chain-of-responsibility) — também encadeia objetos, mas um elo pode interromper o fluxo, enquanto decoradores normalmente sempre delegam.

## Referência

- [Design Patterns Cheat Sheet](https://iretha.github.io/design-patterns/cheat-sheet)
- [Decorator no Refactoring.Guru](https://refactoring.guru/design-patterns/decorator)
