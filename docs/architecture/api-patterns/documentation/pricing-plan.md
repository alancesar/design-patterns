---
title: Pricing Plan
pattern_slug: pricing-plan
category: Documentation
tags:
  - Shared Understanding
  - Simplicity
source: https://api-patterns.org/
sidebar_label: "Pricing Plan"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/documentation/pricing-plan.mdx';

# Pricing Plan

## Descrição

O padrão Pricing Plan associa à descrição da API uma política de preços, que define como o consumo é medido e cobrado de clientes, anunciantes ou outras partes, de modo que o provedor financie a API e o cliente saiba quanto vai pagar.

Uma API é um ativo com valor monetário e imaterial, e desenvolvê-la e operá-la custa dinheiro. O plano de preços torna explícitos os custos e as obrigações mútuas (faturamento, pagamento, limites). Ele também define as métricas a medir, como chamadas por operação ou volume de dados transferido.

As variantes mais comuns são três. No **preço por assinatura**, o cliente paga uma taxa recorrente independente do uso, muitas vezes combinada com um [Rate Limit](/architecture/api-patterns/documentation/rate-limit) para uso justo e com faixas (níveis) entre as quais o cliente escolhe. No **preço por uso**, paga-se apenas o que se consome, com valores que podem variar por operação, ou por pacotes pré-pagos de créditos. No **preço de mercado**, o valor acompanha a demanda e clientes fazem lances. Os planos se combinam: um nível gratuito (freemium) para uso baixo, ou uma assinatura base mais cobrança por excedente.

## Problemas que resolve

- Financiar o desenvolvimento e a operação de uma API sem tratar da mesma forma curiosos e clientes de alto volume
- Dar ao cliente previsibilidade sobre o custo e controle sobre limites de gasto
- Medir o consumo com um nível de detalhe aceitável para as duas partes
- Tornar a cobrança auditável sem expor dados de um cliente a outro

## Quando usar

- Quando a API é um produto ou gera custo relevante que precisa ser recuperado
- Quando há segmentos de clientes com perfis de uso muito diferentes (hobby, startup, grande empresa)
- Quando se quer incentivar a adoção com nível gratuito e converter em planos pagos
- Quando o provedor precisa alinhar limites técnicos e comerciais em um único acordo

## Quando evitar

- Em APIs internas de uma única organização, em que o custo é rateado de outra forma
- Quando o custo de medir e cobrar supera a receita que a cobrança traria
- Quando não há como identificar o cliente de forma confiável (veja [API Key](/architecture/api-patterns/special-purpose-representations/api-key)): sem identidade, não há cobrança correta

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Receita proporcional ao valor entregue e acordo claro sobre custos | Definir preços justos exige conhecer o negócio dos clientes e é difícil de acertar |
| Assinatura é simples de operar e dá previsibilidade | Uso muito baixo ou muito alto fica mal precificado |
| Preço por uso é justo e acompanha o consumo | Exige medição detalhada, relatórios e tratamento de disputas |
| Níveis combinados com limites protegem a capacidade | Mais planos, mais complexidade de comunicar e manter |

- **Medição:** se o sistema de medição cair, o provedor perde receita; é preciso decidir entre pausar a API ou servir sem cobrança durante a falha.
- **Precisão e desempenho:** contar cada chamada com exatidão pode custar latência; um agregado diário reduz o custo, mas piora a transparência.
- **Segurança e privacidade:** dados de cobrança são sensíveis, e em ambientes multilocatário um cliente não deve ver nem inferir o uso de outro.
- **Evolução:** comece pela assinatura e adicione o preço por uso depois, se necessário, pois a primeira é bem mais simples de implementar.

## Diagrama

<Diagram />

O gateway identifica o cliente, mede o uso e repassa os eventos para o faturamento, que aplica as faixas definidas no plano.

## Exemplo

A fintech cobra o acesso à API de cobranças Pix por faixa mensal de chamadas, com um nível gratuito. Os valores são ilustrativos e sempre em centavos. A tabela publicada na documentação é:

```text
Chamadas por mês (até)   Preço por mês
1.000                    grátis
50.000                   R$ 299,00
500.000                  R$ 1.499,00
acima disso              falar com vendas
```

Código que calcula a fatura de um cliente a partir do total de chamadas do mês.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.util.List;

public class PricingPlanDemo {
    record Tier(long upToCalls, long priceCents) {}

    static class PricingPlan {
        private final List<Tier> tiers;

        PricingPlan(List<Tier> tiers) { this.tiers = tiers; }

        long monthlyChargeCents(long calls) {
            for (Tier tier : tiers) {
                if (calls <= tier.upToCalls()) {
                    return tier.priceCents();
                }
            }
            throw new IllegalArgumentException("acima da maior faixa: falar com vendas");
        }
    }

    public static void main(String[] args) {
        PricingPlan plan = new PricingPlan(List.of(
                new Tier(1_000, 0),
                new Tier(50_000, 29_900),
                new Tier(500_000, 149_900)));
        System.out.println(plan.monthlyChargeCents(800));     // 0
        System.out.println(plan.monthlyChargeCents(12_000));  // 29900
        System.out.println(plan.monthlyChargeCents(300_000)); // 149900
    }
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Tier:
    up_to_calls: int
    price_cents: int


class PricingPlan:
    def __init__(self, tiers: List[Tier]) -> None:
        self.tiers = tiers

    def monthly_charge_cents(self, calls: int) -> int:
        for tier in self.tiers:
            if calls <= tier.up_to_calls:
                return tier.price_cents
        raise ValueError("acima da maior faixa: falar com vendas")


plan = PricingPlan([Tier(1_000, 0), Tier(50_000, 29_900), Tier(500_000, 149_900)])
print(plan.monthly_charge_cents(800))      # 0
print(plan.monthly_charge_cents(12_000))   # 29900
print(plan.monthly_charge_cents(300_000))  # 149900
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"errors"
	"fmt"
)

type Tier struct {
	UpToCalls  int64
	PriceCents int64
}

type PricingPlan struct {
	Tiers []Tier
}

// Em Go o excesso de faixa volta como erro, não como exceção.
func (p PricingPlan) MonthlyChargeCents(calls int64) (int64, error) {
	for _, tier := range p.Tiers {
		if calls <= tier.UpToCalls {
			return tier.PriceCents, nil
		}
	}
	return 0, errors.New("acima da maior faixa: falar com vendas")
}

func main() {
	plan := PricingPlan{Tiers: []Tier{
		{1_000, 0}, {50_000, 29_900}, {500_000, 149_900},
	}}
	for _, calls := range []int64{800, 12_000, 300_000} {
		charge, _ := plan.MonthlyChargeCents(calls)
		fmt.Println(charge) // 0, 29900, 149900
	}
}
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Rate Limit](/architecture/api-patterns/documentation/rate-limit) — aplica na prática os limites de cada nível do plano
- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — o plano deve referenciar o SLA que acompanha cada nível
- [API Description](/architecture/api-patterns/documentation/api-description) — a descrição da API é o lugar onde o plano é anexado
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — identifica o cliente cujo uso é medido e cobrado
- [Wish List](/architecture/api-patterns/response-shaping/wish-list) e [Wish Template](/architecture/api-patterns/response-shaping/wish-template) — ajudam o cliente a reduzir o volume de dados quando a cobrança depende dele
- [API Gateway](/architecture/microservices/external-api/api-gateway) — ponto natural para medir o uso e aplicar o plano

## Referência

- [Patterns for API Design, capítulo 9: Pricing Plan](https://api-patterns.org/)
