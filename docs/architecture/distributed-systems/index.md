---
title: "Patterns of Distributed Systems"
sidebar_label: "Distributed Systems"
---

# Patterns of Distributed Systems

Catálogo pessoal baseado no [Catalog of Patterns of Distributed Systems](https://martinfowler.com/articles/patterns-of-distributed-systems/), de Unmesh Joshi, publicado no site de Martin Fowler e que resume o livro *Patterns of Distributed Systems* (2023). Os grupos seguem as partes do livro. Cada padrão tem descrição, problemas que resolve, quando usar, trade-offs, etiquetas (garantias distribuídas) e um diagrama Mermaid.

Padrões marcados com ★ são compartilhados com outro catálogo: este catálogo aponta para o documento original, revisado com o conteúdo desta fonte.

Total: 30 padrões em 5 grupos. Etiquetas: Garantia distribuída.

## Grupos

- [Data Replication](#data-replication) (16)
- [Data Partitioning](#data-partitioning) (3)
- [Distributed Time](#distributed-time) (3)
- [Cluster Management](#cluster-management) (5)
- [Communication between Nodes](#node-communication) (3)

## Data Replication (16) {#data-replication}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Write-Ahead Log](./data-replication/write-ahead-log.md) | O Write-Ahead Log (WAL) é um arquivo de log somente com acréscimos (*append-only*) em disco no qual cada mudança de estado é registrada como um comando antes de ser aplicada às estruturas de dados em memória ou aos arquivos de dados. | [`Durability`](/tags/durability) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Segmented Log](./data-replication/segmented-log.md) | O Segmented Log divide o Write-Ahead Log em vários arquivos menores, chamados segmentos, em vez de manter um único arquivo que cresce indefinidamente. | [`Performance`](/tags/performance) [`Durability`](/tags/durability) |
| [Low-Water Mark](./data-replication/low-water-mark.md) | O Low-Water Mark é um índice (offset) no log abaixo do qual as entradas não são mais necessárias e podem ser descartadas com segurança. | [`Performance`](/tags/performance) [`Durability`](/tags/durability) |
| [Leader and Followers](./data-replication/leader-and-followers.md) | Em Leader and Followers, um servidor do cluster é escolhido como líder e passa a tomar as decisões em nome do grupo: ele recebe as escritas, define a ordem das atualizações e as propaga para os demais servidores, os seguidores. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [HeartBeat](./data-replication/heartbeat.md) | No HeartBeat, cada servidor envia periodicamente a outros servidores uma mensagem curta indicando que continua ativo. | [`Availability`](/tags/availability) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Majority Quorum](./data-replication/majority-quorum.md) | No Majority Quorum, uma atualização só é considerada aceita pelo cluster quando a maioria dos nós a reconhece. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [Generation Clock](./data-replication/generation-clock.md) | O Generation Clock é um número que só cresce e identifica o "mandato" do líder atual. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [High-Water Mark](./data-replication/high-water-mark.md) | O High-Water Mark é um índice no log que marca a última entrada replicada com sucesso em uma maioria (quórum) de nós. | [`Consistency`](/tags/consistency) [`Durability`](/tags/durability) |
| [Paxos](./data-replication/paxos.md) | Paxos é um protocolo de consenso, proposto por Leslie Lamport, que permite a um grupo de nós concordar em um valor mesmo com falhas de nós e de rede e sem um líder fixo. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Replicated Log](./data-replication/replicated-log.md) | No Replicated Log, cada nó do cluster mantém um Write-Ahead Log cujas entradas guardam as requisições do usuário e o estado necessário para o consenso. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Durability`](/tags/durability) |
| [Singular Update Queue](./data-replication/singular-update-queue.md) | A Singular Update Queue usa uma fila de trabalho processada por uma única thread para aplicar mudanças de estado. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Request Waiting List](./data-replication/request-waiting-list.md) | A Request Waiting List é uma estrutura que associa uma chave a uma função de callback. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Idempotent Receiver](../../cloud/cloud-design-patterns/messaging/idempotent-consumer.md) ★ | O padrão Idempotent Consumer projeta consumidores de mensagens de forma que processar a mesma mensagem mais de uma vez produza exatamente o mesmo efeito que processá-la uma única vez. | [`Reliability`](/tags/reliability) |
| [Follower Reads](./data-replication/follower-reads.md) | No Follower Reads, as escritas continuam passando pelo líder, mas as requisições somente de leitura podem ser atendidas pelos seguidores, em especial o mais próximo do cliente. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) [`Availability`](/tags/availability) |
| [Versioned Value](./data-replication/versioned-value.md) | No Versioned Value, cada valor de uma chave é guardado junto com um número de versão que aumenta a cada atualização. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Version Vector](./data-replication/version-vector.md) | O Version Vector associa a cada valor de uma chave um vetor com um contador por nó do cluster. | [`Consistency`](/tags/consistency) [`Availability`](/tags/availability) |

## Data Partitioning (3) {#data-partitioning}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Fixed Partitions](./data-partitioning/fixed-partitions.md) | Fixed Partitions mantém constante o número de partições lógicas de um cluster. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) |
| [Key-Range Partitions](./data-partitioning/key-range-partitions.md) | Key-Range Partitions divide o espaço de chaves ordenadas em intervalos contíguos, e cada intervalo vira uma partição lógica. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) |
| [Two-Phase Commit](./data-partitioning/two-phase-commit.md) | Two-Phase Commit (2PC) grava dados de forma atômica em vários nós, normalmente em partições diferentes. | [`Consistency`](/tags/consistency) [`Durability`](/tags/durability) |

## Distributed Time (3) {#distributed-time}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Lamport Clock](./distributed-time/lamport-clock.md) | O Lamport Clock é um contador lógico, um simples inteiro, mantido por cada nó do cluster para ordenar eventos sem depender do relógio de parede. | [`Consistency`](/tags/consistency) |
| [Hybrid Clock](./distributed-time/hybrid-clock.md) | O Hybrid Clock (relógio lógico híbrido, ou HLC) combina o relógio de parede do sistema com um contador lógico. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Clock-Bound Wait](./distributed-time/clock-bound-wait.md) | O Clock-Bound Wait lida com a incerteza dos relógios físicos de um cluster esperando que ela passe. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |

## Cluster Management (5) {#cluster-management}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Consistent Core](./cluster-management/consistent-core.md) | O Consistent Core separa o cluster em duas partes: um pequeno grupo de nós (tipicamente três a cinco) que executa um algoritmo de consenso e oferece linearizabilidade com tolerância a falhas, e um cluster de dados, que pode ter centenas de nós. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Scalability`](/tags/scalability) |
| [Lease](./cluster-management/lease.md) | Um Lease é uma concessão de acesso exclusivo a um recurso por um tempo limitado. | [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [State Watch](./cluster-management/state-watch.md) | No State Watch, o cliente registra no servidor o interesse em mudanças de determinados valores (uma chave, um prefixo, o estado de um nó). | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |
| [Gossip Dissemination](./cluster-management/gossip-dissemination.md) | No Gossip Dissemination, cada nó guarda os metadados que conhece sobre o cluster (membership, estado de nós, informações de partições) e, em intervalos regulares, por exemplo a cada segundo, escolhe um ou poucos nós aleatórios e troca com eles o que sabe. | [`Scalability`](/tags/scalability) [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [Emergent Leader](./cluster-management/emergent-leader.md) | Em clusters peer-to-peer, todos os nós são iguais e não existe uma eleição explícita como em Leader and Followers. | [`Availability`](/tags/availability) [`Fault Tolerance`](/tags/fault-tolerance) |

## Communication between Nodes (3) {#node-communication}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Single-Socket Channel](./node-communication/single-socket-channel.md) | O Single-Socket Channel usa uma única conexão TCP, aberta e mantida de forma duradoura, para todo o tráfego entre um par de nós, por exemplo entre um follower e o seu líder. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Performance`](/tags/performance) |
| [Request Batch](./node-communication/request-batch.md) | O Request Batch agrupa várias requisições pequenas em uma única mensagem de rede, enviada de uma vez a um nó do cluster. | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |
| [Request Pipeline](./node-communication/request-pipeline.md) | O Request Pipeline faz um nó enviar várias requisições a outro nó sem esperar a resposta de cada uma antes de enviar a seguinte. | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |

## Por etiqueta

### Consistency (16)

[Leader and Followers](./data-replication/leader-and-followers.md), [Majority Quorum](./data-replication/majority-quorum.md), [Generation Clock](./data-replication/generation-clock.md), [High-Water Mark](./data-replication/high-water-mark.md), [Paxos](./data-replication/paxos.md), [Replicated Log](./data-replication/replicated-log.md), [Singular Update Queue](./data-replication/singular-update-queue.md), [Request Waiting List](./data-replication/request-waiting-list.md), [Versioned Value](./data-replication/versioned-value.md), [Version Vector](./data-replication/version-vector.md), [Two-Phase Commit](./data-partitioning/two-phase-commit.md), [Lamport Clock](./distributed-time/lamport-clock.md), [Hybrid Clock](./distributed-time/hybrid-clock.md), [Clock-Bound Wait](./distributed-time/clock-bound-wait.md), [Consistent Core](./cluster-management/consistent-core.md), [Single-Socket Channel](./node-communication/single-socket-channel.md)

### Durability (6)

[Write-Ahead Log](./data-replication/write-ahead-log.md), [Segmented Log](./data-replication/segmented-log.md), [Low-Water Mark](./data-replication/low-water-mark.md), [High-Water Mark](./data-replication/high-water-mark.md), [Replicated Log](./data-replication/replicated-log.md), [Two-Phase Commit](./data-partitioning/two-phase-commit.md)

### Availability (7)

[HeartBeat](./data-replication/heartbeat.md), [Majority Quorum](./data-replication/majority-quorum.md), [Follower Reads](./data-replication/follower-reads.md), [Version Vector](./data-replication/version-vector.md), [Lease](./cluster-management/lease.md), [Gossip Dissemination](./cluster-management/gossip-dissemination.md), [Emergent Leader](./cluster-management/emergent-leader.md)

### Fault Tolerance (12)

[Write-Ahead Log](./data-replication/write-ahead-log.md), [Leader and Followers](./data-replication/leader-and-followers.md), [HeartBeat](./data-replication/heartbeat.md), [Majority Quorum](./data-replication/majority-quorum.md), [Generation Clock](./data-replication/generation-clock.md), [Paxos](./data-replication/paxos.md), [Replicated Log](./data-replication/replicated-log.md), [Consistent Core](./cluster-management/consistent-core.md), [Lease](./cluster-management/lease.md), [Gossip Dissemination](./cluster-management/gossip-dissemination.md), [Emergent Leader](./cluster-management/emergent-leader.md), [Single-Socket Channel](./node-communication/single-socket-channel.md)

### Scalability (8)

[Follower Reads](./data-replication/follower-reads.md), [Fixed Partitions](./data-partitioning/fixed-partitions.md), [Key-Range Partitions](./data-partitioning/key-range-partitions.md), [Consistent Core](./cluster-management/consistent-core.md), [State Watch](./cluster-management/state-watch.md), [Gossip Dissemination](./cluster-management/gossip-dissemination.md), [Request Batch](./node-communication/request-batch.md), [Request Pipeline](./node-communication/request-pipeline.md)

### Performance (14)

[Segmented Log](./data-replication/segmented-log.md), [Low-Water Mark](./data-replication/low-water-mark.md), [Singular Update Queue](./data-replication/singular-update-queue.md), [Request Waiting List](./data-replication/request-waiting-list.md), [Follower Reads](./data-replication/follower-reads.md), [Versioned Value](./data-replication/versioned-value.md), [Fixed Partitions](./data-partitioning/fixed-partitions.md), [Key-Range Partitions](./data-partitioning/key-range-partitions.md), [Hybrid Clock](./distributed-time/hybrid-clock.md), [Clock-Bound Wait](./distributed-time/clock-bound-wait.md), [State Watch](./cluster-management/state-watch.md), [Single-Socket Channel](./node-communication/single-socket-channel.md), [Request Batch](./node-communication/request-batch.md), [Request Pipeline](./node-communication/request-pipeline.md)

### Reliability (1)

[Idempotent Receiver](../../cloud/cloud-design-patterns/messaging/idempotent-consumer.md)
