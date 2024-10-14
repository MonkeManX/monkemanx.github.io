---
title: 'My Homelab Part 4: Wireguard VPN'
updated: 2024-01-28 15:09:25Z
date: 2024-01-19 11:31:55Z
tags: ["homelab"]
---

Sometimes I need access to my home server to work on some configuration files or check the health of the server, but not always do I have physical access to my home server. One way to still get access to my server even when I am far away is through a VPN, which allows me to connect to my home network, and from the home network, I can then SSH into my home server.

[Wireguard](https://www.wireguard.com/) is a free, open-source, modern, and fast VPN service. The other big competitor to Wireguard that I want to mention for completion's sake is [OpenVPN](https://openvpn.net/).

To be more specific, I use [wg-easy](https://github.com/wg-easy/wg-easy) for my server, which is one of the easiest ways to self-host a VPN server. Not only is wg-easy a VPN service, but it also allows you to manage your connection through a WebUI.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/aed9491cae39af755a01815eb44b0c19.png">
</figure>
{{< /rawhtml >}}

## Installation

Just like in my previous blog post with Calibre, I will use Docker Compose to install wg-easy with the following Docker Compose file:
```yml
version: "3.8"
services:
  wg-easy:
    environment:
      # ⚠️ Required:
      # Change this to your host's public address
      - WG_HOST=

      # Optional:
      - PASSWORD=  
    image: weejewel/wg-easy
    container_name: wg-easy
    volumes:
      - /root/wg-easy:/etc/wireguard
    ports:
      - "51820:51820/udp"
      - "51821:51821/tcp"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv4.conf.all.src_valid_mark=1
```

The first thing you have to do is change the `WG_HOST` variable to the IP-Address or domain of your server and set a `PASSWORD` so that not everyone can access the Web UI. After that, you can start the Docker container with:
```sh
docker compose -f wg-easy-compose.yml up -d
```
After some time, you should be able to access the website of wg-easy with the URL: `http://<Server_IP_Address>:51821`.

There are multiple clients available cross-platform to connect to your VPN Server, including an Android/iOS app and a Windows/Linux client. To download a client, you can visit their [Official Website](https://www.wireguard.com/install/).

To establish a VPN connection with your server, you first need to add the connection on the client. You can do that by pressing the `new` button on the wg-easy website.
![2024-01-20_16-58.png](./attachments/2024-01-20_16-58.png)
After giving your connection a name, you can either download the config file and send it to your client device or scan the QR code.

There are two additional things to keep in mind when trying to connect to your VPN Server:
1. If the network from which you use the VPN has the same IP range as the network from your home server, Wireguard will get confused and won't know where to send the internet traffic. You can fix this by using a more uncommon IP range for your home network.
2. If you try to use the Windows Wireguard client, you might experience the issue that all the traffic gets directed towards you in a cycle, and you DoS yourself. This is a [known issue](https://github.com/WireGuard/wireguard-nt/blob/master/TODO.md)(see "Forwarding/WeakHostSend breaks IP_PKTINFO"). You can disable it by:
	1. Opening a powershell terminal
	2. To see the status of weakhostsend, type:
		```sh
		Get-NetIPInterface | ft interfacealias,forwarding,weakhostsend
		```
	4. To disable it, use the following command:
		```sh
		netsh interface ipv4 set interface "Ethernet 2" weakhostreceive=disable
		``` 
	4. Do the same for the `forwarding` variable.	
	
----
References:
- https://www.wireguard.com/
