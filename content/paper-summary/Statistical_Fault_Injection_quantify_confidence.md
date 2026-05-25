---
title: 'Statistical fault injection: Quantified error and confidence'
date: 2026-05-13 10:00:00
tags: ["paper-summary", "Project-ATPG"]
---

**Paper Title:** Statistical fault injection: Quantified error and confidence

**Link to Paper:** https://ieeexplore.ieee.org/document/5090716/  

**Date:** 20. April 2009

**Paper Type:** dependability analysis, statistical fault injection

**Short Abstract:**
The paper addresses a key limitation of statistical fault injection: while only a random subset of possible faults is usually tested in complex circuits, previous work rarely quantified the reliability of the results. It introduces a statistical framework to calculate confidence intervals, margins of error, and the number of fault injections required to achieve a desired level of accuracy and confidence.

## Summary

### Core Problem

Modern integrated circuits are vulnerable to **soft errors** caused by:
* radiation (alpha particles, neutrons),
* electromagnetic interference,
* or deliberate fault attacks (e.g., lasers targeting cryptographic chips).

Testing every possible fault in a complex circuit is computationally infeasible because the number of possible:
* fault locations,
* timings,
* and bit combinations

grows explosively.

As a result, researchers commonly use **Statistical Fault Injection**, where only a random subset of faults is injected.

The authors argue that previous work often claimed:

> “a large number of faults were injected”

without rigorously quantifying:

* how accurate the reported results are,
* or how confident we should be in them.

The paper’s main goal is to provide a **formal statistical framework** for quantifying:
1. **margin of error**, and
2. **confidence level**

in SFI experiments.


### Method

The paper adapts classical statistical sampling theory (similar to polling/surveys) to fault injection campaigns.

The framework allows researchers to determine:
* how many faults must be injected to achieve a desired accuracy,
* or, conversely,
* what confidence/error bounds result from a given sample size.


### Statistical Model

The authors model all possible faults as a finite population of size (N).

A random sample of size (n) is selected uniformly.

The method assumes:
* normal distribution behavior,
* unbiased random sampling,
* finite population sampling without replacement.

The sample size formula is:

n=\frac{N t^2 p(1-p)}{e^2(N-1)+t^2 p(1-p)}

Where:
* (N): total number of possible faults,
* (p): estimated proportion of faults with a given property,
* (e): desired margin of error,
* (t): critical value corresponding to the confidence level.

The paper recommends using:

p=0.5

because it produces the most conservative (largest) required sample size.


### Key Insights

#### 1. Very Small Samples Can Be Sufficient

One of the most important findings is that only a tiny fraction of all possible faults may be needed to obtain statistically reliable results.

Example:

* Total fault population:
  [
  N = 4{,}063{,}170
  ]
* For:
  * 95% confidence
  * 5% margin of error

only:
[
n = 385
]

fault injections are required.

That is only:
[
0.009%
]

of the total fault space.

This is a major practical result because exhaustive fault injection is usually impossible.


### 2. Margin of Error Matters More Than Confidence

The paper shows:
* Increasing confidence (e.g., 95% → 99%) only moderately increases required sample size.
* Reducing margin of error (e.g., 5% → 1%) dramatically increases required experiments.

For example:

| Margin of Error | Confidence | Required Samples |
| --------------- | ---------- | ---------------- |
| 5%              | 95%        | 385              |
| 5%              | 99%        | 663              |
| 1%              | 95%        | 9581             |
| 0.1%            | 95%        | 776,792          |

So precision is much more expensive than confidence.


## Conclusion

The paper demonstrates that **Statistical Fault Injection can be made scientifically rigorous** by applying classical sampling theory.

Its central message is:

> Dependability evaluation does not require exhaustive fault injection if sampling error and confidence are quantified correctly.

This significantly reduces experimental cost while preserving measurable reliability in the results.
