"""Local Hugo entry point; generation never runs in the Pages workflow."""

import os
import signal
import subprocess
import sys
import threading

try:
    from generate_audio import Cancelled, Generator
except ImportError as exc:
    raise SystemExit(f"TTS dependencies are missing ({exc}). Run: cd tools/tts && nix-shell --run 'bash setup_onnx.sh'")


def flag(args, short, long):
    result = False
    for argument in args:
        if argument in (short, long):
            result = True
        elif argument.startswith(long + "="):
            result = argument.split("=", 1)[1].lower() not in ("false", "0")
    return result


def main():
    args = sys.argv[1:]
    binary = os.environ["HUGO_BINARY"]
    command = args[0] if args else ""
    passthrough = {"version", "help", "config", "new", "list", "mod", "env", "gen", "import",
                   "deploy", "completion", "convert"}
    if command in passthrough or any(arg in {"--help", "-h", "--version"} for arg in args):
        return subprocess.call([binary, *args])
    for arg in args:
        if arg in {"--source", "-s", "--contentDir"} or arg.startswith(("--source=", "--contentDir=")):
            raise SystemExit("The local narration wrapper uses this repository's content/ directory; --source/--contentDir are not supported.")
    stop = threading.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())
    generator = Generator(drafts=flag(args, "-D", "--buildDrafts"),
                          future=flag(args, "-F", "--buildFuture"),
                          expired=flag(args, "-E", "--buildExpired"))
    if command not in {"server", "serve"}:
        try:
            with generator.lock():
                success, _ = generator.scan(stop)
            return subprocess.call([binary, *args]) if success and not stop.is_set() else 1
        except Cancelled:
            return 130
    worker = threading.Thread(target=generator.watch, args=(stop,), name="article-narration", daemon=True)
    worker.start()
    process = None
    try:
        process = subprocess.Popen([binary, *args], start_new_session=True)
        while process.poll() is None and not stop.wait(0.2):
            pass
        return process.returncode if process.returncode is not None else 0
    finally:
        stop.set()
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
        worker.join(timeout=15)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        raise SystemExit(f"[audio] ERROR: {exc}")
