---
title: 'Neovim Cheat Sheet'
date: 2024-04-04 
tags: ["neovim"]
---

# Neovim Cheat sheet

This is a short cheat sheet for important keybindings in vim more specific for neovim.
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

