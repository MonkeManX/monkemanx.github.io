---
title: 'An Interpretation of Kants Work "Grundlegung zur Metaphysik der Sitten"'
date: 2026-04-27 10:00:00
tags: ["Philosophy"]
draft: True
---

{{< info "Info" >}}
This interpretation is not my own but based on a seminar I heard at the University of KIT where this work was treated. Further, the text passages I will cite are in german, mabye I will translate this but probably not.
{{< /info >}}

### Preface

One of the first things that we get in the preface is a strcuture of the different fields of philsophy like kant envions thems

```mermaid
flowchart TD
    A["Knowledge"]

    A --> B["formal<br/>concerns itself with the form of understanding,<br/>with knowledge itself, and the general rules of thinking"]
    A --> C["material<br/>concerns itself with objects;<br/>has object(s) as its content"]

    %% Formal branch
    B --> D["Logic<br/>philosophia rationalis<br/>Laws of thought"]
    D --> D1["a priori"]

    %% Material branch
    C --> E["Physics (Natural Philosophy)<br/>philosophia naturalis<br/>Laws of nature"]
    C --> F["Ethics (Moral Philosophy)<br/>philosophia moralis<br/>Laws of freedom"]

    %% Physics sub-branches
    E --> E1["a priori<br/>Metaphysics of nature"]
    E --> E2["empirical<br/>Actual physics"]

    %% Ethics sub-branches
    F --> F1["a priori<br/>Metaphysics of morals"]
    F --> F2["empirical<br/>Practical anthropology"]

    %% Works (Physics side)
    E1 --> G["Critique of Pure Reason"]
    E1 --> G1["Prolegomena to Any Future Metaphysics"]
    E1 --> G2["Metaphysical Foundations of Natural Science"]

    %% Works (Ethics side)
    F1 --> H["Groundwork of the Metaphysics of Morals"]
    F1 --> H2["Metaphysics of Morals"]

```

And as we can see the work which this article is about can be categorized to the Ethical purely a priori branch. This categorication is not new and is alreday done similar with aristotele, what is new is how kant talks about these branches as laws.

The next passages highlight this:

> ob man nicht meine, daß es von der **äußersten Notwendigkeit** sei, einmal eine reine Moralphilosophie zu bearbeiten, die von allem, was nur empirisch sein mag und zur Anthropologie gehört, völlig gesäubert wäre; denn, daß es eine solche geben müsse, leuchtet von selbst aus der gemeinen Idee der Pflicht und der sittlichen Gesetze ein. Jedermann muß eingestehen, daß ein Gesetz, wenn es moralisch, d.i. als Grund einer Verbindlichkeit, gelten soll, **absolute Notwendigkeit** bei sich führen müsse;

When Kant talks about morlaity he mean laws, that are nessecarily and a priori true and not jsut practical rules that one does because they are beneficial, they are not contingent on us humans i.e. they are not ruels unqiue to us human but apply to all being with rationality.

> daß mithin der **Grund der Verbindlichkeit** hier nicht in der Natur des Menschen oder den Umständen in der Welt, darin er gesetzt ist, gesucht werden müsse, sondern **a priori** lediglich in Begriffen der reinen Vernunft,

Anf furtehr every other rule is can maybe called a pratical rule but never a moral law. Morlaity needs nessecaity, withotu nessecarity we do not have a moral law.

> **daß jede andere Vorschrift**, die sich auf Prinzipien der bloßen Erfahrung gründet, und sogar eine in gewissem Betracht allgemeine Vorschrift, so fern sie sich dem mindesten Teile, vielleicht nur einem Bewegungsgrunde nach, auf empirische Gründe stützt, **zwar eine praktische Regel, niemals aber ein moralisches Gesetz heißen kann**.

Hence the argument in the preface goes in very short as follows:
1. Morality is connected with lawfulness.
2. Laws hold (in contrast to regularities) with necessity.
3. Necessity can only be recognized a priori.
4. The discipline that proceeds purely a priori is called metaphysics.
5. Therefore, a “metaphysics of morals” is necessarily required.

> **Eine Metaphysik der Sitten ist also unentbehrlich notwendig**, nicht bloß aus einem Bewegungsgrunde der Spekulation, um die Quelle der a priori in unserer Vernunft liegenden praktischen Grundsätze zu erforschen, sondern **weil die Sitten selber allerlei Verderbnis unterworfen bleiben, so lange jener Leitfaden und oberste Norm ihrer richtigen Beurteilung fehlt.** Denn bei dem, was moralisch gut sein soll, ist es nicht genug, daß es dem sittlichen Gesetze gemäß sei, sondern es muß auch um desselben willen geschehen; widrigenfalls ist jene Gemäßheit nur sehr zufällig und mißlich, weil der unsittliche Grund zwar dann und wann gesetzmäßige, mehrmalen aber gesetzwidrige Handlungen hervorbringen wird. **Nun ist aber das sittliche Gesetz in seiner Reinigkeit und Echtheit (woran eben im Praktischen am meisten gelegen ist) nirgend anders als in einer reinen Philosophie zu suchen, also muß diese (Metaphysik) vorangehen, und ohne sie kann es überall keine Moralphilosophie geben;**

### Structure of the Work

The Grundlegung zur Metaphysik der Sitten" is structured in multiple sections:
1. Preface
2. Common moral rational knowledge -> Philosophical moral knowledge
3. Popular moral philosophy -> Metaphysics of Morals
4. Metaphysics of Morals → Critique of Practical Reason

It is important to know the purpose of the each section. The preface gives an overview of the field of philsophy and place thsi work inside it, further it desicbes the strcuture of kants work and what his goal is.
Next The second and thrid section are both seciton with the goal of ivnestiation the highest law of morality, by starting at soemwhere and then deriving this law, but both ection start with a differnet entry poind, the seocnd section starts with the common moral udnerstanding of the common man and tries do deive the highest law, whiel the thrid seciton start mroe philsophical with more rigor for ma philsophcia lview point. both sction can be seen at different attemt usign different routes to derives the hgihest law, the secodn section is more appraochable for the common man, whiel the htrid is mroe philsophcial rigorious.
In the last section, after he has derived the heighest aklw i nthe preivous seciton he now needs to show that this law is not innert btu actual is active and exist this is the goal of this section.

```mermaid
flowchart LR

    B
    D

    subgraph GMS_III["Festsetzung"]
		n1["GMS III"]
        direction LR
        E["Metaphysik der Sitten<br/>Metaphysics of Morals"] --> F["Kritik der praktischen Vernunft<br/>Critique of Practical Reason"]
    end

    style GMS_III fill:#FFEBEE,stroke:#C62828,stroke-width:2px
	GMS_III
	Aufsuchung
	A
	GMS_I --- A
	B
	GMS_I
	C
	GMS_II --- C
    subgraph "Aufsuchung"
		GMS_II["GMS II"]
		GMS_I["GMS I"]
        direction TB
        A["Gemeine sittliche Vernunfterkenntnis<br/>Common Moral Rational Cognition"] --> B["Philosophische sittliche Vernunfterkenntnis<br/>Philosophical Moral Rational Cognition"]
        C["Populäre sittliche Weltweisheit<br/>Popular Moral Wisdom"] --> D["Metaphysik der Sitten<br/>Metaphysics of Morals"]
    end
	style C color:#000000,fill:#7ED957
	style GMS_II fill:#7ED957
	style D color:#000000,fill:#7ED957
	style Aufsuchung fill:#D9D9D9
	style E fill:#FFDE59
	style F fill:#FFDE59
	E
	n1 --- E
	style n1 fill:#FFDE59
```

### 1. Section

### 2. Section
