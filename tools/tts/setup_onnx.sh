#!/usr/bin/env bash
# Run from the Nix shell: bash setup_onnx.sh
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

source_url=https://github.com/Edge0-AI/Audio8_TTS.git
source_revision=2ab4d9d5d4285644a3cc7b50f6eb29b7dbc8e181
source_dir=.cache/audio8-source
model_id=Edge0/audio8-TTS-0.1B-ONNX-INT8
model_revision=317c12d4e0da83847b594fcf8bd74bf2c76615ec

if [[ ! -x .venv-onnx/bin/python ]]; then
  UV_PYTHON_DOWNLOADS=never uv venv --python python3.12 .venv-onnx
fi
uv pip sync --python .venv-onnx/bin/python requirements-onnx.txt

mkdir -p .cache
if [[ ! -d "$source_dir/.git" ]]; then
  git init "$source_dir"
fi
if ! git -C "$source_dir" cat-file -e "$source_revision^{commit}" 2>/dev/null; then
  git -C "$source_dir" fetch --depth 1 "$source_url" "$source_revision"
fi
git -C "$source_dir" sparse-checkout set onnx_runtime_0_1b_int8
git -C "$source_dir" checkout --detach "$source_revision"

# The reference encoder is not needed for the bundled voice. Download only
# the three inference graphs, their weights, tokenizer, and reference codes.
.venv-onnx/bin/hf download "$model_id" --revision "$model_revision" \
  --local-dir .cache/onnx-model \
  slow_ar_int8.onnx slow_ar_int8.onnx.data \
    fast_ar_int8.onnx fast_ar_int8.onnx.data \
    codec_decoder_fp16.onnx codec_decoder_fp16.onnx.data \
    runtime_manifest.json reference_codes.npy tokenizer/tokenizer.json

if [[ ! -f .cache/onnx-voices/default/meta.json ]]; then
  .venv-onnx/bin/python \
    "$source_dir/onnx_runtime_0_1b_int8/scripts/register_default_voice.py" \
    --model-dir .cache/onnx-model --voices-dir .cache/onnx-voices
fi
printf '\nReady. Run: .venv-onnx/bin/python test_onnx.py\n'
