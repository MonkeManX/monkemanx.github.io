---
title: 'Functional Test Generation for In-Field Testing of Deep Learning Models with Test Storage Constraints'
date: 2026-06-19 14:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Functional Test Generation for In-Field Testing of Deep Learning Models with Test Storage Constraints

**Link to Paper:** https://doi.org/10.1109/ITC58126.2025.00029

**Date:** 2025 (IEEE International Test Conference)

**Paper Type:** Test Generation, Functional Testing, Deep Neural Networks, In-Field Testing

**Short Abstract:**
This paper proposes a **storage-aware, fault-agnostic** framework that jointly optimizes a **fixed-size set of test patterns** to maximize expected fault coverage under a probabilistic fault model. Using Monte Carlo sampling to estimate the expectation over the fault distribution, the method produces a test set of exactly K patterns, while achieving 100% coverage across multiple fault types (weight perturbation, bit flips, stuck-at, composite), outperforming random and adversarial baselines on classification (MLP, ConvNet-7, VGG-19) and segmentation (CamVid) tasks.

## 1. Introduction

DNNs deployed on specialized AI hardware accelerators (TPUs, GPUs) are structurally tested at manufacturing time, independent of the model executed. However, **in-field reliability** demands model-specific functional testing, as hardware failures from aging, environmental disturbances, or manufacturing escapes can degrade inference over time.

The paper identifies three key limitations in existing approaches:

1. **Predefined fault lists** (e.g., Moussa et al. DATE 2023) cover only a fixed set of fault scenarios and fail to generalize to new or probabilistic hardware failures.
2. **Post-generation compaction** generates patterns first, then compresses/compacts to fit storage, this ignores storage limits from the outset and introduces inefficiencies.
3. **Fault-model specificity**, many methods target only one type (bit flips, stuck-at, or adversarial perturbations), limiting comprehensive assessment.

The core insight: instead of generating patterns for individual faults and then compacting, **generate all K test patterns jointly** with K as a user-defined parameter that directly encodes the storage budget. The patterns distribute responsibility across the fault distribution through a joint optimization objective.

> *"A more effective approach would integrate test storage constraints directly into the test generation process, ensuring that the final test set is optimized for both fault coverage and meets practical deployment constraints."*

The paper makes four contributions:
- A **fault-type agnostic** methodology adaptable to any probabilistic fault model.
- A **storage-aware** framework integrating memory/execution constraints into generation.
- **Up to 100% fault coverage** across multiple fault types, models, and datasets — including **segmentation tasks** (first in this line of work).
- Demonstrated scalability to VGG-19 and CNN-based segmentation.

## 2. Methodology

### 2.1 Fault Model: Probabilistic and Agnostic

Unlike prior Tahoori-group papers that define a specific fault model (bit-level weight faults or neuron SAF), this paper treats the fault distribution \(p(f)\) as a general probabilistic model. Any fault model that supports sampling qualifies: weight perturbation (Gaussian noise), bit flips, stuck-at neurons, or composite mixtures. The faults are drawn i.i.d. from \(p(f)\).

### 2.2 Joint Optimization of a Fixed-Size Test Set

The key innovation: instead of generating one pattern per fault or iteratively covering faults, **all K test patterns are optimized jointly**. The objective maximizes the **expected fault coverage** under the fault distribution:

\[
X^\star = \arg\max_{X} \mathbb{E}_{p(f)}\left[ \max_{x \in X} d(x, f) \right]
\]

Where:
- \(X = \{x_1, \dots, x_K\}\) is the set of K test patterns (K = storage budget).
- \(d(x, f)\) measures the softmax divergence between fault-free and faulty outputs (squared Euclidean norm or KL divergence).
- The **inner max** means only the best-matching pattern is responsible for each fault — other patterns remain free to cover different faults.
- The **outer expectation** over \(p(f)\) means patterns are optimized for the full distribution, not a fixed fault list.

This formulation has three properties:
1. **Automatic division of labor**: patterns naturally distribute effort across different fault types/regions.
2. **Fault equivalence**: faults causing similar output behavior are captured by the same pattern.
3. **Explicit storage constraint**: the size K directly encodes the memory budget.

### 2.3 Monte Carlo Gradient Estimation

The expectation cannot be computed analytically, so the authors use **Monte Carlo sampling** with \(N\) fault samples per optimization step:

\[
\mathbb{E}_{p(f)}\left[ \max_{x \in X} d(x, f) \right] \approx \frac{1}{N} \sum_{n=1}^{N} \max_{x \in X} d(x, f^{(n)})
\]
with \(f^{(n)} \sim p(f)\)

The gradient is similarly estimated:

\[
\nabla_X \mathbb{E}_{p(f)}\left[ \max_{x \in X} d(x, f) \right] \approx \frac{1}{N} \sum_{n=1}^{N} \nabla_X \max_{x \in X} d(x, f^{(n)})
\]

**Algorithm 1** in the paper:
1. Initialize \(K\) test patterns randomly.
2. For \(T = 500\) steps:
   - Sample \(N = 500\) faults from \(p(f)\).
   - Estimate objective and gradient via Monte Carlo.
   - Update patterns with Adam.
   - Project to feasible domain (e.g., clip pixel values to [0, 255]).
3. Return the best set \(X^\star\) found.

Note: the same fault samples are reused for both objective and gradient estimation in each step.

### 2.4 Key Differences from Prior Tahoori Methods

| Aspect | **ITC 2025 (this paper)** | **D&T 2024** (min-max) | **TC 2025** (compressed) |
|--------|---------------------------|------------------------|--------------------------|
| **Fault Model** | Any probabilistic \(p(f)\) | Bit-level weight faults (pw, pb) | Neuron SAF |
| **Pattern Generation** | Joint (all K patterns simultaneously) | Iterative (one at a time, removal) | One per fault |
| **Storage Constraint** | **Explicit** (\(K\) = budget) | Implicit (compaction ratio) | Per-pattern compression |
| **Fault Coverage** | Expected over \(p(f)\) | 100% on fixed fault list | 100% on targeted faults |
| **Objective** | \(\max_X \mathbb{E}[\max_{x \in X} d(x,f)]\) | \(\max_x \min_{f \in F} o(x,f)\) | \(\max_\alpha o(B\alpha, f)\) |
| **Method Type** | Storage-aware generation | Pattern-count compaction | Per-pattern compression |

These three approaches from the Tahoori group are **complementary** and could in principle be combined: the ITC 2025 method provides storage-aware joint generation, which could feed into the D&T 2024 compaction, and patterns could be stored using the TC 2025 basis compression.

## 3. Experiments

### 3.1 Setup

- **Datasets:** MNIST (MLP), CIFAR-10 (ConvNet-7, VGG-19), CamVid (segmentation)
- **Models:** MLP (3 FC, size 20), ConvNet-7, VGG-19, CNN-based segmentation (10 layers)
- **Fault types:** Weight perturbation (Gaussian noise), bit flip, stuck-at-zero, **composite** (all three combined)
- **Parameters:** \(K = 30\) (MLP), \(K = 40\) (CNN, segmentation); \(N = 500\) Monte Carlo samples; \(T = 500\) Adam steps
- **Baselines:** Random images, adversarial images (FGSM-based, Li et al.)

### 3.2 Key Results

| Model | Dataset | Fault Model | Random | Adv. [16] | **Proposed** |
|-------|---------|-------------|--------|-----------|-------------|
| MLP | MNIST | WP (p=5%, σ=0.1) | 66% | 56% | **100%** |
| MLP | MNIST | BF (p=5%, ρ=0.1) | 79% | 76% | **100%** |
| MLP | MNIST | SA (p=5%, ρ=0.1) | 68% | 26% | **100%** |
| MLP | MNIST | Composite (p=5%) | 82% | 70% | **100%** |
| ConvNet-7 | CIFAR-10 | WP (p=10%, σ=0.05) | 89% | 54% | **100%** |
| ConvNet-7 | CIFAR-10 | BF (p=10%, ρ=0.05) | 94% | 66% | **99.6%** |
| ConvNet-7 | CIFAR-10 | SA (p=10%, ρ=0.05) | 80% | 60% | **99.8%** |
| ConvNet-7 | CIFAR-10 | Composite (p=10%) | 66% | 77% | **100%** |
| VGG-19 | CIFAR-10 | WP (p=15%, σ=0.1) | 44% | 36% | **100%** |
| VGG-19 | CIFAR-10 | BF (p=15%, ρ=0.1) | 68% | 28% | **100%** |
| CNN-Seg. | CamVid | WP (p=15%, σ=0.1) | 90% | 33% | **100%** |
| CNN-Seg. | CamVid | BF (p=15%, ρ=0.1) | 88% | 46% | **100%** |
| CNN-Seg. | CamVid | SA (p=15%, ρ=0.1) | 87% | 43% | **100%** |
| CNN-Seg. | CamVid | Composite (p=15%) | 61% | 60% | **100%** |

**Key findings:**
- **100% fault coverage** achieved in nearly all settings across all four fault types.
- **Consistently outperforms** both random and adversarial baselines by a large margin.
- **Adversarial baseline fails** especially on segmentation tasks (~33–60% coverage) and stuck-at faults (as low as 26%).
- **Segmentation tasks** are tested for the first time in this line of work, fault coverage remains high despite the model's greater spatial sensitivity.
- **VGG-19 scalability** confirmed: 100% coverage on large model with both weight perturbation and bit flip faults.
- **Test pattern count vs. coverage trade-off** (Fig. 4): With 30 patterns MLP reaches full coverage; CNN needs ~40 patterns for >95% coverage. Below these thresholds, coverage drops, more steeply for CNNs.

### 3.3 Fault Impact Analysis

The paper includes an extensive analysis of how different fault types affect inference accuracy across models (Fig. 2):
- **MLPs** are highly sensitive to weight perturbations, even small σ causes accuracy drops.
- **CNNs** show more robustness to small perturbations due to parameter redundancy and hierarchical feature extraction.
- **Segmentation models** are the most vulnerable, even minor stuck-at faults cause significant pixel-wise misclassification due to lost spatial coherence.
- **Bit flip faults** are less damaging than stuck-at faults (a single flipped bit may not change the weight value enough to matter).
- **Composite faults** naturally combine effects and become severe at higher magnitudes.

## 4. Conclusion

The paper introduces a storage-aware, fault-agnostic test pattern generation method that jointly optimizes a fixed-size set of patterns under a probabilistic fault model. By integrating the storage constraint (K patterns) directly into generation, it avoids the need for post-generation compaction while achieving up to 100% fault coverage across weight perturbation, bit flip, stuck-at, and composite faults, on classification (MLP, ConvNet-7, VGG-19) and segmentation (CamVid) models. This makes it well-suited for in-field testing on hardware-constrained AI accelerators.

---

## 5. FAQ: Detailed Questions and Answers

### (1) What does "jointly optimize" mean in practice?

Instead of generating one pattern at a time (each focused on one specific fault), all K patterns are updated simultaneously during gradient ascent. At each step, every pattern "competes" to be the one that maximizes \(d(x, f)\) for each sampled fault. The gradient update encourages patterns to specialize, each takes responsibility for a subset of the fault distribution. The \(\max_{x \in X}\) operator in the objective ensures that once one pattern covers a fault well, other patterns are free to focus elsewhere.

### (2) How is K chosen?

K is a **user-defined parameter** representing the storage budget (number of test patterns × bytes per pattern ≤ available memory). The paper treats K as a given constraint. Fig. 4 explores the coverage vs. K trade-off: more patterns → higher coverage, but diminishing returns. This is the first Tahoori paper where storage is an **explicit input** rather than an output metric.

### (3) What fault models are supported?

Any probabilistic fault model \(p(f)\) that supports sampling. The paper demonstrates four: weight perturbation (Gaussian noise on weights), bit flip (random bit flips in weight representations), stuck-at-zero (neurons clamped to 0), and composite (all three combined at lower rates). This **fault-agnostic** property is the key generalization over prior work.

### (4) What is the relationship to the other Tahoori papers?

This ITC 2025 paper is the **third distinct methodological thread** from the Tahoori group:

- **DATE 2023 / D&T 2024** (min-max): Iterative compaction: one pattern covers many faults, patterns are few, fault list is fixed.
- **TC 2025** (compressed): Per-pattern storage reduction: many patterns, each stored compactly via basis representation.
- **ITC 2025** (this paper): Storage-aware joint optimization: K patterns are the budget, patterns share responsibility across the fault distribution.

They are complementary and could be combined.

### (5) Why does the adversarial baseline (FGSM) perform so poorly?

FGSM adversarial images are designed for imperceptibility (small perturbations around real images). They are not optimized for maximizing softmax divergence under faults. For stuck-at faults especially (26% coverage on MLP), the small perturbations fail to produce misclassification because they don't exploit the fault's effect on the network's decision boundary.

### (6) How does this scale to larger models compared to the other methods?

- **vs. D&T 2024 (min-max)**: That method requires N forward passes per optimization step (one per fault in the list). This paper uses N = 500 Monte Carlo samples per step for gradient estimation, similar computational cost per step, but produces K patterns jointly rather than iteratively.
- **vs. TC 2025**: That method generates one pattern per fault (potentially thousands). This paper generates exactly K patterns regardless of model size.
- The per-step cost scales linearly with model size for all methods, as each forward/backward pass is through the full network.

### (7) What is the computational cost?

\(T = 500\) steps with \(N = 500\) Monte Carlo samples means 250,000 forward passes per optimization run for ConvNet-7 (500 × 500). For VGG-19, this is substantial but still feasible on an A100 GPU (as used in experiments). The paper notes this is an **offline** cost, the generated patterns are applied cheaply during in-field testing.

### (8) What about segmentation tasks — how is the objective defined?

For segmentation, the same softmax divergence is used, but applied at the **pixel level**. Each pixel's softmax distribution is compared between fault-free and faulty networks. The objective aggregates across all pixels. This makes segmentation inherently more fault-sensitive than classification (more output dimensions to deviate).

---

## 6. Research Gaps

### (1) No unseen-fault generalization analysis

Like the other Tahoori papers, fault coverage is evaluated against faults drawn from the **same distribution** \(p(f)\) used during optimization. The paper does not test generalization to:
- Fault types not seen during optimization (e.g., patterns trained on bit flips tested on stuck-at).
- Fault distributions with different parameters (e.g., trained on ρ=0.05, tested on ρ=0.5).
- Correlated or structured faults (e.g., row/column failures in crossbar arrays).

The 100% coverage claim applies to Monte Carlo estimates from the same distribution, how well it transfers to real hardware fault distributions remains open.

### (2) White-box assumption during generation

Test pattern generation requires full access to model parameters, gradients, and softmax outputs. This is acceptable for **offline generation**, but the method assumes the network is differentiable and accessible,  which may not hold for proprietary or hardware-encrypted models.

### (3) Fault distribution must be known or assumable

The method requires a probabilistic fault model \(p(f)\) to sample from. In practice, the true hardware fault distribution may be unknown or vary between chips, operating conditions, and aging states. The paper uses simple parametric distributions (Gaussian, uniform bit flip), real fault distributions may be more complex.

### (4) VGG-19 is the largest model tested

While VGG-19 (~144M parameters) is used, modern LLMs have 7B–175B+ parameters. The per-step cost of 500 Monte Carlo forward passes through a 7B model is prohibitive (each forward pass is ~14GB of compute on an A100). The paper does not address this.

### (5) No localization capability

The method detects faults (via misclassification) but provides no information about **where** the fault occurred. Unlike DTPG approaches (which include fault-to-fault separability for localization), this is purely a detection method.

---

## 7. Scalability to LLMs and Potential Directions

This is perhaps the most significant open challenge for all ATPG methods, including this paper. Below is an analysis of why LLM-scale ATPG is hard and what approaches could address it.

### 7.1 Why This Method Does Not Scale to LLMs

**Computational barrier:** Each optimization step requires \(N = 500\) forward passes through the full model. For a 7B-parameter LLM:
- Each forward pass: ~14 GB GPU memory, ~50 ms on H100
- Per step cost: 500 × 50 ms = 25 seconds
- \(T = 500\) steps: 12,500 seconds ≈ 3.5 hours per optimization run
- For each fault distribution / K setting tested

Compare to ConvNet-7 (CIFAR-10): each forward pass is ~2 ms, so 500 steps × 500 samples × 2 ms = 500 seconds total.

**Discrete token problem:** The method operates on continuous input spaces (pixel values in [0, 255]). LLMs operate on **discrete token IDs** from a finite vocabulary. Gradient-based optimization on discrete tokens requires relaxation (Gumbel-Softmax, continuous embeddings) or search-based alternatives. Neither is explored in this paper.

**Fault model mismatch:** The paper's fault models (weight perturbation, bit flips, stuck-at neurons) are designed for vision models with ReLU activations. LLMs use LayerNorm, GELU/SwiGLU, residual connections, and attention mechanisms, a neuron stuck at zero behaves fundamentally differently in these architectures.

### 7.2 Potential Approaches to Address LLM Scalability

#### A. Efficient Monte Carlo via Subnet Sampling
The main cost driver is \(N\) forward passes per step. Instead of running the *full* model \(N\) times, **subnet sampling** could be used: for each fault sample, only recompute the affected subgraph. If faults are sparse (e.g., one attention head), only that head's computation path needs re-evaluation. This could reduce per-sample cost from \(O(L)\) to \(O(1)\) for sparse faults.

#### B. Importance-Weighted Fault Sampling
The current method samples faults uniformly from \(p(f)\). For LLMs, weights have highly uneven importance, a single critical weight flip can jailbreak an LLM (PrisonBreak), while most flips have no effect. **Importance-weighted sampling** (using gradient-based sensitivity scores) would focus Monte Carlo samples on faults that actually matter, reducing N needed for good gradient estimates.

#### C. Gradient Accumulation over Mini-Batches
Instead of estimating gradients with \(N = 500\) full-model passes, use **gradient accumulation** with smaller batch sizes over more steps. Each step uses \(N = 1\) fault sample, with gradient noise compensated by more total steps. This trades per-step accuracy for wall-clock time.

#### D. Discrete Token Optimization via Continuous Relaxation
For the discrete token problem, three approaches are promising:
1. **Soft-embedding optimization:** Optimize in the continuous embedding space rather than token space. Start from a random embedding sequence, apply gradient updates, then project back to the nearest valid token sequence at test time.
2. **Prompt-level patterns:** Instead of optimizing individual tokens, optimize entire prompt embeddings (soft prompts) that maximize divergence under faults.
3. **Gumbel-Softmax reparameterization:** Use the Gumbel-Softmax trick to make the discrete token sampling differentiable, enabling gradient-based optimization over the vocabulary.

#### E. Precomputation + Caching
The Monte Carlo samples \(f^{(n)}\) are drawn from \(p(f)\) at each step. For LLMs, the fault distribution may be relatively static. **Precomputing fault effects** on a representative set of input prompts and caching the results could reduce the per-step cost to a table lookup + interpolation, completely avoiding forward passes during optimization.

#### F. Surrogate Model for Gradient Estimation
Train a smaller **surrogate model** that mimics the LLM's output behavior under faults. Use this surrogate for the Monte Carlo gradient estimation during pattern optimization. The surrogate would be much cheaper per forward pass (e.g., distilled 1B model for a 7B target). Only the final pattern verification would run on the full model.

#### G. Layer-Wise Pattern Generation
Instead of generating end-to-end test patterns for the full LLM, generate patterns for **individual layers or attention heads** and compose them. Each layer's pattern is optimized against faults in that layer only, using a reduced model (the layer + surrounding context). This reduces the per-optimization model size from \(O(L)\) to \(O(1)\).

### 7.3 Summary

| Approach | Key Idea | Cost Reduction | Feasibility |
|----------|----------|---------------|-------------|
| Subnet sampling | Only recompute affected subgraph | \(O(L) \to O(1)\) per sample | Medium — requires graph tracing |
| Importance-weighted sampling | Focus on critical weights | \(N\) can be reduced 10-100× | High — PrisonBreak shows weight importance |
| Gradient accumulation | N=1 per step, more steps | Constant per-step cost, more steps | High — standard ML technique |
| Soft-embedding optimization | Continuous embedding space | Solves discrete token problem | High — used in prompt tuning |
| Precomputation + caching | Precompute fault effects | Avoids forward passes entirely | Low — fault effects may be input-dependent |
| Surrogate model | Smaller model for gradients | Reduction proportional to surrogate size | Medium — surrogate accuracy may limit quality |
| Layer-wise generation | Patterns per layer, not full model | \(O(L) \to O(1)\) per optimization | Medium — assumes fault effects are local |

None of these are explored in this paper, but they represent concrete paths for extending the storage-aware joint optimization framework to LLM-scale models.

---

## Comparison with Related ATPG Approaches

All three Tahoori-group papers (DATE 2023, D&T 2024, TC 2025) and the current ITC 2025 paper share the same research group and the **misclassification detection criterion**. However, each represents a distinct methodological thread:

- **ITC 2025 (this paper):** Storage-aware joint optimization: K patterns jointly optimized via Monte Carlo expectation over \(p(f)\). Fault-agnostic.
- **D&T 2024 / DATE 2023:** Iterative compaction: one pattern covers many faults via min-max, pattern count is output, not input.
- **TC 2025:** Per-pattern compression: basis representation for storage-efficient individual patterns.

The ITC 2025 paper is the first to treat K as an **explicit constraint** and the first to use a **probabilistic fault model** rather than a fixed fault list.

| Aspect | **This Paper** (ITC 2025) | **Testing for Multiple Faults** (D&T 2024) | **Compressed TPG** (TC 2025) | **DATE 2023 (compact)** | **ATPG & Compaction** (Zhang et al.) | **ATPG for Printed Neuro** (2025) |
|--------|---------------------------|---------------------------------------------|-----------------------------|--------------------------|--------------------------------------|-----------------------------------|
| **Target** | DNN accelerators | DNN accelerators | DNN accelerators | DNN accelerators | DNNs (software model) | Printed neuromorphic circuits |
| **Fault Model** | **Any probabilistic** (WP, BF, SA, CF) | Multiple bit-level weight faults (pw, pb) | Neuron SAF | Same as D&T 2024 | Stuck-at neuron/filter output | Crossbar, p-tanh, p-inv (analog) |
| **Fault Scope** | Multiple faults (via \(p(f)\) sampling) | Multiple faults (simultaneous) | Single/multiple neurons | Multiple faults | Single fault per test | Single fault assumption |
| **Storage Constraint** | **Explicit** (\(K\) = budget) | Implicit (compaction ratio) | Implicit (basis dimension \(D\)) | Implicit | Not addressed | — |
| **Detection** | Misclassification (label change) | Misclassification (label change) | Misclassification | Same | Output deviation (Euclidean) | Output deviation (KL divergence) |
| **Optimization** | **Joint** (all K patterns via MC expectation) | Min-max (max lower bound) | Gradient-based (single fault) | Same | Gradient-based (single fault) | Gradient-based (KL divergence) |
| **Generation** | Single-stage, \(K\) patterns jointly | Iterative (one pattern, remove faults) | One per fault | Same | One per fault | One per fault |
| **Compression** | **None needed** (K is the budget) | Iterative set cover | Basis representation | Same | K-means + greedy set cover | Not addressed |
| **Max Coverage** | **100%** (all 4 fault types) | 100% (targeted list), 99.9% (unseen) | 100% (targeted neurons) | 100% (targeted list) | Not reported | 98% |
| **Baselines** | Random + Adversarial | Random + Adversarial | Random + Adversarial | None | Not compared | Random patterns |
| **Segmentation?** | **Yes** (CamVid) | No | No | No | No | No |
| **Largest Model** | VGG-19 (19 layers) | VGG-19 (19 layers) | VGG-19 (19 layers) | ConvNet-7 (7 layers) | ConvNet-7 | Small pNCs |
| **Authors** | Moussa et al. (Tahoori group) | Moussa et al. (Tahoori group) | Moussa et al. (Tahoori group) | Moussa et al. (Tahoori group) | Zhang et al. | Azimi et al. |

The key distinction for this ITC 2025 paper: it is the **first storage-aware** method in this family, the **first fault-agnostic** (supports any probabilistic fault model), and the **first to test on segmentation tasks**. The non-Tahoori approaches use output deviation (not misclassification) and target fundamentally different domains (software DNN models, printed neuromorphic circuits).
