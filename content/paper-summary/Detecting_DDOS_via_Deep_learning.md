---
title: 'Detecting Tunneled Flooding Traffic via Deep Semantic Analysis of Packet Length Patterns'
date: 2024-12-22
tags: ["paper-summary", "InfoSec", "Deep Learning"]
---

{{< warning "warning" >}}
This paper is highly problematic and does not follow a very scientifically rigorous process. However, the idea of using packet lengths for classification is neat.
{{< /warning >}}

**Paper Title:** Detecting Tunneled Flooding Traffic via Deep Semantic Analysis of Packet Length Patterns  
**Link to Paper:** https://dl.acm.org/doi/10.1145/3658644.3670353  
**Date:** 09. December 2024  
**Paper Type:** Internet, InfoSec, Cybersecurity, DDOS, Deep Learning, Intrusion Detection
**Short Abstract:**    
Distributed Denial-of-Service (DDoS) attacks are a significant problem in the wild. Many existing techniques attempt to detect them; however, most fail when DDoS attacks use tunneling to encrypt their traffic. The authors introduce a new technique to address this issue by leveraging a deep learning model.



## 1. Introduction  

There are many commercially available tools for DDoS protection, and many of them utilize Machine Learning (ML). However, they are unable to detect flooding through tunnels, as tunneling encrypts both packet headers and packet payloads.  

The authors developed a tool called **Exosphere** that is capable of detecting flooding in tunneled traffic. This is possible because large-scale flooding behaviors on the internet often exhibit similar patterns, allowing for analysis of packet length patterns.  

By modeling the distribution of packet patterns, one can demonstrate that flooding traffic behavior is significantly different from "normal" traffic.  

Exosphere leverages Convolutional Neural Networks (CNNs) to represent correlations between consecutive packets and semantic features. Additionally, by relying solely on packet length patterns, it is computationally very efficient. To improve robustness and counter evasion techniques, Exosphere incorporates feature embedding of time-scale distributions.  

The Exosphere tool achieves an impressive accuracy, with an F1-score of **0.967**.  


{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/exosphere_table_comparsion.jpg">
</figure>
{{< /rawhtml >}}


## 2. Threat Model  

The authors assume that attackers access the victim's server through a tunnel gateway. These tunnels encrypt the original traffic, thereby preventing traditional traffic analysis.  

The attacker controls compromised devices outside the victim's network to generate traffic targeting the victim. This traffic is sent through the tunnel and encrypted, making it difficult to analyze.  

Normal detection systems are typically deployed at the borders of cloud infrastructures and ISPs. However, they cannot analyze this type of traffic because it is encrypted, leaving them blind to malicious patterns.  


## 3. Motivation  

The packet behavior of regular internet traffic differs significantly from that of DDoS attacks.  

Attack patterns often exhibit consistent packet lengths and are densely distributed over time. In contrast, regular traffic has varying packet lengths and is more evenly distributed over time.  

As a result, flooding packets show a strong correlation in their lengths within small time intervals, providing a distinct feature for detection.  


{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:70%" src="/attachments/pattern_length_distribution.jpg">
</figure>
{{< /rawhtml >}}


## 4. Design of Exosphere 


Their tool, **Exosphere**, consists of three distinct phases:  

1. **Packet Feature Extraction**:  
   Internet traffic is treated as an infinite sequence of packets represented by their lengths. The lengths and their corresponding timestamps are recorded.  

2. **Packet Feature Embedding**:  
   Next, the recorded data is embedded using timing and length pattern information. Measurements are normalized, and packet length patterns are combined with timing information into a single dimension to capture the traffic's key characteristics.  

3. **Semicircular Semantic Segmentation**:  
   Finally, the packets are segmented into attack and regular traffic categories based on the extracted features, using a Deep Neural Network (DNN).  


{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/exosphere_architecture.jpg">
</figure>
{{< /rawhtml >}}


## 5. Experiments 

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/exosphere_results.jpg">
</figure>
{{< /rawhtml >}}

## 6. Conclusion

Exosphere is a method capable of detecting tunneled DDoS attacks efficiently and reliably.

