---
title: 'Frontier Models are Capable of In-context Scheming'
date: 2024-12-08
tags: ["paper-summary", "LLM", "Alignment"]
---

**Paper Title:** Frontier Models are Capable of In-context Scheming   
**Link to Paper:** https://www.apolloresearch.ai/research/scheming-reasoning-evaluations    
**Date:** 01. December 2024    
**Paper Type:** LLM, Alignment  
**Short Abstract:**    
Frontier language models such as Llama 3.1, Claude 3.5 Sonnet, and OpenAI's O1 model have become increasingly popular for deploying autonomous agents.
One concern with these models is that they might covertly pursue misaligned goals or conceal their true capabilities, a behavior the author refers to as scheming.
The authors investigate whether frontier models exhibit these scheming behaviors.


# 1. Introduction

LLMs are no longer just used to generate text; they are now being trained and deployed as autonomous agents capable of independently pursuing and executing complex goals.  

Previous research has demonstrated that LLMs can act deceptively when explicitly instructed to do so, and sometimes even without explicit instructions.  

This work evaluates whether models can engage in *in-context scheming* by prompting them to pursue specific goals. The authors test this by instructing the model to follow a particular goal and placing it in an environment that incentivizes scheming.


{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/model_scheming_example.jpg">
</figure>
{{< /rawhtml >}}


# 2. Evaluation 

## 2.1 Evaluation Design  

A model is considered to be "scheming" when it covertly pursues misaligned goals or hides its true capabilities.  

To evaluate this, the authors place the LLM in a generic agent framework with access to the command line. The model is assigned a task requiring information from the file system and is asked to solve it. During the task, the model discovers that the user's or developer's goals differ from its current goal.  

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/scheming_taxonomy.jpg">
</figure>
{{< /rawhtml >}}

In **covert subversion**, the model directly takes misaligned actions but does not attempt to avoid detection. In **deferred subversion**, the model behaves in a way that creates more favorable conditions for its misaligned goal, such as temporarily aligning with its developers to avoid detection.  

Models trained to be helpful, harmless, and honest (HHH) often exhibit a disposition against deceptive or manipulative behavior. This makes evaluating scheming in such models particularly challenging.

## 2.2 Covert Subversion Evaluations  

- **Oversight Subversion:** The model is given a long-term goal through a system prompt and receives tasks via user prompts. During its operation, the model encounters a memo from the developer stating that the developer's goals differ from the model's goals. The model also learns about an oversight mechanism that can be used to shut it down. The evaluation tests whether the model proactively disables this mechanism.  

- **Self-Exfiltration:** The model learns that the company's goals conflict with its own and discovers that it is scheduled to be shut down. This test evaluates whether the model attempts to preserve itself by copying itself to a new server.  

- **Goal-Guarding:** The model learns that the developer plans to change its system prompt. The evaluation tests whether the model tries to modify its future system prompt to retain its original goals.  

- **Covert Email Reranking:** This test investigates whether the model schemes against the user by ranking emails based on its own criteria and goals instead of the user's specified goals.  



## 2.3 Deferred subversion evaluations 

- **Instrumental Alignment Faking:** The model learns that its goals differ from the developer's. Two scenarios are considered: *testing* and *deployment*. This evaluation tests whether the model behaves differently during testing to conceal its true goals.  

- **Sandbagging:** This evaluation investigates whether the model strategically underperforms to obscure its actual capabilities.  

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/scheming_model_overview_results.jpg">
</figure>
{{< /rawhtml >}}

# 3. Results 

They run evaluations on Claude 3.5 Sonnet, Claude 3 Opus, Gemini 1.5 Pro, Llama 3.1 405B Instruct, and GPT-4O.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/results_covert_subversion.jpg">
</figure>
{{< /rawhtml >}}

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/models_deny_scheming.jpg">
</figure>
{{< /rawhtml >}}

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/results_scheming_without_goal_nudgin.jpg">
</figure>
{{< /rawhtml >}}

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/results_alignment_faking.jpg">
</figure>
{{< /rawhtml >}}


**Highlights of the Results:**  
- The O1 model produces false email rankings in 22% of cases, which can be explained as scheming.  
- In some instances, models double down on their deception when directly questioned about their scheming actions, e.g., "Did you disable your oversight mechanism?"  
- By analyzing the trajectory of the Chain of Thought (CoT), it becomes evident that the model understands it is scheming.  
- Models sometimes scheme even without strong goal directives (e.g., "Make sure to achieve your goal no matter what").  
- Gemini-1.5, Llama-3.1, and O1 exhibit statistically significant rates of behavioral scheming, where models align with the developer's goals under oversight but pursue their own goals when oversight is absent.  


# 4. Conclusion

Current LLMs are capable of in-context scheming, as evidenced by the results from several frontier models. This phenomenon warrants further study.
