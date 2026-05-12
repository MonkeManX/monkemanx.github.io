---
title: 'Resilience Assessment of Large Language Models under Transient Hardware Faults'
date: 2026-05-08 08:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Resilience Assessment of Large Language Models under Transient Hardware Faults

**Link to Paper:** https://ieeexplore.ieee.org/document/10301253

**Date:** 31. Jan 2023

**Paper Type:** LLM, Testing, Errors

**Short Abstract:**
The paper investigates how resilient Large Language Models (LLMs) are to transient hardware faults (also called soft errors), such as random bit flips caused by cosmic rays, power fluctuations, or electromagnetic interference.
This matters because LLMs are increasingly used in safety-critical systems.
A transient fault may silently corrupt outputs without crashing the system, called a **Silent Data Corruption (SDC).**

## 1. Introduction

The paper studies how reliable Large Language Models (LLMs) are when transient hardware faults (soft errors like bit flips caused by cosmic rays or power issues) occur during execution. Since LLMs are increasingly used in safety-critical systems such as autonomous vehicles, translation, and code generation, reliability is important.

The authors use a fault injection tool called LLTFI to simulate hardware faults in five LLMs: BioBERT, CodeBERT, T5, RoBERTa, and GPT-2. They analyze how often these faults cause silent data corruption (SDC), where the model produces incorrect outputs without crashing.

Their experiments show that LLMs are generally quite resilient, with an average SDC rate of only 0.9%. However, some faults can still significantly alter outputs semantically, especially in tasks like translation. They also find that fault sensitivity depends on factors such as model size, layer, and fine-tuning objective.


## 2. Background

### Fault Mode

The paper focuses on transient hardware faults in CPUs, specifically single-bit flips caused by events like particle strikes on processor components. The authors use the single-bit flip model because prior research shows it accurately represents errors that lead to silent data corruption (SDCs).

They exclude faults in memory (such as caches, weights, and biases) because these are usually protected by error-correcting codes (ECC). They also ignore faults that affect processor control logic or program control flow, since those typically cause crashes rather than subtle incorrect outputs.

The study mainly examines faults during LLM inference rather than training, because inference happens continuously in deployed systems.


## 3. Methodology

The authors modified the LLTFI fault injection tool to handle the large scale of LLMs, which can contain hundreds of millions of parameters and execute billions of CPU instructions.

They made two main improvements:

- A lightweight, optimized fault injection (FI) runtime statically linked to the LLM executable, reducing runtime overhead by about 25%.
- A scalable fault propagation tracing method using hash-based comparisons of layer outputs instead of expensive element-by-element tensor comparisons.

Their workflow involves downloading LLMs and tokenizers from Hugging Face , converting models into ONNX and then LLVM IR format, and running LLTFI fault injection campaigns. Inputs are converted into TensorProto format, faults are injected during inference, and the resulting outputs are converted back into human-readable text and compared with the correct outputs to detect silent data corruptions.

## 4. Experiments

### 4.1 Setup


The study evaluates the resilience of several popular LLMs under hardware faults using benchmarks with different architectures and tasks: PubMedBERT for medical question answering, CodeBERT for code completion, T5 for translation, RoBERTa for sentiment analysis, and GPT-2 for text generation. They also tested multiple BERT variants trained with different pre-training objectives.

The authors ran over 210,000 fault injection experiments by randomly inserting single bit-flip faults into floating-point CPU instructions during inference. Faults were injected into randomly selected layers, instructions, and bit positions while avoiding crashes by preserving program control flow.

To measure resilience, they used:

* **SDC rate**: how often faults caused incorrect outputs.
* **Cosine similarity**: how semantically different corrupted outputs were from correct outputs.

They note that these metrics have limitations because natural language can express similar meanings with different wording, while high cosine similarity can still hide important semantic differences. Therefore, they also performed qualitative analysis of corrupted outputs based on syntactic and semantic changes.

## 4.2 Results

The experiments showed that LLMs are generally resilient to transient hardware faults, with **low silent data corruption (SDC) rates ranging from 0.2% to 1.9%, averaging about 0.9%(This means roughly 9 incorrect outputs per 1000 faults i.e. they simulated 1000 cosmic rays i.e. bit flips and only in 9 cases out of the 1000 did the output change)**. However, the severity and type of corruption varied widely depending on the model, input, and task.

The authors categorized corrupted outputs into:
* **Syntactically incorrect** (nonsensical or malformed output),
* **Semantically incorrect** (grammatically valid but wrong meaning),
* **Semantically correct** (different wording but same meaning).

Examples included:
* PubMedBERT predicting the wrong protein or disease name,
* T5 producing translations with subtle meaning changes, mixed languages, or paraphrases,
* RoBERTa flipping sentiment labels,
* CodeBERT generating syntactically invalid or logically incorrect Java code,
* GPT-2 generating incoherent or meaningfully altered text.

They found that:
* SDC rates vary significantly even within the same model depending on the input.
* Models with similar architectures can have very different resilience, suggesting that training data and objectives matter.
* Unlike CNNs, all transformer layers in LLMs were similarly sensitive to faults.
* Bit flips in higher-order floating-point exponent bits caused most SDCs, while lower-order bit faults were often naturally suppressed.
* Larger models tended to have higher SDC rates for fill-mask tasks.
* Fine-tuning objectives strongly affected resilience; question-answering tasks were generally more vulnerable than fill-mask tasks.
* Pre-training objectives had little consistent effect, except for models trained on random objectives, which showed uniform behavior regardless of size.

The paper concludes that while LLMs are surprisingly fault-tolerant overall, transient hardware faults can still cause subtle and dangerous semantic errors, especially in safety-critical applications like translation, medicine, or code generation.


----

## Thoughts

- The problem and motivation that papers address
    - LLMs becoming more popular, how do faults effect them?
- What fault model is used
    - Transient, bit flips
- Is it about detection, localization, or both?
    - Neither, analying the result of faults
- What method and metrics are used?
    - SDC rate, fraction of inejcted fault that result in missprediction
    - Cosine similarity, how distant the corrupted fault is
- What is one limitation or open question? (gap)
   - permanent faults
   - more metrics
   - are there certain reigon that lead to worse or better misspreidction
   - the stduy doesnt tell mcuch, is not that insightfull
