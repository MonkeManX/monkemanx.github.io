---
title: 'A Basic Linux Rice'
date: 2024-08-21
tags: ["linux"]
---

# Introduction

A few months ago, I switched from [Debian](https://www.debian.org/) to the [Arch](https://archlinux.org/) operating system. There were three major reasons for my switch:

1. Debian is often hailed as the most *stable* operating system out there. This stability comes from the extensive testing that new software or updates undergo before being released. However, this also has a disadvantage: the software on Debian is often outdated. For example, at the time of writing this post, the latest version of Neovim available on the current Debian release (Bookworm) is `0.7.2`, while Neovim has already released version `0.10.1`.
   
2. Debian comes with a lot of default software that you might not need. I wanted to try a minimal installation with the dynamic tiling window manager [Hyprland](https://hyprland.org/), which, at that time, wasn't supported by Debian.

3. Arch, being very minimal and bare-bones, is great for learning the ins and outs of Linux.

In the process of switching, I built my 'own' operating system step by step by installing and customizing various pieces of software. I gradually *riced* my setup to what you can see below:

{{< gallery dir="/attachments/desktop/" width="100%" height="510px">}}

# What is Ricing?

Linux ricing describes the process of customizing one's desktop environment to their liking. It involves modifying icons, color schemes, the taskbar, startup apps, screensaver, lock screens, and much more. The saying "your creativity is the only limit" is especially true when it comes to ricing your Linux environment.
You can find many Linux rices online, with one popular gathering place being the *unixporn* subreddit.

# My Rice

In this section, I want to go through how I customized linux to look like in the slideshow above. This is not meant as an elaborate complete guide on how to customize linux, but more as a form of documentation for myself and as a starting point of what you can do for others.

My entire rice is based on the [gruvbox dark](https://github.com/morhetz/gruvbox) color palette, if at any point In the guide I use colors I got them from this repository.

## Tiling Manager: i3 

[I3](https://i3wm.org/) is a dynamic [tiling window manager](https://en.wikipedia.org/wiki/Tiling_window_manager) for your Linux desktop environment.

{{< rawhtml >}}
<video style="display: block; margin-left: auto; margin-right: auto; width:80%" controls muted>
    <source src="/attachments/i3.mp4" type="video/mp4">
    Your browser does not support this embedded video.
</video>
{{< /rawhtml >}}

I started with the i3 [default config](https://github.com/i3/i3/blob/next/etc/config.keycodes) and modified it to suit my needs. Here, I’ll highlight some parts of my configuration that differ from the default. You should find the default config file under `~/.config/i3/config`. If it’s not there, create the file and copy the default i3 configuration into it.

I set the font in the i3 config to one of the [Nerd Fonts](https://www.nerdfonts.com/):
```sh
font pango:Hack Nerd Font 10
```
For this to work, you first need to install the font. On Arch, you can do this with `pacman -S <name_nerd_font>`. You can find the names of the Nerd Fonts [here](https://archlinux.org/groups/x86_64/nerd-fonts/).

I created some custom keybindings to launch apps that I often use:
```sh

# start a terminal
bindsym $mod+t exec kitty

# start internet browser
bindsym $mod+i exec firefox

# open file manager
bindsym $mod+f exec thunar

# kill focused window
bindsym $mod+Shift+q kill

# take screenshots
bindsym Print exec "flameshot gui"

# start dmenu (a program launcher)
# bindsym $mod+m exec --no-startup-id dmenu_run # old
bindsym $mod+m exec --no-startup-id rofi -show run
```

Since I use a dual-monitor setup, I define my two monitors:
```sh
set $monitor1 "HDMI-0"
set $monitor2 "DVI-D-2"

workspace $ws1  output $monitor1  
...
workspace $ws10 output $monitor2  

bindsym $mod+1 workspace number $ws1
...
bindsym $mod+0 workspace number $ws10
```
If you're unsure which exact port your monitor is using, you can use `xrandr` to find out.

Setting my Gruvbox color scheme:
```sh
class                 border  backgr. text    indicator child_border
client.focused          #d65d0e #d65d0e #fbf1c7 #d65d0e   #d65d0e 
client.focused_inactive #282828 #282828 #fbf1c7 #282828   #282828
client.unfocused        #282828 #282828 #fbf1c7 #282828   #282828 
client.urgent           #2f343a #900000 #ffffff #900000   #900000
client.placeholder      #000000 #0c0c0c #ffffff #000000   #0c0c0c

client.background       #ffffff
```

Finally, I use the image viewer [feh](https://github.com/derf/feh) for my desktop background and Polybar for my taskbar:
```sh
exec_always ~/.config/polybar/launch.sh &
exec_always feh --bg-fill ~/Pictures/wallpaper/reverend_insanity.jpeg 
```

You can restart i3 and apply your changes using the key combination `SUPER + SHIFT + r` (unless you’ve changed this keybinding in the i3 configuration file).

## Taskbar: Polybar

[Polybar](https://github.com/polybar/polybar) is an easy-to-use status bar.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/polybar1.jpg">
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/polybar2.jpg">
    <figcaption style="text-align:center; margin-top: 10px;"></figcaption>
</figure>
{{< /rawhtml >}}

After installing Polybar, you should be able to find the configuration files under `~/.config/polybar/config.ini`.

I first changed the colors to the Gruvbox theme:
```sh
background = #282828
background-alt = #282828 
foreground = #ebdb2
alert = #cc241d
green = #98971a 
yellow = #d79921 
blue = #458588
purple = #b16286
aqua = #689d6a 
red = #fb4934
```

Then, I set all the modules that I want to have in my status bar:
```sh
modules-left = xworkspaces xwindow
modules-right = pulseaudio memory cpu date
```

I also changed the fonts:
```sh
font-0 = "Hack Nerd Font:size=10;2"
font-1 = "Hack Nerd Font:size=10;2"
```

Finally, I set the color for CPU, Memory, Volume, and Time to yellow:
```sh
format-prefix-foreground = ${colors.yellow}
```

## Terminal: Kitty

[Kitty](https://sw.kovidgoyal.net/kitty/) is a terminal emulator that uses the GPU to make it blazingly fast.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/kitty.jpg">
    <figcaption style="text-align:center; margin-top: 10px;"></figcaption>
</figure>
{{< /rawhtml >}}

As with the previous two applications, you will find its configuration file in `~/.config/kitty/kitty.conf`.

First, let's set the font:
```sh
font_family     Hack Nerd Font
font_size 	    13.0
bold_font       auto
italic_font     auto
bold_italic_font auto
```

Next, we’ll create keybindings that allow us to change the font size in the terminal using `CTRL + PLUS` and `CTRL + MINUS`:
```sh
# increase font size
map ctrl+plus   change_font_size all +1.0
map ctrl+kp_add change_font_size all +1.0

# decrease font size
map ctrl+minus   change_font_size all -1.0
map ctrl+kp_minus change_font_size all -1.0
```

Finally, let's set the Gruvbox theme:
```sh
# Gruvbox theme 
# Based on https://github.com/morhetz/gruvbox by morhetz <morhetz@gmail.com>
# Adapted to Kitty by wdomitrz <witekdomitrz@gmail.com>

cursor                  #928374
cursor_text_color       background

url_color               #83a598

visual_bell_color       #8ec07c
bell_border_color       #8ec07c

active_border_color     #d3869b
inactive_border_color   #665c54

foreground              #ebdbb2
background              #282828
selection_foreground    #928374
selection_background    #ebdbb2

active_tab_foreground   #fbf1c7
active_tab_background   #665c54
inactive_tab_foreground #a89984
inactive_tab_background #3c3836

# black (bg3/bg4)
color0                  #665c54
color8                  #7c6f64

# red
color1                  #cc241d
color9                  #fb4934

# green
color2                  #98971a
color10                 #b8bb26

# yellow
color3                  #d79921
color11                 #fabd2f

# blue
color4                  #458588
color12                 #83a598

# purple
color5                  #b16286
color13                 #d3869b

# aqua
color6                  #689d6a
color14                 #8ec07c

# white (fg4/fg3)
color7                  #a89984
color15                 #bdae93
```

### File Explorer: Thunar

[Thunar](https://docs.xfce.org/xfce/thunar/start) is a file manager for the XFCE desktop environment.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/thunar_gruvbox.jpg">
    <figcaption style="text-align:center; margin-top: 10px;"></figcaption>
</figure>
{{< /rawhtml >}}

The Gruvbox theme can be installed via pacman using `sudo pacman -S gruvbox-material-gtk-theme-git` and `sudo pacman -S gruvbox-material-icon-theme-git`. To switch to the Gruvbox theme, I use [LXAppearance](https://github.com/lxde/lxappearance), which can be installed with `sudo pacman -S lxappearance`. Open LXAppearance and select "Gruvbox-material-Dark" under both the Widgets and Icon Theme sections.

If Thunar doesn’t change its appearance after this, it might be running as a daemon. Run `thunar -q` to quit the daemon and then reopen Thunar; the theme should now be applied.

### Browser: Firefox

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/firefox.jpg">
    <figcaption style="text-align:center; margin-top: 10px;"></figcaption>
</figure>
{{< /rawhtml >}}

The Gruvbox theme can be installed on Firefox via an [addon](https://addons.mozilla.org/en-US/firefox/addon/gruvbox-dark-theme/).

### System Monitor: Btop

[Btop](https://github.com/aristocratos/btop) is a resource monitor, which is a more feature-rich version of `htop`.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/btop.jpg">
    <figcaption style="text-align:center; margin-top: 10px;"></figcaption>
</figure>
{{< /rawhtml >}}

To change the theme in Btop, run `btop`, press `ESC`, choose `Options`, and then select `gruvbox-ark-material` as the color theme.

### PDF Reader: Zathura

[Zathura](https://wiki.archlinux.org/title/Zathura) is a customizable, minimalistic PDF reader that supports Vim keybindings.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/zathura.jpg">
    <figcaption style="text-align:center; margin-top: 10px;"></figcaption>
</figure>
{{< /rawhtml >}}

If you don’t have a config folder for Zathura, you'll need to create one. Navigate to `~/.config/` and run `mkdir Zathura`. After this, you can install the Gruvbox theme by downloading it from [GitHub](https://github.com/eastack/zathura-gruvbox). Unpack it and run:
```sh
cd zathura-gruvbox
cp zathura-gruvbox-dark ~/.config/zathura/zathurarc
```

### Fun: CBonsai, Fortune, Pipes.Sh, CMatrix and Fastfetch

[CBonsai](https://gitlab.com/jallbrit/cbonsai) is a program that grows a bonsai tree, and [Fortune](https://wiki.archlinux.org/title/Fortune) is a program that displays random silly phrases from a database. [Pipes.sh](https://github.com/pipeseroni/pipes.sh) animates pipes in your terminal. [Cmatrix](https://github.com/abishekvashok/cmatrix) makes you look like a hacker. Last but not least, [Fastfetch](https://github.com/fastfetch-cli/fastfetch) is the successor to Neofetch and displays information about your system.

{{< rawhtml >}}
<video style="display: block; margin-left: auto; margin-right: auto; width:80%" controls muted>
    <source src="/attachments/linux_fun.mp4" type="video/mp4">
    Your browser does not support this embedded video.
</video>
{{< /rawhtml >}}

You can combine CBonsai and Fortune to grow a bonsai while displaying a random message:
```sh
cbonsai -S -t 0.5 -m "$(fortune)"
```

The programs can be installed with the following command:
- Fastfetch: `sudo pacman -S fastfetch`
- Fortune: `sudo pacman -S fortune-mod`
- CBonsai: `yay -S cbonsai`
- Pipes.Sh: `yay -S pipes.sh`
- Cmatrix: `yay -S cmatrix-git`

If you’d like, you can autostart these programs to have a nice welcome screen. For example to autostart fastfetch and cbonsai, open your i3 config and add the following lines:
```sh
exec --no-startup-id i3-msg 'workspace 1; exec kitty --hold fastfetch'  
exec --no-startup-id i3-msg 'workspace 1; exec kitty --hold cbonsai -S -t 0.5 -m "$(fortune)"'
```


### Backup Dotfiles Using GitHub

Now that you have a lot of configuration files that you might want to back up, one effective method is to use a Git repository.

First, create a bare Git repository:
```sh
git init --bare $HOME/dotfiles
```

Next, add the following lines to your shell configuration file (in this example, I’m using `fish`):
```sh
alias config='/usr/bin/git --git-dir=$HOME/dotfiles/ --work-tree=$HOME'
```

In the future, you can update your Git repository with the following commands:
```sh
config add ~/.config/nvim
config commit -m "nvim changes"
config push
```

To hide files that you’re not tracking, run this command:
```sh
config config --local status.showUntrackedFiles no
```

To push your dotfiles to GitHub, you’ll need to create a GitHub repository and define a remote:
```sh
config remote add origin REMOTE-URL
```

---
References:
- [Image Slideshow Code](https://github.com/tbiering/hugo-slider-shortcode)
- [Dotfiles Backup](https://www.atlassian.com/git/tutorials/dotfiles)
