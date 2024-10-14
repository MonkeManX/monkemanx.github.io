---
title: 'My Homelab Part 7: UptimeKuma'
updated: 2024-01-29 07:42:44Z
date: 2024-01-20 18:30:47Z
tags: ["homelab"]
---

Maybe at some point you have encountered a situation where, while running all your current containers, you tried accessing one of your services only to realize that the service is not available because the container exited without your knowledge?

For such Issues, it's beneficial to have a notification system that can automatically alert you whenever a container exits or is no longer available.  To address this need, I use [UptimeKuma](https://uptime.kuma.pet/), an easy-to-use self-hosted monitoring tool. UptimeKuma can monitor uptime over means like HTTP(s)/TCP/Ping/Docker/DNS and notify you via various channels such as Telegram, Discord, Gotify, Slack, Email, and more. Additionally, it provides a user-friendly web interface for managing and adding new monitors.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/5fb6d6ee5c143dedeeb77148ea1d2ff3.png">
    <figcaption style="text-align:center">UptimeKuma Page</figcaption>
</figure>
{{< /rawhtml >}}

## Installation

To install UptimeKuma, I utilized Docker Compose with the following configuration in the compose file(uptimeKuma-compose.yml):
```yml
version: '3.8'

services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    volumes:
      - /root/uptime-kuma/:/app/data
      -  /var/run/docker.sock:/var/run/docker.sock
    ports:
      - "3001:3001"  # <Host Port>:<Container Port>
    restart: unless-stopped
```

To install and execute the container, I used the following command:
```sh
docker compose -f uptimeKuma-compose.yml up -d
```
After this, the web UI becomes accessible via the URL:
`http://<Server_IP>:UptimeKuma_Port` 

## Configuration

When configuring UptimeKuma, the first step is to change your login data. In order to do so, navigate to `Settings -> Security -> Change Password`.

To add a new monitor for one of your services, click the `add new monitor` button in the top right corner.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/401ce7a076ab17b1e057480dc491e524.png">
</figure>
{{< /rawhtml >}}

Select the monitor type based on how UptimeKuma should monitor your service. For Instance, for monitoring a Docker container, choose `Docker Container`. The `Friendly Name` field is the display name for your monitor.

Set the `Container Name/ID` to the name or ID of the Docker container you want to monitor. Retrieve this information from your Docker Compose file or using the command `docker ps -a`. Specify the `Docker Host` to indicate where UptimeKuma should listen for the Docker container.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/9d351bececedf9211fed1b35221f2dd2.png">
</figure>
{{< /rawhtml >}}

The `Heartbeat Interval` determines how often UptimeKuma checks your service. After configuring, click `save`, and the monitor will appear on the UptimeKuma web UI, checking your service periodically.

To receive notifications when the status of your service changes, set up notifications by editing a service monitor and clicking `Setup Notification`.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/350e598f2a7d1867bf9874c2c089fecd.png">
</figure>
{{< /rawhtml >}}

For Telegram notifications, follow these steps:
1. Contact the Telegram Bot [BotFather](https://telegram.me/BotFather) to create a new bot.
The `/start` command, will show you a guide on how to setup a bot.
Alternatively, you can follow the steps below.
2. Use the `/newbot` command to create a new bot, following BotFather's guidance.
{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/10e8ce89857027e248f9face00d46aaa.png">
</figure>
{{< /rawhtml >}}

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/0ed96ca3a02e38d033c386b648c4cef4.png">
</figure>
{{< /rawhtml >}}
3. After creating the bot, copy the `HTTP API token` and enter it in UptimeKuma.
{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/e52b53a8a63e98281f9d9975b64c2579.png">
</figure>
{{< /rawhtml >}}
4. Test the configuration and save it. You can now enable Telegram notifications for all your site monitors. 

---
References:
- [UptimeKuma Docs](https://github.com/louislam/uptime-kuma/wiki)
