---
title: 'The Design Philosophy of the DARPA Internet Protocols'
date: 2025-05-07 10:00:00
tags: ["paper-summary", "telematics"]
---
**Paper Title:** The Design Philosophy of the DARPA Internet Protocols   
**Link to Paper:** https://dl.acm.org/doi/10.1145/52325.52336   
**Date:** August 1988  
**Paper Type:** Telmatics, Network Architetcure, Network Protocol Design  
**Short Abstract:**     
This paper explains the original design decision made by DARPA when it created the Internet.


## 1. Introduction

The U.S. military and DARPA have been developing a suite of protocols for packet-switched networks. These include:

* Internet Protocol (IP)
* Transmission Control Protocol (TCP)

It is sometimes difficult to determine the motivations and reasoning behind their design. In fact, over time, the underlying philosophy has evolved consistently and continues to evolve today—for example, through new extensions to protocols.

This paper catalogs the original objectives and motivations for the Internet architecture.


## 2. Fundamental Goal

DARPA’s primary goal was to develop an *effective* method for multiplexing existing interconnected networks.

At the time, the components of the Internet consisted of various networks that DARPA wanted to connect. Examples of these networks include ARPANET and the ARPA packet radio network.

An alternative would have been to develop a single unified network. However, it was considered necessary to incorporate existing network architectures to make the Internet practically useful.

The chosen technique for multiplexing was packet switching, where traffic is routed based on individual packets. An alternative at the time was circuit switching, where traffic is routed through dedicated circuits. Packet switching was selected because certain applications, such as remote login, were better suited to it.

A key aspect of this top-level goal was the assumption that different networks would be connected using an interconnection layer of Internet packet switches. These switches were called *gateways*.


## 3. Second-Level Goals

In addition to the primary goal, there were several secondary objectives:

1. Internet communication must continue despite the loss of networks or gateways.
2. The Internet must support multiple types of communication services.
3. The Internet architecture must accommodate a variety of networks.
4. The Internet architecture must allow distributed management of resources.
5. The Internet architecture must be cost-effective.
6. The Internet must allow hosts to be easily connected.
7. Resources used in the Internet architecture must be accountable.

It is important to note that this was not just a wishlist but a prioritized list. Because the development was driven by the military, reliability of the Internet was far more important than accountability. Had the Internet been developed primarily for commercial purposes, the priorities might have been inverted—and the Internet would likely look very different today.


## 4. Survivability in the Face of Failure

The most important goal on the list was *survivability*—the ability for the Internet to continue providing communication services even when networks or gateways fail.

In particular, if two entities are communicating over the Internet and a failure occurs, their communication should continue without needing to re-establish or reset the session.

To achieve this, the state information associated with a communication session needs to be preserved. In some network designs, this state is stored in intermediate packet switches—a method called *replication*. The Internet architecture, however, chose a different model: to gather and maintain this state information at the endpoints (the communicating hosts). This is known as *fate sharing*.

In the fate-sharing model, it is acceptable to lose the state information if the host itself is lost.

**Advantages of fate sharing over replication:**

1. It protects against the failure of intermediary nodes.
2. It is easier to implement and engineer.

**Consequences of fate sharing:**

1. Intermediate nodes and gateways must not retain essential state information about ongoing communication sessions—they are stateless. Packets are sent as *datagrams*.
2. Trust is placed in the end hosts. If a host fails, any applications relying on its communication also fail.

One problem with the Internet is that it makes weak assumptions about the capabilities of the underlying networks. As a result, the Internet must detect network failures using its own mechanisms, which tends to result in slower and less precise error detection.


## 5. Types of Services

Another key goal of the Internet architecture was to support a variety of service types. Different services have different requirements. The traditional service model is bi-directional and is sometimes referred to as a *virtual circuit* service.

Initially, there was an attempt to make TCP support all these different requirements. However, this quickly proved too difficult. For example, the XNET protocol, used for debugging, required a connectionless, unreliable form of data transmission, which didn’t align with TCP's model.

Another case was real-time delivery of digitized speech. The primary requirement in this case was minimal delay—not reliable delivery. If a packet was lost, TCP would retransmit it across the entire network, causing long delays. It was better for the application if lost packets were simply dropped, resulting in a brief pause in speech.

This led to a split between TCP and IP. TCP provided a reliable, sequenced data stream, while IP offered a basic building block out of which different services could be constructed: the *datagram*. Since datagram delivery was not guaranteed—only "best effort"—this made it possible to build services that were either reliable or optimized for lower delay. One such service was the *User Datagram Protocol (UDP)*.

The Internet architecture, therefore, did not assume that underlying networks had to support specific services. Only basic datagram delivery was required. All other services could be constructed on top of that.

A key difficulty with this approach was that some original networks, such as the X.25 network, were designed with specific service models in mind and were not flexible enough to support other types of services. As a result, even though X.25 was technically part of the Internet, it could not guarantee support for the full variety of services.


## 6. Varieties of Networks

For the Internet to succeed, it had to incorporate and support a wide range of network types, such as:

* Long-haul networks (e.g., ARPANET, X.25)
* Local area networks (e.g., Ethernet, Ringnet)
* Broadcast satellite networks (e.g., DARPA Atlantic Satellite Network)
* Packet radio networks (e.g., DARPA Packet Radio Network)

The Internet achieved this by making only minimal assumptions about the functionality of underlying networks:

* Networks must be capable of transporting packets (datagrams)
* Datagrams must be of a reasonable size (e.g., at least 100 bytes)
* Networks must support some form of addressing

Explicitly **not** assumed services included:

* Sequenced delivery
* Network-level broadcast or multicast
* Priority ranking of packets
* Internal knowledge of failures
* Specific speeds or delays

If these features had been required, then either network interfaces or the networks themselves would have had to support them. This was deemed undesirable because these services would have to be re-engineered and re-implemented for each individual network.

Instead, by engineering such services at the endpoints—for example, reliable delivery via TCP—each host needed to implement these services only once. After that, the implementation of network interface software was typically simple.


## 7. Other Goals

The remaining goals were of lesser importance. One was to permit distributed management, which has been partially met in practice.

The Internet architecture does not provide as cost-effective utilization as more tailored networks. For example, Internet packet headers are relatively long (typically 40 bytes). For small packets, this overhead is significant, whereas for large packets, the relative overhead is much smaller.

Another inefficiency arises from the retransmission of lost packets. Since packet loss cannot be recovered at the network level, data may need to be retransmitted from one end of the Internet to the other, crossing multiple networks. This is a trade-off that results from providing services at the endpoints.

Attaching a host to the Internet is also more costly than in some other networks, because mechanisms such as acknowledgments and retransmissions must be implemented in the host rather than the network.

A related issue is that poor implementation of communication mechanisms at the host can negatively affect both the host and the network.

The final goal was accountability. At the time of writing, there are still few tools available to track and account for packet flows across the Internet.


## 8. Datagrams

A fundamental feature of the Internet architecture is the use of *datagrams* to transport messages across networks. Datagrams are important because:

1. They eliminate the need for maintaining connection state in intermediate switching nodes, simplifying failure recovery.
2. They provide a basic building block for constructing other services.
3. They represent the minimum assumption required from the network layer.

It is important to understand that the datagram itself is not a service, but a building block for building services.


## 9. TCP

TCP has undergone many iterations, and only a few key design decisions are discussed here.

The original ARPANET protocol used flow control based on both bytes and packets. This was considered overly complex. TCP chose instead to regulate the delivery of *bytes* rather than the number of packets.

This decision was motivated by several considerations:

1. Acknowledging bytes (rather than packets) allowed the insertion of control information into the sequence (though this use was later dropped).
2. It enabled TCP packets to be broken into smaller units, if necessary, to fit through smaller networks.
3. It allowed multiple small packets to be grouped into a larger one. This turned out to be especially useful in systems like UNIX.

In retrospect, a better design decision might have been for TCP to support flow control based on both packets and bytes.

Another design decision was the use of the End-of-Letter (EOL) flag, which has since been replaced by the PSH (Push) flag. The original intent was to break the byte stream into discrete records.


## 10. Conclusion

The Internet architecture has been extremely successful. Its protocols are widely used in both commercial and military environments.

However, it has also become clear that, in certain situations, the priorities of the original designers do not align with the needs of actual users.

While datagrams have served well in achieving many goals, they have not worked equally well in all contexts. Most datagrams are actually part of a flow or sequence of packets between a source and a destination, rather than isolated units. However, gateways can only handle packets in isolation and are unaware of larger flows.
