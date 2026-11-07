import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from article_text import enabled, front_matter, narration_text, split_chunks
from generate_audio import Cancelled, Generator, Settings, duration_label
from hugo_local import flag
from onnx_narrator import OnnxNarrator


class TextTests(unittest.TestCase):
    def test_yaml_toml_json_front_matter(self):
        samples = [
            "\ufeff---\r\ntitle: Example\r\naudio: true\r\n---\r\nBody.",
            '+++\ntitle = "Example"\naudio = true\n+++\nBody.',
            '{"title": "Example", "audio": true}\nBody.',
        ]
        for source in samples:
            with self.subTest(source=source):
                meta, body = front_matter(source)
                self.assertEqual(meta, {"title": "Example", "audio": True})
                self.assertEqual(body, "Body.")

    def test_front_matter_requires_mapping_and_closing_delimiter(self):
        for source in ("---\naudio: true", "---\n- wrong\n---\nBody"):
            with self.assertRaises(ValueError):
                front_matter(source)

    def test_opt_in_is_boolean_and_respects_visibility(self):
        self.assertFalse(enabled({"audio": "true"}))
        self.assertFalse(enabled({"audio": False}))
        self.assertFalse(enabled({"audio": True, "draft": True}))
        self.assertTrue(enabled({"audio": True, "draft": True}, drafts=True))
        self.assertFalse(enabled({"audio": True, "date": "2099-01-01"}))
        self.assertTrue(enabled({"audio": True, "date": "2099-01-01"}, future=True))
        self.assertFalse(enabled({"audio": True, "expiryDate": "2000-01-01"}))
        self.assertTrue(enabled({"audio": True, "expiryDate": "2000-01-01"}, expired=True))

    def test_readable_prose_excludes_code_math_media_tables_and_footnotes(self):
        body = r"""## Heading

Hello **world**. Read [this link](https://example.com), and use `nix-shell`.

![image description](image.png)

```python
DO_NOT_READ_CODE
```

| Header | Other |
| --- | --- |
| DO_NOT_READ_TABLE | value |

Formula $DO_NOT_READ_MATH$ and \(DO_NOT_READ_LATEX\).

$$
DO_NOT_READ_BLOCK_MATH
$$

A claim[^1].

[^1]: DO_NOT_READ_FOOTNOTE

<script>DO_NOT_READ_SCRIPT</script>
<figure><figcaption>DO_NOT_READ_FIGURE</figcaption></figure>
<!-- DO_NOT_READ_COMMENT -->

{{< info "DO_NOT_READ_ARGUMENT" >}}
Keep this prose.
{{< /info >}}
{{< img src="DO_NOT_READ_IMAGE" >}}
"""
        text = narration_text("Title", body)
        self.assertTrue(text.startswith("Title."))
        for expected in ("Heading.", "Hello world.", "this link", "nix-shell", "A claim.", "Keep this prose."):
            self.assertIn(expected, text)
        self.assertNotIn("DO_NOT_READ", text)
        self.assertNotIn("https://", text)
        self.assertNotIn("image description", text)
        self.assertNotIn("{{", text)

    def test_entities_and_nested_html(self):
        text = narration_text("Title", "<p>Fish &amp; chips <strong>are good</strong>.</p><pre><code>omit</code></pre><p>Afterwards.</p>")
        self.assertIn("Fish & chips are good.", text)
        self.assertIn("Afterwards.", text)
        self.assertNotIn("omit", text)

    def test_chunks_preserve_words_and_stay_bounded(self):
        text = " ".join(["A sentence with ordinary words."] * 50)
        chunks = split_chunks(text, 90)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(0 < len(chunk) <= 90 for chunk in chunks))
        self.assertEqual(" ".join(chunks), text)
        self.assertEqual(split_chunks(""), [])
        self.assertTrue(all(len(chunk) <= 40 for chunk in split_chunks("x" * 120, 40)))
        with self.assertRaises(ValueError):
            split_chunks("text", 0)

    def test_settings_validation(self):
        for kwargs in ({"voice": ".."}, {"voice": "../escape"}, {"threads": 0}, {"chunk_chars": 10}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Settings(**kwargs)

    def test_duration_and_hugo_flags(self):
        self.assertEqual(duration_label(522), "8 min 42 sec")
        self.assertEqual(duration_label(59.9), "1 min 00 sec")
        self.assertTrue(flag(["server", "-D"], "-D", "--buildDrafts"))
        self.assertFalse(flag(["server", "--buildDrafts=false"], "-D", "--buildDrafts"))


class FakeBackend:
    def __init__(self, revision="test-1"):
        self.calls = []
        self.revision = revision
        self.fail = False
        self.callback = None

    def identity(self, voice):
        return {"engine": "test", "revision": self.revision, "voice": voice}

    def synthesize(self, text, settings, stop_event):
        self.calls.append(text)
        if self.fail:
            raise RuntimeError("deliberate synthesis failure")
        if self.callback:
            self.callback()
        return np.sin(np.arange(4410) * 0.04).astype(np.float32) * 0.1, 44100


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.site = Path(self.directory.name)
        self.article = self.site / "content/articles/example.md"
        self.article.parent.mkdir(parents=True)
        self.write_article()
        self.backend = FakeBackend()
        self.generator = Generator(self.site, backend=self.backend)
        self.mp3 = self.site / "static/audio/articles/example.mp3"

    def write_article(self, body="A short narration test.", extra="", audio="true"):
        self.article.write_text(f"---\ntitle: Example\naudio: {audio}\n{extra}---\n{body}\n", encoding="utf-8")

    def record(self):
        return json.loads(self.generator.manifest_path.read_text())["articles"]["articles/example.md"]

    def fake_ffmpeg(self, args, **kwargs):
        wav = Path(args[args.index("-i") + 1])
        Path(args[-1]).write_bytes(b"ID3-test-mp3" + wav.read_bytes()[:100])

    def scan(self, generator=None, **kwargs):
        generator = generator or self.generator
        with patch("generate_audio.shutil.which", return_value="/ffmpeg"), patch("generate_audio.subprocess.run", side_effect=self.fake_ffmpeg):
            with generator.lock():
                return generator.scan(**kwargs)

    def test_opt_in_generation_and_cache(self):
        self.assertEqual(self.scan(), (True, 1))
        self.assertTrue(self.mp3.is_file())
        record = self.record()
        self.assertEqual(record["src"], "audio/articles/example.mp3")
        self.assertEqual(record["source_sha256"], hashlib.sha256(self.article.read_bytes()).hexdigest())
        self.assertEqual(record["audio_sha256"], hashlib.sha256(self.mp3.read_bytes()).hexdigest())
        calls = len(self.backend.calls)
        modified = self.mp3.stat().st_mtime_ns
        manifest_modified = self.generator.manifest_path.stat().st_mtime_ns
        self.assertEqual(self.scan(), (True, 1))
        self.assertEqual(len(self.backend.calls), calls)
        self.assertEqual(self.mp3.stat().st_mtime_ns, modified)
        self.assertEqual(self.generator.manifest_path.stat().st_mtime_ns, manifest_modified)

    def test_metadata_and_markdown_only_changes_reuse_audio(self):
        self.scan()
        calls = len(self.backend.calls)
        fingerprint = self.record()["fingerprint"]
        self.write_article(body="A **short** narration test.", extra="tags: [Test]\n")
        self.scan()
        self.assertEqual(len(self.backend.calls), calls)
        self.assertEqual(self.record()["fingerprint"], fingerprint)
        self.assertEqual(self.record()["source_sha256"], hashlib.sha256(self.article.read_bytes()).hexdigest())

    def test_text_changes_and_opt_out(self):
        self.scan()
        old = self.record()["fingerprint"]
        self.write_article("Completely different text.")
        self.scan()
        self.assertNotEqual(old, self.record()["fingerprint"])
        calls = len(self.backend.calls)
        self.write_article(audio="false")
        self.assertEqual(self.scan(), (True, 0))
        self.assertEqual(len(self.backend.calls), calls)

    def test_missing_or_corrupt_mp3_uses_cached_chunks(self):
        self.scan()
        calls = len(self.backend.calls)
        self.mp3.unlink()
        self.scan()
        self.assertTrue(self.mp3.exists())
        self.mp3.write_bytes(b"corrupt")
        self.scan()
        self.assertTrue(self.mp3.read_bytes().startswith(b"ID3"))
        self.assertEqual(len(self.backend.calls), calls)

    def test_force_regenerates_chunks(self):
        self.scan()
        calls = len(self.backend.calls)
        self.scan(force=True)
        self.assertGreater(len(self.backend.calls), calls)

    def test_model_and_settings_changes_invalidate_cache(self):
        self.scan()
        old = self.record()["fingerprint"]
        other = Generator(self.site, backend=FakeBackend("test-2"), settings=Settings(chunk_chars=200))
        self.scan(other)
        self.assertNotEqual(old, self.record()["fingerprint"])
        self.assertTrue(other.backend.calls)

    def test_failure_keeps_previous_audio_and_does_not_retry_forever(self):
        self.scan()
        old_mp3 = self.mp3.read_bytes()
        old_manifest = self.generator.manifest_path.read_bytes()
        self.write_article("A new passage that must fail.")
        self.backend.fail = True
        self.assertFalse(self.scan()[0])
        self.assertEqual(self.mp3.read_bytes(), old_mp3)
        self.assertEqual(self.generator.manifest_path.read_bytes(), old_manifest)
        calls = len(self.backend.calls)
        self.assertFalse(self.scan()[0])
        self.assertEqual(len(self.backend.calls), calls)
        self.backend.fail = False
        self.write_article("An edited passage should retry.")
        self.assertTrue(self.scan()[0])

    def test_edit_during_generation_discards_stale_result(self):
        self.backend.callback = lambda: self.write_article("Changed during synthesis.")
        self.assertFalse(self.scan()[0])
        self.assertFalse(self.mp3.exists())
        self.assertFalse(self.generator.manifest_path.exists())
        self.backend.callback = None
        self.scan()
        self.assertTrue(self.mp3.exists())

    def test_cancellation_does_not_publish_partial_audio(self):
        stop = threading.Event()
        self.backend.callback = stop.set
        with self.assertRaises(Cancelled):
            self.scan(stop_event=stop)
        self.assertFalse(self.mp3.exists())
        self.assertFalse(self.generator.manifest_path.exists())

    def test_drafts_are_skipped_by_default(self):
        self.write_article(extra="draft: true\n")
        self.assertEqual(self.scan(), (True, 0))
        self.assertFalse(self.mp3.exists())
        generator = Generator(self.site, backend=self.backend, drafts=True)
        self.assertEqual(self.scan(generator), (True, 1))

    def test_nested_content_and_leaf_bundles(self):
        second = self.site / "content/paper-summary/example/index.md"
        second.parent.mkdir(parents=True)
        second.write_bytes(self.article.read_bytes())
        self.assertEqual(self.scan(), (True, 2))
        self.assertTrue((self.site / "static/audio/paper-summary/example/index.mp3").exists())

    def test_lock_excludes_other_generators(self):
        other = Generator(self.site, backend=FakeBackend())
        with self.generator.lock():
            with self.assertRaises(RuntimeError):
                with other.lock():
                    self.fail("second process acquired generation lock")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg required")
    def test_real_mp3_encoding(self):
        with self.generator.lock():
            self.assertEqual(self.generator.scan(), (True, 1))
        output = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(self.mp3)])
        stream = json.loads(output)["streams"][0]
        self.assertEqual(stream["codec_name"], "mp3")
        self.assertEqual(stream["channels"], 1)
        self.assertEqual(stream["sample_rate"], "44100")


class BackendSafetyTests(unittest.TestCase):
    def backend(self, frames=2, audio=None):
        backend = OnnxNarrator()
        backend.runtime = SimpleNamespace(
            manifest={"max_seq_len": 2048, "sample_rate": 44100},
            voices=SimpleNamespace(load=lambda voice: (np.zeros((10, 2)), {"reference_text": "Reference."})),
            prompt_builder=SimpleNamespace(build=lambda *args: np.zeros((1, 11, 100))),
            iter_codes=lambda **kwargs: iter([np.zeros(10, dtype=np.int64)] * frames),
            decode_codes=lambda codes: np.ones(100, dtype=np.float32) * 0.1 if audio is None else audio,
        )
        return backend

    def test_frame_limited_or_empty_output_is_rejected(self):
        for count in (0, 4):
            with self.subTest(frames=count), self.assertRaises(RuntimeError):
                self.backend(frames=count).synthesize("Text.", Settings(max_frames=4), threading.Event())

    def test_silent_and_nonfinite_output_is_rejected(self):
        for audio in (np.zeros(100), np.full(100, np.nan), np.array([])):
            with self.subTest(audio=audio), self.assertRaises(RuntimeError):
                self.backend(audio=audio).synthesize("Text.", Settings(max_frames=4), threading.Event())

    def test_valid_audio_is_returned(self):
        audio, rate = self.backend().synthesize("Text.", Settings(max_frames=4), threading.Event())
        self.assertEqual(rate, 44100)
        self.assertEqual(audio.size, 100)

    def test_cancelled_generation_is_rejected(self):
        stop = threading.Event()
        stop.set()
        with self.assertRaises(Cancelled):
            self.backend().synthesize("Text.", Settings(), stop)


@unittest.skipUnless(shutil.which("hugo"), "Hugo required")
class HugoPlayerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.site = Path(self.directory.name)
        self.article = self.site / "content/articles/Upper.Mixed.md"
        self.mp3 = self.site / "static/audio/articles/Upper.Mixed.mp3"
        self.index = self.site / "data/narration.json"
        for path in (self.article, self.mp3, self.index):
            path.parent.mkdir(parents=True, exist_ok=True)
        (self.site / "hugo.toml").write_text("baseURL = 'https://example.org/blog/'\n")
        layouts = self.site / "layouts"
        (layouts / "_default").mkdir(parents=True)
        (layouts / "partials").mkdir()
        (layouts / "_default/baseof.html").write_text('<!doctype html><html><body>{{ block "main" . }}{{ end }}</body></html>')
        (layouts / "_default/single.html").write_text('{{ define "main" }}{{ partial "article-audio.html" . }}{{ end }}')
        source = Path(__file__).resolve().parents[3] / "layouts/partials/article-audio.html"
        shutil.copyfile(source, layouts / "partials/article-audio.html")
        self.article.write_text('---\ntitle: Test\ndate: 2024-01-01\naudio: true\n---\nBody.\n')
        # This is a template-only fixture, not a playable test recording.
        self.mp3.write_bytes(b"ID3-template-fixture")
        record = {"src": "audio/articles/Upper.Mixed.mp3", "duration_label": "1 min 00 sec",
                  "source_sha256": hashlib.sha256(self.article.read_bytes()).hexdigest()}
        self.index.write_text(json.dumps({"version": 1, "articles": {"articles/Upper.Mixed.md": record}}))

    def build(self):
        result = subprocess.run([shutil.which("hugo"), "--source", str(self.site)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return (self.site / "public/articles/upper.mixed/index.html").read_text(), result.stdout + result.stderr

    def test_case_sensitive_source_paths_and_subdirectory_urls(self):
        html, logs = self.build()
        self.assertIn('src="/blog/audio/articles/Upper.Mixed.mp3"', html)
        self.assertIn('<audio controls preload="none"', html)
        self.assertIn('AI-generated narration', html)
        self.assertNotIn('deprecated', logs)

    def test_missing_mp3_hides_player_and_warns(self):
        self.mp3.unlink()
        html, logs = self.build()
        self.assertNotIn('<audio', html)
        self.assertIn('missing or outdated', logs)

    def test_missing_index_hides_player_and_warns(self):
        self.index.unlink()
        html, logs = self.build()
        self.assertNotIn('<audio', html)
        self.assertIn('missing or outdated', logs)

    def test_outdated_text_hides_old_player(self):
        self.article.write_text(self.article.read_text().replace('Body.', 'Changed.'))
        html, logs = self.build()
        self.assertNotIn('<audio', html)
        self.assertIn('missing or outdated', logs)

    def test_quoted_true_is_not_an_opt_in(self):
        self.article.write_text(self.article.read_text().replace('audio: true', 'audio: "true"'))
        html, logs = self.build()
        self.assertNotIn('<audio', html)
        self.assertNotIn('missing or outdated', logs)

    def test_opt_out_hides_player_without_warning(self):
        self.article.write_text(self.article.read_text().replace('audio: true', 'audio: false'))
        html, logs = self.build()
        self.assertNotIn('<audio', html)
        self.assertNotIn('missing or outdated', logs)


if __name__ == "__main__":
    unittest.main()
