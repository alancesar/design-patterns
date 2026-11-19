---
title: Data Transfer Resource
pattern_slug: data-transfer-resource
category: Endpoint Roles
tags:
  - Decoupling
  - Performance
source: https://api-patterns.org/
sidebar_label: "Data Transfer Resource"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/endpoint-roles/data-transfer-resource.mdx';

# Data Transfer Resource

## Descrição

O padrão Data Transfer Resource expõe um endpoint compartilhado que serve de área intermediária para trocar dados entre parceiros que não precisam estar disponíveis ao mesmo tempo nem se conhecer diretamente.

É um refinamento do [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) que funciona como um quadro compartilhado: um participante deposita os dados no recurso e os outros os retiram depois, no seu próprio ritmo. O recurso tem um endereço único e global e oferece ao menos uma operação de criação de estado e uma de recuperação; qualquer cliente autorizado que conheça o endereço pode também ler, atualizar e apagar. Os parceiros ficam desacoplados no tempo (não precisam estar ativos juntos) e no local (basta alcançarem o recurso), e podem até se comunicar quando um deles está atrás de firewall ou roda no navegador.

A propriedade dos dados deve ficar com os clientes, não com o provedor. Há três variantes, conforme os padrões de acesso e a vida do recurso: o **Relay Resource**, com um só escritor e um só leitor, em que a propriedade passa de quem escreve para quem lê; o **Published Resource**, com um escritor e um número grande e imprevisível de leitores, às vezes anos depois, em que o escritor decide por quanto tempo o recurso fica disponível; e o **Conversation Resource**, em que vários clientes leem, escrevem e por fim apagam, e qualquer participante é dono do recurso. Os clientes combinam o endereço antecipadamente, descobrem-no por um [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) ou o primeiro a publicar o informa aos demais.

## Problemas que resolve

- Parceiros que não estão disponíveis ao mesmo tempo e precisam trocar dados mesmo assim
- Payloads grandes que sobrecarregam as mensagens de controle e atrasam as chamadas
- Acoplamento direto entre quem produz e quem consome os dados
- Necessidade de entregar o mesmo conteúdo a destinatários que o buscam em momentos diferentes, inclusive depois que o dado já foi enviado e quando o número de destinatários é desconhecido
- Participantes que não conseguem se falar diretamente (atrás de NAT ou firewall, em navegadores) ou que só podem usar um cliente HTTP básico, sem instalar um middleware de mensageria

## Quando usar

- Emissor e receptor operam de forma assíncrona ou em horários distintos
- O volume é grande demais para trafegar em uma chamada comum
- É preciso desacoplar identidade, localização e disponibilidade dos parceiros
- Os dados são temporários e podem ser descartados após o consumo

## Quando evitar

- Quando a comunicação precisa de resposta imediata e síncrona
- Quando o volume é pequeno e a chamada direta resolve de forma mais simples
- Quando os dados são sensíveis e o armazenamento intermediário não pode ser protegido adequadamente
- Quando a retenção intermediária cria risco de acúmulo de dados sem dono ou de vazamento
- Quando já existe um middleware de mensageria operado e disponível para todos os participantes, com entrega garantida

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Parceiros desacoplados no tempo e na identidade | Latência maior e entrega menos previsível |
| Suporte a grandes volumes fora das mensagens de controle | Provedor guarda dados temporários e precisa gerenciar espaço e prazo |
| Cada parte age no seu ritmo | Precisa de convenções sobre quem remove os dados e quando |
| Reaproveitável para vários destinatários | Armazenamento intermediário amplia a superfície de segurança |

- **Segurança:** o recurso de transferência exige autorização e, em geral, links temporários e criptografia dos dados em repouso.
- **Retenção:** defina um prazo de expiração para evitar acúmulo de dados esquecidos.
- **Notificação:** combine como o receptor sabe que há dados (consulta periódica, evento ou callback).
- **Propriedade:** defina quem é responsável pela validade e pela limpeza do conteúdo (emissor, receptor ou o provedor que arca com o armazenamento); prefira a propriedade dos clientes.
- **Confiabilidade:** o HTTP não garante a entrega, mas escrever com PUT e ler com GET é idempotente, então o cliente repete a chamada até funcionar, sem precisar remover duplicatas.
- **Visibilidade da entrega:** o emissor não sabe se alguém leu; o recurso pode expor metadados de acesso (quantas leituras), úteis também para limpar recursos sem uso.
- **Latência:** são dois saltos em vez de um; o padrão prioriza transferir dados entre muitos participantes e ao longo do tempo, não a rapidez de uma transferência.
- **Integridade:** inclua tamanho e hash do conteúdo para que o receptor valide o que recebeu.

## Diagrama

<Diagram />

O emissor grava no recurso intermediário, o receptor retira depois, e os dois nunca precisam estar conectados ao mesmo tempo.

## Exemplo

A fintech recebe extratos de investimentos de renda fixa de um parceiro custodiante, em arquivos grandes enviados de madrugada. O parceiro deposita o arquivo; o serviço de conciliação o lê quando está pronto.

```http
PUT /transfers/fixed-income-statement-2026-11-16 HTTP/1.1
Content-Type: text/csv
Content-Length: 5242880

... linhas do extrato, com valores em centavos ...
```

```http
HTTP/1.1 201 Created
Location: /transfers/fixed-income-statement-2026-11-16
```

O `PUT` é idempotente, então o parceiro pode repeti-lo se a conexão cair. Depois, o serviço de conciliação faz `GET /transfers/fixed-income-statement-2026-11-16` e, após processar, `DELETE` no mesmo endereço. Aqui o recurso funciona como um Relay Resource: um escritor, um leitor, e a propriedade passa ao leitor. O recurso expira sozinho em 24 horas se ninguém o remover.

## Padrões relacionados

- [File Transfer](/architecture/eip/integration-styles/file-transfer) — estilo de integração por arquivos; aqui o arquivo passa por um recurso de API com ciclo de vida próprio
- [Shared Database](/architecture/microservices/service-collaboration/shared-database) — também troca dados por um repositório comum, mas expõe o esquema; o recurso de transferência esconde isso atrás de um contrato
- [Claim Check](/architecture/cloud-design-patterns/messaging/claim-check) — envia só uma referência na mensagem e guarda o conteúdo grande à parte
- [Valet Key](/architecture/cloud-design-patterns/security-and-access/valet-key) — dá ao cliente acesso temporário e restrito direto ao armazenamento
- [Asynchronous Request-Reply](/architecture/cloud-design-patterns/messaging/asynchronous-request-reply) — outra forma de lidar com trabalho que não termina na mesma chamada
- [Information Holder Resource](/architecture/api-patterns/endpoint-roles/information-holder-resource) — o recurso de transferência é um tipo de recurso centrado em dados, mas temporário
- [Link Lookup Resource](/architecture/api-patterns/endpoint-roles/link-lookup-resource) — ajuda os clientes a descobrir o endereço do recurso compartilhado
- [State Creation Operation](/architecture/api-patterns/operation-responsibilities/state-creation-operation) e [Retrieval Operation](/architecture/api-patterns/operation-responsibilities/retrieval-operation) — as duas operações mínimas do recurso

## Referência

- [Patterns for API Design, capítulo 5: Data Transfer Resource](https://api-patterns.org/)
