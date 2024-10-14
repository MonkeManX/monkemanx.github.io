---
title: 'My Homelab Part 11: Backup'
updated: 2024-01-29 09:11:57Z
date: 2024-01-27 11:33:02Z
tags: ["homelab"]
---

It goes without saying that backups are crucial. If you aim to preserve your data for the future, proper backup practices are a necessity. The golden rule of backing up is the 3-2-1 rule, which advises having three copies of your data, on two different media, with one copy off-site.

In my case, I needed a backup solution for various types of data:
- **Photos**: Currently stored on my phone.
- **Text files**: Including university notes, general notes, and articles, currently saved on my computers.
- **Configuration files**: From my server, currently saved on the SD card of the server.

For my backup needs, I opted for two solutions: **Syncthing** and **rsync**.

**Syncthing**:
You may already be familiar with Syncthing from my previous post in the Homelab Series, where I introduced it for data synchronization. However, it can also serve as a backup tool. By synchronizing every Syncthing folder I use with my server, I automatically create a copy on my server. Specifically, I configured Syncthing so that all synchronized data (such as photos and writings) is stored on the first external disk of the server.

**Rsync**:
Given that my Raspberry Pi server uses an SD card for main storage, where the operating system and home folder are stored, I use rsync to back up my home folder to the first external disk. Rsync allows for folder-level backups, crucial in server environments where SD cards are prone to breaking under constant stress.

Using only one disk introduces the risk of disk failure. To mitigate this, I employ an additional disk to back up my first disk, again utilizing rsync for this task.

Although I considered using a RAID system, I decided against it for two reasons:
1. **Lack of RAID Controller**: I don't have a RAID controller and didn't want to invest in one. Using a RAID controller on the software level tends to be slower.
2. **Scale and Need:** RAID isn't very effective at the scale of two disks, and I didn't require additional backup storage at the moment.

For information on installing Syncthing, refer to my earlier post in this series, "My Homelab Part 6: Syncthing."

## Rsync

[Rsync](https://linux.die.net/man/1/rsync) is a command-line tool that should already be pre-installed on most Linux operating systems. To initiate a folder clone, use the command:
```sh
rsync -r /origin/ /target
```

Keep in mind that rsync is slower than a simple move or clone command because it checks every file. For the initial backup, it's recommended to use the cloning command.

To regularly back up my home folder, I use cron(see "My Homelab Part 0: Prologue"), which allows me to schedule commands. To do that, start crontab with:
```sh
crontab -e
```
Here's an example of scheduling:
```sh
0 4 * * * rsync -aAXvh /mnt/externalDisk/ /mnt/externalBackupDisk/BackupDisk/
0 2 * * * rsync -aAXvh /root /mnt/externalBackupDisk/BackupHome/
```

You can customize the scheduling as needed. In my case, I back up my home folder at 02:00 every day and my disk at 04:00. The meaning of the arguments can be [read here](https://linux.die.net/man/1/rsync), but to summarize briefly:
- `a`: Archive option, indicating recursion and keeping everything.
- `A`: Updates the permission of the files.
- `X`: Removes extended attributes of files.
- `v`: Increases the amount of information given during transfer.
- `h`: Outputs numbers in a human-readable format.

That's it, and always remember, backups are crucial.

{{< rawhtml >}}
<figure style="display: block; margin-left: auto; margin-right: auto; width:80%; text-align:center">
    <img src="/attachments/backups.png">
    <figcaption style="text-align:center"><a href="https://xkcd.com/1718/">Source</a></figcaption>
</figure>
{{< /rawhtml >}}

## Off-Site Backups

In the beginning I talked about the 3-2-1 backup rule, one part of this is to have a backup offsite. Which I didn't quite address in this post, one way to achieve that is by placing your server not inside the house you live, this could be in the home of your parents or a friend. Another way could be to rent a server, and use synthing again there to sync your data between your rented server and your home server.

