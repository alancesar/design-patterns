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
| [Write-Ahead Log](/architecture/distributed-systems/data-replication/write-ahead-log) | O Write-Ahead Log (WAL) é um arquivo de log somente com acréscimos (*append-only*) em disco no qual cada mudança de estado é registrada como um comando antes de ser aplicada às estruturas de dados em memória ou aos arquivos de dados. | [`Durability`](/tags/durability) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Segmented Log](/architecture/distributed-systems/data-replication/segmented-log) | O Segmented Log divide o Write-Ahead Log em vários arquivos menores, chamados segmentos, em vez de manter um único arquivo que cresce indefinidamente. | [`Performance`](/tags/performance) [`Durability`](/tags/durability) |
| [Low-Water Mark](/architecture/distributed-systems/data-replication/low-water-mark) | O Low-Water Mark é um índice (offset) no log abaixo do qual as entradas não são mais necessárias e podem ser descartadas com segurança. | [`Performance`](/tags/performance) [`Durability`](/tags/durability) |
| [Leader and Followers](/architecture/distributed-systems/data-replication/leader-and-followers) | Em Leader and Followers, um servidor do cluster é escolhido como líder e passa a tomar as decisões em nome do grupo: ele recebe as escritas, define a ordem das atualizações e as propaga para os demais servidores, os seguidores. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [HeartBeat](/architecture/distributed-systems/data-replication/heartbeat) | No HeartBeat, cada servidor envia periodicamente a outros servidores uma mensagem curta indicando que continua ativo. | [`Availability`](/tags/availability) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Majority Quorum](/architecture/distributed-systems/data-replication/majority-quorum) | No Majority Quorum, uma atualização só é considerada aceita pelo cluster quando a maioria dos nós a reconhece. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [Generation Clock](/architecture/distributed-systems/data-replication/generation-clock) | O Generation Clock é um número que só cresce e identifica o "mandato" do líder atual. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [High-Water Mark](/architecture/distributed-systems/data-replication/high-water-mark) | O High-Water Mark é um índice no log que marca a última entrada replicada com sucesso em uma maioria (quórum) de nós. | [`Consistency`](/tags/consistency) [`Durability`](/tags/durability) |
| [Paxos](/architecture/distributed-systems/data-replication/paxos) | Paxos é um protocolo de consenso, proposto por Leslie Lamport, que permite a um grupo de nós concordar em um valor mesmo com falhas de nós e de rede e sem um líder fixo. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Replicated Log](/architecture/distributed-systems/data-replication/replicated-log) | No Replicated Log, cada nó do cluster mantém um Write-Ahead Log cujas entradas guardam as requisições do usuário e o estado necessário para o consenso. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Durability`](/tags/durability) |
| [Singular Update Queue](/architecture/distributed-systems/data-replication/singular-update-queue) | A Singular Update Queue usa uma fila de trabalho processada por uma única thread para aplicar mudanças de estado. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Request Waiting List](/architecture/distributed-systems/data-replication/request-waiting-list) | A Request Waiting List é uma estrutura que associa uma chave a uma função de callback. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Idempotent Receiver](/architecture/cloud-design-patterns/messaging/idempotent-consumer) ★ | O padrão Idempotent Consumer projeta consumidores de mensagens de forma que processar a mesma mensagem mais de uma vez produza exatamente o mesmo efeito que processá-la uma única vez. | [`Reliability`](/tags/reliability) |
| [Follower Reads](/architecture/distributed-systems/data-replication/follower-reads) | No Follower Reads, as escritas continuam passando pelo líder, mas as requisições somente de leitura podem ser atendidas pelos seguidores, em especial o mais próximo do cliente. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) [`Availability`](/tags/availability) |
| [Versioned Value](/architecture/distributed-systems/data-replication/versioned-value) | No Versioned Value, cada valor de uma chave é guardado junto com um número de versão que aumenta a cada atualização. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Version Vector](/architecture/distributed-systems/data-replication/version-vector) | O Version Vector associa a cada valor de uma chave um vetor com um contador por nó do cluster. | [`Consistency`](/tags/consistency) [`Availability`](/tags/availability) |

## Data Partitioning (3) {#data-partitioning}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Fixed Partitions](/architecture/distributed-systems/data-partitioning/fixed-partitions) | Fixed Partitions mantém constante o número de partições lógicas de um cluster. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) |
| [Key-Range Partitions](/architecture/distributed-systems/data-partitioning/key-range-partitions) | Key-Range Partitions divide o espaço de chaves ordenadas em intervalos contíguos, e cada intervalo vira uma partição lógica. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) |
| [Two-Phase Commit](/architecture/distributed-systems/data-partitioning/two-phase-commit) | Two-Phase Commit (2PC) grava dados de forma atômica em vários nós, normalmente em partições diferentes. | [`Consistency`](/tags/consistency) [`Durability`](/tags/durability) |

## Distributed Time (3) {#distributed-time}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Lamport Clock](/architecture/distributed-systems/distributed-time/lamport-clock) | O Lamport Clock é um contador lógico, um simples inteiro, mantido por cada nó do cluster para ordenar eventos sem depender do relógio de parede. | [`Consistency`](/tags/consistency) |
| [Hybrid Clock](/architecture/distributed-systems/distributed-time/hybrid-clock) | O Hybrid Clock (relógio lógico híbrido, ou HLC) combina o relógio de parede do sistema com um contador lógico. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Clock-Bound Wait](/architecture/distributed-systems/distributed-time/clock-bound-wait) | O Clock-Bound Wait lida com a incerteza dos relógios físicos de um cluster esperando que ela passe. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |

## Cluster Management (5) {#cluster-management}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Consistent Core](/architecture/distributed-systems/cluster-management/consistent-core) | O Consistent Core separa o cluster em duas partes: um pequeno grupo de nós (tipicamente três a cinco) que executa um algoritmo de consenso e oferece linearizabilidade com tolerância a falhas, e um cluster de dados, que pode ter centenas de nós. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Scalability`](/tags/scalability) |
| [Lease](/architecture/distributed-systems/cluster-management/lease) | Um Lease é uma concessão de acesso exclusivo a um recurso por um tempo limitado. | [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [State Watch](/architecture/distributed-systems/cluster-management/state-watch) | No State Watch, o cliente registra no servidor o interesse em mudanças de determinados valores (uma chave, um prefixo, o estado de um nó). | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |
| [Gossip Dissemination](/architecture/distributed-systems/cluster-management/gossip-dissemination) | No Gossip Dissemination, cada nó guarda os metadados que conhece sobre o cluster (membership, estado de nós, informações de partições) e, em intervalos regulares, por exemplo a cada segundo, escolhe um ou poucos nós aleatórios e troca com eles o que sabe. | [`Scalability`](/tags/scalability) [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [Emergent Leader](/architecture/distributed-systems/cluster-management/emergent-leader) | Em clusters peer-to-peer, todos os nós são iguais e não existe uma eleição explícita como em Leader and Followers. | [`Availability`](/tags/availability) [`Fault Tolerance`](/tags/fault-tolerance) |

## Communication between Nodes (3) {#node-communication}

| Padrão | Resumo | Etiquetas |
| --- | --- | --- |
| [Single-Socket Channel](/architecture/distributed-systems/node-communication/single-socket-channel) | O Single-Socket Channel usa uma única conexão TCP, aberta e mantida de forma duradoura, para todo o tráfego entre um par de nós, por exemplo entre um follower e o seu líder. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Performance`](/tags/performance) |
| [Request Batch](/architecture/distributed-systems/node-communication/request-batch) | O Request Batch agrupa várias requisições pequenas em uma única mensagem de rede, enviada de uma vez a um nó do cluster. | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |
| [Request Pipeline](/architecture/distributed-systems/node-communication/request-pipeline) | O Request Pipeline faz um nó enviar várias requisições a outro nó sem esperar a resposta de cada uma antes de enviar a seguinte. | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |

## Por etiqueta

### Consistency (16)

[Leader and Followers](/architecture/distributed-systems/data-replication/leader-and-followers), [Majority Quorum](/architecture/distributed-systems/data-replication/majority-quorum), [Generation Clock](/architecture/distributed-systems/data-replication/generation-clock), [High-Water Mark](/architecture/distributed-systems/data-replication/high-water-mark), [Paxos](/architecture/distributed-systems/data-replication/paxos), [Replicated Log](/architecture/distributed-systems/data-replication/replicated-log), [Singular Update Queue](/architecture/distributed-systems/data-replication/singular-update-queue), [Request Waiting List](/architecture/distributed-systems/data-replication/request-waiting-list), [Versioned Value](/architecture/distributed-systems/data-replication/versioned-value), [Version Vector](/architecture/distributed-systems/data-replication/version-vector), [Two-Phase Commit](/architecture/distributed-systems/data-partitioning/two-phase-commit), [Lamport Clock](/architecture/distributed-systems/distributed-time/lamport-clock), [Hybrid Clock](/architecture/distributed-systems/distributed-time/hybrid-clock), [Clock-Bound Wait](/architecture/distributed-systems/distributed-time/clock-bound-wait), [Consistent Core](/architecture/distributed-systems/cluster-management/consistent-core), [Single-Socket Channel](/architecture/distributed-systems/node-communication/single-socket-channel)

### Durability (6)

[Write-Ahead Log](/architecture/distributed-systems/data-replication/write-ahead-log), [Segmented Log](/architecture/distributed-systems/data-replication/segmented-log), [Low-Water Mark](/architecture/distributed-systems/data-replication/low-water-mark), [High-Water Mark](/architecture/distributed-systems/data-replication/high-water-mark), [Replicated Log](/architecture/distributed-systems/data-replication/replicated-log), [Two-Phase Commit](/architecture/distributed-systems/data-partitioning/two-phase-commit)

### Availability (7)

[HeartBeat](/architecture/distributed-systems/data-replication/heartbeat), [Majority Quorum](/architecture/distributed-systems/data-replication/majority-quorum), [Follower Reads](/architecture/distributed-systems/data-replication/follower-reads), [Version Vector](/architecture/distributed-systems/data-replication/version-vector), [Lease](/architecture/distributed-systems/cluster-management/lease), [Gossip Dissemination](/architecture/distributed-systems/cluster-management/gossip-dissemination), [Emergent Leader](/architecture/distributed-systems/cluster-management/emergent-leader)

### Fault Tolerance (12)

[Write-Ahead Log](/architecture/distributed-systems/data-replication/write-ahead-log), [Leader and Followers](/architecture/distributed-systems/data-replication/leader-and-followers), [HeartBeat](/architecture/distributed-systems/data-replication/heartbeat), [Majority Quorum](/architecture/distributed-systems/data-replication/majority-quorum), [Generation Clock](/architecture/distributed-systems/data-replication/generation-clock), [Paxos](/architecture/distributed-systems/data-replication/paxos), [Replicated Log](/architecture/distributed-systems/data-replication/replicated-log), [Consistent Core](/architecture/distributed-systems/cluster-management/consistent-core), [Lease](/architecture/distributed-systems/cluster-management/lease), [Gossip Dissemination](/architecture/distributed-systems/cluster-management/gossip-dissemination), [Emergent Leader](/architecture/distributed-systems/cluster-management/emergent-leader), [Single-Socket Channel](/architecture/distributed-systems/node-communication/single-socket-channel)

### Scalability (8)

[Follower Reads](/architecture/distributed-systems/data-replication/follower-reads), [Fixed Partitions](/architecture/distributed-systems/data-partitioning/fixed-partitions), [Key-Range Partitions](/architecture/distributed-systems/data-partitioning/key-range-partitions), [Consistent Core](/architecture/distributed-systems/cluster-management/consistent-core), [State Watch](/architecture/distributed-systems/cluster-management/state-watch), [Gossip Dissemination](/architecture/distributed-systems/cluster-management/gossip-dissemination), [Request Batch](/architecture/distributed-systems/node-communication/request-batch), [Request Pipeline](/architecture/distributed-systems/node-communication/request-pipeline)

### Performance (14)

[Segmented Log](/architecture/distributed-systems/data-replication/segmented-log), [Low-Water Mark](/architecture/distributed-systems/data-replication/low-water-mark), [Singular Update Queue](/architecture/distributed-systems/data-replication/singular-update-queue), [Request Waiting List](/architecture/distributed-systems/data-replication/request-waiting-list), [Follower Reads](/architecture/distributed-systems/data-replication/follower-reads), [Versioned Value](/architecture/distributed-systems/data-replication/versioned-value), [Fixed Partitions](/architecture/distributed-systems/data-partitioning/fixed-partitions), [Key-Range Partitions](/architecture/distributed-systems/data-partitioning/key-range-partitions), [Hybrid Clock](/architecture/distributed-systems/distributed-time/hybrid-clock), [Clock-Bound Wait](/architecture/distributed-systems/distributed-time/clock-bound-wait), [State Watch](/architecture/distributed-systems/cluster-management/state-watch), [Single-Socket Channel](/architecture/distributed-systems/node-communication/single-socket-channel), [Request Batch](/architecture/distributed-systems/node-communication/request-batch), [Request Pipeline](/architecture/distributed-systems/node-communication/request-pipeline)

### Reliability (1)

[Idempotent Receiver](/architecture/cloud-design-patterns/messaging/idempotent-consumer)
