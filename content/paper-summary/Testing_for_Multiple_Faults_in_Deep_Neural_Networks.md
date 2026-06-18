---
title: 'Testing for Multiple Faults in Deep Neural Networks'
date: 2026-06-17 15:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Testing for Multiple Faults in Deep Neural Networks

**Link to Paper:** https://doi.org/10.1109/MDAT.2024.3365988

**Date:** May/June 2024

**Paper Type:** Test Generation, Deep Neural Networks, Hardware Faults, Fault Detection

**Short Abstract:**
Deep Neural Networks (DNNs) implemented on specialized hardware accelerators are vulnerable to various manufacturing and runtime hardware faults. Single faults have negligible impact on DNN accuracy, but multiple faults can severely degrade inference. This paper proposes a compact test pattern generation approach to detect multiple bit-level weight faults in DNNs. Using a min-max optimization that maximizes the minimum output difference across a sampled fault list, the method iteratively produces a compact set of test patterns. Results show 100% coverage on targeted faults, up to 50× compaction on larger networks (VGG-19), and up to 99.9% coverage on unseen faults, significantly outperforming random and adversarial test baselines.

## 1. Introduction

DNNs require significant computational resources, motivating specialized accelerators such as TPUs and Memristor crossbar arrays. Hardware faults in these accelerators threaten inference accuracy and reliability. The paper makes a key observation:

> *"The impact of single faults is usually negligible for DNNs. Nevertheless, multiple faults can have a severe impact on the accuracy of DNN accelerators."*

From a technological perspective, large accelerator sizes and the inherent imperfection of emerging memristive devices make multiple faults probable. Testing for such faults by evaluating a whole dataset is costly, motivating a compact set of test patterns.

### Limitations of Related Work

The paper identifies two main shortcomings in existing approaches:

1. **Over-reliance on real input images:** Adversarial-image methods start from a real input and add small perturbations. This is unnecessarily restrictive — test patterns do not need to resemble real data or be imperceptible.
2. **Output deviation as detection metric:** Measuring faults via output logit variation is unrealistic because:
   - In black-box deployment, intermediate results like logits may be unavailable.
   - Runtime variations (e.g., voltage fluctuations) can mimic fault-induced deviations.
   - Faults that do not cause misclassification may be negligible.

The paper instead detects faults **via misclassification (label change)**, which is more practical for black-box testing.

## 2. Methodology

### 2.1 Fault Model

Bit-level fault injection in weight representations. Two parameters define the model:

- **pw** — percentage of weights that have bits altered
- **pb** — percentage of bits flipped per affected weight

Since each fault instance alters multiple weights and multiple bit positions, this constitutes a **multiple fault model**.

### 2.2 Test Pattern Generation via Min-Max Optimization

For a test pattern \(x\), the objective for a single fault \(f\) is:

\[
o(x, f) := \left\| \text{Softmax}(\text{Net}(x)) - \text{Softmax}(\text{Net}_f(x)) \right\|_2^2
\]

Rather than targeting individual faults, the paper solves a **min-max optimization** over a sampled fault list \(F = \{f_1, \dots, f_N\}\):

\[
x^\star = \arg\max_{x \in X} \min_{f \in F} o(x, f)
\]

This maximizes the *lower bound* on the objective across all faults in the list, so the resulting test pattern is effective against many faults simultaneously.

### 2.3 Iterative Compaction Algorithm

The algorithm (Algorithm 1 in the paper):

1. Choose \((pw, pb, N)\) and generate fault list \(F\).
2. Define coverage: a fault \(f\) is *detected* if \(\arg\max \text{Net}(x) \neq \arg\max \text{Net}_f(x)\).
3. **Repeat** until \(F\) is empty:
   - Solve the min-max optimization to find \(x^\star_k\).
   - Remove all faults detected by \(x^\star_k\) from \(F\).
   - Add \(x^\star_k\) to test set \(X\).
4. Return compact test set \(X\).

The algorithm naturally produces **compact** test sets — each new pattern is optimized against the *hardest remaining* faults.

### 2.4 Storage Optimization via Seeding

Instead of storing each full faulty network instance, the paper stores only a **random seed** \(n\) for each fault \(f_n\). The fault pattern can be regenerated on demand by re-running the random generation procedure with the same seed. This avoids the storage overhead of saving partial or complete network states for every fault instance.

## 3. Experiments

### 3.1 Setup

- **Datasets:** MNIST, CIFAR-10
- **Models:** MLP (3 FC layers, size 20), LeNet-5 (7 layers), ConvNet-7 (7 layers, custom), **VGG-19** (19 layers, 16 Conv + 3 FC)
- **Weights:** Floating-point 32-bit, PyTorch
- **Fault parameters:** \(pw \in \{5\%, 10\%\}\), \(pb \in \{50\%, 70\%, 100\%\}\)
- **Fault list sizes:** 50, 100, 150, 200

### 3.2 Results

| Model | Dataset | pw | pb | FP | TP | CR | Targeted Cov | Unseen Cov |
|-------|---------|-----|-----|-----|-----|------|-------------|-----------|
| MLP | MNIST | 5% | 100% | 50 | 10 | 5× | 100% | 98.6% |
| MLP | MNIST | 10% | 70% | 100 | 9 | 11.1× | 100% | 98.7% |
| MLP | MNIST | 10% | 50% | 150 | 13 | 11.5× | 100% | 98.2% |
| LeNet-5 | MNIST | 5% | 100% | 50 | 4 | 12.5× | 100% | 97.8% |
| LeNet-5 | MNIST | 10% | 70% | 150 | 24 | 6.2× | 100% | 98.6% |
| LeNet-5 | MNIST | 10% | 50% | 200 | 31 | 6.4× | 100% | 98.7% |
| ConvNet-7 | CIFAR-10 | 5% | 100% | 50 | 2 | 25× | 100% | 99.9% |
| ConvNet-7 | CIFAR-10 | 10% | 70% | 100 | 10 | 10× | 100% | 99.8% |
| ConvNet-7 | CIFAR-10 | 10% | 50% | 200 | 21 | 9.5× | 100% | 99.5% |
| **VGG-19** | CIFAR-10 | 5% | 100% | 50 | **1** | **50×** | 100% | 100% |
| **VGG-19** | CIFAR-10 | 10% | 70% | 100 | **2** | **50×** | 100% | 98.5% |
| **VGG-19** | CIFAR-10 | 10% | 50% | 200 | **4** | **50×** | 100% | 99.4% |

(FP = fault patterns, TP = test patterns, CR = compaction ratio. FP = number of targeted faults.)

**Key findings:**
- **100% coverage** on targeted faults across all settings.
- **Up to 50× compaction** on VGG-19 — 1 test pattern covering 50 faults.
- **Up to 99.9% coverage on unseen faults** (1000 random faults outside the fault list).
- Compaction ratios are **higher for larger networks**, supporting scalability claims.

### 3.3 Comparison with Baselines

The paper compares against two baselines:

- **Random test images:** Required >6000 random images to cover all faults in challenging settings. Storage and test time increase significantly despite low per-image generation cost.
- **Adversarial image (FGSM-based):** Failed to achieve high coverage — only 34% for LeNet-5. Adversarial methods are designed for imperceptibility, which limits their effectiveness as test patterns.

The proposed method outperforms both baselines on coverage, compaction, and unseen fault detection.

## 4. Conclusion

The paper proposes a compact test pattern method for detecting multiple bit-level weight faults in DNNs. By maximizing the minimum output difference across a fault list and iteratively covering faults, it produces small test sets with high detection rates. The method achieves 100% coverage on targeted faults, up to 50× compaction ratio on VGG-19, and up to 99.9% coverage on unseen faults — outperforming both random and adversarial baselines.

---

## 5. Relationship to the DATE 2023 Paper

This paper (IEEE Design & Test, 2024) is a **journal extension** of the conference paper *"Compact Test Pattern Generation For Multiple Faults In Deep Neural Networks"* (DATE 2023) by the same authors (Moussa, Hefenbrock, Tahoori). The methodology is identical — same fault model, same min-max optimization, same iterative algorithm. The main additions in this journal version are:

| Aspect | DATE 2023 (Conference) | IEEE D&T 2024 (Journal) |
|--------|----------------------|------------------------|
| **Pages** | 2 pages | 7 pages |
| **Models** | MLP, LeNet-5, ConvNet-7 | + VGG-19 |
| **Compaction** | Up to 25× (ConvNet-7) | Up to 50× (VGG-19, 1 pattern) |
| **Baselines** | None explicitly compared | Random images + Adversarial images |
| **Fault list analogy** | Not explicitly framed | "Training set" analogy |
| **Discussions** | Minimal | Expanded discussions on storage, runtime tradeoffs, scalability |
| **Random seed storage** | Mentioned briefly | Explained with motivation |

The core contributions remain the same; this journal version provides stronger evidence of scalability (VGG-19) and demonstrates clear superiority over baselines.

---

## 6. FAQ: Detailed Questions and Answers

The following Q&A addresses common questions about the method.

### (1) What exactly is \(f_i\) in the fault list \(F = \{f_1, f_2, \dots, f_N\}\)? Give a concrete example.

Each \(f_i\) is one concrete **fault instance**: a specific corrupted version of the network. The paper says faults are made by altering the bit-level representation of a randomly chosen subset of parameters, with the pair \((pw, pb)\) fixing "how many weights" and "how many bits per selected weight" are altered. So \(f_1\) and \(f_2\) are two different random corruption patterns of the same type.

**Concrete example:** In a toy network with 10 weights, \(f_1\) might mean "corrupt weights 2 and 7 by flipping 50% of their bits," while \(f_2\) might mean "corrupt weights 1 and 9 by flipping 50% of their bits." Each is a different random draw from the same \((pw, pb)\) distribution.

### (2) How is \(N\) chosen?

The paper does not give a formula for \(N\). It treats \(N\) as a **chosen fault-list size** and reports experiments with \(N \in \{50, 100, 150, 200\}\). So \(N\) is a practical sample size, not something derived from the network size. The reason is that the true multiple-fault space is intractable to enumerate.

### (3) How are the \(f_i\) chosen? Do they try to make them "similar"?

They are chosen as **randomly generated fault patterns** under the same global fault model. The paper explicitly says the fault list consists of randomly generated faults — it is only a finite sample of an enormous fault space. The authors do **not** cluster faults by similarity, locality, or "same region of the network." Instead, the method relies on optimizing against a sample of faults and hoping the resulting patterns generalize to unseen faults of the same fault type.

### (4) If \(N\) does not cover all faults, do they make a new list of uncovered faults? Why not set \(N\) to the total number of faults?

They do **not** enumerate all faults, because the paper says the number of possible multiple faults is **exponential** in the number of fault sites and therefore intractable. What they do: generate a finite fault list, optimize a test pattern, remove the faults that pattern covers, and repeat on the **reduced** list until the list is empty. They do not create a brand-new list of "all remaining faults in the universe" — that would not be feasible.

### (5) What does storing \(f_n\) via seed \(n\) mean?

Instead of saving each full faulted network instance, the paper saves only a **random seed** for each list entry. Later, when \(f_n\) is needed, the same random generation procedure is re-run with seed \(n\) to recreate that exact fault pattern. This avoids storing a large amount of network data for every fault instance.

### (6) How does gradient descent work for multiple faults vs. a single fault?

For **one fault**: compare healthy vs. faulty output, use gradient descent to maximize the difference.

For **multiple faults**, the paper changes the objective into a **robust max-min problem**:

\[
x^\star = \arg\max_x \min_{f \in F} o(x, f)
\]

The test image is optimized not for one specific fault, but for the **worst-covered fault in the current fault list**. In plain language: "find an input that is as effective as possible against the hardest fault among those I still care about." After that image is found, the method tests it against every fault in the list, removes the faults it detects, and repeats. Multiple faults are handled by a robust objective plus an iterative elimination loop.

### (7) What does "compression ratio" mean? What would the original number of test patterns be?

The compression ratio is **fault-list size divided by number of generated test patterns**. In Table 1, they define CR that way. So if the fault list has 200 sampled faults and the method needs 4 test patterns, the compression ratio is \(200/4 = 50\times\).

It is **not** "number of parameters divided by number of tests." They are not enumerating one test per parameter or one test per possible bit flip. The "original" number would be the naive approach of one test per fault in the sampled list.

### (8) In absolute numbers, how many test patterns are needed for VGG-19?

For the VGG-19 rows in Table 1, the proposed method uses only **single-digit test patterns**: 1, 2, or 4 patterns depending on the \((pw, pb)\) setting. This is for sampled fault lists of size 50–200. The paper reports 100% coverage on those targeted fault lists and up to 99.9% coverage on 1000 unseen faults.

### (9) What is the "execution time" in the table? Generation time or testing time?

It is the time to **generate** the test patterns, not to apply them during field testing. The paper explicitly says "execution time required to generate the test patterns" and compares it to random images (cheap per-image generation but many needed) and adversarial images (short generation time but low coverage). The paper does not specify the exact CPU/GPU hardware for timing.

### (10) Explain the scalability claim: why does generation time grow with model size, but the number of test generation runs stays constant?

Each optimization step evaluates the network and computes gradients, so a bigger model makes **each generation run** slower. But the **number of runs** is controlled by the fault-list size and the iterative compaction procedure, not by the number of parameters. Since the method optimizes a compact set of test patterns against a finite sampled fault list, the number of generated patterns stays small even as the network gets larger. The scalability benefit is: **offline generation cost increases, but the number of final test patterns does not scale with parameter count**.

### (11) What does 100% fault coverage actually mean? What about faults outside the fault list?

This is arguably the most important nuance. The **100% fault coverage** claim applies only to the sampled fault list of size \(N\). The paper does **not** claim "we can detect all possible faults." The interesting result is not the 100% itself (which is expected when patterns are optimized against the list), but rather:

1. **Compaction:** Only a handful of test patterns cover the entire sampled list — 1 pattern for VGG-19 in some settings.
2. **Generalization:** The patterns are tested against **1000 unseen faults** (same fault distribution, not in the list) and achieve up to **99.9% coverage**.

The unseen fault coverage is the metric that really matters — it estimates real-world performance. However, there is an important caveat: the unseen faults come from the **same fault distribution** (\(pw, pb\) combination). The paper does not test generalization to:
- Different fault distributions
- Different hardware defect mechanisms
- Spatially correlated faults
- Layer-specific faults
- Manufacturing clusters or aging effects

Analogy: the fault list is a "training set," the unseen faults are a "test set," and the test patterns are the learned model. The 99.9% unseen coverage is essentially the test accuracy on the same distribution.

---

## 7. Research Gaps

The following gaps are open problems that this method does not address and that represent important directions for future work, particularly in the context of extending ATPG to modern architectures like Large Language Models.

### (1) Scalability to billions of parameters

The largest model tested is VGG-19 (~144M parameters). Modern LLMs have 7B–175B+ parameters. Each test pattern generation run requires:
- Full forward pass through the model for *every fault* in the fault list (to compute \(\min_{f \in F} o(x, f)\)).
- Backward pass through the model for gradient computation.

For a 7B-parameter model with a fault list of size \(N=200\), this means 200 forward passes + 1 backward pass per optimization step. The per-step cost scales linearly with both model size and fault list size, making this approach potentially infeasible at LLM scale without algorithmic modifications.

### (2) Adapting to LLMs and the discrete token problem

This method operates on continuous input spaces (pixel values in [0, 255]). LLMs operate on **discrete token spaces** — inputs are integer token IDs from a finite vocabulary. Gradient-based optimization on discrete inputs is not directly applicable because:

- The argmax over the vocabulary is non-differentiable.
- Starting from a random token sequence and applying gradient updates is undefined (tokens are categorical, not continuous).
- Even with soft relaxations (e.g., Gumbel-Softmax, continuous embeddings), the optimized "input" may not correspond to any valid token sequence.

Potential workarounds include:
- **Continuous embedding optimization:** Optimize in the embedding space rather than the token space, then project back to the nearest valid tokens.
- **Prompt-level patterns:** Generate test patterns at the prompt level rather than individual token level.
- **Latent-space perturbations:** Instead of optimizing inputs, optimize latent representations that can be decoded back to prompts.

None of these are trivial, and none are explored in this paper.

### (3) Weight importance for fault list construction

The current method selects faults **uniformly at random** across all weights. However, multiple studies (PrisonBreak, SBFA, SilentStriker, BitFlipScope) have shown that **LLM weights have highly uneven importance** — a single critical weight flip can jailbreak an LLM, while most weight flips have negligible effect. This suggests several improvements to fault list construction:

- **Importance-weighted sampling:** Instead of uniform random faults, sample faults from a distribution that over-represents critical weights (e.g., weights with high sensitivity or attention scores).
- **Stratified fault lists:** Include both random faults (for coverage breadth) and targeted faults on critical weights (for coverage of dangerous failure modes).
- **Layer-aware sampling:** Earlier layers and attention projection matrices may be more fault-sensitive than others. A fault list stratified by layer importance could yield more informative test patterns.
- **Combination approach:** A fault list that mixes random and importance-weighted faults might improve both targeted coverage and generalization to unseen faults.

This paper does not consider weight importance at all in fault list construction.

### (4) Better analysis of unseen fault coverage

The paper's strongest result is 99.9% coverage on *unseen* faults. However, the unseen faults are generated from the **same random distribution** as the training fault list. A more rigorous evaluation would test generalization across different fault *types*:

- **Critical-weight faults:** How well do patterns trained on random weight faults detect faults injected only on the *most important* weights? This is the more relevant scenario for real attacks (PrisonBreak, SBFA).
- **Non-critical faults:** How well do they detect faults on *least important* weights? This tests whether patterns truly learn the fault type or just exploit shortcuts.
- **Faults of varying severity:** A fault that flips 100% of bits on one critical weight vs. 5% of bits spread across 10% of weights are qualitatively different — do patterns trained on one regime transfer to another?
- **Spatially correlated faults:** Manufacturing defects often affect adjacent memory cells. The random independent fault model does not capture this.
- **Structured faults:** Entire rows/columns of a crossbar failing together.

Without this analysis, the 99.9% unseen coverage result is only known to hold for random i.i.d. faults of the same type. It is **not yet shown** to generalize to the fault distributions that matter most for safety-critical deployment.

---

## Comparison with Related ATPG Approaches

This paper (Moussa et al., IEEE D&T 2024) is the **journal extension** of the DATE 2023 compact pattern paper. The key differences from other ATPG-related papers on this site:

| Aspect | **This Paper** (IEEE D&T 2024) | **DATE 2023 (compact)** | **ATPG & Compaction for DNN** (Zhang et al.) | **ATPG for Printed Neuro Circuits** (2025) |
|--------|-------------------------------|------------------------|---------------------------------------------|-------------------------------------------|
| **Target** | DNN accelerators | DNN accelerators | DNNs (software model) | Printed neuromorphic circuits |
| **Fault Model** | Multiple bit-level weight faults (pw, pb) | Same | Stuck-at neuron/filter output | Crossbar, p-tanh, p-inv (analog) |
| **Fault Scope** | Multiple faults (simultaneous) | Same | Single fault per test | Single fault assumption |
| **Detection** | Misclassification (label change) | Same | Output deviation (Euclidean) | Output deviation (KL divergence) |
| **Optimization** | Min-max (max lower bound) | Same | Gradient-based (single fault) | Gradient-based (KL divergence) |
| **Compaction** | Iterative covering via min-max | Same | K-means + greedy set cover | Not explicitly addressed |
| **Key Metric** | Compaction ratio, unseen coverage | Compaction ratio, unseen coverage | Fault coverage | Fault coverage (%) |
| **Baselines** | Random + adversarial images | None | Not compared | Random patterns |
| **Largest Model** | **VGG-19** (19 layers) | ConvNet-7 (7 layers) | ConvNet-7 | Small pNCs (9 models) |

The main distinction from the non-Tahoori-group papers is the **multiple-fault model** and the **misclassification criterion**. The Zhang et al. paper (ATPG & Compaction for DNN) targets single stuck-at neuron faults using output deviation as detection — a fundamentally different fault model and detection philosophy.
