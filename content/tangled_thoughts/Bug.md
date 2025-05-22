---
title: Bug
date: 2024-11-03
---

A long time ago, at least 5 years back, when I came home from school, it was [bulky waste](https://en.wikipedia.org/wiki/Bulky_waste) day. People put waste like furniture out on the street, where a truck would later pick it up.

On that day, as I was walking home, I saw a monitor lying there and decided to bring it home with me. It wasn’t a new monitor, quite the opposite. It had a maximum resolution of 1280x768 and was 19 inches in size, but it was good enough to use as a second monitor.

One issue, though, was that the monitor only supported VGA, which my graphics card didn’t support, so I bought a VGA-to-DVI adapter.

This setup worked fine until recently, when I updated my graphics card driver and kernel. The update introduced a [bug](https://bbs.archlinux.org/viewtopic.php?id=297296) that caused the second monitor to be detected but display only a black screen.

There’s a solution: to downgrade the graphics drivers and kernel, which I tried. However, I encountered issues with dependencies and ended up uninstalling packages, which accidentally “nuked” my system.

Fortunately, I was triple-booting and still have my old Debian distribution, so I’m going back to Debian.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/debian_my_beloved.gif">
</figure>
{{< /rawhtml >}}


