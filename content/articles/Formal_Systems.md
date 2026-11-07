---
title: 'Formal Systems'
date: 2026-11-06 15:00:00
tags: ["Computer Science", "Logic"]
markup:
  tableOfContents:
    endLevel: 2
    ordered: false
    startLevel: 1
Description: "This article provides an overview of the content of the lecture Formal Systems, covering the propositional logic block: syntax and semantics, Craig interpolation, binary decision diagrams, and SAT solving. Each section ends with a list of problems and solutions that readers can work through. This article serves more as a reference rather than a complete tutorial."
draft: True
---

{{< warning "Info" >}}
The terms I use in this article may not be the standard mathematical terms, as I originally learned about this topic by listening to and reading lectures in German. As such, the terms were translated into English.
{{< /warning >}}

{{< toc >}}

## 1. Introduction

### 1.1 What Makes Up a Logic

A logic consists of three components:

1. **Syntax**: the alphabet of the logic, and the rules that say which strings of symbols are well-formed statements.
2. **Semantics**: the meaning behind the logic, called models, and which of them make a statement true.
3. **Calculi**: rule systems or algorithms to check the "truth content" of a statement, answering questions such as satisfiability or general validity.

In plain words: syntax says how statements are written down, semantics says what they mean, and calculi say how to work with them mechanically. The three parts are developed together throughout the lecture, and this article follows the same order for the propositional block.

### 1.2 The Blocks of the Course

The lecture is organized in four blocks. Each block introduces one logic and treats it in the same order: first syntax, then semantics, then calculi.

1. **Propositional logic**: logic over atomic truth statements. It treats syntax and semantics, the Hilbert calculus as a theoretical calculus for proofs, and SAT solvers as a practical decision procedure.
2. **Predicate logic**: a logic that "speaks about objects". Example: "At night all cats are gray.", "Miez is a cat.", "Miez is red.", "It is not night." (the old Greeks could already do this). It treats syntax and semantics, calculi, equality, and predicate logic over theories such as the natural numbers.
3. **Formal specification**: the application of predicate logic to prove properties of programs. Specifications are written in the Java Modeling Language (JML) and checked with the verification tool KeY.
4. **Modal and temporal logic**: logics that know several states. Example: "After the window has been opened, the heating is switched off." It treats syntax and semantics of modal logic, temporal logic, and the question whether an "automaton" fulfills a temporal specification (model checking).

## 2. Propositional Logic: Syntax and Semantics

### 2.1 Vocabulary

Before any statement can be written, the language needs an alphabet. The first definition fixes the symbols of this alphabet, the second fixes how the statement letters are gathered into a signature.

> **Definition** Logical symbols  
> 
> The vocabulary of propositional logic consists of:
>
> 1. the symbol \(1\) for the truth value *true*,
> 2. the symbol \(0\) for the truth value *false*,
> 3. \(\neg\), the negation symbol ("not"),
> 4. \(\wedge\), the conjunction symbol ("and"),
> 5. \(\vee\), the disjunction symbol ("or"),
> 6. \(\rightarrow\), the implication symbol ("if ... then"),
> 7. \(\leftrightarrow\), the symbol for bilateral implication ("if and only if"),
> 8. \((,)\), the two parentheses.

{{< addspace height="40px" >}}

> **Definition** Signature  
> 
> A (propositional) signature is a countable set \(\Sigma\) of symbols, for instance
>
> $$
\Sigma = \{P_0, \ldots, P_n\} \quad \text{or} \quad \Sigma = \{P_0, P_1, \ldots\}.
$$
>
> The elements of \(\Sigma\) are also called *atomic statements*, *atoms*, or *propositional variables*.

### 2.2 Formulas

The symbols of the alphabet alone do not yet make statements. The following definition says which strings of symbols count as statements, and it does so by building them up step by step from atoms and constants.

> **Definition** Formulas  
> 
> For a signature \(\Sigma\), the set \(\text{For}^0_\Sigma\) of *formulas over \(\Sigma\)* is defined inductively:
>
> - \(1 \in \text{For}^0_\Sigma\) and \(0 \in \text{For}^0_\Sigma\),
> - \(\Sigma \subseteq \text{For}^0_\Sigma\),
> - if \(A, B \in \text{For}^0_\Sigma\), then also \(\neg A\), \((A \wedge B)\), \((A \vee B)\), \((A \rightarrow B)\), \((A \leftrightarrow B)\) are elements of \(\text{For}^0_\Sigma\).

Nothing else is a formula. So a formula is either a constant, an atom, or built up from smaller formulas by one of the five operators.

### 2.3 Semantics

The syntax says how formulas are written, the semantics says what they mean. Two definitions do this: an interpretation assigns a truth value to every atom, and the valuation computes from it the truth value of every formula.

> **Definition** Interpretation  
> 
> Let \(\Sigma\) be a propositional signature. An *interpretation* over \(\Sigma\) is an arbitrary mapping
>
> $$
I : \Sigma \rightarrow \{W, F\},
$$
>
> where \(W\) stands for true and \(F\) for false.

> **Definition** Valuation  
> 
> To every interpretation \(I\) over \(\Sigma\) belongs a *valuation* of the formulas over \(\Sigma\),
>
> $$
\text{val}_I : \text{For}^0_\Sigma \rightarrow \{W, F\},
$$
>
> defined by
>
> $$
\text{val}_I(1) = W, \qquad \text{val}_I(0) = F, \qquad \text{val}_I(P) = I(P) \text{ for every } P \in \Sigma,
$$
>
> and
>
> $$
\text{val}_I(\neg A) =
\begin{cases}
F & \text{if } \text{val}_I(A) = W \\
W & \text{if } \text{val}_I(A) = F
\end{cases}
$$

The remaining connectives are given by the usual truth table:

{{< table "data-table" "" >}}  
| \(\text{val}_I(A)\) | \(\text{val}_I(B)\) | \(\text{val}_I(A \wedge B)\) | \(\text{val}_I(A \vee B)\) | \(\text{val}_I(A \rightarrow B)\) | \(\text{val}_I(A \leftrightarrow B)\) |
|---|---|---|---|---|---|
| W | W | W | W | W | W |
| W | F | F | W | F | F |
| F | W | F | W | W | F |
| F | F | F | F | W | W |
{{< /table >}}

Note that \(\text{val}_I\) is a recursive definition: the value of a compound formula is computed from the values of its immediate subformulas. That this way of defining a function on formulas is legitimate is justified by the recursion principle of inductive definitions below.

### 2.4 Inductive Structures

Formulas are an example of a general pattern worth writing down once.

> **Definition** Inductively generated sets  
> 
> Let \(H\) be a set. Given a set of base cases \(B \subseteq H\) and a set of constructors
>
> $$
K = \{k_1 : H^{n_1} \rightarrow H, \ldots, k_r : H^{n_r} \rightarrow H\},
$$
>
> \(H\) is called *inductively generated* from \(B\) and \(K\) if every element of \(H\) can be represented by an expression over \(B\) and \(K\).

Examples:

- Natural numbers: \(B_{\mathbb{N}_0} = \{0\}\), \(K_{\mathbb{N}_0} = \{(+1) : \mathbb{N}_0 \rightarrow \mathbb{N}_0\}\).
- Propositional logic: \(B_{AL} = \text{Var}_{AL} \cup \{1, 0\}\), \(K_{AL} = \{\neg, \wedge, \vee, \rightarrow, \leftrightarrow\}\).

**Inductive definitions as a recursion principle.** To define a function \(f : H \rightarrow X\) uniquely, it suffices to:

- fix the value \(f(b)\) for every base case \(b \in B\),
- for every constructor \(k_i : H^{n_i} \rightarrow H\), fix a function \(g_i : X^{n_i} \rightarrow X\) with

$$
f(k_i(h_1, \ldots, h_{n_i})) = g_i(f(h_1), \ldots, f(h_{n_i})).
$$

**Induction principle for proofs (structural induction).** To show \(P(h)\) for all \(h \in H\), it suffices to show:

- \(P(h)\) for every \(h \in B\) (induction start),
- from \(P(h_1), \ldots, P(h_{n_i})\) follows \(P(k_i(h_1, \ldots, h_{n_i}))\) (induction step).

This is the direct generalization of complete induction over the natural numbers.

### 2.5 Model Sets

Instead of evaluating a formula under a single interpretation, one can ask which interpretations make a formula true. This gives a set-valued semantics. Let \(\mathcal{I}_\Sigma\) be the set of all interpretations over \(\Sigma\). Define inductively:

$$
\begin{aligned}
\text{mod}(\neg A) &= \mathcal{I}_\Sigma \setminus \text{mod}(A) \\
\text{mod}(A \wedge B) &= \text{mod}(A) \cap \text{mod}(B) \\
\text{mod}(A \vee B) &= \text{mod}(A) \cup \text{mod}(B) \\
\text{mod}(A \rightarrow B) &= (\mathcal{I}_\Sigma \setminus \text{mod}(A)) \cup \text{mod}(B) \\
\text{mod}(A \leftrightarrow B) &= (\text{mod}(A) \cap \text{mod}(B)) \cup ((\mathcal{I}_\Sigma \setminus \text{mod}(A)) \cap (\mathcal{I}_\Sigma \setminus \text{mod}(B)))
\end{aligned}
$$

This is again an inductive definition.

> **Theorem**  
> 
> \(\text{mod}(A)\) describes exactly the set of models of \(A\), that is
>
> $$
\text{mod}(A) = \{I \in \mathcal{I}_\Sigma \mid \text{val}_I(A) = W\} =: M(A).
$$

**Proof.** By structural induction over the constructors. For \(A \wedge B\), the induction hypothesis gives \(\text{mod}(A) = M(A)\) and \(\text{mod}(B) = M(B)\), hence

$$
\begin{aligned}
\text{mod}(A \wedge B) &= \text{mod}(A) \cap \text{mod}(B) = M(A) \cap M(B) \\
&= \{I \in \mathcal{I}_\Sigma \mid \text{val}_I(A) = W \text{ and } \text{val}_I(B) = W\} \\
&= \{I \in \mathcal{I}_\Sigma \mid \text{val}_I(A \wedge B) = W\} = M(A \wedge B).
\end{aligned}
$$

The base cases and the cases \(\vee\), \(\rightarrow\), \(\leftrightarrow\) are analogous.

### 2.6 Logical Ground Notions

With syntax and semantics in place, the central notions of the logic can be defined in plain terms: a formula may be true under a given interpretation, it may be true under all interpretations, and it may be true under at least one. The following definitions give these intuitions their names.

> **Definition**  
> 
> - A *model* of a formula \(A \in \text{For}^0_\Sigma\) is an interpretation \(I\) over \(\Sigma\) with \(\text{val}_I(A) = W\).
> - For a set of formulas \(\mathcal{M} \subseteq \text{For}^0_\Sigma\), a *model of \(\mathcal{M}\)* is an interpretation \(I\) which is a model of every \(A \in \mathcal{M}\).
> - \(A \in \text{For}^0_\Sigma\) is called *generally valid* (a tautology) iff \(\text{val}_I(A) = W\) for every interpretation \(I\) over \(\Sigma\). Notation: \(\models A\).
> - \(A \in \text{For}^0_\Sigma\) is called *satisfiable* iff there exists an interpretation \(I\) over \(\Sigma\) with \(\text{val}_I(A) = W\).

> **Definition**  
> 
> Let \(\Sigma\) be a signature, \(\mathcal{M} \subseteq \text{For}^0_\Sigma\), \(A, B \in \text{For}^0_\Sigma\).
>
> - \(\mathcal{M} \models A\) (read: "from \(\mathcal{M}\) follows \(A\)") iff every model of \(\mathcal{M}\) is also a model of \(A\).
> - \(A, B \in \text{For}^0_\Sigma\) are called *logically equivalent* iff \(\{A\} \models_\Sigma B\) and \(\{B\} \models_\Sigma A\).

### 2.7 Examples of Generally Valid Formulas

The following tautologies occur constantly when transforming formulas. They are worth knowing by name, since most manipulations of formulas are applications of one of them.

{{< table "data-table" "" >}}  
| Formula | Name |
|---|---|
| \(A \rightarrow A\) | Self-implication |
| \(\neg A \vee A\) | Tertium non datur |
| \(A \rightarrow (B \rightarrow A)\) | Weakening |
| \(0 \rightarrow A\) | Ex falso quodlibet |
| \((A \wedge (A \rightarrow B)) \rightarrow B\) | Modus ponens |
| \(A \wedge A \leftrightarrow A\) | Idempotency |
| \((\neg\neg A) \leftrightarrow A\) | Double negation |
| \(A \wedge (A \vee B) \leftrightarrow A\) | Absorption |
| \((A \leftrightarrow B) \leftrightarrow ((A \rightarrow B) \wedge (B \rightarrow A))\) | Equivalence/implication |
| \(A \wedge (B \vee C) \leftrightarrow (A \wedge B) \vee (A \wedge C)\) | Distributivity |
| \(A \vee (B \wedge C) \leftrightarrow (A \vee B) \wedge (A \vee C)\) | Distributivity |
| \((A \rightarrow B) \leftrightarrow (\neg B \rightarrow \neg A)\) | Contraposition |
| \((A \rightarrow (B \rightarrow C)) \leftrightarrow ((A \rightarrow B) \rightarrow (A \rightarrow C))\) | Distribution |
| \(\neg(A \vee B) \leftrightarrow \neg A \wedge \neg B\) | De Morgan |
| \(\neg(A \wedge B) \leftrightarrow \neg A \vee \neg B\) | De Morgan |
{{< /table >}}

### 2.8 Simple Theorems

The notions of Section 2.6 are related to each other in simple ways. The following theorems collect these relationships; in practice they are used to shift a question from one notion to another, for example from entailment to general validity.

> **Theorem**  
> 
> - \(A\) is satisfiable iff \(\neg A\) is not generally valid.
> - \(\models A\) iff \(A\) is generally valid. (Notational restatement.)
> - \(\models \neg A\) iff \(A\) is unsatisfiable.
> - \(A \models B\) iff \(\models A \rightarrow B\).
> - \(\mathcal{M} \cup \{A\} \models B\) iff \(\mathcal{M} \models A \rightarrow B\).
> - \(A, B\) are logically equivalent iff \(A \leftrightarrow B\) is generally valid.

These small equivalences are used constantly: they allow a semantic question ("does \(\mathcal{M}\) entail \(A\)?") to be turned into a question about the general validity of a single formula, and vice versa.

> **Theorem** Logical transformation  
> 
> If
>
> - \(A\) and \(B\) are logically equivalent,
> - \(A\) is a subformula of \(C\),
> - \(C'\) arises from \(C\) by replacing \(A\) with \(B\),
>
> then \(C\) and \(C'\) are logically equivalent.

This theorem justifies all the algebraic manipulation of formulas one does in practice: replacing any subformula by an equivalent one never changes the meaning of the whole formula.

### 2.9 Boolean Functions

Every formula determines a function: it maps an assignment of truth values to its atoms to a truth value. The following definition makes this precise. The theorem of functional completeness then states that the converse holds as well: every such function is described by some formula.

> **Definition**  
> 
> 1. A function \(f\) from \(\{W, F\}^n\) to \(\{W, F\}\) for \(n \in \mathbb{N}\) is called an *\(n\)-ary Boolean function*.
> 2. Let \(A \in \text{For}^0_\Sigma\) with \(\Sigma = \{P_1, \ldots, P_n\}\). The *Boolean function \(f_A\)* of \(A\) is defined by
>
> $$
f_A(\bar{b}) = \text{val}_I(A),
$$
>
> where \(\bar{b} \in \{W, F\}^n\) and \(I(P_i) = b_i\).

The Boolean function \(f_A\) depends on the order of the propositional atoms occurring in it. For \(A = P_1 \wedge P_3\) in the signature \(\Sigma = \{P_1, P_2, P_3\}\) the truth table is:

{{< table "data-table" "" >}}  
| \(P_1\) | \(P_2\) | \(P_3\) | \(f_A(P_1, P_2, P_3)\) |
|---|---|---|---|
| W | W | W | W |
| W | W | F | F |
| W | F | W | W |
| W | F | F | F |
| F | W | W | F |
| F | W | F | F |
| F | F | W | F |
| F | F | F | F |
{{< /table >}}

The variable \(P_2\) is irrelevant for \(f_A\), but it still appears in the signature, so the table has \(2^3\) rows.

> **Theorem** Functional completeness  
> 
> For every Boolean function \(f : \{W, F\}^n \rightarrow \{W, F\}\) there exists a formula \(A \in \text{For}^0_\Sigma\) with \(f = f_A\).

**Proof.** Let \(\bar{b}_1, \ldots, \bar{b}_k\) be exactly the \(n\)-tuples from \(\{W, F\}^n\) with \(f(\bar{b}_i) = W\). Set

$$
A = A_1 \vee \ldots \vee A_k, \qquad A_i = A_{i,1} \wedge \ldots \wedge A_{i,n}
$$

with

$$
A_{i,j} =
\begin{cases}
P_j & \text{if } b_{i,j} = W \\
\neg P_j & \text{if } b_{i,j} = F
\end{cases}
$$

Each \(A_i\) is true exactly under the interpretation \(\bar{b}_i\), so their disjunction is true exactly under the interpretations where \(f\) is true.

> **Definition** Basis  
> 
> A set \(K_{Op}\) of propositional constants and operators is called a *basis* if for every Boolean function \(f : \{W, F\}^n \rightarrow \{W, F\}\) there exists a formula \(A\) built only with constants and operators from \(K_{Op}\), with \(f_A = f\). No minimality of \(K_{Op}\) is required.

Examples of bases:

- \(\{1, 0, \neg, \wedge, \vee, \rightarrow, \leftrightarrow\}\)
- \(\{\neg, \wedge\}\)
- \(\{0, \rightarrow\}\)
- \(\{\downarrow\}\), where \(A \downarrow B = \neg(A \vee B)\):

{{< table "data-table" "" >}}  
| \(\text{val}_I(A)\) | \(\text{val}_I(B)\) | \(\text{val}_I(A \downarrow B)\) |
|---|---|---|
| W | W | F |
| W | F | F |
| F | W | F |
| F | F | W |
{{< /table >}}

The single Sheffer operator \(\downarrow\) alone is enough to express every Boolean function.

### 2.10 Set of Problems and Solutions

{{< warning "TODO" >}}
The problems and solutions for this section will be added later.
{{< /warning >}}

## 3. Normal Forms

The algorithms of Section 6 expect their input in a specific shape. Normal forms standardize the shape of formulas. Every formula can be transformed into an equivalent formula in normal form, which for practical purposes is done by repeated application of the transformation theorem from Section 2.8.

> **Definition** Conjunctive and disjunctive normal form  
> 
> 1. A *literal* is an atom or a negated atom.
> 2. A formula is in *disjunctive normal form* (DNF) if it is a disjunction of conjunctions of literals (with degenerate cases allowed).
> 3. A formula is in *conjunctive normal form* (CNF) if it is a conjunction of disjunctions of literals. A disjunction of literals is called a *clause*; CNF is therefore also called *clause normal form*.

> **Theorem**  
> 
> Every formula has an equivalent disjunctive normal form and an equivalent conjunctive normal form.

The construction from the proof of functional completeness (Section 2.9) already produces a DNF. For the CNF one first pushes negations inward using the De Morgan equivalences and removes double negations, then distributes \(\vee\) over \(\wedge\).

Two remarks from the Skript worth keeping in mind:

- The *complete* CNF (every clause mentions every atom of the signature, possibly trivially) is unique up to the order of clauses, but practically useless: the complete CNF of \(P_1 \wedge P_2\) over \(\{P_1, P_2\}\) already has 4 clauses, and over a signature with \(n\) atoms up to \(2^n\).
- The equivalent CNF can be exponentially larger than the original formula; for the purposes of Section 6 one can also work with formulas that are only *satisfiability-equivalent* to a CNF, which avoids the blow-up.

## 4. Craig's Interpolation Lemma

William Craig (1918–2016, UC Berkeley) formulated his lemma in the 1950s for predicate logic. Its practical relevance was discovered around the turn of the millennium, when it became a tool in model checking (see Section 4.4).

### 4.1 The Lemma

The lemma answers the question of what an implication \(A \rightarrow B\) rests on when \(A\) and \(B\) use different atoms. Its answer: the implication can be factored through a formula that speaks only the language common to \(A\) and \(B\).

> **Theorem** Craig's interpolation lemma  
> 
> Let \(A, B\) be propositional formulas with
>
> $$
\models A \rightarrow B.
$$
>
> Then there exists a formula \(C\) with
>
> $$
\models A \rightarrow C \qquad \text{and} \qquad \models C \rightarrow B,
$$
>
> such that in \(C\) only those propositional atoms \(P \in \Sigma\) occur which occur both in \(A\) and in \(B\).

The formula \(C\) is called an *interpolant*. Intuitively: if \(A\) implies \(B\), then there is a "common reason" for this implication which speaks only the language shared by \(A\) and \(B\).

### 4.2 An Example

\(P_1 \wedge P_2 \rightarrow P_1 \vee P_3\) is a tautology. So are \(P_1 \wedge P_2 \rightarrow P_1\) and \(P_1 \rightarrow P_1 \vee P_3\). Therefore \(P_1\) is an interpolant for \(P_1 \wedge P_2 \rightarrow P_1 \vee P_3\): it contains only the atom \(P_1\), which occurs in both \(A = P_1 \wedge P_2\) and \(B = P_1 \vee P_3\).

### 4.3 Construction of an Interpolant

The lemma is constructive. Let \(P_1, \ldots, P_n\) be all the atoms that occur in \(A\) but not in \(B\). For constants \(c_i \in \{1, 0\}\), denote by \(A[c_1, \ldots, c_n]\) the formula obtained from \(A\) by replacing each \(P_i\) with \(c_i\). Set

$$
C \equiv \bigvee_{(c_1, \ldots, c_n) \in \{1,0\}^n} A[c_1, \ldots, c_n].
$$

In words: \(C\) is the disjunction of all variants of \(A\) in which the \(A\)-private atoms are exhaustively set to true or false. The proof of the correctness of this construction can be found in the Skript.

**Example 1.** Consider the tautology \(A \rightarrow B\) with \(A = P_1 \wedge P_2\), \(B = P_1 \vee P_3\). The atom \(P_2\) is the only one that occurs in \(A\) but not in \(B\).

$$
\begin{aligned}
A[1] &= P_1 \wedge 1 \equiv P_1 \\
A[0] &= P_1 \wedge 0 \equiv 0 \\
C &= A[1] \vee A[0] \equiv P_1 \vee 0 \equiv P_1
\end{aligned}
$$

**Example 2.** Consider

$$
A = (P_1 \vee \neg P_2) \wedge (\neg P_1 \vee \neg P_3) \wedge P_2, \qquad B = \neg((\neg P_2 \vee P_3) \wedge (P_2 \vee P_4) \wedge \neg P_4).
$$

Here \(A \equiv P_1 \wedge P_2 \wedge \neg P_3\) and \(B \equiv \neg P_2 \vee \neg P_3 \vee P_4\), and \(A \rightarrow B\) is a tautology. The atom \(P_1\) is the only one that occurs in \(A\) and not in \(B\).

$$
\begin{aligned}
A[1] &= (1 \vee \neg P_2) \wedge (\neg 1 \vee \neg P_3) \wedge P_2 \equiv 1 \wedge \neg P_3 \wedge P_2 \equiv \neg P_3 \wedge P_2 \\
A[0] &= (0 \vee \neg P_2) \wedge (\neg 0 \vee \neg P_3) \wedge P_2 \equiv \neg P_2 \wedge 1 \wedge P_2 \equiv 0
\end{aligned}
$$

So \(C = (\neg P_3 \wedge P_2) \vee 0 \equiv \neg P_3 \wedge P_2\) is an interpolant for \(A \rightarrow B\).

### 4.4 Application: Model Checking

**Interpolant for satisfiability.** An interpolant \(P\) for two propositional formulas \(A, B\) for which \(A \wedge B\) is *unsatisfiable* has the following properties:

- \(A \rightarrow P\) is generally valid,
- \(P \wedge B\) is unsatisfiable,
- in \(P\) only the common AL variables of \(A\) and \(B\) occur.

This view is dual to the first definition, and it is the form used in practice (K.L. McMillan, *Interpolation and SAT-Based Model Checking*, CAV 2003). Interpolants are used there to compute an inductive invariant over an abstraction of the state space.

**Modeling dynamic systems.** A system can be modeled by propositional variables in \(\Sigma\): possible initial states by a formula over \(\Sigma\), state transitions by a formula that uses two copies \(x\) and \(x'\) of the variables (primed variables stand for the successor state), and forbidden states by a formula \(\text{Bad}\).

> **Definition** Transition system  
> 
> A (symbolic) transition system \(TS = (\text{Init}, \text{Tr}, \text{Bad})\) over a signature \(\Sigma\) is given by the AL formulas
>
> - \(\text{Init} \in \text{Fml}_\Sigma\): valid start states,
> - \(\text{Tr} \in \text{Fml}_{\Sigma \cup \Sigma'}\): transition relation (copies of the variables),
> - \(\text{Bad}(x)\): forbidden states.

Example (traffic light). \(\Sigma = \{r, y, g\}\) for "red", "yellow", "green":

$$
\begin{aligned}
\text{Init} &:= r \wedge \neg y \wedge \neg g \\
\text{Tr} &:= (r' \leftrightarrow y \leftrightarrow \neg r) \wedge (y' \leftrightarrow \neg y) \wedge (g' \leftrightarrow y \wedge r) \\
\text{Bad} &:= r \wedge g
\end{aligned}
$$

For modeling a run with several states, several copies of the variables are needed: \(\Sigma, \Sigma', \Sigma'', \ldots\). Consider the conjunction

$$
P_4 := \text{Init} \wedge \text{Tr}_{\Sigma,\Sigma'} \wedge \ldots \wedge \text{Tr}_{\Sigma''',\Sigma''''} \wedge \text{Bad}_{\Sigma''''}.
$$

If \(P_4\) is satisfiable, then there exists a run (of length 4) in this transition system that reaches a forbidden state.

Craig's theorem now states: there is a formula \(F\) that summarizes the first three transitions and uses only variables from \(\Sigma'''\), such that

$$
P_4 \text{ satisfiable} \iff F \wedge \text{Tr}_{\Sigma''',\Sigma''''} \text{ satisfiable}.
$$

This "summarizing" of transitions reduces the search space considerably in some model checking approaches.

### 4.5 Set of Problems and Solutions

{{< warning "TODO" >}}
The problems and solutions for this section will be added later.
{{< /warning >}}

## 5. Binary Decision Diagrams

### 5.1 Shannon Formulas

Shannon formulas are propositional formulas built from

- the ternary operator \(\text{sh}\),
- the constants \(0\) and \(1\),
- the propositional variables \(P_1, \ldots, P_n, \ldots\).

The semantics of \(\text{sh}\) under an interpretation \(I\) is

$$
\text{val}_I(\text{sh}(P_1, P_2, P_3)) =
\begin{cases}
\text{val}_I(P_2) & \text{if } \text{val}_I(P_1) = F \\
\text{val}_I(P_3) & \text{if } \text{val}_I(P_1) = W
\end{cases}
$$

or in table form:

{{< table "data-table" "" >}}  
| \(\text{val}_I(P_1)\) | W | W | W | W | F | F | F | F |
|---|---|---|---|---|---|---|---|---|
| \(\text{val}_I(P_2)\) | W | W | F | F | W | W | F | F |
| \(\text{val}_I(P_3)\) | W | F | W | F | W | F | W | F |
| \(\text{val}_I(\text{sh}(P_1,P_2,P_3))\) | W | F | W | F | W | W | F | F |
{{< /table >}}

So \(\text{sh}(A, B, C)\) means: if \(A\) then \(C\), else \(B\). It is an if-then-else on the level of formulas.

**Properties of the sh operator.**

$$
\begin{aligned}
\text{sh}(P_1, P_2, P_3) &\leftrightarrow (\neg P_1 \wedge P_2) \vee (P_1 \wedge P_3) \\
\text{sh}(P_1, P_2, P_3) &\leftrightarrow (\neg P_1 \vee P_3) \wedge (P_1 \vee P_2) \\
\text{sh}(P_1, P_2, P_3) &\leftrightarrow (P_1 \rightarrow P_3) \wedge (\neg P_1 \rightarrow P_2) \\
\neg\,\text{sh}(A, B, C) &\leftrightarrow \text{sh}(A, \neg B, \neg C) \\
\text{sh}(0, P_2, P_3) &\leftrightarrow P_2 \\
\text{sh}(1, P_2, P_3) &\leftrightarrow P_3 \\
\text{sh}(P, 0, 1) &\leftrightarrow P \\
\text{sh}(P, 1, 0) &\leftrightarrow \neg P \\
\text{sh}(P_1, P_2, P_2) &\leftrightarrow P_2 \\
\text{sh}(\text{sh}(P_1, P_2, P_3), P_4, P_5) &\leftrightarrow \text{sh}(P_1, \text{sh}(P_2, P_4, P_5), \text{sh}(P_3, P_4, P_5)) \\
A &\leftrightarrow \text{sh}(P, A_{P=0}, A_{P=1})
\end{aligned}
$$

The last identity is the Shannon expansion: every formula \(A\) can be decomposed according to whether an atom \(P\) is false or true, where \(A_{P=0}\) and \(A_{P=1}\) arise from \(A\) by replacing \(P\) with \(0\) and \(1\).

### 5.2 Normalized Shannon Formulas

We fix an order on the set of propositional variables, for instance the one given by the order of the indices.

> **Definition**  
> 
> 1. The constants \(0, 1\) are normalized sh-formulas.
> 2. \(\text{sh}(P_i, A, B)\) is a normalized sh-formula if \(A\) and \(B\) are normalized sh-formulas and for every variable \(P_j\) occurring in \(A\) or \(B\): \(i < j\).

> **Theorem**  
> 
> Every propositional formula has an equivalent normalized sh-formula.

The proof repeatedly applies the Shannon expansion \(A \leftrightarrow \text{sh}(P, A_{P=0}, A_{P=1})\), always splitting along the smallest remaining variable.

### 5.3 Shannon Graphs

There is an obvious correspondence between normalized sh-formulas and a graph representation. From now on we work with the graphs directly.

> **Definition** Shannon graph  
> 
> A *sh-graph* is a directed, binary, connected acyclic graph in which
>
> - every nonterminal node \(v\) is assigned a natural number \(\text{index}(v)\), and exactly two edges leave \(v\), one labeled \(0\) and one labeled \(1\);
> - every terminal node \(v\) is labeled \(0\) or \(1\), and we define \(\text{wert}(0) = F\) and \(\text{wert}(1) = W\);
> - if the nonterminal node \(w\) is an immediate successor of \(v\), then \(\text{index}(v) < \text{index}(w)\);
> - there is exactly one root node.

Evaluation trees of a formula are sh-graphs, but not minimal ones. The correspondence to normalized sh-formulas is: the \(n\)-th variable corresponds to a node with index \(n\).

**Shannon graphs as Boolean functions.** To every sh-graph \(G\) one can assign an \(m\)-ary Boolean function \(f_G\), where \(m\) is the number of different indices \(i_1, \ldots, i_m\) occurring in \(G\). The function value \(f_G(P_{i_1}, \ldots, P_{i_m})\) is determined by walking a path through \(G\) starting at the root: at a node \(v\), follow the \(0\)-edge if the input variable \(P_{\text{index}(v)}\) has value \(F\), otherwise the \(1\)-edge. The value of the terminal node reached is the function value.

<!-- TODO: figure: Shannon graph for f(P1,P2,P3) with f_G(F,W,F) = F and f_G(W,F,W) = W -->

**Construction of a Shannon graph.** Given a function \(f\), the graph is built top-down: the root asks the first variable \(P_1\); the two successors represent the restrictions \(f_1(P_2, P_3) = f(W, P_2, P_3)\) and \(f_2(P_2, P_3) = f(F, P_2, P_3)\), and so on recursively. For the majority function on three variables,

$$
f(P_1, P_2, P_3) =
\begin{cases}
W & \text{if } |\{1 \leq i \leq 3 \mid P_i = W\}| = 2 \\
F & \text{otherwise}
\end{cases}
$$

the subfunctions \(f_3(P_3) = \neg P_3\), \(f_4(P_3) = P_3\), \(f_5(P_3) = F\) and \(f_6(P_3) = P_3\) arise, and one observes \(f_6 = f_4\): two subgraphs coincide and can be shared.

<!-- TODO: figure: construction of the Shannon graph for the majority function -->

### 5.4 Reduced Shannon Graphs

A Shannon graph for a function can contain redundancy: identical subgraphs may appear several times. Reduction removes this redundancy. The first definition says what counts as redundant, the second says when two graphs count as the same.

> **Definition** Reduction  
> 
> A sh-graph is called *reduced* if
>
> 1. there are no two distinct nodes \(v\) and \(w\) such that the subgraph \(G_v\) rooted in \(v\) is isomorphic to the subgraph \(G_w\) rooted in \(w\);
> 2. there is no node \(v\) such that both edges leaving \(v\) lead to the same successor node.
>
> A reduced Shannon graph is also called an *ordered binary decision diagram*: (O)BDD.

> **Definition** Isomorphism  
> 
> Let two sh-graphs \(H, G\) with node sets \(V_1, V_2\) be given. \(H\) and \(G\) are called *isomorphic* (\(H \cong G\)) iff there is a bijective mapping \(\pi\) from \(V_1\) to \(V_2\) with:
>
> 1. \(\text{index}(k) = \text{index}(\pi(k))\) for every nonterminal node \(k \in V_1\),
> 2. \(\text{wert}(k) = \text{wert}(\pi(k))\) for every terminal node \(k \in V_1\),
> 3. for every nonterminal node \(k \in V_1\) whose \(0\)-edge / \(1\)-edge leads to the node \(k_0\) / \(k_1\): the \(0\)-edge of \(\pi(k)\) leads to \(\pi(k_0)\) and the \(1\)-edge to \(\pi(k_1)\).

> **Theorem** A criterion for reducedness  
> 
> Let \(G\) be a Shannon graph such that for all nonterminal nodes \(v, w\) and all terminal nodes \(u, s\):
>
> - if \(\text{index}(v) = \text{index}(w)\), the \(1\)-successors of \(v\) and \(w\) are identical and the \(0\)-successors of \(v\) and \(w\) are identical, then \(v = w\);
> - if \(\text{wert}(u) = \text{wert}(s)\), then \(u = s\).
>
> Then \(G\) fulfills condition (1) of the definition of reduced Shannon graphs, i.e. for every pair \(x, y\) of nodes: if \(G_x\) is isomorphic to \(G_y\), then \(x = y\).

In words: it suffices to merge same-index nodes with identical children (rule 1 of the definition) and to merge terminals of equal value (rule 2), because by induction over the graph this removes *all* isomorphic subgraphs. Reduction is therefore a purely local operation.

<!-- TODO: figure: example of isomorphism and stepwise reduction of a sh-graph -->

### 5.5 Uniqueness of Reduced Shannon Graphs

The effort of the reduction pays off in uniqueness. The theorem states that, after reduction, the graph of a function is a canonical object: the function determines the graph, and not merely the other way around.

> **Theorem**  
> 
> Let \(G, H\) be reduced sh-graphs over \(\Sigma = \{P_1, \ldots, P_n\}\). Then
>
> $$
f_G = f_H \iff G \cong H.
$$
>
> That is: for every Boolean function \(f\) there is, up to isomorphism, exactly one reduced sh-graph \(H\) with \(f = f_H\).

This is the central result justifying BDDs as a *canonical* representation of Boolean functions: deciding equality of two functions reduces to checking isomorphism of their reduced BDDs, which is a cheap graph comparison.

### 5.6 BDD Size and Variable Ordering

The size of a BDD depends drastically on the chosen variable order. Two BDDs for the same function

$$
(x_1 \wedge x_2) \vee (x_3 \wedge x_4) \vee (x_5 \wedge x_6) \vee (x_7 \wedge x_8)
$$

look very different under the orders \(x_1 < x_2 < x_3 < x_4 < x_5 < x_6 < x_7 < x_8\) and \(x_1 < x_3 < x_5 < x_7 < x_2 < x_4 < x_6 < x_8\): the first order gives a compact graph, the second an exponentially wider one.

<!-- TODO: figure: the two BDDs for (x1∧x2)∨(x3∧x4)∨(x5∧x6)∨(x7∧x8) under the two variable orders -->

> **Theorem** Hardness of multiplication  
> 
> Let \(X\) contain the \(2k\) variables \(\{x_0, \ldots, x_{k-1}, y_0, \ldots, y_{k-1}\}\), where \(x = x_0 \ldots x_{k-1}\) and \(y = y_0 \ldots y_{k-1}\) denote \(k\)-digit binary numbers. For \(0 \leq i < 2k\), let \(\text{Multi}_i\) be the Boolean function describing the \(i\)-th bit of the product of \(x\) and \(y\). Then for every order \(<\) of the variables in \(X\) there exists an index \(0 \leq i < 2k\) such that the BDD \(B_{\text{Multi}_i,<}\) has at least \(2^{k/8}\) nodes.

So no matter how cleverly the variables are ordered, some output bit of integer multiplication has an exponentially large BDD. BDDs are a powerful canonical representation, but not a universal one.

### 5.7 Set of Problems and Solutions

{{< warning "TODO" >}}
The problems and solutions for this section will be added later.
{{< /warning >}}

## 6. The Satisfiability Problem

### 6.1 The SAT Problem

The practical goal of this block of the course is a single computational problem: deciding whether a formula is satisfiable. The following definition fixes the problem, and the theorem of Cook classifies its difficulty.

> **Definition** SAT  
> 
> - *Instance:* a propositional formula \(F \in \text{For}^0\).
> - *Question:* is \(F\) satisfiable? That is, is there an interpretation \(I\) with \(\text{val}_I(F) = W\)?

SAT is NP-complete: if there were a (deterministic) polynomial decision algorithm for satisfiability, then \(\text{NP} = \text{P}\), i.e. every nondeterministically polynomial decision problem would also be deterministically polynomial.

> **Theorem** Theorem of Cook (1971)  
> 
> The satisfiability problem of propositional logic (SAT) is NP-complete.

Stephen A. Cook (born 1939), professor of computer science at the University of Toronto, Turing Award laureate, proved this as the first NP-completeness result.

### 6.2 Subclasses

The complexity of satisfiability depends heavily on the shape of the input formulas:

{{< table "data-table" "" >}}  
| Formula class | Complexity of satisfiability |
|---|---|
| CNF | NP-complete |
| 3-CNF | NP-complete |
| 2-CNF | polynomially decidable |
| DNF | polynomially decidable (\(O(n \log n)\)) |
| Horn formulas | polynomially decidable (\(O(n^2)\)) |
{{< /table >}}

Remarks: \(k\)-CNF formulas are conjunctions of disjunctions with at most \(k\) literals. 2-CNF formulas are also called *Krom formulas*.

So restricting the shape of formulas can move the problem from NP-complete to polynomial. The interesting question is which restrictions still suffice for practical expressiveness. Horn formulas are the most important subclass with a non-NP-complete satisfiability problem.

### 6.3 Horn Formulas

Horn formulas are a restricted shape of CNF formulas for which satisfiability becomes easy. The restriction is small: every clause may contain at most one positive literal.

> **Definition** Horn formula  
> 
> A propositional formula \(A\) is a *Horn formula* if
>
> - \(A\) is in CNF, and
> - every disjunction (clause) in \(A\) contains at most one positive literal.

**Alternative notation.** A clause \(\neg B_1 \vee \ldots \vee \neg B_m \vee A\) is written as the rule \(B_1 \wedge \ldots \wedge B_m \rightarrow A\), a clause \(\neg B_1 \vee \ldots \vee \neg B_m\) as the query \(B_1 \wedge \ldots \wedge B_m \rightarrow 0\), and a single positive literal \(A\) as the fact \(A\). For the empty disjunction we write \(\Box\). The conjunction \(B_1 \wedge \ldots \wedge B_m\) is called the *body* ("Rumpf") and \(A\) the *head* ("Kopf").

Attention: the empty set of clauses \(\{\}\) is different from the set \(\{\Box\}\) containing the empty clause, and from \(\Box\) itself.

**Example.** The Horn formula

$$
\begin{aligned}
&\neg P \\
&\wedge \; (Q \vee \neg R \vee \neg S) \\
&\wedge \; (\neg Q \vee \neg S) \\
&\wedge \; R \\
&\wedge \; S \\
&\wedge \; (\neg Q \vee P)
\end{aligned}
$$

reads in rule notation:

$$
\begin{aligned}
& (P \rightarrow 0) \\
\wedge\; & (R \wedge S \rightarrow Q) \\
\wedge\; & (Q \wedge S \rightarrow 0) \\
\wedge\; & R \\
\wedge\; & S \\
\wedge\; & (Q \rightarrow P)
\end{aligned}
$$

> **Theorem**  
> 
> For Horn formulas, satisfiability is decidable in quadratic time.

**Satisfiability test.** Let \(C = D_1 \wedge \ldots \wedge D_m\) be a Horn formula. *Marking* an atom in \(C\) means marking it at all places of its occurrence in \(C\).

1. If \(\Box\) is in \(C\): output "unsatisfiable". Stop. Otherwise, if there are no facts in \(C\): output "satisfiable". Stop. Otherwise: mark all facts.
2. 
   1. If there exists a \(B_1 \wedge \ldots \wedge B_m \rightarrow 0\) (a query) such that all atoms \(B_i\) in the body are marked: output "unsatisfiable". Stop.
   2. If there exists a \(B_1 \wedge \ldots \wedge B_m \rightarrow A\) (a rule) such that all atoms \(B_i\) in the body are marked but the head \(A\) is not: mark \(A\). Go to 2.
   3. Otherwise: output "satisfiable". Stop.

The idea is forward chaining: facts are what must be true; a rule whose body is completely true forces its head to be true; if a query's body becomes completely true, the formula is contradictory.

**Example.** Consider the Horn clause set

$$
p, \quad q, \quad q \wedge r \rightarrow s, \quad p \rightarrow r, \quad s \rightarrow 0.
$$

The facts \(p\) and \(q\) are marked. Rule \(p \rightarrow r\) fires: mark \(r\). Rule \(q \wedge r \rightarrow s\) fires: mark \(s\). Now the query \(s \rightarrow 0\) has a fully marked body: the formula set is unsatisfiable.

<!-- TODO: figure: stepwise marking of the example formula set -->

### 6.4 Excursion: The Exponential Time Hypothesis

Lower bounds for the satisfiability problem are usually derived from a stronger assumption than \(\text{P} \neq \text{NP}\). The following assumption is the standard one.

> **Assumption** ETH (Impagliazzo & Paturi 1999)  
> 
> There is no deterministic algorithm that solves 3-SAT in subexponential time \(2^{o(n)}\).

The ETH is stronger than \(\text{P} \neq \text{NP}\) and is the foundation of many lower bounds in parameterized complexity theory.

A remark on the state of the art: on 26 October 2026, OpenAI and Anthropic independently claimed to have refuted the ETH, each with a deterministic 3-SAT algorithm of running time \(2^{O(n \cdot \log\log n / \sqrt{\log n})}\). There exists a Lean proof. It is early days: experts judge the proofs differently (among other things, suspicion of errors, no peer review, differently formalized bounds). The algorithm would only become faster than brute force from roughly \(10^{1000}\) variables onwards. ETH implies \(\text{P} \neq \text{NP}\), but refuting the ETH does not prove \(\text{P} = \text{NP}\).

### 6.5 The Davis–Putnam–Logemann–Loveland Procedure

The DPLL procedure is the classical method for deciding the general satisfiability problem, and the basis of the currently fastest and almost exclusively used practical procedures. Its input is a formula in CNF.

**Excursion: clause notation.** In disjunctions and conjunctions, neither the order of the subformulas nor the multiplicity of identical subformulas matters. This suggests set notation: a disjunction as a set is a *clause*, a CNF formula as a set is a *set of clauses*. Notation: \(\Box\) for the empty clause, \(\emptyset\) for the empty clause set.

> **Definition** Semantics of the clause notation  
> 
> Let \(I\) be an interpretation, \(S\) a set of clauses, \(C\) a clause:
>
> 1. \(\text{val}_I(S) := W\) if for all \(C \in S\): \(\text{val}_I(C) = W\); else \(F\).
> 2. \(\text{val}_I(C) := W\) if there exists an \(L \in C\) with \(\text{val}_I(L) = W\); else \(F\).
> 3. Hence \(\text{val}_I(\emptyset) = W\) (the empty clause set is satisfiable by every interpretation).
> 4. Hence \(\text{val}_I(\Box) = F\) (the empty clause is satisfied by no interpretation).

**The procedure.** With

$$
\text{atom}(S) = \bigcup_{C \in S} \text{atom}(C), \quad \text{atom}(C) = \{P \in \Sigma \mid P \in C \text{ or } \neg P \in C\},
$$

$$
\text{red}_{\{L\}}(S) = \{\text{red}_{\{L\}}(C) \mid C \in S \text{ with } L \notin C\}, \quad \text{red}_{\{L\}}(C) = C \setminus \{L\}, \text{ where } \overline{A} = \neg A \text{ and } \overline{\neg A} = A \text{ for } A \in \Sigma,
$$

and \(S_P = S \cup \{\{P\}\}\), \(S_{\neg P} = S \cup \{\{\neg P\}\}\), the procedure reads:

```
procedure DPLL(clause set S)
1 if S = ∅ then return true;
2 if □ ∈ S then return false;
3 if S contains a unit clause
4    then choose a unit clause {L} ∈ S;
5       return DPLL(red{L}(S));
6    else choose P ∈ atom(S)
7       return DPLL(S_P) ∨ DPLL(S_¬P);
```

Explanation of the lines:

- Line 1: no clauses left, nothing to satisfy, so the answer is satisfiable.
- Line 2: the empty clause is unsatisfiable, so the answer is unsatisfiable overall.
- Line 5: if there is a unit clause, make it true and propagate the consequence (unit propagation).
- Line 7: otherwise, case distinction over an arbitrary atom.

**Example.** We start with the clause set

$$
S = \left\{
\begin{array}{cc}
\{P_1, P_2, P_3\} & \{\neg P_1, P_2, \neg P_4\} \\
\{\neg P_1, P_3\} & \{\neg P_1, \neg P_3, P_4\} \\
\{P_1, \neg P_3\} & \{\neg P_2\}
\end{array}
\right\}
$$

At the first call of DPLL(S), the subroutine \(\text{red}_{\{\neg P_2\}}(S)\) is applied (unit propagation of the unit clause \(\{\neg P_2\}\)), which yields \(S_1\). In the following, *struck out* means the whole clause is removed, *removed* means a literal is deleted from a clause:

$$
S_1 = \left\{
\begin{array}{cc}
\{P_1, P_3\} & \{\neg P_1, \neg P_4\} \\
\{\neg P_1, P_3\} & \{\neg P_1, \neg P_3, P_4\} \\
\{P_1, \neg P_3\} &
\end{array}
\right\}
$$

\(S_1\) contains no unit clause, so the variable \(P_1\) is chosen and DPLL(\(S_{1,0}\)) and DPLL(\(S_{1,1}\)) are called, where \(S_{1,0} = S_1 \cup \{\{P_1\}\}\) and \(S_{1,1} = S_1 \cup \{\{\neg P_1\}\}\).

For \(S_{1,0}\), the reduction \(\text{red}_{\{P_1\}}(S_{1,0})\) removes all clauses containing \(P_1\) and deletes \(P_1\) from the remaining ones:

$$
S_{2,0} = \text{red}_{\{P_1\}}(S_{1,0}) = \{\{\neg P_4\}, \{P_3\}, \{\neg P_3, P_4\}\}.
$$

The call \(\text{red}_{\{P_3\}}(S_{2,0})\) yields \(\{\{\neg P_4\}, \{P_4\}\}\), and then \(\text{red}_{\{P_4\}}(\{\{P_4\}, \{\neg P_4\}\}) = \{\Box\}\). From the empty clause follows the unsatisfiability of \(S_{1,0}\).

Now DPLL(\(S_{1,1}\)) is processed. The reduction \(\text{red}_{\{\neg P_1\}}(S_{1,1})\) removes the clauses containing \(\neg P_1\) and strikes \(P_1\) from the rest, which yields

$$
\{\{P_3\}, \{\neg P_3\}\},
$$

from which in the next step \(\{\Box\}\) arises. This yields the unsatisfiability of \(S_{1,1}\) and thereby the unsatisfiability of \(S\) altogether.

> **Theorem**  
> 
> 1. The DPLL algorithm terminates for every input.
> 2. The DPLL algorithm is correct and complete: (a) from DPLL(\(S\)) = true it follows that \(S\) is satisfiable, and (b) if \(S\) is satisfiable, then DPLL(\(S\)) = true.

**Proof idea.** *Termination:* at every reduction an atom disappears. *Correctness/completeness:* every step leads to a satisfiability-equivalent clause set; \(\emptyset\) is satisfiable, \(\{\Box\}\) is unsatisfiable.

### 6.6 Excursion: Conflict Driven Clause Learning (CDCL)

A weakness of plain DPLL: it can explore the same failed partial assignments repeatedly, because it learns nothing from a conflict. CDCL extends DPLL by *learning* clauses from conflicts: when a case distinction leads to the empty clause, a new clause is derived that explains the conflict, and the search backtracks not chronologically but to the highest decision involved in that clause. The learned clause then prunes large parts of the remaining search space.

<!-- TODO: figure: DPLL vs CDCL search tree on the example clause set (A∨B, B∨C, ¬B∨C, P∨Q, ¬P∨Q, R∨¬Q∨¬C, ¬R∨¬Q∨¬C) -->

The practical impact is enormous. In the SAT competition, the winning solvers from year to year (zchaff, minisat, glucose, lingeling, maple, kissat, ...) solve steadily more instances within the same CPU time budget; current solvers handle up to 8 million variables and 129 million clauses.

<!-- TODO: figure: SAT competition winners chart on the SC2020 benchmark suite (data by Armin Biere and Marijn Heule), source: http://fmv.jku.at/kissat/ -->

### 6.7 Set of Problems and Solutions

{{< warning "TODO" >}}
The problems and solutions for this section will be added later.
{{< /warning >}}

## 7. Conclusion

This article is by no stretch of the imagination complete, highly accurate, or very intuitive and understandable. It is more like hastily written notes from my lecture combined with various external materials. The most use one can get from this article is to use it as a reference for definitions and theorems, and later to calculate through the *problem solution sets*, where the solutions should be fairly accurate.

---

Resources:
- The lecture "Formale Systeme" (Winter 2026/2027) by Dr. Mattias Ulbrich, KASTEL, Institut für Informationssicherheit und Verlässlichkeit, KIT
- The lecture Skript "Formale Systeme"
