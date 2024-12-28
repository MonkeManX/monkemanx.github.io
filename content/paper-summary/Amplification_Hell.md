---
title: 'Amplification Hell: Revisiting Network Protocols for DDoS Abuse'
date: 2024-12-20
tags: ["paper-summary", "InfoSec"]
---

**Paper Title:** Amplification Hell: Revisiting Network Protocols for DDoS Abuse  
**Link to Paper:** https://www.ndss-symposium.org/ndss2014/ndss-2014-programme/amplification-hell-revisiting-network-protocols-ddos-abuse/  
**Date:** 22. Feburary 2014  
**Paper Type:** Internet, InfoSec, Cybersecurity, Attack-Paper, DNS, DDoS, DRDoS   
**Short Abstract:**    
In this paper, the authors introduce *Distributed Reflective Denial-of-Service (DRDoS)* attacks, where attackers exploit open public servers to send large volumes of traffic to a target using IP spoofing. They demonstrate multiple protocols that are vulnerable to such attacks.


# 1. Introduction

Denial-of-Service (DoS) attacks send a large amount of traffic to a victim to disrupt their services.  
In Distributed DoS (DDoS) attacks, multiple machines—often part of a botnet—are used to send traffic to the victim.  
In Reflective DDoS (DRDoS) attacks, an adversary attempts to exhaust the victim's bandwidth by sending requests to publicly accessible servers, known as amplifiers, while spoofing the requests to appear as though they originate from the victim's IP address. This causes the response packets to be sent to the victim instead.  

Advantages of DRDoS over DDoS:
- The attacker disguises themselves as the victim through IP spoofing.
- Sending traffic to multiple servers allows for a highly distributed attack.
- Response packets are often larger than request packets, amplifying the strength of the attack.

There have already been incidents of DRDoS attacks, often involving DNS servers as amplifiers. With the increasing adoption of DNSSEC, which encrypts DNS traffic, the amplification becomes worse due to the larger DNS response sizes.


# 2. Threat Model

The threat model assumes that an attacker (A) attempts to exhaust the victim's (V) bandwidth. To achieve this, DRDoS is used, where A does not send traffic directly to V but instead to systems (amplifiers) that reflect the traffic back to V.

The following assumptions are made about the attacker:
- A can send IP packets with spoofed source addresses. This assumption is reasonable, as 25% of Autonomous Systems (AS) allow spoofing.
- A knows at least one UDP protocol that can be used to request services from the server.
- A cannot control the configuration of the amplifiers. They can only use services that are freely available to them and cannot use bots.



# 3. Amplification Vulnerabilities

In DRDoS attacks, two factors determine the impact of an attack:  
- The chosen protocol used for the attack.  
- The number of amplifiers available.  

## 3.1 Protocol Overview  

For a protocol to be exploitable, it needs to meet two characteristics:  
1. Small requests must lead to large responses.  
2. It must allow traffic with spoofed IP addresses.  

As a result, TCP protocols are excluded, since the TCP handshake requires proper identity verification.  

However, many UDP protocols can be abused for such attacks. The next section provides an overview of these protocols.  


## 3.2 Amplifier Enumeration  

The researchers developed a tool to search for vulnerable amplifiers within a subset of all IPv4 addresses. They assume that the UDP port is standardized. Their findings indicate that the tool does not need to run for long to discover a sufficient number of amplifiable servers.  

{{< rawhtml >}}  
<figure>  
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/drdos_search_time_amplifier.jpg">  
</figure>  
{{< /rawhtml >}}  


## 3.3 Amplification Factors  

The researchers define two measures to quantify how traffic is amplified:  
- **Bandwidth Amplification Factor (BAF):** The ratio by which the bandwidth increases, measured in terms of UDP payload bytes.  
- **Packet Amplification Factor (PAF):** The ratio by which the number of packets increases, measured in terms of IP packet counts.  

{{< rawhtml >}}  
<figure>  
    <img style="display: block; margin-left: auto; margin-right: auto; width: 80%;" src="/attachments/drdos_amplification_factor.jpg">  
</figure>  
{{< /rawhtml >}}  


# 4. Real-World Observations  

The researchers employed the following methods to observe DRDoS activity in the real world:  

1. **NetFlow Data**  
   Using NetFlow data from a large ISP, they analyzed traffic patterns to identify potential DRDoS attacks.  

2. **Darknet Traffic**  
   Scans targeting UDP ports in darknet traffic indicate that attackers may be actively searching for amplifiers.  

3. **Amplifier Baits**  
   They published bait services on the internet, intentionally vulnerable to DRDoS attacks, to study how attackers exploit them.  


{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/drdos_udp_scans_darknet.jpg">
</figure>
{{< /rawhtml >}}

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/drdos_attacks_dataset.jpg">
</figure>
{{< /rawhtml >}}

They identified 15 DRDoS attacks targeting subscribers of the ISP, with the largest attack reaching 711 Mbit/s.


# 5. Countermeasures  

The following countermeasures can help mitigate DRDoS attacks:  

1. **Prevent IP Address Spoofing**  
   Autonomous Systems (AS) should implement measures to prevent IP address spoofing.  

2. **Protocol Hardening**  
   UDP protocols should introduce sessions and handshakes to ensure that communication partners are legitimate, thus preventing spoofing.  

3. **Request/Response Symmetry**  
   Reduce amplification rates by designing protocols so that request sizes are proportional to response sizes.  

4. **Rate Limiting**  
   Limit the number of requests a client can make within a given timeframe to prevent abuse.  

5. **Secure Configuration**  
   Services should be securely configured. For example, DNS name servers should not offer recursive name resolution to unauthorized users.  

6. **Packet-Based Filtering**  
   Implement packet filtering mechanisms to identify and block traffic likely originating from DRDoS attacks.  


# 6. Conclusion

DRDoS is bad, do countermeasures against it!
