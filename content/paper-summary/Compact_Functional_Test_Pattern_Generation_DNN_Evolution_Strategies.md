---
title: 'Compact Functional Test Pattern Generation for DNNs Using Evolution Strategies'
date: 2026-07-01 10:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Compact Functional Test Pattern Generation for DNNs Using Evolution Strategies

**Link to Paper:** https://doi.org/10.1109/VTS69484.2026.11563375 (VTS 2026)

**Date:** 2026

**Paper Type:** Automatic Test Pattern Generation, Deep Neural Networks, Evolution Strategies, Black-Box Testing

**Short Abstract:**
This paper proposes a black-box functional testing framework that detects hardware faults in DNNs exclusively through their observable effects on network outputs. Instead of the typical two-phase pipeline (generate patterns first, compact them second), the method uses Covariance Matrix Adaptation Evolution Strategy (CMA-ES) to jointly optimize fault coverage and test-set size in a single step. This is important because the compactness criterion makes the objective non-differentiable, ruling out gradient-based approaches. Across five architectures including CNNs, ResNets, a Vision Transformer, and a segmentation network, the method achieves on average 98.7% fault coverage while using 9× fewer test patterns than a gradient-based baseline, with up to 16.3× compaction in the best case.

## Why CMA-ES Instead of Gradients

The central observation of this paper is that test pattern generation with built-in compaction is fundamentally a non-differentiable optimization problem. The fault coverage metric depends on argmax operations (did the predicted class change or not?), and the decision of which test patterns to keep in the final set is a discrete selection. Gradient-based methods need smooth objectives, which is why prior ATPG work separates generation and compaction into two phases: first use gradients to maximize coverage with a large pattern set, then apply clustering or greedy set cover to prune it down. But this separation is inefficient, because patterns optimized individually may become redundant once they are considered together.

The authors frame a single objective function \\(J(X)\\) that combines three terms: fault coverage, output deviation, and test-set size. Fault coverage measures what fraction of faults in the fault pool \\(F\\) are detected by at least one pattern in \\(X\\), where a fault is detected if the predicted class label changes between the fault-free and faulty network. Output deviation captures the maximum softmax \\(\\ell_2\\) distance between the two outputs, averaged over faults. Test-set size is the number of active patterns, normalized by a user-defined upper bound \\(K\\). The objective rewards high coverage and large deviations while penalizing too many patterns. Crucially, the argmax operations in the coverage term and the binary active/inactive decision for each pattern make this objective non-differentiable.

Because gradient descent cannot optimize \\(J(X)\\) directly, the paper turns to CMA-ES, an evolutionary algorithm that samples candidate solutions from a multivariate Gaussian distribution and iteratively updates its mean and covariance to bias sampling toward better regions of the search space. CMA-ES is a natural fit here: it handles non-differentiable, multimodal landscapes well, it adapts its exploration-exploitation balance dynamically, and it is widely regarded as one of the most effective black-box optimizers for continuous search spaces.

## How the Method Works

The authors redesign the test pattern generation task so that CMA-ES can operate on it. Each individual in the CMA-ES population encodes an entire test suite as a flattened vector \\(Z \\in \\mathbb{R}^{K \\times (d+1)}\\), where \\(K\\) is the maximum number of patterns allowed and \\(d\\) is the flattened input dimension (for images, \\(d = \\text{height} \\times \\text{width} \\times \\text{channels}\\)). The extra dimension per pattern is an activation mask \\(m_k \\in [0,1]\\) that controls whether the pattern is actually used. If \\(m_k\\) exceeds a threshold \\(\\tau\\), the pattern is active; otherwise it is ignored. This mask mechanism is what lets CMA-ES dynamically shrink or grow the effective suite size while keeping the genotype length fixed.

During optimization, CMA-ES samples candidate test suites, evaluates \\(J(X)\\) for each by running them through the fault ensemble, and updates the search distribution to favor lower objective values. The initial mean is seeded from training samples with added Gaussian noise, and the mask means are initialized so that most patterns start inactive and only a few are likely active. Two stages of optimization are used. In the first stage, hyperparameters (population size, step size, loss weights, threshold value) are tuned with short CMA-ES runs and early stopping. The best configuration is then used in the second stage for a longer run that produces the final test suite.

## Fault Models and Experimental Setup

The paper evaluates on three fault model families. Bit-flip faults select a fraction \\(p_w\\) of weights and flip a fraction \\(p_b\\) of their bits, with three variants: BF-Random (random bit positions), BF-MSB (always the most significant bit), and BF-LSB (always the least significant bit). Gaussian perturbation faults add noise \\(\\epsilon \\sim \\mathcal{N}(0, \\gamma\\cdot\\sigma)\\) to selected weights. Stuck-at faults cover both weight-level stuck-at-0/1 (forcing individual weights to constant 0 or 1) and neuron-level stuck-at-0 (zeroing all outgoing weights from a randomly selected neuron).

Five models are tested, spanning four architectural families: CNN-8L on CIFAR-10 (convolutional, 1.29M params), ResNet-19 on Tiny-ImageNet (residual CNN, 11.28M params), ResNet-20 on CIFAR-10 (residual CNN, 0.27M params), ViT-Tiny on SVHN (transformer, 5.53M params), and a ResNet-50 with PPM-Deeplab head on ADE20K (encoder-decoder segmentation, 51.70M params). The gradient-based baseline uses the method from Moussa et al. (DATE 2023) with the standard generate-then-compact pipeline. Both methods use identical fault-injection settings per benchmark.

## Results

On the training fault pool, the CMA-ES approach matches or exceeds gradient-based coverage across all architectures while using far fewer patterns. For CNN-8L, coverage improves from 92.3% to 96.7% while patterns shrink from 19 to 3 (6.3×). For ResNet-20, both methods reach 100% coverage, but the gradient baseline needs 98 patterns whereas CMA-ES achieves it with just 6 (16.3× compaction). ViT-Tiny reaches 100% coverage with 4 patterns versus 12, and the ADE20K segmentation model reaches 97.5% with 3 patterns versus 8. Averaged across all benchmarks, the proposed method achieves 98.7% coverage using on average 3.2 patterns, compared to 97.5% coverage with 28.8 patterns for the baseline, a 9× compaction.

The paper also tests generalization to unseen faults by evaluating suites optimized on a training fault pool \\(F_{\\text{tr}}\\) against a disjoint validation pool \\(F_{\\text{val}}\\) of 30 faulty ResNet-20 instances per fault model. For BF-LSB, BF-MSB, and weight perturbation faults, the gradient baseline drops to 43.3-70.0% coverage on \\(F_{\\text{val}}\\), while CMA-ES maintains 96.7-100%. For stuck-at faults, both methods reach 100% coverage. The compact suites also reduce execution time per faulty DNN from 0.17-0.24 seconds to 0.01-0.02 seconds and storage size from 0.99-1.44 MB to 0.03-0.10 MB.

An interesting finding in the discussion is that MSB and LSB bit-flips produce similar accuracy-drop curves at medium and high severities, which the authors attribute to most learned weights having small magnitude combined with batch normalization and ReLU — many nominal MSB flips behave more like moderate rescalings inside redundant channels rather than fully destructive changes. The practical consequence is that a compact test suite effective at exposing generic bit-flip faults will typically detect both LSB and MSB errors, but inferring which specific bit position flipped from functional outputs alone is considerably more difficult.

The trade-off is in offline generation cost. CMA-ES takes on the order of ten hours per model, slower than the gradient-based baseline. But this cost is paid once, and once the compact suite is obtained, in-field testing requires evaluating only 1-10 inputs per DNN, making runtime and storage overhead during deployment negligible.

## Feasibility for Test Pattern Generation on LLMs

Several aspects of this paper are relevant to extending ATPG to large language models.

**Non-differentiable objectives are the norm for LLM test generation.** If the goal is to detect faults through discrete token outputs (rather than through continuous logits), the objective becomes non-differentiable in the same way. The CMA-ES approach naturally handles this. However, CMA-ES operates in a continuous search space, and finding a suitable input encoding is the first challenge. For image inputs, each pixel is already a continuous value and the search space dimension is \\(K \\times (h \\times w \\times c)\\), which is manageable. For text, the search space would be over token sequences, requiring either a continuous relaxation (like Gumbel-Softmax) to parameterize distributions over tokens, or a latent-space embedding approach where CMA-ES optimizes in embedding space and the result is projected back to tokens.

**The activation mask mechanism transfers directly.** The idea of encoding an entire test suite with binary masks and letting the optimizer decide which patterns to keep is independent of the input modality. For LLMs, the same approach would allow generating \\(K\\) candidate prompt sequences and learning which subset forms the most compact high-coverage suite.

**The fault coverage criterion needs rethinking for autoregressive models.** The current method uses label mismatch (argmax change) as the detection criterion, which works for classifiers and even segmentation networks. For autoregressive LLMs, where the output is a generated sequence, defining what counts as "detected" is more complex. Options include perplexity shift, generation divergence at critical tokens, or a separate judge model comparing outputs. None of these have the clean argmax property of classification, which makes the objective even less smooth and further favors black-box evolutionary approaches over gradient-based ones.

**The computational cost is the main barrier.** CMA-ES requires evaluating each candidate suite against a pool of faulty networks. For a 7B parameter model with 60+ faulty instances, one generation with population size 10 would require 600+ forward passes. Even on modern hardware, ten hours of offline generation for a CNN with ~1M parameters could easily become weeks for an LLM. Accelerating this with surrogate models, gradient-guided CMA-ES, or hybrid evolutionary-gradient approaches is listed as future work in the paper and would be a prerequisite for LLM-scale application.

**The generalization to unseen faults is encouraging.** The paper demonstrates that suites optimized on a training fault pool maintain high coverage on disjoint validation faults. If this property holds for LLMs as well, it would mean that compact test suites for LLMs could be generated once (albeit expensively) and then used to detect a broad range of hardware faults during deployment without regenerating patterns for each new fault instance.
