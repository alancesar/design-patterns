---
title: Experimental Preview
pattern_slug: experimental-preview
category: Life-Cycle Management
tags:
  - Evolvability
  - Shared Understanding
source: https://api-patterns.org/
sidebar_label: "Experimental Preview"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/api-patterns/life-cycle-management/experimental-preview.mdx';

# Experimental Preview

## Descrição

O padrão Experimental Preview disponibiliza uma API em regime de melhor esforço, sem compromisso com funcionalidade, estabilidade ou tempo de vida, e deixa essa falta de maturidade explícita para que os clientes ajustem suas expectativas.

O provedor publica uma versão ainda instável fora do processo normal de gestão, por exemplo em um ambiente de sandbox sem contrato de nível de serviço e com uma descrição de API em rascunho. Os clientes entram voluntariamente, sabendo que a prévia pode mudar de forma incompatível, sair do ar sem aviso ou ter prazo fixo e curto. Em troca, ganham acesso antecipado: podem estimar o esforço de integração e adiantar o desenvolvimento enquanto a API final ainda está sendo desenhada. A prévia pode ser aberta a qualquer cliente ou restrita a um grupo fechado (por exemplo com [API Keys](/architecture/api-patterns/special-purpose-representations/api-key) específicas), o que limita o esforço de suporte e de comunicação. Costuma rodar em um ambiente de não produção, ligado à versão em desenvolvimento e com níveis de serviço bem frouxos; quem preferir estabilidade continua na versão oficial. É o compromisso de suporte mais fraco que um provedor pode oferecer, parecido com um programa de beta, e o provedor pode conceder um período de transição quando a prévia é promovida.

## Problemas que resolve

- Lançar uma API nova sem saber se o desenho atende às necessidades reais dos clientes
- Evitar que mudanças incompatíveis, ainda esperadas durante o desenvolvimento, quebrem integrações em produção
- Dar aos clientes interessados uma forma de testar e opinar antes de a API ser congelada
- Não assumir, cedo demais, as garantias e o custo de suporte de uma API estável
- A alternativa de esperar a versão final impede os clientes de começar a integrar durante meses, e a de lançar versões incompatíveis com frequência sobrecarrega a governança e dificulta o acompanhamento

## Quando usar

- Quando uma funcionalidade nova ou um redesenho grande ainda está em fase de descoberta
- Quando o provedor quer feedback de clientes-chave antes de fixar contratos e versões
- Quando é preciso validar desempenho, segurança ou usabilidade em escala menor
- Como etapa anterior à entrega da API em produção, combinada com [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) ou [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee)

## Quando evitar

- Quando clientes já dependem do recurso em produção e não toleram quebras
- Quando a API é regulada ou crítica e exige garantias formais desde o primeiro dia
- Quando não há equipe para colher e tratar o feedback: a prévia vira uma API instável sem propósito
- Quando o aviso de instabilidade não chegará aos clientes de forma clara

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Feedback precoce de quem vai usar a API | Clientes podem usar a prévia em produção apesar do aviso |
| Liberdade para mudar o desenho sem versionar | Pode haver desgaste de relacionamento se mudanças forem frequentes demais |
| Menor custo de suporte e de governança | Exige comunicar claramente a ausência de garantias |
| Integração antecipada dos clientes interessados | O trabalho dos clientes pode ser descartado quando a prévia mudar ou sair do ar |

- **Expectativas:** deixe o status na URL, na documentação e nas respostas, para que ninguém o confunda com a API estável.
- **Prazo:** uma prévia sem data de encerramento tende a virar a API de fato; defina quando ela termina ou é promovida.
- **Público:** um grupo fechado reduz o suporte, mas também o volume de feedback.
- **Ambiente extra:** operar e proteger mais um ambiente e um canal de acesso dá trabalho, e o desenvolvimento fica transparente, com erros que não farão parte da API final.
- **Atratividade:** a falta de compromisso de longo prazo pode fazer a API parecer imatura e afastar clientes.
- **Promoção:** ao estabilizar, publique a versão final com o identificador e as garantias do padrão de ciclo de vida escolhido.

## Diagrama

<Diagram />

As versões beta mudam e podem sumir sem aviso; só a versão promovida para produção assume garantias de compatibilidade e de tempo de vida.

## Exemplo

Uma fintech quer abrir uma API de cobranças Pix parceladas (Pix Automático) a parceiros. Antes de fixar o contrato, publica uma prévia em um host separado, com aviso explícito nas respostas.

```http
POST /v2beta1/pix-charges HTTP/1.1
Host: sandbox.api.fintech.example
Content-Type: application/json

{"accountId": "acc-4821", "amountCents": 125000, "currency": "BRL", "installments": 3}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json
Warning: 299 - "Experimental Preview: sem garantias de estabilidade ou disponibilidade"

{
  "id": "pix-9f3a",
  "status": "PENDING",
  "amountCents": 125000,
  "currency": "BRL",
  "installments": 3,
  "preview": {"stage": "beta1", "mayChangeWithoutNotice": true, "endsOn": "2027-02-28"}
}
```

O sufixo `beta1`, o host de sandbox, o cabeçalho `Warning` e o objeto `preview` deixam claro que não há garantias, e `endsOn` fixa o fim da prévia.

## Padrões relacionados

- [Two in Production](/architecture/api-patterns/life-cycle-management/two-in-production) — governa o ciclo de vida da API de produção depois que a prévia termina; na variante N in Production, a prévia pode conviver com as demais versões
- [Limited Lifetime Guarantee](/architecture/api-patterns/life-cycle-management/limited-lifetime-guarantee) — a garantia que a API final passa a oferecer, ao contrário da prévia
- [Aggressive Obsolescence](/architecture/api-patterns/life-cycle-management/aggressive-obsolescence) — retira partes da API depois de estável, com aviso prévio, enquanto a prévia não oferece nem isso
- [API Key](/architecture/api-patterns/special-purpose-representations/api-key) — pode restringir o acesso à prévia a clientes selecionados
- [Version Identifier](/architecture/api-patterns/versioning/version-identifier) — identifica as versões beta e a versão final, embora a prévia não seja obrigada a tê-lo
- [API Description](/architecture/api-patterns/documentation/api-description) — a prévia costuma ter uma descrição em rascunho
- [Service Level Agreement](/architecture/api-patterns/documentation/service-level-agreement) — a prévia normalmente não está coberta por um SLA
- [Strangler Fig](/architecture/cloud-design-patterns/integration-and-modernization/strangler-fig) — migra funcionalidade aos poucos para um sistema novo; aqui o objetivo é testar uma API nova com clientes voluntários

## Referência

- [Patterns for API Design, capítulo 8: Experimental Preview](https://api-patterns.org/)
