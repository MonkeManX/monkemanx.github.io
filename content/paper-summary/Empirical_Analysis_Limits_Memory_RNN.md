---
title: 'Empirical Analysis of Limits for Memory Distance in Recurrent Neural Networks'
date: 2025-10-15 08:00:00
tags: ["paper-summary", "Deep Learning"]
---

**Paper Title:** Empirical Analysis of Limits for Memory Distance in Recurrent Neural Networks

**Link to Paper:** https://arxiv.org/abs/2212.11085

**Date:** 20. Dec 2022

**Paper Type:** RNN, Memory Limit, LSTM

**Short Abstract:**
In this paper, the authors investigate the memory limits of Recurrent Neural Networks (RNNs) and compare them with other architectures such as Long Short-Term Memory networks (LSTMs) and Gated Recurrent Units (GRUs).


### 1. Introduction

Neural networks have established themselves as a popular tool in machine learning.

A special type of architecture used for time-series data is the *Recurrent Neural Network (RNN)*. RNNs process a stream of data piece by piece, allowing information to be carried over between time steps.

Another important architecture is the *Long Short-Term Memory network (LSTM)*, which was introduced to address the vanishing gradient problem found in RNNs. The *Gated Recurrent Unit (GRU)* is a more recent variant that retains similar capabilities while using fewer parameters than the LSTM.

The main idea behind all RNN-based architectures is to carry over relevant information during the processing of sequential data. For example, when predicting the weather hour by hour, it makes sense to retain information about the past few days’ conditions.

In this paper, the authors analyze the memory limitations of these architectures—specifically, how far back in time they can effectively “remember” information. To test this, they use a memorization task based on random input sequences.


### 2. Background

* **Recurrent Neural Networks (RNNs)**
  * Process input data along with a hidden state
  * Typically use the tanh activation function
* **Long Short-Term Memory Networks (LSTMs)**
  * Address the vanishing gradient problem
  * Contain a forget gate and a memory cell
  * Require a high number of trainable parameters
* **Gated Recurrent Units (GRUs)**
  * A newer LSTM variant with fewer parameters
  * Do not use a separate memory cell
* **Echo State Networks (ESNs)**
  * Differ from RNNs by having sparsely connected neurons
  * Reservoir weights are fixed
  * Trained using pure backpropagation rather than BPTT

The amount of information that can be stored is measured using *memory capacity (MC)*, defined as the correlation between input and output, summed over all time delays:

$$
MC = \sum^{\infty} MC_k = \sum^{\infty} \frac{cov^2(x(t - k), y_k(t))}{Var(x(t))Var(y_k(t))}
$$

This measures how much input variance can be recovered by an optimally trained output neuron.


### 3. Method

To determine how far information from past states can be carried over, the authors implemented an experiment using sequences of random lengths containing random numbers as input data to the RNN.

Because the sequences are of random lengths, the RNN cannot know in advance which parts of the input stream will be relevant until the final step. This setup forces the network to retain as much information as possible throughout the sequence.

The experiment was conducted using RNN, LSTM, and GRU architectures, each tested with varying numbers of layers and neurons.


### 4. Experimental Results

* **RNN Results**
  * Positions 1 ≤ p ≤ 4 are learned quickly.
  * Positions 6 ≤ p ≤ 8 stagnate, with loss not dropping below approximately 0.15.
  * Overall, the network loses accuracy and cannot reliably reproduce values at later positions.
* **LSTM Results**
  * LSTMs take longer to train for simpler positions (1 ≤ p ≤ 5).
  * Some learning progress is observed even after 500 epochs, particularly at position p = 6.
* **GRU Results**
  * GRU behavior appears most similar to that of LSTMs.


### 5. Conclusion

The results indicate that Jaeger’s upper bound on the short-term memory of Echo State Networks (ESNs) remains valid for deep RNN architectures trained using backpropagation (RNN, LSTM, GRU).

For stacked, multi-layer architectures, the theoretical maximum memory capacity could not be reached. Instead, an upper bound of
$$MC \le N - (l - 1) \text{ with } N = c \times l$$
was observed.
