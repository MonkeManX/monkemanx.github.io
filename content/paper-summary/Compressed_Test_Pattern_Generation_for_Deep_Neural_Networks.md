---
title: 'Compressed Test Pattern Generation for Deep Neural Networks'
date: 2026-06-18 09:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Compressed Test Pattern Generation for Deep Neural Networks

**Link to Paper:** https://doi.org/10.1109/TC.2024.3457738

**Date:** January 2025

**Paper Type:** Test Generation, Deep Neural Networks, Test Compression, Fault Detection

**Short Abstract:**
Deep Neural Networks (DNNs) on specialized accelerators are vulnerable to faults that impair accuracy. Many test patterns are required for certain fault types to achieve target coverage, increasing storage and testing overhead. While compression is typically applied *after* test generation, this paper argues it is more efficient when considered from the start. It proposes generating test patterns in a compressed form by representing each pattern as a **linear combination of a jointly-used set of basis patterns**. Only the coefficients need to be stored; the basis is regenerated on-demand from a pseudo-random seed. The method achieves up to 99.99% fault coverage and up to **307.2× compression** compared to storing full test patterns directly, outperforming random and adversarial test baselines.

## 1. Introduction

DNNs deployed on specialized accelerators (systolic arrays, memristive crossbars) face reliability challenges from manufacturing and runtime faults. Testing these accelerators requires effective test patterns, but achieving high fault coverage typically requires a large number of patterns, driving up storage costs.

The paper makes a key observation about existing approaches:

> *"Test pattern generation is normally a two-stage process. Namely, the generation of the test patterns and (optionally) afterwards the application of compression methods. However, compression could be more efficient when it is already considered in the first step."*

### Limitations of Related Work

The paper identifies several shortcomings in existing ATPG approaches:

1. **Adversarial-image methods** (e.g., Li et al. [17], FGSM-based) start from real images and add perturbations. They generate many images that are costly to store, and the adversarial constraint (imperceptibility) limits coverage.

2. **Output-deviation methods** (e.g., Liu et al. [20]) maximize the difference between fault-free and faulty output logits. This is unreliable because normal runtime variations (voltage fluctuations) can mimic fault-induced deviations. Crucially, these methods do not encourage a *different class label*, the pattern may produce a large deviation without actually causing misclassification.

3. **Two-stage generation+compaction** (e.g., Moussa et al. DATE 2023 [23]) generates test patterns first and compacts them afterwards, potentially missing efficiency gains from integrating compression into the generation step itself.

The paper proposes a **single-stage compressed generation** approach: test patterns are optimized directly in a low-dimensional coefficient space, yielding a compressed representation without a separate compression step.

## 2. Methodology

### 2.1 Fault Model: Neuron-Level Stuck-At Faults

The paper adopts **neuron-level stuck-at faults (SAF)** rather than bit-level weight faults. A neuron SAF means the output of a neuron (or filter in CNNs) is stuck at a fixed deterministic value \(v\):

\[
\text{Neuron}^l_j(x) = v \quad \forall x \in X
\]

The values \(v\) are chosen as the min or max of the activation function's range (e.g., 0 and 1 for Sigmoid, 0 and 6 for ReLU6).

**Rationale for neuron SAF over weight faults:** The paper performs fault simulation to justify this choice. Injecting weight faults at the bit level and observing neuron outputs shows that:
- Weight faults with <80% of weights affected at <90% bit-flip rate are **masked** (redundant, no observable effect).
- Weight faults exceeding these thresholds manifest as neuron outputs clamped to the activation function's min or max.

Hence, neuron SAF is a tractable abstraction: the number of neurons is orders of magnitude smaller than the number of weights, making fault simulation and pattern generation computationally feasible. The paper also extends SAF to CNN filters, where a faulty filter produces a constant output channel.

### 2.2 Test Pattern Generation

For a single fault \(f\), a test pattern \(x^\star\) maximizes the softmax divergence between the fault-free network \(\text{Net}(x)\) and the faulty network \(\text{Net}_f(x)\):

\[
x^\star = \arg\max_{x \in X} o(x, f)
\]
with
\[
o(x, f) = \|\text{Softmax}(\text{Net}(x)) - \text{Softmax}(\text{Net}_f(x))\|_2^2
\]

The objective uses **misclassification (label change)** as the detection criterion — not merely output deviation. If the predicted class label differs between Net and Net\(_f\), the fault is detected. This is more practical for black-box or sealed-accelerator deployment where only the final class output is observable.

### 2.3 Compressed Test Pattern Generation

The core innovation: instead of storing full test patterns, each pattern \(x\) is generated directly in a compressed representation as a **linear combination of a shared basis \(B\)**:

\[
x = B\alpha = \sum_{k=1}^D b_k \cdot \alpha_k
\]

Where:
- \(B \in \mathbb{R}^{P \times D}\) is a matrix of \(D\) basis vectors (columns), where \(P\) is the input dimension (e.g., \(32 \times 32 \times 3 = 3072\) for CIFAR-10)
- \(\alpha \in \mathbb{R}^D\) is the coefficient vector to be stored
- \(D \ll P\) (e.g., \(D = 10\) vs. \(P = 3072\))

The optimization becomes:

\[
\alpha^\star = \arg\max_{\alpha \in \mathbb{R}^D} o(\text{Normalize}(B\alpha), f)
\]

The normalization ensures the reconstructed pattern \(x = \text{Normalize}(B\alpha)\) satisfies pixel-range constraints (e.g., [0, 255]).

### 2.4 Basis Generation and Storage Advantage

The basis vectors \(b_k\) are **pseudo-randomly generated with fixed seeds**. This means:
- The basis \(B\) **does not need to be stored**, it is regenerated on demand from seeds.
- Only the coefficient vectors \(\alpha^{(n)}\) for each fault \(f^{(n)}\) are stored.
- The total storage cost drops from \(N \times P\) (full patterns) to \(N \times D\) (coefficients only).

**Concrete storage comparison** (from the paper): For 1000 test patterns on MNIST (28×28 = 784 pixels), with \(D = 20\) basis vectors and 32-bit floating point:
- Uncompressed: \(4 \times (784 \times 1000) = 3,136,000\) bytes
- Compressed (proposed): \(4 \times (1000 \times 20) = 80,000\) bytes
- **Compression ratio: 39.2×**

The algorithm (Algorithm 1 in the paper):
1. Choose \(D\) (number of basis vectors) and generate \(B\) from seeds.
2. For each fault \(f^{(n)}\) in the fault list \(F\):
   - Solve \(\alpha^\star = \arg\max_{\alpha \in \mathbb{R}^D} o(\text{Normalize}(B\alpha), f)\) via gradient-based optimization (Adam).
   - Store \(\alpha^\star\).
3. During testing: reconstruct \(x^{(n)} = \text{Normalize}(B\alpha^{(n)})\) on demand.

### 2.5 Key Difference from Conventional Compaction

This is **not** a compaction method (which reduces the *number* of patterns). The basis representation reduces the *storage per pattern*. The paper explicitly notes that compaction approaches (fault collapsing, set cover) are **orthogonal** and can be freely combined.

## 3. Experiments

### 3.1 Setup

- **Datasets:** MNIST, CIFAR-10
- **Models:** MLP (MNIST), LeNet-5 (MNIST), ConvNet-7 (CIFAR-10), **VGG-19** (CIFAR-10)
- **Fault models:** Single and multiple stuck-at neuron faults (SA0, SA1, SA6 for ReLU6)
- **Activation functions:** Sigmoid, Tanh, ReLU, ReLU6
- **Basis vector counts \(D\):** 10–50 (depending on model)
- **Optimizer:** Adam (grid search for learning rate from \(10^{-7}\) to 1)

### 3.2 Results

The full experimental results are in Table II of the paper. Key highlights:

| Model | Dataset | Activation | Fault Model | Basis \(D\) | Patterns | Rand. | Adv. [17] | Proposed | Comp. Ratio |
|-------|---------|-----------|-------------|-------------|----------|-------|-----------|----------|-------------|
| MLP | MNIST | Sigmoid | SA0 | 20 | 20 | 50% | 10% | 98% | **39.2×** |
| MLP | MNIST | Sigmoid | SA0(15%) | 25 | 51 | — | 0% | 100% | **31.4×** |
| MLP | MNIST | Sigmoid | SA1 | 15 | 10 | — | 0% | 100% | **52.3×** |
| MLP | MNIST | ReLU6 | SA6 | 10 | 34 | 15% | 95%* | 95% | **78.4×** |
| MLP | MNIST | ReLU6 | SA0 | 20 | 10 | — | 0% | 100% | **39.2×** |
| LeNet-5 | MNIST | ReLU6 | SA6 | 10 | 10 | 5% | 98%* | 98% | **78.4×** |
| LeNet-5 | MNIST | Sigmoid | SA0 | 10 | 3 | 5% | 100%* | 100% | **78.4×** |
| ConvNet-7 | CIFAR-10 | ReLU6 | SA6 | 10 | 50 | 25% | 95%* | 95% | **307.2×** |
| ConvNet-7 | CIFAR-10 | ReLU6 | SA6(10%) | 10 | 70 | — | 0% | 100% | **307.2×** |
| VGG-19 | CIFAR-10 | ReLU | SA6(5%) | 50 | 4096 | — | 0% | 100% | **61.4×** |
| VGG-19 | CIFAR-10 | ReLU | SA0(5%) | 50 | 4096 | — | 0% | 100% | **61.4×** |

(*Adversarial baseline reaches high coverage only in some LeNet-5 settings with Sigmoid — but the paper notes these are exceptions, not the rule.)

**Key findings:**
- **Up to 100% fault coverage** on single and multiple neuron SAF across all models.
- **Up to 307.2× compression** ratio (ConvNet-7, 10 basis vectors).
- **Outperforms adversarial and random baselines** in nearly all settings — adversarial patterns often achieve 0% coverage on ReLU-based networks.
- **Scalability to VGG-19:** 100% coverage demonstrated, though with many patterns (4096) per fault.
- **Fault coverage increases with more basis vectors** (higher \(D\) spans a larger subspace), but this reduces the compression ratio.

### 3.3 Weight-to-Neuron Fault Validation

A key experimental contribution: the paper validates that **multiple weight faults can be accurately modeled as neuron SAF**. Injecting >80% of a neuron's weights with >90% bit flips causes the neuron output to stick at its activation function's min or max — exactly the SAF model. This justifies using neuron-level fault simulation (tractable) instead of weight-level simulation (computationally expensive).

## 4. Conclusion

The paper proposes a compressed test pattern generation method for DNN hardware accelerators. By generating test patterns as linear combinations of pseudo-random basis vectors and storing only the coefficients, it achieves simultaneous pattern generation and compression. The method reaches 100% fault coverage for single and multiple stuck-at neuron faults, up to 307.2× storage reduction compared to uncompressed patterns, and outperforms both random and adversarial test images. The basis is regenerated on demand from seeds, requiring no additional storage.

---

## 5. FAQ: Detailed Questions and Answers

### (1) What exactly does "compressed test pattern" mean here?

It does *not* mean fewer test patterns (compaction). It means each individual test pattern is stored in a **compressed representation**: instead of storing all \(P\) pixel values (e.g., 3072 for CIFAR-10), only \(D\) coefficients are stored (e.g., 10). The full pattern is reconstructed on demand as a linear combination of basis vectors.

### (2) Where is the basis stored?

It is **not stored**. The basis vectors are pseudo-randomly generated from fixed seeds (integers 1 to \(D\)). Since the seeds are deterministic, the same basis can be reproduced exactly during test application. This is the same seed-reuse trick used in the group's other papers.

### (3) What is the trade-off with the number of basis vectors \(D\)?

More basis vectors \(\rightarrow\) higher fault coverage (spans a larger subspace) \(\rightarrow\) lower compression ratio (more coefficients to store). Example from Fig. 3 in the paper: for MLP on MNIST, \(D = 6\) gives 96.7% coverage at 131× compression, while \(D = 20\) gives 98% coverage at 39.2× compression. The paper treats \(D\) as a user-chosen parameter.

### (4) Why does the adversarial baseline often achieve 0% coverage?

The adversarial method (FGSM-based, Li et al. [17]) starts from a real image and adds small perturbations. These perturbations are designed for imperceptibility, not for maximizing the gap between fault-free and faulty outputs. For ReLU-based networks especially, small perturbations may not change neuron activations enough to cause misclassification under a neuron SAF. The proposed method, by contrast, optimizes from a random starting point without imperceptibility constraints.

### (5) How does this compare to the group's other work on weight-level faults?

The other papers inject faults directly at the **weight bit level** (flipping bits in weight representations). This paper injects faults at the **neuron output level** (stuck-at min/max). The two are linked: the paper shows experimentally that severe weight faults (affecting >80% of weights with >90% bit flips) manifest as neuron SAF. However, the fault models are conceptually different and target different abstraction levels.

### (6) What does the "percentage" next to SA0(10%) mean?

It means **10% of all neurons in the network** are injected with stuck-at-0 faults (multiple neurons simultaneously). This tests the method's ability to handle multiple concurrent faults, not just single-neuron faults.

### (7) Is the method applicable to non-image inputs?

In principle, the method requires only a differentiable network and a continuous input space. For discrete inputs (e.g., text tokens for LLMs), the normalization and linear combination approach would need adaptation. The paper does not address this.

### (8) What is the one-fault-per-pattern limitation?

Unlike the group's min-max approach (which optimizes one pattern to detect *many* faults simultaneously), this paper optimizes one pattern per fault (or per group of injected neurons). This means the number of test patterns equals the number of faults, which can be large (e.g., 4096 patterns for VGG-19). The compression helps with storage, but test application time scales linearly with the number of faults.

---

## 6. Research Gaps

### (1) One-pattern-per-fault scalability

The method generates one test pattern per fault (or per fault group). For VGG-19 with a fault list of 4096 neurons, this means 4096 patterns. While storage is compressed (61.4×), the **test application time** still requires applying all 4096 patterns. For models with millions of neurons, this becomes prohibitive. The paper does not explore combining this with compaction methods to reduce pattern count.

### (2) No unseen-fault generalization analysis

Unlike the group's multiple-fault paper (which tests generalization to 1000 unseen weight faults), this paper does **not** evaluate whether patterns generated for one set of neuron SAFs detect *different* faults. The 100% coverage claim applies only to the targeted fault set. It remains unclear whether patterns generalize across different neuron fault locations or fault severities.

### (3) Basis quality is not optimized

The basis vectors are pseudo-random. The paper acknowledges that basis quality affects the compression ratio and fault coverage, but does not explore learned or optimized bases. Integrating basis search into the optimization procedure is mentioned as future work but is non-trivial (it requires solving a large joint optimization over all faults simultaneously).

### (4) Limited fault model validation

The paper validates that weight faults map to neuron SAF, but only for specific activation functions (Sigmoid, ReLU6) with bounded ranges. For ReLU (unbounded upper range) and Tanh, the paper assigns ad-hoc values (stuck-at-6 for ReLU's max). The mapping for modern activation functions (GELU, SiLU) is not explored.

### (5) Scalability to LLMs

Same limitation as the other Tahoori papers: the method operates on continuous pixel-valued inputs. Adapting to discrete token spaces for LLMs is not addressed. Additionally, the neuron SAF model assumes stuck-at values from activation function ranges — for LLMs using LayerNorm, GELU, and residual connections, a neuron stuck at a fixed value may not be a meaningful fault model.

---

## Comparison with Related ATPG Approaches

All three Tahoori-group papers (this TC 2025 paper, the D&T 2024 journal, and the DATE 2023 conference paper) share the same research group (Moussa, Hefenbrock, Tahoori) and the **misclassification detection criterion**. However, this TC 2025 paper represents a **different methodological thread**: it compresses *per-pattern storage* via basis representation (\(N \times D\) vs \(N \times P\)), while the D&T 2024 / DATE 2023 papers compact *pattern count* (fewer patterns covering many faults via min-max). These two approaches are **orthogonal** and could be combined. The key differences from all related ATPG approaches:

| Aspect | **This Paper** (TC 2025) | **Testing for Multiple Faults** (D&T 2024) | **DATE 2023 (compact)** | **ATPG & Compaction for DNN** (Zhang et al.) | **ATPG for Printed Neuro Circuits** (2025) |
|--------|--------------------------|---------------------------------------------|--------------------------|----------------------------------------------|---------------------------------------------|
| **Target** | DNN accelerators | DNN accelerators | DNN accelerators | DNNs (software model) | Printed neuromorphic circuits |
| **Fault Model** | Neuron SAF (stuck-at min/max) | Multiple bit-level weight faults (pw, pb) | Same as D&T 2024 | Stuck-at neuron/filter output | Crossbar, p-tanh, p-inv (analog) |
| **Fault Scope** | Single/multiple neurons | Multiple faults (simultaneous) | Same | Single fault per test | Single fault assumption |
| **Detection** | Misclassification (label change) | Misclassification (label change) | Same | Output deviation (Euclidean) | Output deviation (KL divergence) |
| **Optimization** | Gradient-based (single fault) | Min-max (max lower bound) | Same | Gradient-based (single fault) | Gradient-based (KL divergence) |
| **Compression Method** | **Basis representation** (per-pattern) | Iterative covering via min-max | Same | K-means + greedy set cover | Not explicitly addressed |
| **Compression Type** | Storage per pattern | Pattern count reduction | Same | Pattern count reduction | — |
| **Max Compression** | **307.2×** (storage) | 50× (compaction) | 25× | Not reported | — |
| **Patterns per Fault** | 1 pattern per fault | ~1 pattern per 50 faults | ~1 per 25 | ~1 per cluster | ~1 per fault |
| **Key Metrics** | Fault coverage, compression ratio | Compaction ratio, unseen coverage | Compaction ratio, unseen coverage | Fault coverage | Fault coverage (%) |
| **Baselines** | Random + Adversarial | Random + Adversarial | None | Not compared | Random patterns |
| **Largest Model** | VGG-19 (19 layers) | VGG-19 (19 layers) | ConvNet-7 (7 layers) | ConvNet-7 | Small pNCs (9 models) |
| **Authors** | Moussa et al. (Tahoori group) | Moussa et al. (Tahoori group) | Moussa et al. (Tahoori group) | Zhang et al. | Azimi et al. |

The Tahoori-group papers (this one, D&T 2024, DATE 2023) share the **misclassification detection criterion** and focus on **hardware accelerator faults**. The key distinction within the group is:

- **TC 2025** compresses *per-pattern storage* (basis representation, \(N \times D\) vs \(N \times P\)).
- **D&T 2024 / DATE 2023** compacts *pattern count* (fewer patterns covering many faults via min-max).

These are **orthogonal** and could be combined. The non-Tahoori papers use **output deviation** as detection rather than misclassification, and target fundamentally different domains (software DNN models, printed neuromorphic circuits).
