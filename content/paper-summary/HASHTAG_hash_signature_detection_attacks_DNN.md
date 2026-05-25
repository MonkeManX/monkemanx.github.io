---
title: 'HASHTAG: Hash Signatures for Online Detection of Fault-Injection Attacks on Deep Neural Networks'
date: 2026-05-15 08:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:**  HASHTAG: Hash Signatures for Online Detection of Fault-Injection Attacks on Deep Neural Networks

**Link to Paper:** https://arxiv.org/abs/2111.01932

**Date:** 2. Nov. 2021 

**Paper Type:** Hashing, DNN, Fault Injection, Fault Detection, Attacks 

**Short Abstract:**
HASHTAG is a lightweight framework that detects fault-injection (bit-flip) attacks on deep neural networks by creating a precomputed hash-based signature of the most vulnerable network layers and checking it at runtime during inference. It identifies sensitive layers via sensitivity analysis and verifies model integrity in real time with low overhead, achieving strong detection of memory tampering attacks.


## 1. Introduction 

DNNs used in safety-critical systems are highly vulnerable to fault-injection attacks, where flipping just a few bits in model weights (e.g., via DRAM attacks) can severely degrade accuracy. Existing defenses either add constraints that reduce model performance or rely on ML-based detectors that lack strong guarantees and can still produce errors.

HASHTAG proposes a real-time detection method that builds a compact hash-based “signature” of the most vulnerable layers in a DNN before deployment, then checks these signatures during inference to detect tampering. It uses sensitivity analysis to focus only on the layers most likely to be attacked and applies a low-overhead Pearson hash to enable fast integrity checks with provable detection guarantees, 0% false positives, and minimal runtime/storage cost.

## 2. Background 

### 2.1 Bit-Flip Attacks 

Bit-flip attacks exploit hardware-level memory faults (like Rowhammer) to flip bits in DRAM storing DNN weights, causing severe degradation in model accuracy. Early attacks showed that even flipping a single parameter can change predictions, and more advanced methods achieve over 90% accuracy loss by carefully targeting vulnerable bits.

Modern attacks use gradient-based strategies to identify which bits in quantized DNN weights are most sensitive, iteratively flipping those that maximize the model’s loss until performance collapses or specific misclassification goals are reached. These methods are general and apply across different attack variants, including both untargeted accuracy degradation and targeted misclassification.


### 2.2 Existing Defense 

Prior work on defending DNNs against fault-injection attacks focuses mainly on training-time robustness, inference-time constraints, or external detectors. Some approaches improve robustness by adding training constraints like clustering or binarization, or by reconstructing weights during inference, but these methods do not actually detect attacks and often reduce model accuracy while still failing to fully prevent bit-flip damage.

Other methods use ML-based detectors (e.g., checker networks or classifiers on sensitive weights), but their performance is limited by model accuracy, they add extra overhead, and they can themselves be attacked. Checksum-based methods detect bit errors over groups of weights, but their effectiveness depends heavily on grouping size and can miss certain patterns of bit flips, leading to weaker guarantees and higher false negatives.

In contrast, HASHTAG avoids these limitations by using lightweight hash-based signatures with sensitivity-guided layer selection, enabling higher detection accuracy, lower overhead, and stronger probabilistic guarantees without affecting the original DNN’s inference performance.

## 2. Method: HASHTAG 

### 2.1 Overview 

HASHTAG works by first building a compact “signature” of a clean (untampered) DNN using hash values computed from selected, highly vulnerable layers. This selection is guided by a sensitivity analysis that identifies which layers are most likely to be targeted by bit-flip attacks, allowing the system to focus only on the most informative checkpoints instead of the entire network.

During deployment, the system runs normally but simultaneously recomputes hashes from these checkpoint layers and compares them to the stored ground-truth signatures. If any mismatch occurs, it signals that the model parameters have been altered (e.g., by a fault-injection attack) and triggers an alert so the system can reload safe weights.

The method assumes a strong attacker who knows the model, the detection mechanism, and even which layers are monitored, but not the secret hash ordering or stored signatures. Despite this, HASHTAG remains efficient (low memory and runtime overhead) and practical for embedded systems while still enabling real-time detection of parameter tampering.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/hashtag_overview.png">
</figure>
{{< /rawhtml >}}

### 2.2 Hash-based signature Extraction 

HASHTAG uses a lightweight 8-bit Pearson hash to compress each selected DNN layer into a fixed-size “signature” that represents its clean state. During deployment, it recomputes these hashes from layer weights (using a secret ordering) and compares them to stored values to detect any bit-flip-induced changes. The method is efficient for embedded systems, works well with quantized weights, and adds security through a secret input ordering while maintaining low overhead and strong detection capability.

### 2.3 Per-layer Sensitivity Analysis 

HASHTAG uses a Taylor-expansion–based sensitivity analysis to identify which DNN weights and layers are most vulnerable to bit-flip attacks. It estimates how much flipping a parameter (especially sign changes) increases the loss, approximating this effect using gradients so it can be computed efficiently via a single backward pass.

Each weight’s sensitivity is proportional to \((p_n \cdot \partial L / \partial p_n)^2\), and layer sensitivity is derived from the most sensitive weights within that layer. The top-k most sensitive layers are then selected as checkpoints for hash-based attack detection.

## 3. Experiments 


HASHTAG is evaluated on CIFAR10 and ImageNet across several DNNs (e.g., VGG11, ResNet, AlexNet, MobileNetV2) under strong bit-flip attacks, and it consistently shows very strong performance. The sensitivity analysis correctly identifies the most attack-prone layers, and using only a few checkpoint layers (often 1–3) is enough to achieve near or perfect detection.

Key results: HASHTAG reaches **100% detection rate** with **0% false positives** on most models, and remains robust even for complex networks like MobileNetV2 (≥96% with few checkpoints, 100% with slightly more). It is largely insensitive to bitwidth when using more than two checkpoints, making it broadly applicable.

Compared to prior work (WED and RADAR), HASHTAG achieves **higher or equal detection (up to 100%)**, **zero false positives**, and dramatically lower overhead: about **20–400× less storage** and up to **~175× faster runtime**. Overall, it provides accurate real-time attack detection with minimal memory and computation cost, making it suitable for embedded systems.
