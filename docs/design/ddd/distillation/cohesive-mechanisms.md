---
title: Cohesive Mechanisms
pattern_slug: cohesive-mechanisms
category: Distillation
tags:
  - Simplicity
  - Decoupling
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
sidebar_label: "Cohesive Mechanisms"
---

# Cohesive Mechanisms

## Descrição

Cohesive Mechanisms são mecanismos computacionais complexos, como algoritmos de grafos, motores de regras ou resolução de restrições, que se infiltram no modelo de domínio e o enchem de detalhes procedimentais. O padrão propõe extrair esse mecanismo para uma estrutura separada, com uma interface que revela a intenção.

O modelo de domínio passa a expressar o quê (conceitos e regras de negócio) enquanto o mecanismo cuida do como (a mecânica do cálculo). O mecanismo é coeso, tem uma responsabilidade clara e pode ser testado e evoluído sem tocar nas regras do negócio.

É diferente de um [Generic Subdomain](/design/ddd/distillation/generic-subdomains): o subdomínio genérico trata de conceitos de negócio sem diferencial, enquanto o mecanismo é uma questão técnica de computação que, às vezes, é publicada como framework ou biblioteca.

## Problemas que resolve

- Algoritmos complexos misturados às entidades e aos serviços do domínio, que escondem as regras de negócio.
- Dificuldade de testar a lógica de domínio isolada da mecânica do cálculo.
- Modelo difícil de ler porque a intenção se perde em detalhes de implementação.
- Impossibilidade de trocar ou otimizar o algoritmo sem alterar o domínio.

## Quando usar

- Quando uma parte do código é principalmente computação (grafos, otimização, regras, cálculo numérico) e não conhecimento de negócio.
- Quando o mecanismo pode ser descrito por uma interface simples orientada à intenção.
- Quando o mesmo algoritmo pode servir a mais de um ponto do modelo ou ser substituído no futuro.

## Quando evitar

- Quando o cálculo faz parte da regra de negócio e deve ser conhecimento explícito do domínio; extraí-lo esconderia o core.
- Quando a lógica é simples demais para justificar uma estrutura separada.
- Quando a abstração teria de expor tantos detalhes internos que a interface não ficaria enxuta.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Domínio mais legível e focado em conceitos | Mais uma estrutura para manter |
| Mecanismo testável e evoluível por conta própria | A fronteira entre regra e mecanismo pode ser difícil de traçar |
| Troca ou otimização do algoritmo sem afetar o domínio | Risco de abstrair demais e esconder regras de negócio |
| Possibilidade de reuso por vários componentes | Pode exigir conhecimento técnico especializado |

- **Interface:** deve ser expressa em termos do domínio ([Intention-Revealing Interfaces](/design/ddd/supple-design/intention-revealing-interfaces)), não dos detalhes do algoritmo.
- **Fronteira:** é o ponto mais sensível; o mecanismo resolve o como, e decisões do quê permanecem no modelo.
- **Reuso:** frequentemente se transforma em uma biblioteca ou em um framework interno.

## Diagrama

```mermaid
classDiagram
    class LoanOfferService {
        +offer(proposal, pricing) LoanOffer
    }
    class RateSolver {
        <<interface>>
        +solveMonthlyRate(releasedCents, installmentsCents) double
    }
    class NewtonRateSolver {
        +solveMonthlyRate(releasedCents, installmentsCents) double
    }
    class BisectionRateSolver {
        +solveMonthlyRate(releasedCents, installmentsCents) double
    }
    LoanOfferService --> RateSolver
    RateSolver <|.. NewtonRateSolver
    RateSolver <|.. BisectionRateSolver
```

O serviço de domínio `LoanOfferService` expressa o problema em termos de negócio e delega o cálculo numérico da taxa do CET a um mecanismo substituível por trás de `RateSolver`.

## Exemplo

Uma fintech de crédito monta ofertas de empréstimo com taxa, parcelas, tarifas e IOF, e precisa informar o CET de cada uma. O CET é a taxa que iguala as parcelas, trazidas a valor presente, ao valor efetivamente liberado ao cliente; essa equação não tem solução fechada e exige um método numérico, como Newton-Raphson ou bisseção. Colocar essas iterações dentro de `LoanOffer` ou `PricingRule` tornaria essas classes ilegíveis.

A equipe extrai o cálculo para um mecanismo com uma interface voltada à intenção, e o domínio apenas o invoca com seus próprios conceitos.

```java
public interface RateSolver {
    // Taxa mensal que iguala o valor presente das parcelas ao valor liberado.
    double solveMonthlyRate(long releasedCents, List<Long> installmentsCents);
}

public class LoanOfferService {
    private final RateSolver solver;

    public LoanOfferService(RateSolver solver) {
        this.solver = solver;
    }

    public LoanOffer offer(CreditProposal proposal, PricingRule pricing) {
        List<Long> installmentsCents = pricing.installmentsFor(proposal);
        long releasedCents = proposal.amountCents() - pricing.upfrontChargesCents(proposal);
        double monthlyCet = solver.solveMonthlyRate(releasedCents, installmentsCents);
        return LoanOffer.of(proposal, installmentsCents, monthlyCet);   // regra de negócio
    }
}
```

## Padrões relacionados

- [Generic Subdomains](/design/ddd/distillation/generic-subdomains) — vizinho conceitual, mas voltado a conceitos de negócio e não a mecanismos de computação.
- [Core Domain](/design/ddd/distillation/core-domain) — o mecanismo é retirado para manter o core expressivo.
- [Intention-Revealing Interfaces](/design/ddd/supple-design/intention-revealing-interfaces) — dá ao mecanismo uma interface em termos do domínio.
- [Domain Service](/design/ddd/building-blocks/domain-service) — o ponto do modelo que normalmente invoca o mecanismo.
- [Strategy](/coding/gof/behavioral/strategy) — forma comum de tornar o algoritmo substituível.
- [Separated Interface](/design/poeaa/base/separated-interface) — separa a interface da implementação em pacotes distintos.

## Referência

- [DDD Reference, Eric Evans (2015)](https://www.domainlanguage.com/ddd/reference/)
- *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Eric Evans (Addison-Wesley, 2003)
