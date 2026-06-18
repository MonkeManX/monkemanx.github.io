---
title: 'Compact Test Pattern Generation For Multiple Faults In Deep Neural Networks'
date: 2026-06-17 10:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Compact Test Pattern Generation For Multiple Faults In Deep Neural Networks

**Link to Paper:** https://ieeexplore.ieee.org/document/10137004

**Date:** 2023

**Paper Type:** Test Generation, Deep Neural Networks, Hardware Faults, Fault Detection

**Short Abstract:**
This paper proposes a compact test pattern generation approach to detect *multiple* bit-level weight faults in DNNs. This method constructs test patterns that induce misclassification. The approach uses a min-max optimization to maximize the minimum output difference across a fault list and iteratively covers faults with a compact set of test patterns.

## 1. Introduction

DNNs require significant computational resources, motivating specialized accelerators such as TPUs and Memristor crossbar arrays. However, hardware faults in these accelerators threaten inference accuracy and reliability. Existing testing approaches typically detect faults by measuring output deviations from the fault-free case, but this has two practical shortcomings:

1. **Black-box testing constraints:** In many scenarios (e.g., DNNs as Intellectual Property), internal model parameters are inaccessible. Only input-output behavior can be observed.
2. **Output deviation instability:** Normal runtime variations can cause small output fluctuations that are indistinguishable from fault-induced deviations.

The paper argues that a fault is only practically relevant if it causes a **misclassification** — a change in the predicted label. Faults that merely shift output probabilities without changing the argmax can be safely ignored. This motivates generating test patterns that specifically trigger label changes in the presence of faults.

## 2. Methodology

### 2.1 Fault Model

The paper targets **bit-level fault injection** in weight representations. The fault model is defined by two parameters:

- **pw** — the percentage of weights that have bits altered
- **pb** — the percentage of bits flipped *per affected weight*

A fault pattern is therefore a specific random instance of altering weights at the bit level. Since each instance affects multiple weights and multiple bit positions, this constitutes a **multiple fault model**, distinct from single-fault approaches.

A fault list \(F(pw, pb) = \{f_n \mid n = 1, \dots, N\}\) is generated for each \((pw, pb)\) combination, where each \(f_n\) is a specific randomly-generated fault pattern applied to a network instance \(\text{Net}_{f_n}\).

### 2.2 Test Pattern Generation

The core objective is to find test inputs that cause **label mismatch** between the fault-free and faulty networks:

\[
o(x, f) := \left\| \text{Softmax}(\text{Net}(x)) - \text{Softmax}(\text{Net}_f(x)) \right\|_2^2
\]

However, rather than targeting individual faults, the paper proposes a **min-max optimization** to generate test patterns that detect *many* faults simultaneously:

\[
x^\star = \arg\max_{x \in X} \min_{f \in F} o(x, f)
\]

This maximizes the *lower bound* on the objective across all faults in the fault list. By doing so, a single test pattern \(x^\star\) is effective against many fault patterns in \(F\).

### 2.3 Iterative Compaction Algorithm

The algorithm (Algorithm 1 in the paper) works as follows:

1. Generate a fault list \(F\) for chosen \((pw, pb, N)\).
2. Define the set of faults *covered* by a test pattern \(x\) as those where the argmax label changes.
3. **Repeat** until all faults in \(F\) are covered:
   - Solve the min-max optimization to find \(x^\star_k\).
   - Remove covered faults \(F_c(x^\star_k)\) from \(F\).
   - Add \(x^\star_k\) to the test set \(X\).
4. Return the compact test set \(X\).

This approach naturally produces a **compact** test set — each new test pattern is optimized to cover as many remaining faults as possible.

## 3. Experiments

### 3.1 Setup

The method was evaluated on:
- **Datasets:** MNIST and CIFAR-10
- **Models:** MLP (3 fully-connected layers, size 20), LeNet-5 (7 layers), ConvNet-7 (7 layers, custom)
- **Weights:** Floating-point 32-bit, implemented in PyTorch
- **Fault parameters:** \(pw \in \{5\%, 10\%\}\), \(pb \in \{50\%, 70\%, 100\%\}\)
- **Fault list sizes:** 50, 100, 150, 200

### 3.2 Results

| Model | Dataset | pw | pb | Fault Patterns | Generated Tests | Compaction Ratio | Fault Coverage (Targeted) | Fault Coverage (Unseen) |
|-------|---------|-----|-----|---------------|----------------|-----------------|-------------------------|------------------------|
| MLP | MNIST | 5% | 100% | 50 | 10 | 5.0× | 100% | 98.6% |
| MLP | MNIST | 10% | 70% | 100 | 9 | 11.1× | 100% | 98.7% |
| MLP | MNIST | 10% | 50% | 150 | 13 | 11.5× | 100% | 98.2% |
| LeNet-5 | MNIST | 5% | 100% | 50 | 4 | 12.5× | 100% | 97.8% |
| LeNet-5 | MNIST | 10% | 70% | 150 | 24 | 6.2× | 100% | 98.6% |
| LeNet-5 | MNIST | 10% | 50% | 200 | 31 | 6.4× | 100% | 98.7% |
| ConvNet-7 | CIFAR-10 | 5% | 100% | 50 | 2 | 25.0× | 100% | 99.9% |
| ConvNet-7 | CIFAR-10 | 10% | 70% | 100 | 10 | 10.0× | 100% | 99.8% |
| ConvNet-7 | CIFAR-10 | 10% | 50% | 200 | 21 | 9.5× | 100% | 99.5% |

Key findings:
- **100% fault coverage** on targeted fault patterns across all settings.
- **High compaction ratios** — e.g., 2 test patterns covering 50 fault patterns on ConvNet-7 (25×).
- **Excellent generalization to unseen faults** — up to 99.9% coverage on 1000 unseen fault patterns.
- Only a small number of iterations needed (as few as 6 for ConvNet-7).

The accuracy degradation analysis (Fig. 1) showed that flipping 50% of bits in only 5% of weights already causes significant accuracy drops, confirming the relevance of the fault model.

## 4. Conclusion

The paper proposes a compact test pattern generation approach for detecting multiple bit-level weight faults in DNNs. By maximizing the minimum output difference across a fault list and iteratively covering faults, it produces small test sets with high detection rates. The generated patterns achieve 100% coverage on targeted faults and up to 99.9% on unseen faults, with compaction ratios as high as 25×.

---

### Thoughts

- **Limitations:**
  - The fault model assumes random bit flips, realistic fault distributions (e.g., spatial locality, bit-position bias) are not considered.
  - Only small-scale models tested (MLP, LeNet-5, ConvNet-7), scalability to modern architectures (ResNet, Transformers) is unclear.
  - Single (pw, pb) combination per fault list, real hardware faults may span multiple (pw, pb) regimes simultaneously.

---

## Comparison with Related ATPG Approaches

This paper sits alongside three other ATPG-related papers in the research area. The key differences are:

| Aspect | **This Paper** (Moussa et al. 2023) | **ATPG & Compaction for DNN** (Zhang et al. 2023) | **ATPG for Printed Neuro Circuits** (2025) | **Diagnostic Test for pNCs** (2026) |
|--------|--------------------------------------|---------------------------------------------------|------------------------------------------|--------------------------------------|
| **Target** | DNN accelerators (silicon) | DNNs (software model) | Printed neuromorphic circuits | Printed neuromorphic circuits |
| **Fault Model** | Multiple bit-level weight faults (pw, pb) | Stuck-at neuron/filter output | Crossbar, p-tanh, p-inv (analog) | Crossbar, p-tanh, p-inv (analog) |
| **Fault Scope** | Multiple faults (simultaneous) | Single fault per test | Single fault assumption | Single fault assumption |
| **Optimization** | Min-max (max lower bound) | Gradient-based (single fault) | Gradient-based (KL divergence) | Gradient-based (detection + localization) |
| **Compaction** | Iterative covering via min-max | K-means + greedy set cover | Not explicitly addressed | Not explicitly addressed |
| **Key Metric** | Compaction ratio, fault coverage | Fault coverage | Fault coverage (%) | Diagnostic coverage |
| **Testing Scenario** | Black-box (labels only) | White-box (internal layers) | Black-box (voltages) | Black-box (diagnostic) |

The main conceptual distinction is that **Moussa et al. treat the fault detection problem as a min-max covering problem**, each test pattern is explicitly optimized to handle *many* simultaneous faults. In contrast, the other works target single faults and rely on clustering or greedy selection for compaction. 
