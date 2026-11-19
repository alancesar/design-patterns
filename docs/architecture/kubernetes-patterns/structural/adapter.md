---
title: Adapter
pattern_slug: adapter
category: Structural
tags:
  - Operational Excellence
  - Performance Efficiency
source: https://k8spatterns.com/
sidebar_label: "Adapter"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/structural/adapter.mdx';

# Adapter

## Descrição

O padrão Adapter usa um contêiner auxiliar no mesmo Pod para fazer um sistema heterogêneo expor uma interface uniforme e normalizada, que possa ser consumida por quem está fora do Pod. É uma especialização do Sidecar com um único propósito: adaptar o acesso à aplicação, sem alterar a aplicação.

O exemplo mais comum é o monitoramento. Serviços escritos em linguagens diferentes publicam métricas em formatos distintos, ou apenas as gravam em arquivos de log, e a ferramenta de monitoramento espera um único formato e protocolo. Cada Pod ganha então um contêiner adapter que lê as métricas específicas da aplicação (por exemplo, de um arquivo em um volume compartilhado) e as expõe em um endpoint HTTP no formato esperado.

O mesmo raciocínio vale para logs: o adapter normaliza formatos e níveis de detalhe, enriquece as linhas com contexto do Pod e as entrega para o agregador central. Funciona como um proxy reverso que esconde a complexidade da aplicação atrás de uma interface padrão.

## Problemas que resolve

- Serviços heterogêneos que expõem métricas, logs ou status em formatos incompatíveis com o sistema que os consome
- Necessidade de integrar uma aplicação legada ou de terceiros a um padrão de observabilidade sem poder alterar seu código
- Ferramentas de monitoramento que precisariam conhecer o formato de cada serviço
- Lógica de conversão duplicada dentro de cada aplicação, em cada linguagem

## Quando usar

- Quando vários serviços precisam aparecer para o monitoramento ou para o agregador de logs em um formato único
- Quando a aplicação não pode ser modificada (imagem de terceiros, código legado) mas precisa se integrar a um padrão da plataforma
- Quando se quer manter a aplicação sem conhecimento sobre as ferramentas que a observam
- Quando a conversão pode ser feita a partir de dados locais compartilhados, como arquivos em um volume ou uma porta em localhost

## Quando evitar

- Quando a aplicação já expõe o formato esperado ou pode adotá-lo com uma biblioteca simples
- Quando a conversão exige acesso profundo à lógica interna da aplicação
- Quando o custo de um contêiner extra por Pod supera o benefício, como em Pods muito numerosos e pequenos
- Quando a necessidade é de conectividade de saída, e não de uma interface de entrada padronizada: use um Ambassador

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Interface única para sistemas heterogêneos, simplificando o consumidor | Um contêiner extra por Pod, com consumo de CPU e memória |
| Aplicação desacoplada da ferramenta de monitoramento ou de logs | Mais um componente para empacotar, versionar e manter |
| Adapters reutilizáveis entre aplicações que compartilham o mesmo formato de origem | A conversão pode ficar defasada se o formato da aplicação mudar |
| Troca da ferramenta de observabilidade sem tocar na aplicação | O adapter compartilha o ciclo de vida e a escala do Pod |

- **Dados compartilhados:** o adapter costuma ler dados locais por volume ou localhost, então o formato desse canal vira um contrato entre os dois contêineres.
- **Responsabilidade única:** mantenha o adapter focado em traduzir; lógica de negócio não pertence a ele.
- **Recursos:** defina requests e limits para o adapter, pois ele conta no total do Pod.
- **Nome distinto:** chamar o padrão de Adapter, e não apenas de Sidecar, comunica com mais precisão a intenção do contêiner.

## Diagrama

<Diagram />

A aplicação grava métricas no seu formato próprio em um volume compartilhado. O adapter as lê, converte para o formato que o Prometheus entende e as expõe por HTTP, sem que o `card-service` saiba da existência do monitoramento.

## Exemplo

O `card-service` registra o tempo de autorização de cada compra em um arquivo de log. Um adapter no mesmo Pod lê esse arquivo e publica as métricas para o Prometheus.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: card-service
  namespace: fintech
spec:
  replicas: 2
  selector:
    matchLabels:
      app: card-service
  template:
    metadata:
      labels:
        app: card-service
    spec:
      containers:
        - name: card-service
          image: registry.fintech.example/card-service:2.1.0
          env:
            - name: AUTH_LOG_FILE
              value: /logs/authorizations.log
          volumeMounts:
            - name: logs
              mountPath: /logs
        - name: metrics-adapter
          image: registry.fintech.example/card-metrics-exporter:0.3.1
          env:
            - name: AUTH_LOG_FILE
              value: /logs/authorizations.log
          ports:
            - containerPort: 9100
          volumeMounts:
            - name: logs
              mountPath: /logs
              readOnly: true
      volumes:
        - name: logs
          emptyDir: {}
```

Os dois contêineres compartilham o volume `logs`; o adapter monta o volume somente leitura e publica as métricas na porta 9100.

## Padrões relacionados

- [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) — o Adapter é uma especialização do Sidecar voltada a normalizar a interface da aplicação.
- [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador) — a outra especialização do Sidecar: atua como proxy para o mundo externo, enquanto o Adapter expõe a aplicação de forma uniforme.
- [Adapter (GoF)](/coding/gof/structural/adapter) — o mesmo princípio de converter interfaces, aplicado a classes dentro do código em vez de a contêineres.
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — um adapter pode traduzir o estado de uma aplicação legada em um endpoint de saúde padrão.
- [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness) — o adapter pode enriquecer logs e métricas com informações do Pod.

## Referência

- [Kubernetes Patterns, capítulo 17: Adapter](https://k8spatterns.com/)
- [Pods (documentação do Kubernetes)](https://kubernetes.io/docs/concepts/workloads/pods/)
