---
title: 'My Homelab Part 0: Prologue'
updated: 2024-01-27 19:19:27Z
date: 2023-12-16 10:13:35Z
tags: ["sleeping", "homelab"]
---

Lately, maintaining a consistent sleeping schedule has posed big challenge for me.
Different university courses have lead me to wake up on some days as early as 6 a.m., while on other days, I've found myself rising as late as 12. p.m .
This irregular sleeping schedule has been quite a struggle, especially on days where I had to get up early.
My body, accustomed to my late-night schedule, could never fall asleep soon enough for a well-rested morning.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/insomnia.png">
    <figcaption style="text-align:center"><a href="https://imgs.xkcd.com/comics/insomnia.png">Source</a></figcaption>
</figure>
{{< /rawhtml >}}

Thus I decided to establish a more consistent sleep schedule by waking up early on every weekday.
The big question was how could I make this happen?

The solution I arrived at consisted of three parts:
1. Shutting down my computer early 
2. A phone free bedroom
3. Light as Sleep-Wake Signal 

## Early Shutdown of Computer

I often caught myself watching YouTube videos after YouTube video late into the night, even when I knew that I should have gone to bed long ago.
In an attempt to stop this behavior, I came up with the idea of automatically shutting down my computer on a schedule.

Implementing this was straightforward. 
Given that I use Linux(Debian 12) as operating system for my Computer, I could use use [cron](https://en.wikipedia.org/wiki/Cron) to automatically shutdown my computer on a specified schedule.

To achieve this, I first needed to edit the crontab file - the crontab file is a configuration file that is responsible for storing all the scheduled jobs the cron daemon executes.
Users have the option to use their own crontab file or utilize the system-wide crontab file.

To access and edit the crontab file, the following command is used:
```sh
sudo crontab -e
```
The usage of `sudo` is particularly noteworthy. This grants the necessary privileges to edit the crontab file of the root user. Omitting the `sudo` would mean editing the crontab file of the current user. This is important because the shutdown commands requires sudo privileges for execution.

Upon executing the above command, users can then input the desired command to be executed to a specific schedule, following the syntax:
```
# ┌───────────── minute (0–59)
# │ ┌───────────── hour (0–23)
# │ │ ┌───────────── day of the month (1–31)
# │ │ │ ┌───────────── month (1–12)
# │ │ │ │ ┌───────────── day of the week (0–6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * <command to execute>
```
To ensure correctness in the syntax, a helpful tool is is [grontab guru](https://crontab.guru/).
This tool enables users to validate the syntax and show its semantic meaning.

For my particularly use case, I inserted the following line into the crontab file:
```sh
45 21 * * 0-4 systemctl shutdown
```
This command will shutdown my computer on 21:45 on every day of the week from Sunday to Thursday.
This should work on all Linux operating systems that use [Systemd](https://en.wikipedia.org/wiki/Systemd) such as fedora, debian, ubuntu, arc and ect.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:40%" src="/attachments/Strip-Mr-CRON-550-finalenglish.jpg">
    <figcaption style="text-align:center"><a href="https://www.commitstrip.com/en/2013/09/23/et-sil-etait-humain/?">Source</a></figcaption>
</figure>
{{< /rawhtml >}}


## A phone free bedroom

Implementing a phone-free bedroom has brought another very positive change in my routine.
Previously, I found myself often glued to the screen for long period of times.

To establish the habit of removing my phone from my sleeping space, I followed roughly [James Clear's](https://jamesclear.com/) habit formation list, as outlined in his his book [Atomic Habits](https://jamesclear.com/atomic-habits), which emphasizes the following:
- **Make it obvious**:  Create cues for your habit.
- **Make it attractive**: Utilize habit bundling.
- **Make it easy**:  Reduce friction.
- **Make it Satisfying**:  Use positive reinforcement.

I relocated my phone charger to the power plug next to my toothbrush.
This simple act had multiple effect. Spotting the charger when I brush my teeth serve as a reminder to charge my phone and leave it out the bedroom - thereby *making it obvious*.
Additionally, by combining the habit of leaving my phone outside of the room with brushing teeth, *I make it attractive and easy*. 

A last aspect that I want to mention is that of the alarm clock. Like most people, I used my phone as an alarm clock. To gain independence from that I bought a cheap digital alarm clock.

## Light as Sleep-Wake Signal 

Light plays a vital role in regulating our body's  circadian rhythm, the natural 24-hour cycle that governs our sleep-wake patterns.
For more on this check out the awesome book [Circadian code by Satchin Panda](https://www.goodreads.com/en/book/show/37534452).
By simulating natural light of sunrise and sunset, we can signal our bodies when it time to wake up and when its time to fall asleep. 

Initially, I considered about buying a daylight alarm clock capable of mimicking the light of sunrise and sunset.
However good options like the Philips HF3531 or Lumie Bodyclocks were outside of my price range.

That's where smart lighting solution like smart lamps come into play.
This option is not only affordable but combined with a central server which runs [Home Assistant](https://www.home-assistant.io/) maximal flexible.

In the blog entries in the series "My Homelab", I want to write about how I exactly set up my server, Home Assistant and smart lightning.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:40%" src="/attachments//prosanation_comic.png">
</figure>
{{< /rawhtml >}}


(I really feel like I ignored the bigger issue, and procrastinated by creating this whole elaborated setup, well you will see what I mean in the following posts :P)
