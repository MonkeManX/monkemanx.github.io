"""Generate listening samples and benchmark Audio8 Preview 0.1B ONNX on CPU.

Inside tools/tts/nix-shell: .venv-onnx/bin/python test_onnx.py
Runs offline after setup_onnx.sh. No article or website files are changed.
"""

import argparse
import json
from pathlib import Path
import resource
import sys
import time

import numpy as np
import onnxruntime as ort
import soundfile as sf

ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT / ".cache/audio8-source/onnx_runtime_0_1b_int8"
SAMPLES = {
    "german": "Guten Tag. Dies ist ein Test der Sprachsynthese auf einer AMD-Grafikkarte unter NixOS. Die Qualität dieses Modells ist bemerkenswert gut.",
    "english": "Hello. This is a test of speech synthesis running on an AMD graphics card. If you can hear this clearly, the pipeline works.",
}


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="Speak this plain text instead of the built-in samples")
    source.add_argument("--text-file", type=Path, help="Read plain UTF-8 text from a file")
    source.add_argument("--sample", choices=["german", "english", "both"], default="both")
    parser.add_argument("--threads", type=positive_int, default=8)
    parser.add_argument("--max-new-tokens", type=positive_int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/onnx")
    args = parser.parse_args()
    if not (RUNTIME_DIR / "arktts_runtime/runtime.py").is_file():
        parser.error("runtime missing; run: nix-shell --run 'bash setup_onnx.sh'")
    if args.text is not None or args.text_file is not None:
        text = args.text if args.text is not None else args.text_file.read_text(encoding="utf-8")
        samples = {"custom": text}
    else:
        samples = SAMPLES if args.sample == "both" else {args.sample: SAMPLES[args.sample]}
    if any(not text.strip() for text in samples.values()):
        parser.error("text must not be empty")

    sys.path.insert(0, str(RUNTIME_DIR))
    from arktts_runtime import ArkTtsRuntime

    print(f"ONNX Runtime {ort.__version__}; CPU only; {args.threads} threads", flush=True)
    start = time.perf_counter()
    runtime = ArkTtsRuntime(ROOT / ".cache/onnx-model", ROOT / ".cache/onnx-voices",
                           threads=args.threads)
    load_seconds = time.perf_counter() - start
    providers = {name: getattr(runtime, name).get_providers() for name in ("slow", "fast", "decoder")}
    print(f"Sessions loaded in {load_seconds:.2f}s: {providers}", flush=True)
    rate = int(runtime.manifest["sample_rate"])
    reference_codes, reference_meta = runtime.voices.load("default")
    report = {"model": runtime.manifest["model_id"],
              "model_fingerprint": runtime.manifest["model_fingerprint"],
              "onnxruntime": ort.__version__, "threads": args.threads, "seed": args.seed,
              "voice": "bundled default (Chinese reference)", "providers": providers,
              "load_seconds": load_seconds, "samples": []}
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for name, text in samples.items():
        prompt = runtime.prompt_builder.build(text, reference_meta["reference_text"], reference_codes)
        prompt_positions = int(prompt.shape[-1])
        available = int(runtime.manifest["max_seq_len"]) - prompt_positions
        if available < 1:
            parser.error("text exceeds model context; split it into shorter passages")
        cap = min(args.max_new_tokens, available)
        print(f"Generating {name}: {prompt_positions} prompt positions; cap {cap} frames", flush=True)
        start = time.perf_counter()
        frames = list(runtime.iter_codes(text=text, voice="default", max_new_tokens=cap,
                                         temperature=0.7, top_p=0.9, top_k=50, seed=args.seed))
        generation_seconds = time.perf_counter() - start
        if not frames:
            raise RuntimeError("model generated no audio frames")
        codes = np.stack(frames, axis=1)
        start = time.perf_counter()
        audio = runtime.decode_codes(codes)
        decode_seconds = time.perf_counter() - start
        if not audio.size or not np.isfinite(audio).all():
            raise RuntimeError("decoder produced empty or non-finite audio")
        duration = audio.size / rate
        elapsed = generation_seconds + decode_seconds
        wav_path = args.output_dir / f"{name}.wav"
        sf.write(wav_path, audio, rate, subtype="PCM_16")
        hit_cap = len(frames) >= cap
        result = {"file": wav_path.name, "text": text, "sample_rate": rate,
                  "prompt_positions": prompt_positions, "frames": len(frames),
                  "generation_seconds": generation_seconds, "decode_seconds": decode_seconds,
                  "duration_seconds": duration, "total_seconds": elapsed,
                  "realtime_factor": elapsed / duration, "speedup": duration / elapsed,
                  "hit_frame_cap": hit_cap, "peak_amplitude": float(np.max(np.abs(audio)))}
        report["samples"].append(result)
        print(f"{wav_path}: {duration:.2f}s audio in {elapsed:.2f}s "
              f"({duration / elapsed:.2f}x realtime; generation {generation_seconds:.2f}s, "
              f"decode {decode_seconds:.2f}s)", flush=True)
        if hit_cap:
            print("WARNING: frame limit reached; speech may be cut off.", file=sys.stderr)
        report["peak_rss_mib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        (args.output_dir / "benchmark.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Peak process memory: {report['peak_rss_mib']:.0f} MiB", flush=True)


if __name__ == "__main__":
    main()
