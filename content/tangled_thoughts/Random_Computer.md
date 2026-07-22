---
title: Computer
date: 2024-11-17
---

Computer Broke. This is the first time that, through my own actions, I not only nuked the operating system (as I did with Debian, Arch, and FreeBSD) but also the entire computer.  

The background is that I was booting NixOS and wanted to switch from `systemd-boot` to `grub` because it looks "nicer." While executing the command for switching, I got a warning: "`/boot` not found." I decided to try rebooting my computer to see if the issue would resolve.  

To no one's surprise, my computer didn’t boot anymore—it didn’t even show the UEFI. When I turned the computer on, it just displayed a black screen for 10 seconds, turned off, and restarted in an endless loop, going round and round like a washing machine.  

Troubleshooting steps I tried:  
- Removing the second monitor  
- Removing the RAM  
- Removing the SSD on which NixOS was installed  
- Removing the SSD on which Windows was installed  
- Booting from a Live USB stick  

Operating system: three points. MonkeMan: zero points.  

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/my-pain-is-constant-and-sharp.webp">
</figure>
{{< /rawhtml >}}

