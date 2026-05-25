---
title: 'A Systematic Literature Review on Hardware Reliability Assessment Methods for Deep Neural Networks'
date: 2026-05-12 10:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** A Systematic Literature Review on Hardware Reliability Assessment Methods for Deep Neural Networks

**Link to Paper:** https://arxiv.org/abs/2305.05750

**Date:** 9. May 2023

**Paper Type:** Neural Network Reliability, Fault Simulation, Fault Injection, Literature Review

**Short Abstract:**
This paper reviews methods for assessing the reliability of Deep Neural Networks (DNNs), especially in safety-critical applications where hardware errors can have serious consequences. It presents a systematic literature review categorizing reliability assessment approaches into Fault Injection (FI), Analytical, and Hybrid methods. The study explains the strengths, weaknesses, platforms, and evaluation metrics of these methods, highlighting that while FI is the most common approach, Analytical and Hybrid methods are more lightweight and still accurate, making them promising directions for future DNN reliability research.

## 1. Introduction

This paper examines the reliability of Deep Neural Networks (DNNs), particularly in safety-critical applications such as autonomous vehicles, where hardware faults can lead to catastrophic failures like incorrect traffic light detection. As DNNs become larger and are deployed on specialized hardware accelerators (GPUs, ASICs, FPGAs, and multi-core processors), ensuring their reliability becomes increasingly important. The paper highlights that different hardware platforms face different fault types, and even small hardware-induced errors can significantly reduce DNN accuracy.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/hardware_induced_faults_dnn.png">
</figure>
{{< /rawhtml >}}


To address this issue, many researchers have proposed methods for assessing and improving DNN reliability. However, because DNNs are used across many applications and platforms, existing methods are fragmented and difficult to generalize. Previous survey papers mainly focused on reliability enhancement or fault injection techniques, but none provided a complete review of reliability assessment methods themselves.

This work presents the first comprehensive Systematic Literature Review (SLR) dedicated to DNN reliability assessment methods. Reviewing studies published between 2017 and 2022.

## 2. Preliminaries

- There are various deep learning architectures that can be used in hardware.
    - Importantly: quantized Neural Networks (QNNs) and Binarized Neural Networks (BNNs) are often used.
- DNNs can be implemented in software or in hardware.
    - Software: PyTorch, TensorFlow
    - Hardware: FPGAs, ASICs, GPUs, TPUs
- Main fault sources affecting DNN reliability:
    - Soft errors: Temporary radiation-induced faults.
    - Aging effects: Long-term transistor degradation causing timing errors.
    - Process variations: Manufacturing inconsistencies affecting chip behavior.
- Fault categories:
    - Permanent faults: Persistent faults caused by defects, aging, or process variations.
    - Transient faults: Short-lived faults caused by radiation, voltage, or temperature changes.
- Fault outcomes:
    - Faults may be masked/corrected or propagate to outputs.
    - Output-visible faults are classified as:
        - SDC (Silent Data Corruption): Fault affects output without detection.
        - DUE (Detected Unrecoverable Error): Fault is detected but cannot be recovered.
- Three major reliability assessment methods:
    - Fault Injection (FI): Injects simulated faults into hardware/software to study effects.
    - Analytical methods: Use mathematical models to estimate reliability.
    - Hybrid methods: Combine FI with analytical modeling.
- Characteristics of methods:
    - FI is the most realistic but computationally expensive and time-consuming.
    - Analytical and hybrid methods are faster and lighter-weight.
- Common FI fault models:
    - Transient logic faults: Exist for one clock cycle.
    - Memory bit flips: Persist until execution ends.
    - Stuck-at faults:
        - sa-0: Bit permanently fixed at 0.
        - sa-1: Bit permanently fixed at 1.
- Reliability metrics used:
    - FIT (Failures In Time): Failures per 10^9 hours.
    - AVF (Architectural Vulnerability Factor): Probability of fault propagation.
    - SDC rate: Fraction of corrupted outputs.
    - SER (Soft Error Rate): Frequency of soft errors.
    - Cross-section: Ratio of observed errors to particle strikes.
- FI experiments require statistical sampling because exhaustive testing across all bits and clock cycles is computationally infeasible

## 4. Study Overview

### 4.1 Taxonomy

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/li_review_overview.png">
</figure>
{{< /rawhtml >}}


Fault Injection (FI) methods evaluate DNN reliability by introducing faults and observing their effects. They are divided into three approaches:
- **fault simulation**, where DNNs are modeled in software or HDL and faults are injected into the model (including hardware-independent, hardware-aware, and RTL-based implementations);
- **hardware emulation**, where DNNs run on real hardware such as FPGAs, GPUs, or processors while faults are injected via software or frameworks; and
- **irradiation**, where hardware executing DNNs is exposed to radiation to induce real physical faults. FI is the most widely used approach in reliability assessment and is characterized by platform, fault type, and evaluation metrics.

**Analytical methods** estimate reliability without injecting faults by analyzing the internal structure of DNNs, such as neurons and layer connections, to model how faults affect outputs and identify critical components, offering lower computational cost.

**Hybrid methods** combine analytical modeling with fault injection to reduce the complexity of extensive FI experiments while maintaining higher realism than purely analytical approaches, enabling more efficient and scalable reliability evaluation.

### 4.2 Research Trends

The paper analyzes 139 studies on DNN reliability (2017–2022) to show research trends. It finds that the topic started in 2017 and has steadily grown, becoming an active research area. Most studies rely on **Fault Injection (FI)** methods for reliability assessment, while only about 10% use **analytical methods** (11 papers) or **hybrid analytical/FI methods** (3 papers).

Among FI-based studies, most use **software simulation**, especially hardware-independent approaches, while in hardware emulation, **GPU-based platforms** are the most common. Overall, the statistics show a strong dominance of FI methods and limited use of analytical and hybrid approaches, highlighting potential areas for future research.

## 5. Characterization

## 5.1 Fault Injection Method

### 5.1.1 Fault Simulation

#### 5.1.1.1 Hardware-Independent Platform

General:
* DNNs are implemented in software frameworks such as **PyTorch, TensorFlow, Keras, Caffe, and DarkNet**.
* Fault injection is performed directly at the software level, making it flexible for studying different fault models.
* Both **transient faults** and **permanent faults** are considered, but most studies focus on transient faults (e.g., soft errors, SEU, MBU).

**Fault modeling:**
* **Permanent faults:**
    * Easy to model in software.
    * Persist throughout execution by forcing values (0 or 1) in weights or activations.
* **Transient faults:**
    * Modeled as random bit flips in memory (usually weights or activations).
    * Faults remain until overwritten.
    * Also injected into activations to study effects on both memory and logic.


**Injection strategy:**
* Faults are typically injected into **random weights or activations**.
* Most works use a **Bit Error Rate (BER)** to determine how many bits are corrupted.
* Experiments are repeated multiple times to achieve statistical confidence (e.g., 95% confidence, 1% error margin).

**Evaluation methods:**
* **Accuracy loss:** Difference between clean and faulty model performance.
* **Fault classification based on outputs:**
    * **Masked:** No difference from golden model.
    * **Observed-safe:** Output changes but confidence drop < 5%.
    * **Observed-unsafe:** Output changes with confidence drop > 5%.
* **SDC-based classification:**
    * Silent Data Corruption (SDC), software exceptions, or corrupted execution outcomes.
* **Semantic segmentation-specific categories:**
    * Masked, No Impact SDC, Tolerable SDC, Critical SDC.

**SDC rate-based evaluation:**
* Some works only measure the fraction of faults that change outputs (SDC rate), as these are considered most critical.

**Software FI tools:**
* Common frameworks: **PyTorchFI**, **TensorFI / TensorFI+**, **Ares**
* Capabilities:
    * Inject transient and permanent faults into weights and activations.
    * Control fault rates and measure accuracy loss and SDC rate.
* Extensions and improvements:
    * **BinFI:** Identifies critical bits in networks.
    * **LLTFI:** Faster fault injection at instruction level.
    * Checkpoint-based injectors: framework-independent SDC analysis.

**Overall insight:**
* Hardware-independent FI is the most widely used and flexible approach.
* It relies heavily on software-level modeling, random fault injection, and statistical evaluation of DNN robustness.



#### 5.1.1.2 **Hardware-Aware Platform:**

General:
* DNNs are implemented in software frameworks (e.g., Keras, PyTorch, TensorFlow) while also incorporating an **abstract model of the hardware accelerator** (e.g., systolic arrays, FPGA-like or RTL-inspired architectures).
* Combines **software-level fault injection** with awareness of hardware behavior.
* Supports more realistic reliability evaluation than purely hardware-independent approaches.

**Fault injection approach:**
* Both **transient faults** and **permanent faults** are studied.
* Faults are injected into:
    * **Memory elements** (weights, feature maps)
    * **Datapath/MAC units** (computation logic)
    * **PE outputs and accelerator components**
* Hardware models include systolic arrays, MAC units, FPGA-inspired designs, and accelerator simulations.
* Fault rates are often based on **BER**, with repeated experiments for statistical confidence (e.g., 95% confidence, 1% error margin).

**Permanent fault studies:**
* Target MAC units, on-chip memory, feature maps, and processing elements.
* Methods include:
    * Weight remapping strategies to mitigate faults
    * Fault-aware training to improve inference robustness

**Evaluation methods:**
* Most works use **accuracy loss** after fault injection.
* Some use **SDC rate** (fraction of misclassifications).
* Some compute **FIT at accelerator level**, combining:
    * Manufacturer FIT values
    * Component size
    * Observed SDC from FI experiments

**Advanced SDC classification (example study):**
* **SDC-1:** Top-1 misclassification.
* **SDC-5:** True label not in top-5 predictions.
* **SDC-10%:** >10% confidence drop in top prediction.
* **SDC-20%:** >20% confidence drop.



#### 5.1.1.3 **RTL Model Platform:**

General:
* Uses **Register-Transfer Level (RTL) models** of hardware accelerators for simulation-based reliability analysis.
* Includes three main categories:
    * **2D systolic array accelerators** (e.g., TPU-like, Eyeriss-inspired designs)
    * **RTL implementations of DNNs**
    * **MPSoC-based systems** (multi-core processor platforms for DNN execution)

**Fault injection at RTL level:**
* Performed directly in hardware design simulation.
* Common faults:
    * **Permanent faults** in processing elements (PEs), MAC units, and arrays
    * **Transient faults** in buffers, registers, and control logic
    * **SEU faults** in LUTs (look-up tables)
* MPSoC frameworks simulate faults in pipeline-based or multi-core execution setups.

**Evaluation methods:**
* Mainly **accuracy loss** after fault injection.
    * Some works use **fault classification schemes**, including:
* **Masked, SDC, crash, hang**
* Extended classifications include:
    * Tolerable misclassification
    * No-impact misclassification
    * Critical misclassification
    * Tolerable correct classification
    * Beneficial correct classification

**Overall insight:**
* Hardware-aware and RTL-based approaches are more realistic than software-only FI.
* They better capture real accelerator behavior but are more complex and expensive to simulate.

### 5.1.2 Fault Emulation

#### 5.1.2.1 **FPGA platform for DNN reliability:**

General
* DNNs are deployed fully or partially on FPGAs for inference, often using **Zynq SoC architectures** (ARM + FPGA).
* Fault injection is performed while the network runs on hardware, combining **software-controlled FI with real FPGA execution**.
* Some studies implement only specific layers on FPGA for targeted analysis.

**Three main FI setups:**
* **Host-computer controlled FI:** faults generated on a PC and sent to FPGA; mainly SEUs in configuration bits; results analyzed on host.
* **Embedded-processor FI:** faults generated by on-board ARM processor; injected into configuration memory or on-chip memory (transient and permanent faults).
* **On-hardware FI modules:** fault injector directly integrated into FPGA design (e.g., modifying PE outputs or registers).

**Fault modeling:**
* Focus on **SEUs in configuration bits**, weights, activations, and on-chip memory.
* Includes both **transient faults (radiation-like effects)** and **permanent faults (stuck-at or memory corruption)**.
* Configuration memory FI is iterative: inject → run → reset → inject next fault.

**Frameworks and tools:**
* **FireNN, Fiji-FIN, FINN-based extensions** are commonly used platforms.
* They enable structured injection into FPGA bitstreams and memory while comparing against a golden model.

**Evaluation methods:**
* Most works use **accuracy loss** across tasks (classification, detection, generation).
* Some also use **task-specific metrics**:
    * Top-1 / Top-5 accuracy (classification)
    * mAP (object detection)
    * SSIM (image generation)
* Fault severity often grouped by impact:
    * ≤1% loss (low impact)
    * 1–5% loss (medium impact)
    * ≥5% loss (high impact)
* Some classify faults as:
    * **Tolerable**, **Critical**, or **system-breaking (exceptions/crashes)**.
* Layer-wise vulnerability analysis categorizes parameters as low/medium/high risk.

**Advanced reliability metrics:**
* **AVF (Architectural Vulnerability Factor):** probability of fault propagation, computed via FI.
* **Cross-section:** derived from AVF and configuration bit usage.
* **SER (Soft Error Rate):** estimated from radiation data and used for fault modeling.
* **System reliability models:** exponential reliability functions based on layer failure rates.

**Overall insight:**
* FPGA-based FI provides **high realism and hardware accuracy**, but is more complex than software-based methods.
* It enables fine-grained analysis of real accelerator behavior, configuration memory sensitivity, and hardware-induced fault effects.


#### 5.1.2.2 **GPU Platform (FI in DNNs):**

General:
* Fault injection is performed on GPUs running DNN inference.
* Most studies focus on **transient faults**, while some also consider **permanent faults**.
* Fault injection is typically done using frameworks or custom GPU-level tools.

**FI frameworks used:**
* Common tools: **SASSIFI (NVIDIA), NVBitFI, FlexGripPlus, CAROL-FI, CLASSES**
* Some works implement custom FI using **CUDA or TensorRT**.
* SASSIFI is the most widely used and injects faults into **ISA-visible states** (registers, memory, predicates, condition registers).
* Fault rate and experiment count are adjusted for statistical confidence (error margin + confidence level).

**Fault modeling:**
* Focus on **bit-flip (SEU) transient faults** in GPU execution states.
* Also includes memory, register, and instruction-level faults.
* Some frameworks allow architecture-level injection across layers of abstraction.

**Evaluation methods:**
* Almost all works classify outcomes into:
    * **Masked:** no effect on output
    * **SDC (Silent Data Corruption):** output differs from golden model
    * **DUE (Detected Unrecoverable Error):** crash, hang, or reboot
* DUE is sometimes referred to as **crash**.

**Refined SDC classifications:**
* Based on impact on output quality:
    * **Non-critical:** minor confidence change, no misclassification or ranking change
    * **Light-critical:** ranking changes without misclassification
    * **Critical:** misclassification occurs
* For object detection tasks:
    * Classified using **precision and recall thresholds** (e.g., safety-critical vs non-critical scenarios)
* Some methods also use **bounding box overlap differences** to define SDC severity.

**Vulnerability analysis metrics:**
* Used to measure how likely faults propagate to outputs at different abstraction levels:
* **KVF (Kernel Vulnerability Factor)**
    * **LVF (Layer Vulnerability Factor)**
    * **IVF (Instruction Vulnerability Factor)**
    * **PVF (Program Vulnerability Factor)**
    * **Operation VF**
    * **AVF (Architecture Vulnerability Factor)**
* These metrics help identify which parts of GPU or DNN are most sensitive to faults.

**Overall insight:**
* GPU-based FI is one of the most mature and widely studied platforms.
* It provides detailed, multi-level analysis (instruction → kernel → architecture).
* Strong focus on **fault classification and vulnerability quantification**, especially for safety-critical applications like autonomous driving.


#### 5.1.2.3  **Processors Platform (DNNs on CPUs/edge devices):**

General:
* Focuses on DNN execution on **multi-core processors**, mainly for **IoT and edge applications**.
* Most studies analyze **soft errors**, especially in **ARM processor register files**.
* Instruction-level vulnerability is also studied in some works.

**Fault injection frameworks:**
* **ARM-FI**: used to inject and simulate faults in ARM-based processors.
* **SOFIA**: widely used framework for emulating soft errors in processor components.
* These tools allow fault injection into different processor parts (registers, instructions, memory, etc.).

**Evaluation methods:**
* Most works use **fault classification**, similar to other platforms:
    * **Masked**
    * **Tolerable SDC**
    * **Critical SDC**
    * **DUE (Detected Unrecoverable Error)**
* For object detection tasks, faults are further categorized as:
    * **Incorrect probability:** correct detection but changed confidence scores
    * **Wrong detection:** misclassification or missing objects
    * **No prediction:** no output produced

**Reliability metrics:**
* **MWTF (Mean Work To Failure):**
    * Measures how much computation is completed before failure occurs
    * Combines execution time and probability of critical faults
    * Higher MWTF → more reliable system
* **AVF (Architectural Vulnerability Factor):**
    * Used to measure vulnerability of register files and processor components
* **PVF (Program Vulnerability Factor):**
    * Captures vulnerability at instruction and program level

**Overall insight:**
* Processor-based DNN reliability studies mainly target **edge/embedded systems**.
* Focus is on **register-level soft errors and instruction vulnerability**.
* Reliability is evaluated using both **classification-based fault impact** and **quantitative metrics (MWTF, AVF, PVF)**.

### 5.1.3 Irradiation

See paper for details.

## 5.2 Analytical Methods


Analytical methods for DNN reliability assessment model reliability mathematically instead of directly injecting faults during evaluation. They analyze the structure and behavior of DNNs, particularly neurons, layers, and weights, to estimate how faults would affect outputs and to determine the vulnerability of different components. The main idea is to link the importance or influence of a component on the output with its susceptibility to faults, thereby identifying critical neurons and layers. Although these methods may still use fault injection for validation, they do not rely on it for modeling.

Four main approaches are used: **Layerwise Relevance Propagation (LRP)-based analysis**, which assigns contribution scores to neurons and ranks them by vulnerability; **gradient-based analysis**, which uses gradients of outputs with respect to weights or activations to measure sensitivity and identify critical components; **estimation-based analysis**, which uses statistical measures such as activation ranges or norms to quickly approximate vulnerability with lower accuracy but higher efficiency; and **machine learning-based analysis**, which applies methods like Open-Set Recognition to detect abnormal outputs and identify critical faults via thresholds on output logits.

Across all approaches, vulnerability of neurons, feature maps, and weights is the key concept for assessing reliability. These methods are generally lightweight, accelerator-agnostic, and faster than fault injection, though estimation-based methods trade accuracy for speed, while LRP and gradient-based methods provide more accurate results closer to fault injection outcomes.


### 5.3 Hybrid Methods

See paper for details.

## 6. Discussion

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 100%;" src="/attachments/lit_review_reliability_overview_final_table.png">
</figure>
{{< /rawhtml >}}


**Key open challenges identified in DNN reliability assessment:**
* **Training phase reliability is largely unexplored:**
While some work studies faulty training data, there is no systematic study of how faults in parameters or hardware affect reliability during training itself.
* **Limited diversity of DNN models and tasks:**
Most studies focus on **CNNs for image classification and object detection**, while other architectures like **RNNs and LSTMs** and broader applications remain underexplored.
* **Lack of software FI frameworks in hardware-aware platforms:**
There is a gap in flexible simulation tools for hardware-aware reliability assessment; better **DNN accelerator simulators** are needed.
* **FPGA fault injection limitations:**
Existing FPGA studies could benefit from **generalized HLS-based FI frameworks** to reduce design complexity and development time.
* **Neglected control logic reliability:**
Very few studies analyze the **control units of DNN hardware accelerators (FPGAs/ASICs)**, even though they can significantly affect system reliability.
* **Underdeveloped analytical methods:**
Current analytical approaches are limited in scope:
    * Mostly focus on **critical neuron identification**
    * Very few estimate overall reliability or use formal metrics
    * Only limited use of **ML-based analytical techniques**
  → There is strong potential for expanding ML-driven analytical models.
* **Limited generalization of analytical methods:**
Most analytical approaches are restricted to **CNNs and vision tasks**, lacking adaptation to other architectures and domains.
* **Potential of hybrid methods:**
Hybrid FI + analytical approaches are promising but still underdeveloped and could become a major direction for future research.
* **Lack of standardized DNN reliability metrics:**
Current works rely on general metrics (accuracy loss, fault classification, FIT), but there is a need for **DNN-specific reliability metrics**.


**Main future research directions:**
* Develop **new analytical and hybrid methods**, especially those incorporating **machine learning**, to create faster, scalable, and DNN-specific reliability assessment techniques.
* Design **new tools and frameworks** tailored to DNN reliability, beyond traditional reliability engineering tools.
* Introduce **novel DNN-specific reliability metrics** for more meaningful evaluation.
* Expand reliability research to **new DNN architectures (RNNs, LSTMs)** and **emerging IoT/edge applications**, not only safety-critical systems.
