---
title: Service Discovery
pattern_slug: service-discovery
category: Behavioral
tags:
  - Reliability
  - Performance Efficiency
source: https://k8spatterns.com/
sidebar_label: "Service Discovery"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/behavioral/service-discovery.mdx';

# Service Discovery

## Descrição

O padrão Service Discovery dá a um conjunto de Pods um ponto de acesso estável, com nome e endereço fixos, usando o recurso Service do Kubernetes para que consumidores encontrem os produtores sem conhecer seus endereços dinâmicos. Pods nascem e morrem o tempo todo, e seus IPs mudam a cada recriação; o Service esconde essa volatilidade atrás de um IP virtual e de um nome DNS.

O Service seleciona Pods por labels e mantém a lista de endereços atualizada, incluindo apenas os que estão prontos, segundo a readiness probe. Quem chama usa o nome do Service, que o DNS do cluster resolve para o IP virtual, e o tráfego é distribuído entre os Pods. Na descoberta **interna**, o tipo `ClusterIP` expõe o serviço dentro do cluster, e o Service headless (`clusterIP: None`) devolve diretamente os IPs dos Pods, útil para StatefulSets e para balanceamento no cliente. Na descoberta **manual**, um Service sem seletor aponta para recursos Endpoints mantidos à mão (em geral IPs fora do cluster), e `ExternalName` cria um alias DNS (CNAME) para um nome externo; assim o destino pode migrar de fora para dentro do cluster sem mudar o endereço usado pelos clientes. Na descoberta a partir de **fora** do cluster, `NodePort` abre uma porta em todos os nós, `LoadBalancer` soma um balanceador do provedor de nuvem e o Ingress, na camada de aplicação, atua como roteador HTTP na frente de vários Services, com um único balanceador e IP externo.

## Problemas que resolve

- Endereços de Pods que mudam a cada reinício, reagendamento ou escala
- Consumidores acoplados a IPs fixos ou a configuração manual de destinos
- Distribuição de tráfego entre várias réplicas sem um balanceador próprio
- Envio de requisições a Pods que ainda não estão prontos ou que já falharam

## Quando usar

- Sempre que um componente precisa ser chamado por outros e roda em mais de um Pod ou pode ser recriado
- Quando se quer descoberta por nome DNS ou variáveis de ambiente, sem registro explícito na aplicação
- Para expor um serviço fora do cluster, por NodePort, LoadBalancer ou Ingress
- Para dar um nome interno estável a um serviço externo, como uma API de terceiros

## Quando evitar

- Quando o consumidor precisa escolher a instância com lógica própria: use um Service headless e descoberta pelo cliente
- Para protocolos ou balanceamento avançados (por exemplo, por requisição ou por cabeçalho), que pedem um proxy de camada 7 ou uma malha de serviços
- Para identificar uma réplica específica de um serviço com estado sem o Service headless
- Quando um único Pod é chamado por um nome conhecido e estável, e o Service não agrega nada

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Nome e IP estáveis, independentes do ciclo de vida dos Pods | O balanceamento é simples, sem consciência de carga ou de sessão |
| Registro e remoção automáticos, guiados por labels e readiness | Seletor de labels errado deixa o Service sem endpoints, sem erro evidente |
| Aplicação independente da plataforma, que só usa nomes DNS | Depende do DNS do cluster, que precisa estar saudável e com cache bem ajustado |
| Opções de exposição interna e externa no mesmo modelo | Exposição externa exige mais configuração e cuidados de segurança |

- **Readiness:** só Pods prontos entram no Service; uma probe mal configurada derruba capacidade ou envia tráfego cedo demais.
- **Variáveis de ambiente:** são injetadas só na criação do Pod, então o DNS é a forma preferida e funciona sem ordem de criação.
- **Nomes completos:** use `<service>.<namespace>` para chamadas entre namespaces.
- **Cliente com cache:** clientes que guardam o IP resolvido por muito tempo podem continuar usando endereços antigos.
- **Segurança:** combine com NetworkPolicy para controlar quem pode chamar quem.
- **Camada 4:** o Service balanceia no transporte; `sessionAffinity: ClientIP` fixa um cliente a um Pod, mas afinidade por cookie HTTP exige um Ingress ou proxy de camada 7.
- **NodePort:** exige regras de firewall e que o cliente escolha um nó saudável (um balanceador na frente ajuda); `externalTrafficPolicy: Local` evita o salto extra e preserva o IP de origem, mas só encaminha para Pods do próprio nó.
- **LoadBalancer:** depende de suporte do provedor de nuvem, e o tratamento do endereço de origem varia entre provedores.
- **Ingress:** é o mecanismo mais poderoso e o mais complexo, exige um Ingress controller no cluster e é mais útil para expor vários serviços sob um IP quando todos falam o mesmo protocolo de camada 7.

## Diagrama

<Diagram />

Consumidores internos chamam o nome do Service e o tráfego chega só aos Pods prontos; o Ingress leva o tráfego externo ao mesmo Service.

## Exemplo

O `pix-service` exposto dentro do cluster por um Service, com uma readiness probe que define quais Pods recebem tráfego.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pix-service
  namespace: fintech
spec:
  type: ClusterIP
  selector:
    app: pix-service
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pix-service
  namespace: fintech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pix-service
  template:
    metadata:
      labels:
        app: pix-service
    spec:
      containers:
        - name: pix-service
          image: registry.fintech.example/pix-service:1.4.2
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
```

Outros serviços chamam `http://pix-service` no mesmo namespace ou `pix-service.fintech` de fora dele; apenas os Pods que passam na readiness probe entram na lista de endpoints.

## Padrões relacionados

- [Server-Side Discovery](/architecture/microservices/service-discovery/server-side-discovery) — o Service do Kubernetes é a forma nativa dessa estratégia, com a plataforma resolvendo e balanceando
- [Client-Side Discovery](/architecture/microservices/service-discovery/client-side-discovery) — o Service headless permite que o cliente obtenha os IPs e escolha a instância
- [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) — a readiness probe determina quais Pods o Service inclui
- [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) — usa Service headless para dar nome DNS a cada Pod
- [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador) — um proxy auxiliar pode abstrair a descoberta e o acesso a serviços externos
- [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness) — o Pod pode conhecer o próprio nome e namespace para se registrar ou montar nomes DNS

## Referência

- [Kubernetes Patterns, capítulo 13: Service Discovery](https://k8spatterns.com/)
- [Service na documentação do Kubernetes](https://kubernetes.io/docs/concepts/services-networking/service/)
- [DNS para Services e Pods na documentação do Kubernetes](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
