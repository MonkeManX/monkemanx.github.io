---
title: 'Neovim Markdown Preview: Command not working'
date: 2024-08-20
tags: ["Neovim"]
---

{{< info "Info" >}}
This post isn't meant as an introduction to any of the topics discussed below. Instead, it's a brief guide on how to make the Markdown-Preview plugin work.
{{< /info >}}

## Background

(Neo)vim is, for the most part, the only editor I use for all my needs -— whether it's programming, editing configuration files, or taking notes. I write all of my notes in Markdown for several reasons: it's widely compatible, has easy-to-understand syntax, is very readable even without rendering, and, through various flavors, allows for additional functionality.

Even though Markdown is quite readable in plain text, it's helpful to render it for features like images and LaTeX. To do this, I use the Neovim plugin [Markdown Preview](https://github.com/iamcco/markdown-preview.nvim).

{{< rawhtml >}}
<video style="display: block; margin-left: auto; margin-right: auto; width:70%" controls muted>
    <source src="/attachments/Markown_preview.mp4" type="video/mp4">
    Your Browser does not support this embedded video.
</video>
{{< /rawhtml >}}



## Installation

If you're using the Lazy plugin manager, you can install the Markdown Preview plugin by opening your Neovim configuration (in Lunarvim with <space> + L + c) and adding the following to the list of plugins:
```lua
 {
    "iamcco/markdown-preview.nvim",
    ft = "markdown",
    build = function()
        vim.fn["mkdp#util#install"]()
    end,
    config = function()
      vim.cmd([[do FileType]])
      vim.cmd([[
         function OpenMarkdownPreview (url)
            let cmd = "firefox -P 'Clean' --new-window " . shellescape(a:url) . " &"
            silent call system(cmd)
         endfunction
      ]])
      vim.g.mkdp_browserfunc = "OpenMarkdownPreview"
      vim.g.mkdp_theme = "dark"
    end,
  },
```
In the `OpenMarkdownPreview` function, make sure to replace `firefox` with the name of the browser you use. If you don't have a browser profile named clean, you should also remove the `-P 'Clean'` option.

After restarting Neovim, the plugin should install automatically. If not, type `:Lazy`, press `S` to sync, and then `I` to install the plugin. You can now use the command `:MarkdownPreview` when inside a Markdown file, and your browser should open with the rendered Markdown file. If you're interested in further configuring the plugin, check out its [GitHub repository](https://github.com/iamcco/markdown-preview.nvim).

## Command not Working

If you run the command and nothing happens -- no error message and your browser doesn’t open—try typing `:messages` to see if there’s an error. If you see something like `Error: Cannot find module 'tslib'`, follow these steps to fix it:
1. Check your message log for a file path similar to `/lvim/lazy/markdown-preview.nvim/app/lib/app/` (your path might differ).
2. Go to where the plugin is installed:
```
cd ~/lvim/lazy/markdown-preview.nvim/app/lib/app/
```
3. Install the necessary dependencies:
```
npm install
```
4. Restart neovim, it should work now.


---
References:
- https://github.com/iamcco/markdown-preview.nvim/issues/148
- https://www.reddit.com/r/neovim/comments/1b1kw8d/help_configuring_markdownpreviewnvim_with_custom/
