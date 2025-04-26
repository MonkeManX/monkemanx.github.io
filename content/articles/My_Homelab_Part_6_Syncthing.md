---
title: 'My Homelab Part 6: Syncthing'
updated: 2024-01-28 17:51:53Z
date: 2024-01-20 16:38:39Z
tags: ["homelab"]
---

In this installment, I explore another valuable use case for my server - file synchronization between my various devices. This includes regular backups of the pictures taken on my phone, archiving important documents, and seamless access to notes across all devices for tasks like blogging, to-dos, projects, and university-related work. To accomplish this, I rely on the powerful capabilities of [synthing](https://syncthing.net/) a continuous file synchronization program.

Syncthing operates by synchronizing files between two or more devices, akin to the functionality of OneDrive synchronization on Windows. However, instead of storing files on a cloud server, Syncthing saves them locally on my home server. The software comes equipped with a user-friendly WebUI that facilitates easy management of file synchronization and connected devices.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/2eb72858a7d12a81c0c1280e559dac46.png">
    <figcaption style="text-align:center">Example Syncthing Page.</figcaption>
</figure>
{{< /rawhtml >}}

## Installation

For the installation process, I utilize Docker Compose with the following configuration in the `synthing-compose.yml` file:
```yml
version: "3"
services:
  syncthing:
    image: syncthing/syncthing
    container_name: syncthing
    hostname: my-syncthing
    environment:
      - PUID=1000
      - PGID=1000
    volumes:
      - /mnt/externalDisk/st-sync:/var/syncthing
      - /mnt/externalDisk/media:/media
    ports:
      - 8384:8384 # Web UI
      - 22000:22000/tcp # TCP file transfers
      - 22000:22000/udp # QUIC file transfers
      - 21027:21027/udp # Receive local discovery broadcasts
    restart: unless-stopped
```

Remember to customize the Docker Compose file according to your preferences, particularly adjusting the `PUID` and `PGID` to match the owner ID of your Syncthing volume. To install and run the container, use the following command:
```sh
docker compose -f synthing-compose.yml up -d
```
After installation, you can access the Syncthing WebUI using the URL: `http://<IP_Of_Your_Server>:Synthing_Port`.

## Configuration and Sychronization

For security, it's essential to set a password for the WebUI. Navigate to `Actions -> Settings -> GUI` and configure the GUI Authentication User and GUI Authentication Password fields.

### Synchronize Phone with Server

To synchronize a folder between your server and phone, install the [official Syncthing app](https://play.google.com/store/apps/details?id=com.nutomic.syncthingandroid&hl=en&gl=US). Add your phone as a remote device on the server by clicking the `add remote Device` button.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:70%" src="/attachments/c1e52179d9d2652b71b31f7404ec3a38.png">
</figure>
{{< /rawhtml >}}

Insert your phone's device ID in the provided field (find it in the Syncthing app menu). Similarly, add your server as a device on your phone.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:50%" src="/attachments/722eb6143ff5c4f1b86a8b0b92681d0f.png">
</figure>
{{< /rawhtml >}}

You should also add your server as device to your phone, this works very similar to how you did it above.

Create a synchronization target by pressing the "+" button, select the folder, and share it with your server.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:50%" src="/attachments/38c70dd4cd4e4b8d37eaf3a806a9146b.png">
</figure>
{{< /rawhtml >}}

 A popup on the server's Syncthing WebUI will appear, asking if you want to synchronize with the phone folder.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/b5e2a589822c5893e97c286f000c501e.png">
    <figcaption style="text-align:center"><a href="https://futurehousestore.co.uk/what-is-home-assistant-and-what-it-can-do">Source</a></figcaption>
</figure>
{{< /rawhtml >}}

That's it! Your phone pictures will now automatically upload to your server.

### Synchronize Computer with Server

If you want to synchronize your Computer with your Server, you first need to install the [synthing software](https://syncthing.net/downloads/) on your computer.

And after that, just like with the phone you need to add your computer as device to the server and vice versa.
Then you can again create a synchronization target.

### Things to keep in mind

- **Synchronization Issues:** If you are sharing a folder among devices with different operating systems and disk formats, enable the `ignoring Permissions` setting in the `Advanced` settings section of your synchronization target.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/8608b9ca84474054aad0baac8452da6a.png">
</figure>
{{< /rawhtml >}}

- **Battery Optimization on Phone:** Disable battery optimization for the Syncthing app on your phone to prevent interference and ensure continuous synchronization.

For additional information, refer to the [Syncthing documentation](https://docs.syncthing.net/).

---
References:
- https://syncthing.net/
- https://docs.syncthing .net/
