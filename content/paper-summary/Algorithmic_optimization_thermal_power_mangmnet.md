---
title: 'Algorithmic Optimization of Thermal and Power Management for Heterogeneous Mobile Platforms'
date: 2026-05-24 08:00:00
tags: ["paper-summary", "battery"]
---

**Paper Title:** Algorithmic Optimization of Thermal and Power Management for Heterogeneous Mobile Platforms

**Link to Paper:** https://ieeexplore.ieee.org/document/8120141

**Date:** 27. Nov. 2017

**Paper Type:** Dynamic power management, heterogeneous computing, multicore architectures, multiprocessor systems-on-chip (MPSoCs). thermal management 

**Short Abstract:**  
Modern mobile devices use powerful multi-core chips that generate significant heat, making temperature control critical for performance and user comfort. This paper presents a dynamic thermal and power management algorithm that predicts device temperature and adjusts CPU usage to reduce overheating, cutting temperature violations dramatically while also lowering power consumption by about 7%.


## 1. Introduction

The paper addresses the growing thermal and power challenges in modern mobile multiprocessor systems-on-chips (MPSoCs). As smartphones and tablets become more powerful, manufacturers integrate more CPU cores, heterogeneous architectures, GPUs, and specialized accelerators. While this increases computational capability, it also significantly raises power consumption and device temperature. Excessive heat not only limits performance and battery life, but also negatively impacts long-term reliability because repeated temperature fluctuations stress hardware components.

To manage this problem, mobile systems already employ techniques such as dynamic voltage-frequency scaling (DVFS), idle power management, and heterogeneous big.LITTLE architectures. In big.LITTLE systems, high-performance “big” cores handle demanding tasks while energy-efficient “little” cores handle lighter workloads. However, experiments on Samsung Exynos chips show that intensive workloads can still drive temperatures beyond safe operating levels. Unlike desktop systems, mobile devices cannot rely on active cooling solutions such as fans, and reactive thermal throttling often causes major performance degradation and unstable temperature oscillations.

To solve this issue, the paper proposes a predictive dynamic thermal and power management (DTPM) framework for heterogeneous mobile platforms. The approach consists of two main parts. First, the authors develop a methodology for constructing accurate power and thermal models for heterogeneous MPSoCs using real hardware measurements. Second, they design a runtime DTPM algorithm that predicts future temperatures, computes safe power budgets, and proactively adjusts CPU/GPU configurations to avoid thermal violations while minimizing performance loss.

The main contributions are:

1. A methodology for generating accurate power and thermal models for heterogeneous MPSoCs.
2. A runtime algorithm that dynamically computes power budgets using thermal prediction.
3. A predictive DTPM algorithm based on performance gradients and thermal constraints.
4. Extensive validation on commercial Samsung Exynos big.LITTLE systems showing substantial reduction in temperature violations and lower power consumption with minimal performance loss.


## 2. Overview of the proposed Framework

The proposed DTPM framework integrates with existing mobile operating system infrastructure instead of replacing default governors and drivers. Existing CPU governors continue determining frequencies and active cores, while the proposed framework supervises these decisions using predictive power and thermal models.

The framework first predicts power consumption for the frequencies selected by the default governor. These predicted power values are then passed into the thermal model to estimate future temperatures. If no thermal violation is predicted, the framework allows the default configuration to proceed unchanged. Therefore, the system remains nonintrusive under normal operating conditions.

When a future thermal violation is predicted, the framework computes the maximum allowable power budget that keeps the system below the thermal limit. Multiple hardware configurations may satisfy this power budget, but different configurations have different impacts on performance. The framework therefore searches for the configuration that minimizes performance degradation.

The paper first discusses a previously proposed CPU cluster-oriented algorithm (CCA), which prioritizes the big CPU cluster because it has the greatest performance impact. However, this method is limited because it does not effectively handle GPU-intensive workloads.

To address this limitation, the paper introduces a new gradient search algorithm (GSA). Unlike CCA, GSA uses runtime information such as CPU and GPU utilization to determine which hardware resource can be throttled with the smallest performance penalty. This allows the algorithm to manage both CPU- and GPU-bound workloads more effectively.

## 3. Power/Thermal Modeling Methodology 

The effectiveness of predictive thermal management depends heavily on accurate runtime models of both power consumption and thermal behavior. The authors therefore develop empirical modeling techniques that rely on real hardware measurements.

### 3.1 Power Modeling

The total power consumption of each hardware resource is modeled as the sum of dynamic power and leakage power. Dynamic power depends primarily on switching activity, capacitance, voltage, and frequency, while leakage power strongly depends on temperature.

The paper derives analytical equations describing leakage current as an exponential function of temperature. Because many technology-specific parameters are unknown, the authors experimentally characterize these parameters using actual hardware measurements.

To measure leakage power, the target platform is placed inside a temperature-controlled furnace. The system is operated under light workloads so that dynamic power does not significantly influence temperature. By sweeping ambient temperature from 40°C to 80°C and recording power measurements, the authors fit the leakage model parameters using nonlinear curve fitting techniques.

At runtime, the Linux kernel periodically computes the activity factor and switching capacitance product (αC) using sensor readings. The process involves:

1. Reading current power and temperature sensors.
2. Estimating leakage power using the thermal model.
3. Subtracting leakage power from total power to obtain dynamic power.
4. Dividing dynamic power by (V^2f) to compute αC.

The resulting power models achieve less than 5% average prediction error across many workloads and platforms.

### 3.2 Thermal Modeling

Thermal dynamics are modeled using a linear state-space representation derived from the analogy between electrical and thermal systems. The model describes how temperatures evolve over time based on power consumption and thermal coupling between hardware components.

Instead of relying on unavailable floorplans or material parameters, the authors use system identification techniques. They experimentally excite hardware resources using pseudorandom frequency patterns while measuring temperatures and power consumption. These measurements allow them to estimate the thermal conductance and capacitance matrices directly.

The thermal model captures two important effects:

* temporal coupling, meaning past temperatures affect future temperatures,
* spatial coupling, meaning heat generated by one component affects neighboring components.

The resulting models accurately describe thermal behavior while remaining computationally lightweight enough for runtime execution.

### 3.3 Thermal Prediction and Validation

Using the state-space thermal model, the framework predicts future temperatures several control intervals ahead. Before changing a frequency, the system estimates the resulting power consumption and then predicts how temperatures will evolve.

The prediction mechanism assumes frequencies remain constant during the prediction horizon while accounting for temperature-dependent leakage power. The prediction model is implemented directly inside the Linux kernel.

Experimental validation shows very high accuracy. Temperature prediction error remains below approximately 3% for predictions up to one second ahead and below about 7% even for five-second prediction windows. Most of the prediction error arises from uncertainty in future workload behavior rather than inaccuracies in the thermal model itself.

## 4. Dynamic Thermal and Power Management 

This section introduces the predictive DTPM algorithms that proactively avoid thermal violations using the previously developed models.

### 4.1. Runtime Power Budget Computation

The framework begins by defining a maximum safe temperature constraint for all thermal hotspots. Using the thermal prediction equations, the system computes how much additional power each hotspot can safely tolerate before violating thermal limits.

This available margin is referred to as thermal headroom. The thermal headroom equations translate thermal constraints into corresponding power constraints for CPUs, GPUs, and other hardware resources.

Because many combinations of frequencies and active resources can satisfy the same power budget, the challenge becomes selecting the configuration that minimizes performance degradation.

### 4.2 Predictive DTPM Algorithm Using Gradient Search

#### 1) CPU Cluster-Oriented Algorithm (CCA)

The earlier CCA algorithm first checks whether the configuration chosen by the default governor would cause a thermal violation. If so, it reduces the frequency of the big CPU cluster because big cores contribute most strongly to thermal hotspots.

If lowering the big-core frequency is insufficient, the algorithm further reduces GPU frequency or migrates workloads to little cores. This approach works reasonably well for CPU-bound workloads but struggles with GPU-intensive applications.

#### 2) Problem Formulation

The authors formulate thermal management as a constrained optimization problem. The objective is to minimize application execution time while satisfying thermal constraints.

Performance is approximated as inversely proportional to operating frequencies weighted by resource utilization. The thermal constraints are rewritten as nonlinear inequalities involving frequencies, voltages, and leakage power.

Because voltage depends approximately linearly on frequency, power consumption becomes a cubic function of frequency. The final optimization problem is therefore a convex constrained optimization problem.

#### 3) Solution Approach

The authors analyze the gradient and Hessian of the objective function and show that the optimization problem is convex. This means performance degradation increases predictably as frequencies decrease.

An exhaustive search over all possible frequency combinations would be computationally too expensive for runtime execution inside the kernel. Instead, the authors exploit convexity to design a more efficient gradient-based search algorithm.

#### 4) Gradient Search Algorithm (GSA)

The GSA algorithm begins by predicting future temperatures. If no violation is predicted, the default governor decisions are accepted unchanged.

If a violation is predicted, the algorithm evaluates the performance impact of reducing each resource’s frequency by one level. It computes the projected performance loss associated with throttling each CPU cluster or GPU frequency.

The resource whose frequency reduction produces the smallest performance penalty is selected first. The algorithm iteratively lowers frequencies, recomputes power consumption and thermal predictions, and repeats until the thermal constraints are satisfied.

If all resources reach minimum frequency and thermal violations still persist, the algorithm places the hottest cores into sleep states and migrates their tasks elsewhere.

Because the algorithm relies on runtime utilization information, it can intelligently distinguish CPU-bound from GPU-bound workloads and throttle the least performance-critical component first.

## 5. Experiment 

### 5.1. Experimental Setup and Methodology

The framework is evaluated on the Odroid-XU3 platform using the Samsung Exynos 5422 MPSoC. This platform includes four big Cortex-A15 cores, four little Cortex-A7 cores, a GPU, temperature sensors, and built-in power measurement hardware.

The experiments use a wide collection of benchmarks, including:

* MiBench embedded workloads,
* PARSEC multithreaded benchmarks,
* graphics benchmarks such as 3DMark and GLBench.

The authors compare three configurations:

1. the default Linux thermal management without a fan,
2. the earlier CPU cluster-oriented algorithm (CCA),
3. the proposed gradient search algorithm (GSA).

All algorithms are integrated directly into the Linux kernel. The runtime overhead of the proposed framework is extremely small, below 0.39%.

### 5.2. Power Consumption and Temperature Prediction Accuracy

The experimental results show that the power model achieves less than 5% average prediction error across most workloads. Slightly larger errors occur during workloads with rapidly fluctuating activity patterns.

The thermal prediction model also demonstrates strong accuracy. Predicting temperatures one second ahead produces less than 3% average error and never exceeds approximately 5%.

These results confirm that the models are sufficiently accurate for proactive thermal management.

### 5.3. Temperature Control and Stability

The experiments demonstrate that the proposed GSA algorithm successfully regulates temperatures without requiring active cooling.

For GPU-intensive benchmarks such as 3DMark, the default configuration and CCA both experience substantial thermal violations because they do not effectively control GPU frequencies. In contrast, GSA dynamically throttles GPU frequency and maintains temperature within safe limits.

For CPU-intensive benchmarks, both CCA and GSA successfully prevent thermal violations. However, GSA provides more general and robust behavior because it handles both CPU and GPU hotspots simultaneously.

The authors also show that light workloads experience almost no interference because the framework only intervenes when thermal violations are predicted.

### 5.4. Performance, Power, and Energy Consumption Evaluation

The paper evaluates the tradeoff between thermal stability and performance. Performance is measured using execution time for CPU benchmarks and frame rate for GPU benchmarks.

The experiments show that GSA drastically reduces temperature violations while introducing only small performance losses. Most workloads experience less than 9% performance degradation, with average performance loss around 5%.

GPU benchmarks particularly highlight the advantage of GSA over CCA. GSA significantly lowers temperature violations while maintaining frame rates close to the default configuration.

The proposed approach also reduces overall power and energy consumption. Since mobile devices cannot realistically use fans, eliminating active cooling already saves considerable power. Additionally, throttling resources intelligently further decreases power usage.

On average, GSA achieves:

* approximately 7% power savings,
* approximately 4% energy savings,
* an order-of-magnitude reduction in temperature violations.
