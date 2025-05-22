---
title: 'SoK: Science, Security and the Elusive Goal of Security as a Scientific Pursuit'
date: 2024-12-06
tags: ["paper-summary", "InfoSec", "philosophy"]
---

**Paper Title:** SoK: Science, Security and the Elusive Goal of Security as a Scientific Pursuit  
**Link to Paper:** https://ieeexplore.ieee.org/document/7958573  
**Date:** 26 May 2017  
**Paper Type:** Review, Philosophy of Science, Definition of InfoSec, History of security  
**Short Abstract:**    
In our ever-increasing digital world, the security of information systems is of utmost importance. But how do we define security? This paper provides an overview of the historical definition of security and the problems associated with it.


## 1. Introduction and Overview

The field of security faces many challenges, such as:  
- Difficulty in measuring progress  
- The presence of active adversaries  

In this paper, the authors review both the history and philosophy of the science of security.  

They find that aspects from the philosophy of science can be applied to the field of security.  


## 2. History of Philosophy of Science

### 2.1 Separation of Deductive and Inductive Statements

Inductive and deductive statements constitute different types of knowledge claims.  
Induction involves drawing conclusions from empirical data, while deduction proves claims based on axioms.  

For example, from many observed data points, we may infer rules. However, these rules can be invalidated if further data contradicts them. In contrast, deductive reasoning is always true when derived correctly from its premises.

Historically, Plato distinguished between the "messy" physical realm and the idealized world of forms, a concept that has heavily influenced Western thought.  
Kant further categorized statements as either *a priori* (independent of experience) or *a posteriori* (dependent on observation).  

The logical positivists later differentiated between *analytic* and *synthetic* propositions. An *analytic* proposition’s truth follows directly from its premises and is associated with *deductive* statements. In contrast, the truth of a *synthetic* proposition depends on the relationship between its meaning and the real world, aligning it with *inductive* statements.

#### Hume’s Problem of Induction

A key question arises: when can we rely on inductive statements?  
Hume's "Problem of Induction" highlights the weakness of the logical basis for believing in inductive statements compared to deduction. No amount of evidence can establish the universal truth of a generalization—for example, the observation that all swans are white does not guarantee that we will not encounter a black swan in the future.  

#### The Rise of Empirical Science

With the rise of empirical science, beginning with figures like Galileo, inductive reasoning gained prominence. Bacon formalized an inductive method of generalization—an early form of the scientific method—in contrast to classical deductive approaches, such as those of Aristotle.  

While Plato argued that observable phenomena were mere shadows of a perfect world of forms, Mill took the opposite stance. He asserted that induction is our only path to understanding the world since deduction cannot independently discover new knowledge about it.

#### Deduction and Its Limitations

A.J. Ayer emphasized:  
> The characteristic mark of a purely logical inquiry is  
> that it is concerned with the formal consequences of  
> our definitions and not with questions of empirical fact.  

This distinction is now well-established. Serious scientists do not claim to deduce truths about the world that are not already implicit in their assumptions. As Medawar famously wrote:  
> Deduction in itself is quite powerless as a method of  
> scientific discovery—and for this very simple reason:  
> the process of deduction as such only uncovers,  
> brings out into the open, makes explicit, information  
> that is already present in the axioms or premises  
> from which the process of deduction began.  

Deduction cannot lead to *new* facts because axioms and definitions do not constitute real-world facts. However, deduction that starts from inductive inferences—such as Newton’s laws—can explore the implications of those inferences in the real world.  


### 2.2 Falsification as a Criterion for Scientific Theories  

Deduction does not provide reliable knowledge of the world, and induction cannot produce general statements that are universally true.  

Karl Popper sought to establish a criterion to distinguish scientific theories from non-scientific ones. Simplified, Popper argued that scientific theories should be falsifiable.  

In other words, a scientific theory must make predictions that can be contradicted by empirical evidence.  

#### Examples of Falsifiability  

Popper criticized theories like Marxism and Freudian analysis, describing them as "too elastic" to be falsifiable. In contrast, Einstein’s theory of relativity is an example of a falsifiable scientific theory because it makes precise predictions that could, in principle, be proven wrong by empirical observations.  

#### Separation of Science from Other Disciplines  

Religion and metaphysical claims are also excluded from scientific theories under Popper’s criterion. Similarly, mathematics is not considered a science in this context because it does not provide direct knowledge about the real world—it deals with abstract structures and logical relationships.  

The less precise a claim, the harder it is to falsify.  

However, not every theory is clearly or straightforwardly falsifiable, leading to ongoing debates about the boundaries of scientific inquiry.  

### 2.3 Relation between Mathematics and Science  

Under the falsification criterion, mathematics is categorized as a non-scientific theory, which may seem counterintuitive.  

However, because mathematical statements cannot be contradicted by observations in the real world, they make no claims about it. For instance, we might think Euclidean geometry describes the physical world, but altering Euclid’s parallel line axiom gives rise to non-Euclidean geometries—each with a plausible claim to describe reality.  

As Ayer explains:  
> Whether a geometry can be applied to the actual  
> physical world or not is an empirical question which  
> falls outside the scope of the geometry itself. There  
> is no sense, therefore, in asking which of the various  
> geometries known to us are false and which are true.  
> Insofar as they are all free from contradiction, they  
> are all true.  

#### Empirical Testing of Mathematical Models  

The validity of a mathematical model’s application to the real world can only be tested empirically. Consequently, statements about the real world derived from deductive systems carry some uncertainty, depending on how well the model aligns with reality.  

When evaluating a mathematical model, its accuracy in representing the real world is key. If there is a conflict between the model and empirical data, the data always prevails.  

In disciplines like economics, direct measurements may be difficult to obtain, which can lead to reliance on alternative forms of validation. However, Friedman reminds us that reasonable assumptions are not a substitute for empirical evidence.  

#### Mathematics in Computer Security  

The origins of computer security lie in World War II cipher code-breaking, grounding the discipline in cryptography and giving it a strong mathematical flavor. Tony Hoare’s work on formal proof of algorithms further cemented this mathematical focus.  

However, real-world programs do not only involve inputs and outputs; they also interact with unpredictable human factors, including adversarial behavior. This complexity highlights the need for more empirical approaches to complement mathematical reasoning in computer security.  

### 2.4 Viewpoints of Major Scientists  

Many philosophers argue that Popper's analysis is incomplete, yet most scientists' education in the philosophy of science often ends with Popper's ideas.  

For instance, Platt advocates that when presenting an observation, we should explicitly state which hypothesis it refutes, and when offering a hypothesis, we should clarify which observations would refute it.  

Despite these critiques, falsification remains a firmly established principle in the philosophy of science.  


### 2.5 Basic Scientific Method  

To qualify as scientific, a theory should possess the following properties:  
- **Consistency**  
- **Falsifiability**  
- **Predictive Power and Progress**  

An inconsistent or unfalsifiable theory provides no new understanding or accurate predictions.  

#### Summary of the Scientific Method  

1. **Formulate a hypothesis** based on observations.  
2. **Develop falsifiable predictions** from the hypothesis.  
3. **Test the hypothesis**: If new observations contradict the theory, reject the hypothesis; if they align, the hypothesis is supported but not proven.  


### 2.6 Science of the Artificial  

Security is distinct from other sciences because it is an interdisciplinary field, incorporating methodologies from diverse domains.  

One notable aspect of security is its focus on computers, which are man-made artifacts. For this reason, Simon refers to security as the *science of the artificial*, emphasizing the creation of artifacts with specific desired properties.  

Simon observes:  
> The natural sciences almost drove the sciences of  
> the artificial from professional school curricula, a  
> development that peaked about two or three decades  
> after the Second World War. Engineering schools  
> gradually became schools of physics and mathematics;  
> medical schools became schools of biological sciences;  
> business schools became schools of finite mathematics ...  
> academic respectability calls for subject matter that is  
> intellectually tough, analytic, formalizable, and teachable.  
> In the past much, if not most, of what we knew about  
> design and the artificial sciences was intellectually soft,  
> intuitive, informal, and cook-booky.  

Security research heavily relies on human-made artifacts, such as specific software or hardware systems. As a result, many findings in security lack the long-term relevance associated with fundamental research in natural sciences, such as physics.  


## 3. History of the Science of Security  

(Refer to the cited paper for details.)  


## 4. Failures to Apply Lessons from Science  

Key lessons from the history and philosophy of science reveal several common shortcomings in the field of security:  

1. **Failure to observe the inductive-deductive split:**  
Both inductive and deductive reasoning have value, but their limitations must be recognized. A frequent error is treating mathematical guarantees as if they reflect properties of real-world systems.  
*Example:* The term *provable security* misleadingly implies real-world assurances.  

2. **Reliance on unfalsifiable claims:**  
Many claims in computer security are not falsifiable. For example, how do we define "secure" or "insecure"? What observations would confirm or refute a system's security?  
*Example:* The lack of a clear criterion to definitively classify a system as secure.  

3. **Failure to bring theory into contact with observation:**  
Scientific models should be judged based on their accuracy when applied to real-world data. Security research often relies on reasonable-sounding assumptions rather than empirical validation.  
*Example:* The assumption that including uppercase letters strengthens passwords—empirical evidence shows this does not significantly enhance security.  

4. **Failure to make claims and assumptions explicit:**  
Theories are only falsifiable if their claims are specific and clear. Ambiguous or implicit assumptions hinder progress.  
*Example:* Advising users to include special symbols in passwords implicitly assumes the use of random passwords, which is often not the case.  

5. **Failure to seek refutation rather than confirmation:**  
The scientific method is most effective when hypotheses are subjected to rigorous testing and potential refutation. Observations should challenge existing beliefs rather than merely confirm them. Generalizations from limited data must also be avoided.  
*Example:* Positive example: Recent research demonstrated that new passwords can often be guessed based on patterns in old ones, offering refutable and actionable insights.  


## 5. Conclusion  

To advance the field of security, it is crucial to precisely define what security entails and to learn from past mistakes as well as insights from the philosophy of science.  
