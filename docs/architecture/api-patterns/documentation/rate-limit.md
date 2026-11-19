---
title: Rate Limit
pattern_slug: rate-limit
category: Documentation
tags:
  - Performance
  - Security
source: https://api-patterns.org/
sidebar_label: "Rate Limit"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/documentation/rate-limit.mdx';

# Rate Limit

## Descrição

O padrão Rate Limit protege uma API contra o uso excessivo ao definir e comunicar um número máximo de requisições que cada cliente pode fazer em uma janela de tempo, rejeitando, adiando ou degradando as que passarem do limite.

O limite pode valer para a API inteira, para um endpoint ou para um grupo de operações, e nem toda chamada precisa pesar o mesmo: operações caras podem consumir mais unidades que uma simples leitura. A janela (por minuto, dia ou mês) pode ser fixa, com reinício periódico, ou deslizante. O limite também pode restringir a concorrência, por exemplo uma única requisição simultânea no plano gratuito. Ao estourar a cota, o provedor pode recusar as chamadas (em HTTP, com o status 429 Too Many Requests), atender com menos recursos, deixar para o próximo período ou oferecer um plano maior. Clientes que reincidem podem ter a chave suspensa.

Para medir e aplicar o limite, o provedor precisa identificar o cliente, normalmente por uma [API Key](/architecture/api-patterns/special-purpose-representations/api-key) ou por autenticação, ou, em serviços abertos, pelo endereço IP. Clientes responsáveis acompanham a cota restante, o que o provedor facilita ao informar o estado do limite nas respostas, por exemplo em cabeçalhos HTTP.

## Problemas que resolve

- Clientes, por abuso ou por erro, que consomem capacidade e degradam o serviço para os demais
- Rajadas que esgotam a cota mensal em minutos e sobrecarregam o provedor
- Custo de infraestrutura crescente sem proporção com a receita
- Falta de transparência para o cliente sobre quanto ainda pode usar

## Quando usar

- Em APIs públicas ou de parceiros com capacidade compartilhada entre muitos clientes
- Quando há planos com níveis de uso diferentes e é preciso fazer valer a diferença
- Quando o impacto de um cliente abusivo, deliberado ou acidental, é alto o bastante para justificar o custo da medida
- Para proteger operações caras, como geração de extratos ou consulta de score

## Quando evitar

- Quando o risco de abuso é baixo e o custo de implementar e comunicar limites supera o benefício
- Quando limites agressivos afastariam clientes importantes sem proteger nada de relevante
- Em APIs internas confiáveis, em que outras formas de controle de carga bastam
- Quando o provedor não consegue identificar o cliente, pois então o limite pune quem compartilha um IP

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Proteção da qualidade do serviço para todos os clientes | Calibrar o limite exige experimentação: alto demais não protege, baixo demais irrita |
| Capacidade mais previsível e custo sob controle | A API passa a ter estado (contadores), o que afeta a escala horizontal |
| Base técnica para diferenciar planos de preço | Clientes precisam tratar o limite: reenviar com espera, enfileirar, priorizar |
| Defesa contra bots e uso malicioso | Custo de manter e monitorar a medição por cliente |

- **Janela:** a janela fixa é simples, mas permite uma rajada dupla na virada; janelas deslizantes ou token bucket suavizam isso, ao custo de mais estado.
- **Estado distribuído:** com várias instâncias, os contadores precisam ficar em um armazenamento compartilhado ou ser aproximados por instância.
- **Comunicação:** informe limite, restante e reinício nas respostas para que o cliente se ajuste sozinho.
- **Combinação:** um limite mensal costuma vir com um limite por segundo, para evitar que a cota inteira seja gasta de uma vez.

## Diagrama

<Diagram />

O gateway conta as chamadas por cliente em cada janela, deixa passar as que cabem na cota e responde 429 às demais, informando quando tentar de novo.

## Exemplo

A API de cobranças Pix da fintech permite 3 requisições por janela de 60 segundos por chave (valor reduzido para o exemplo; em produção seria bem maior). Uma resposta dentro do limite e outra acima dele:

```http
HTTP/1.1 201 Created
X-RateLimit-Limit: 3
X-RateLimit-Remaining: 2
X-RateLimit-Reset: 1790000060
Content-Type: application/json

{"id": "pix_981", "accountId": "acc_1042", "amountCents": 15000, "status": "PENDING"}
```

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 3
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1790000060
Retry-After: 42
Content-Type: application/json

{"error": "RATE_LIMIT_EXCEEDED", "message": "Limite de 3 requisições por minuto atingido."}
```

Um limitador de janela fixa por cliente, com o tempo recebido como parâmetro para o resultado ser previsível:

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.HashMap;
import java.util.Map;

public class RateLimitDemo {
    static class FixedWindowRateLimiter {
        private final int limit;
        private final long windowSeconds;
        private final Map<String, long[]> state = new HashMap<>(); // {janela, contagem}

        FixedWindowRateLimiter(int limit, long windowSeconds) {
            this.limit = limit;
            this.windowSeconds = windowSeconds;
        }

        boolean tryAcquire(String clientId, long nowSeconds) {
            long window = nowSeconds / windowSeconds;
            long[] s = state.computeIfAbsent(clientId, k -> new long[] {window, 0});
            if (s[0] != window) {
                s[0] = window;
                s[1] = 0;
            }
            if (s[1] >= limit) {
                return false;
            }
            s[1]++;
            return true;
        }
    }

    public static void main(String[] args) {
        FixedWindowRateLimiter limiter = new FixedWindowRateLimiter(3, 60);
        for (long t : new long[] {0, 1, 2, 3, 61}) {
            System.out.print(limiter.tryAcquire("pix-partner-42", t) + " ");
        }
        System.out.println(); // true true true false true
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from typing import Dict, List


class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.state: Dict[str, List[int]] = {}  # {janela, contagem}

    def try_acquire(self, client_id: str, now_seconds: int) -> bool:
        window = now_seconds // self.window_seconds
        current = self.state.get(client_id)
        if current is None or current[0] != window:
            current = [window, 0]
            self.state[client_id] = current
        if current[1] >= self.limit:
            return False
        current[1] += 1
        return True


limiter = FixedWindowRateLimiter(3, 60)
print(" ".join(str(limiter.try_acquire("pix-partner-42", t)).lower() for t in (0, 1, 2, 3, 61)))
# true true true false true
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import "fmt"

type window struct{ id, count int64 }

type RateLimiter struct {
	limit         int64
	windowSeconds int64
	state         map[string]*window
}

func NewRateLimiter(limit, windowSeconds int64) *RateLimiter {
	return &RateLimiter{limit: limit, windowSeconds: windowSeconds, state: map[string]*window{}}
}

// Sem sincronização, para manter o exemplo curto: em produção use um mutex ou um armazenamento compartilhado.
func (r *RateLimiter) TryAcquire(clientID string, nowSeconds int64) bool {
	id := nowSeconds / r.windowSeconds
	w, ok := r.state[clientID]
	if !ok || w.id != id {
		w = &window{id: id}
		r.state[clientID] = w
	}
	if w.count >= r.limit {
		return false
	}
	w.count++
	return true
}

func main() {
	limiter := NewRateLimiter(3, 60)
	for _, t := range []int64{0, 1, 2, 3, 61} {
		fmt.Print(limiter.TryAcquire("pix-partner-42", t), " ")
	}
	fmt.Println() // true true true false true
}
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Pricing Plan](/architecture/api-patterns/documentation/pricing-plan) — o limite faz valer os níveis de cobrança do plano
- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — os detalhes do limite podem fazer parte do SLA
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — identifica o cliente a quem o limite se aplica
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — pode carregar na mensagem o estado atual da cota
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) e [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — ajudam a não violar limites baseados em volume de dados
- [Rate Limiting](/architecture/cloud-design-patterns/resiliency/rate-limiting-pattern) — a mesma técnica vista do lado da arquitetura de nuvem; aqui o foco é o contrato publicado com o cliente
- [Throttling](/architecture/cloud-design-patterns/resiliency/throttling) — controla o consumo de recursos para sustentar o serviço, às vezes sem acordo explícito; o Rate Limit é uma cota declarada por cliente
- [Retry](/architecture/cloud-design-patterns/resiliency/retry) — o cliente deve esperar e tentar de novo ao receber 429, respeitando `Retry-After`

## Referência

- [Patterns for API Design, capítulo 9: Rate Limit](https://api-patterns.org/)
- [RFC 6585: 429 Too Many Requests](https://www.rfc-editor.org/rfc/rfc6585#section-4)
