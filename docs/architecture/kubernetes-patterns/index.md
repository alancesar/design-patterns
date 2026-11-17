---
title: "Kubernetes Patterns"
sidebar_label: "Kubernetes Patterns"
---

# Kubernetes Patterns

Catálogo pessoal baseado no livro [*Kubernetes Patterns*](https://k8spatterns.com/), de Bilgin Ibryam e Roland Huß (O'Reilly, 1ª edição, 2019), que descreve elementos reutilizáveis para projetar aplicações cloud native sobre o Kubernetes. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (pilares do Well-Architected Framework), um diagrama Mermaid e, quando ajuda, um manifesto YAML de exemplo.

Padrões marcados com ★ são compartilhados com outro catálogo: este catálogo aponta para o documento original, revisado com o conteúdo desta fonte.

Total: 24 padrões em 5 grupos. Etiquetas: Pilares do Well-Architected Framework.

## Grupos

- [Foundational](#foundational) (5)
- [Behavioral](#behavioral) (7)
- [Structural](#structural) (4)
- [Configuration](#configuration) (4)
- [Advanced](#advanced) (4)

## Foundational (5) {#foundational}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) | O padrão Predictable Demands consiste em declarar, no manifesto de cada workload, as dependências de execução e o perfil de recursos de seus contêineres, para que o Kubernetes saiba onde colocá-los e como tratá-los quando o cluster fica sob pressão. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) | O padrão Declarative Deployment descreve a versão desejada de uma aplicação em um recurso `Deployment` e deixa que o Kubernetes execute, no servidor, todos os passos para sair da versão atual e chegar a ela, de forma repetível e com possibilidade de reverter. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe) | O padrão Health Probe faz a aplicação expor ao Kubernetes sinais sobre o seu próprio estado, por meio de sondas que o kubelet executa periodicamente, para que a plataforma decida se deve reiniciar o contêiner ou parar de enviar tráfego a ele. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle) | O padrão Managed Lifecycle faz a aplicação escutar e reagir aos eventos de ciclo de vida emitidos pelo Kubernetes, como sinais de encerramento e hooks de início e fim, para iniciar e terminar de forma limpa, sem perder trabalho em andamento. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement) | O padrão Automated Placement delega ao scheduler do Kubernetes a decisão de em qual nó cada Pod vai rodar, considerando os recursos solicitados e as regras de posicionamento declaradas, e permite influenciar essa decisão sem escolher os nós manualmente. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) |

## Behavioral (7) {#behavioral}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) | O padrão Batch Job executa uma unidade de trabalho finita e isolada em Pods de vida curta, usando o recurso Job do Kubernetes para garantir que ela termine com sucesso mesmo diante de falhas de contêiner ou de nó. | [`Reliability`](/tags/reliability) [`Cost Optimization`](/tags/cost-optimization) |
| [Periodic Job](/architecture/kubernetes-patterns/behavioral/periodic-job) | O padrão Periodic Job dispara a execução de um Batch Job por um evento temporal, usando o recurso CronJob do Kubernetes para agendar a criação de Jobs no formato cron. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Daemon Service](/architecture/kubernetes-patterns/behavioral/daemon-service) | O padrão Daemon Service executa um Pod de infraestrutura em cada nó do cluster, ou em um subconjunto escolhido de nós, usando o recurso DaemonSet para ampliar as capacidades da plataforma. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service) | O padrão Singleton Service garante que apenas uma instância ativa de um serviço esteja em execução por vez, seja por controle externo da plataforma, seja por uma disputa de liderança dentro da própria aplicação. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service) | O padrão Stateful Service executa aplicações com estado usando o recurso StatefulSet, que dá a cada Pod uma identidade estável, armazenamento persistente próprio e uma ordem previsível de criação, atualização e remoção. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery) | O padrão Service Discovery dá a um conjunto de Pods um ponto de acesso estável, com nome e endereço fixos, usando o recurso Service do Kubernetes para que consumidores encontrem os produtores sem conhecer seus endereços dinâmicos. | [`Reliability`](/tags/reliability) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness) | O padrão Self Awareness permite que uma aplicação conheça informações sobre si mesma e sobre o ambiente em que roda, usando a Downward API do Kubernetes para injetar metadados do Pod por variáveis de ambiente ou arquivos. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |

## Structural (4) {#structural}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Init Container](/architecture/kubernetes-patterns/structural/init-container) | O padrão Init Container separa as tarefas de inicialização de um Pod dos contêineres da aplicação, executando-as antes, em sequência e com ciclo de vida próprio. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar) ★ | O padrão Sidecar implanta componentes auxiliares de uma aplicação em um processo ou contêiner separado, executado ao lado da aplicação principal. | [`Security`](/tags/security) [`Operational Excellence`](/tags/operational-excellence) |
| [Adapter](/architecture/kubernetes-patterns/structural/adapter) | O padrão Adapter usa um contêiner auxiliar no mesmo Pod para fazer um sistema heterogêneo expor uma interface uniforme e normalizada, que possa ser consumida por quem está fora do Pod. | [`Operational Excellence`](/tags/operational-excellence) [`Performance Efficiency`](/tags/performance-efficiency) |
| [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador) ★ | O padrão Ambassador cria serviços auxiliares que enviam requisições de rede em nome de uma aplicação ou serviço consumidor. | [`Reliability`](/tags/reliability) [`Security`](/tags/security) |

## Configuration (4) {#configuration}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration) | O padrão EnvVar Configuration externaliza a configuração de uma aplicação em variáveis de ambiente, o mecanismo mais simples e universalmente suportado para alterar o comportamento de um contêiner sem reconstruir a imagem. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |
| [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource) | O padrão Configuration Resource guarda a configuração de uma aplicação em recursos nativos do Kubernetes, ConfigMap para dados comuns e Secret para dados confidenciais, desacoplando o ciclo de vida da configuração do ciclo de vida da aplicação. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |
| [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration) | O padrão Immutable Configuration empacota os dados de configuração de um ambiente em uma imagem de contêiner passiva e versionada, que é ligada à aplicação apenas em tempo de execução. | [`Reliability`](/tags/reliability) [`Operational Excellence`](/tags/operational-excellence) |
| [Configuration Template](/architecture/kubernetes-patterns/configuration/configuration-template) | O padrão Configuration Template gera, na inicialização da aplicação, arquivos de configuração grandes e complexos a partir de um modelo único e de um pequeno conjunto de parâmetros específicos do ambiente. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |

## Advanced (4) {#advanced}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Controller](/architecture/kubernetes-patterns/advanced/controller) | O padrão Controller é um processo que observa continuamente um conjunto de recursos do Kubernetes e age para aproximar o estado real do estado desejado declarado neles. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Operator](/architecture/kubernetes-patterns/advanced/operator) | O padrão Operator é um Controller que usa uma CustomResourceDefinition (CRD) para encapsular o conhecimento operacional de uma aplicação específica de forma algorítmica e automatizada. | [`Operational Excellence`](/tags/operational-excellence) [`Reliability`](/tags/reliability) |
| [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale) | O padrão Elastic Scale faz a capacidade de uma aplicação acompanhar a carga automaticamente, escalando em várias dimensões: horizontalmente (número de réplicas de Pod), verticalmente (requests e limits de cada Pod) e no nível do cluster (número de nós). | [`Performance Efficiency`](/tags/performance-efficiency) [`Cost Optimization`](/tags/cost-optimization) [`Reliability`](/tags/reliability) |
| [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder) | O padrão Image Builder constrói as imagens de contêiner dentro do próprio cluster Kubernetes, usando o escalonador e os recursos da plataforma para executar os builds em vez de um sistema de build externo. | [`Operational Excellence`](/tags/operational-excellence) [`Security`](/tags/security) |

## Por etiqueta

### Reliability (18)

[Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands), [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment), [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe), [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle), [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement), [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job), [Periodic Job](/architecture/kubernetes-patterns/behavioral/periodic-job), [Daemon Service](/architecture/kubernetes-patterns/behavioral/daemon-service), [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service), [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service), [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery), [Init Container](/architecture/kubernetes-patterns/structural/init-container), [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador), [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration), [Configuration Template](/architecture/kubernetes-patterns/configuration/configuration-template), [Controller](/architecture/kubernetes-patterns/advanced/controller), [Operator](/architecture/kubernetes-patterns/advanced/operator), [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale)

### Cost Optimization (4)

[Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands), [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement), [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job), [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale)

### Performance Efficiency (7)

[Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands), [Automated Placement](/architecture/kubernetes-patterns/foundational/automated-placement), [Stateful Service](/architecture/kubernetes-patterns/behavioral/stateful-service), [Service Discovery](/architecture/kubernetes-patterns/behavioral/service-discovery), [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness), [Adapter](/architecture/kubernetes-patterns/structural/adapter), [Elastic Scale](/architecture/kubernetes-patterns/advanced/elastic-scale)

### Operational Excellence (17)

[Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment), [Health Probe](/architecture/kubernetes-patterns/foundational/health-probe), [Managed Lifecycle](/architecture/kubernetes-patterns/foundational/managed-lifecycle), [Periodic Job](/architecture/kubernetes-patterns/behavioral/periodic-job), [Daemon Service](/architecture/kubernetes-patterns/behavioral/daemon-service), [Singleton Service](/architecture/kubernetes-patterns/behavioral/singleton-service), [Self Awareness](/architecture/kubernetes-patterns/behavioral/self-awareness), [Init Container](/architecture/kubernetes-patterns/structural/init-container), [Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar), [Adapter](/architecture/kubernetes-patterns/structural/adapter), [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration), [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource), [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration), [Configuration Template](/architecture/kubernetes-patterns/configuration/configuration-template), [Controller](/architecture/kubernetes-patterns/advanced/controller), [Operator](/architecture/kubernetes-patterns/advanced/operator), [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder)

### Security (5)

[Sidecar](/architecture/cloud-design-patterns/integration-and-modernization/sidecar), [Ambassador](/architecture/cloud-design-patterns/integration-and-modernization/ambassador), [EnvVar Configuration](/architecture/kubernetes-patterns/configuration/envvar-configuration), [Configuration Resource](/architecture/kubernetes-patterns/configuration/configuration-resource), [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder)
