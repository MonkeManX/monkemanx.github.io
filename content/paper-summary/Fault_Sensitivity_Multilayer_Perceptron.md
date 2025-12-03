---
title: 'Fault Sensitivity Analysis of Printed Bespoke Multilayer Perceptron Classifiers'
date: 2025-12-03 12:00:00
tags: ["paper-summary", "circuits"]
---

**Paper Title:** Fault Sensitivity Analysis of Printed Bespoke Multilayer Perceptron Classifiers

**Link to Paper:** https://ieeexplore.ieee.org/document/10567964

**Date:** 20. May 2024

**Paper Type:** SNN, Printed Electronics, Circuit Design

**Short Abstract:**
This paper studies how neural networks in printed flexible circuits fail when they contain defects. This is important because printed circuits have a higher failure rate than silicon-based circuits.

## 1. Introduction

Printed electronics (PE) offer low cost, flexibility, and customized fabrication. That is why they are very popular in IoT devices, such as wearables and smart packaging.
Until now, the reliability of printed neural networks has not been studied much, whereas that of silicon-based spiking neural networks (SNNs) has been examined far more extensively.

## 2. Preliminaries

Printed electronics use additive printing instead of silicon lithography. This is very cheap but has lower precision, resulting in more variability and thus more defects.

Analog multilayer perceptrons (p-AMLPs) use in-circuit resistor crossbars for weights, inverter circuits for negative weights, and analog tanh-like circuits for activation functions. Importantly, they do not need expensive ADC converters.

Printed digital multilayer perceptrons (p-DMLPs) can be optimized using bespoke architectures; that is, circuits are highly tailored to one specific dataset and model. Approximate computing (AxC) can also be used to reduce area and power by making multipliers approximate.

We consider two types of faults: catastrophic faults and parametric faults.
Parametric faults are caused by components not having the precise value they should have—for example, resistors drifting to incorrect values.
Catastrophic faults can be classified as stuck-open and stuck-short faults. A stuck-open fault represents a broken connection and can be modeled as a very large resistor; a stuck-short fault is a short circuit and can be modeled as a very small resistor.

## 3. Evaluation

Fault injection in p-AMLP:
To simulate crossbar faults, a conductance mask is applied to the weights, setting them either to 0 (stuck open) or infinity (stuck short).
Nonlinear faults can be modeled by injecting transistor-level faults, which can be simulated in SPICE. Faults can be inserted using Monte Carlo sampling.

Training for p-AMLP is done using four strategies:

1. **Nominal:** standard training
2. **Variation-aware:** modeling parameter variation during training
3. **Dropout:** randomly disabling nodes during training
4. **Variation-aware + dropout:** combined method

Fault injection for p-DMLP is done by extracting a netlist of wires. A random wire is selected as faulty, and it becomes stuck at 0 or 1. Full gate-level simulation is used to compute classification accuracy under faults.

For architectures, three families are considered:

* **Customization level:** generic, bespoke
* **Approximation level:** pow2, pow2 + approximate accumulate, AxAll
* **Dropout**

## 5. Conclusion

Bespoke digital printed MLPs are the most fault-tolerant overall. Approximate bespoke circuits, while small and efficient, are more fragile. Analog printed MLPs are very vulnerable to catastrophic faults and require better fault-tolerant design strategies. Dropout improves robustness for both analog and digital systems but does not solve the fundamental weaknesses of analog PE.
