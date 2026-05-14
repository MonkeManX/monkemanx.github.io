---
title: 'Diagnostic Test Generation for Fault Localization in Printed Neuromorphic Circuits'
date: 2026-05-14 14:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Diagnostic Test Generation for Fault Localization in Printed Neuromorphic Circuits

**Link to Paper:** https://past.date-conference.com/proceedings-archive/2026/DATA/1197.pdf 

**Date:** 2026

**Paper Type:** Test Generation, Fault Detection, Fault Localization, Neuromorphic Computing, Neural Networks, Printed Electronics

**Short Abstract:**
Printed electronics enable cheap, flexible, and lightweight devices, but their unreliable manufacturing process makes them prone to defects. This paper proposes a diagnostic testing framework for printed neuromorphic circuits that not only detects faults but also localizes them more effectively, achieving significantly higher diagnostic coverage and reducing undetectable subcircuits compared to traditional methods.



# 1. Preliminaries

## 1.1. Background: What are printed neuromorphic circuits?

Printed electronics are circuits made by *printing conductive and semiconductive materials* onto flexible substrates.

Examples:
* wearable sensors
* smart packaging
* disposable IoT devices

Unlike silicon chips:
* they are cheap
* flexible
* printable over large areas

But:
* manufacturing is noisy and unreliable
* defects happen often

The paper focuses on **printed neuromorphic circuits (pNCs)**:
* analog neural-network-like circuits
* physically implement ML models
* used for ultra-low-power edge AI

These are built from reusable analog primitives like:
* resistor crossbars
* nonlinear activation blocks (`p-tanh`, `p-inv`)


## 1.2. The reliability problem

Printed manufacturing creates defects such as:
* opens (broken connections)
* shorts (accidental connections)
* parameter drift

Because these circuits are analog and densely interconnected:
* tiny defects can drastically change behavior.

Worse:
* these systems are usually **black boxes**
* you can only observe inputs and outputs
* no scan chains or internal probes like digital chips

So debugging is hard.


## 1.3. Traditional ATPG vs this paper

Traditional chip testing uses:
* **ATPG** = Automatic Test Pattern Generation

ATPG generates inputs that reveal faults.

Example:

If input `x = 1011` causes bad output,
then that test detects a fault.

But detection alone is insufficient.

Two different faults might produce:
* the same wrong output

Then you know:
* something is broken
* but not *where*.

This paper extends ATPG into:
* **DTPG** = Diagnostic Test Pattern Generation

The goal becomes:

> Generate test inputs that make different faults behave differently.


# 2. Method 

## 2.1 Setup

They assume:
* black-box access only
* one fault at a time (single-fault assumption)

They model faulty versions of the circuit:
$$
{y_f(\cdot)}_{f \in F}
$$

where:
* \(y(\cdot)\) = correct circuit
* \(y_f(\cdot)\) = circuit with fault (f)

They want to find a compact set of test inputs:

$$
X = {x_1, x_2, ..., x_m}
$$

that:
1. detect faults
2. distinguish faults from different primitives


## 2.2. Objective function

They optimize:
$$
L(X) = L_{det}(X) + \lambda L_{loc}(X)
$$

where:
* \(L_{det}\) = fault detection objective
* \(L_{loc}\) = fault localization objective
* \(\lambda\) balances the two

The detection part tries to maximize:

$$
d(y_x^0, y_x^f)
$$

meaning:
* difference between correct output
* and faulty output

If the outputs differ strongly, the fault is easy to detect.


In addition, they want faults from *different primitives* to produce distinguishable outputs.

They maximize:
$$
d(y_x^f, y_x^{f'})
$$

when:
* (f) and (f') belong to different primitives.

So:
* if resistor block A fails,
* and resistor block B fails,

the generated tests try to make their behaviors visibly different.


For optimization purpose they use *Adam*.

## 2.3. Diagnostic coverage

They define a new metric:

A primitive pair is:
* detectable if faults change output
* distinguishable if their faulty signatures differ

Then:
$$
\text{DiagCov} =
\frac{
\text{distinguishable primitive pairs}
}{
\text{detectable primitive pairs}
}
$$


# 3. Results

They evaluate on:
* 10 UCI datasets
* mapped onto printed neuromorphic circuits

Compared against:
1. sensitivity-based data-driven testing
2. previous ATPG method (detection only)

Their method achieved:
* +20.7% better diagnostic coverage
* 3.6× fewer undetected primitives


---

## Some Thoughts 

Thoughts:
* They do not detect where exactly in the neural network the fault is. Rather, they differentiate between different faults by maximizing the distance between their output signatures.
* These faults are based on previously simulated real fault models, allowing the system to infer what kind of fault it is.
* A limitation of this paper is that it can only detect faults that were already simulated; it cannot detect unknown faults.
* Furthermore, it cannot locate the precise physical location where the fault occurs.
