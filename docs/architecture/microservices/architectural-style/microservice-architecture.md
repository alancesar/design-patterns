---
title: Microservice Architecture
pattern_slug: microservice-architecture
category: Architectural Style
tags:
  - Reliability
  - Operational Excellence
  - Performance Efficiency
  - Security
source: https://microservices.io/patterns/microservices.html
sidebar_label: "Microservice Architecture"
---

# Microservice Architecture

## Descrição

Microservice Architecture estrutura a aplicação como dois ou mais serviços implantáveis de forma independente e fracamente acoplados. Cada serviço contém um ou mais subdomínios, e cada subdomínio pertence a um único serviço (exceto bibliotecas compartilhadas).

Uma equipe é dona dos serviços que contêm seus subdomínios. Tipicamente cada serviço tem seu próprio repositório e pipeline de implantação, e um API Gateway serve como ponto de entrada para os clientes. Operações que atravessam serviços são implementadas com padrões de colaboração, como Saga e API Composition.

O estilo troca a simplicidade de um componente único por autonomia de equipes e flexibilidade, ao custo de lidar com os desafios de sistemas distribuídos.

## Problemas que resolve

- Como agrupar os subdomínios da aplicação em componentes implantáveis ou executáveis.
- Necessidade de componentes simples, fáceis de entender, com autonomia de equipe para desenvolver e implantar.
- Necessidade de pipelines rápidos, viabilizados por componentes pequenos.
- Suporte a múltiplas pilhas tecnológicas.
- Segregação de subdomínios por escalabilidade, disponibilidade ou segurança.

## Quando usar

- Aplicações críticas que precisam mudar de forma rápida, frequente e confiável.
- Organizações com várias equipes multifuncionais e entrega contínua automatizada.
- Quando subdomínios têm requisitos distintos de escala, disponibilidade, segurança ou tecnologia.

### Quando evitar

- Aplicações pequenas ou com domínio ainda instável, onde as fronteiras de serviço seriam adivinhadas.
- Equipes sem maturidade em automação, observabilidade e operação de sistemas distribuídos.
- Quando transações ACID entre subdomínios e baixa latência de interação são requisitos centrais.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Serviços pequenos e fáceis de entender | Operações distribuídas são complexas de entender e depurar |
| Equipes desenvolvem, testam e implantam de forma independente | Algumas operações distribuídas podem ser ineficientes |
| Build e testes rápidos por serviço | Banco por serviço costuma exigir consistência eventual |
| Pilhas tecnológicas diferentes por serviço | Acoplamento em tempo de execução pode reduzir a disponibilidade |
| Agrupamento por escalabilidade, segurança etc. | Acoplamento em tempo de projeto pode forçar mudanças coordenadas |

- Exige investimento em observabilidade, descoberta de serviços, resiliência e automação de implantação.
- Definir fronteiras corretas (por capacidade de negócio ou subdomínio) é decisivo para reduzir acoplamento.

## Diagrama

```mermaid
flowchart LR
    C[Client] --> GW[API Gateway]
    GW --> S1[Order Service]
    GW --> S2[Customer Service]
    GW --> S3[Delivery Service]
    S1 --> DB1[(Orders DB)]
    S2 --> DB2[(Customers DB)]
    S3 --> DB3[(Deliveries DB)]
    S1 -. "messages / calls" .-> S2
    S1 -. "messages / calls" .-> S3
```

Cada serviço é implantado de forma independente, possui seu próprio banco e é acessado por um API Gateway; a colaboração entre serviços ocorre por mensagens ou chamadas remotas.

## Padrões relacionados

- [Monolithic Architecture](./monolithic-architecture.md) — estilo alternativo, com um único componente implantável.
- [Decompose by Business Capability](../service-boundaries/decompose-by-business-capability.md) — define as fronteiras dos serviços.
- [Decompose by Subdomain](../service-boundaries/decompose-by-subdomain.md) — define as fronteiras dos serviços a partir do DDD.
- [Database per Service](../service-collaboration/database-per-service.md) — cada serviço possui seus próprios dados.
- [Saga](../../../cloud/cloud-design-patterns/distributed-coordination/saga.md) — consistência em operações que atravessam serviços.
- [API Composition](../service-collaboration/api-composition.md) — consultas que combinam dados de vários serviços.
- [CQRS](../../../cloud/cloud-design-patterns/data-management/cqrs.md) — consultas eficientes sobre dados distribuídos.
- [Messaging](../communication-styles/messaging.md) — comunicação assíncrona entre serviços.
- [Remote Procedure Invocation](../communication-styles/remote-procedure-invocation.md) — comunicação síncrona entre serviços.
- [Transactional Outbox](../transactional-messaging/transactional-outbox.md) — publicação atômica de mensagens e atualizações de dados.
- [API Gateway](../external-api/api-gateway.md) — ponto de entrada para os clientes.
- [Client-side Discovery](../service-discovery/client-side-discovery.md) — localização de instâncias de serviço.
- [Server-side Discovery](../service-discovery/server-side-discovery.md) — localização de instâncias via roteador.
- [Circuit Breaker](../../../cloud/cloud-design-patterns/resiliency/circuit-breaker.md) — evita falhas em cascata entre serviços.
- [Access Token](../security/access-token.md) — propagação da identidade entre serviços.
- [Log Aggregation](../observability/log-aggregation.md) — observabilidade de sistemas distribuídos.
- [Distributed Tracing](../observability/distributed-tracing.md) — rastreamento de requisições entre serviços.
- [Health Check API](../../../cloud/cloud-design-patterns/resiliency/health-endpoint-monitoring.md) — verificação da saúde de cada serviço.
- [Service Component Test](../testing/service-component-test.md) — teste isolado de cada serviço.
- [Microservice Chassis](../cross-cutting-concerns/microservice-chassis.md) — preocupações transversais reutilizáveis.
- [Externalized Configuration](../../../cloud/cloud-design-patterns/deployment-and-topology/external-configuration-store.md) — configuração fora do artefato.

## Referência

- [Página do padrão no microservices.io](https://microservices.io/patterns/microservices.html)
