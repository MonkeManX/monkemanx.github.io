---
title: 'The Sybil Attack'
date: 2025-07-03 14:00:00
tags: ["paper-summary", "Decentralized Systems"]
---

**Paper Title:** The Sybil Attack  
**Link to Paper:** https://dl.acm.org/doi/10.5555/646334.687813  
**Date:** 07. March 2002  
**Paper Type:** Networks, Architectures, Decentralized Systems   
**Short Abstract:**   
In this paper, the authors introduce the Sybil attack — a method by which attackers can forge multiple identities in a decentralized system. They demonstrate that Sybil attacks are always possible in realistic scenarios.


## 1. Introduction

The central thesis of this paper is that in a distributed system, it is always possible, outside of impractical systems, for an unfamiliar entity to present more than one identity.

Peer-to-peer systems rely on multiple independent entities to mitigate threats. Examples include:
* Storage replication systems such as **CFS**
* File-sharing systems like **Kademlia**

Such systems need to ensure that distinct identities correspond to distinct physical or logical entities. Otherwise, a malicious participant can deceive the system by creating a sufficient number of fake identities—for instance, to control replication in CFS or to manipulate routing in Kademlia.

Instead of using a distributed approach, a centralized system could be used—for example, with an explicit certification authority or a system like DNS. However, these approaches rely on a trusted third party to establish identity, which is not always feasible.


## 2. Formal Model

The model consists of:

* A set **E** of entities, which includes:
  * A subset **C** of honest (correct) entities/clients
  * A subset **F** of malicious (faulty) entities/clients
* A broadcast communication cloud
* A communication "pipe" connecting each entity to the cloud

Entities communicate via messages, where a message is a bit string. An entity sends a message through its pipe to the cloud, and the message is then delivered to all other entities within a bounded amount of time. Message delivery is guaranteed, but order is not.

Each entity can perform operations whose computational complexity is polynomial in *n*, where *n* is a predefined security parameter of the system.

Direct links between entities can be established through the cloud using public/private keys. No direct physical connection exists.


## 3. Results

The authors differentiate between:
* **Directly validated identities**
* **Indirectly validated identities**

For both cases, they show that:
* A faulty entity can counterfeit a constant number of identities
* Each correct identity must be validated **simultaneously** as it is presented; otherwise, a faulty entity can counterfeit an **unbounded** number of identities

These issues pose significant challenges to the scalability of decentralized systems:
* In the first case, resource discrepancies can exacerbate the problem
* In the second case, the requirement for parallel validation limits the number of nodes that can be active in the network at the same time

For direct validation, the key lemmas are:

> **Lemma 1**
> If *p* is the ratio of resources available to a faulty entity *f* compared to the resources of a minimally capable (honest) entity, then *f* can present *g = |p|* distinct identities to a local entity *l*.

This gives a lower bound on the potential damage a faulty entity can cause. There are three strategies to enforce this bound, depending on which resource is limited:

* **Bandwidth limitation**: require a challenge that must be broadcast within a certain time interval
* **Storage limitation**: require the storage of a large amount of data
* **Computation limitation**: require solving a computational puzzle, e.g., a hash function such that `hash(x‖y‖z) = 0`

> **Lemma 2**
> If a local entity *l* accepts identities that are not validated simultaneously, then a single faulty entity *f* can present an arbitrarily large number of distinct identities to *l*.

The lemmas for **indirect validation** are analogous.


## 4. Conclusion

When designing decentralized peer-to-peer systems, one must always consider the **minimally capable entity**, as it defines:
* Who is able to participate
* How vulnerable the system is to a Sybil attack
