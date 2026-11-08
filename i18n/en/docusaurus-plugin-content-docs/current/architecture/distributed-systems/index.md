---
title: "Patterns of Distributed Systems"
sidebar_label: "Distributed Systems"
---

# Patterns of Distributed Systems

Personal catalog based on Unmesh Joshi's [Catalog of Patterns of Distributed Systems](https://martinfowler.com/articles/patterns-of-distributed-systems/), published on Martin Fowler's site, which summarizes the *Patterns of Distributed Systems* book (2023). The groups follow the parts of the book. Each pattern has a description, the problems it solves, when to use it, trade-offs, tags (distributed guarantees), and a Mermaid diagram.

Patterns marked with ★ are shared with another catalog: this catalog points to the original document, revised with content from this source.

Total: 30 patterns in 5 groups. Tags: Distributed guarantee.

## Groups

- [Data Replication](#data-replication) (16)
- [Data Partitioning](#data-partitioning) (3)
- [Distributed Time](#distributed-time) (3)
- [Cluster Management](#cluster-management) (5)
- [Communication between Nodes](#node-communication) (3)

## Data Replication (16) {#data-replication}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Write-Ahead Log](/architecture/distributed-systems/data-replication/write-ahead-log) | The Write-Ahead Log (WAL) is an append-only log file on disk in which every state change is recorded as a command before it's applied to the in-memory data structures or the data files. | [`Durability`](/tags/durability) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Segmented Log](/architecture/distributed-systems/data-replication/segmented-log) | The Segmented Log splits the Write-Ahead Log into several smaller files, called segments, instead of keeping a single file that grows indefinitely. | [`Performance`](/tags/performance) [`Durability`](/tags/durability) |
| [Low-Water Mark](/architecture/distributed-systems/data-replication/low-water-mark) | The Low-Water Mark is an index (offset) in the log below which entries are no longer needed and can be safely discarded. | [`Performance`](/tags/performance) [`Durability`](/tags/durability) |
| [Leader and Followers](/architecture/distributed-systems/data-replication/leader-and-followers) | In Leader and Followers, one server in the cluster is chosen as the leader and makes decisions on behalf of the group: it receives writes, defines the order of updates, and propagates them to the other servers, the followers. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [HeartBeat](/architecture/distributed-systems/data-replication/heartbeat) | In HeartBeat, each server periodically sends other servers a short message saying it's still alive. | [`Availability`](/tags/availability) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Majority Quorum](/architecture/distributed-systems/data-replication/majority-quorum) | In Majority Quorum, an update is considered accepted by the cluster only when a majority of nodes acknowledge it. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [Generation Clock](/architecture/distributed-systems/data-replication/generation-clock) | The Generation Clock is a monotonically increasing number that identifies the current leader's "tenure". | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [High-Water Mark](/architecture/distributed-systems/data-replication/high-water-mark) | The High-Water Mark is an index in the log that marks the last entry successfully replicated to a majority (quorum) of nodes. | [`Consistency`](/tags/consistency) [`Durability`](/tags/durability) |
| [Paxos](/architecture/distributed-systems/data-replication/paxos) | Paxos is a consensus protocol, proposed by Leslie Lamport, that lets a group of nodes agree on a value despite node and network failures and without a fixed leader. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) |
| [Replicated Log](/architecture/distributed-systems/data-replication/replicated-log) | In Replicated Log, each node in the cluster keeps a Write-Ahead Log whose entries hold the user requests and the state needed for consensus. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Durability`](/tags/durability) |
| [Singular Update Queue](/architecture/distributed-systems/data-replication/singular-update-queue) | A Singular Update Queue uses a work queue processed by a single thread to apply state changes. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Request Waiting List](/architecture/distributed-systems/data-replication/request-waiting-list) | A Request Waiting List is a structure that maps a key to a callback function. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Idempotent Receiver](/architecture/cloud-design-patterns/messaging/idempotent-consumer) ★ | The Idempotent Consumer pattern designs message consumers so that processing the same message more than once has exactly the same effect as processing it a single time. | [`Reliability`](/tags/reliability) |
| [Follower Reads](/architecture/distributed-systems/data-replication/follower-reads) | In Follower Reads, writes still go through the leader, but read-only requests can be served by followers, especially the one closest to the client. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) [`Availability`](/tags/availability) |
| [Versioned Value](/architecture/distributed-systems/data-replication/versioned-value) | In Versioned Value, each value of a key is stored along with a version number that increases on every update. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Version Vector](/architecture/distributed-systems/data-replication/version-vector) | The Version Vector associates with each value of a key a vector holding one counter per node in the cluster. | [`Consistency`](/tags/consistency) [`Availability`](/tags/availability) |

## Data Partitioning (3) {#data-partitioning}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Fixed Partitions](/architecture/distributed-systems/data-partitioning/fixed-partitions) | Fixed Partitions keeps the number of logical partitions in a cluster constant. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) |
| [Key-Range Partitions](/architecture/distributed-systems/data-partitioning/key-range-partitions) | Key-Range Partitions divides the ordered key space into contiguous ranges, and each range becomes a logical partition. | [`Scalability`](/tags/scalability) [`Performance`](/tags/performance) |
| [Two-Phase Commit](/architecture/distributed-systems/data-partitioning/two-phase-commit) | Two-Phase Commit (2PC) writes data atomically across multiple nodes, typically in different partitions. | [`Consistency`](/tags/consistency) [`Durability`](/tags/durability) |

## Distributed Time (3) {#distributed-time}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Lamport Clock](/architecture/distributed-systems/distributed-time/lamport-clock) | Lamport Clock is a logical counter, a simple integer, kept by each node in the cluster to order events without relying on the wall clock. | [`Consistency`](/tags/consistency) |
| [Hybrid Clock](/architecture/distributed-systems/distributed-time/hybrid-clock) | Hybrid Clock (hybrid logical clock, or HLC) combines the system's wall clock with a logical counter. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |
| [Clock-Bound Wait](/architecture/distributed-systems/distributed-time/clock-bound-wait) | Clock-Bound Wait deals with the uncertainty of physical clocks in a cluster by waiting for it to pass. | [`Consistency`](/tags/consistency) [`Performance`](/tags/performance) |

## Cluster Management (5) {#cluster-management}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Consistent Core](/architecture/distributed-systems/cluster-management/consistent-core) | Consistent Core splits the cluster into two parts: a small group of nodes (typically three to five) that runs a consensus algorithm and provides fault-tolerant linearizability, and a data cluster, which can have hundreds of nodes. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Scalability`](/tags/scalability) |
| [Lease](/architecture/distributed-systems/cluster-management/lease) | A Lease is a grant of exclusive access to a resource for a limited time. | [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [State Watch](/architecture/distributed-systems/cluster-management/state-watch) | In State Watch, the client registers with the server its interest in changes to certain values (a key, a prefix, a node's state). | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |
| [Gossip Dissemination](/architecture/distributed-systems/cluster-management/gossip-dissemination) | In Gossip Dissemination, each node keeps the metadata it knows about the cluster (membership, node state, partition information) and, at regular intervals, for example every second, picks one or a few random nodes and exchanges what it knows with them. | [`Scalability`](/tags/scalability) [`Fault Tolerance`](/tags/fault-tolerance) [`Availability`](/tags/availability) |
| [Emergent Leader](/architecture/distributed-systems/cluster-management/emergent-leader) | In peer-to-peer clusters, all nodes are equal and there's no explicit election as in Leader and Followers. | [`Availability`](/tags/availability) [`Fault Tolerance`](/tags/fault-tolerance) |

## Communication between Nodes (3) {#node-communication}

| Pattern | Summary | Tags |
| --- | --- | --- |
| [Single-Socket Channel](/architecture/distributed-systems/node-communication/single-socket-channel) | Single-Socket Channel uses a single, long-lived TCP connection for all traffic between a pair of nodes, for example between a follower and its leader. | [`Consistency`](/tags/consistency) [`Fault Tolerance`](/tags/fault-tolerance) [`Performance`](/tags/performance) |
| [Request Batch](/architecture/distributed-systems/node-communication/request-batch) | Request Batch groups several small requests into a single network message and sends it to a cluster node in one go. | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |
| [Request Pipeline](/architecture/distributed-systems/node-communication/request-pipeline) | Request Pipeline lets a node send several requests to another node without waiting for the response to each one before sending the next. | [`Performance`](/tags/performance) [`Scalability`](/tags/scalability) |

## By tag

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
