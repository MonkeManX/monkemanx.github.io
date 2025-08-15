---
title: 'Introduction to Setting Up NixOS'
date: 2025-07-23 09:00:00
tags: ["Linux"]
draft: True
---

 A while ago my computer broke, I never quite figured out what exactly the problem was, but it was probaly related to the motherboard. I thought this was a good oppourtintiy for an upgrade as my old my was over 10 years old. So after I bought  the parts and build my new pc, the question became what oporating system to use. I knew that I would use windows for the rare gaming I do, but in additon i wanted second eprating sytsem i.e. dual booting for work related stuff, my choice fell on NixOS a linux oeprting system that is fully determinstic, I was already previosuly curious about nixos but never managed to make it work be it on a VM or on my rasperry, as such this represetned a good opportunity to finaly make nixos work properly.

## Why NixOS?

There are many linux distirbution, almost as many as sandcorns as on a beach, from the memey hannah montana oeprating system, the trusted stable debian distibution, ubuntu for the evryday man, fedora for the coperate worker, to arch and gentoo for the tinkerer.

NixOS is special in that it promises fully determinisic declerative operating system resistant to breakge. In most operating system if you want to isntall a software than you either downlaod the fostware from your intenret browser and rung it liek in windows or you use a apckage manager like in debian `sudo apt-get install firefox` or arch `sudo pacman -S firefox`.
NixOS differs from both of these imperative approaches, where one software is isnatlled after another in a sequential manner, to a declerative approach, where we have one file in which we write the sofwtare that we want to install and it gets installed for you.

Why would we want this? This has numerous advantages, (1) because all the software that you have installed on your system is descirbed in a single file, you can copy this file to another system that is running nix and you will have all software described above it (2) because everything is written on a file, we can take hashes hashes of the current software, which gives us a uniqe (we can still have hash collision) identifiable srting, that represents the current isntalled software and importantly its version, this allows us when movign the file to another system nox only to install exact same sofware, but also the sofwrate will be the exact same version, for example you run neovim version 0.9 in one system and copy the software file to naother system running nix ou will too have neovim running exactyl the same version 0.9 (3) when softwar gets updates regression, bugs or other features cna be introduced that break the software, this is especially problematic for systems that use rolling release, meaning that software in the oepraitng system gets updates when the softwraeg ets a new update, as opposed having a release cycle where software will be released i ncycles allowing thus for betetr testting, but even in idisturbiton with release cylses bug can slip through the etsting phase, in a normal oeprating system you need to hope that system destyrong bug does not slip throguh (which almost never happens) else you would need to reisntlla you whole system, but even if single software breaks you need to uninstall then ew version and reinstall an older version, in NixOS because we keep hashes of the software and old software on the system when a bug occurs we can simply rollback the oeprating system to an odler configuraton with the press of a button. (4) The updating of yoru system in NixOs is fully atomic this means either the updates suceeds and all yous oftware is uscefull updated or it fails, but you will never have a mix of half broken software and good working software (5) the fully etermisntic nature of nixos goes above simply keeping track of the version of the ofwatre you are running, it also keeps tracks of all your operating system and with the usage of extension even all the settings of your software, for example in the delercative file you can write down your hostname or user accounts or keyboardlayout and when copying the file to naother system all this will remain. (6) because all configuration of both software and oeprating system can be done in one file at one palce, you dont need to scorue through all your `.config` files or at another places you can make yoru seetign changes all at one place, through simply chaging some of the lines in the nix cofniguraiton file. (7) You also will have never to deal with dependecny conflict ever agin, because nixos gives evry libary and software a unqiue hash, it can differentiate between oen software needing to use an oler liabry while another softwraen eeds the neevr evrsion of the smael ibary.

But its not all sunshine and rainbows in niox, nixos also has some disavnatges (1) the learning curve if nixos is high, becazse all configuaraiton file of nixos is written in its own fucntional programming language nix, you will need to learn the language to a certain extend at least to make changes (2) the docuemntation of nixos is not great, because there are so many setting that can be set, by the natue that each software expsoes many settings, not everythign can be docuemnted and it is often tiems hard to know what teh setting is caalled to change a given thing, often times ones need to scoru github nix repos to see how someone else did it to learn how to do it in nixos, (3) andother big problem is that if you have erros in our conigfuration the erros that are produced by your nixos system are often obscure and it is often not clear what tehse error mean, i myself am unsure if this is jsu tthe nature of funtional prorgammign languages that are lazily evlauted or if nix language itself is at fault, (proably both to a cetain exten, tough i wil lsay haskell which is equaly lazily evaluated and ufnction also has many ratehr osbcure error) (4) it is also improtant to keep in mind, becuase nixos keeps hashes of all the softwrae you isntall and older liabries, you willl need more disk space than on a reguar linux operaitn sytsem, tough i personally feel it manabgnle (5) setting up delvoping environments can be harder, because they to "need" to be determinstic.

Personally what really attracted me at the nixos, is the promise to have one derterminstic file i nwhich i can keeep track fo my whole oeperaitng sytsem all my settign and configuration and when i move this to another file, my system will be exactly the same, in other word you need to mkake your oeprating stysme cofngiruation file once and then theortehicalyl you will never need to touch it agin, in practise you will soemtimes if youwant to isntall or udpate osofwtare or change setting.


## What this article is about

Important cveat that has to make here, when I said that even the version of the software are fully detterminstic this too is not entriely true, NixOS configuration can be written two ways (1) the "normal" way and the (2) flakes way, in the falke way the version are fully deteerminstic, similar to other software manager like `cargo` from rust, it creates a `.lock` file in which all the version number are listed, this is not done in (1) here the version are not fully determinstic, if this tells you somehting (2) can be understood as being purely functional including inputs like where software comes from (1) is not pure functional, the inputs are not fulyl determinstic.

We already talked about that NixOs has one conguraito nfile that determisntic deetermines the whole system, but this is not entirely true, since the ocnifugraiton file is wirtten using their own programming language `nix`, it is equaly possible to sperate the file into multiple other files with different seperatio nfo cocnern, think about it like an Obejcted oriented programming project, where yo uhave different classses for different section of project, the same thing you can do in nix. As such there eixts many possible ways on how strcture ones fconiugraiton file, if one chooses to sue multiple ones.

In the following artcile I want to explain one possbile way on how to srtucture on NixOs Configuration, filled with example appliction so that in the end you will have a fully working environment with all the importaaaaaaant software, with a nxios configuration thta is structured in such a way that it can be easily cusotmized.

My NixOs config is ehavily inspired by [Nixy], as such another way to think about this article is as an attempt to explain their NixOs configuration, sprinkeled in with some of my own shit.


## Installing NixOs: A walk in the Park

Okay, you are now convicned by amazing prose to give NixOs a try, but where d oI start? I am Glad you asked because this is what this whole thing is about.

The first thign that we need to do is to create a bootable medium, that is in our case an USB-stick on which we isntall the nixos operating system, from this usb-stick we will then later boot and insteall NixOS.

So you will need:
- An Usb Stick at least 5 Gib
- A working Computer
- Internet Connection

Head to the [NixOS]() Homepage and follow the download link, you will have the option to chosoe form minimal, GNOME and KDE, which are different desktop environment aka how zour deskop will look and feel, KDE feels morel iek windows, GNOME more like android or apple.
The exact choice doesnt matter that much, as we will chnage it later on, don't choose minimal tough if yo udont wnat to start from a terminal, I picked KDE.

Next we need a software which will flash the downloaded NIxOS ISO to our USB-Stick, for windows [rufus]() is an good option, on linux I like [pop-flasher]() you might get a warning that the ISO choosen is not supported, i think yo ucan ignore that.

After we have done, its now time to install NixOs, for this put the USB:stick into the computer you want to install it on, shut down the pc and start it again, you will need to get into the boot menu for that you will need to press a key when your pc starts up, the exact key differs from mainboard to mainboard, if you know your mainboard manufactor you can google else you can try one of these common keys `F10`, `F11`, `F12`, `DEL`.
If ou have arrived in the boot menu select the the usb-stick for booting, fi yo udont know its name you should be able to recognize the usb stick by the amount of of storage which should be far less in your usb-stick than on your physical disk.

After you have booted you should be now in a live NixOs environment from here on you should be able to isntall NixOs using the installer. The isntaller should be rather straightforward just follow it and isntall it, after taht you can huwtdown the pc remove the usb-stick and start the PC again you should now boot into NixOs.


## NixOs: The Basics

Before we go all in with the cusotmization and ricing and more advanced stuff We need to go throught the basics, lame I know, but nessecarily espeically because NixO rather poor documenation and numerous command that seemingly all do the same thing while having different names.

For starter you will find the configuration files in `/etc/nixos`, it should consits of two files `configuration.nix` and `hardware-configuration.nix`, the former defiend you entire operating sytsem and software, this is where you will do changes if you want to isntall new software or adjsut setttings, the later file is automatically generated based on the hardware that your computer used and defines things, like the disks you have where the bios is installed and so on, you will almost never need to touch this and if you do, you will proably alreday know what you are doing.





I wont go over the syntax of thep rogaming language niix which nixos uses, it is rather similar to other fucntional languages and i think the mosti mportant stuff you will learn by doing, i'll try to explain synatx that is unclear when it coems up.


## It Begins or The End is already built in the Beginning



## A Dirge of Windows and Linux: Failing, more Failing and Succeeding

This is about my struggle to dualboot NixOs and Windows, you can skip this if you are not interested. If you want to dualboot, the single most important advice i can give you is **install windows first*** then isntall NixOs. Tough I do think you will elarn a thign or two on how to fix a borked setup.
