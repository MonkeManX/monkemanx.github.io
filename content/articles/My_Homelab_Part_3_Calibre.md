---
title: 'My Homelab Part 3: Calibre'
updated: 2024-01-27 22:27:05Z
date: 2024-01-19 11:30:23Z
tags: ["homelab"]
---

In my free time, I enjoy reading books. For a long time, I organized the books I read on physical paper notes. However, as the list grew longer and paper deteriorated over time, I realized it was impractical. To address this, I decided to switch to a digital organization strategy, and for that, I chose the software Calibre.

Calibre is a free and open-source e-book management program. It supports organizing existing e-books into virtual libraries, displaying and editing e-books, and even synchronizing them with different e-readers.

[Calibre-Web](https://github.com/janeczku/calibre-web) is a web app for Calibre that allows access to Calibre via the internet.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/ca92bc5421fc394fb5a55384fe696aea.png">
    <figcaption style="text-align:center">"An exemplary view of the Calibre-Web software.</figcaption>
</figure>
{{< /rawhtml >}}


In this short blog post, I'll guide you through the process of installing Calibre-Web. 
If you are interested in how I set up my homeserver, you can read one of my previous blog posts.

## Installation

For the installation of Calibre-Web, I used Docker, specifically Docker Compose. If you're curious about why, you can check out my blog post "My Homelab Part 1: Introduction," where I explain the advantages of docker.

In Docker, to start a container, you typically use a long command with configurations as arguments. This approach can be confusing and hard to reproduce.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/0d442bad34cd850c0ca7cba6f033393e.png">
    <figcaption style="text-align:center">Example of a docker command to run a container.</figcaption>
</figure>
{{< /rawhtml >}}

A better option is Docker Compose, where all the configurations are placed in a `compose.yaml` file, making it clearer and easier to reproduce.

In general the docker compose file uses [YAML](https://en.wikipedia.org/wiki/YAML) as a file format, which is a human readable data language.
The Compose files uses some predefined keys that can be used to configure how docker should behave, to read more [check this out](https://docs.docker.com/compose/).

The Docker Compose file for Calibre I used is as follows:
```yaml
---
version: "2.1"
services:
  calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    container_name: calibre-web
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin
    volumes:
      - /root/calibre/config:/config
      - /mnt/externalDisk/calibre/libary:/books
    ports:
      - 8083:8083
    restart: unless-stopped
```
This configuration file needs some explanation:
- `image`  describes the container pulled from the internet i.e the software that you want to install. Images can be found on the [docker hub website](https://hub.docker.com/).
- `environment` specifies additional settings for the container. For instance:
	- `TZ` specifies the timezone for the software
	-  `PUID/PGID` the id of the user and group under which the software will run.
		- to find out your `PUID/PGID` you can run the following command for user id:
			 ```sh
			 id -u username
			 ``` 
			 and for group id:
			 ```sh
			 id -g username
			 ```
- `volumes` describe where data from the software is saved. The first path is the physical location on the computer, while the second is a virtual location inside the docker container, the paths are separated by `:`.
- `ports`  specify which ports are exposed to the docker container.
- `restart` instructs Docker on what to do if the container shuts down unexpectedly.

Normally, you will be able to find a list of keys that you can set for the given image by looking at the docker hub page or on the maintainers page. 
For instance you can check out [linuxserver page on calibre](https://docs.linuxserver.io/images/docker-calibre/#optional-run-configurations).

To install Calibre on your server, follow these steps:
1. create a file titled `calibre-web-compose.yml` and copy the content of the above into the YAML file.
2. Edit the file to suit your needs, you should especially change the volumes, timezone, and PUID/PGID. Ensure the PUID and PGID match the owner of the volumes.
3. Move the file to your server. Save it in your home directory, and use `scp` to transfer it if needed.
4. Open a terminal at the file location and run::
	```sh
	docker compose -f calibre-web-compose.yml up -d
	```
	This starts the container in the background:
	The `-f` specifies the file name of the compose file 
	`-d` tells docker to start the container in the background without displaying the logs in the terminal.
5. After installation, check the container status by running:
	```sh
	docker ps -a
	```

6. Access Calibre-Web at `http://<IP_Of_Your_Server>:Calibre_Port`, log in using the default credentials (Username: admin, Password: admin123).

    {{< rawhtml >}}
    <figure>
        <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202024-01-19%2017-59-03.png">
    </figure>
    {{< /rawhtml >}}
    Should the default login data have changed, you should be able to find them on the [image doc site](https://docs.linuxserver.io/images/docker-calibre-web/#version-tags) of calibre.

7. After login in you should get greeted by a window similar to the image below.

    {{< rawhtml >}}
    <figure>
        <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202024-01-19%2018-01-34.png">
    </figure>
    {{< /rawhtml >}}

In order to function properly Calibre-Web will need a virtual library, which is a databank that saves all the information about your books.
Unfortunately Calibre-Web, doesn't let you create new  libraries from scratch, instead it only works with already created existing libraries.
For that you can either:
- Download Calibre on your computer create an empty library and export it or
- You can download an already created database, via the command: 
	```sh
	weget sempervieo.de/metadata.db
	```  
	If you do download this file make sure to make yourself the owner of the file and give you full permission on this file(see "My Homelab Part 2: DietPi").
	
After you have downloaded or created the file move the file into your books volume, that you have defined in your `compose` file. Following that, you should be able to select the books folder as database folder in the Calibre-Web application.

The last thing you should do, is enabling uploads of books via Calibre-Web and change your password. To do that navigate to
- `Configuration -> Edit Basic Confguration -> Feature Configuration -> Enable Uploads`
- `admin -> edit user`

## OPDS

The Open Publication Distribution System (OPDS) is an electronic catalog format for electronic publications. OPDS can be used on the server to enable clients, such as e-readers or programs with ODPS support, to discover and download e-books.

I use ODPS to download books to my e-reader (which uses Koreader software) or to my computer (which uses Calibre) whenever I want to read an e-book.

To configure ODPS for Koreader:
1. Open the menu by tapping on the top of the screen
2. Navigate to the magnifying glass.

    {{< rawhtml >}}
    <figure>
        <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/2024-01-20_11-54.png">
    </figure>
    {{< /rawhtml >}}

3. Press the ODPD Catalog option, and press the + Button in the top left corner to add an ODPS Catalogue.

    {{< rawhtml >}}
    <figure>
        <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/2024-01-20_11-57.png">
    </figure>
    {{< /rawhtml >}}

4. Choose a catalogue name; the catalogue URL should be: `http://<Server_IP>:Calibre_Port/opds`. Enter the username and password defined in your Calibre-Web server.
5. To connect to your OPDS catalogue, press the newly added catalogue.

As a last piece of advice,[Annas Archive](https://annas-archive.org/) has an enormous library of e-books available for free download. However, please keep in mind that supporting authors is crucial for them to continue producing their awesome works.

----
References:
- https://github.com/janeczku/calibre-web/wiki
- https://docs.linuxserver.io/images/docker-calibre-web/#version-tags
- https://en.wikipedia.org/wiki/Open_Publication_Distribution_System
- [Calibre Web: Ebook Verwaltung leicht gemacht](https://youtu.be/bucvyiwsnMc?si=SDn_PfIWOIXNgMoV)
