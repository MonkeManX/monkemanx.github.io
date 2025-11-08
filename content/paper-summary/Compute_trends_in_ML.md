---
title: 'Compute Trends Across Three Eras of Machine Learning'
date: 2025-10-30 06:00:00
tags: ["paper-summary"]
---

**Paper Title:** Compute Trends Across Three Eras of Machine Learning

**Link to Paper:** https://arxiv.org/abs/2202.05924

**Date:** 11. Feb. 2022

**Paper Type:** Deep-Learning, Machine Learning

**Short Abstract:**
This paper gives an overview of the increase in computing time during the training of machine learning models.

## 1. Introduction

The paper contributes the following:

* A dataset of 123 milestone machine learning models and the compute it took to train them.
* Separation of the trends in compute across three eras: Pre-Deep Learning, Deep Learning, and Large-Scale.

## 2. Trends

In short, in the pre-Deep Learning era there was slow growth of compute time, followed by rapid growth in the Deep Learning era, and then the Large-Scale era with an increased compute-time growth of two orders of magnitude.

{{< rawhtml >}}

<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/training_flops_over_time_ml.png">
</figure>
{{< /rawhtml >}}

{{< rawhtml >}}

<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/training_flops_over_time_ml_summary.png">
</figure>
{{< /rawhtml >}}

## 3. Conclusion

In particular, the authors identify an 18-month doubling time between 1952 and 2010, a 6-month doubling time between 2010 and 2022, and a new trend of large-scale models between late 2015 and 2022, which started 2 to 3 orders of magnitude above the previous trend and displays a 10-month doubling time.

To summarize: in the Pre-Deep Learning Era, compute grew slowly. Around 2010, the trend accelerated as we transitioned into the Deep Learning Era. In late 2015, companies began releasing large-scale models that surpassed the trend (e.g., AlphaGo), marking the beginning of the Large-Scale Era.
