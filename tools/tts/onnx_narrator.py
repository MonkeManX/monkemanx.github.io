"""Lazy, offline adapter for the pinned Audio8 0.1B ONNX runtime."""

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import onnxruntime as ort

ROOT = Path(__file__).resolve().parent


class Cancelled(Exception):
    pass


class OnnxNarrator:
    def __init__(self):
        self.runtime_dir = ROOT / ".cache/audio8-source/onnx_runtime_0_1b_int8"
        self.model_dir = ROOT / ".cache/onnx-model"
        self.voices_dir = ROOT / ".cache/onnx-voices"
        self.runtime = None

    def identity(self, voice):
        paths = [self.model_dir / "runtime_manifest.json",
                 self.voices_dir / voice / "codes.npy"]
        paths += [self.runtime_dir / "arktts_runtime" / name
                  for name in ("runtime.py", "prompt.py", "voices.py")]
        digest = hashlib.sha256()
        try:
            for path in paths:
                digest.update(path.read_bytes())
            meta = json.loads((self.voices_dir / voice / "meta.json").read_text())
        except FileNotFoundError as exc:
            raise RuntimeError("TTS setup is missing. Run: cd tools/tts && nix-shell --run 'bash setup_onnx.sh'") from exc
        digest.update(meta["reference_text"].encode())
        return {"engine": "Audio8-Preview-0.1B-ONNX-INT8",
                # Weight revision pinned by setup_onnx.sh.
                "weights_revision": "317c12d4e0da83847b594fcf8bd74bf2c76615ec",
                "runtime_and_voice_sha256": digest.hexdigest(), "onnxruntime": ort.__version__}

    def synthesize(self, text, settings, stop_event):
        if stop_event.is_set():
            raise Cancelled()
        if self.runtime is None:
            sys.path.insert(0, str(self.runtime_dir))
            from arktts_runtime import ArkTtsRuntime
            print("[audio] Loading Audio8 ONNX sessions (CPU).", flush=True)
            self.runtime = ArkTtsRuntime(self.model_dir, self.voices_dir, threads=settings.threads)
        runtime = self.runtime
        codes, meta = runtime.voices.load(settings.voice)
        prompt = runtime.prompt_builder.build(text, meta["reference_text"], codes)
        cap = min(settings.max_frames, int(runtime.manifest["max_seq_len"]) - prompt.shape[-1])
        if cap < 1:
            raise ValueError("chunk exceeds the model context; use a smaller --chunk-chars value")
        frames = list(runtime.iter_codes(text=text, voice=settings.voice, max_new_tokens=cap,
                                        temperature=0.7, top_p=0.9, top_k=50,
                                        seed=settings.seed, stop_event=stop_event))
        if stop_event.is_set():
            raise Cancelled()
        if not frames or len(frames) >= cap:
            raise RuntimeError("chunk was empty or hit the frame limit; no audio published. Try a smaller --chunk-chars value.")
        audio = runtime.decode_codes(np.stack(frames, axis=1))
        if stop_event.is_set():
            raise Cancelled()
        if not audio.size or not np.isfinite(audio).all() or np.max(np.abs(audio)) == 0:
            raise RuntimeError("decoder returned invalid or silent audio")
        return audio, int(runtime.manifest["sample_rate"])
