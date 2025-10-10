---
title: 'Surrogate Gradient Learning in Spiking Neural Networks'
date: 2025-10-10 11:00:00
tags: ["paper-summary", "Neuromorphic"]
---

**Paper Title:** Surrogate Gradient Learning in Spiking Neural Networks

**Link to Paper:** https://arxiv.org/abs/1901.09948

**Date:** 3 May 2019

**Paper Type:** Neuromorphic, Architecture, RNN, SNN, Training

**Short Abstract:**
This paper provides an overview of the problems encountered when training Spiking Neural Networks (SNNs) and the different approaches proposed to solve them.

## 1. Introduction

Our brains are highly efficient; therefore, taking inspiration from them is a natural approach.
Recurrent Neural Networks (RNNs) have become very powerful for solving noisy time-series prediction problems.
These RNNs share similarities with our brain. Based on these similarities, spiking leaky integrate-and-fire (LIF) networks have been developed, which are widely used today.

RNNs are difficult to train due to noise and the challenge of capturing long-range temporal and spatial dependencies. This problem is even worse in SNNs because the depth of the network is of utmost importance when solving complex tasks, making the training process crucial.

## 2. Understanding SNNs as RNNs

When the author uses the term *RNN*, they mean it in the broadest sense—referring not only to networks with explicit connections from past to future neurons, but also to those with temporal dynamics within a single neuron, i.e., a neuron can “remember” information.

A LIF neuron can be described as:

$$
U[n+1] = \beta U[n] + I[n] - S[n]
$$

The state of neuron *i* is determined by the synaptic current (*I*), which represents the input, and the membrane voltage (*U*), which represents the state.
Since the neuron “remembers” previous states through *U[n]*, it can be considered a type of RNN.

## 3. Training RNNs

To train a powerful RNN, we need several key components:
* A cost or loss function, e.g., mean squared error
* A mechanism to update weights, e.g., gradient descent

Gradient descent, in particular, is able to solve the **credit assignment problem**, which can be separated into:
* **Spatial credit assignment:** In order to train a neural network, we must determine which parts of the network (i.e., which weights) deserve credit or blame for the final prediction. This is commonly solved using backpropagation, which guarantees learning but comes with high communication costs.
* **Temporal credit assignment:** When we train a network with temporal components, such as an RNN, we also face the temporal credit assignment problem, where the task is to determine which weight is *when* blameworthy or praiseworthy for the final prediction. This is commonly solved using gradient backpropagation through time (BPTT).

BPTT has a space complexity of (O(NT)), where (N) is the number of neurons per layer and (T) is the number of time steps.

## 4. Credit Assignment with SNNs

There are two main challenges when applying RNN training methods to SNNs:

1. The **non-differentiability** of the SNN, more precisely of the Heaviside activation function
2. **BPTT** is very expensive in terms of computation and memory, making it poorly suited for neuromorphic processors

To overcome these challenges, several approaches have been proposed:

1. Using entirely biologically inspired local learning rules
2. Translating conventional neural networks to SNNs
3. Smoothing the network to make it differentiable
4. Defining surrogate gradients as relaxations of real gradients

This paper focuses primarily on methods (3) and (4).

## 5. Smoothed SNNs

We can further categorize smoothing approaches into:

* **Gradients in soft nonlinearity models:** Can be applied to all SNN models. In this method, the spiking nonlinearity is replaced by a continuous-valued gating function. The resulting network can then be optimized using standard gradient-based methods.
* **Gradients in probabilistic models:** Binary probabilistic models smooth out discontinuous nonlinearities.
* **Gradients in rate-coding networks:** Here, a rate-based coding scheme is assumed. The idea is to use the spike rate as the underlying signal and construct an *f-I* curve, which can then be used for gradient optimization. These methods offer good performance but can be inefficient.
* **Gradients in single-spike timing-coding networks:** In this approach, neuron outputs are based on firing times, meaning individual spikes carry significantly more information than in rate-based schemes. This method was popularized by *SpikeProp*.
  **Disadvantage:** Each hidden unit must emit exactly one spike per trial.

## 6. Surrogate Gradients

* **Surrogate gradients:** In the backward pass, the Heaviside operation is replaced by a differentiable approximation function. This method still relies on BPTT.
* **Surrogate gradients with local update rules:** Since relying on BPTT does not solve the problem of computational cost, local update rules can be used in conjunction with surrogate gradients to improve efficiency.

## 7. Applications

Some applications of smoothed or surrogate gradient methods for SNNs include:

* **Feedback alignment and random error BP:**
  Feedback alignment or random error backpropagation are relaxations of standard backpropagation. They approximate the gradient to sidestep the nonlocality problem by replacing weights in the backprop rule with random weight matrices. Random BP results in remarkably little loss in classification performance on benchmarks but tends to underperform in deeper networks.
* **Supervised learning with local three-factor learning rules:**
  Popularized by *SuperSpike*. It uses synaptic eligibility traces to solve the temporal credit assignment problem. However, it does not scale well for very large multilayer networks.
* **Learning using local errors:**
  Here, a layer-wise loss is defined and used only to update the associated layer. This simplification reduces space complexity to (O(N)).
* **Learning using gradients of spike time:**
  The difficulties in training SNNs stem from the discrete nature of spikes. One way to remedy this is to use spike timing instead, capitalizing on the continuous nature of time in SNNs. Spike time is continuous and can therefore be differentiated easily.
