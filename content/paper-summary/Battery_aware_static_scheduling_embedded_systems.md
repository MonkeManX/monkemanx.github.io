---
title: 'Battery-Aware Static Scheduling for Distributed Real-Time Embedded Systems'
date: 2026-05-23 18:00:00
tags: ["paper-summary", "battery"]
---

**Paper Title:** Battery-Aware Static Scheduling for Distributed Real-Time Embedded Systems

**Link to Paper:** https://dl.acm.org/doi/10.1145/378239.378553

**Date:** 22. Jun. 2001 

**Paper Type:** Dynamic power management, heterogeneous computing, multicore architectures, multiprocessor systems-on-chip (MPSoCs). thermal management.

**Short Abstract:**
This paper proposes two battery-aware scheduling techniques for distributed real-time embedded systems that improve battery lifespan by reducing and smoothing power consumption while still meeting timing and task-dependency constraints. One method optimizes the discharge power profile directly, while the other uses voltage scaling with efficient slack-time reallocation, achieving battery-life improvements of up to 76% in experiments.


## Background and Motivation

Traditional embedded scheduling research mainly focused on meeting deadlines and reducing energy consumption. Prior work had already shown that battery efficiency worsens when:

* discharge current is high,
* current fluctuates heavily,
* power spikes occur frequently.

The authors build on earlier battery studies showing that two systems with the same average power consumption can still have very different battery lifetimes depending on the shape of their discharge profile.

The system model used in the paper represents applications as periodic task graphs:

* nodes represent tasks,
* edges represent communication between tasks,
* deadlines must always be satisfied,
* task graphs may execute at different rates (multi-rate systems).

The challenge is therefore to create schedules that are:

* real-time correct,
* precedence-safe,
* battery-efficient.

## Battery Behavior Model

The paper models battery efficiency using a utilization factor (c(I)), which measures how much usable capacity remains at a given discharge current (I).

The effective battery drain depends on both:

* the average current level,
* the distribution of current over time.

The authors rely on empirical battery behavior models such as Peukert’s law:

$$
c(I)=\frac{k}{I^{\alpha}}
$$

This equation captures the fact that higher discharge current reduces usable battery capacity.

The paper also uses a power-based formulation where the “actual” battery power consumed depends on the entire discharge profile over time, not simply average power.

A major implication is:

* minimizing peak power and current variance improves battery lifespan,
* even if total energy consumption remains unchanged.

## First Scheduling Scheme: Battery-Aware Power Profile Optimization

The first scheduling method focuses on reshaping the discharge power profile without changing hardware voltage levels.

The algorithm begins with a valid static schedule and applies schedule transformations to reduce power spikes and flatten the load distribution.

The two major techniques are:

* local schedule transformations,
* global shifting.

### Local Schedule Transformations

The scheduler examines high-power time intervals and tries to reduce peaks by:

* swapping neighboring tasks,
* shifting tasks forward or backward,
* moving communication events.

These transformations are only allowed if they:

* preserve task precedence,
* preserve deadlines,
* reduce the battery cost metric.

The scheduler repeatedly improves the schedule until no further improvement is possible.

The paper demonstrates that simply rearranging tasks can significantly reduce instantaneous power spikes and improve battery life.

### Global Shifting

Local optimizations alone may get stuck in poor solutions. To address this, the paper introduces a global shifting stage.

This stage:

* pushes tasks toward later execution times,
* increases scheduling flexibility,
* creates opportunities for later local optimizations.

The algorithm tries to keep average power below a threshold while moving tasks.

This combination of global and local optimization produces smoother discharge profiles and lower peak power consumption.

## Second Scheduling Scheme: Variable-Voltage Scheduling

The second scheme assumes the system contains voltage-scalable processors.

Voltage scaling reduces processor speed and supply voltage to save energy.

The paper uses standard CMOS power relationships:

$$
p=\frac{1}{2}NV_{dd}^{2}f
$$

This shows that processor power scales quadratically with supply voltage, making voltage scaling highly effective.

### Slack-Time Reallocation

The key innovation is efficient redistribution of slack time.

Slack time is unused execution time before deadlines. The scheduler reallocates slack across tasks so that more tasks can run at reduced voltage.

The algorithm:

* computes available slack,
* redistributes it near-optimally,
* stretches task execution durations,
* lowers processor voltage safely,
* preserves deadlines.

This not only reduces average power consumption, but also smooths the overall power profile.

The authors formulate an optimization problem minimizing total energy under timing constraints.

## Experimental Results

The experiments use randomly generated task graphs and compare several scheduling approaches.

### Battery-Aware Scheduling Without Voltage Scaling

Optimizing only the discharge power profile improved battery lifespan by:

* 8.5%–16.6% in moderate conditions,
* 12.6%–28.8% in harsher battery conditions.

The gains became larger when battery capacity was limited or discharge conditions were more demanding.

This demonstrates that power-profile shaping alone can meaningfully improve battery efficiency.

### Variable-Voltage Scheduling Results

The voltage-scaling scheme produced much larger improvements.

Compared to non-voltage-scalable scheduling:

* average power consumption decreased by up to 38%,
* battery lifespan improved by up to 76%.

Compared to voltage scaling *without* slack redistribution:

* battery lifespan improved by up to 56%.

The results also showed that considering the *shape* of the power profile gave larger gains than considering average power alone.

This confirms the paper’s central argument that flattening discharge patterns is critically important for battery-aware design.

## Key Takeaway

The paper argues that battery-aware embedded scheduling should not only minimize energy usage, but also carefully manage *when* energy is consumed.

A smoother, flatter discharge profile:

* reduces effective battery loss,
* improves usable battery capacity,
* significantly extends system lifetime.

By combining schedule reshaping with voltage scaling and slack redistribution, the authors show that substantial battery-life improvements are possible without violating real-time guarantees.
