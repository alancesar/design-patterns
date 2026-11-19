---
title: Processing Resource
pattern_slug: processing-resource
category: Endpoint Roles
tags:
  - Decoupling
  - Evolvability
source: https://api-patterns.org/
sidebar_label: "Processing Resource"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/processing-resource.mdx';

# Processing Resource

## Descrição

O padrão Processing Resource expõe um endpoint cuja função é executar uma ação de negócio, e não guardar dados, oferecendo uma ou mais operações que o cliente invoca para disparar processamento no provedor.

Em vez de modelar o contrato em torno de dados, o endpoint é modelado em torno de uma atividade (transferir, aprovar, calcular, cancelar). Cada operação recebe os parâmetros da ação e devolve o resultado ou uma confirmação, e o estado interno que muda como consequência fica escondido atrás da interface. É o papel adequado quando a lógica de negócio é o que importa e os detalhes do armazenamento não deveriam vazar para os clientes.

As operações de um Processing Resource são, em geral, de criação de estado, de transição de estado ou funções de cálculo; a leitura costuma se limitar a consultar o andamento de uma atividade, pois o acesso amplo a dados é papel do Information Holder Resource. Cada operação recebe uma mensagem de comando e, quando é uma troca de requisição e resposta, devolve um documento com o resultado. O recurso pode ser com estado (um coordenador de processo) ou sem estado (um utilitário de cálculo), e o contrato precisa declarar pré-condições, invariantes e pós-condições. A diferença para um recurso orientado a dados é a intenção: o cliente pede que algo seja feito, em vez de manipular uma entidade diretamente.

## Problemas que resolve

- Ações de negócio que não cabem bem em operações genéricas de criar, ler, atualizar e apagar sobre uma entidade
- Clientes que precisariam conhecer e coordenar vários recursos de dados para realizar uma única atividade
- Acoplamento do contrato a detalhes do modelo de dados interno, que dificulta mudar a implementação
- Regras de negócio e validações duplicadas em cada cliente em vez de centralizadas no provedor

## Quando usar

- A atividade tem semântica de negócio própria, como executar um Pix, aprovar um crédito ou conciliar um lote
- A ação toca vários dados internos que o cliente não deveria enxergar nem coordenar
- É preciso manter a lógica e as invariantes no provedor, mesmo que o armazenamento mude
- O contrato é consumido por clientes diversos que querem pedir resultados, não manipular estado

## Quando evitar

- Quando o cliente precisa apenas ler ou manter dados: um [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) é mais simples
- Quando as operações viram uma lista de verbos arbitrários sem coesão, tornando o endpoint um depósito de procedimentos
- Quando muitas operações compartilham o mesmo estado e o contrato passa a ser, na prática, um acesso remoto disfarçado a dados
- Quando o cliente precisa de visibilidade e controle fino do estado intermediário que o endpoint esconde
- Quando a orientação a atividades teria de ser forçada sobre um domínio naturalmente orientado a dados, como arquivos e inventários: prefira o Information Holder Resource
- Misturar ações e dados no mesmo endpoint, embora possível, não é recomendado em arquiteturas de microsserviços, pelo acoplamento que traz

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Contrato expressa a intenção de negócio e esconde o modelo de dados | Cliente depende da semântica de cada operação, difícil de padronizar |
| Lógica e invariantes ficam centralizadas no provedor | Endpoint pode crescer e acumular responsabilidades sem coesão |
| Liberdade para mudar a implementação sem quebrar clientes | Ações com efeito colateral exigem cuidado com repetição e idempotência |
| Menos chamadas coordenadas pelo cliente | Dificulta cache e reuso, pois não há recurso identificável para armazenar |

- **Coesão:** agrupe apenas operações que servem à mesma atividade de negócio; endpoints grandes demais devem ser divididos.
- **Idempotência:** operações com efeito colateral, como mover dinheiro, precisam de chave de idempotência para tolerar repetição após falha de rede.
- **Tipo da operação:** decida, para cada operação, se ela cria estado, transiciona estado, calcula ou lê, e documente isso no contrato.
- **Tempo de resposta:** se a ação demora ou o cliente não precisa do resultado na hora, devolva um identificador e deixe o cliente acompanhar depois (consulta periódica ou callback), em vez de bloquear a chamada.
- **Compensação:** o que uma transação do sistema não desfaz, como uma notificação já enviada, exige uma operação de compensação no nível da aplicação.
- **Segurança e auditoria:** cada ação precisa de autorização própria e, muitas vezes, de trilha de auditoria, o que torna o provedor com estado mesmo quando o domínio não pede.
- **Risco de RPC:** se as operações forem apenas procedimentos remotos disfarçados, o acoplamento de tempo e de formato aumenta; modele atividades de negócio, não funções internas.
- **Resposta:** devolva um identificador do que foi criado ou o resultado calculado, para que o cliente possa acompanhar sem adivinhar.

## Diagrama

<Diagram />

O cliente invoca operações com nome de atividade; o endpoint aplica as regras e altera os dados internos, que não aparecem no contrato.

## Exemplo

O serviço de pagamentos da fintech expõe um endpoint `/pix-processor` com duas operações de negócio. O cliente pede a transferência e recebe um identificador; não conhece contas, razão contábil nem filas internas.

```http
POST /pix-processor/execute-transfer HTTP/1.1
Content-Type: application/json
Idempotency-Key: 6d8f2c1e-3b7a-4d51-9a10-0b4f1e22c9aa

{
  "sourceAccountId": "acc-1001",
  "pixKey": "maria@example.com",
  "amount": { "cents": 15000, "currency": "BRL" }
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{ "transferId": "pix-77231", "status": "PROCESSING" }
```

```http
POST /pix-processor/cancel-transfer HTTP/1.1
Content-Type: application/json

{ "transferId": "pix-77231", "reason": "CUSTOMER_REQUEST" }
```

O valor é enviado em centavos inteiros. Se a transferência já foi liquidada, o cancelamento é recusado, e o estorno entra como um novo lançamento no razão (`LedgerEntry`), nunca como edição do original.

## Padrões relacionados

- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — o papel complementar: foca em dados, e não em ações
- [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) — tipo de operação típico de um Processing Resource
- [State Transition Operation](/architecture/api-patterns/operation-responsibilities/state-transition-operation) — operação que move o estado interno de um estágio a outro
- [Computation Function](/architecture/api-patterns/operation-responsibilities/computation-function) — operação sem efeito colateral que calcula um resultado
- [Remote Facade](/design/poeaa/distribution/remote-facade) — fachada de granularidade grossa por trás da qual a lógica e os dados ficam escondidos
- [Asynchronous Request-Reply](/architecture/cloud-design-patterns/messaging/asynchronous-request-reply) — modelo para ações de longa duração, com consulta do resultado depois
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key), [Rate Limit](/architecture/api-patterns/documentation/rate-limit) e [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — costumam proteger e regular o uso das operações
- [Context Representation](/architecture/api-patterns/special-purpose-representations/context-representation) — isola parâmetros técnicos para que não invadam o corpo das mensagens
- [Command Message](/architecture/eip/message-construction/command-message) — o equivalente em mensageria de pedir a execução de uma ação

## Referência

- [Patterns for API Design, capítulo 5: Processing Resource](https://api-patterns.org/)
