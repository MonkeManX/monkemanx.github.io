---
title: 'Neovim Tricks'
date: 2024-04-04 
tags: ["neovim"]
---

This is a short cheat sheet for important keybindings in vim more specific for neovim. I am using [NVChad](https://nvchad.com/) as such not all keybindings are applicable to standard vim/nvim.  
Capitalization is important!

**Modes:**  
- `ESC`, switch to normal mode.
-  `v`, switch to visual mode.
- `i` or `a`, switch to insert mode. 
- `R`, replace mode. 

**Navigation:**  
- `arrow keys`, shame on you!
- Movement keys, can be combined with arbitrary number
    - `h`, to the left.
    - `l`, to the right.
    - `j`, downwards.
    - `k`, upwards.
    - Example: `10j` jumps 10 lines downwards, `5k` jumps 4 lines upwards.
- `_` or `0`, beginning of the line.
- `$`, to the end of the line.
- `e`, one word forward.
- `b`, one word backward.
- `:NUMBER`, jumps to the line number.
- `f` + `CHAR`, jumps to the *next* character matching the input char.
- `F` + `CHAR`, jumps to the *previous* character matching the input char. 
- `gg`, moves to the *top* of the files.
- `G`, moves to the *bottom* of the file.
- `20G`, moves cursor to line 20.


**Navigating Code:**  
- `%`, to the matching bracket.
- `[` + `{`, jumps to *previous* curly bracket.
- `]` + `}`, jumps to *next* curly bracket.
- `]` + `m`, next method beginning.
- `[` + `m`, previous method beginning.

**Files:**  
- `:w`, save current file to disk.
- `:wall`, saves all open files to disk.
- `:q`, closes current window.
- `:qall`, closes all windows.
- `:qall!`, forcefully closes all windows.
- `:wq`, saves and closes window.

**Selecting:**
- `v` + `i` + `p`, select the current paragraph.
    - can be repeated `vipipipip`.
- `y` + `a` + `p`, yanks paragraph.

**Editing**:  
- `d` + `POSTFIX`, stands for delete depends on postfix.
    - `d`, deletes whole line 
    - `$`, deletes from current postion up to *last* character in the line.
    - `_`, deletes from current postion up to *first* character in the line.
    - `e`, deletes next word.
    - `b`, deletes previous word.
- `D`, same as `d$`.
- `u`, undo last change.
- `STRG` + `r`, redoes the last change.
- In visual mode: `y`, copy(yank) the selected text.
- `y` + `y`, yank current line.
    - can be paired with a number, example `5` + `y` + `y`, yanks the next 5 lines.
- `p`, paste the yanked text *after* the cursor.
- `P`, paste the yanked text *before* the cursor.
- `x`, deletes current character.
- `c` + `c`, remove current line and edit it. 
- `"` + `BUFFER` + `p`, chooses a clipboard buffer and then pastes it.
- If you have multiple lines and want to add in theb eginning of each line something
    1. Move to the first character of the first line you want to change.
    2. Press Ctrl + V to enter Visual Block Mode.
    3. Use j or arrow keys to select the lines downward.
    4. Press I (uppercase i).
    5. Type -.
    6. Press Esc.
- `STRG` + `a`, increases a number of a string by 1.
- `STRG` + `x`, decreases a number of a string by 1.

**Search:**  
- `/`, searches for patterns forward.
- `?`, searches for pattern backward.
- `n`, jumps to next found pattern.

**Misc:**  
- `vsp`, vertically splits screen.
- `hsplit`, horizontal splits screen.
- In visual mode `>`, intends marked lines in the *right* direction.
- In visual mode `<`, intends marked lines in the *left* direction.
- `z` + `=`, correct spelling mistake.

**Telescope File Browser**
- `<leader>` + `fb`, opens the telescope file browser.
- `ctrl` + `f`, switches between file and folder mode.
- In `normal` mode:
    - `c`, create a file.
    - `r`, rename a file.
    - `y`, copy a file.
    - `d`, delete a file.
    - `g`, goes to parent folder.

**Search and Replace**
- `:%s/foo/bar/gc`, changes all occurence of `foo` in the current file to `bar`, asks for confirmation
- `:%s/foo/bar/g`, changes all occurence of `foo` in the current file to `bar`, doesn't asks for confirmation
- `:%s/<foo>/bar/gc`, Changes only whole wors exactly matching `foo`.
- Example: `:%s/\$\([^$]*\)\$/\\(\1\\)/g``, match text enclosed in dollar signs (e.g., $some random text$) and replace it with LaTeX-style \(some random text\)`.

# Debugging Neovim 

0. Start Neovim
1. Find the PID of neovim `:lua print(vim.fn.getpid())` or use something like `htop` or `btop`.
2. Attach the debugger to neovim `gdb -tui -p PID nvim`, the gdb interactive prompt will appear, useful commands:  
    -`n` step over the next statement   
    -`s` step into the next statement   
    -`c` continue   
    -`finish` step out of the current function   
    -`bt` to see the backtrace from current location   
3. Reproduce the bug and check the backtrace 

----
References:
- [Neovim Dev Tools](https://neovim.io/doc/user/dev_tools.html)
- [NvChad Doc](https://nvchad.com/)
