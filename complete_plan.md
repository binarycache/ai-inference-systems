Yes. Now that you clarified your constraints, we can plan properly.

With **12 focused hours/week**, your goal is realistic, but it should be framed correctly:

## Your practical 12-month goal

> **Become an AI Inference Systems Engineer focused on LLM serving performance, with public proof through benchmarks, technical writing, and open-source contributions to vLLM, SGLang, or llama.cpp.**

This is realistic because you already have:

* Python: okay
* C++: okay
* Linux: okay
* ML basics: comfortable
* transformers: comfortable
* GPU/CUDA: basic clarity

That means we do **not** need to spend 3 months on generic ML. We can go directly into inference systems.

The strongest target is **vLLM first**, because it is directly about high-throughput, memory-efficient LLM serving. The current vLLM docs mention PagedAttention, continuous batching, chunked prefill, prefix caching, quantization, optimized attention kernels, speculative decoding, and disaggregated prefill/decode, which map almost perfectly to your goal. ([GitHub][1])

Your secondary projects should be:

* **SGLang**, for production-level low-latency and high-throughput serving across single GPU to distributed clusters. ([SGLang Documentation][2])
* **llama.cpp**, for local inference, C/C++, quantization, and device-side inference. ([GitHub][3])
* **TensorRT-LLM**, later, for NVIDIA-specific optimized inference and Python/C++ runtime understanding. ([GitHub][4])

---

# Honest feasibility

With **12 hours/week**, you can aim for:

## 3 months

You understand the core concepts and can run, benchmark, and explain LLM inference.

## 6 months

You have a benchmark repo, understand vLLM at a beginner-internal level, and have made at least one small open-source contribution attempt.

## 9 months

You have 2 to 3 meaningful contribution attempts, at least one stronger technical write-up, and can discuss inference tradeoffs seriously.

## 12 months

You are ready to apply for remote/global roles like:

* ML Systems Engineer
* AI Inference Engineer
* LLM Serving Engineer
* AI Infrastructure Engineer
* Model Serving Engineer
* Performance Engineer, AI

You will not be a CUDA kernel expert in 12 months unless you spend much more time. But you can become a credible **LLM inference systems candidate**, which is the wiser path.

---

# Your weekly structure

You were right that tiny daily splits are bad. This is the better structure:

| Day       |    Time | Focus                                   |
| --------- | ------: | --------------------------------------- |
| Sunday    | 2.5 hrs | Deep concept setup, roadmap, review     |
| Monday    | 1.5 hrs | Concept block                           |
| Tuesday   | 1.5 hrs | Concept plus math                       |
| Wednesday | 1.5 hrs | Code reading                            |
| Thursday  | 1.5 hrs | Paper/docs reading                      |
| Friday    |    1 hr | Review and notes                        |
| Saturday  | 2.5 hrs | Implementation, experiments, benchmarks |

Total: **12 hours/week**

This gives depth. You will not switch context every 15 minutes.

---

# Your first week: May 10 to May 16, 2026

## Week 1 theme

> **Build the mental model of LLM inference: prefill, decode, KV cache, memory bottlenecks, and where these appear in vLLM.**

No open-source contribution this week. No CUDA rabbit hole. No TensorRT-LLM yet. This week is foundation plus first real code contact.

---

## Sunday, May 10, 2026, 2.5 hours

### Goal

Set up your learning system and define the exact target.

### Block 1, 30 min: Create workspace

Create this folder structure:

```txt
ai-inference-systems/
  roadmap.md
  glossary.md
  weekly-reviews/
  notes/
  papers/
  code-reading/
  experiments/
  benchmarks/
  open-source/
```

In `roadmap.md`, write:

```md
# 12-month goal

Become an AI Inference Systems Engineer focused on LLM serving performance.

Primary project:
- vLLM

Secondary projects:
- SGLang
- llama.cpp

Later project:
- TensorRT-LLM

Core skills:
- LLM inference
- prefill and decode
- KV cache
- batching
- quantization
- GPU memory
- benchmarking
- serving systems
- open-source contribution
```

### Block 2, 45 min: Define the job target

Create `notes/target-role.md`.

Write:

```md
# Target role

Role names:
- AI Inference Engineer
- ML Systems Engineer
- LLM Serving Engineer
- AI Infrastructure Engineer
- Model Serving Engineer

I want proof in:
- benchmarks
- open-source PRs/issues
- technical writing
- code reading
- system design
```

Then write:

```md
# What I must be able to explain

1. Why decode is often memory-bound.
2. Why KV cache exists.
3. Why KV cache becomes expensive.
4. Why batching improves throughput.
5. Why latency and throughput conflict.
6. How vLLM improves serving.
7. How quantization affects memory and speed.
8. How to benchmark inference properly.
```

### Block 3, 45 min: Read project overviews

Read only the top-level docs or README for:

* vLLM
* SGLang
* llama.cpp

Do not dive into code yet.

Write `open-source/project-map.md`:

```md
# Project map

## vLLM
Best for:
- high-throughput serving
- KV cache
- PagedAttention
- batching
- production LLM serving

## SGLang
Best for:
- low-latency serving
- high-throughput serving
- multimodal serving
- distributed serving

## llama.cpp
Best for:
- local inference
- C/C++
- quantized inference
- device-side inference
```

### Block 4, 30 min: Start glossary

Create `glossary.md`.

Add:

```md
# Glossary

## Inference
Running a trained model to produce outputs.

## Training
Updating model weights using gradients.

## Token
A unit of text processed by the model.

## Prefill
The stage where the model processes the input prompt.

## Decode
The stage where the model generates output tokens one by one.

## KV cache
Stored key and value tensors from previous tokens.

## Latency
Time taken for one request.

## Throughput
Amount of work completed per unit time.

## TTFT
Time to first token.

## TPS
Tokens per second.
```

### Done when

You have:

* workspace
* roadmap
* target-role note
* project map
* glossary

---

## Monday, May 11, 2026, 1.5 hours

### Goal

Understand LLM inference flow deeply.

### Block 1, 45 min: Concept

Create `notes/01-llm-inference-flow.md`.

Write this in your own words:

```md
# LLM inference flow

1. User sends prompt.
2. Text is converted into tokens.
3. Tokens are passed through the model.
4. The model predicts probabilities for the next token.
5. One token is selected.
6. That token is appended to the sequence.
7. The loop repeats until stopping.
```

Then answer:

```md
## Questions

1. Why does inference not update weights?
2. Why does generation happen token by token?
3. Why is long output slower than short output?
4. What is the difference between prompt tokens and generated tokens?
```

### Block 2, 30 min: Draw the flow

In text:

```txt
prompt
  ↓
tokenizer
  ↓
input token IDs
  ↓
model forward pass
  ↓
logits
  ↓
sampling
  ↓
next token
  ↓
append token
  ↓
repeat
```

### Block 3, 15 min: Self-test

Close your notes and answer:

> “What happens when an LLM generates one token?”

If you cannot answer in 90 seconds, repeat the concept.

### Done when

You can explain inference without using vague words like “AI thinks.”

---

## Tuesday, May 12, 2026, 1.5 hours

### Goal

Understand prefill vs decode.

### Block 1, 45 min: Concept

Create `notes/02-prefill-vs-decode.md`.

Write:

```md
# Prefill

Prefill is the stage where the model processes the full prompt.

Example:
Prompt has 1,000 tokens.
The model processes those 1,000 tokens and prepares internal states.

# Decode

Decode is the stage where the model generates new tokens one by one.

Example:
Generate token 1001.
Then token 1002.
Then token 1003.
```

Now answer seriously:

```md
## Questions

1. Why can prefill use more parallelism?
2. Why is decode more sequential?
3. Why does time to first token depend heavily on prefill?
4. Why do output tokens per second depend heavily on decode?
5. Why might a serving system want to separate prefill and decode?
```

### Block 2, 30 min: Hardware intuition

Write:

```md
# Hardware intuition

Prefill:
- processes many input tokens
- can use large matrix operations
- often more compute-friendly

Decode:
- generates one token at a time
- repeatedly accesses model weights
- uses KV cache
- can become memory-bandwidth-limited
```

### Block 3, 15 min: Summary

Write a 10-line explanation:

> “Why prefill and decode are different workloads.”

### Done when

You can answer:

> “Why is reading a long prompt different from generating a long answer?”

---

## Wednesday, May 13, 2026, 1.5 hours

### Goal

Understand KV cache clearly.

### Block 1, 45 min: Concept

Create `notes/03-kv-cache.md`.

Write:

```md
# KV cache

In attention, tokens produce keys and values.

During generation, previous tokens do not change.

Instead of recomputing keys and values for all previous tokens at every step, we store them.

This stored memory is the KV cache.
```

Now answer:

```md
## Why KV cache matters

1. What computation does KV cache avoid?
2. Why does it help decoding?
3. Why does it consume memory?
4. Why does longer context increase KV cache?
5. Why does more batch/concurrency increase KV cache?
```

### Block 2, 30 min: KV cache formula intuition

Write this:

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

Then write:

```md
# Key intuition

If context length doubles, KV cache roughly doubles.
If active requests double, KV cache roughly doubles.
If precision goes from FP16 to FP8, KV cache memory can reduce.
```

### Block 3, 15 min: One-page explanation

Write:

```md
# KV cache in simple terms

KV cache is like keeping the previous attention memory around so the model does not redo old work. It speeds up generation, but it creates a new problem: memory usage grows with context length and number of active users.
```

### Done when

You can explain why KV cache is both a speed optimization and a memory bottleneck.

---

## Thursday, May 14, 2026, 1.5 hours

### Goal

Connect concepts to vLLM.

### Block 1, 45 min: vLLM docs/code map

Create:

```txt
code-reading/vllm-term-map.md
```

Search the vLLM docs/repo for:

```txt
KV cache
PagedAttention
prefill
decode
scheduler
batching
chunked prefill
prefix caching
quantization
```

For each term, write:

```md
## Term: KV cache

Where I found it:
-

What it seems related to:
-

What I understand:
-

What I do not understand:
-
```

vLLM is the right first target because its current project description explicitly emphasizes PagedAttention, continuous batching, chunked prefill, prefix caching, quantization, optimized kernels, speculative decoding, and disaggregated prefill/decode. ([GitHub][1])

### Block 2, 30 min: Contribution surface map

Create:

```txt
open-source/vllm-contribution-surfaces.md
```

Write:

```md
# Possible contribution surfaces

Beginner:
- docs
- examples
- installation notes
- benchmark reproduction
- issue reproduction

Intermediate:
- tests
- benchmark scripts
- small bug fixes
- model support debugging

Advanced:
- scheduler changes
- KV cache changes
- kernel-level optimization
- distributed serving
```

### Block 3, 15 min: Reflection

Write:

```md
What parts of vLLM seem closest to my goal?
What parts are too advanced right now?
```

### Done when

You have mapped vLLM terminology, not mastered it.

---

## Friday, May 15, 2026, 1 hour

### Goal

Read the PagedAttention paper at a high level.

### Block 1, 40 min: Paper reading

Read:

* abstract
* introduction
* problem statement
* skip details if they get too dense

Create:

```txt
papers/pagedattention-first-read.md
```

Answer:

```md
# PagedAttention first read

1. What problem is the paper solving?
2. Why is KV cache memory difficult?
3. Why does memory fragmentation matter?
4. What is the paging analogy?
5. What did I not understand?
```

### Block 2, 20 min: Convert to your own words

Write:

```md
# My understanding

PagedAttention is trying to make KV cache memory management more efficient, similar to how operating systems manage memory in pages. This helps serving systems fit more requests and improve throughput.
```

### Done when

You understand the problem, even if you do not yet fully understand the solution.

---

## Saturday, May 16, 2026, 2.5 hours

### Goal

First implementation block: run or prepare local inference.

### Option A: If setup works

Use llama.cpp or a Python-based local inference setup.

Run one small model.

Record:

```md
# First local inference experiment

model:
model size:
quantization:
hardware:
prompt:
prompt tokens:
output tokens:
time to first token:
tokens per second:
memory used:
notes:
```

### Option B: If setup fails

Do not pretend.

Document the failure:

```md
# Setup attempt

What I tried:
-

Error:
-

Likely reason:
-

Next action:
-
```

Then read llama.cpp’s build/run instructions and document the commands you need next.

llama.cpp is a good implementation target because it is a C/C++ LLM inference project and is active across local and device-oriented inference areas. ([GitHub][3])

### Block split

|   Time | Task                      |
| -----: | ------------------------- |
| 30 min | Install or clone          |
| 45 min | Build/run attempt         |
| 45 min | Run first prompt or debug |
| 20 min | Record measurements       |
| 10 min | Write next steps          |

### Done when

You either:

* run one model and record numbers, or
* have a clean failure log with next steps.

Both are real progress.

---

# Week 1 success criteria

By Saturday night, you should have:

```txt
roadmap.md
glossary.md
notes/01-llm-inference-flow.md
notes/02-prefill-vs-decode.md
notes/03-kv-cache.md
code-reading/vllm-term-map.md
open-source/vllm-contribution-surfaces.md
papers/pagedattention-first-read.md
experiments/first-local-inference.md
```

You should be able to explain:

1. What inference is.
2. What prefill is.
3. What decode is.
4. What KV cache is.
5. Why memory matters.
6. Why vLLM is relevant.

That is a real first week.

---

# The 12-month milestone plan

## Month 1: Inference fundamentals

### Goal

Understand LLM inference as a system.

### Topics

* inference vs training
* transformer forward pass
* prefill vs decode
* KV cache
* latency vs throughput
* TTFT
* tokens/sec
* GPU memory basics

### Code

* run local inference
* measure basic speed
* write first benchmark notes

### Milestone

By June 6, 2026:

> You can run a small model, explain prefill/decode/KV cache, and record basic inference metrics.

---

## Month 2: KV cache and benchmarking

### Goal

Understand why KV cache is central to serving.

### Topics

* KV cache memory formula
* context length
* batch size
* concurrency
* PagedAttention
* memory fragmentation
* benchmark methodology

### Code

* build a simple benchmark script
* compare prompt lengths
* compare output lengths
* compare quantization levels if possible

### Paper

* PagedAttention/vLLM paper more seriously
* FlashAttention abstract and introduction

### Milestone

By July 4, 2026:

> You have a benchmark repo with at least 3 controlled experiments.

---

## Month 3: vLLM and serving systems

### Goal

Understand model serving, not just local inference.

### Topics

* OpenAI-compatible API server
* request scheduling
* batching
* continuous batching
* prefix caching
* chunked prefill
* serving metrics

### Code

* run vLLM if hardware allows
* otherwise read benchmark code and use a small cloud GPU once
* send requests to a local server
* measure TTFT and tokens/sec

### Open-source

Start reading issues weekly.

### Milestone

By August 1, 2026:

> You can explain how served inference differs from running one local prompt.

---

## Month 4: Quantization and memory efficiency

### Goal

Understand compression and precision tradeoffs.

### Topics

* FP32, FP16, BF16
* FP8, INT8, INT4
* weight-only quantization
* activation quantization
* KV cache quantization
* GGUF
* AWQ/GPTQ basics

### Code

* compare quantized models
* compare memory usage
* compare speed
* write quality observations

### Milestone

By August 29, 2026:

> You can explain how quantization affects memory, speed, and quality.

---

## Month 5: First open-source contribution attempt

### Goal

Stop only learning. Start interacting with maintainers.

### Open-source work

Pick one:

* vLLM docs fix
* benchmark documentation improvement
* issue reproduction
* example improvement
* setup clarification
* small test
* useful issue comment with reproduction details

### Code reading

Read specific parts of vLLM related to:

* serving entrypoint
* scheduler
* KV cache
* benchmarking scripts

### Milestone

By September 26, 2026:

> You have opened at least one useful issue, PR, or reproduction comment.

Accepted PR is ideal. A high-quality issue reproduction is still progress.

---

## Month 6: Portfolio checkpoint

### Goal

Produce proof.

### Deliverables

1. `llm-inference-benchmarks` GitHub repo
2. One technical report
3. One open-source contribution attempt
4. vLLM architecture map
5. PagedAttention summary

### Report title

```md
Understanding LLM Inference Bottlenecks: KV Cache, Batching, and Quantization
```

### Milestone

By October 24, 2026:

> You have a credible public portfolio artifact.

This is the first point where you can start light networking.

---

## Months 7 to 9: Specialization

Choose one branch.

Given your goals, I recommend:

## Primary branch: Serving systems

Focus:

* vLLM
* SGLang
* scheduling
* batching
* prefix caching
* prefill/decode
* distributed serving
* benchmarking

SGLang is a strong secondary project because it is explicitly positioned for production-level low-latency and high-throughput inference from single GPU to large distributed clusters. ([SGLang Documentation][2])

### Secondary branch: GPU performance basics

Focus:

* CUDA concepts
* Triton basics
* memory hierarchy
* profiling
* kernels at a reading level

Do not make this your main branch yet.

### Milestone

By January 24, 2027:

> You have 2 to 3 contribution attempts and can read parts of vLLM/SGLang without getting lost.

---

## Months 10 to 12: Job-readiness phase

### Goal

Convert knowledge into applications.

### Deliverables

1. Resume tailored to AI infra roles.
2. GitHub portfolio.
3. 2 technical blog posts.
4. 3 to 5 contribution attempts.
5. One system design document.
6. Interview preparation notes.

### System design document

Write:

```md
Designing a Low-Latency LLM Inference System for Real-Time AI Agents
```

Include:

* model choice
* serving engine
* batching
* cache strategy
* latency target
* cost model
* GPU assumptions
* failure modes
* monitoring

### Milestone

By May 10, 2027:

> You are ready to apply to remote/global AI infra, ML systems, and inference roles with evidence.

---

# What I would not do yet

Do **not** start with:

* full CUDA mastery
* building your own inference engine from scratch
* reading 20 papers randomly
* contributing to TensorRT-LLM immediately
* distributed inference before single-machine serving
* obsessing over every new model release

Do start with:

* vLLM
* KV cache
* benchmarking
* serving systems
* small OSS contribution
* written explanations

---

# Your tracking system

Every Sunday, fill this:

```md
# Weekly Review

Week:
Hours completed:

## Concepts understood
-

## Code touched
-

## Experiments run
-

## Docs/papers read
-

## Open-source activity
-

## Confusions
-

## Next week priority
-

## Am I on track?
Yes/No

## If no, why?
-
```

Monthly scorecard:

| Metric                | Month 1 | Month 2 | Month 3 |
| --------------------- | ------: | ------: | ------: |
| Hours                 |      48 |      48 |      48 |
| Notes                 |      8+ |      6+ |      6+ |
| Experiments           |       2 |       4 |       4 |
| Papers/docs           |       2 |       3 |       3 |
| Issues read           |  0 to 5 |      10 |      20 |
| Contribution attempts |       0 |       0 |  0 to 1 |

---

# The most important adjustment

Your goal is not:

> Learn AI hardware.

Your goal is:

> Become useful in LLM inference systems.

That means every week must produce one of four things:

1. A concept you can explain.
2. Code you ran or read.
3. A benchmark result.
4. An open-source action.

If a week produces none of those, it was not useful.

With **12 hours/week**, this is a serious path. Not easy, not guaranteed, but realistic.

[1]: https://github.com/vllm-project/vllm?utm_source=chatgpt.com "GitHub - vllm-project/vllm: A high-throughput and memory-efficient ..."
[2]: https://docs.sglang.io/?utm_source=chatgpt.com "Welcome to SGLang - SGLang Documentation"
[3]: https://github.com/ggml-org/llama.cpp?utm_source=chatgpt.com "GitHub - ggml-org/llama.cpp: LLM inference in C/C++"
[4]: https://github.com/NVIDIA/TensorRT-LLM?utm_source=chatgpt.com "GitHub - NVIDIA/TensorRT-LLM: TensorRT LLM provides users with an easy ..."
