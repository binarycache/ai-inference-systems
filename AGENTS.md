# Repository Guidelines

## Project Structure & Module Organization

This repository is a documentation and research workspace for AI inference systems. Keep top-level Markdown files focused:

- `roadmap.md`: the 12-month goal and high-level focus.
- `complete_plan.md`: the detailed learning plan.
- `glossary.md`: short definitions for inference-system terms.
- `notes/`: personal notes, role targets, and learning summaries.
- `papers/`: paper notes and reading logs.
- `code-reading/`: source walkthroughs for vLLM, SGLang, and llama.cpp.
- `experiments/`: runnable prototypes or small investigations.
- `benchmarks/`: benchmark scripts, raw results, and analysis.
- `open-source/`: contribution tracking, issue notes, and project maps.
- `weekly-reviews/`: weekly progress reviews and next actions.

## Build, Test, and Development Commands

There is no global build system yet. Use lightweight commands while the repo is Markdown-first:

- `rg --files`: list tracked workspace files quickly.
- `rg "KV cache|PagedAttention|batching"`: search notes for a concept.
- `sed -n '1,120p' complete_plan.md`: inspect the main plan without opening an editor.

If runnable code is added under `experiments/` or `benchmarks/`, include setup and run commands.

## Coding Style & Naming Conventions

Write Markdown with clear headings, short paragraphs, and fenced code blocks. Prefer lowercase, hyphenated filenames such as `week-01-review.md` or `vllm-kv-cache-notes.md`.

For Python experiments, use 4-space indentation, descriptive snake_case names, and small scripts. Store generated outputs separately.

## Testing Guidelines

No test framework is configured at the root. For future Python code, use `pytest` and place tests next to the relevant experiment or in a local `tests/` folder. Benchmark work should record the command, model, hardware, date, and key environment details.

## Commit & Pull Request Guidelines

This path is not currently initialized as a Git repository, so no existing commit convention is available. When Git is added, use concise imperative commits, for example `Add week 01 review`.

Pull requests should summarize the changed artifact, link related issues or papers, and include reproduction commands for benchmark or experiment changes.

## Agent-Specific Instructions

Be direct and honest, especially on career, learning-priority, and technical tradeoff questions. Do not flatter weak ideas. State the strongest recommendation, the reasoning behind it, and what should be avoided.

## Security & Configuration Tips

Do not commit API keys, tokens, model credentials, or private benchmark data. Keep machine-specific configuration outside the repository, and redact secrets from copied logs before saving them in notes or reviews.
