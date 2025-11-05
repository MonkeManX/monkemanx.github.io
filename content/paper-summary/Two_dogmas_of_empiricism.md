---
title: 'Two Dogmas Of Empiricism'
date: 2025-11-05 10:00:00
tags: ["paper-summary", "philosophy"]
---

**Paper Title:** Two Dogmas Of Empiricism

**Link to Paper:** https://en.wikipedia.org/wiki/Two_Dogmas_of_Empiricism

**Date:** 1951

**Paper Type:** Philosophy, Epistemology, Ontology

**Short Abstract:**
In this paper, Willard Van Orman Quine attacks the analytic–synthetic distinction and reductionism. The former refers to statements that are true by definition and require no prior knowledge, while the latter requires information from the world. Reductionism, on the other hand, claims that every statement can be reduced to some logical construction. Quine critiques and ultimately rejects both views.


## 1. Background for Analyticity

### 1.1 History of Analyticity

The term *analyticity*, although not explicitly named as such, was already used by earlier philosophers:
* **Hume:** “Relations of Ideas” (analytic) vs. “Matters of Fact” (synthetic)
* **Leibniz:** “Truths of Reason” (analytic) vs. “Truths of Fact” (synthetic)
* **Kant:** “Predicate is contained in the subject” (analytic) vs. “Adds new information” (synthetic)

However, all of these definitions of *analytic* are somewhat unclear and lack rigor in explaining exactly what “analytic” means.


### 1.2 Meaning vs. Naming

Frege introduced the distinction between **meaning** and **naming** of words, arguing that they are not the same. For example:
* “The morning star” and “the evening star” both refer to the same object — Venus — but have different meanings.
* Similarly, “9” and “the number of planets” refer to the same number but differ in meaning.

This distinction between meaning and naming applies to atomic words, but it can be extended to more general terms through the notions of **extension** and **intension**:
* **Extension:** the things the term applies to.
* **Intension:** what the term means.

For example, “creature with a heart” and “creature with kidneys” have the same extension (since all creatures with hearts also have kidneys) but different intensions — thus, different meanings.


### 1.3 Essence vs. Meaning

Even in antiquity, we find a similar distinction. For Aristotle, things had an **essence** — qualities that were essential to what the thing *is*.

In the modern world, a shift occurred: instead of investigating the *essence* of things, we investigate the **meaning** of words.

> “Meaning is what essence becomes when it is divorced from the object of reference and wedded to the word.”

But just as it was unclear what exactly *essence* meant, the same problem remains for *meaning*.


### 1.4 Analyticity and Meaning

Recall that we want to understand what “analytic” means. One approach is to investigate it through the **meaning of words**.

There are two classes of analytic truth:

1. **Logical Truth:** Statements that remain true no matter how you interpret the non-logical terms.
   > Example: “No unmarried man is married.”
2. **Analytic by Synonymy:** Statements that are true by meaning, not just by logic.
   > Example: “No bachelor is married.”
   > This sentence becomes true if we replace *bachelor* with *unmarried man*.1;129B27;129u
However, this second kind depends on **synonymy** — so, to know what *analytic* means, we must first understand what *synonymy* means.


### 1.5 Carnap’s Attempt: Analyticity and State Descriptions

Carnap proposed the notion of a **state-description**, which is a list of atomic statements that are either true or false.

For example:

* A = “John is a bachelor.”
* B = “John is married.”

There are four possible state-descriptions:

1. A = true, B = true
2. A = true, B = false
3. A = false, B = true
4. A = false, B = false

Carnap then defines:

> **Definition 1**
>
> A statement is *analytic* if it is true in all possible state-descriptions.

An example of this would be:

> “No unmarried man is married.”

No matter how you assign truth values to the parts (“unmarried,” “man,” “married”), the logical structure ensures it is always true.

However, this definition of analyticity only works for the first class of analytic truths, not for those *analytic by synonymy*.

For example:

> “No bachelor is married.”

If “bachelor” and “unmarried man” are treated as different atomic words, then one possible state-description could be:
* “John is a bachelor” = true
* “John is unmarried” = false

If that’s allowed, then “No bachelor is married” could turn out false in some state-descriptions.
So, by Carnap’s definition, it would not count as analytic anymore.


## 2. Definition

### 2.1 Analytic Truths Reduced to Definition

One idea for defining analyticity is as follows:

> **Definition 2**
>
> A statement is *analytic* if it becomes a logical truth once we expand the definitions of its terms.

**Example:**
“No bachelor is married” → define *bachelor* = *unmarried man* → “No unmarried man is married,” which is logically true.


### 2.2 Where Do Definitions Come From?

One problem with this definition of analyticity is the question:
**Where do definitions themselves come from in the first place?**

We can distinguish between several kinds of definition:

**a) Reporting existing synonymy (lexicographic definitions)**
* These are standard dictionary definitions.
* Example: “Bachelor = unmarried man” simply reports how people actually use the word.
* Such definitions don’t explain *why* a statement is analytic — they merely record usage.

**b) Explication (Carnap’s philosophical definition)**
* Philosophers or scientists refine meanings to make them more precise or useful.
* Example: defining a new, more exact version of a term for scientific purposes.
* However, as Quine points out, even explication depends on existing synonymies in certain *favored contexts*.
* It preserves existing meaning in some cases while sharpening it in others.
* Thus, synonymy must already exist to some extent — definitions don’t generate it from scratch.

**c) Purely conventional abbreviation**
* You invent a new symbol or term explicitly to stand for another.
* Example: Let “♣” mean “unmarried man” in this paper.
* Here, synonymy is created by stipulation.
* This is the only case where a definition truly generates synonymy — but it is trivial and purely formal, not the rich linguistic meaning we deal with in ordinary language.

### 2.3 Why Defining Analyticity Through Definition Fails

As we can see, the idea that all analytic statements reduce to logical truths via definition fails — except in the trivial case of purely conventional abbreviations. In all other cases, definitions rely on **pre-existing synonymy**.

And since the purely conventional case is uninteresting, this approach cannot explain the meaningful notion of analyticity.

In other words, you cannot explain analytic truths purely by definition, because:
* Most definitions are based on existing language use.
* Explication still depends on pre-existing meaning in context.
* Only trivial or formal definitions truly *create* synonymy — but those don’t capture what analytic truths are about.


## 3. Interchangeability

### 3.1 Interchangeability *Salva Veritate*

Another idea is to define analyticity (and synonymy) through **substitution**.

Two expressions are *salva veritate* synonyms (“preserving truth”) if you can substitute one for the other everywhere without changing the truth value of any statement.

Using this, we might define analyticity as follows:

> **Definition 3**
>
> A statement is *analytic* if it becomes a logical truth once all expressions are replaced by their *salva veritate* equivalents.


### 3.2 Problems with Substitution *Salva Veritate*

The first problem concerns **fragmentation of words**.
For example, substituting “bachelor of arts” with “unmarried man of arts” doesn’t make sense.
We could solve this by saying that we treat compound expressions like “bachelor of arts” as single, indivisible units and only allow substitution of whole terms.

However, the deeper problem is that substitution *salva veritate* is **not sufficient** for synonymy.

We can distinguish between two types of synonymy:

* **Cognitive synonymy:** the kind of synonymy relevant to meaning and analyticity.
  * Example: “Bachelor” = “unmarried man” makes the statement “All and only bachelors are unmarried men” analytic.
* **Extensional agreement:** two predicates happen to be true of the same things.
  * Example: “Creature with a heart” and “creature with kidneys” refer to the same set of creatures, but they do *not* mean the same thing.

Substitution *salva veritate* only preserves **extensional agreement**, not **cognitive synonymy**.
It tells us that two expressions refer to the same objects (extensionally), but not that they *mean* the same thing.
Yet meaning is precisely what we are trying to understand when discussing analyticity.

**Example:**

Let’s define two predicates:
* F(x) = “x has a heart”
* G(x) = “x has kidneys”

Both are true of the same objects (e.g., all humans), so they are *extensionally equivalent*.

By substitution *salva veritate*, we could replace one with the other everywhere:

> “All creatures with a heart have hearts.”

This is analytically true by its meaning.
Now, replace F with G:

> “All creatures with kidneys have hearts.”

This is not analytically true, it depends on biology.

Hence, **interchangeability *salva veritate*** is not a good criterion for analyticity, because it fails to capture the crucial link between meaning and truth.

## 4. Semantical Rules

### 4.1 The Core Problem of Defining Analyticity

So far, every attempt to define *analyticity* has failed, because to define “analytic” we must already presuppose it in some form, making any definition circular.

In other words, whenever we say:

> “S is analytic in L if and only if it is listed in the semantical rules of L,”

whatever these “semantical rules” are will again depend on understanding what *analytic* means.


### 4.2 Why Semantic Rules Depend on Understanding Analyticity

Suppose we try to write rules for a formal language that define which statements are analytic. We would already need to know what *analytic* means to do so.

For example, imagine I say, “This set contains all the *special numbers*,” but I never explain what *special* means. All I can do is list some numbers, but to understand *why* those numbers are special, I must already know what “special” means.

It is the same with analyticity.

Imagine we create an artificial language with the following semantic rules:

1. P(a) → P(a) is analytic
2. Q(b) → Q(b) is analytic
3. R(c) ∨ ¬R(c) is analytic

You now know *which* statements in L are analytic according to this list, but you still don’t know *why* they are analytic. The definition tells us only *which* statements count as analytic, not *what makes them so*.


## 5. The Verification Theory and Reductionism

Another approach to defining analyticity is through **verificationism**.

Verificationism claims: *the meaning of a statement is the method of its empirical verification.*

In other words, we might define:

> **Definition 4**
>
> A statement is *analytic* if it is verified no matter what.


### 5.1 Radical Reductivism

The most naïve form of this idea is **radical reductivism**, which holds that every meaningful statement can, in principle, be translated into statements about direct sense experience.

But in practice, this never works. We always need some abstract concepts, theoretical terms, or logical structure that cannot be reduced to raw experience.


### 5.2 Weak Reductionism

A weaker version of reductionism proposes that:

> Each individual statement is associated with a distinct range of confirming and disconfirming experiences.

However, this too fails. It is not *individual* statements that are verified or falsified by experience, but rather **the entire network of beliefs**; including science, language, and logic together.

This leads to **holism**: we can test or revise our beliefs only as part of the *whole system*, not in isolation.


## 6. Empiricism Without the Dogmas

We have now seen that all attempts to define analyticity fail to do so properly.

Quine suggests that we cannot meaningfully distinguish between *analytic* and *synthetic* statements. Instead, **all our knowledge forms a “web of belief”**, a single interconnected system, ranging from everyday facts to physics and mathematics.

Experience affects only the *outer edges* of this web, and the impact of empirical evidence diminishes toward the inner parts.

When experience conflicts with part of our knowledge, we adjust elements of the web to restore coherence. No statement is absolutely immune to revision, not even the laws of logic.

For example, in quantum mechanics, some have proposed revising classical logic (such as the law of excluded middle) to make sense of quantum phenomena.

Statements closer to the periphery of the web i.e. those connected to direct experience, are revised more easily and more frequently.
Deeper beliefs, such as the laws of physics, mathematics, or ontology, are more resistant to change, but still *in principle* revisable.

To organize our experience and simplify predictions, we introduce **posits**: entities like physical objects, forces, numbers, and classes.
* Physical objects are simpler and more useful posits than, for example, Homeric gods.
* Atoms or mathematical entities are posits that make our theories more coherent and efficient.

These posits are **pragmatic fictions**, not proven truths, but useful tools for navigating experience.


## Criticism

My main criticism is that Quine draws a strong conclusion, that the analytic–synthetic distinction is illusory, from the failure of existing definitions.

However, one could argue that this does not prove the distinction itself meaningless; it may simply mean that we have **not yet found the right definition** of *analytic*.

In other words, Quine’s conclusion rests on less stable grounds than he suggests: the failure of past definitions does not necessarily entail that the distinction is incoherent in principle.
