# Week 01 Schedule: May 10-16, 2026

This week starts on Sunday, May 10, 2026. The repo was created on May 10, so that day counts as the setup day. Monday, May 11, 2026 is the first concept block.

## Theme

Build the first serious mental model of LLM inference serving:

- prefill
- decode
- KV cache
- batching and scheduling
- why vLLM is the right first open-source target

Do not start CUDA, TensorRT-LLM, distributed inference, or random paper reading this week.

## Weekly Success Criteria

By Saturday night, produce these artifacts:

- `notes/01-llm-inference-flow.md`
- `notes/02-prefill-vs-decode.md`
- `notes/03-kv-cache.md`
- `code-reading/vllm-term-map.md`
- `open-source/vllm-contribution-surfaces.md`
- `papers/pagedattention-first-read.md`
- `experiments/first-local-inference.md`
- `weekly-reviews/week-01-review.md`

You should be able to explain, without hand-waving:

1. What happens when an LLM generates one token.
2. Why prefill and decode are different workloads.
3. Why KV cache speeds up decoding.
4. Why KV cache becomes a memory bottleneck.
5. Why vLLM focuses on memory management, batching, and scheduling.

## Sunday, May 10, 2026: Setup Completed

Time: already completed

Created or confirmed:

- `roadmap.md`
- `complete_plan.md`
- `glossary.md`
- `notes/target-role.md`
- `open-source/project-map.md`

This counts as the workspace setup block from the original plan.

## Monday, May 11, 2026: Inference Flow

Time: 1.5 hours

This is the exact May 11 reading and writing block.

### Read In This Order

1. `complete_plan.md`, the section titled `Monday, May 11, 2026`.

Read only that Monday section. Its job is to make the inference loop concrete.

2. `glossary.md`

Read only these terms:

- inference
- training
- token
- prefill
- decode
- KV cache
- latency
- throughput
- TTFT
- TPS

Do not try to master all terms yet. Just make sure the words are not vague.

3. `notes/target-role.md`

Read only `What I must be able to explain`. This is the reason the week starts with inference flow instead of jumping straight into vLLM internals.

### Write

Create `notes/01-llm-inference-flow.md`.

Write the generation loop in your own words:

```txt
prompt
tokenizer
input token IDs
model forward pass
logits
sampling or token selection
next token
append token
repeat
```

Answer:

1. Why does inference not update weights?
2. Why does generation happen token by token?
3. Why is long output slower than short output?
4. What is the difference between prompt tokens and generated tokens?

Done when: you can answer "what happens when an LLM generates one token?" in 90 seconds.

## Tuesday, May 12, 2026: Prefill vs Decode

Time: 1.5 hours

### Read In This Order

1. `complete_plan.md`, the section titled `Tuesday, May 12, 2026`.

Read only that Tuesday section. It defines the shape of the work: prefill, decode, hardware intuition, and a 10-line summary.

2. Hugging Face Transformers: `Optimizing inference`

URL: https://huggingface.co/docs/transformers/main/llm_optims

Read only:

- the opening explanation of why LLM inference is hard
- `Static kv-cache and torch.compile`
- stop before `Decoding strategies`

What to extract:

- why inference repeatedly generates the next token
- why KV cache exists
- why a dynamic cache grows during generation

3. Hugging Face Transformers: `Cache strategies`

URL: https://huggingface.co/docs/transformers/main/kv_cache

Read only:

- intro through `Default cache`
- `Prefill a cache (prefix caching)`

What to extract:

- what keys and values are cached for
- what "prefilling a cache" means
- why reuse only helps when a prefix is shared

4. vLLM: `Automatic Prefix Caching`

URL: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/

Read only:

- `Introduction`
- `Example workloads`
- `Limits`

What to extract:

- APC reuses KV cache when queries share a prefix
- APC helps the prefilling phase
- APC does not speed up the decoding phase when most time is spent generating a long answer

### Do Not Read On Tuesday

- Do not read the PagedAttention paper yet.
- Do not read vLLM scheduler source yet.
- Do not read CUDA kernels yet.
- Do not compare vLLM and SGLang yet.

Those are real topics, but they are distractions before you can cleanly explain prefill and decode.

### Write

Create `notes/02-prefill-vs-decode.md`.

Use this structure:

```md
# Prefill vs Decode

## Prefill

Prefill is:

Example with a 1,000-token prompt:

Why prefill can use more parallelism:

Why TTFT depends heavily on prefill:

## Decode

Decode is:

Example generating tokens 1001, 1002, and 1003:

Why decode is sequential:

Why output tokens per second depend heavily on decode:

## Hardware Intuition

Prefill:
-

Decode:
-

## Why Serving Systems Care

Why might a system separate or schedule prefill and decode differently?

## 10-Line Summary

Why prefill and decode are different workloads:

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
```

Done when: you can answer "why is reading a long prompt different from generating a long answer?"

## Wednesday, May 13, 2026: KV Cache

Time: 1.5 hours

Create `notes/03-kv-cache.md`.

Focus:

- what computation KV cache avoids
- why it helps decode
- why memory grows with context length
- why memory grows with active requests
- why batching and KV cache are tied together

Write the formula intuition:

```txt
KV cache memory roughly grows with:

number of layers
x sequence length
x batch size
x number of KV heads
x head dimension
x bytes per value
x 2 because key and value are both stored
```

Done when: you can explain why KV cache is both a speed optimization and a memory bottleneck.

## Thursday, May 14, 2026: vLLM Term Map

Time: 1.5 hours

Create `code-reading/vllm-term-map.md`.

Search the vLLM docs and repo for:

- KV cache
- PagedAttention
- prefill
- decode
- scheduler
- batching
- chunked prefill
- prefix caching
- quantization

For each term, write:

```md
## Term

Where I found it:
-

What it seems related to:
-

What I understand:
-

What I do not understand:
-
```

Also create `open-source/vllm-contribution-surfaces.md` with beginner, intermediate, and advanced contribution surfaces.

Done when: you have mapped vLLM terminology, not mastered it.

## Friday, May 15, 2026: PagedAttention First Read

Time: 1 hour

Create `papers/pagedattention-first-read.md`.

Read only:

- abstract
- introduction
- problem statement

Answer:

1. What problem is the paper solving?
2. Why is KV cache memory difficult?
3. Why does memory fragmentation matter?
4. What is the paging analogy?
5. What did I not understand?

Done when: you understand the problem, even if the solution is still fuzzy.

## Saturday, May 16, 2026: First Local Inference Attempt And Review

Time: 2.5 hours

Spend the first 2 hours on the local inference attempt.

Create `experiments/first-local-inference.md`.

Option A: if setup works, run one small local model and record:

```md
# First Local Inference Experiment

date:
hardware:
model:
model size:
quantization:
runtime:
prompt:
prompt tokens:
output tokens:
time to first token:
tokens per second:
memory used:
notes:
```

Option B: if setup fails, record the failure cleanly:

```md
# Setup Attempt

date:
what I tried:
error:
likely reason:
next action:
```

Then spend the final 30 minutes on the weekly review.

Create `weekly-reviews/week-01-review.md`.

Use this template:

```md
# Week 01 Review

Week: May 10-16, 2026
Hours completed:

## Concepts Understood
-

## Code Touched Or Read
-

## Experiments Run
-

## Docs Or Papers Read
-

## Open-Source Activity
-

## Confusions
-

## Strongest Next Week Priority
-

## Am I On Track?
Yes/No

## If No, Why?
-
```

Done when: you either have one real measurement or a clean failure log with next actions, plus a short Week 01 review.

Week 02 should stay on KV cache and PagedAttention, not jump to CUDA or distributed serving.
