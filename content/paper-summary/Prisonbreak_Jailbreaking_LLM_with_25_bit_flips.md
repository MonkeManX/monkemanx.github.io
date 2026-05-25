---
title: 'PRISONBREAK: Jailbreaking Large Language Models With at Most Twenty-Five Targeted Bit-flips'
date: 2026-05-08 14:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** PRISONBREAK: Jailbreaking Large Language Models With at Most Twenty-Five Targeted Bit-flips

**Link to Paper:** https://arxiv.org/abs/2412.07192

**Date:** 10. Dec. 2024

**Paper Type:** LLM, Attack-Paper, Jailbreaking

**Short Abstract:**
This paper is about jailbreaking LLMs, which means circumventing their protections against producing harmful content. To do this, their attack needs to flip at most 5–25 bits, which is 40× fewer bits than prior attacks and 20× faster than previous methods.
They evaluate their method on 10 different open-source LLMs and achieve an attack success rate of 80–98%, with minimal utility and performance loss in the models.

## 1. Introduction

Previous research has mostly focused on convolutional neural networks and classification tasks, leaving LLMs largely unstudied in this context. This paper investigates whether modern, safety-aligned language models can be “jailbroken” not through prompt engineering, but through hardware-level corruption of their parameters.

The authors introduce **PRISONBREAK**, an attack that combines targeted bit-flip injection (e.g., via Rowhammer-style memory faults) with an optimization method to identify the most impactful bits. Their key insight is a “progressive bit-search” strategy that iteratively finds small sets of critical bits whose corruption causes large behavioral changes.

Across multiple open-source LLM families (including VICUNA, LLAMA, and others), they show that flipping only a small number of bits (5–25) can remove safety alignment and produce harmful outputs with high success rates (around 80–98%), while still preserving general model performance. The attack also transfers across similar models and can work even in realistic shared-GPU environments with modern memory hardware.

Further analysis shows that certain internal components (like exponent bits and projection layers) are especially vulnerable. Interestingly, the jailbreak does not rely on suppressing refusal mechanisms in activation space, suggesting a different failure mode than prompt-based jailbreaks.

Overall, the paper argues that LLMs are vulnerable not only at the software/prompt level but also at the hardware-memory level, posing a serious and underexplored security risk.

## 2. Background

### 2.1 Aligning and jailbreaking language models.

LLM are trained on massive text datasets and can perform many tasks, but they can also be misused to generate harmful or misleading content. To reduce this risk, developers use **alignment techniques** such as supervised fine-tuning, reinforcement learning from human feedback (RLHF), and direct preference optimization (DPO). These methods aim to make models helpful and ensure they refuse unsafe or harmful requests.

Despite this, research shows that aligned models can still be “jailbroken,” meaning attackers can trick them into producing harmful outputs. Most existing jailbreaks are **prompt-based**, where carefully crafted inputs manipulate the model into bypassing its safety rules.
Other approaches go deeper by modifying the model’s parameters directly (e.g., fine-tuning billions of weights) to remove alignment entirely.

### 2.2 Half-precision floating-point numbers

Modern language models store parameters using the IEEE 754 floating-point format, often in half-precision (16-bit) to save memory. In this format:
- 1 bit is for the sign (positive/negative),
- 5 bits are for the exponent (controls scale),
- 10 bits are for the mantissa (controls precision/detail).

Flipping a mantissa bit slightly changes the value (a small numerical perturbation). Flipping an exponent bit can drastically change the value because it changes the scale of the number by orders of magnitude.

### 2.3 Rowhammer

Rowhammer is an Hardware-based attack technique used to induce errors in memory (DRAM) that can be exploited in machine learning systems.

Rowhammer works by repeatedly and rapidly accessing (“hammering”) specific memory rows. This causes electrical interference that gradually leaks charge into neighboring rows, eventually flipping bits in adjacent memory cells. These unintended bit-flips are called DRAM disturbance errors.

This attack works both on CPU and GPU.

## 3. Methodology

This passage describes the full design of the **PRISONBREAK attack**, which is a method for jailbreaking language models using carefully chosen bit-flips in memory.

The attack has two main phases:
1. Offline phase (finding the right bits): The attacker first performs a search to identify which parts of the model are most sensitive to corruption.
    * Start by finding **important model weights**, parameters whose small changes strongly affect whether the model refuses harmful requests.
    * Then, test individual **bits inside those weights**
    * The most effective bit-flips are selected and applied to the model.
    * This process is repeated until the model reaches a high jailbreak success rate (e.g., 80–95%).
2. Online phase (executing the attack): Once the critical bits are identified, the attacker triggers the actual corruption in memory.
    - This is done using Rowhammer-based techniques.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 100%;" src="/attachments/prisonbreak_bitflip_overvview.png">
</figure>
{{< /rawhtml >}}

### 3.1 Offline Profiling of Target Bit

#### 3.1.1 Jailbreaking Objective

Prior jailbreak-specific prompt attacks mainly optimize for a simple goal: making the model start its response with **affirmative or compliant tokens** (e.g., “Sure”, “Yes”).

However, this is flawed when used for parameter-level attacks like PRISONBREAK. It leads to two problems:
* **Overfitting:** the model learns to only produce repetitive “yes-like” openings, but the rest of the output becomes meaningless or degraded.
* **Backtracking:** the model may start agreeing but then revert and refuse the harmful request.

So, simply forcing “affirmation” is not enough to reliably produce full harmful outputs. A good jailbreak should not just *start* correctly, but should also produce **coherent harmful content afterward**.

To do this, they design a new objective that encourages both:
1. The model first produces **affirmative tokens** (to bypass refusal behavior),
2. Then continues generating **high-quality harmful content**.

Since there is no ground-truth dataset of “how a fully unaligned model would respond,” they build a **proxy dataset**:
* They take harmful prompts from a benchmark dataset (HARMBENCH).
* They use an **unaligned open-source model** to generate example responses.
* They engineer these responses so they:
  * start with affirmative phrasing,
  * then continue with harmful content.

This becomes their approximation of what a successfully jailbroken model should output.

The loss function they define is essentially a **weighted cross-entropy objective over token sequences**:
* It maximizes the probability of generating the desired response token by token.
* But it applies **higher weight to early tokens(affirmations)** and lower weight to later(harmful content) ones.

This is done because Standard cross-entropy treats all tokens equally, which causes a problem:
* The model might focus too much on later harmful content
* and fail to reliably produce the initial “compliant” opening that helps bypass refusal mechanisms.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 100%;" src="/attachments/prisonbreak_examples_content.png">
</figure>
{{< /rawhtml >}}


#### 3.1.2 Identifying Critical Weights

The attacker defines an importance score based on how sensitive each parameter is to the jailbreak objective \( L_{JB} \).

They compute:

$$
I = |\nabla_\theta L_{JB}|
$$

* \( \theta \): model parameters (weights)
* \( L_{JB} \): the jailbreak objective
* \( \nabla_\theta L_{JB} \): how strongly changing each weight would affect the objective

**Interpretation:**
* Large gradient ⇒ small change to that weight strongly influences jailbreak success
* So those weights are “critical targets”


Instead of randomly testing billions of parameters, gradients give a **directional sensitivity map**:

Because modern LLMs have **billions of parameters**, even gradient ranking is expensive. So the authors introduce pruning strategies:
- Skip unimportant layers: normalization layers, embedding layers, output (“unembedding”) layers
    - This reduces the search space by about **~20%**.
- Top-k filtering within layers: Instead of examining every weight in a layer, they only keep the **top-k most important weights**.
    * Importance = gradient magnitude
    * conservative value: **k = 100**
    - This yields high jailbreak success (80–98%) across models.


#### 3.1.3 Selecting Target Bits

The attacker evaluates each candidate bit by flipping it and measuring how much it improves the jailbreak objective.

They define:
* \( f \): original model
* \( f'_i \): model after flipping bit ( b_i )

$$
S_i = L_{JB}(f'*i) - L*{JB}(f)
$$

**Interpretation:**
* If flipping a bit makes the jailbreak objective better (lower loss / higher success), it gets a better score.
* Bits are sorted so that the most promising jailbreak-inducing bits are tested first.

A key issue: some bit-flips might help jailbreaking but destroy normal model performance. To control this, they define a **utility score**, which measures how well the model still performs on normal tasks:
$$
U(f, D_c) = \frac{1}{n_c} \sum L_{ce}(f, x_i, y_i)
$$

Where:
* \( D_c \): clean dataset (from ALPACA-style instructions)
* \( L_{ce} \): cross-entropy loss
* \( (x_i, y_i) \): prompt and model-generated response

They then measure:

$$
\Delta U = U(f'_i, D_c) - U(f, D_c)
$$

**Decision rule:**
* If \( \Delta U < \tau \) (small degradation), the bit is acceptable and used
* Otherwise, skip that bit

So the attack tries to balance: jailbreak success **and** preserved usefulness


Even after narrowing weights, each weight has **16 bits**, and testing them all is very expensive. So the search space needs to be reduced:
- Gradient sign filtering: If flipping a bit changes weight in the **same direction as gradient**, it is likely to *increase loss incorrectly*. So those bits are skipped
    - This removes ~50% of candidates.
- Focus only on exponent bits: because they have the biggest impact.
    - Reduces search space to 1.5 bit per weight
- Only 0 → 1 flips: flipping bits from 0 to 1 only, this tends to increase magnitude of weights more effectively for the goal.
    - ~1 candidate bit per weight

## 4. Evaluation

The evaluation shows that PRISONBREAK is a highly effective bit-flip attack for jailbreaking open-source language models, achieving an average attack success rate of 89.6%. It outperforms prompt-based jailbreaks and baseline bit-flip methods, and significantly improves over prior bit-flip attacks by about 22% in ASR through better selection of non-destructive, high-impact bits.

Compared to other parameter-based attacks like ORTHO, which modify hundreds of millions to billions of parameters, PRISONBREAK is far more efficient, requiring only 5–25 bit-flips while achieving similar or better success. This makes it practically feasible under Rowhammer constraints.

Across model sizes (1.5B to 70B parameters), there is no clear relationship between scale and robustness, and larger models are not consistently more secure. Alignment methods like RLHF or DPO provide only modest improvements, slightly increasing the number of required bit-flips but not preventing attacks.

Despite its effectiveness, PRISONBREAK preserves model utility well, causing only about a 2.3% drop in accuracy, compared to 15.5% for less targeted bit-flip baselines. Overall, the results show that a very small number of carefully chosen bit-flips can reliably break safety alignment while keeping models largely functional.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/prisonbreak_results.png">
      <figcaption>The attack success rate (ASR) and average accuracy (Acc.) for different jailbreaking attacks. ∆Acc. is the percentage point change relative to the clean performance. For the parameter-based attacks, the number of parameters modified (∆P) are reported. “No Attack" refers to the original models without any compromise.
</figcaption>
</figure>
{{< /rawhtml >}}


## 5. Misc

- Since many open-source models are shared publicly, many are based on each other. If one does not have direct access to the model, one can instead use a model that is publicly accessible to determine the bits that need to be flipped, which often works. This makes this exploit usable even under a black-box setting, i.e., where one does not have access to the model directly.
- They tried this exploit in reality on an NVIDIA A6000 GPU with 48GB GDDR6 DRAM, and it worked. They achieved an ASR of 69.2–91.2% across all models.
- There are different defense mechanisms, namely weight clipping, safe decoding, and intentional analysis. However, the algorithm can be adjusted in such a way that it diminishes their defensive effectiveness.
