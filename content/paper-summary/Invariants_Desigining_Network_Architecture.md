---
title: 'Invariants: a new design methodology for network architectures'
date: 2025-05-06
tags: ["paper-summary", "telematics"]
---

**Paper Title:** Invariants: a new design methodology for network architectures  
**Link to Paper:** https://dl.acm.org/doi/10.1145/1016707.1016719  
**Date:** June 1963     
**Paper Type:** Telematics, Network Architetcure, Methodology  
**Short Abstract:**   
This paper presents a new methodology for designing network architecture based on invariants, which are fixed design points


## 1. Introduction

Any given system consists of a number of standards that provide functionality. But over time, as more standards and features are added, existing systems can no longer support new capabilities and become obsolete.
The characteristic that limits this evolution is often referred to as the *lowest common denominator*, *fixed point*, or **invariant**.

The Internet is a large system that is very flexible — it can accommodate new protocols, applications, and link technologies.
Despite this flexibility, the Internet has some invariants — for example, the unique IP addresses assigned to interfaces. A trivial change to the address format cannot be easily accommodated.

This paper identifies invariants as the central limiting factor in system design. We can differentiate between *explicit* and *implicit* invariants.
**Explicit invariants** are planned characteristics resulting from deliberate decisions. With careful planning, these explicit invariants can offer significant benefits.
**Implicit invariants**, on the other hand, are unplanned side effects. They evolve when a network-wide approach is needed for a particular function, but instead of explicit support, the implementation develops informally during deployment.

All systems — regardless of the design process — will have invariants. But identifying and understanding them will help in designing better, more adaptable systems.


## 2. Invariants

The foundational principles of the Internet include:

* Packet switching
* Global self-addressing of datagrams
* The end-to-end principle

Together, these principles have created a highly flexible system that works with fast optical links, slow modems, and unreliable (lossy) wires.
Other aspects of the Internet are less flexible, especially end-to-end addressing. IPv4, for instance, provides $2^{32}$ unique addresses. Although its successor, IPv6, offers vastly more, adoption has been slow.

**Invariants** are aspects of a design that limit its changeability — the fixed points of the system.

### 2.1. Example: Internet Invariants

The most prominent invariant of the Internet is IPv4 addressing, which identifies location in the network topology.
Several modern functionalities complicate this:

* **Multi-homing**, due to the dual use of IP addresses for both identity and location
* **NAT (Network Address Translation)**, which breaks end-to-end connectivity

The Internet transport layer has another invariant: **port numbers**. Originally a flow identifier, their role has expanded and they have become an implicit invariant.

Common to Internet invariants is that they are conceptually simple but deeply embedded, which makes them hard to change.

### 2.2. Example: Cellular Network Invariants

This section focuses on the *Universal Mobile Telecommunications System (UMTS)*.

The primary invariant is the concept of a hardware token — the **SIM number**. Like IP addresses, it acts as an identifier, though the two differ widely in scope and usage.

The second invariant is the **set of services** provided during a particular session.

Both of these invariants are **explicit**, resulting from deliberate design choices.


## 3. Invariant-Based Architecture Evaluation

Identifying invariants is difficult — there is no systematic process. It requires experience and deep understanding. However, some general criteria can help assess the quality of invariants:

* **Is the set complete?**
  A network design that overlooks key requirements is incomplete and vulnerable to the emergence of new, unintended implicit invariants.
* **Is the set independent?**
  Each invariant should serve a distinct function. Redundant or overlapping invariants complicate the design unnecessarily.

Other useful questions include:

* Does an invariant affect many components, or just a few?
* Does it impact many aspects of the architecture, or only limited parts?
* Does it affect hardware (silicon) or just software?
* Does it have security or privacy implications?
* Does it allow for flexibility?

The purpose of evaluating invariants is to determine which architectural design will best adapt to future changes.


## 4. Invariant-Aware Architecture Design

Using invariants, we can outline the following method for designing architectures:

1. Identify the architecture’s invariants
2. Evaluate the invariants
3. Revise the architecture based on the evaluation
4. Repeat the process
