---
title: 'My Homelab Part 8: Homepage'
updated: 2024-01-29 07:57:00Z
date: 2024-01-21 18:30:17Z
tags: ["homelab"]
---

If you have been following my Homelab Series so far, you probably have quite a number of services running, and perhaps you're losing track of all your services. In that case, you might want to consider having a central page that links to all your hosted services.

[Homepage](https://github.com/gethomepage/homepage) is a highly customizable, fully static, fast, and modern dashboard with integration for many services. It allows users to see all running services at a glance and can be easily configured by editing a YAML file.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/aa21552515d1f292852d17cbeda6d676.png">
    <figcaption style="text-align:center">Example Dashboard with homepage</figcaption>
</figure>
{{< /rawhtml >}}


## Installation 

Similar to the previous blog posts, I will use Docker Compose with the following compose file(homepage-compose.yml) to install Homepage:
```yml
version: "3.3"
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    environment:
      PUID: 1000
      PGID: 1000
    ports:
      - 3000:3000
    volumes:
      - /root/homepage/config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock:ro # optional, for docker integrations
    restart: unless-stopped
```

As always, before installing Homepage, make sure to customize the compose file to your liking. You might want to change the port, PUID/PGID, restart behavior, and the volumes.

If you want to display the status of the Docker container on your central page, you need to run the container in root mode, which means removing PUID and PGID.

To install homepage, follow these steps:
1. Start the docker container:
	```sh
	docker compose -f homepage-compose.yml up -d
	```
2. You should be able to reach the website under: `http://<IP_Of_Your_Server>:homepage_port`

## Configuration

To learn more about configuring the dashboard, you can read the documentation in the references. I will only show my basic configuration.

If you didn't change the volumes, all the configuration files can be found in the `homepage/config` folder. The `services.yaml` is the most important file; in there, you can change what services should be visible on the dashboard. My configuration file looks like this:
```yml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/services

- Services:
    - Syncthing:
         href: http://syncthing.my_domain
         description: Synchronizes your files.
         server: my-docker
         container: synthing

    - CalibreWeb:
        href: http://calibre.my_domain
        description: OnlineBooks
        server: my-docker
        container: claibre-web

    - UptimeKuma:
        href: http://uptime.my_domain
        description: Monitors Docker Container
        server: my-docker
        container: uptime-kuma

    - Vaultwarden:
        href: http://vaultwarden.my_domain
        description: Password manager
        server: my-docker
        container: vaultwarden
        
     - Media:
        href: https://media.monkeman.duckdns.org
        description:  File browser for my Photos and Videos

- Local Services:
    - Wireguard:
        href: http://server_ip:51821/
        description: WireguardVPN
        server: my-docker
        container: wg-easy
    
    - HomeAssistant:
        href: http://192.168.12.100:8123/
        description: The Home Assistant
        server: my-docker
        container: homeassistant

- External Links:
    - FritzBox:
        href: http://fritz.box/
        description: My Router

    - DuckDNS:
        href: https://www.duckdns.org/
        description: My dynamic DNS 
``` 

I use the `container` and `server` variables to show the current status of the service, where `container` is the name of the Docker container as defined in the respective compose file. To use this, your `docker.yaml` file inside your config folder needs to look like this:
```yml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/docker/

#my-docker:
#  host: 127.0.0.1
#  port: 2375

my-docker:
  socket: /var/run/docker.sock
```

There is a great number of services that have some kind of integration with Homepage; you can check this [list](https://gethomepage.dev/latest/widgets/) out. Most code for the widget would be written in the `service.yaml` into the respective category, but some widgets need to be written into the `widgets.yaml` file.

---
References:
- [Homepage Docs](https://gethomepage.dev/latest/)
