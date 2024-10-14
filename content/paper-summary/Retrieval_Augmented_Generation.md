---
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
date: 2024-02-03 10:31:09Z
tags: ["paper-summary"]
---

**Paper Title:** Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks 
**Link to Paper:** https://arxiv.org/abs/2005.11401  
**Date:** 22. May 2020  
**Paper Type:** LLM, knowledge-retrival  
**Short Abstract:**  
Language models (LLMs) have been demonstrated to store knowledge within their parameters. However, updating the model's knowledge requires updating these parameters. This poses challenges. To address this, the paper introduces the Retrieval-Augmented Generation (RAG) model, where knowledge is stored in a non-parametric dense vector database.  

# 1. Introduction

LLMs lack external memory, leading to difficulties in adding or removing knowledge, understanding the model's knowledge, and generating "hallucinations." Hybrid models, combining both parametric and non-parametric storage, can mitigate these issues by allowing direct access to non-parametric knowledge.

The authors present the Retrieval-Augmented Generation (RAG) model, a pre-trained language model based on the seq2seq transformer BART. It incorporates a non-parametric memory, acting as a dense vector index of Wikipedia, accessible via neural retrieval. These components are trained end-to-end, where the retriever identifies documents similar to the prompt, and the found documents, along with the input prompt, are used to generate the output.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/2ac0dedaa0bcc4843293bf3a3f2f4241.png">
</figure>
{{< /rawhtml >}}

Training of the generator and retriever is performed jointly by minimizing log-likelihood using the ADAM optimizer. The document encoder remains frozen, and only the retriever's decoder is updated.

# 3. Experiments

A collection of Wikipedia pages serves as the non-parametric knowledge base for all experiments. The retriever's encoder computes document embeddings once.

Experiments test the RAG model on four different domains:
- **Open-domain Question Answering(QA)** through the benchmarks NaturalQuestion, TriviaQA, WebQuestions and  CuratedTree.
- **Abstractive Question Answering** through the benchmark MSMARCO NLG task v2.1.
- **Jeopardy Question** through the benchmark SearchQA.
- **Fact Verification** through the FEVER benchmark.

# 4. Results

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/0eace9f6bde6444aa37d8111d469817d.png">
</figure>
{{< /rawhtml >}}

RAG achieves a new state-of-the-art in Open-domain Question Answering and Jeopardy, while approaching the state-of-the-art in Abstractive Question Answering and Fact Verification.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/a84caaaab22c129be05584c571b86a19.png">
</figure>
{{< /rawhtml >}}

Additional documents enhance performance up to a certain point, beyond which further additions result in deteriorating results.

# 5. Conclusion

RAG is an intriguing technique that promises to externalize a model's knowledge from its parameters to a non-parametric knowledge database. This is crucial for updating the model's knowledge.
