"""Generate MP3 narration for Hugo pages with boolean `audio: true` front matter."""

import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import threading

import numpy as np
import soundfile as sf

from article_text import Article, enabled, front_matter, narration_text, split_chunks
from onnx_narrator import Cancelled, OnnxNarrator

SITE = Path(__file__).resolve().parents[2]
PIPELINE_VERSION = 1


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def duration_label(seconds):
    minutes, seconds = divmod(round(seconds), 60)
    return f"{minutes} min {seconds:02d} sec" if minutes else f"{seconds} sec"


@dataclass(frozen=True)
class Settings:
    voice: str = "default"
    threads: int = 8
    seed: int = 42
    chunk_chars: int = 300
    max_frames: int = 1024
    pause_ms: int = 300
    bitrate: str = "96k"

    def __post_init__(self):
        if self.threads < 1 or self.chunk_chars < 40 or self.max_frames < 1 or self.pause_ms < 0:
            raise ValueError("threads and max_frames must be positive; chunk_chars at least 40; pause_ms non-negative")
        if not self.voice or self.voice in {".", ".."} or Path(self.voice).name != self.voice:
            raise ValueError("voice must be a single profile name")


def default_settings():
    return Settings(threads=int(os.environ.get("TTS_THREADS", "8")),
                    chunk_chars=int(os.environ.get("TTS_CHUNK_CHARS", "300")))


class Generator:
    def __init__(self, site=SITE, *, settings=None, backend=None, drafts=False, future=False, expired=False):
        self.site = Path(site).resolve()
        self.settings = settings or default_settings()
        self.backend = backend or OnnxNarrator()
        self.visibility = dict(drafts=drafts, future=future, expired=expired)
        self.cache = self.site / "tools/tts/.cache/narration"
        self.manifest_path = self.site / "data/narration.json"
        self.failed = {}
        self.file_hashes = {}
        self.signature = None

    @contextmanager
    def lock(self):
        self.cache.mkdir(parents=True, exist_ok=True)
        with (self.cache / "generation.lock").open("w") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("Another local narration process is running; stop it before starting this one.") from exc
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def fingerprint(self, text):
        if self.signature is None:
            self.signature = {"pipeline_version": PIPELINE_VERSION, "settings": asdict(self.settings),
                              "backend": self.backend.identity(self.settings.voice)}
        return sha256(json_bytes({"text": text, **self.signature}))

    def file_hash(self, path):
        stat = path.stat()
        key = (stat.st_size, stat.st_mtime_ns)
        cached = self.file_hashes.get(path)
        if cached is None or cached[0] != key:
            cached = (key, sha256(path.read_bytes()))
            self.file_hashes[path] = cached
        return cached[1]

    def read_manifest(self):
        if not self.manifest_path.exists():
            return {"version": 1, "articles": {}}
        result = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        if result.get("version") != 1 or not isinstance(result.get("articles"), dict):
            raise ValueError(f"Invalid narration manifest: {self.manifest_path}")
        return result

    def save_manifest(self, manifest):
        value = json_bytes(manifest)
        if self.manifest_path.exists() and self.manifest_path.read_bytes() == value:
            return
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=self.cache, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(value)
        try:
            os.replace(temporary, self.manifest_path)
        finally:
            temporary.unlink(missing_ok=True)

    def chunk_audio(self, text, stop_event, force=False):
        key = self.fingerprint(text)
        destination = self.cache / "chunks" / f"{key}.wav"
        if destination.exists() and not force:
            try:
                info = sf.info(destination)
                if info.frames and info.channels == 1 and info.samplerate == 44100:
                    return destination
            except (OSError, sf.LibsndfileError):
                pass
        if stop_event.is_set():
            raise Cancelled()
        audio, rate = self.backend.synthesize(text, self.settings, stop_event)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".wav", delete=False) as handle:
            temporary = Path(handle.name)
        try:
            sf.write(temporary, audio, rate, subtype="PCM_16")
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
        return destination

    def source_current(self, article):
        return article.path.is_file() and sha256(article.path.read_bytes()) == article.source_hash

    def generate(self, article, fingerprint, stop_event, force=False):
        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg is missing; run inside tools/tts/shell.nix or use ./hugo.")
        chunks = split_chunks(article.text, self.settings.chunk_chars)
        if not chunks:
            raise ValueError("article has no readable text")
        print(f"[audio] {article.key}: {len(chunks)} chunks", flush=True)
        with tempfile.TemporaryDirectory(dir=self.cache) as directory:
            directory = Path(directory)
            wav = directory / "narration.wav"
            with sf.SoundFile(wav, mode="w", samplerate=44100, channels=1, subtype="PCM_16") as combined:
                for index, chunk in enumerate(chunks):
                    if stop_event.is_set():
                        raise Cancelled()
                    if not self.source_current(article):
                        print(f"[audio] {article.key}: changed during generation; discarding result.", flush=True)
                        return None
                    print(f"[audio] {article.key}: chunk {index + 1}/{len(chunks)}", flush=True)
                    path = self.chunk_audio(chunk, stop_event, force=force)
                    info = sf.info(path)
                    if info.samplerate != 44100 or info.channels != 1:
                        raise ValueError("narration chunks must be 44.1 kHz mono")
                    if index:
                        combined.write(np.zeros(round(44100 * self.settings.pause_ms / 1000), dtype=np.float32))
                    for block in sf.blocks(path, blocksize=44100, dtype="float32"):
                        combined.write(block)
            duration = sf.info(wav).duration
            mp3 = directory / "narration.mp3"
            subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
                            "-i", str(wav), "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame",
                            "-b:a", self.settings.bitrate, str(mp3)], check=True)
            if stop_event.is_set():
                raise Cancelled()
            # An edit or opt-out during synthesis must not publish stale speech.
            if not self.source_current(article):
                print(f"[audio] {article.key}: changed during generation; discarding result.", flush=True)
                return None
            article.audio_path.parent.mkdir(parents=True, exist_ok=True)
            audio_hash = sha256(mp3.read_bytes())
            os.replace(mp3, article.audio_path)
        return {"src": article.audio_path.relative_to(self.site / "static").as_posix(),
                "source_sha256": article.source_hash, "speech_sha256": sha256(article.text.encode()),
                "fingerprint": fingerprint, "audio_sha256": audio_hash,
                "duration_seconds": round(duration, 3), "duration_label": duration_label(duration),
                "engine": self.signature["backend"], "settings": asdict(self.settings)}

    def scan(self, stop_event=None, force=False):
        stop_event = stop_event or threading.Event()
        manifest = self.read_manifest()
        success = True
        count = 0
        for path in sorted((self.site / "content").rglob("*")):
            if stop_event.is_set():
                raise Cancelled()
            if path.suffix.lower() not in {".md", ".markdown"} or path.stem == "_index":
                continue
            key = path.relative_to(self.site / "content").as_posix()
            source_hash = None
            try:
                raw = path.read_bytes()
                source_hash = sha256(raw)
                if self.failed.get(key) == source_hash and not force:
                    success = False
                    continue
                metadata, body = front_matter(raw.decode("utf-8"))
                if not enabled(metadata, **self.visibility):
                    continue
                count += 1
                text = narration_text(metadata.get("title", path.stem), body)
                relative_audio = Path("audio") / Path(key).with_suffix(".mp3")
                article = Article(path, key, source_hash, text, self.site / "static" / relative_audio)
                fingerprint = self.fingerprint(text)
                record = manifest["articles"].get(key, {})
                reusable = (not force and record.get("fingerprint") == fingerprint
                            and record.get("src") == relative_audio.as_posix()
                            and article.audio_path.is_file() and article.audio_path.stat().st_size > 0
                            and record.get("audio_sha256") == self.file_hash(article.audio_path))
                if reusable:
                    # Tags, dates, or Markdown-only changes do not require speech synthesis.
                    if record.get("source_sha256") != source_hash:
                        record["source_sha256"] = source_hash
                        self.save_manifest(manifest)
                    continue
                record = self.generate(article, fingerprint, stop_event, force)
                if record is not None:
                    manifest["articles"][key] = record
                    self.save_manifest(manifest)
                    print(f"[audio] Saved {relative_audio} ({record['duration_label']}).", flush=True)
                else:
                    success = False
                self.failed.pop(key, None)
            except Cancelled:
                raise
            except Exception as exc:
                success = False
                self.failed[key] = source_hash
                print(f"[audio] ERROR {key}: {exc}", flush=True)
        return success, count

    def watch(self, stop_event):
        try:
            with self.lock():
                print("[audio] Watching audio-enabled pages. Failures retry after an edit or restart.", flush=True)
                while not stop_event.is_set():
                    self.scan(stop_event)
                    stop_event.wait(1)
        except Cancelled:
            pass
        except Exception as exc:
            print(f"[audio] ERROR: {exc}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--force", action="store_true", help="Regenerate all opted-in pages and their chunks")
    defaults = default_settings()
    parser.add_argument("--threads", type=int, default=defaults.threads)
    parser.add_argument("--chunk-chars", type=int, default=defaults.chunk_chars)
    parser.add_argument("--voice", default="default")
    parser.add_argument("--drafts", action="store_true")
    args = parser.parse_args()
    if args.threads < 1 or args.chunk_chars < 40 or not args.voice or args.voice in {".", ".."} or Path(args.voice).name != args.voice:
        parser.error("threads must be positive, chunk-chars at least 40, and voice a single name")
    if args.force and args.watch:
        parser.error("--force cannot be combined with --watch")
    stop = threading.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())
    generator = Generator(settings=Settings(threads=args.threads, chunk_chars=args.chunk_chars, voice=args.voice),
                          drafts=args.drafts)
    if args.watch:
        generator.watch(stop)
        return
    try:
        with generator.lock():
            success, count = generator.scan(stop, force=args.force)
        if not success:
            raise SystemExit(1)
        print(f"[audio] Narration up to date for {count} enabled pages.", flush=True)
    except Cancelled:
        raise SystemExit(130)
    except (OSError, RuntimeError, ValueError) as exc:
        parser.exit(1, f"[audio] ERROR: {exc}\n")


if __name__ == "__main__":
    main()
