---
title: State Creation Operation
pattern_slug: state-creation-operation
category: Operation Responsibilities
tags:
  - Decoupling
  - Performance
source: https://api-patterns.org/
sidebar_label: "State Creation Operation"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/operation-responsibilities/state-creation-operation.mdx';

# State Creation Operation

## Descrição

O padrão State Creation Operation é uma operação de API de natureza somente escrita, com a qual o cliente informa ao provedor que algo aconteceu, sem esperar dele nada além de uma confirmação de recebimento. Em termos de estado, ela grava (cria ou acrescenta dados) no lado do provedor, mas não depende de ler esse estado para responder.

A operação representa um único incidente de negócio: um pagamento recebido, um pedido concluído, uma carga em lote finalizada. O provedor pode simplesmente armazenar o relato ou disparar um processamento posterior, e o cliente recebe apenas um "recebido" ou um identificador para consultar depois. Como relatos podem chegar duplicados, fora de ordem ou se perder, cada incidente deve carregar um identificador único e, de preferência, o instante em que ocorreu segundo o relógio do cliente, para que o provedor detecte repetições e a operação pareça idempotente.

Uma variante comum é a Event Notification Operation, que só armazena o evento como veio (alinhada a event sourcing); outra é o Bulk Report, em que vários incidentes seguem juntos em um [Request Bundle](/architecture/api-patterns/message-exchange-optimization/request-bundle).

## Problemas que resolve

- Clientes que precisam avisar o provedor de algo que aconteceu sem se acoplar ao processamento interno que isso desencadeia
- Mistura de operações que escrevem e operações que só calculam no mesmo endpoint, o que dificulta balanceamento de carga e implantação
- Relatos duplicados ou reenviados após falhas de rede, que geram lançamentos repetidos
- Premissas implícitas sobre efeitos em estado, que deixam de valer sem que ninguém perceba

## Quando usar

- Para notificar eventos já ocorridos no cliente ou em outro sistema (um Pix recebido, uma compra aprovada)
- Para iniciar um processo de longa duração apenas registrando o pedido, como a abertura de uma contratação de crédito
- Para reportar a conclusão de uma carga em lote ou a ingestão de um conjunto de eventos em um data lake
- Quando o provedor precisa escalar a escrita e evitar ler estado a cada chamada

## Quando evitar

- Quando o cliente precisa de um resultado calculado a partir do estado atual: use uma operação de leitura ou de transição
- Quando é preciso validar invariantes complexas contra o estado existente antes de aceitar, pois a operação evita justamente essas leituras
- Quando a mudança depende de um estado anterior identificado na requisição: prefira uma [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation)
- Para apenas calcular algo sem guardar nada: use uma [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function)

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Baixo acoplamento: cliente e provedor não compartilham estado de aplicação | Verificações de consistência no provedor ficam difíceis, pois a operação evita ler estado |
| Escrita simples de escalar e de implantar separada das leituras | Relatos contraditórios ou fora de ordem exigem uma política explícita de tratamento |
| Resposta rápida, muitas vezes só uma confirmação | Sem confirmação ou identificador, o cliente não sabe se deve reenviar |
| Contrato claro sobre o efeito da chamada no estado | Reenvios exigem identificadores únicos e deduplicação para manter a idempotência |

- **Idempotência:** o identificador do incidente permite descartar repetições sem criar lançamentos duplicados.
- **Tempo:** o instante do cliente e o instante de chegada podem divergir; registre ambos quando a ordem importar.
- **Consistência:** defina se o relato é só armazenado, se é processado depois ou se altera o comportamento de outras operações.
- **Segurança:** quando exposta em uma [Public API](/architecture/api-patterns/foundations/public-api), proteja com [API Key](/architecture/api-patterns/special-purpose-representations/api-key) e [Rate Limit](/architecture/api-patterns/documentation/rate-limit).

## Diagrama

<Diagram />

O provedor só grava e confirma. Se o mesmo incidente chegar de novo, o identificador permite responder sem criar outro registro.

## Exemplo

O parceiro que processa liquidações Pix avisa a fintech de que um Pix foi recebido em uma conta. A fintech apenas registra o evento, e o saldo e o `LedgerEntry` correspondente são produzidos depois, de forma assíncrona.

```http
POST /pix-events HTTP/1.1
Content-Type: application/json

{
  "eventId": "evt-501",
  "type": "PixReceived",
  "accountId": "acc-42",
  "amountCents": 15000,
  "occurredAt": "2026-11-03T14:21:07-03:00"
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{ "eventId": "evt-501", "status": "RECEIVED" }
```

Um reenvio com o mesmo `eventId` devolve `"status": "ALREADY_RECEIVED"` e não grava nada novo. O código abaixo mostra o núcleo da operação.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        PixEventProcessor processor = new PixEventProcessor();
        PixReceivedEvent event = new PixReceivedEvent("evt-501", "acc-42", 15_000);
        System.out.println(processor.informAbout(event)); // RECEIVED
        System.out.println(processor.informAbout(event)); // ALREADY_RECEIVED
    }
}

record PixReceivedEvent(String eventId, String accountId, long amountCents) {}

class PixEventProcessor {
    private final Map<String, PixReceivedEvent> store = new LinkedHashMap<>();

    // Só grava, sem ler o estado de negócio. Repetir o eventId é inofensivo.
    String informAbout(PixReceivedEvent event) {
        return store.putIfAbsent(event.eventId(), event) == null
                ? "RECEIVED" : "ALREADY_RECEIVED";
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PixReceivedEvent:
    event_id: str
    account_id: str
    amount_cents: int

class PixEventProcessor:
    def __init__(self) -> None:
        self._store = {}

    # Só grava, sem ler o estado de negócio. Repetir o event_id é inofensivo.
    def inform_about(self, event: PixReceivedEvent) -> str:
        if event.event_id in self._store:
            return "ALREADY_RECEIVED"
        self._store[event.event_id] = event
        return "RECEIVED"

processor = PixEventProcessor()
event = PixReceivedEvent("evt-501", "acc-42", 15_000)
print(processor.inform_about(event))  # RECEIVED
print(processor.inform_about(event))  # ALREADY_RECEIVED
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
)

type PixReceivedEvent struct {
	EventID     string
	AccountID   string
	AmountCents int64
}

type PixEventProcessor struct {
	store map[string]PixReceivedEvent
}

// Só grava, sem ler o estado de negócio. Repetir o EventID é inofensivo.
func (p *PixEventProcessor) InformAbout(event PixReceivedEvent) string {
	if _, seen := p.store[event.EventID]; seen {
		return "ALREADY_RECEIVED"
	}
	p.store[event.EventID] = event
	return "RECEIVED"
}

func main() {
	processor := &PixEventProcessor{store: map[string]PixReceivedEvent{}}
	event := PixReceivedEvent{"evt-501", "acc-42", 15_000}
	fmt.Println(processor.InformAbout(event)) // RECEIVED
	fmt.Println(processor.InformAbout(event)) // ALREADY_RECEIVED
}
```

</TabItem>
</Tabs>

## Padrões relacionados

- [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) — lê e escreve o estado e normalmente identifica o elemento a alterar; a State Creation Operation só escreve
- [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — o oposto: lê o estado sem escrever, puxando dados em vez de empurrá-los
- [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) — não lê nem escreve estado
- [Processing Resource](/architecture/api-patterns/endpoint-roles/processing-resource) e [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — os endpoints que costumam hospedar a operação
- [Id Element](/architecture/api-patterns/element-stereotypes/id-element) — o identificador do evento e o devolvido na confirmação
- [Error Report](/architecture/api-patterns/special-purpose-representations/error-report) — formato comum para a resposta quando o relato é rejeitado
- [Domain Event](/architecture/microservices/service-collaboration/domain-event) — ajuda a identificar essas operações, em especial na variante de notificação de evento
- [Event Message](/architecture/eip/message-construction/event-message) — a mensagem de evento do EIP que a variante Event Notification Operation expõe por API
- [Idempotent Consumer](/architecture/cloud-design-patterns/messaging/idempotent-consumer) — técnica para processar o mesmo relato mais de uma vez com segurança

## Referência

- [Patterns for API Design, capítulo 5: State Creation Operation](https://api-patterns.org/)
