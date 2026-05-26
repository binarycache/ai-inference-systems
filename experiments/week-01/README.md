# Week 01 — LLM inference sandbox

Target hardware: **NVIDIA RTX 3050 Ti (4 GB VRAM)**. Use **CUDA 12.4** PyTorch wheels (driver reports CUDA 13.0 max; these wheels remain compatible).

## Model choice

**`google/gemma-3-270m`** (~268M params in BF16 weights per model card) is the smallest **Gemma 3** text checkpoint and fits easily in 4 GB for inference. It is **gated** on Hugging Face: accept the license on the model page, create an access token, then authenticate (see below). For a fully ungated tiny model if you prefer zero login, alternatives include community small LMs (e.g. SmolLM/TinyLlama-class); this week’s notebook defaults to Gemma 3 270M.

## Setup (uv)

Use a recent **uv** (0.5+) so PyTorch can resolve from the CUDA wheel index without breaking the rest of PyPI. If `uv sync` fails on dependency resolution, run `python -m pip install -U uv` once, then retry.

From this directory:

```powershell
cd d:\ai-inference-systems\experiments\week-01
uv sync --python 3.11
```

If you see a hardlink warning during install, it is safe to ignore on Windows, or set `UV_LINK_MODE=copy` for that session.

Activate the virtualenv (uv creates `.venv`):

```powershell
.\.venv\Scripts\Activate.ps1
```

Hugging Face token (required for Gemma):

```powershell
$env:HF_TOKEN = "hf_..."   # session only
# or: huggingface-cli login
```

Prefetch the model into the HF cache (after you can access the repo on the website):

```powershell
.\.venv\Scripts\python.exe scripts\download_gemma_cache.py
```

Start JupyterLab (uses this folder’s `.venv`):

```powershell
.\.venv\Scripts\jupyter.exe lab notebooks
```

In the notebook UI, pick the kernel **Python (week-01-llm)** (registered from this venv).

## Verify GPU

In a notebook or `python -c`:

```python
import torch
print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))
```

Expected: `True` and your RTX 3050 Ti name.
