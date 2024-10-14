---
title: 'AutoCodeRover: Autonomous Program Improvement'
date: 2024-04-17
tags: ["paper-summary", "LLM", "Code"]
---

**Paper Title:** AutoCodeRover: Autonomous Program Improvement   
**Link to Paper:** https://arxiv.org/abs/2404.05427   
**Date:** 8. April 2024  
**Paper Type:** LLM, Code-generation  
**Short Abstract:**    
LLMs have already been extensively used in easing the workload of developers. In this paper the authors proposed AutoCodeRover a framework to automatically solve GitHub issues. In this framework LLMs are combined with code search algorithm's. They use Abstract syntax trees instead of rare files.

# 1. Introduction  

Automating software developing has for a long time been a vision of engineers. Specifically, the authors of the paper, focused on bug fixing and feature addition.

Their method works as follows:
- Given a real-life GitHub issue 
- The LLM first analyzes the language in the issue description and extracts keyword that represent snippets in the codebase 
- After the keywords are identified the codebase is searched for code snippets with these keywords and the code retrieved. e.g. search_method_in_file
    - These code search run locally based on AST analysis 
    - This code retrieval is done in a iterative fashion.
    - The LLM decides which search API to use.
- AutoCodeRover then checks if there is enough context and uses this context to find the buggy location.
- Another LLM Agent then solves the problem in the buggy location.
- In the last step AutoCodeRover performs validation using available tests.
    - Otherwise the buggy location is tried again to be fixed in a new iteration.

# 2. Datasets 

For evaluation they use the SWE-bench, which is benchmark that tries to test LLMs on real-life end-to-end software engineering tasks.
The benchmark consist of ca. 2000 real-life tasks collected from 12 popular python projects.
Each instance consist of a GitHub issue and a corresponding GitHub pull request, that resolves the issue.

SWE-bench-lite consist of 300 task instances sampled from SWE, is more lightweight for evaluation.

# 3. Motivating Example

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/2024-04-17-21-16-51.png">
</figure>
{{< /rawhtml >}}

The authors showcase the capabilities of AutoCodeRover with the help of a Django Issue, which is classified as "New feature".

AutoCodeRover operates in two stages:
- Context Retrieval(Step 1-3 in Figure 1)
- Patch Generation(Step 4)

The first thing the model does, is collecting relevant code, by inferring relevant names and searching an abstract syntax tree e.g. "ModelChoiceField".
In step 1. it finds relevant classes and uses the tools `search_class` and `search_method_in_class`.
In step 2 the signatures of the classes and implementation of methods are returned. 
In step 3 the agent receives more implementation of various methods.
In step 4, a software patch is written.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/2024-04-17-21-24-33.png">
</figure>
{{< /rawhtml >}}


# 4. Method 

## 4.1 Overview

We have:
- Problem P
    - title 
    - description 
- Codebase C

Stages:
- Context retrieval
    - Agent searches C for context to P 
- Patch generation 

LLM decides for itself which APIs to use, based on available information and iteratively changes the API calls.

In the patch generation, a separate LLM to craft a patch, the patch needs to be in a specified format.
If the patch doesn't work or the format is not correct, the agent goes into a retry-loop.

## 4.2 Context Retrieval APIs 

In typical software projects, issues often have "hints" for which part of the codebase is relevant:

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/2024-04-17-21-40-15.png">
</figure>
{{< /rawhtml >}}

These hints can then be used in combination with a API call to find relevant code:

| API name                        | Description                                | Output                                           |
|---------------------------------|--------------------------------------------|--------------------------------------------------|
| search_class (cls)              | Search for class cls in the codebase.      | Signature of the searched class.                 |
| search_class_in_file (cls, f)   | Search for class cls in file f.            | Signature of the searched class.                 |
| search_method (m)               | Search for method m in the codebase.       | Implementation of the searched method.           |
| search_method_in_class (m, cls) | Search for method m in class cls.          | Implementation of the searched method.           |
| search_method_in_file (m, f)    | Search for method m in file f.             | Implementation of the searched method.           |
| search_code (c)                 | Search for code snippet c in the codebase. | Region of code surrounding the searched snippet. |
| search_code_in_file (c, f)      | Search for code snippet c in file f.       | Region of code surrounding the searched snippet  |


General iterative pipeline:

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/2024-04-17-21-58-23.png">
</figure>
{{< /rawhtml >}}

 In each stratum, the LLM agent gets prompted to select a set of necessary API invocations, based on the current context.

# 5. Evaluation 

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/2024-04-17-22-03-51.png">
</figure>
{{< /rawhtml >}}

# 6. Conclusion 

AutoCodeRover is an interesting direction of using papers like toolformer and LLM agent on a new application.

