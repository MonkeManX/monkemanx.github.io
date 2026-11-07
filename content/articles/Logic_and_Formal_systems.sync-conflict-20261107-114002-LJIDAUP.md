---
title: 'From Logic to Formal Systems: Foundations, Methods, and Applications'
date: 2026-10-29 16:00:00
tags: ["Mathematics"]
draft: True
---

{{< info "Info" >}}
This is a summary of the lecture [Formal Systems](https://formal.kastel.kit.edu/teaching/FormSysWS2627/) at the KIT, it was created through the lectures slides and lecture script and can be seen more as a dirty translation.
{{< /info >}}

## 1. Introduction 

TBD: Why this article? 

## 2. Propositional Logic: Syntax and Semantics

### 2.1 Introductory Problem

The lecture opens with two puzzles that show what propositional logic is good for: stating combinatorial problems as *satisfiability problems*.

{{< img src="/attachments/" width="60%" >}}

**Sudoku.** For every cell position \((i,j)\) and every digit \(k\) with \(1 \leq k \leq 9\), introduce a Boolean variable \(D^k_{i,j}\) that is true exactly when the cell \((i,j)\) holds the digit \(k\). The rules of Sudoku then become formulas:

- \(D^1_{1,1} \vee D^1_{1,2} \vee \dots \vee D^1_{1,9}\) says the digit 1 must appear at least once in the first row. The corresponding formulas cover every digit in every row, column, and \(3 \times 3\) region.
- \(\neg(D^s_{i,j} \wedge D^t_{i,j})\) for all \(1 \leq i,j,s,t \leq 9\) with \(s < t\) says a cell holds at most one digit. That is \(81 \cdot 36 = 2916\) formulas.

In total the puzzle needs \(2916 + 3 \cdot 81 = 3159\) formulas. A solution is an assignment of truth values to all variables that makes every formula true.

{{< img src="/attachments/" width="60%" >}}

**The Eight Queens Problem.** Place eight queens on a chessboard so that no queen threatens another. One Boolean variable \(D_{i,j}\) per square, true when a queen stands there. For each square \((i,j)\), a formula \(FE_{i,j}\) expresses that a queen there excludes every other square in its row, column, and both diagonals, for example:

$$D_{1,1} \rightarrow \neg D_{1,2} \wedge \neg D_{1,3} \wedge \dots \wedge \neg D_{1,8}$$

and analogously for the column and the diagonals. The formulas \(R_k = D_{1,k} \vee D_{2,k} \vee \dots \vee D_{8,k}\) for \(1 \leq k \leq 8\) force at least one queen per row. A solution is again an interpretation that makes all these formulas true. The problem has 92 solutions, or 12 if symmetric ones are counted only once.

### 2.2 Syntax

We begin with symbols from which propositional logic is build.

{{< definition number="2.1" name="Logical Symbols" >}}
|  Symbols | Meaning |
|---|---|
| \(1\) | symbol for the truth value "true" |
| \(0\) | symbol for the truth value "false" |
| \(\neg\) | negation symbol ("not") |
| \(\wedge\) | conjunction symbol ("and") |
| \(\vee\) | disjunction symbol ("or") |
| \(\rightarrow\) | implication symbol ("if \(\dots\) then", "implies") |
| \(\leftrightarrow\) | symbol for implication in both directions ("if and only if") |
| \((,)\) | the two parentheses |
{{< /definition >}}

The symbols \(\neg\), \(\wedge\), \(\vee\), \(\rightarrow\), and \(\leftrightarrow\) are called Boolean or propositional operators, and \(1\), \(0\) Boolean constants.

The logical symbols occur in every propositional logic. The second category of symbols is the signature.

{{< definition number="2.2" name="Signature" >}}
A (propositional) *signature* is a countable set \(\Sigma\) of symbols, for example

$$\Sigma = \{P_0, \dots, P_n\}$$

or

$$\Sigma = \{P_0, P_1, \dots\}.$$

The elements of \(\Sigma\) are also called *atomic statements*, *atoms*, or *propositional variables*.
{{< /definition >}}

Only the choice of a signature turns the logical symbols into a concrete propositional language.

{{< definition number="2.3" name="Propositional Formulas" >}}
With a signature \(\Sigma\), the set \(For_0^\Sigma\) of all formulas over \(\Sigma\) is defined inductively by:

1. \(1, 0 \in For_0^\Sigma\) and \(\Sigma \subseteq For_0^\Sigma\).
2. If \(A, B\) are elements of \(For_0^\Sigma\), then so are \(\neg A\), \((A \wedge B)\), \((A \vee B)\), \((A \rightarrow B)\), \((A \leftrightarrow B)\).
{{< /definition >}}

### 2.3 Semantic 

Syntactically, formulas are meaningless strings. The semantics fixes what they mean: a formula is read as a statement that is true or false.

{{< definition name="Interpretation" >}}
Let \(\Sigma\) be a propositional signature. An *interpretation* over \(\Sigma\) is an arbitrary mapping

$$I : \Sigma \rightarrow \{W, F\}.$$
{{< /definition >}}

Here \(W\) and \(F\) denote the truth values true and false.

{{< definition name="Valuation" >}}
For every \(I\) over \(\Sigma\), an associated evaluation of the formulas over \(\Sigma\) is defined:

$$val_I : For_0^\Sigma \rightarrow \{W, F\}$$

with:

- \(val_I(1) = W\)
- \(val_I(0) = F\)
- \(val_I(P) = I(P)\) for every \(P \in \Sigma\)
{{< /definition >}}

**Example 2.10.** Let \(\Sigma = \{P, Q, R\}\). We compute \(val_I((P \wedge \neg R) \rightarrow \neg(R \vee Q))\) for the interpretation \(I\) with \(I(P) = W\), \(I(Q) = F\), \(I(R) = W\). For easier follow-up, the table includes the evaluation of all subformulas.

{{< table "latex_table" >}}
| Value | Subformula |
|---|---|
| W | \(I(P)\) |
| F | \(I(Q)\) |
| W | \(I(R)\) |
| F | \(val_I(\neg R)\) |
| F | \(val_I(P \wedge \neg R)\) |
| W | \(val_I(R \vee Q)\) |
| F | \(val_I(\neg(R \vee Q))\) |
| W | \(val_I((P \wedge \neg R) \rightarrow \neg(R \vee Q))\) |
{{< /table >}}

### 2.4 Logical Inference

{{< definition number="2.16" name="Model" >}}
An interpretation \(I\) with \(val_I(A) = W\) for a formula \(A \in For_0^\Sigma\) is called a *model* of \(A\). For a set of formulas \(M \subseteq For_0^\Sigma\), a model of \(M\) is an interpretation \(I\) that is a model of every \(A \in M\).
{{< /definition >}}

Note that the empty set has every interpretation as a model.

{{< definition number="2.17" name="Logical Consequence" >}}
Let \(\Sigma\) be a signature, \(M \subseteq For_0^\Sigma\), and \(A \in For_0^\Sigma\). \(A\) is called a *logical consequence* of \(M\), in symbols \(M \models A\), exactly when every model of \(M\) is also a model of \(A\).

Instead of \(\emptyset \models A\) we write \(\models A\); instead of \(\{B\} \models A\) we write \(B \models A\).
{{< /definition >}}

{{< definition number="2.18" name="Validity and Satisfiability" >}}
Let \(A \in For_0^\Sigma\) and \(M \subseteq For_0^\Sigma\).

- \(A\) is called *valid* iff \(\models A\), that is, \(val_I(A) = W\) for every interpretation \(I\).
- \(A\) is called *satisfiable* iff there is an interpretation \(I\) with \(val_I(A) = W\).
- \(M\) is called *satisfiable* iff there is an interpretation \(I\) with \(val_I(B) = W\) for all \(B \in M\).
{{< /definition >}}

Valid formulas are also called *tautologies*. 

**Example.** The difference is about how many situations make a formula true, where a situation is one complete assignment of truth values to all atoms. \(P \wedge Q\) is satisfiable: it holds in the situation with \(P\) and \(Q\) both true, and one such situation is enough. \(P \wedge \neg P\) is not satisfiable: no assignment makes it true. \(P \vee \neg P\) is valid: whichever value \(P\) takes, one disjunct holds. The two notions are directly connected: \(A\) is valid exactly when \(\neg A\) is unsatisfiable. 

Questions of logical consequence can be reduced to questions of validity:

{{< definition kind="Theorem" >}}
- \(A\)G is satisfiable iff \(\neg A\) is not valid.
- \(A\) is valid iff \(\neg A\) is not satisfiable.
- \(\models \neg A\) iff \(A\) is unsatisfiable.
- \(A \models B\) iff \(\models A \rightarrow B\).
- \(M \cup \{A\} \models B\) iff \(M \models A \rightarrow B\).
- \(A\) and \(B\) are logically equivalent iff \(A \leftrightarrow B\) is valid.
{{< /definition >}}

**Example.** The following formulas are valid:

{{< table "latex_table" >}}
| Formula | Name |
|---|---|
| \(A \rightarrow A\) | self-implication |
| \(\neg A \vee A\) | tertium non datur |
| \(A \rightarrow (B \rightarrow A)\) | weakening |
| \(0 \rightarrow A\) | ex falso quodlibet |
| \((A \wedge (A \rightarrow B)) \rightarrow B\) | modus ponens |
| \(A \wedge A \leftrightarrow A\) | idempotence |
| \(\neg\neg A \leftrightarrow A\) | double negation |
{{< /table >}}

{{< definition number="2.11" name="Boolean Function" >}}
A Boolean function is a function from \(\{W, F\}^n\) to \(\{W, F\}\) for some \(n \in \mathbb{N}\).

One can also read a propositional formula as a notation for a Boolean function. This view is at home in computer engineering.
{{< /definition >}}

{{< definition number="2.12" name="Boolean Function of a Formula" >}}
Let \(A \in For_0^\Sigma\). To explain the Boolean function \(f_A\) assigned to \(A\), one first needs an assignment of the argument positions of \(f_A\) to the propositional atoms in \(\Sigma\). Here we assume \(\Sigma = \{P_1, \dots, P_n\}\) and assign the \(i\)-th argument position of \(f_A\) to the atom \(P_i\). For every argument \(\bar{b} \in \{W, F\}^n\) we set

$$f_A(\bar{b}) = val_I(A)$$

where \(I(P_i) = \bar{b}[i]\) for all \(1 \leq i \leq n\).
{{< /definition >}}

**Example.** For \(A = P_1 \wedge P_3\) in the signature \(\Sigma = \{P_1, P_2, P_3\}\), \(f_A\) results from the following table:

{{< table "latex_table" >}}
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

{{< definition kind="Lemma" number="2.14" name="Functional Completeness" >}}
For every \(n \in \mathbb{N}\) and every Boolean function \(f : \{W, F\}^n \rightarrow \{W, F\}\) there is a formula \(A \in For_0^\Sigma\), for \(\Sigma = \{P_1, \dots, P_n\}\), with

$$f_A = f.$$
{{< /definition >}}

**Remark.** The lemma says that formulas can compute every Boolean function. A Boolean function is just a table of W and F entries, and most such tables have no obvious formula behind them. The lemma asserts that for any table there is nonetheless a formula \(A\) whose truth table is exactly that one, \(f_A = f\). The language of Definition 2.1 therefore covers the entire supply of Boolean functions, which is what "functional completeness" means. Concretely, for any table one can build such a formula: for every row ending in W, write the conjunction of the literals matching that row (\(P_i\) for W, \(\neg P_i\) for F), then join these conjunctions with \(\vee\). Completeness depends on the operators available: \(\{\neg, \wedge\}\) still suffices, \(\{\wedge, \vee\}\) does not.


### 2.5 Basis 


The propositional constants and operators chosen in Definition 2.3, namely \(1\), \(0\), \(\neg\), \(\wedge\), \(\vee\), \(\rightarrow\), \(\leftrightarrow\), are highly redundant. For instance, one can get by with the operators \(\neg\) and \(\wedge\) alone. That is, formulas of the form \(1\), \(0\), \(A \vee B\), \(A \rightarrow B\), and \(A \leftrightarrow B\) can be replaced by formulas with the same Boolean function that are built only from \(\neg\) and \(\wedge\), as follows:

{{< table "latex_table" >}}
| Formula | Replacement |
|---|---|
| \(0\) | \(P_0 \wedge \neg P_0\) |
| \(A \vee B\) | \(\neg(\neg A \wedge \neg B)\) |
| \(1\) | \(\neg(P_0 \wedge \neg P_0)\) |
| \(A \rightarrow B\) | \(\neg A \vee B\) |
| \(A \leftrightarrow B\) | \((A \rightarrow B) \wedge (B \rightarrow A)\) |
{{< /table >}}

In this table, each row already makes use of the replacements established in the rows above it.

{{< definition number="2.15" name="Basis" >}}
A set \(K_{\mathrm{Op}}\) of propositional constants and operators such that for every Boolean function \(f : \{W, F\}^n \rightarrow \{W, F\}\) there exists a formula \(A\) built only from constants and operators in \(K_{\mathrm{Op}}\) with \(f_A = f\), is called a (propositional) *basis*.
{{< /definition >}}

So far we have met the bases \(\{1, 0, \neg, \wedge, \vee, \rightarrow, \leftrightarrow\}\) and \(\{\neg, \wedge\}\). Another basis is \(\{0, \rightarrow\}\), as the following replacements show:

{{< table "latex_table" >}}
| Formula | Replacement |
|---|---|
| \(\neg A\) | \(A \rightarrow 0\) |
| \(A \vee B\) | \(\neg A \rightarrow B\) |
| \(1\) | \(0 \rightarrow 0\) |
| \(A \wedge B\) | \(\neg(\neg A \vee \neg B)\) |
| \(A \leftrightarrow B\) | \((A \rightarrow B) \wedge (B \rightarrow A)\) |
{{< /table >}}

There are also propositional bases consisting of a single operation. An example is the operation \(\downarrow\), defined by the following truth table:

{{< table "latex_table" >}}
| \(val_I(A)\) | \(val_I(B)\) | \(val_I(A \downarrow B)\) |
|---|---|---|
| W | W | F |
| W | F | F |
| F | W | F |
| F | F | W |
{{< /table >}}

The truth profile of \(A \downarrow B\) coincides with that of the formula \(\neg(A \vee B)\), which is often written \(A\ \mathrm{NOR}\ B\). The functional completeness of the one-element operator set \(\{\downarrow\}\) follows from the translation table:

{{< table "latex_table" >}}
| Formula | Replacement |
|---|---|
| \(\neg A\) | \(A \downarrow A\) |
| \(A \wedge B\) | \(\neg A \downarrow \neg B\), that is \((A \downarrow A) \downarrow (B \downarrow B)\) |
{{< /table >}}

The rest follows, since we already know that \(\{\neg, \wedge\}\) is a basis.

### 2.6 Interpolation 

The study of interpolants, for both propositional logic and predicate logic, is part of the standard repertoire of theoretical logic.

{{< definition number="2.25" name="Interpolant" >}}
Let \(A, B\) be propositional formulas such that \(A \rightarrow B\) is a tautology. A formula \(C\) is called an *interpolant* of \(A \rightarrow B\) if:

1. \(A \rightarrow C\) and \(C \rightarrow B\) are tautologies, and
2. \(C\) contains only such propositional atoms \(P \in \Sigma\) that occur both in \(A\) and in \(B\).

Because of (22) in Table 2.3.4, we can assume that \(1\) and \(0\) do not occur in \(C\).
{{< /definition >}}

{{< definition kind="Lemma" number="2.26" name="Craig's Interpolation Lemma" >}}
For any two propositional formulas \(A, B\) such that \(A \rightarrow B\) is a tautology, an interpolant exists.
{{< /definition >}}

**Example.** \(P_1 \wedge P_2 \rightarrow P_1 \vee P_3\) is a tautology.

- Likewise \(P_1 \wedge P_2 \rightarrow P_1\).
- Likewise \(P_1 \rightarrow P_1 \vee P_3\).
- Therefore: \(P_1\) is an interpolant for \(P_1 \wedge P_2 \rightarrow P_1 \vee P_3\).


{{< definition number="2.25" name="Cosntrutction" >}}
**Interpolation Lemma: Construction.** Let \(P_1, \dots, P_n\) be all the propositional atoms occurring in \(A\) that do not occur in \(B\). For constants \(c_i \in \{1, 0\}\), let \(A[c_1, \dots, c_n]\) denote the formula that results from \(A\) by replacing \(P_i\) with \(c_i\) for all \(1 \leq i \leq n\). We set

$$C \equiv \bigvee_{(c_1, \dots, c_n) \in \{1, 0\}^n} A[c_1, \dots, c_n]$$

{{< /definition >}}

**Example.** Simple example for the construction of \(C\):

- Consider the tautology \(A \rightarrow B\) with \(A = P_1 \wedge P_2\), \(B = P_1 \vee P_3\).
- \(P_2\) is the only atom that occurs in \(A\) but not in \(B\).
- \(A[1] = P_1 \wedge 1 \equiv P_1\)
- \(A[0] = P_1 \wedge 0 \equiv 0\)
- \(C = A[1] \vee A[0] \equiv P_1 \vee 0 \equiv P_1\)

**Example.** Another example for the construction of \(C\):

- \(A \rightarrow B\) with \(A = (P_1 \vee \neg P_2) \wedge (\neg P_1 \vee \neg P_3) \wedge P_2\) and \(B = \neg((\neg P_2 \vee P_3) \wedge (P_2 \vee P_4) \wedge \neg P_4)\).
- \(A \equiv P_1 \wedge P_2 \wedge \neg P_3\) and \(B \equiv \neg P_2 \vee \neg P_3 \vee P_4\).
- \(A \rightarrow B\) is a tautology.
- \(P_1\) is the only atom in \(A\) and not in \(B\).
- \(A[1] = (1 \vee \neg P_2) \wedge (\neg 1 \vee \neg P_3) \wedge P_2 \equiv 1 \wedge \neg P_3 \wedge P_2 \equiv \neg P_3 \wedge P_2\)
- \(A[0] = (0 \vee \neg P_2) \wedge (\neg 0 \vee \neg P_3) \wedge P_2 \equiv \neg P_2 \wedge 1 \wedge P_2 \equiv 0\)
- Therefore \(C = (\neg P_3 \wedge P_2) \vee 0 \equiv \neg P_3 \wedge P_2\) is an interpolant for \(A \rightarrow B\).

**Application: model checking.** Interpolants are used in SAT-based model checking, notably by K.L. McMillan in "Interpolation and SAT-Based Model Checking" (CAV 2003), to compute an inductive invariant over an abstracted state space. There the interpolant \(P\) of two mutually inconsistent formulas \(A\) and \(B\) is characterized by three properties: \(A \rightarrow P\), \(P \wedge B\) is unsatisfiable, and \(P\) only uses variables that occur in both \(A\) and \(B\).

### 2.7 Normal Forms 

{{< definition number="2.32" name="Conjunctive and Disjunctive Normal Form" >}}
1. A *literal* is an atom or a negated atom.
2. A formula is in *disjunctive normal form* (DNF) if it is a disjunction of conjunctions of literals.
3. A formula is in *conjunctive normal form* (CNF) if it is a conjunction of disjunctions of literals.
{{< /definition >}}

{{< definition kind="Lemma" number="2.33" >}}
1. For every propositional formula \(A\) there is a logically equivalent formula in disjunctive normal form and likewise a logically equivalent formula in conjunctive normal form.
2. The algorithms for producing both normal forms follow immediately from elementary tautologies.
3. If the truth table of a formula is given, the disjunctive and conjunctive normal forms can be read off from it "directly".
{{< /definition >}}

**Remark.** 1. The satisfiability of a formula in DNF and 2. the validity of a formula in CNF can be checked in polynomial time. (The "reverse" problems, e.g. satisfiability of CNF, are much harder!)

{{< definition number="2.34" name="Complete Normal Form" >}}
1. A disjunctive normal form \(D = \bigvee_{K \in \mathcal{K}} K\) in the signature \(\Sigma\) is called *complete* if for every \(P \in \Sigma\), in every clause \(K \in \mathcal{K}\) one of the literals \(P\) or \(\neg P\) occurs in \(K\).
2. Complete normal forms are unique up to reordering.
{{< /definition >}}

{{< definition number="2.36" name="Minimal Normal Form" >}}
1. A disjunctive normal form \(D = \bigvee_{K \in \mathcal{K}} K\) is called *minimal* if every shorter formula \(D'\) is not equivalent to \(D\). \(D' = \bigvee_{K' \in \mathcal{K}'} K'\) is *shorter* than \(D\) if for every \(K' \in \mathcal{K}'\) there exists a \(K \in \mathcal{K}\) such that \(K'\) is a subformula of \(K\).
2. Minimal disjunctive and conjunctive normal forms of a formula are not unique.
{{< /definition >}}

**Example 2.40.** To see how fast a CNF can grow, consider

$$A_n = (P_{1,1} \wedge P_{1,2}) \vee \dots \vee (P_{n,1} \wedge P_{n,2}).$$

Think of the pairs \((P_{i,1}, P_{i,2})\) as \(n\) groups of two atoms each. \(A_n\) is true exactly when in at least one group both atoms are true. It is false exactly when in *every* group at least one atom is false, that is, when one literal per group can be picked such that all picked literals are false under the interpretation.

The conjunctive normal form of \(A_n\) is:

$$\bigwedge \{\, P_{1,f(1)} \vee \dots \vee P_{n,f(n)} \;|\; f : \{1, \dots, n\} \rightarrow \{1, 2\} \,\}.$$

Each clause corresponds to one way \(f\) of picking one literal from every group. Such a clause evaluates to F exactly when all its picked literals are false, which happens precisely under the interpretations that make \(A_n\) false: given such an interpretation, pick \(f(i)\) as a false literal in group \(i\), and the clause for \(f\) is falsified. So each clause rules out one of these "one false per group" patterns, and together the clauses rule out all of them, making the conjunction equivalent to \(A_n\).

For \(n = 3\) this is:

$$\begin{aligned}
&(P_{1,1} \vee P_{2,1} \vee P_{3,1}) \wedge (P_{1,1} \vee P_{2,1} \vee P_{3,2}) \wedge
(P_{1,1} \vee P_{2,2} \vee P_{3,1}) \wedge (P_{1,1} \vee P_{2,2} \vee P_{3,2}) \\
&\wedge (P_{1,2} \vee P_{2,1} \vee P_{3,1}) \wedge (P_{1,2} \vee P_{2,1} \vee P_{3,2}) \wedge
(P_{1,2} \vee P_{2,2} \vee P_{3,1}) \wedge (P_{1,2} \vee P_{2,2} \vee P_{3,2})
\end{aligned}$$

The point of the example: \(A_n\) contains \(2n\) literals, but its CNF contains \(n \cdot 2^n\) — there is one clause per choice function \(f\), and there are \(2^n\) of those. The distribution laws used to convert a formula into CNF can therefore blow the formula up exponentially.

**Short CNF: goal.** Find a construction of a formula in CNF that does not grow exponentially. This CNF cannot always be equivalent to the original formula. But it is equivalent with respect to one important property (more on this later).

**Construction of the short CNF.**

1. Introduce an abbreviation (a new atom) for every subformula whose top-level operator is binary.
2. For each of these abbreviations, state the definition according to the corresponding subformula, taking into account "deeper" abbreviations.
3. Resolve the equivalences in the definitions.
4. Convert the definitions into CNF.

The conjunction of the definitions together with the top-level abbreviation is the short CNF.

**Example.** Compute the short CNF for the following formula, which is equivalent to \(A_3\) from the previous example:

$$\neg((\neg P_{1,1} \vee \neg P_{1,2}) \wedge (\neg P_{2,1} \vee \neg P_{2,2}) \wedge (\neg P_{3,1} \vee \neg P_{3,2}))$$

Steps 1 and 2 introduce one abbreviation per binary subformula, from the inside out:

$$\begin{aligned}
&Q_1 \leftrightarrow \neg P_{1,1} \vee \neg P_{1,2} \qquad
Q_2 \leftrightarrow \neg P_{2,1} \vee \neg P_{2,2} \qquad
Q_3 \leftrightarrow \neg P_{3,1} \vee \neg P_{3,2} \\
&Q_4 \leftrightarrow Q_1 \wedge Q_2 \qquad Q_5 \leftrightarrow Q_4 \wedge Q_3
\end{aligned}$$

plus the top-level unit \(\neg Q_5\).

Step 3 resolves each equivalence \(Q \leftrightarrow F\) into the two halves \(\neg Q \vee F\) and \(Q \vee \neg F\):

$$\begin{aligned}
&\neg Q_1 \vee \neg P_{1,1} \vee \neg P_{1,2} \qquad Q_1 \vee (P_{1,1} \wedge P_{1,2}) \\
&\neg Q_2 \vee \neg P_{2,1} \vee \neg P_{2,2} \qquad Q_2 \vee (P_{2,1} \wedge P_{2,2}) \\
&\neg Q_3 \vee \neg P_{3,1} \vee \neg P_{3,2} \qquad Q_3 \vee (P_{3,1} \wedge P_{3,2}) \\
&\neg Q_4 \vee (Q_1 \wedge Q_2) \qquad\qquad\;\; Q_4 \vee \neg Q_1 \vee \neg Q_2 \\
&\neg Q_5 \vee (Q_4 \wedge Q_3) \qquad\qquad\;\; Q_5 \vee \neg Q_4 \vee \neg Q_3 \\
&\neg Q_5
\end{aligned}$$

Step 4 distributes the remaining conjunctions into CNF:

$$\begin{aligned}
&\neg Q_1 \vee \neg P_{1,1} \vee \neg P_{1,2} \qquad (Q_1 \vee P_{1,1}) \wedge (Q_1 \vee P_{1,2}) \\
&\neg Q_2 \vee \neg P_{2,1} \vee \neg P_{2,2} \qquad (Q_2 \vee P_{2,1}) \wedge (Q_2 \vee P_{2,2}) \\
&\neg Q_3 \vee \neg P_{3,1} \vee \neg P_{3,2} \qquad (Q_3 \vee P_{3,1}) \wedge (Q_3 \vee P_{3,2}) \\
&(\neg Q_4 \vee Q_1) \wedge (\neg Q_4 \vee Q_2) \qquad Q_4 \vee \neg Q_1 \vee \neg Q_2 \\
&(\neg Q_5 \vee Q_4) \wedge (\neg Q_5 \vee Q_3) \qquad Q_5 \vee \neg Q_4 \vee \neg Q_3 \\
&\neg Q_5
\end{aligned}$$

The CNF of these formulas is satisfiability-equivalent to \(A_3\).

{{< definition kind="Theorem" >}}
For every propositional formula \(A\) with \(n\) literal occurrences there is a conjunctive normal form \(A_{\mathrm{kcnf}}\) such that:

- \(A\) is satisfiable iff \(A_{\mathrm{kcnf}}\) is satisfiable,
- \(A_{\mathrm{kcnf}}\) contains at most \(c \cdot n\) literal occurrences for a constant \(c\) independent of \(n\),
- \(A_{\mathrm{kcnf}}\) can be constructed from \(A\) effectively in polynomial (even linear) time.
{{< /definition >}}

**Note.** Satisfiability-equivalent means \(A\) and \(A_{\mathrm{kcnf}}\) are either both satisfiable or both unsatisfiable, but they are not logically equivalent. They can disagree on individual interpretations, and \(A_{\mathrm{kcnf}}\) may be true under interpretations that assign values to atoms \(A\) does not contain (the new \(Q_i\)). What is preserved is only the answer to the question "does some interpretation make it true?". This is enough in practice: SAT solvers require CNF input, the plain CNF can blow up exponentially (see Example 2.40), while the short CNF stays linear in size. An assignment satisfying \(A_{\mathrm{kcnf}}\) can always be restricted to the original atoms, and that restriction satisfies \(A\), and vice versa. Since questions of validity and logical consequence reduce to satisfiability (\(A\) valid iff \(\neg A\) unsatisfiable, \(A \models B\) iff \(A \wedge \neg B\) unsatisfiable), the short CNF is the format in which SAT solvers actually process these questions.



