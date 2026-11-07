# Article narration

Narration uses the official [Audio8 Preview 0.1B INT8 ONNX export](https://huggingface.co/Edge0/audio8-TTS-0.1B-ONNX-INT8) on the CPU. Audio is generated locally and published as MP3. Visitors only use the browser's audio player; GitHub Pages runs no inference.

## Enable an article

Add a boolean field to the article's existing YAML front matter:

```yaml
---
title: My article
date: 2026-01-01
audio: true
---
```

For TOML front matter, use `audio = true`. New pages default to `audio = false` in `archetypes/default.md`. Existing pages are unchanged until opted in.

From the repository root, run:

```bash
./hugo server
```

`./hugo serve` also works. Use the repository-local `./hugo`, including the `./`; the system `hugo` command does not generate audio. Hugo has no native Python pre-build hook. The wrapper opens the Nix environment, starts Hugo, and watches for audio-enabled Markdown pages in `content/`.

The page is served immediately with a placeholder while missing or outdated narration is generated. When generation finishes, Hugo reloads the page with a native player at the bottom, labelled "AI-generated narration" and showing its duration. `preload="none"` avoids downloading audio until playback is requested. Text edits trigger regeneration; unchanged speech is reused. No model sessions are loaded unless uncached speech is needed.

Drafts, future pages, and expired pages are skipped unless the corresponding Hugo flag (`-D`, `-F`, `-E`) is passed. The wrapper supports this repository's `content/` directory, not custom `--source` or `--contentDir` paths. Stop it with Ctrl+C to stop both Hugo and the narration worker.

## Setup on NixOS

Run once, and again after dependency updates:

```bash
cd tools/tts
nix-shell --run 'bash setup_onnx.sh'
```

Setup downloads pinned upstream code and about 420 MiB of inference files into `.cache/`, installs locked Python dependencies in `.venv-onnx/`, and registers the bundled reference voice. The Nix shell provides FFmpeg. The optional voice encoder and HTTP service are not installed. After setup, generation runs offline; PyTorch and ROCm are not needed. The shell uses the local `<nixpkgs>` channel.

## Text, chunks, and caching

The title and readable prose are narrated. Markdown emphasis and link formatting are removed. Images, code blocks, tables, footnotes, math, and embedded media are skipped. Paired Hugo shortcodes retain their inner prose, but their names and arguments are omitted. This is a text extractor, not Hugo's renderer, so check articles with unusual markup before publishing.

Speech is split at paragraph and sentence boundaries, with a default maximum of 300 characters per chunk. Chunk WAVs are cached under `.cache/narration/`. They are joined with short pauses and encoded as mono 96 kbit/s MP3. A failed or interrupted run retains completed chunks for reuse. Empty, silent, invalid, or frame-limited model output is rejected rather than published as complete narration.

The cache hashes spoken text and generation settings, including the model/runtime identity. A tags-only or formatting-only edit updates the source hash without synthesizing speech again. After a text edit, the old player is hidden until current narration is complete. An edit during synthesis discards the outdated result. Failures are logged and retried after another edit or a restart, not continuously.

To reduce CPU use or shorten chunks, restart the server with overrides:

```bash
TTS_THREADS=4 TTS_CHUNK_CHARS=150 ./hugo server
```

For manual generation, from `tools/tts/`:

```bash
nix-shell
.venv-onnx/bin/python generate_audio.py
.venv-onnx/bin/python generate_audio.py --force
```

`--force` regenerates all opted-in pages and their cached chunks. `--watch` runs the watcher without Hugo; `--drafts` includes drafts. Custom settings invalidate the corresponding cache. Only one narration process may run at a time.

## Publish

A page at `content/articles/example.md` produces:

```text
static/audio/articles/example.mp3
data/narration.json
```

The JSON index records duration, hashes, and generation settings. Audio paths follow source paths, including subdirectories and leaf-bundle `index.md` files, independently of slugs and permalinks. Commit both the MP3 files and the JSON index with the article.

```bash
./hugo
# Listen to the narration, then publish:
git add .
git commit -m "Update articles"
git push
```

`./hugo` waits for generation before building and fails if generation fails. The existing GitHub Pages workflow remains unchanged: its system `hugo` publishes the already-generated audio. Missing or outdated narration produces a build warning and no broken player. URLs respect Hugo's `baseURL`, including a subdirectory.

Setting `audio: false` hides the player and stops generation. It does not delete existing MP3s or index entries; remove unwanted files explicitly. Static files are public even if their article is a draft, so do not commit private draft audio. Hugo output, generated image caches, editor settings, model weights, Python environments, cached chunks, and test outputs are ignored by Git. `git add .` includes the website source, published MP3s, and `data/narration.json`.

The scripts, requirements, and tests in `tools/tts/` remain versioned so the local setup can be reproduced. Hugo does not publish that directory; only the generated MP3s in `static/audio/` are served to visitors.

## Listening tests and measurements

The bundled voice has a Chinese reference transcript. English is a primary language of the base checkpoint; German is experimental. Listen for pronunciation errors, omissions, and voice changes before publishing. A successful run does not establish acceptable narration quality.

From `tools/tts/`, inside `nix-shell`:

```bash
.venv-onnx/bin/python test_onnx.py
.venv-onnx/bin/python test_onnx.py --text "A passage to test."
.venv-onnx/bin/python test_onnx.py --text-file passage.txt
.venv-onnx/bin/python -m unittest discover -s tests -v
```

The listening test writes `outputs/onnx/english.wav`, `german.wav`, and `benchmark.json`. Custom input produces `custom.wav`; `--text-file` accepts plain UTF-8 text. These files are overwritten on subsequent runs.

On the Core Ultra 7 265K, ONNX Runtime 1.23.2, eight CPU threads, seed 42:

| Sample | Audio duration | Generation and decoding | Speed |
| --- | ---: | ---: | ---: |
| German | 11.33 s | 12.55 s | 0.90x realtime |
| English | 10.26 s | 11.29 s | 0.91x realtime |

Session loading added 1.59 seconds per process; peak process memory was about 2.3 GiB. These short-passage measurements include prompt prefill but exclude MP3 encoding. Full articles have repeated prompt overhead.

The model cards disagree on licensing: the [base checkpoint](https://huggingface.co/Edge0/Audio8-TTS-Preview-0.1b#license) specifies the revenue-capped Audio8 Community License v1.0, while the ONNX export card lists Apache 2.0. Check the applicable terms before publishing or commercial use.
