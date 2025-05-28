---
title: 'Server Upgrade or Documentation of my new Homelab'
date: 2024-10-05 21:00:00
tags: ["homelab", "proxmox", "zfs"]
markup:
  tableOfContents:
    startLevel: 1 
    endLevel: 2
Description: "This article details my homelab upgrade, in which I transitioned from a Raspberry Pi 3B to a dedicated server. I share my thought process behind selecting the new server, along with the configurations and software I installed on it."
---


{{< toc >}}

## 0. Changes 

List of Changes Made of This Article:

**15.10.24:** Fixed Typo.  
**23.01.25:** Added a Spacer to the Article.  
**23.05.25:** Added a new Section to Notification Managment.  
**28.05.25:** Added a small Section for Quality Control of Radarr.

## 1. Introduction

For a while now I have been running a Homelab (:= A server that is running at home, often with low budget hardware, hosting several applications.) using a weak Raspberry 3b, originally I was using it to better [regulate my sleep schedule](/articles/my_homelab_part_0_prologue/) using HomeAssistant. But over time the motivation for running my Homelab changed, I wanted to experiment more, learn about various new technologies and more philosophical I wanted to be less dependented on centralized services -- Like, google drive for backups, netflix for entertainment, one drive for syncing devices and many more.

And with this change of motivation my demand for my Homelab increased no longer did I want to run a single application, I wanted to run several applications all at once all containerized and virtualized, my two meager external hard drives dangling of my Rasperry Pi was not adequate anymore for my storage need, I wanted more drives and I wanted them in a
RAID setup for redudancy and with ZFS to prevent bit rot.  
Sadly, my trusted Rasberry 3b was no longer powerfull enough to fullfill my needs, so it was time to upgarde my Homelab to something more powerfull.

This post is a documentation of this upgrading undertaking, first going over the acquirement of the hardware of my homelab, then the proces of choosing a operating system, and finally through the different applications that I selfhosted with it and the different technologies they interface with.

This post will probably rather long, because of the sheer amount of software I decided to selfhost, so grab a cup of coffee or tea and enjoy the reading (or not since this will be a bit dry, I'll try to add some semi funny images).

{{< img src="/attachments/Love.jpg" width="50%" >}}


## 2. The Hardware Requirements

Before I could think about what kind of server I wanted to buy, I first needed to know what my hardware requirements were and how important they were.
This allowed me to balance, my nice-to-have features with the cost of including them. Also, how could I waste hours looking for the perfect server, if I didn't have a lengthy wishlist?

I've already touched on some of my server requirements in the introduction. Now, I would like to explore them in more detail. Below is a list of factors, along with related question, that shaped my final requirements:

- Size of the Computer: USFF, SFF, DT 
    - How many disks fit into the case?
- Motherboard
    - How many SATA connectors do I need?
    - Does it support ECC?
- Disks
    - What disk capacity do I want?
    - Refurbished Disks vs New Disks?
    - How many disks?
- Processor: Intel vs Amd
    - Does it support Quick Sync Video (QSV)?
    - Which processor generation?
    - How many cores do I want?
    - What is it power usage?
    - Does the processor include an onboard graphics card?
- RAM
    - How much RAM?
    - Do I need ECC?
- Power Usage 

{{< addspace height="70px" >}}

### 2.1 Storage Requirements

Using the server as a [NAS](https://en.wikipedia.org/wiki/Network-attached_storage) and as a media center for streaming movies and TV shows to all my devices were two key factors that prompted me to upgrade my Homelab. With the NAS demanding significant storage capacity and the media center needing a more powerful processor than the one I currently had. 
As such I will analyze the requirements of these two functionalities first.

{{< img src="/attachments/it_server.jpg" width="50%" >}}

First of for the NAS, since I want to use my homelab as a media server for movies, tv-shows, music and photos, the most important aspect to consider for the NAS aspect of my server are the storage requirements.
The biggest bulk of required storage will come from my media server, specfically movies and tv-shows. The size of tv-shows is really hard to compare from series to series, they have different amount of seasons, different amount of episodes per season, different length per episode.
Movies on the other side, are a lot more handy, they all have roughtly the same length, making the average file size of a movie fairly repsresentetive.
Allowing me to estimate my required storage needs, by estimating the average file size of movie first and the extrapolate from there.

So I created a table of various popular movies and their file size, by picking some well known movies and search for them on Piratebay, which reports for each torrent various statistics about it such as: used encoding, resolution, Video-Bitrate and many more.  You can see the table below:

{{< table "movie_data" "Source: Piratebay, August. 2024" >}}
| Movie Name                         | Release Year   | Movie Length | Encoding | Resolution | File Size(GB) |
|------------------------------------|--------|--------------|----------|------------|---------------|
| Interstellar                       | 2014   | 2h49m        | x264     | 1080p      | 2.20    |
| Interstellar                       | 2014   | 2h49m        | x264     | 4K         | 14.80   |
| Interstellar                       | 2014   | 2h49m        | remux    | 4K         | 42.71   |
| Pulp Fiction                       | 1994   | 2h34m        | x264     | 1080p      | 1.40    |
| The Silence of the Lambs           | 1991   | 1h58m        | x264     | 1080p      | 1.50    |
| The Silence of the Lambs           | 1991   | 1h58m        | remux    | 1080p      | 31.45   |
| Spirited Away                      | 2001   | 2h4m         | x265     | 1080p      | 7.99    |
| The Departed                       | 2006   | 2h31m        | x264     | 1080p      | 2.00    |
| All Quiet on the Western Front     | 2022   | 2h28m        | x264     | 1080p      | 5.29    |
| Ad Astra                           | 2019   | 2h3m         | x264     | 1080p      | 5.99    |
| Ad Astra                           | 2019   | 2h3m         | x265     | 4K         | 11.37   |
| Jojo Rabbit                        | 2019   | 1h48m        | x264     | 1080p      | 1.93    |
| Jojo Rabbit                        | 2019   | 1h48m        | x265     | 4K         | 6.79    |
| Jojo Rabbit                        | 2019   | 1h48m        | remux    | 4K         | 48.5    |
| Blade Runner 2049                  | 2017   | 2h44m        | x264     | 1080p      | 3.14    |
| Blade Runner 2049                  | 2017   | 2h44m        | x265     | 4K         | 19.2    |
| Blade Runner 2049                  | 2017   | 2h44m        | remux    | 4K         | 77.97   |
| Ex Machina                         | 2015   | 1h48m        | x265     | 1080p      | 1.63    |
| Ex Machina                         | 2015   | 1h48m        | x265     | 4K         | 22.13   |
| The Big Short                      | 2015   | 2h10m        | x264     | 1080p      | 3.28    |
| The Big Short                      | 2015   | 2h10m        | x264     | 1080p      | 3.28    |
| Inception                          | 2010   | 2h28m        | x265     | 1080p      | 2.87    |
| Inception                          | 2010   | 2h28m        | x265     | 4K         | 8.91    |
| The Dark Knight                    | 2008   | 2h32m        | x265     | 1080p      | 1.87    |
{{< /table >}}

You can skip the following boring python code section, which calculates the average movie file size, by collapsing the section and continuing reading from afterwards it:


{{< details "Calculating the Average Movie Length" "true" >}}

{{< info "Info" >}}
For the subsequent calulcations it is important to note, that they are only rough estimates. For example we can have two times the same movie which both use the same encoding, but drastically different file size based on the quality preset choosen when the movie was encoded.
Another example, I have seen a fair number of movies with the same resolution where they differ in encoding one using `x264` and the other one `x265` and even though `x265` is supposed the more efficient one, the file with the `x264` encoding ends up having a smaller file size (this too is the fault of the set quality preset when encoding).
{{< /info >}}

I could have used an calculator to quickly crunch the numbers, but because I like doing it harder than it already is; I used python in combination with pandas, a data anlaysis libary.

The first thing we do is importing the pandas libary and/cap importing our data into python:

```python
import pandas as pd
df = pd.read_csv("movies.txt", sep="|")
df.head()
```

Which will return in the following output:

{{< img src="/attachments/homelab_jupyter_1.jpg" width="100%" >}}

As you can see, there are multiple issues: for one we have two weird columns titld `unamed: 0` and `unamed 7` and second our first row is also weird, we should remove both.

```python
df = df.dropna(how="all", axis="columns") # drops the columns 
df = df.drop(0) # drops the first column 
df.head()
```

Which will result in the following output:


{{< img src="/attachments/homelab_jupyter_2.jpg" width="70%" >}}

There are still one issue persisting, we have whitespaces in the column names and in the data fields, you can see that through the following command:


```python 
df.columns
```

Which will return the following:


```python
Index([' Movie Name                         ', ' Year ', ' Movie Length ',
       ' Encoding ', ' Resolution ', ' File Size(GB) '],
      dtype='object')
```

In order to remove the white-spaces we can do the following:

```python
df = df.rename(columns=lambda x : x.strip()) # strips whitespaces from the columns 
df = df.apply(lambda x: x.str.strip() if x.dtype=="object" else x) # Remove white spaces in the dataframes
```

We have one last problem, when we execute:

```python
df.info()
```

We get:
```python
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 24 entries, 1 to 24
Data columns (total 6 columns):
 #   Column         Non-Null Count  Dtype 
---  ------         --------------  ----- 
 0   Movie Name     24 non-null     object
 1   Year           24 non-null     object
 2   Movie Length   24 non-null     object
 3   Encoding       24 non-null     object
 4   Resolution     24 non-null     object
 5   File Size(GB)  24 non-null     object
dtypes: object(6)
memory usage: 1.3+ KB
```

As we can see the the column `File Size(GB)` is from type `object`, with which we can't calculate, so we need to transform it into the `float` dtype:

```python
df["File Size(GB)"] = pd.to_numeric(df["File Size(GB)"])
```

Finally, we can calculate the average file size:


```python
round(df.loc[df["Resolution"] == "1080p"]["File Size(GB)"].mean(), 2)
round(df.loc[df["Resolution"] == "4K"]["File Size(GB)"].mean(), 2)
round(df.loc[(df["Resolution"] == "4K") & (df["Encoding"] == "remux")]["File Size(GB)"].mean(), 2)
round(df.loc[(df["Resolution"] == "4K") & (df["Encoding"] != "remux")]["File Size(GB)"].mean(), 2)
```

Which gives us the following result:
```
5.05
28.04
26.39
13.87
```
{{< /details >}}

{{< info "Info" >}}
**Remux:** The data was copied without being changed e.g. from the Blueray. It is most often the highest quality, the media can be.
{{< /info>}}

With the previous calculation we get the following table:

{{< table "movie_avg" >}}
|                |Avg. File Size(GB) |
|----------------|-------------------|
|1080p           | 5.05              |
| 4K             | 28.04             |
| 4K & remux     | 26.39             |
| 4K & non remux | 13.87             |
{{< /table >}}


As we can see, the size increase from higher resolution movies is substantial, which makes sense since 4K contains `4` times more pixels than 1080p. Although I haven't personally measured it, with reasonable quality presets, we can expect `x265` encoding to save up to [50%](https://cloudinary.com/guides/video-formats/decoding-the-future-x264-vs-x265) bitrate compared to `x264`. 

Assuming my estimates are accurate, this means we can store roughly 198 movies in 1080p or about 35 movies in 4K per terabyte of disk space. Since I currently don't have any 4K-capable devices, I’ll go with the 1080p estimate.

With that in mind, 1TB should be sufficient for my movie media needs. However, it’s important to remember that movies aren't the only data I plan to store on the server. Additionally, we want to leave room for future expansion should my storage needs increase significantly. What this estimate gives me is a rough idea of the storage I need—not 1000TB or even 100TB, but more likely around 10TB.

{{< img src="/attachments/Titanic.jpg" width="50%" >}}

### 2.2 Processor Requirements

For my processor, there were three important aspects that I needed to consider:
- **Number of Cores**: Since the processor would run in a server environment, more cores would help with concurrency.
- **Power Usage**: Power costs where I live in Germany are rather expensive, so I wanted to minimize them as much as possible.
- **Integrated Graphics Card**: This would help when streaming movies and TV shows from my server to a client.
- **Price**: How expensive the processor is.

I quickly decided that the processor should be from Intel. Intel processors are great for media streaming due to [Quick Sync Video (QSV)](https://en.wikipedia.org/wiki/Intel_Quick_Sync_Video), Intel's video encoding and decoding engine, which excels at handling video formats like movies. Another reason is that Intel processors come with integrated graphics cards, which QSV uses for the encoding/decoding process. Additionally, Intel’s i3 and i5 processors, particularly from the later generations, are very power efficient—perhaps not as efficient as ARM processors, but still quite close.

It was also fairly easy to decide on which generation of CPU I wanted. Anything beyond the 13th generation was a no-go due to [instability issues](https://www.xda-developers.com/intel-13th-gen-14th-gen-crashes/) with the newer models. Anything older than the 5th generation was out of the question because they don’t support QSV. The 9th generation was ideal, as it was the first to support HVEC codecs, making any generation beyond that a solid choice. 

An added benefit of processors from the 8th generation onwards is that the default number of cores increased from 4 to 6, which improves performance a lot for multi task workloads. The 9th generation processors use the UHD 630 as their integrated graphics chip, with the next major performance jump arriving in the 11th generation. For more details on codec support for Intel CPUs, you can refer to the [Media Capabilities Supported by Intel Hardware List](https://www.intel.com/content/www/us/en/docs/onevpl/developer-reference-media-intel-hardware/1-1/overview.html#ENCODE-OVERVIEW-9TH).

Finally, within the Intel Core series, the i9 and i7 models were too expensive, both in terms of price and power usage, leaving me with the option of either an i3, which is more efficient but less performant, or an i5, which consumes more power but offers better performance.

To recap, I am looking for an Intel i3 or i5 processor, preferably from the 9th generation, with the 11th generation as an even better option.


### 2.3 Computer Size

A quick note on the size of the computer: I wanted a server that had enough space for my disks but was still compact enough to fit comfortably in the corner of a room. Because of this, I primarily focused on small form factor (SFF) computer cases.

{{< img src="/attachments/desktop_size.jpg" width="50%" >}}

### 2.4 RAM Requirements

Regarding RAM, there isn’t much to say—you only need as much memory as you actually use (unless you're doing something extreme like using [ZFS Deduplication](https://www.truenas.com/docs/references/zfsdeduplication/)). I'll start with a modest amount and buy more when needed. Scalability isn’t a big concern, as most modern motherboards have four slots for RAM sticks. 

One thing worth mentioning is that having [ECC RAM](https://www.truenas.com/docs/references/zfsdeduplication/) would be nice, but it’s not essential, especially for a small home setup like mine and it is rather expensive.


### 2.5 Short Interlude

From the decisions I’ve made so far, you’ve probably noticed that this server sounds more like a consumer desktop computer than a sleek, rack-mounted server. And that’s true, but in my defense, "real" servers are both expensive and power-hungry. Compared to my previous server (a Raspberry Pi 3b), this is already a significant upgrade.

{{< img src="/attachments/server_meme.webp" width="60%" >}}

## 3. Dr. Salesman or: How I Learned to Stop Waiting for the Perfect Deal

Now that we've gone through the server requirements, it was time to actually make the purchase. The first option I considered was buying all the parts separately and building it myself. However, after using [pcpartpicker](https://pcpartpicker.com/), I arrived at a total cost of around 600€, which was more than I wanted to spend. I could have bought the parts used and individually, which would have saved me a lot of money, but it also carried the risk of purchasing faulty components or exceeding my budget if I didn't track the expenses closely.

So, I went with my second option: shopping for used office computers that met my specifications. Initially, I tried several random websites, but I eventually shifted my focus entirely to [eBay](https://www.ebay.com/), where I spent about two weeks checking deals every day before finding something that worked for me. There are certain manufacturers and product lines that work well as servers, such as:
- Fujitsu Thin Clients
- Dell Wyse
- Dell Optiplex
- HP ProDesk

Just keep in mind that different versions of these machines exist, and some are better suited than others. I'd recommend monitoring eBay for a while to get a feel for the prices, and when you see a good deal, go for it.

The only components I bought separately were the hard disks and, later, additional RAM when I needed it. For disks, many people recommend [Server Part Deals](https://serverpartdeals.com/collections/manufacturer-recertified-drives), but using [DiskPrices](https://diskprices.com/), I ended up purchasing my drives from Amazon.

Here’s a breakdown of my final costs:
- HP ProDesk 600 G5 (16GB RAM, i5-9500, 250GB SSD): 180€
- Kingston Fury Beast DDR4 2x32GB RAM: 120€
- 1x Intenso SSD 256GB: 20€
- 2x Seagate Enterprise v6 10TB ST10000NM0046: 220€

**Total**: 540€

It turned out to be a bit more expensive than I initially expected, mostly because I underestimated the cost of RAM and hard disks.

{{< img src="/attachments/naked.jpg" width="50%" >}}

## 4. A look inside the Machine

I thought I had taken a photo when the machine first arrived, but I didn’t, so here’s how the computer is currently set up. On top of the computer are two hard disks that I use for regular backups. You can’t really see them in the photo, but just because they’re not visible doesn’t mean they’re not there!

{{< img src="/attachments/server_imgs/IMG_20240927_204550120.jpg" width="50%" >}}

Below you can see how I installed the disks into the machine. The ProDesk 600 G5 has exactly four SATA connectors, which is just enough for the disks I needed. I had to get a bit creative with the mounting spots -— Yes, I did use duct tape to mount them.

{{< rawhtml >}}
<figure style="display: flex; justify-content: center;" height="235px">
    <img loading="lazy" style="width: 50%;" src="/attachments/server_imgs/IMG_20240815_234023627.jpg">
    <img loading="lazy" style="width: 50%;" src="/attachments/server_imgs/IMG_20240815_234153914.jpg">
</figure>
{{< /rawhtml >}}


## 5. My Storage Situtation

Before discussing the operating system I chose, I want to first touch on my storage setup. As mentioned earlier, I purchased two 10TB hard drives and a 256GB SSD, in addition to the 256GB SSD that came with the computer. I also had two 1TB external disks lying around that I wanted to use.

The big question now is: which disks should be responsible for what? Should I separate data from running software and configuration files? Should I use some disks for backup? Should I set up the drives in a RAID system? Should I go for hardware or software RAID? These and many other questions arose as I planned the setup.

### 5.1 What is RAID?

To better explain my decision on how I use the disks, I’d like to briefly introduce what RAID is.

**Redundant Array of Independent Disks (RAID)** is a system used to organize disk storage. It is a data virtualization technology that combines multiple physical disks into one logical unit, typically for performance gains, redundancy, or both. There isn’t a single RAID system; instead, there are multiple RAID levels, each with its own set of advantages and disadvantages. These levels are identified by numbers, which uniquely define the configuration and capabilities of each system.

In **RAID-0**, also known as **striping**, multiple disks are combined into one by distributing the data across the disks in rows, as shown in the image below. This configuration has one major advantage: performance. Since consecutive sectors are spread across different disks, when we need to access a large block of data, we can read from multiple disks simultaneously. This parallel access significantly increases bandwidth compared to accessing data from just one disk, which would be limited by the bandwidth of that single device.

However, RAID-0 also has a major disadvantage. If any of the disks in the RAID array fails, the data on that disk is permanently lost, with no chance of recovery. This can be catastrophic, as the lost sectors could be part of critical data, rendering the entire dataset unusable.

{{< img src="/attachments/RAID_0.png" width="30%" >}}

In **RAID-1**, also known as **mirroring**, two disks are synchronized so that when data is written to one disk, it is simultaneously written to the other. This ensures that at all times, you have two copies of your data. If one disk fails, the other still holds a complete copy, providing redundancy as the main benefit.

However, this setup comes with a downside: you sacrifice 50% of your storage capacity for redundancy, which can be costly. For example, if you buy two 10TB hard drives for €120 each, instead of having 20TB of usable storage, you only get 10TB because the other 10TB is used for mirroring, "wasting" 120€ in the process.

{{< img src="/attachments/RAID_1.png" width="30%" >}}

RAID-0 and RAID-1 can be combined into a setup called **RAID-01**, which provides both the redundancy of mirroring and the performance gains of striping. RAID-01 works by first striping the data across disks and then mirroring those striped sets. 

With RAID-01, the performance improvement is even greater than with RAID-0 because now you can read from four disks simultaneously and write to two disks at the same time. This results in 4x read access and 2x write access.

The disadvantage of RAID-01 is that it requires at least four disks, and like with RAID-1, you lose 50% of your storage to redundancy. However, this redundancy allows one disk to fail without any data loss.

{{< img src="/attachments/RAID_01.png" width="50%" >}}

The last RAID system I want to introduce is **RAID-5**. To use RAID-5, you need at least three disks. Like RAID-0, it uses striping to improve performance. However, RAID-5 also provides redundancy, allowing for the failure of one disk without data loss.

This redundancy is achieved by using parity blocks, which are distributed across all the disks. If one disk fails, the system can use these parity blocks to reconstruct the missing data. However, after a disk failure, it may take some time to rebuild and restore full access to all data. RAID-5 is one of the most cost-efficient RAID setups, offering a good balance between performance, redundancy, and storage capacity.

{{< img src="/attachments/RAID_5.png" width="50%" >}}

There are many more RAID systems than the ones I’ve introduced, but these are some of the most important ones, especially for my use case. You can use the [raid-calculator](https://www.raid-calculator.com/) to explore more options.

### 5.2 The Magical Filesystem: ZFS

There are many file systems available to choose from, ranging from long-established ones like EXT4 and Windows-compatible NTFS to more modern options like Btrfs and the relatively new [drama-infested](https://www.phoronix.com/news/Linus-Torvalds-Bcachefs-Regrets) file system, Bcachefs. Each of these file systems has its own strengths and weaknesses. 

However, I want to briefly discuss a special file system called **Zettabyte File System (ZFS)**. ZFS has been around in some shape or form since 2001, but it only became widely available on Linux in 2010. It offers some really powerful features. While I won’t provide a comprehensive overview, there are many guides that do a far better job than I ever could, I want like to highlight some of its cool features:
- **Natively supports RAID storage.**
- **Prevents [bit rot](https://en.wikipedia.org/wiki/Data_degradation)** through automatic checksum calculation, enabling silent self-healing of data.
- **Allows for automatic backups and version rollback** through snapshots.
- **Natively supports data compression**, including for snapshots and deduplication.

Although ZFS is quite impressive, it is [not perfect](https://blog.fosketts.net/2017/07/10/zfs-best-filesystem-now/) and can be somewhat inflexible, along with having a few other issues.

### 5.3 The Storage Plan

{{< info "Info" >}}
Normally, when building a RAID system, it's advisable to buy disks from separate brands to reduce the likelihood that multiple disks will fail at the same time. I didn’t follow this guideline, so we’ll see if that decision comes back to bite me.
{{< /info >}}


To recap, my available storage consists of:
- 2x 256GB SSDs
- 2x 10TB hard drives
- 2x 1TB external disks

The most important aspect for my server was redundancy. While extra performance would be nice, it was not essential for the type of software and use cases I planned to run, which excluded RAID-0. Additionally, since I only purchased two of each disk type, RAID-01 and RAID-5 were not viable options.

For a while, I considered buying additional disks to meet the three-disk requirement for RAID-5. However, the HP ProDesk 600 G5 I purchased didn’t have enough SATA connectors, and I would have had to buy an [HBA card](https://www.techtarget.com/searchstorage/definition/host-bus-adapter), which seemed like too much work and expense.

Ultimately, I settled on the following setup:
- SSDs in a RAID mirror configuration with ZFS for the operating system and running software.
- HDDs in a RAID mirror configuration with ZFS for all my data, such as movies and photos.
- External disks in a RAID mirror configuration with ZFS for backups.

{{< img src="/attachments/seattle.jpg" width="50%" >}}


## 6. The Server Operating System: Proxmox

For the Operating System, I decided to use [Proxmox](https://www.proxmox.com/en/), which is an open-source virtualization platform. A virtualization platform allows you to quickly spin up containers and virtual machines to run programs in isolated environments. You might ask yourself, "What is the benefit of virtualizing my programs?"

I'm glad you asked, there are numerous benefits:

- **Increased Security:** Virtualization which containers your programs, enhances security. If one container is compromised, it’s very difficult for an attacker to escalate the breach to the entire system.
- **Avoiding Dependency Conflicts:** If you install everything directly on bare metal, you might run into a major issue: different programs may have conflicting dependencies. This can land you in "dependency hell," resulting in a bloated system. For instance, have you ever (accidentally, of course) installed some programs that depend on [Wayland](https://en.wikipedia.org/wiki/Wayland_(protocol)) and others that depend on [X.Org](https://en.wikipedia.org/wiki/X.Org_Server)? Then, when you try to remove one of them, you find yourself having to reinstall everything. Not fun, right?
- **Impact of Failure:** Virtualization ensures that if one of your containers fails, whether due to an update or something else, it won’t affect the rest of your system. This minimizes the impact a single program failure can have.
- **Ease of Management:** Managing your software becomes much simpler. You can start or stop containers in seconds, configure them to start on boot, duplicate them easily, and even limit how many resources each container is allowed to use.
- **Simplified Backup:** Backing up your software i.e. configurations and data, is also straightforward with containers. You can even back up the running state, minimizing downtime during the process.
- **Dynamic Load Balancing:** Finally, if you have multiple servers, you can combine them into one large data center cluster. This allows you to dynamically balance server loads, where a container can be moved from one server to another to reduce the load. If one server goes down, containers can be transferred to another, improving uptime.

You could also get all these benefits without using Proxmox by running an operating system like Debian or Arch with Docker or LXC. However, Proxmox provides a convenient web-based GUI that makes managing containers much easier.

{{< img src="/attachments/proxmox.jpg" width="90%" figcaption=" An example of my Proxmox setup." >}}


### 6.1 Proxmox: Installation

Setting up Proxmox is fairly straightforward. First, download the [ISO](https://www.proxmox.com/en/downloads/proxmox-virtual-environment/iso) and create a bootable medium. I recommend using a USB stick, and one tool you can use for this is [Popsicle](https://github.com/pop-os/popsicle).

Next, ramm the USB stick with all the force you can into the correct port of your newly purchased computer (trust me, it helps!). Boot up the computer, enter the BIOS/EFI settings, and select the USB stick as the boot device. Then, follow the [installation guide](https://pve.proxmox.com/wiki/Installation). You’ll need a monitor, keyboard, and mouse during the installation process, but once it's done, you can safely disconnect them.

When you reach the screen where you need to choose the installation destination and if you’re following the same set-up as me, select ZFS with RAID 1 and choose the two SSDs as the target disks. We’ll deal with the external disks and hard drives later.

{{< img src="/attachments/proxmox_setup_select_disks.png" width="80%" >}}

When prompted to create an account, I highly recommend using a real email (or even creating a separate email just for your server). This will allow you to receive regular reports on backups and alerts when something goes wrong, such as a hard disk failure.

{{< img src="/attachments/pve-set-password.png" width="80%" >}}

For the network configuration, make sure to select an IP address that is actually free. You can check your router to see the currently occupied addresses. Your DNS server will most likely be your router, so enter its address. The netmask will probably be `255.255.255.0`, but verify this with your router to be sure.

{{< img src="/attachments/pve-setup-network.png" width="80%" >}}

After the installation is complete, you can remove all peripherals and connect to your Proxmox server via the selected IP address and port 8006: `http://<selected-ip>:8006`.

### 6.2 Proxmox: Post Installation Steps

After connecting to Proxmox via the web app, you’ll be prompted to log in. Use the login credentials you created during the installation process, and make sure to write them down somewhere —- It would really suck to forget them. The default username is `root`. When logging in, ensure that `PAM` is selected as the *realm*, or you won’t be able to connect.

#### 6.2.1 Activating No-Subscription Repo

The first thing you’ll probably want to do is enable the "No-Subscription Repository" for updates. To do this, navigate to: `machine (pve) -> Updates -> Repositories -> Add -> No-Subscription`.

{{< img src="/attachments/gui-node-repositories.png" width="80%" >}}

After you have enabled the community repository, you can update Proxmox by navigating to: `machine (pve) -> Updates -> press refresh & press upgrade`.

{{< img src="/attachments/proxmox_update.jpg" width="80%" >}}

#### 6.2.2 Creating ZFS-Pool

Next, we want to create a ZFS pool for the four remaining disks (the two external ones and the two hard drives). To do this, navigate to: `machine (pve) -> Disks -> ZFS -> Create ZFS`. For the RAID level, select `Mirror`, and leave compression set to `on`. This will slightly reduce performance, but you'll save disk space. Do this once for the external drives and name the pool `backups`, then repeat this for the hard drives and name the pool `data`.

{{< img src="/attachments/proxmox_zfs.jpg" width="80%" >}}

If you are finished, this should look like this:

{{< img src="/attachments/proxmox_zfs_overview.jpg" width="80%" >}}

#### 6.2.3 Check Disks S.M.A.R.T Settings

Next, we want to check if [S.M.A.R.T. monitoring](https://en.wikipedia.org/wiki/Self-Monitoring,_Analysis_and_Reporting_Technology) is enabled and functioning. S.M.A.R.T. is a vital monitoring service that performs checks to detect the health of HDDs and SSDs, which is crucial when running a server, as disk failures can happen easily through the constant disk usage. Navigate to: `machine (pve) -> Disks` you can then select the disks and press the `Show S.M.A.R.T values` button. This should similar to this:

{{< img src="/attachments/proxmox_smart_values.jpg" width="80%" >}}

#### 6.2.4 IOMMU

If you plan to use a graphics card or other PCIe devices inside your containers and VMs, you'll need to enable *IOMMU*. This can be done in your computer's BIOS. The exact steps vary depending on the manufacturer, so I won’t provide further details here. Later, when this is really important I will say more to this.

## 7. Creating Our Data Vault with OpenMediaVault NAS

I wanted one central service to manage all the data on my disks. Typically, you'd use an external NAS in addition to your server, which helps with redundancy—if the server fails, your data is still safe on another device. However, since I’m as poor as a church mouse, I need to combine the server and NAS into one system.

To achieve this, I’ll use a VM running the [Openmediavault](https://www.openmediavault.org/) operating system. It provides a nice graphical interface for managing permissions and shared folders. Initially, I considered using software like [Cockpit](https://github.com/45Drives/cockpit-file-sharing) to create NFS shares instead of a full NAS operating system, but I ultimately decided that using a full VM as a NAS would make the process easier.

### 7.1 Openmediavault: Installation

The first step is to download the OpenMediaVault [ISO](https://www.openmediavault.org/download.html) to your computer. After that, you can upload it to the server by navigating to: `local -> ISO Images -> Upload`.

{{< img src="/attachments/proxmox_upload.jpg" width="80%" >}}

After this you can press the big blue button with the text `Create VM` in the top right to create a virtual machine. For the storage choose `local` we want the VM to run on the SSDs, choose `openmediavault` as ISO image, for the hardware 1 core with 6GB RAM and 32GB disk space should be enough.

{{< img src="/attachments/proxmox_nas.jpg" width="80%" >}}

In the Proxmox sidebar, you can now double-click on the NAS, which will open a new browser window, allowing you to access the NAS interface. You should be able to see the IP address in the terminal. Alternatively, you can copy the IP address and use proper remote access software to connect to the NAS. The default login name when connecting via ssh is `root`.

OpenMediaVault (OMV) should now be available as a web service. This means you can open your browser and enter `http://<nas-ip-address>`, where you'll be greeted by a login screen. The default login credentials are `admin` as the username and `openmediavault` as the password. After logging in, you should see the OMV dashboard (your version might look slightly different).

{{< img src="/attachments/omv_dashboard.jpg" width="80%" >}}

### 7.2 Openmediavault: Post-Installation Steps

The first thing you should do is change the default password. Click on the person icon in the top right corner and select `Change Password`. Next, we want to create a filesystem that we can later use for all our data. Navigate to: `Storage -> File System -> Create`. Since we are already using ZFS for the underlying disks, be sure to choose `ext4` as the file system. You can mount the file system by pressing the play button while having selected the new file system.

{{< img src="/attachments/omv_file_system.jpg" width="80%" >}}

Next, we want to create a user who will be able to access the data on the file system over the network. To do this, navigate to `Users -> Create`. 

Once you've created the user, we can finally set up a shared folder, which will allow access to its data as long as you are connected to the network. Go to: `Storage -> Shared Folders -> Create`, give it a name, and select the new file system.

After creating the shared folder, you need to grant your newly created user permissions to access it. Select your shared folder and click on `Permissions`, where you can assign read or read-and-write access to users.

In the end, we need to enable the SAMBA service and add our shared folder to it, to make it accessible. For this navigate to: `Service -> SMB -> Settings -> Enable` and then `Services -> SMB -> Shares -> Create` select your previous created shared folder. Make sure to save the changes in OMV.

You should now be able to connect to your shared folder via your file manager both in linux and windows.

{{< img src="/attachments/nas_access.jpg" width="80%" >}}

## 8. Simplifying Your URLs with Nginx Proxy Manager

[Nginx Proxy Manager](https://nginxproxymanager.com/) is, as you might have guessed from the name, a proxy manager. A proxy manager is essentially a central routing service through which all requests to access a service must pass. This setup enhances security and simplifies access to those services. If you'd like to learn more about proxy managers, you can check out a previous article of mine on the [Caddy Proxy Manager](/articles/my_homelab_part_9_caddy_fileserver_and_duckdns/). In this article, however, I'll focus on how I installed Nginx Proxy Manager.

### 8.1 Nginx Proxy Manager: Installation

For the installation, I used the [Proxmox Helper Scripts by tteck](https://tteck.github.io/Proxmox/). I installed the service on the SSD ZFS dataset. To install Nginx Proxy Manager, simply copy the helper command from the website and paste it into the terminal of your Proxmox machine (`pve`). You'll then be greeted by the *tteck* installation script, which will guide you through the installation process.

{{< img src="/attachments/proxmox_nginx_installation.jpg" width="80%" >}}

Once the installation process is complete, you should see a new container under your Proxmox machine (`pve`) in the sidebar. You can click on it to view its details. In the top-right corner, you'll find options to start or shut down the container. Under the `Options` tab, you can enable the container to start automatically if you wish.

Similar to the OpenMediaVault virtual machine, you can double-click the new Nginx container to connect to it. In the container's shell, use the command `hostname -I` to view its IP address. Once you have the IP, you can connect to the Nginx web service by visiting `http://<your_ip>/admin`. The default login is `admin@example.com`, with the password `changeme`. As the name suggests, make sure to change both the email and password in the Nginx settings.

{{< img src="/attachments/nginx_home.jpg" width="80%" >}}

You can use [DuckDns](https://www.duckdns.org/) to make your service accessible via a domain name like `myverycoolserver.duckdns.org`. However, to use this with Nginx Proxy Manager, you first need to install its dependencies. You can do this by accessing the container's shell and typing: `pip install certbot_dns_duckdns`.

At this point, you have two options: 
1. You can make your services (currently just Nginx, but later we’ll install more) accessible from anywhere on the internet.
2. You can restrict access to your services so they are only available on your local network.

I chose the second option. Making your services accessible over the internet can be risky, as it allows attackers to potentially infiltrate your home network. I recommend doing this only if you're confident in securing your setup.

To proceed with the second option, go to DuckDns (although you can also use a purchased domain or another free domain name service, but for this guide, I’ll use DuckDns). Once logged in, create a new domain by entering a name in the `subdomains` field. 

After creating the domain, it will point to your **external IP address**. Since we only want to access the service on the local network, you’ll need to change this to the **local IP address** of your Nginx Proxy Manager. This is the same IP you used to access Nginx through your browser. For example, my local IP address follows the format `192.168.xxx.xxx`, but this may vary for you.

{{< img src="/attachments/duckdns.jpg" width="80%" >}}

We can now make Proxmox and Nginx Proxy Manager accessible through your newly created domain. If you want your service to be accessible via `https` (instead of just `http`), you can use [Let’s Encrypt](https://letsencrypt.org/), which provides free certificates for your domain using ACME challenges. Fortunately, Nginx can handle this automatically. 

Go to the Nginx web interface and navigate to `SSL Certificates -> Add SSL Certificate`. Choose `Let’s Encrypt`, and for the domain name, enter two entries: `<your_domain>` and `*.<your_domain>` from DuckDns. The `*` in front of your domain is called a *wildcard* and allows you to secure subdomains like `proxmox.<your_domain>`, which is very useful for all the services we will add here later on.

Activate the slider for the `DNS challenge`, select DuckDns as the provider, and enter your DuckDns token (you can find it under your email address when logged into DuckDns). After this, press save. It may take some time for the certificate to fully propagate, so if there’s a delay, you can edit the SSL certificate and increase the propagation time.

Now, let’s add your first proxy. Go to `Hosts -> Proxy Hosts -> Add Proxy Host`. Enter the domain name you want for your service. For Nginx, I recommend using just your domain name, and for Proxmox, use something like `prox.<your_domain>`. Don't forget to select the SSL certificate you created earlier, I also recommend to enable *Force SSL* and *HTTP/2 Support*.

{{< rawhtml >}}
<figure style="display: flex; justify-content: center;" height="367px">
    <img loading="lazy" style="width: 40%;" src="/attachments/nginx_proxy_1.jpg">
    <img loading="lazy" style="width: 50%;" src="/attachments/nginx_proxy_2.jpg">
</figure>
{{< /rawhtml >}}

In principle, you can add all the services you self-host that are accessible via an IP address to Nginx Proxy Manager. This will allow you to access them using a domain name instead of needing to remember the IP address. However, some services may not work right out of the box with the proxy manager and might require additional configurations, such as Home Assistant.

## 9. Vaultwarden the Password Manager

I’ve also previously written about [Vaultwarden](https://github.com/dani-garcia/vaultwarden) in a [prior post](/articles/my_homelab_part_10_vaultwarden/). To recap, it’s a self-hosted, free, open-source password manager based on the popular Bitwarden software.

Vaultwarden can be easily installed using the [Proxmox Helper Scripts by tteck](https://tteck.github.io/Proxmox/), I recommend isntalling it on the local SSD ZFS dataset. Once installed, you can add it to the list of proxy hosts in Nginx, as shown in the previous section. Just remember, when adding a service to Nginx, you should use the **internal IP address** (the one you use to access the service, which you can find using the command `hostname -I` in the container's shell), not the **external IP address**.

## 10. News Aggregation with FreshRSS

[Really Simple Syndication (RSS)](https://en.wikipedia.org/wiki/RSS) is a protocol used for news aggregation. Websites can offer an RSS feed that users can subscribe to, allowing newly released information on the feed to be forwarded directly to the user's RSS client. The content of an RSS feed can vary widely, though most of it is text-based. It can also notify users of new podcast episodes, among other updates. [FreshRSS](https://github.com/FreshRSS/FreshRSS) is one of these RSS clients, that is selfhosted free and open source.

**Why use RSS?**  
Nowadays, more and more platforms use automated [recommendation systems](https://www.nvidia.com/en-us/glossary/recommendation-system/) to suggest new content. Whether it's social media like Facebook, or even worse, TikTok—where all content is driven by recommendation algorithms—or the news pages on Android phones or Windows machines, the trend is the same.
I believe that, on a large scale, these recommendation systems are unhealthy for society. They are optimized for user retention, which often leads to the promotion of more extreme content. *AlmostFridayTv* has a great semi-related [sketch on this](https://www.youtube.com/watch?v=jZkGqlq8xwE), which I highly recommend.
This is where RSS comes in. It gives people the power to take control back from the algorithm by allowing them to curate their own news feed, free from the influence of any recommendation system.

### 10.1 Installation FreshRSS

The installation for this setup is a bit more complicated than for Vaultwarden since there isn’t a single script available. However, we can use tteck’s [Docker LXC](https://tteck.github.io/Proxmox/#docker-lxc) script and then utilize Docker Compose. Just like with Vaultwarden, copy the command from tteck’s page and paste it into the shell of your Proxmox machine (`pve`). Be sure to use the first link, not the second one, which is based on an Alpine container. When asked whether you want to install additional software, only agree to `docker-compose`.

Once the installation is complete, a new container should appear in your Proxmox sidebar. It’s a good idea to give it a more specific name, which you can do under `DNS -> Hostname`. Enter the container’s shell, as we’ll now create a `docker-compose` file to define the settings for your software. I’ve discussed this process in more detail in my posts [My Homelab Part 1: Introduction](http://localhost:1313/articles/my_homelab_part_1_introduction/) and [My Homelab Part 3: Calibre](/articles/my_homelab_part_3_calibre/), if you’d like to learn more.

You can create the `docker-compose.yaml` file using `vi` or `nano`. If you prefer another editor, you can install it using `apt-get`, for example, `apt-get install vim`. Once the file is created, add the following content to it:
```yaml
version: "2.4"

volumes:
  data:
  extensions:

services:
  freshrss:
    image: freshrss/freshrss:latest
    container_name: freshrss
    hostname: freshrss
    restart: unless-stopped
    volumes:
      - ./rss/data:/var/www/FreshRSS/data
      - ./rss/extensions:/var/www/FreshRSS/extensions
    environment:
      TZ: Europe/Berlin
      CRON_MIN: '3,33'
    ports:      
      - "8080:80"
```

After you’ve created the `docker-compose.yaml` file, you can run the software using the command:

```bash
docker compose -f docker-compose.yaml up -d
```

To check the status of the running Docker containers, you can use the command:

```bash
docker ps -a
```

The output should look similar to this:

{{< img src="/attachments/freshrss_docker.jpg" width="100%" >}}

As with the previous services, you should be able to connect to the web service using the container's IP address and port `8080`. The URL will look like this: `http://<your_ip>:8080`. With this setup, you now have a central server for aggregating news and blog posts.

{{< img src="/attachments/freshrss_home.jpg" width="80%" >}}

Your site’s appearance can be customized under `Settings -> Display -> Theme`. Here, you can change the look of your RSS reader. Personally, I prefer the Nord theme, which is also what you can see in the image above.

If you're behind a reverse proxy like Nginx, you may need to change the base address of FreshRSS. To check this, visit `https://<your_domain>/api/`. If you receive a warning or see the IP address instead of the domain name, you'll need to update the base URL.

To do this:
1. Shut down FreshRSS by running the command `docker stop freshrss`.
2. Enter the config folder via the container's shell and look for the `data/config.php` file.
3. Open the file and change the base URL to match your domain name.
4. Once done, restart FreshRSS with `docker start freshrss`.

You can verify if the base URL is set correctly by going to `Settings -> System Configuration -> Base URL`.

### 10.2 Third Party Clients

You have now a central website from which you can read blog posts from, but maybe you want to read some of RSS content offline, for that you can use client that synchronizes your read articles and favourites with your server. A full list of compatible clients can be found [here](https://github.com/FreshRSS/FreshRSS?tab=readme-ov-file#apis--native-apps). I personally use [RSSGuard](https://github.com/martinrotter/rssguard) for my windows laptop and [Read You](https://github.com/Ashinch/ReadYou/) for my phone.

{{< img src="/attachments/read_you_rss.png" width="30%" >}}

To allow clients to synchronize with your FreshRSS instance, you first need to enable this. Navigate to `Settings -> Authentication` and check the box for `Allow API Access`. Then, go to the `Profile` section in settings and fill in the `API password` field. This will be the password required to log in from your clients.

To synchronize the *Read You* app with your server, go to `Settings -> Accounts -> Add Account -> FreshRSS`. When adding the URL, make sure to append the following suffix: `/api/greader.php`. For more details, you can refer to this [guide](https://freshrss.github.io/FreshRSS/en/users/06_Mobile_access.html).

## 11. Managing Your Cooking Recipes with Tandoor

[Tandoor](https://github.com/TandoorRecipes/recipes) is a self-hosted, free, open-source recipe manager. It allows you to create recipes, meal plans, and shopping lists, save them on your server, and make them accessible to your entire network.

{{< img src="/attachments/tandoor_example.jpg" width="80%" >}}

The service is easy to install, thanks to the [tteck script](https://tteck.github.io/Proxmox/#tandoor-recipes-lxc). After installation, all you need to do is create a user and a workspace, and then you can start creating recipes.

By default, Tandoor doesn’t come with any ingredients preloaded. You can manually create ingredients for each recipe, or alternatively, you can import pre-existing ingredients. To do this, go to `Space Settings -> Open Data Importer`, choose the language (`en` for English), select the items you want, and press `Import`.

## 12. Service Dashboard with Homarr

By now, we have a good number of services running. Even though they’re behind a reverse proxy with easily remembered names, as the number of services grows, it might become difficult to remember how to access each one.

This is where [Homarr](https://github.com/ajnart/homarr) comes in. Homarr is a modern dashboard that centralizes all your services in one place, making it easy to access everything. It’s easily configurable through its web interface and offers many widget integrations with different apps.

There are plenty of other dashboard services out there, such as [Dashy](https://github.com/Lissy93/dashy), [Glance](https://github.com/glanceapp/glance), [Homepage](https://github.com/gethomepage/homepage), and many more. The exact dashboard you choose is largely a matter of personal preference, as they all function similarly. I chose Homarr because it had a [tteck script](https://tteck.github.io/Proxmox/#homarr-lxc) available, making installation easier.

{{< img src="/attachments/homarr.jpg" width="80%" >}}

To add a service to Homarr, click on the *Edit Mode* button in the top-right corner. Once in edit mode, you can add new tiles by clicking the button in the top-right corner again. These tiles can be a service, a widget, or a category, which can be used to group services together.

## 13. Torrenting All the Media You Want with the Arr-Stack

{{< info "Info" >}}
**Torrenting** is the act of downloading and uploading files through the BitTorrent network. Instead of downloading from a central server, users download and upload files to each other in a process called peer-to-peer (P2P) file sharing. Each torrent has a `.torrent` file associated with it, which contains metadata about the files and folders being shared, as well as a list of *trackers* that help participants find each other.  

**Torrent Trackers** are a special type of server that assist in the communication between peers. They keep track of where file copies reside on peer machines, which ones are available, and help coordinate the transmission and reassembly of the files being shared.
{{< /info >}}


The **arr-stack** is a suite of software used to manage and automate the torrenting of media, such as movies, TV shows, music, and books. The exact composition of the arr-stack can vary, but my setup includes the following:

- **Torrent Client:** This is responsible for the actual torrenting process. Popular options include [Transmission](https://github.com/transmission/transmission) and [qBittorrent](https://github.com/qbittorrent/qBittorrent).
- **VPN:** A VPN is crucial to hide your torrenting activity, especially if torrenting is illegal in your country. I use [AirVPN](https://airvpn.org/), which supports port forwarding—an important feature for torrenting.
- **Media Management Tools:** These tools help organize and automate media downloading.
    - [Sonarr](https://github.com/Sonarr/Sonarr): Manages TV shows.
    - [Radarr](https://github.com/Radarr/Radarr): Manages movies.
    - [Lidarr](https://github.com/Lidarr/Lidarr): Manages music.
    - [Readarr](https://github.com/Readarr/Readarr): Manages books.
- **[Jellyseerr](https://github.com/Fallenbagel/jellyseerr):** A tool for managing media requests, allowing users to request new movies or TV shows for the library.
- **[Gluetun](https://github.com/qdm12/gluetun):** A VPN client running inside a Docker container, supporting multiple VPN providers.

I won’t go into too much detail since there are already many excellent guides on the topic, such as:
- [Self-host an automated Jellyfin media streaming Stack](https://zerodya.net/self-host-jellyfin-media-streaming-stack/)
- [Plex and the *ARR stack](https://sysblob.com/posts/plex/)
- [Docker Compose Arr Stack](https://mafyuh.com/posts/docker-arr-stack-guide/)

As a basic overview, Jellyseerr provides a Netflix-like interface where users can request media (movies or TV shows). These requests are forwarded to Radarr for movies and to Sonarr for TV shows. These tools, in turn, forward the requests to Prowlarr (or Jackett), which searches for torrents and sends them to the torrent client (in my case, qBittorrent, though Transmission is another option). Once the torrent is downloaded, the media becomes available in Jellyfin for consumption. 

Everything runs inside a Docker container with Gluetun, which tunnels all network activity from qBittorrent through the VPN. If downloading `.torrent` files is illegal in your country, you should also route the network activity of Prowlarr, Sonarr, and Radarr through the VPN.

{{< img src="/attachments/mediastack.png" width="100%" figcaption="Image is from <i>zerodya</i>. In my setup, I use <i>Prowlarr</i> instead of Jackett and <i>qBittorrent</i> instead of Transmission." >}}

### 13.1 Installation: Torrenting Stack

The first step is to set up a virtual machine (VM) for the arr-stack. I chose **Debian 12** as the operating system, which you can download [here](https://www.debian.org/download). Like we did with the NAS and OpenMediaVault setup, first, download the ISO file and upload it to your Proxmox server.

Once the ISO is uploaded, we can create the VM. Here are the settings that worked well for me:
- **8GB RAM**
- **32GB Disk Space** (on the SSD, i.e., the local ZFS dataset)
- **2 Processors**

Since the local ZFS dataset doesn't have enough space to store all the movies, we want to save the torrented media on our **data** ZFS dataset instead. To do this, follow these steps:

1. Enter the shell of the newly created VM and install **cifs-utils** to enable the VM to connect to shared folders on your NAS via SAMBA. Run:
   ```bash
   apt install cifs-utils
   ```

2. On OpenMediaVault, create a new shared folder called `media_root` and share it via SAMBA.

3. On your VM, create a corresponding folder to mount this shared folder:
   ```bash
   cd /mnt/ && mkdir media_root
   ```

4. Now, add an entry to your **fstab** file to automatically mount the newly created SAMBA directory on your VM. Open the `fstab` file with:
   ```bash
   nano /etc/fstab
   ```
   Add the following entry to the file:
   ```bash
   //<your_nas_ip>/media_root /mnt/media_root cifs _netdev,x-systemd.automount,noatime,uid=1000,gid=1000,dir_mode=0770,file_mode=0770,credentials=/etc/smbcredentials
   ```
5. Create a new credentials file in the `etc` directory, in this we will save in plaintext the username and password used to connect to the SMB share:
    ```bash
    nano /etc/smbcredentials
    ```
    The file shoud be in the following format:
    ```bash
    username=xxxx
    password=xxxx
    ```

6. After creating the credential file, restart your VM:
   ```bash
   reboot
   ```

7. Once your VM is restarted, the `media_root` folder should be mounted. I recommend setting up your folders by following the [Trash folder structure guide](https://trash-guides.info/Hardlinks/How-to-setup-for/Docker/).

8. A final note is that the *arr-stack* depends on *OpenMediaVault (OMV)* already running, as it uses the Samba drives from *OMV*. Therefore, you should change the reboot order: set *arr-stack* to order 2 and *OMV* to order 1. It’s advisable to add a slight delay to allow *OMV* some time to set up before other services that depend on it start. You can do this by setting UP to, for example, 60, which means all VMs that come after it will start 60 seconds after *OpenMediaVault*.

{{< rawhtml >}}
<figure height="543px">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/arr_stack_boot.jpg">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/nas_boot.jpg">
</figure>
{{< /rawhtml >}}

Now, you're ready to create a **Docker Compose** file for the arr-stack. Make sure to adjust the VPN settings in the **Gluetun** service to match your specific VPN provider.

{{< details "Arr Stack Docker Compose" "false" >}}
```yaml
services:
  gluetun:
    image: qmcgaw/gluetun
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    ports:
      - 8888:8888/tcp # HTTP proxy
      - 8388:8388/tcp # Shadowsocks
      - 8388:8388/udp # Shadowsocks
      - 8085:8085 # qbittorrent
      - 6885:6881 # qbittorrent
      - 6885:6881/udp # qbittorrent
      - 7878:7878 # radarr
      - 8989:8989 # sonarr
      - 6767:6767 # bazarr
      - 8686:8686 # lidarr
    volumes:
      - ./gluetun:/gluetun
    environment:
      # See https://github.com/qdm12/gluetun-wiki/tree/main/setup#setup
      - VPN_SERVICE_PROVIDER=
      - VPN_TYPE=openvpn
      - OPENVPN_USER=
      - OPENVPN_PASSWORD=
      - SERVER_COUNTRIES=Netherlands
      # Timezone for accurate log times
      - TZ=Europe/Berlin
      # Server list updater
      # See https://github.com/qdm12/gluetun-wiki/blob/main/setup/servers.md#update-the-vpn-servers-list
      - UPDATER_PERIOD=24h
  
    qbittorrent:
        image: lscr.io/linuxserver/qbittorrent:latest
        container_name: qbittorrent
        env_file: arr-stack.env
        network_mode: "service:gluetun"
        environment:
          - WEBUI_PORT=8085
        volumes:
          - ./qbittorrent/config:/config
          - /mnt/media_root/torrents/:/data/torrents/
        restart: unless-stopped

    radarr:
        image: lscr.io/linuxserver/radarr:latest
        container_name: radarr
        env_file: arr-stack.env
        network_mode: "service:gluetun"
        volumes:
          - ./radarr/config:/config
          - /mnt/media_root:/media_root/
        restart: unless-stopped

    sonarr:
        image: lscr.io/linuxserver/sonarr:latest
        container_name: sonarr
        env_file: arr-stack.env
        network_mode: "service:gluetun"
        volumes:
          - ./sonarr/config:/config
          - /mnt/media_root:/media_root/
        restart: unless-stopped

    lidarr:
        image: lscr.io/linuxserver/lidarr:latest
        container_name: lidarr
        env_file: arr-stack.env
        network_mode: "service:gluetun"
        volumes:
          - ./lidarr/config:/config
          - /mnt/media_root:/media_root/
        restart: unless-stopped

    bazarr:
        image: lscr.io/linuxserver/bazarr:latest
        container_name: bazarr
        env_file: arr-stack.env
        volumes:
          - ./bazarr/config:/config
          - /mnt/media_root:/media_root/
        restart: unless-stopped

    
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    env_file: arr-stack.env 
    ports:
      - 9696:9696 # prowlarr
    volumes:
      - ./prowlarr/config:/config
      - /mnt/media_root/torrents/:/data/torrents/
    restart: unless-stopped


flaresolverr:
    image: ghcr.io/flaresolverr/flaresolverr:latest
    container_name: flaresolverr
    ports:
      - 8191:8191 # flaresolverr
    environment:
      - LOG_LEVEL=info
    restart: unless-stopped
```
{{< /details >}}

In addition to the `docker-compose.yaml` file, you will also need a `.env` file, which defines some environment-specific settings. Make sure to create this `.env` file in the same directory as your `docker-compose.yaml` file.
```env
# this file is used to set environment variables for all the linuxserver images
TZ=Europe/Berlin

# set to your own user id and group
# this is required for filesytem management
# use: `$ id $(whoami)` in terminal to find out
PUID=1000
PGID=1000
```

{{< warning "Warning" >}}
It's important to note that using the user with ID `1000` for the arr-stack setup, which corresponds to the `root` user (with administrative privileges), carries certain security implications.
{{< /warning >}}

You can now create the Docker container for the `arr-stack` by running:

```bash
docker compose up -f arr-stack-compose.yaml up -d
```

### 13.2 Common Issues

1. **Docker Daemon Socket Permission Error**:
   If you encounter the error `permission denied while trying to connect to the docker daemon socket`, you can check the permissions of the Docker socket with the command:

   ```bash
   ls -l /var/run/docker.sock
   ```

   If the permissions appear broken, you can fix them with:

   ```bash
   sudo chmod 666 /var/run/docker.sock
   ```

   This command gives all users read and write permissions to the Docker socket, allowing non-root users to access Docker commands.

2. **File Permissions in `media_root`**:
   You need to ensure that your user has access to all directories inside the `media_root` shared folder. This can be done with the following commands:

   ```bash
   sudo chown -R $USER:$USER /data
   sudo chmod -R a=,a+rX,u+w,g+w /data
   ```

   - `chown` sets the ownership of `/data` to your current user.
   - `chmod` sets appropriate permissions, allowing you to read, write, and execute as necessary.

3. **qBittorrent WebUI Authorization Error**:
   When trying to connect to qBittorrent, you might get an error like `app is unauthorized`. If you encounter this issue, refer to this [forum article](https://discourse.linuxserver.io/t/opening-qbittorrent-webui-via-dashboard-app-is-unauthorized-mismatched-ips/7363/3) for guidance. Following its steps should resolve the authorization problem.


{{< img src="/attachments/500days.jpg" width="50%" figcaption="<i>Completly unrelated, another cool movie poster.</i>" >}}


## 13.3 Quality Control 

Maybe you have already requested some movies using *Radarr* and have noticed that the files you are downloading are rather large—exceeding your requirements, especially if your storage is limited, like mine.

The first thing you can do when requesting media is to change the quality profile. This will determine the quality of the media you download.

{{< img src="/attachments/request_movie.jpg" width="70%" >}}

But maybe even after you've done this, the file is still too large. For this purpose, you can change what the quality profile means. To do this, navigate to `Settings -> Quality -> Quality Definition`.
Here you will find quality labels that a media file can have. You can use the slider to set the minimum and maximum size for each file. For example, if the media size is too big, you can decrease the slider.

{{< img src="/attachments/quality_prfofile_radarr.jpg" width="70%" >}}

For a more extensive elaboration on this topic, refer to the [Trash Guide](https://trash-guides.info/).


## 14. Netflix like Media-Managment with Jellyfin

[Jellyfin](https://jellyfin.org/) is a free, open-source media server that allows you to manage and stream your media collection, much like Netflix. It organizes and displays all your downloaded media in a user-friendly interface, keeping track of what you've watched, your progress, and additional information like cast details, IMDb scores, and more.

Jellyfin integrates smoothly with the *arr-stack*, which is responsible for the acquisition of media, whereas Jellyfin's role is to manage and play back the already downloaded content. This way, your entire media management workflow is streamlined: from downloading media through the *arr-stack* to consuming it through Jellyfin.

{{< rawhtml >}}
<figure height="653px">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/jellyfin_movies.jpg">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/jellyfin_details.jpg">
</figure>
{{< /rawhtml >}}

### 14.1 Jellyfin: Installation

Just like with previously installed software like *Tandoor* or *Homarr*, we can use a [Tteck script](https://tteck.github.io/Proxmox/#jellyfin-media-server-lxc) to easily install Jellyfin. However, setting up Jellyfin is a bit more complicated than in these two previous cases.

The first thing to note is that an unprivileged container **should** work, but you may encounter issues with hardware encoding. Personally, I opted for a privileged container because it simplifies the setup process for hardware acceleration and allows for direct mounting of Samba devices. 

If you prefer to use an unprivileged container, it is still possible to mount the Samba drive on the host machine (`pve`) and utilize [LXC bind mounts](https://pve.proxmox.com/wiki/Linux_Container#_bind_mount_points) to make it available in Jellyfin. I will demonstrate this technique for other software later in this article. Alternatively, you can check out [this forum post](https://forum.proxmox.com/threads/tutorial-unprivileged-lxcs-mount-cifs-shares.101795/) for more information.

To set up hardware encoding in Jellyfin, you can follow the [official guide](https://jellyfin.org/docs/general/administration/hardware-acceleration/intel/#lxc-on-proxmox). Remember, for this to work, IOMMU must be supported by your CPU and motherboard, and it needs to be enabled.

#### 14.1.1 Enabling IOMMU

To enable IOMMU, we need to edit our boot configuration file:

```bash
nano /etc/default/grub
```

Change the following line. This only works for Intel graphics cards; if your graphics card is from another manufacturer, you will need to research how to enable IOMMU for that specific card:

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on"
```

After this, we can update our GRUB configuration by running:

```bash
update-grub
```

Next, edit the modules file:

```bash
nano /etc/modules
```

Add the following modules:

```bash
vfio 
vfio_iommu_type1 
vfio_pci 
vfio_virqfd
```

After making these changes, reboot the server and run the following command to verify if IOMMU is successfully enabled:

```bash
dmesg | grep -d DMAR -e IOMMU
```

#### 14.1.2 GPU Configuration

Type the following command into your shell to find your GPU's address:

```bash
lspci -nnv | grep VGA
```

Here is an example output:

```bash
0:02.0 VGA compatible controller [0300]: Intel Corporation CoffeeLake-S GT2 [UHD Graphics 630] [8086:3e92] (prog-if 00 [VGA controller])
```

Next, in Proxmox, navigate to `Datacenter -> Resource Mapping -> Add` and add your GPU. It should look similar to this:

{{< img src="/attachments/ressource_mapping_ihpu.jpg" width="80%" >}}

#### 14.1.3 Setting Permissions

{{< info "Info" >}}
If you're using an **unprivileged** Jellyfin container, you'll need to edit the LXC configuration file to give the container access to your graphics card for hardware-accelerated video playback. This can be done by adding the following lines to the LXC configuration file:

```bash
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry: /dev/dri/renderD128 dev/dri/renderD128 none bind,optional,create=file
```
{{< /info>}}

We need to ensure that our user has permission to access the graphics card. Enter the following commands in the host shell:

```bash
chmod -R 777 /dev/dri
```

Then, in the LXC container shell, run:

```bash
sudo usermod -aG render jellyfin
sudo usermod -aG video jellyfin
```

These permissions will reset upon a reboot, so we need to make them persistent. To do this, edit the crontab file with:

```bash
crontab -e
```

Then, add the following entry:

```bash
@reboot sleep 20 && chmod -R 777 /dev/dri
```
We add a delay because the graphics drivers may not be initialized yet.

For more information, check out this [forum post](https://forum.proxmox.com/threads/guide-jellyfin-remote-network-shares-hw-transcoding-with-intels-qsv-unprivileged-lxc.142639/) on the Proxmox forum.

#### 14.1.4 Testing Hardware Encoding

To ensure hardware encoding is working, run a movie that requires [transcoding](https://corp.kaltura.com/blog/what-is-transcoding/#) and execute the following command in the shell:

```bash
intel_gpu_top
```

(Note: You need to install `intel-gpu-tools` first and need to have a movie on your Jellyfin instance.) You should see some utilization of your graphics card.

Another test to confirm hardware encoding is to run:

```bash
sudo -u jellyfin /usr/lib/jellyfin-ffmpeg/ffmpeg -v verbose -init_hw_device vaapi=va:/dev/dri/renderD128 -init_hw_device opencl@va
```

After running the previous command, you should receive an output that looks similar to this:

{{< img src="/attachments/jellyfin_hw_test.jpg" width="100%" >}}

#### 14.1.5 Giving Jellyfin Access to the NAS

Since our data is on the **data** ZFS dataset, we need to connect this ZFS dataset with our newly created Jellyfin LXC container.

1. Just like with the ARR-stack, Jellyfin should start after the NAS-VM.
2. First, install `cifs-utils`:

   ```bash
   apt install cifs-utils
   ```

3. Normally, you should be able to define the mount point of your SMB share in the host shell under `/etc/pve/lxc/your_lxc_container_id.conf`. However, if this doesn't work, you can use `crontab`. Open it with:

   ```bash
   crontab -e
   ```

   Then add the following line:

   ```bash
   @reboot sleep 5 && mount -t cifs //<your_nas_ip>/media_root /mnt/media_root -o ro,_netdev,x-systemd.automount,noatime,dir_mode=0770,file_mode=0770,credentials=/etc/smbcredentials
   ```

   *(The `ro` option means read-only; Jellyfin shouldn't need write access to our media.)*

4. The mounted directory will be owned by root, so we need to give Jellyfin permission to access it:

   ```bash
   usermod -aG root jellyfin
   ```

   *(Be careful; this has security implications, as you are essentially giving Jellyfin root access.)*

5. You can test if Jellyfin has access by running the following command:

   ```bash
   sudo -u jellyfin ls /mnt/media_root
   ```

### 14.2 Jellyfin: Final Note

When creating your media library, you should enable the `NFO` option, which will save metadata locally. This is necessary because we didn't grant Jellyfin write access to the `media_root` directory.

{{< img src="/attachments/cat7.jpg" width="80%" figcaption="<i>A picture of a cat inside a server, has nothing to do Jellyfin.</i>" >}}


## 15. Synchronize Files Across Multiple Devices with Syncthing

I already talked about [Syncthing](/articles/my_homelab_part_6_syncthing/) in a prior post, which I recommend checking out for more information. 

To recap, Syncthing is a synchronization service that allows you to sync files across multiple devices. I personally use it to synchronize my written notes across all my devices.

{{< img src="/attachments/synthing.jpg" width="80%" >}}

### 15.1 Syncthing: Installation

As luck would have it, there is a [TTeck script](https://tteck.github.io/Proxmox/#syncthing-lxc) that we can use for the installation process.

After this, we need to change one last thing. We created the *local* SSD ZFS dataset and the *data* HDD ZFS dataset to separate where we save our software and their associated configuration files (on the *local* dataset) from where we save the actual data (on the *data* dataset), e.g., movies in the case of the Arr-Stack. 

We want to do the same with Syncthing, where we save our data on an SMB share of OMV, while the software itself is stored on the *local* dataset. To achieve this, during the installation process, choose to use the *local* dataset for installation.

Once the installation is complete, we can add our SMB share to the LXC container. To do that, we will use [LXC bind mounts](https://pve.proxmox.com/wiki/Linux_Container#_bind_mount_points).

1. Open the OpenMediaVault web interface and create a new shared folder, which I’ll call `syncthing`. Navigate to `Storage -> Shared Folder -> Create`. After creating it, you’ll need to share the folder: go to `Services -> SMB -> Shares -> Create`.

2. Next, create a new user with read-write permission to access this shared folder: `Users -> Users -> Create`. To grant the user access to the new share, go to `Storage -> Shared Folders -> Select the correct folder -> Permissions`.

3. With OMV configured, create a `syncthing` folder (or whatever you named your shared folder) in both the host system and the LXC container, under the `/mnt` directory.

4. Now, we need to mount the folder to our local machine (`PVE`). To do this, edit the `fstab` file using `nano /etc/fstab` on the host machine and add the following entry:
    ```bash
    //<your_nas_ip>/syncthing /mnt/lxc_shares/syncthing cifs _netdev,x-systemd.automount,noatime,nobrl,uid=100000,gid=110000,dir_mode=0770,file_mode=0770,credentials=/etc/smbcredentials_syncthing 0 0
    ```
    In this example, I mounted the folder inside the `lxc_share` directory. If you chose a different directory, adjust the path accordingly.

5. Inside the `/etc` directory on your host machine, create an `smbcredentials` file and add the username and password, just like we did with the Arr-Stack setup.

6. Find the ID of your LXC container. You can check this in the Proxmox sidebar where it will be displayed next to the container's name.

    {{< img src="/attachments/proxmox_id.jpg" width="30%" >}}

7. Now, edit the LXC configuration file by running:
    ```bash
    nano /etc/pve/lxc/<your_syncthing_id>.conf
    ```
    Add the following entry:
    ```bash
    mp0: /mnt/lxc_shares/syncthing,mp=/mnt/syncthing
    ```
    This will allow the SMB drive from the host machine to be accessed inside the Syncthing LXC container.

8. Reboot the LXC container, and you should now be able to access the mounted `syncthing` folder inside the LXC container.

9. Lastly, since this LXC container depends on OMV, don’t forget to change the boot priority of this container to 2.

You should now be able to add your sync folder and syncrhonize them across devices.

## 16. Document Management with Paperless-NGX

> Are your shelves overflowing with paper documents like car insurance, health insurance forms, or bank statements? Do you find yourself spending too much time rummaging through stacks of folders, hopelessly searching for that one important document? Worse yet, are you tired of manually copying details from physical papers to your digital files?  
>
> Introducing [Paperless-Ngx](https://docs.paperless-ngx.com/), the open-source solution designed to simplify your document management. Say goodbye to the clutter of physical paperwork and the headache of searching through piles of folders.  
>
> With Paperless-Ngx, you can automatically import documents from various sources, converting them into neatly organized, searchable PDFs that are stored securely on your own server—completely free from third-party access. No more data being transmitted elsewhere!  
>
> Our powerful OCR (Optical Character Recognition) feature ensures that even scanned images are transformed into fully searchable text, allowing you to find exactly what you need, when you need it. Supporting over 100 languages, Paperless-Ngx ensures global functionality, so you’ll never be left searching aimlessly again.  
>
> Ready to regain control over **your** documents? Download Paperless-Ngx today.Completely free and see how easy it is to take back your space and sanity.  

{{< img src="/attachments/documents-smallcards-dark.png" width="100%" >}}

### 16.1 Paperless-Ngx: Installation

Installation is very easy thanks to the [TTeck script](https://tteck.github.io/Proxmox/#paperless-ngx-lxc). 

If, after installation, you encounter the error: "`CSRF verification failed`", it could be due to your reverse proxy. To fix this, go to `/opt/paperless/paperless.conf` and set `PAPERLESS_URL` to your reverse proxy URL.

As with previous software, we want to save our files on the *data* ZFS dataset. To do this, create a new shared folder in OMV, add a new user with permission to access it, and then add the SMB share to the `fstab` of the host machine. Afterward, edit the LXC config file to bind the SMB share from the host machine to the LXC container.
And as always, don't forget to change the boot order of Paperless-NGX to 2.
If you need additional information about any of these tips, check out the prior section on Syncthing.

As an additional tip, there is a [Paperless app](https://github.com/astubenbord/paperless-mobile) available on Android for browsing your documents.

## 17. Accessing Our Services from Outside Our Local Network with WG-Easy

We have installed many services, such as Tandoor, Syncthing, and Paperless-NGX, but so far, we can only access them within our local network. However, there may be times when we want to access these services from outside our local network without exposing them directly to the internet, which could leave us vulnerable to cyber attacks.

To address this, we can host our own VPN with [WG-Easy](https://github.com/wg-easy/wg-easy), which tunnels all our network activity when we're outside our local network. I also considered using [Tailscale](https://tailscale.com/), which has a nicer and easier interface. However, their free plan only allows a limited number of users. If you’re okay with this limitation, I highly recommend Tailscale.

{{< img src="/attachments/wg-easy.png" width="60%" figcaption="<i>Wg-easy dashboard.</i>" >}}

### 17.1 Wg-easy: Installation

There is no direct TTeck script for WG-Easy, but like we did with *FreshRSS*, we can use the [TTeck Docker script](https://tteck.github.io/Proxmox/#docker-lxc). You only need to install Docker Compose when prompted by the script; the other software is not required.

After the installation is complete, we can rename the hostname of the container to clarify what service this container is for. To do this, go to `New LXC Container -> DNS -> Hostname`. We also do not need two processors, which is the default setting of the script; you can change that by going to `New LXC Container -> Resources -> Cores`.

The first thing we need to do is create a new domain. This time, unlike before, this domain needs to point to our **external** IP address. This is necessary so that we can always use the same domain to connect to our VPN instead of using the IP address.

Just like last time, I used DuckDNS again, but this time I left the default IP address that was already written in it. Sometimes your IP can change; for example, this can happen if you have a dynamic IP. Because of this, we need to regularly update the IP address that the DuckDNS domain points to. For this, we can use a [Linux cron](https://www.duckdns.org/install.jsp) script from their website. Just follow the instructions on their page and install it on the host machine (`PVE`).

Now, we can use the following Docker Compose script:
```yaml
volumes:
  etc_wireguard:

services:
  wg-easy:
    environment:
      # Change Language:
      # (Supports: en, ua, ru, tr, no, pl, fr, de, ca, es, ko, vi, nl, is, pt, chs, cht, it, th, hi)
      - LANG=en
      # ⚠️ Required:
      # Change this to your host's public address
      - WG_HOST=
      - PASSWORD_HASH=

    image: ghcr.io/wg-easy/wg-easy
    container_name: wg-easy
    volumes:
      - etc_wireguard:/etc/wireguard
    ports:
      - "51820:51820/udp"
      - "51821:51821/tcp"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
      # - NET_RAW # ⚠️ Uncomment if using Podman
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv4.conf.all.src_valid_mark=1
```

There are two important parameters you need to change: `WG_HOST`, which should equal the new domain you created, and `PASSWORD_HASH`. For this, use the following [guide](https://github.com/wg-easy/wg-easy/blob/master/How_to_generate_an_bcrypt_hash.md) to generate the password hash.

After that, you can start the software with `docker compose up -f <name> -d`. It is important when using Nginx Proxy Manager to still use the standard domain, not the new domain, because the standard domain is for internal use.

The last thing you need to do is forward port `51820` of your `docker-wgeasy` container, not of the host machine.

For more information refer to my [prior article](/articles/my_homelab_part_4_wireguard_vpn/) on this subject.

## 18. Book Managment with Calibre-Web Automated and Audiobookshelvf

[Calibre-Web Automated](https://github.com/crocodilestick/Calibre-Web-Automated), which is based on [Calibre](https://calibre-ebook.com/) and [Calibre-Web](https://github.com/janeczku/calibre-web), is a book management software that allows you to read books, rate them, view their metadata, create book lists, send books to an e-reader, and enjoy many other features.

{{< img src="/attachments/calibre_automated.jpg" width="80%" >}}

[Audiobookshelf](https://www.audiobookshelf.org/), similar to Calibre, is an audiobook management software that offers a range of features. It allows you to organize your audiobook collection, stream audiobooks to different devices, track your listening progress, and customize metadata. Additionally, it supports multiple users, making it perfect for shared libraries.

{{< img src="/attachments/audiobookshelf.png" width="80%" figcaption="<i>Image is from geek-cookbook.</i>" >}}


In addition to both of these software, I will use [Readarr](https://github.com/Readarr/Readarr), *Prowlarr*, *gluetune*, and *qBittorrent* to create a setup similar to my *Arr-Stack. This will allow me to automatically torrent e-books and audiobooks, streamlining the process just like I do with other media.

### 18.1 Calibre-Web Automated and Audiobookshelf: Installation 

Just like with *WG-Easy*, there isn't a direct TTeck script available for this. Instead, we’ll use the [TTeck Docker script](https://tteck.github.io/Proxmox/#docker-lxc) and install the software via Docker.

If you want to store your books on the *data* ZFS dataset, you can follow the same process we used for Syncthing. If you go this route, as always, remember to change the boot order to 2. Personally, I created two shared folders—one for books and another for audiobooks.

When initializing Calibre, the software requires an empty library that it can populate in order to function properly, so make sure you have that ready. You can read more about this in my [old blog post](/articles/my_homelab_part_3_calibre/).

You can use the following Docker Compose setup:
{{< details "Book *Arr-Stack" "false" >}}
```yaml
services:
   gluetun:
    image: qmcgaw/gluetun
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    ports:
      - 8888:8888/tcp # HTTP proxy
      - 8388:8388/tcp # Shadowsocks
      - 8388:8388/udp # Shadowsocks
      - 8080:8080 # qbittorrent
      - 41957:41957 # qbittorrent
      - 41957:41957/udp # qbittorrent
    volumes:
      - ./gluetun:/gluetun
    environment:
      # See https://github.com/qdm12/gluetun-wiki/tree/main/setup#setup
      - VPN_SERVICE_PROVIDER=
      - VPN_TYPE=
      - SERVER_NAMES=
      # Timezone for accurate log times
      - TZ=Europe/Berlin
      # Server list updater
      # See https://github.com/qdm12/gluetun-wiki/blob/main/setup/servers.md#update-the-vpn-servers-list
      - UPDATER_PERIOD=24h

  calibre-web-automated:
    image: crocodilestick/calibre-web-automated:latest
    container_name: calibre-web-automated
    environment:
      - PUID=0
      - PGID=0
      - TZ=UTC
      - DOCKER_MODS=linuxserver/mods:universal-calibre
    volumes:
      - ./calibre/config:/config
      - ./calibre/book-ingest:/cwa-book-ingest
      - /mnt/calibre/libary:/calibre-library
    ports:
      - 8084:8083 # Change the first number to change the port you want to access the Web UI, not the second
    restart: unless-stopped

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:4.6.6
    network_mode: "service:gluetun"
    container_name: qbittorrent
    environment:
      - PUID=0
      - PGID=0
      - TZ=Etc/UTC
      - WEBUI_PORT=8080
      - TORRENTING_PORT=41957
    volumes:
      - /mnt/audiobookshelf/audiobooks:/audiobooks
      - ./calibre/book-ingest:/cwa-book-ingest
      - ./qbittorrent/scripts:/scripts
      - ./qbittorrent/appdata:/config
      - ./qbittorrent/downloads:/downloads #optional
    restart: unless-stopped
  
  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    # ABS runs on port 13378 by default. If you want to change
    # the port, only change the external port, not the internal port
    ports:
      - 13378:80
    volumes:
      # These volumes are needed to keep your library persistent
      # and allow media to be accessed by the ABS server.
      # The path to the left of the colon is the path on your computer,
      # and the path to the right of the colon is where the data is
      # available to ABS in Docker.
      # You can change these media directories or add as many as you want
      - /mnt/audiobookshelf/audiobooks:/audiobooks
      - /mnt/audiobookshelf/podcasts:/podcasts
      # The metadata directory can be stored anywhere on your computer
      - ./audiobookshelf/metadata:/metadata
      # The config directory needs to be on the same physical machine
      # you are running ABS on
      - ./audiobookshelf/config:/config
    restart: unless-stopped
    # You can use the following environment variable to run the ABS
    # docker container as a specific user. You will need to change
    # the UID and GID to the correct values for your user.
    environment:
      - user=0:0

  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=0
      - PGID=0
      - TZ=Etc/UTC
    volumes:
      - ./prowlarr/data:/config
    ports:
      - 9696:9696
    restart: unless-stopped
```
{{< /details >}}

Make sure to configure the VPN settings for Gluetun or remove Gluetun from the Docker Compose file. Additionally, double-check the volumes to ensure they match your setup if you're not using the same configuration as mine. 
I set the version of qBittorrent to 4.6.6 because I was using [MyAnonamouse](https://www.myanonamouse.net/), a [private tracker](https://www.reddit.com/r/torrents/comments/174b1d/what_are_private_trackers_and_how_do_they_work/) that, at the time, didn't allow higher qBittorrent versions. I highly recommend myanommouse, it's not very hard to get into and offers a wide range of books. If you don’t plan on joining MyAnonamouse, you can replace `image: lscr.io/linuxserver/qbittorrent:4.6.6` with `image: lscr.io/linuxserver/qbittorrent:latest` in the Docker Compose file.

{{< warning "Warning">}}
I set `PUID` and `GID` to `0`, which essentially gives the container root-level access. While this simplifies permissions management, it also has significant security implications, as it could potentially expose your system to vulnerabilities or unauthorized access. If security is a priority, consider using a non-root user by setting the appropriate `PUID` and `GID` values for better isolation and protection.
{{< /warning >}}

For post-installation steps, follow the [official Calibre-Web Automated guide](https://github.com/crocodilestick/Calibre-Web-Automated). You should change the default username and set the location of your database to ensure proper functionality.

For qBittorrent, the default username is *admin*, and you’ll find the password inside the Docker logs. After logging in, make sure to change the default credentials. I also recommend setting a speed limit to prevent bandwidth issues.

In Prowlarr, you need to add Readarr as a connection. You can do this by navigating to `Settings -> Apps -> Readarr`. Additionally, add qBittorrent as your download client. After this, you'll want to add some book trackers in Proxmox, which will automatically sync to Readarr.

{{< img src="/attachments/prowlarr.jpg" width="80%" >}}

When setting up a reverse proxy for these services, ensure you enable WebSocket support for Audiobookshelf.

The last step is to ensure that books and audiobooks are downloaded to the correct folders. To do this, go to Prowlarr and add two categories: `audiobookshelf` and `books`. Navigate to `Settings -> Download Clients -> qBittorrent -> Mapped Categories` and configure them accordingly.

{{< rawhtml >}}
<figure height="1010px">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/prowlarr_category.jpg">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/prowlarr_books.jpg">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/prowlarr_audiobooks.jpg">
</figure>
{{< /rawhtml >}}

Once completed, you should see these categories on the sidebar in qBittorrent. For the audiobook category, set the download folder to `/audiobooks`, and for books, choose `/downloads`. Books saved in the `cwa-ingest` folder will be imported and deleted automatically, which means they can't be seeded. 

To ensure books are moved to the correct folder after downloading, go to qBittorrent's settings and add an external program to run when downloads are finished: `cp -r "%F" "/cwa-book-ingest"`. This will automatically copy the book to Calibre while still allowing you to seed it in qBittorrent.

{{< img src="/attachments/qbittorent_external_programm.jpg" width="80%" >}}

Now, whenever you search for a book on Prowlarr, it should automatically download to the correct folder and show up in both Audiobookshelf and Calibre-Web.


## 19. Immich

[Immich](https://immich.app/) is an open-source image management software designed for self-hosting on local servers. It provides a user experience similar to Google Photos, offering features such as automatic photo backup, organization, sharing, and search capabilities. Immich supports a range of functionalities like facial recognition, location tagging, and album creation, a versatile tool for managing personal photos without relying on cloud-based services.

{{< img src="/attachments/immich.webp" width="80%" figcaption=" <i>Image is from elest.io</i>" >}}

### 19.1 Immich: Installation

Similar to *Calibre*, there isn't a dedicated TTeck script available for Immich. Instead, we’ll use the [TTeck Docker script](https://tteck.github.io/Proxmox/#docker-lxc) and install the software via Docker.

If you have any questions during the process, you can refer to the [official Immich Docker Compose guide](https://immich.app/docs/install/docker-compose), which also provides the necessary Docker Compose file.

#### 19.1.1 Data Storage Configuration

When running Immich, it generates additional data, such as thumbnails or facial recognition data. If you'd like, you can separate the storage location for this data from your actual photos. For more details on how to do this, refer to [this discussion](https://github.com/immich-app/immich/discussions/2328). Personally, I store the generated data on my *local* SSD ZFS dataset and my photos on the *data* ZFS dataset.

If you plan to go this route, you'll need to create a new shared folder in OMV for your Immich photos, mount it on your host machine, and use LXC binds to make it available in your container.

#### 19.1.2 Hardware Acceleration

If you want to use features like facial recognition, I highly recommend enabling hardware acceleration, similar to how we did it for Jellyfin.

{{< info "Info" >}}
If you're using an **unprivileged** Immich container, the first step is to edit the LXC configuration file to grant the container access to your graphics card for hardware acceleration. Add the following lines to the LXC configuration file:

```bash
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry: /dev/dri/renderD128 dev/dri/renderD128 none bind,optional,create=file
```
{{< /info >}}

Next, you'll need to give the user permission to access the graphics card by setting permissions in crontab with `@reboot sleep 20 && chmod -R 777 /dev/dri`. This step is necessary because the permissions reset after a container reboot.

Additionally, you will need to execute the following command in the LXC container shell:

```bash
sudo usermod -aG render immich
sudo usermod -aG video immich
```
This will give the immich user the necessary permissions to access the graphics card.

#### 19.1.3 External Library Configuration

If you want to include an external library (e.g., old family photos that aren’t on your smartphone), you can follow [this guide](https://immich.app/docs/guides/external-library/). I personally use the following folder structure:

```
photos/
├── ExternalLibraries/
│   ├── holidays_2020
│   ├── holidays_2021
│   └── holidays_2019
└── Immich/
```

### 19.1.4 Configuring the `.env` and Docker Compose Files

In addition to the Docker Compose file from the official Immich guide I linked earlier, you’ll also need a `.env` file to set certain parameters, such as storage locations. If you plan to separate your photos from immich's generated data, you can use the following `.env` file:

```
LIBRARY_LOCATION=/mnt/photos/Immich/
THUMBS_LOCATION=./thumbs/
UPLOAD_LOCATION=./upload/
PROFILE_LOCATION=./profile/
VIDEO_LOCATION=~./encoded-video/
```

You'll also need to modify the volumes section of the Docker Compose file as follows:

```
${LIBRARY_LOCATION}:/usr/src/app/upload/library
${UPLOAD_LOCATION}:/usr/src/app/upload/upload
${THUMBS_LOCATION}:/usr/src/app/upload/thumbs
${PROFILE_LOCATION}:/usr/src/app/upload/profile
${VIDEO_LOCATION}:/usr/src/app/upload/encoded-video
/mnt/photos/ExternalLibraries:/mnt/ExternalLibraries:ro
/etc/localtime:/etc/localtime:ro
```

#### 19.1.5 Migrating from Google Photos

To migrate from Google Photos, you can either use the [Immich mobile app](https://immich.app/docs/features/mobile-app/) or follow [this guide](https://www.chuck-builds.com/immich-and-google-photos/).

## 20. Backups

We’ve hosted various software applications, and this took considerable time and effort. The last thing we want is to lose all of this progress due to disk failures, so it’s essential to set up a proper backup system.

You might think that using a RAID system, which mirrors every disk, provides backup protection. However, RAID is not a backup.

{{< img src="/attachments/raid_backup.png" width="70%" >}}

Here’s a comment that explains this well:
> If your home server were stolen, a backup would be used to restore your data elsewhere.
>
> If your home server were in a house fire, a backup would be used to restore your data.
>
> If both hard drives failed before the rebuild finished, a backup would restore your data.
> 
> If you accidentally opened a file that encrypted your data, a backup would restore your data.
> 
> If your home server was dropped during a move, a backup would restore your data.
> 
> If you were editing a video and overwrote the original, a backup would recover the original file.
> 
> If a hacker got in and destroyed your data, you’d need the backup.
>
> If a family member messed things up, you’d need the backup.

### 20.1 What Data Should You Backup?

Not all data needs to be backed up, only the original data that is important to you. This is crucial because backing up everything can require a lot of storage space—and that can be expensive.

The best practice for backups is the **3-2-1 rule**, which suggests you should have:
- **3 copies** of your data,
- **2 different types** of storage media, and
- **1 offsite copy**.

This is the ideal goal, but in practice, it may not always be feasible due to costs.

### 20.2 Important Data and My Previous Backup Strategy

The first step is to identify which data is important for you to back up. For me, this includes:
- My Proxmox configuration files.
- My personal notes (including this website).
- My personal images and family photos.
- My Linux configuration files.

Once you’ve identified the critical data, think about your backup strategy.

- My **Linux configuration files** are already stored on two different devices, with one being offsite (on my computer and in a GitHub repository).
- My **personal notes** are relatively secure as I sync them between my laptop, desktop, and server, resulting in 3 copies on different devices.
- My **personal image collection** is less secure. My personal images are on my phone and server, while my family photos have two copies: one on my server and one with my dad.

That leaves my **Proxmox configuration**, which currently has no backup. Since I tinker with my homelab often, things can go wrong, and having a backup would allow me to roll back to prior versions.

### 20.3 My Backup Plan

Initially, I planned to use [Proxmox Backup Server](https://www.proxmox.com/en/proxmox-backup-server/overview) on my Raspberry Pi 3B, as its server role was defunct after a homelab upgrade. Unfortunately, Proxmox Backup Server isn't built for the ARM processor in the Raspberry Pi, but there’s an alternative version called [PiBS](https://github.com/Proxmox-Backup-Server-for-ARM) available on GitHub, which works with ARM. Proxmox Backup Server is great because it integrates directly with Proxmox. I even found a nice [guide](https://liersch.it/2023/09/proxmox-backup-server-auf-raspberry-pi-installieren/) for setting it up (it’s in German, though).

Sadly, while flashing the SD card for the Raspberry Pi 3B, it broke (which is why you should use an SSD), and I didn’t have the funds to fix it.

### 20.4 The Alternative Plan

Instead, I decided to use two external 1TB hard drives I already had for backup storage. Since data loss from a single drive failure would be catastrophic, I set them up in a **ZFS mirror**, which minimizes the risk of data loss.

The plan was to connect these drives to my server and have it automatically back up the Proxmox configuration at a set time each day. While this setup isn’t ideal (as the backup drives aren’t offsite), it’s better than nothing.

### 20.5 Backup Retention Strategy

Given the limited storage (only 1TB), I couldn’t back up everything daily, as it would quickly exceed the available space. This is where **backup retention** comes in. Backup retention allows you to define how long backups are kept on a daily, weekly, monthly, and yearly basis. After some experimentation, I settled on the following parameters:
- **keep-daily: 7** (daily backups for the past week),
- **keep-weekly: 3** (weekly backups for the past 3 weeks, resulting in 4 weekly backups with daily backups included),
- **keep-monthly: 6** (monthly backups for half a year),
- **keep-yearly: 5** (1 backup per year for the last 5 years).

You can explore the effects of this strategy using the [backup retention simulator](https://pbs.proxmox.com/docs/prune-simulator/), which I highly recommend.

This setup has worked well so far. After a month of running, my server’s backup storage is about half full.

{{< img src="/attachments/backup_usage.jpg" width="80%" >}}

### 20.6 Implementing My Backup Strategy

To implement my backup strategy, follow these steps:

1. **Prepare Your Disks:**
   If the disks already contain important data, ensure you save it elsewhere before proceeding. Then, connect the disks to your server.

2. **Wipe the Disks:**
   In Proxmox, navigate to `pve -> Disks`, select the two newly connected disks, and press the **Wipe** button. This will erase any existing data on the disks.

3. **Create ZFS Mirror:**
   Go to `pve -> Disks -> ZFS -> Create ZFS`. Select your two newly connected disks and set the RAID level to `mirror`. For compression, I recommend using `zstd`. If you're curious about the trade-offs between different compression algorithms, [this blog post](https://manishrjain.com/compression-algo-moving-data) offers a good overview. In summary, `lz4` is faster but compresses less, while `zstd` compresses more effectively but is slower and uses more CPU resources.

4. **Add Backup Directory:**
   Next, navigate to `Datacenter -> Storage -> Add -> Directory`. For the content type, choose `VZdump`. Select a name for the directory and add it.

5. **Set Up Backup Schedule:**
   Go to `Datacenter -> Backup -> Add`, and add the newly created directory. Set the node to your host machine, and choose the schedule for when you want to back up your devices. I have mine set to back up every day at `00:00`. For the backup mode, I use `Snapshot`. You can read more about the different backup modes [here](https://pve.proxmox.com/wiki/Backup_and_Restore#_backup_modes). I also recommend enabling email notifications, so you’ll get alerts when a backup completes, helping you spot any errors early. For retention, choose the settings that suit your needs.

6. **Exclude NAS Storage from Backup:**
   To exclude your NAS storage from backups, navigate to your OpenMediaVault virtual machine, go to the **Hardware** section, select the disks, and click **Remove from Backup**.

7. **Test the Backup:**
   A backup is not a *real* backup if you haven’t tested it. To do so, navigate to `Datacenter -> Backup` and manually create a backup. While the job is running, check the job details to ensure the NAS disks are properly excluded.

8. **Verify the Backup:**
   Once the backup is finished, scroll down the left sidebar in Proxmox to your backup storage. You should now see the newly created backup.

9. **Restore and Test:**
   To verify that everything is working, pick a random container, shut it down, and go to the backup tab to restore it. Afterward, check that the restored container is functioning correctly.

10. **Congratulations!**  
    You now have a working backup strategy!

{{< img src="/attachments/30year_old_saver.png" width="70%" >}}

## 21. Server Power Optimization

If you, like me, live in a European country, power consumption is probably a concern due to the high cost of electricity.

{{< img src="/attachments/electricity_2023_prices.jpg" width="80%" >}}

As such, it’s essential to optimize the power consumption of your server. I used the [Shelly Plug S](https://www.shelly.com/de/products/shop/shelly-plus-plug-s-1) to measure my power usage. This power monitor plugs into your wall socket and measures the consumption of any connected device. It’s quite affordable at around 20 bucks and accurate enough for my use case.

### 21.1 Power-Saving Optimizations

A helpful thread on the [Home Assistant Forum](https://community.home-assistant.io/t/psa-how-to-configure-proxmox-for-lower-power-usage/323731) discusses optimizing server power usage. One of the most impactful changes, aside from removing unused electronics, is using the power-saving scaling governor for the CPU. You can activate this by running the following command:

```bash
echo "powersave" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### 21.2 Measuring Power Consumption

When the server is idle and not performing any tasks, it consumes approximately 20 watts of power (with the powersave scaling governor). With minor workloads like torrenting, the consumption goes up to 30 watts. Under full load, the power usage increases even more.

We can use any of the many [electricity calculators online](https://www.rapidtables.com/calc/electric/energy-cost-calculator.html) to estimate the cost of running the server. For example, using the following parameters: 

- **Power consumption**: 30 watts  
- **Operating time**: 24 hours per day  
- **Electricity price**: €0.40 per kWh (as of April 29th, Germany)

This results in an annual energy cost of approximately **€105**. By reducing the server's operating time from 24 hours to 18 hours a day, the total cost drops to around **€80** per year.

### 21.3 Scheduled Server Shutdowns

Another simple way to save power is by not leaving your server on all the time. I, for example, turn off my server at 01:00 and then turn it on again when needed.

#### 21.4 Automating Server Shutdown

To automatically turn off your server at a specific time, you can schedule a cron job. First, open crontab for editing by running `crontab -e`, and add the following line to schedule a shutdown at 01:00:

```bash
0 1 * * * /usr/sbin/shutdown -h now
```

If you're unfamiliar with cron syntax, you can use [Crontab Guru](https://crontab.guru/) for explanations and testing.

### 21.5 Automatically Turning Your Server Back On

Now that your server can shut down automatically, you’ll want a convenient way to turn it back on without physically pressing the power button. For this, you can use [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN), which sends a special network packet to turn on your server remotely.

#### 21.5.1 Setting Up Wake-on-LAN

To enable Wake-on-LAN, follow these steps:
1. Go to `pve -> Network` and find the name of your network device.
2. Run the command `ethtool <device_name>` (e.g., `ethtool enp6s0`) to check the device’s status. If you see `wake on: d`, it means Wake-on-LAN is disabled.
3. You may need to enable it in your BIOS settings.

#### 21.5.2 Sending the Wake-on-LAN Packet

To send the wake-up packet, I use my smartphone with the [WakeOnLan app](https://github.com/Florianisme/WakeOnLan). 

The configuration of *WakeOnLan* app should look similar to this:
{{< img src="/attachments/wake_on_lan.png" width="30%" >}}

You can get your server's MAC address, by running the following command after installing `net-tools` (with `apt-get install net-tools`):
```bash
ifconfig -a
```

Alternatively, you can use the command `ip link` and look for the device labeled as `ether`. The MAC address will be listed next to it.

{{< img src="/attachments/ifcofig.jpg" width="80%" >}}


## 22. Notification with Gotify

One important consideration for maintaining a secure and well-monitored Proxmox environment is setting up a notification system. This becomes especially crucial in scenarios where immediate attention is required—such as a disk failure or a backup job that didn’t complete successfully. Early alerts can help you act quickly, minimizing downtime and reducing the risk of data loss.

Proxmox supports several notification methods out of the box, including email. However, I opted to use Gotify, an open-source push notification server that enables real-time alerts directly to your smartphone or other devices. It’s lightweight, easy to set up, and perfect for receiving instant updates from your Proxmox server. For example, if a scheduled backup fails in the middle of the night, Gotify can send a push notification straight to your phone, ensuring you’re aware of the issue without delay.


1. **Deploy Gotify in an LXC Container:** Use the community script available at [Proxmox VE Community Scripts](https://community-scripts.github.io/ProxmoxVE/scripts?id=gotify) to install Gotify easily in an LXC container. The default settings usually work well, but you can customize them if needed.


2. **Access the Gotify Web UI:** Once the container is created, the Proxmox console will display its IP address. Open a browser and go to that IP—Gotify runs on port **80** by default. You can log in using the default credentials:

    * **Username:** `admin`
    * **Password:** `admin`

    Make sure to **change your password** immediately after logging in for security reasons.


    {{< img src="/attachments/gotify_login.jpg" width="80%" >}}


3. **Configure NGINX Reverse Proxy (Optional but Recommended):** For better accessibility and security, especially if you plan to access Gotify remotely, it's advisable to set up an NGINX reverse proxy. Be sure to **enable WebSocket support**, as Gotify uses WebSockets to push notifications in real-time.

4. **Enable Autostart for the LXC Container:** In the Proxmox web UI, navigate to the options of the Gotify container and enable **Autostart**, so Gotify launches automatically after a host reboot.

5. **Add Gotify as a Notification Target in Proxmox:**  Go to:

    ```
    Datacenter -> Notifications -> Add -> Gotify
    ```

    Here, you’ll need to enter the Gotify server URL and an access token. To generate a token:


    {{< img src="/attachments/gotify-proxmox.jpg" width="80%" >}}

    1. In the Gotify web UI, create a new **application**.
    2. Copy the **access token**.
    3. Paste it into the corresponding field in Proxmox.

    {{< img src="/attachments/gotify_apps.jpg" width="80%" >}}

With this Proxmox can now send system notifications to Gotify, but we are not finished yet, we now need to tell Gotify that it should send the message that it received to your phone.

6. **Connect Your Mobile Device:** To receive push notifications on your phone:

    1. Download the **Gotify app** from the Google Play Store (or F-Droid).
    2. Open the app and enter your Gotify server URL along with your login credentials.
    3. After logging in, your phone should appear as a connected client in the Gotify web interface.

    {{< img src="/attachments/gotify_clients.jpg" width="80%" >}}

7. **Send a Test Notification:** To verify everything is working:

    1. In Proxmox, go to `Datacenter -> Notifications`.
    2. Select your Gotify endpoint and click the **Test** button.
    3. You should receive the notification both in the Gotify web UI and on your phone.


8. **Set Up Notification Filters (Optional)_** To control what types of messages you receive:

    1. In Proxmox, go to `Datacenter -> Notifications`.
    2. Scroll to the bottom and click **Add** under **Notification Matchers**.
    3. Give your matcher a name.
    4. Under the **Targets to Notify** tab, select your Gotify endpoint.
    5. In the **Match Rules** tab, choose which types of notifications (e.g., backup failures, hardware issues) you want to be alerted about.

{{< img src="/attachments/notfication_matcher_proxmox.jpg" width="80%" >}}

**Bonus Tip:** Disable the "Connected" Notification on Android. The Gotify Android app may display a persistent "Connected" notification. To remove it:

1. Go to your **Android system settings**.
2. Navigate to **Apps -> Gotify -> Notifications**.
3. Disable the **Foreground Service Notification**.


{{< img src="/attachments/gotify_app_notifcation_disable.jpg" width="30%" >}}

**Bonus Bonus Tipp:** There is also a cross platform [tray application](https://github.com/seird/gotify-tray) out there that you can install for your laptop or desktop PC, to receive notification from your gotfiy service.

## 23. The End

That's it, we're done. No more services to install, no more configurations left to configure, no more users and permissions to set, and especially no more documentation to write.

Not really, there's always something that can be done. But for now, I am free!

This was the longest piece of continuous text I've ever written, and it took me way too long to finish it. But I’m happy I did. I think I learned a lot and hopefully, you dear reader, learned something too.

At last, enjoy these last server-themed movie posters.

{{< rawhtml >}}
<figure style="display: flex; justify-content: center; gap: 10px;" height="387px">
    <img loading="lazy" style="width: 33%;" src="/attachments/back_up.jpg">
    <img loading="lazy" style="width: 33%;" src="/attachments/the_ecc_buster.jpg">
    <img loading="lazy" style="width: 33%;" src="/attachments/Alien3.png">
</figure>
{{< /rawhtml >}}
