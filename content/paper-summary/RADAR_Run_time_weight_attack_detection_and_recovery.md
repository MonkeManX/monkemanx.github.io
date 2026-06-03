---
title: 'RADAR: Run-time Adversarial Weight Attack Detection and Accuracy Recovery'
date: 2026-05-26 12:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** RADAR: Run-time Adversarial Weight Attack Detection and Accuracy Recovery

**Link to Paper:** https://arxiv.org/abs/2101.08254

**Date:** 20. Jan 2021 

**Paper Type:** Neural networks, weight attack, run-time detec-
tion, protection

**Short Abstract:**
Adversarial bit-flip attacks on neural network weights can severely degrade model accuracy, even with only a few flipped bits. The proposed RADAR method detects such attacks at runtime using lightweight checksum-based signatures and restores accuracy by zeroing compromised weight groups with minimal overhead.

## 1. Introduction 

Neural networks are vulnerable to adversarial weight bit-flip attacks like PBFA, which can drastically reduce accuracy with only a few bit changes, and existing defenses either fail to detect such attacks or are too costly. The paper introduces RADAR, a lightweight runtime defense that detects attacks using checksum-based 2-bit signatures on interleaved weight groups and restores accuracy by zeroing corrupted groups. It achieves high detection and recovery performance with very low memory and runtime overhead.

## 2. Background 

DNNs are vulnerable to runtime memory attacks like rowhammer and PBFA, which can deliberately flip bits in DRAM and severely degrade model accuracy. While defenses such as binarization, soft-error detection, and ECC exist, they are often either passive, limited to random faults, or can still be bypassed by sophisticated attacks.

## 3. Method

### 3.1 Threat Model 

The paper defines a threat model where an attacker combines PBFA (a gradient-guided bit-flip attack) with rowhammer-style DRAM fault injection to corrupt DNN weights at runtime under a white-box assumption. PBFA is shown to be extremely effective because it mostly targets MSBs and small-valued weights, and the analysis reveals that vulnerable bits are scattered across the model, enabling only a few flips to cause catastrophic accuracy drops.

### 3.2 RADAR SCHEME: DETECTION

The system is designed around the idea that DNN weights live in DRAM (which is vulnerable to rowhammer attacks) but are processed in fast on-chip cache during inference, so every time weights are loaded they could already be corrupted. Because of this, the authors want a detection method that runs during inference itself, with almost no slowdown and almost no extra secure memory usage.

Instead of heavy mechanisms like ECC or cryptographic hashes, they use a very simple idea: group weights together, add them up, and compress that sum into a tiny 2-bit “signature.” That signature acts like a fingerprint for each group of weights. At deployment time, they store the correct (“golden”) signatures in secure memory. During inference, they recompute the signature for the currently loaded weights and compare it to the stored one—if they differ, an attack is assumed.

To make this simple checksum harder to bypass, they add two protections. First is masking: before summing, some weights are randomly sign-flipped using a secret key. This makes the checksum depend on a secret pattern, so an attacker cannot easily predict how changes in weights affect the signature. Second is interleaving: instead of grouping nearby weights together, they mix weights that are far apart in memory into the same group. This is important because real bit-flip attacks often affect localized memory regions, so spreading weights out makes it harder for an attacker to manipulate a whole group without being detected.

Finally, the system runs this process continuously during inference: every time a batch of weights is fetched from DRAM into cache, it recomputes signatures and compares them to the secure reference. If a mismatch is found, it flags that group as corrupted and triggers mitigation (like zeroing weights in the full method).


### 3.3 RADAR SCHEME: RECOVERY

The recovery part of RADAR is intentionally very simple and is triggered once an attack is detected. Instead of trying to precisely fix corrupted weights or restore them from backup (which would be slow and costly), the system quickly assumes that any group flagged as compromised is unreliable and resets it entirely.

The key observation behind this design is how PBFA works: it tends to flip the most significant bit (MSB) of small-valued weights, turning them into very large positive or negative values. This causes a disproportionate change in the neural network’s activations (especially after ReLU), which is what leads to the dramatic accuracy collapse. So even if only a few bits are flipped, their effect spreads widely through the network.

To counter this, RADAR doesn’t try to correct individual bits. Instead, once a group is flagged by the checksum-based detector, it simply sets *all weights in that group to zero*. The intuition is that most weights in a DNN group are already small and centered near zero, so zeroing them out does less damage than leaving a few heavily corrupted values in place.

If interleaving was used during detection, the system first “de-interleaves” the weights to restore their original ordering, and then applies the zeroing so the model structure remains consistent.

This approach trades precision for speed: it avoids expensive repair or rollback mechanisms and instead uses a fast, blunt reset that still preserves most of the model’s functionality, allowing significant accuracy recovery even after strong PBFA attacks.


## 4. Experiments 

### 4.1 Detection results

The key result is that RADAR can detect almost all bit-flips:
* Without interleaving, detection is good for small groups but degrades when groups get large, because multiple flipped bits can cancel each other out inside one group.
* With interleaving, detection stays high even for large groups because the flipped bits get spread across different groups.
* For ResNet-18, RADAR detects about **9.5 out of 10 bit-flips on average**, which is very high.

They also measure very rare failure cases and show that the probability of missing an attack can be as low as **10⁻⁵ to 10⁻⁶**, meaning it is extremely unlikely to miss PBFA in practice.


### 4.2 Recovery results

Recovery is based on a very simple rule:
**if a group is flagged as corrupted, set all weights in that group to zero.**

Even though this is very coarse, it works well because:
* PBFA typically corrupts only a few critical bits (especially MSBs),
* and those corrupted values dominate the network’s behavior.

Results:
* Without attack, ResNet-20 has ~90% accuracy and ResNet-18 ~70%.
* After PBFA (10 bit-flips), accuracy drops to:
  * **18% (ResNet-20)**
  * **0.18% (ResNet-18)** (almost random guessing)
* After RADAR recovery:
  * ResNet-20 recovers to **~61–81%**
  * ResNet-18 recovers to **~57–66%**

Interleaving consistently improves recovery because it improves detection quality, so fewer clean weights are wrongly zeroed.


### 4.3 Trade-offs (group size vs storage vs accuracy)

A major design choice is the group size (G):
* Small (G): better accuracy recovery but more signatures → more storage overhead
* Large (G): less storage but weaker detection granularity

They find optimal points:
* ResNet-20: best around **G = 8**
* ResNet-18: best around **G = 512**

Storage overhead is very small overall:
* ~8.2 KB (ResNet-20)
* ~5.6 KB (ResNet-18)


### 4.4 Runtime overhead

RADAR is very efficient:
* ~5% overhead for smaller model (ResNet-20)
* ~1%–2% overhead for ResNet-18
* Even less in batched inference settings

### 4.5 Comparison with other methods

Compared to ECC or CRC:
* Those methods are more expensive in storage and computation.
* RADAR achieves similar or better detection with:
  * much lower storage
  * much lower runtime cost

For example, CRC may need **~28–36 KB**, while RADAR needs only **~5–8 KB**.


### 4.6 Strong attacker case

Even if the attacker knows RADAR exists:
* They might try flipping more bits or avoiding MSBs.
* Interleaving still spreads corruption, maintaining detection.
* If they avoid MSBs, they need many more flips (harder attack).

They also suggest extending the signature to 3 bits if attackers shift to lower bits, trading slightly more storage for stronger defense.
