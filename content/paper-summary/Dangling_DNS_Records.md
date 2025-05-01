---
title: 'All Your DNS Records Point to Us'
date: 2024-12-19
tags: ["paper-summary", "InfoSec"]
---

**Paper Title:** All Your DNS Records Point to Us    
**Link to Paper:** https://dl.acm.org/doi/10.1145/2976749.2978387  
**Date:** 24. October 2016  
**Paper Type:** Internet, InfoSec, Cybersecurity, Attack-Paper, DNS  
**Short Abstract:**    
In this paper, the author explores how dangling DNS records (Dare) can be exploited for domain hijacking to gain full control of domains.

## 1. Introduction

The Domain Name System (DNS) is integral to the functioning of the internet. As such, it is vital to maintain trust in it by ensuring integrity and authenticity.

Attempts such as [DNSSEC](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions) only secure the channel between the server and the client. However, what is needed is the authentication of the resources to which DNS records point.

A DNS record can be represented by a tuple `<name, TTL, class, type, data>`, where `name` is the domain name, and `data` specifies the resource to which the domain name points.

A dangling DNS record (Dare) occurs when the owner of a domain forgets to remove its related DNS record. This means the domain is still active but forwards traffic to a missing resource in the `data` field.

To exploit a Dare, an attacker needs access to a resource with the same address as the `data` field in the Dare. These addresses can be either IP addresses or domain names.

Ways of Attack:
1. **Cloud Services**: Cloud computing has become increasingly popular for modern websites. In cloud environments, addresses are often shared between customers. If an attacker gains access to a shared address, they could exploit the Dare.  
2. **Third-Party Services**: Many websites use third-party services that require adding an `A` or `CNAME` record to the DNS server to claim ownership of subdomains. An attacker can abuse abandoned subdomains of these third-party services.  
3. **Expired Domains**: Domains can expire, and an attacker could search for expired domains in the `data` field of DNS records.


**Empirical Study**  
To assess the magnitude of this problem, the authors analyzed the top 1 million domains on Alexa using a tool designed to automatically detect Dares. They confirmed 791 Dares and identified 5,982 potential Dares that could be exploited. These records appear trustworthy because attackers can easily obtain HTTPS certificates for them using services like `Let's Encrypt`.

**Mitigation**  
A protocol needs to be developed to authenticate the ownership of the resources referenced by a DNS record. Additionally, DNS servers should periodically remove DNS records associated with expired domains.


## 2. DNS Overview

The interaction between a DNS server and an IP address, called DNS resolution, works as follows:

1. The client queries a local or remote DNS server, which checks its cache for the requested DNS record.  
2. If a cache miss occurs, the server recursively queries the root server, followed by the `.com` server, and then other relevant servers.  
3. The DNS server responds with the IP address.  
4. The client obtains the IP address and connects to the website.  


## 3. Dangling DNS Records

A DNS record is considered *dangling* if the resource specified in the `data` field is no longer in use or has been released.  

### 3.1 Types of Dangling DNS Records (Dare)

- **Dare-A**: Points to an IPv4 address. It becomes compromised if an attacker gains control of the IP address.  
- **Dare-CNAME**: Points to a domain, functioning as an alias.  
- **Dare-MX**: Responsible for email exchange. An attacker could potentially send and receive emails from the domain.  
- **Dare-NS**: Delegates a domain to an authoritative DNS (aDNS) server.  

### 3.2 Risk Factors in Different Scenarios  

Many websites use third-party services like GoDaddy to host their domains. In typical configurations, these services host multiple domains on a single machine, sharing the same IP address. In such cases, Dare-A records are relatively safe, as adversaries cannot easily obtain a specific IP address.  

However, the risk is different in cloud environments, where customers can acquire public IP addresses from a shared pool. A malicious user could repeatedly allocate and release IP addresses until they obtain the desired address, making Dare-A records exploitable in these scenarios.  

Modern websites often rely on third-party services like Shopify. These services provide users with a subdomain (e.g., `alice.myshopify.com`). To use their own domain (e.g., `shop.alice.com`), users set up a CNAME record that points to the third-party domain. Frequently, users forget to remove these DNS records after discontinuing the service. For example, `shop.alice.com` might still direct traffic to `shops.shopify.com`. An attacker could then claim ownership of the abandoned subdomain and exploit it.  

### 3.3 Exploiting Expired Domains  

Expired domains are particularly easy to exploit. An attacker only needs to check if a domain referenced in a DNS record has expired. Once identified, the attacker can register the domain and abuse it for malicious purposes.  


## 4. Results

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/results_dares_top_domains.jpg">
</figure>
{{< /rawhtml >}}

Dare-A and Dare-CN constitute the majority of confirmed and potential Dares. This makes sense since they are more frequently used in practice.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/figures_dares.jpg">
</figure>
{{< /rawhtml >}}


## 5. Threat Analysis  

People often trust familiar domain names, and this trust can be exploited in various attacks:  
- **Scamming and Phishing**: Creating a site that closely resembles the original to deceive users.  
- **Cookie Theft**: Stealing cookies; users only need to visit the website briefly for this attack to succeed.  
- **Email Fraud**: Exploiting Dares to send and receive emails under the guise of a trusted domain.  


## 6. Mitigations  

Mitigation strategies include:  
- Authenticating the IP addresses in the `data` field of DNS records.  
- Encouraging third-party services to deprecate unused or outdated DNS records.  
- Regularly checking for expired domains and removing their associated DNS records.  
