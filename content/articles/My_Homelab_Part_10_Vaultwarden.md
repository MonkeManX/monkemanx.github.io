---
title: 'My Homelab Part 10: Vaultwarden'
updated: 2024-01-29 09:37:21Z
date: 2024-01-25 11:30:36Z
tags: ["homelab"]
---

Vaultwarden is an unofficial implementation of the Bitwarden password manager. One of its primary advantages is its lower resource intensity for hosting compared to the official implementation, along with the support of a robust community.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/8ddd4488bb9c1a355dc41d6b6db4898f.png">
    <figcaption>Vaultwarden Website.</figcaption>
</figure>
{{< /rawhtml >}}

Before adopting Vaultwarden, I relied on the offline password manager KeePassXC. However, it posed challenges with synchronization across multiple devices. For instance, if I altered a password on my phone, I had to transfer the entire password database to my computer to ensure synchronization. In contrast, Vaultwarden streamlines this process by automatically synchronizing password changes across all devices.

Here's how Vaultwarden operates: the Vaultwarden software is hosted on your server, managing and storing your passwords. Clients can access these passwords by connecting directly to your hosted Vaultwarden website, through the official Bitwarden browser extension, or via the Bitwarden app on a mobile device.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Untitled%20Diagram.drawio.png">
    <figcaption>Explanation of Vaultwarden.</figcaption>
</figure>
{{< /rawhtml >}}

## Installation

As with my previous blog posts, I'll use Docker Compose to install Vaultwarden, employing the following Docker Compose file(vaultwarden-compose.yml):
```yml
version: '3'
services:
  vaultwarden:
    container_name: vaultwarden
    image: vaultwarden/server:latest
    restart: unless-stopped
    volumes:
      - /mnt/externalDisk/vaultwarden/:/data/
    ports:
      - 150:80
    environment:
      - DOMAIN=
      - WEB_VAULT_ENABLED=true
      - ADMIN_TOKEN=XXXXX
      - SIGNUPS_ALLOWED=false
      - EMERGENCY_ACCESS_ALLOWED=true
```

It's crucial to note that Vaultwarden deals with sensitive information, requiring a secure connection (HTTPS). In a non-secure connection (HTTP), accessing your password vault won't be possible. Therefore, I highly recommend following my previous blog post, where I demonstrated how to assign a domain to your internal services for secure internet access. If you've followed that guide, remember to update your Caddyfile for this new service:
```
vaultwarden.{$DOMAIN} {
    import tls
    import header
    
    reverse_proxy localhost:{$VAULTWARDEN_PORT}
}
```

Additionally, starting from version `1.28` of Vaultwarden, the admin token must be [hashed](https://github.com/dani-garcia/vaultwarden/wiki/Enabling-admin-page). To do that, follow these steps:
1. Execute the command `docker run --rm -it vaultwarden/server /vaultwarden hash` to initiate a temporary Vaultwarden instance for hashing your password.

2. Enter your desired password when prompted.

3. After receiving the password hash, escape the dollar sign using the command: 
    ```
    echo "your_password" | sed 's#\$#\$\$#g'
    ```

4. Copy the password hash and insert it into your Docker Compose file.

To install Vaultwarden, proceed with these steps:

1. For the initial run, set `SIGNUPS_ALLOWED` to `true` to create an account. After registration, stop the Vaultwarden container and set this variable to `false`.

2. Don't forget to set the `DOMAIN` in the Docker Compose file to your domain.

3. After configuring these variables, start your container using:
	```sh
	docker compose -f vaultwarden-compose.yml up -d
	```

4. After a while, access your Vaultwarden service at `https://vaultwarden.Your_Domain`, displaying a page similar to this:  
    {{< rawhtml >}}
    <figure>
        <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202024-01-20%2012-42-41.png">
    </figure>
    {{< /rawhtml >}}

5. Click "Create account," leading to the registration page:  
    {{< rawhtml >}}
    <figure>
        <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202024-01-20%2012-43-28.png">
    </figure>
    {{< /rawhtml >}}

6. After registration, stop the Vaultwarden container, disable sign ups, and restart the container using the following commands:
	```sh
	docker ps -a
	docker stop vaultwarden_id
	```
7. Upon restarting the container, you can log in with your registered account. To manage settings, including user accounts, access the admin page at `https://vaultwarden.Your_Domain/admin`, requiring your admin token as password.

---
References:
- https://github.com/dani-garcia/vaultwarden
