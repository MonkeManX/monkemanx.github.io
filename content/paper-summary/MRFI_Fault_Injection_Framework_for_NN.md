---
title: 'MRFI: An Open Source Multi-Resolution Fault Injection Framework for Neural Network Processing'
date: 2026-05-11 10:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** MRFI: An Open Source Multi-Resolution Fault Injection Framework for Neural Network Processing

**Link to Paper:** https://arxiv.org/abs/2306.11758

**Date:** 12. Dec. 2023

**Paper Type:** Neural Network Reliability, Fault Simulation, Fault Injection

**Short Abstract:**
MRFI is a highly configurable, multi-resolution fault injection tool for deep neural networks, designed to address the limitations of existing fault injection solutions.

## 1. Introduction

Deep Neural Networks (DNNs) are increasingly deployed in safety-critical applications (e.g., autonomous driving, avionics) and large-scale systems (e.g., LLMs), where hardware faults—such as process variations, defects, noise, or bit flips—can cause erroneous inferences with potentially severe consequences. Therefore, thorough reliability evaluation through fault injection before deployment is essential.

Existing fault injection tools (e.g., PyTorchFI, Ares, TensorFI, etc.) provide basic error injection and reliability analysis, but suffer from several key limitations:
- Lack of calibration with realistic hardware architectures, making the correlation between neuron-level faults and actual hardware faults unclear.
- Inconsistent error models, metrics, and quantization setups, leading to incomparable or biased results across studies.
- Tight coupling with neural network frameworks (e.g., PyTorch), which complicates usage, limits flexibility for fine-grained or layer-specific injections, and hinders scalability to GPUs and parallel systems.
- Insufficient support for fine-grained, multi-level vulnerability analysis needed for selective fault-tolerant designs.

**MRFI** (Multi-Resolution Fault Injection) is a highly configurable, open-source fault injection framework designed to overcome these issues.

**Key Advantages:**
- Provides **unified** error models, quantization setups, and evaluation metrics for consistent and comparable reliability studies.
- Supports **multi-resolution vulnerability analysis** at different granularities and perspectives to better guide selective protection.
- Uses a flexible tree-structure configuration that does **not** require modifying the original neural network model or PyTorch’s computing engine → enables natural GPU parallelism and fast simulation.
- Fault injection is calibrated against architecture-specific simulators and validated for accuracy.

## 2. Methedology: MRFI Framework

### 2.1. MRFI Overview
MRFI consists of two main parts: **Configuration** and **Execution Modules**.

1. **Configuration Approaches**:
  - **EasyConfig**: Simple YAML-based config for quick experiments. Users specify layers and fault injection settings that apply uniformly.
  - **DetailConfigTree**: Advanced tree-structured configuration that mirrors the hierarchical structure of PyTorch models. Enables fine-grained, module/layer-specific control without modifying the original model.
2. **Execution Modules**: Provide common fault injection functions (with support for user customization).


### 2.2. Integration with PyTorch

MRFI is built on top of **PyTorch** and uses **PyTorch hooks** for error injection. This approach offers several advantages:
- Seamless integration without altering the original model or PyTorch’s core computing engine.
- Supports dynamic modification of intermediate tensors (weights and activations).
- Naturally compatible with CPU and GPU execution for high performance.
- Avoids the limitations of manually replacing or wrapping layers.

### 2.3. Major MRFI Execution Modules

MRFI has four key components:

1. **Quantizer** (Optional): Handles simulation of quantized (fixed-point/integer) inference. Converts floating-point tensors to integer and back, allowing realistic evaluation of quantized models.
2. **Selector**: Determines *where* errors are injected. Supports:
   - Random positions (for soft errors with given error rates)
   - Fixed positions (for permanent faults)
   - Custom masks or user-defined selectors for selective fault tolerance.
3. **Error Model**: Defines *how* errors are applied at selected positions. Includes:
   - Bit flips (random or fixed)
   - Additive noise (e.g., Gaussian)
   - Stuck-at faults, fixed-value faults, random values, etc.
   - Fully customizable.
4. **Observer**: Monitors internal neuron values and error effects without necessarily injecting faults. Useful for:
   - Analyzing activation distributions (e.g., dynamic range for quantization)
   - Golden-run comparisons
   - Measuring error propagation (count of affected neurons, RMSE, etc.)

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/MRFI_Fault_framework.png">
</figure>
{{< /rawhtml >}}

## 3. Results

It works, shrimple as!

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/shrimple_as_that.jpg">
</figure>
{{< /rawhtml >}}


---

### Stuff

- The problem and motivation that papers address
    - [Faults](2026-05-12_faults.md) in DNN
    - Not a single injection framework that can do all the different kinds of faults
- What fault model is used
    - permanent faults
    - transient faults
    - weight inejction
    - quantized
    - floating point faults
- Is it about detection, localization, or both?
    - Neither, it creates faults for testing
- What method and metrics are used?
    - Accuracy, MAE, RMSE
- What is one limitation or open question? (gap)
   - /
