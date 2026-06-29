---
title: 'Gradient-based Adversarial Attacks against Text Transformers'
date: 2026-06-19 09:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Gradient-based Adversarial Attacks against Text Transformers

**Link to Paper:** https://arxiv.org/abs/2104.13733

**Date:** 15. Apr. 2021

**Paper Type:** Adversarial Attacks, Natural Language Processing, Transformers, Gradient-Based Optimization

**Short Abstract:**
This paper proposes **GBDA (Gradient-based Distributional Attack)**, the first general-purpose gradient-based attack against transformer models for text. Instead of searching for a single discrete adversarial example, GBDA parameterizes a **distribution over token sequences** using a continuous matrix. This enables standard gradient-based optimization via the Gumbel-Softmax relaxation. The method incorporates differentiable fluency (language model perplexity) and semantic similarity (BERTScore) constraints to produce natural-looking adversarial text. GBDA achieves state-of-the-art attack success rates in both white-box and black-box transfer settings across multiple NLP benchmarks, while preserving grammatical correctness and semantic meaning.

## 1. Introduction

Deep neural networks are vulnerable to adversarial examples: small, often imperceptible perturbations that cause a model to misclassify an input. While gradient-based attacks are highly successful in image and speech domains (where inputs like pixels or sound waves are continuous), text data poses two fundamental challenges:

1. **Discreteness:** Text is composed of discrete tokens (words or subwords). A model cannot mathematically "nudge" a word slightly to see how the output changes; it must either keep the word or replace it entirely with another discrete token. This blocks standard gradient descent.
2. **Perceptibility:** There is no natural distance metric for text. Inserting a single word like "not" can completely flip the meaning of a sentence, yet only represents an edit distance of 1. 

Prior text attacks rely on heuristic word-replacement strategies (such as synonym substitution or masked language model predictions) combined with black-box greedy or beam search. These methods suffer from:
- **Unnatural perturbations**: Misspellings, grammatical errors, and semantic drift.
- **Inefficient optimization**: Suboptimal results due to zeroth-order (trial-and-error) search.
- **Sequential token dependencies**: Tokens are modified one by one in an arbitrary order, ignoring the combinatorial interactions between multiple word changes.

GBDA overcomes these limitations by reformulating the attack as a **distributional search** over token sequences.

## 2. The Core Problem: Why Gradient Descent Fails on Text

In image attacks, an input is a continuous tensor of pixels \( x \in \mathbb{R}^{H \times W \times C} \). The attack objective is to minimize a loss function:

\[
\min_{x'} \ell(x', y; h) + \lambda \cdot \rho(x, x')
\]

This equation is directly differentiable with respect to the image \( x' \). Calculating the gradient \( \nabla_{x'} \ell \) tells the attacker exactly how to change each pixel's color value slightly to increase the model's error. Taking a step in that direction yields a perturbed image.

For text, an input is a sequence of **discrete token indices** \( z = z_1 z_2 \dots z_n \) where each token \( z_i \) is an integer from \( 1 \) to \( V \) (the vocabulary size). Attempting to differentiate with respect to \( z_i \) yields an undefined gradient. It is not possible to take a "small step" from token #42 (e.g., "cat") to token #43 (e.g., "dog") because the token space has no topology or inherent distance. The loss function operates like a step function over a discrete set.

**The key insight of GBDA:** Instead of optimizing a single, rigid token sequence directly, the method optimizes a **continuous-valued matrix** \( \Theta \in \mathbb{R}^{n \times V} \). This matrix parameterizes a probability distribution over all possible token sequences. The attacker then samples discrete sequences from this continuous distribution.

## 3. Methodology: How GBDA Makes Discrete Tokens Differentiable

### 3.1 The Adversarial Distribution

To start, a parameter matrix \( \Theta \in \mathbb{R}^{n \times V} \) is defined. This matrix acts as a continuous "score sheet" where \( n \) is the sequence length and \( V \) is the vocabulary size. For each position \( i \) in the sentence, the model applies a Softmax function to the scores to turn them into a valid probability vector:

\[
\pi_i = \text{Softmax}(\Theta_i) \in \mathbb{R}^V
\]

This defines a categorical distribution \( P_\Theta \). From this distribution, each token \( z_i \) is independently drawn like a weighted lottery:

\[
z_i \sim \text{Categorical}(\pi_i)
\]

The optimization goal is to adjust the score sheet \( \Theta \) to minimize the expected loss of the attack:

\[
\min_{\Theta \in \mathbb{R}^{n \times V}} \mathbb{E}_{z \sim P_\Theta} \left[ \ell(z, y; h) \right]
\]

However, this expectation is **still non-differentiable**. Sampling from a categorical distribution is a discrete, step-like operation. Drawing a token is akin to flipping a weighted coin; there is no smooth slope to descend, meaning standard backpropagation cannot calculate how changing \( \Theta \) will affect the final loss.

### 3.2 The Gumbel-Softmax Trick: The Heart of the Method

To solve the non-differentiability problem, GBDA uses the Gumbel-Softmax distribution (Jang et al., 2016), which provides a **continuous relaxation** of the categorical sampling process. Instead of forcing a hard choice between discrete tokens, the method allows the model to mathematically "hedge its bets" using blended probabilities. 

**Step 1: The Gumbel-Max trick.** 
Mathematically, drawing a sample from a Categorical distribution can be reparameterized (rewritten) as an optimization problem:

\[
z_i = \arg\max_{v \in V} \left( \log \pi_{i,v} + g_{i,v} \right)
\]

Here, \( g_{i,v} \sim \text{Gumbel}(0, 1) \) represents i.i.d. Gumbel noise samples. The variable \( g_{i,v} \) acts as a random nudge added to each token's log-probability. This is an exact reparameterization: adding this specific statistical noise and picking the highest value produces the exact same probabilities as standard categorical sampling.

**Step 2: The Softmax relaxation.** 
The \( \arg\max \) operation above is the source of the discreteness, as it outputs a hard one-hot vector (picking exactly one winner and setting all others to zero). To make it differentiable, the \( \arg\max \) is replaced with a Softmax function to get a **continuous, differentiable approximation**:

\[
(\tilde{\pi}_i)_j = \frac{\exp\left( (\Theta_{i,j} + g_{i,j}) / T \right)}{\sum_{v=1}^{V} \exp\left( (\Theta_{i,v} + g_{i,v}) / T \right)}
\]

In this equation:
- \( g_{i,j} \sim \text{Gumbel}(0, 1) \) is the random noise for exploration.
- \( T > 0 \) is a **temperature parameter** that controls how "hard" or "soft" this approximation is.
- \( \tilde{\pi}_i \) is no longer a single token, but a **probability vector** that is fully differentiable with respect to the original scores \( \Theta_{i,j} \).

**The temperature \( T \) is critical:** The temperature parameter behaves like heating or cooling a material.
- **As \( T \to 0 \) (Cold):** The distribution "freezes" back into a hard argmax (one-hot), closely matching a true categorical sample. However, the gradients become sharp and ill-behaved (variance explodes), making learning unstable.
- **As \( T \to \infty \) (Hot):** The distribution "melts" into a uniform distribution, giving very smooth gradients but a poor approximation of the actual discrete choice.
- In practice, \( T \) is set to a small positive value (e.g., 1.0) to balance smooth gradient flow with approximation fidelity.

**Step 3: Embedding relaxation.** 
Transformers use an embedding lookup table \( e(\cdot) \) to convert discrete tokens into continuous vectors. Since the method no longer produces a single token, GBDA computes a **convex combination** (a weighted average) of *all* token embeddings in the vocabulary, weighted by the relaxed probabilities \( \tilde{\pi}_i \):

\[
e(\tilde{\pi}_i) = \sum_{j=1}^{V} (\tilde{\pi}_i)_j \cdot e(j) \in \mathbb{R}^d
\]

For instance, rather than passing the embedding for a single word such as "dog", the model passes a blended vector that might be 80% "dog", 15% "cat", and 5% "bird." This operation is fully differentiable with respect to \( \tilde{\pi}_i \), and since \( \tilde{\pi}_i \) is differentiable with respect to \( \Theta_i \), gradients can flow all the way back to the original score matrix.

**The complete chain of differentiation:**

```
Θ (continuous score matrix)
  ↓
Softmax(Θ_i + g_i) / T  ← Add Gumbel noise + apply temperature
  ↓
π̃_i (relaxed probability vector over vocabulary)
  ↓
e(π̃_i) = Σ_j (π̃_i)_j · e(j)  ← blend token embeddings together
  ↓
Transformer forward pass (takes continuous blended input → continuous output)
  ↓
Loss ℓ (adversarial loss + constraints)
  ↓
∇_Θ ℓ  ← backpropagation through the entire chain
  ↓
Adam update of Θ (update the scores)
```

**This is the core breakthrough:** The discrete token selection is completely bypassed during optimization. It is no longer necessary to "jump" between discrete words; the probabilities \( \pi_i \) are smoothly adjusted via gradient descent on the continuous matrix \( \Theta \).

### 3.3 Soft Constraints for Naturalness

If the optimization solely targets fooling the target model, the attack might replace the original sentence with gibberish such as "zzx qwer banana" to break the classifier. To ensure the generated adversarial text looks like natural language and preserves meaning, GBDA incorporates two differentiable constraints:

**Fluency constraint (language model perplexity):** 
To keep the text grammatically sound, GBDA uses a causal language model \( g \) (like GPT-2) to compute the negative log-likelihood of the relaxed token sequence:

\[
\text{NLL}_g(\tilde{\pi}) = -\sum_{i=1}^{n} \sum_{j=1}^{V} (\tilde{\pi}_i)_j \cdot \log g(e(\tilde{\pi}_1) \dots e(\tilde{\pi}_{i-1}))_j
\]

In plain terms, this measures how "surprised" the language model is by the generated sequence. It penalizes the attack if it generates sequences that are highly unlikely under natural human language.

**Semantic similarity constraint (BERTScore):** 
To ensure the attack does not completely change the meaning of the sentence, GBDA uses BERTScore to measure token-level similarity between the original input \( x \) and the perturbed sequence \( \tilde{\pi} \):

\[
\rho_g(x, \tilde{\pi}) = 1 - \text{BERTScore}(x, \tilde{\pi})
\]

This is differentiable because BERTScore uses soft cosine-similarity over contextualized embeddings, allowing gradients to flow.

### 3.4 Complete Objective

The full optimization problem combines the attack goal with these guardrails:

\[
\mathcal{L}(\Theta) = \underbrace{\mathbb{E}_{\tilde{\pi} \sim \tilde{P}_\Theta} \left[ \ell(e(\tilde{\pi}), y; h) \right]}_{\text{adversarial loss}} + \lambda_{\text{lm}} \underbrace{\text{NLL}_g(\tilde{\pi})}_{\text{fluency}} + \lambda_{\text{sim}} \underbrace{\rho_g(x, \tilde{\pi})}_{\text{semantic similarity}}
\]

In summary, the **Total Loss** is the sum of: (Fooling the target model) + (Weight × Keeping it fluent) + (Weight × Keeping meaning the same).

Where:
- \( \ell \) is the **margin loss**, which pushes the target model's prediction away from the true label: \( \ell(z, y; h) = \max(0, \max_{k \neq y} \phi_h(z)_k - \phi_h(z)_y + \kappa) \)
- \( \lambda_{\text{lm}} \) and \( \lambda_{\text{sim}} \) are hyperparameters tuning how much weight is given to fluency vs. meaning.
- Optimization uses Adam with learning rate 0.3, batch size 10, for 100 iterations.

### 3.5 Sampling Adversarial Text After Optimization

During training, "blended" embeddings are used to calculate gradients. Ultimately, however, a Transformer requires real discrete words. Once the score matrix \( \Theta \) is fully optimized:

1. **Draw hard samples:** The probabilities are snapped back to discrete reality. A sample \( z \sim P_\Theta \) is drawn by taking the argmax over the probabilities: \( z_i = \arg\max_j \Theta_{i,j} \). This yields an actual sequence of discrete text tokens.
2. **Test against the model:** This real text is fed into the target model. If \( h(z) \neq y \) (the model is fooled), it is a valid adversarial example.
3. **Repeat:** Up to 100 samples are drawn until one succeeds.

**Transfer attack capability:** Since \( P_\Theta \) defines a whole distribution of potential sentences (not just a single optimized sentence), it can be sampled indefinitely to query a *different* target model. This enables a powerful black-box transfer attack that only requires the hard-label outputs (e.g., "Positive" or "Negative") from the target model, with no need for internal continuous confidence scores.

## 4. Summary of Results

| Model | Task | Clean Acc. | Adv. Acc. (after attack) | Cosine Sim. |
|-------|------|-----------|------------------------|------------|
| **BERT** | AG News | 95.1% | **2.5%** | 0.82 |
| **BERT** | Yelp | 97.3% | **4.7%** | 0.92 |
| **BERT** | IMDB | 93.0% | **3.0%** | 0.92 |
| **GPT-2** | DBPedia | 99.2% | **5.2%** | 0.91 |
| **XLM (en-de)** | MNLI (m.) | 76.9% | **1.3%/8.4%** | 0.74/0.80 |

Key findings:
- Reduces model accuracy to below 10% in almost all cases.
- Maintains cosine similarity > 0.8, proving semantic preservation.
- Transfer attack (GPT-2 → BERT, RoBERTa, ALBERT, XLNet) matches or exceeds prior black-box methods with fewer queries.
- Total runtime: ~20 seconds per example, on par with black-box attacks like BERT-Attack.

## 5. Limitations

1. **Token replacements only**: The method cannot insert or delete tokens; the sequence length \( n \) is fixed.
2. **Over-parameterized**: The matrix \( \Theta \) is size \( n \times V \), which is computationally excessive for short sentences requiring only a few token changes.
3. **Re-tokenization artifacts**: There is a ~2% token error rate when converting back to raw text. For example, "juicy" might be tokenized as "jui-" + "cy" during the attack, but reconstructed as "juic-" + "y" after re-tokenization.

---

### Feasibility for Test Pattern Generation on LLMs

GBDA is directly relevant to the problem of generating **test patterns for fault detection in LLMs** (the ATPG-for-LLMs problem). Automatic Test Pattern Generation (ATPG) seeks to find inputs that trigger specific hardware or software faults in a model. Here is an analysis of what transfers from GBDA to ATPG and what needs adaptation.

#### What Works Directly

**1. The discrete-token gradient problem is solved.** This is the primary challenge in extending ATPG from traditional DNNs (continuous pixel space) to LLMs (discrete token space). GBDA's Gumbel-Softmax formulation provides a principled, well-tested solution: parameterize a distribution over token sequences, compute gradients through the relaxed sampling process, and optimize with standard gradient descent.

**2. The core optimization pipeline maps cleanly.** Instead of an adversarial margin loss (aiming for misclassification), the objective is replaced with a **divergence loss** that measures the difference between fault-free and faulty model outputs:

\[
\mathcal{L}_{\text{ATPG}}(\Theta) = \mathbb{E}_{\tilde{\pi} \sim \tilde{P}_\Theta} \left[ \text{KL}\big( h(e(\tilde{\pi})) \parallel h_f(e(\tilde{\pi})) \big) \right] + \lambda_{\text{lm}} \cdot \text{NLL}_g(\tilde{\pi})
\]

Here, \( h_f \) is the faulty model (with an injected fault, such as a bit-flip in a weight tensor). The Kullback-Leibler (KL) divergence is differentiable through both the healthy model \( h \) and the faulty model \( h_f \), allowing the optimizer to find inputs that cause the two models to behave differently.

**3. The fluency constraint is beneficial, not incidental.** Unlike image-domain ATPG where any continuous pixel vector works as a test pattern, text patterns that are not valid language may traverse different internal pathways in the LLM. The language model perplexity constraint keeps patterns grammatical, ensuring test patterns exercise realistic computation pathways and making the divergence signal more reliable.

**4. Distributional sampling enables ensemble testing.** After optimization, the distribution \( P_\Theta \) can be sampled \( k \) times. If *any* sample triggers divergent behavior between \( h \) and \( h_f \), the fault is detected. This approach is robust to the stochasticity of the Gumbel-Softmax process.

#### What Needs Adaptation

**1. Loss function: margin → KL divergence.** The margin loss used in GBDA targets misclassification (a hard threshold). For fault detection, the goal is to measure **output distribution shift**, where KL divergence between the softmax outputs of \( h \) and \( h_f \) captures even small deviations. For autoregressive LLMs, a **per-position KL summed over the sequence** is used:

\[
\text{KL}(h \parallel h_f) = \sum_{t=1}^{n} \sum_{v \in V} h(\mathbf{x})_{t,v} \log \frac{h(\mathbf{x})_{t,v}}{h_f(\mathbf{x})_{t,v}}
\]

**2. Remove (or weaken) the similarity constraint.** GBDA's BERTScore constraint enforces imperceptibility, which is irrelevant for ATPG. The hyperparameter \( \lambda_{\text{sim}} \) is set to 0. If patterns degenerate to nonsense (despite the fluency constraint), a weak similarity to a natural-language seed can be added as regularization.

**3. The autoregressive dimension is an open challenge.** GBDA was designed for classification tasks where the output is a single label. For autoregressive LLM generation, the KL divergence must account for position-specific effects. Per-position KL summed over the sequence is a pragmatic starting point, but the optimal formulation is an open research question.

#### Computational Cost Estimate

| Component | Cost per optimization step |
|-----------|---------------------------|
| Forward pass through fault-free model \( h \) | 1× forward |
| Forward pass through faulty model \( h_f \) | 1× forward |
| Backward pass for KL gradient | 1× backward |
| Language model (fluency) forward + backward | 1× forward + 1× backward |
| **Total** | **~3× forward + ~2× backward per step** |

- **GPT-2 (124M):** ~30 seconds per fault on one GPU
- **LLaMA 3.2 (7B):** ~5–10 minutes per fault on one GPU
- **Batch of 200 faults:** ~16–33 hours

**Key mitigating factor:** GBDA's transfer property (demonstrated in the original paper) suggests patterns optimized for one faulty instance may transfer to other faults on the same architecture. If transfer holds for ATPG, the computational cost drops to **one optimization per architecture** rather than per individual fault.
