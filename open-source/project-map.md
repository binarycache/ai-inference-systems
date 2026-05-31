My focus is LLM serving performance through:
  - KV cache memory management
  - batching and scheduling
  - prefill/decode tradeoffs
  - latency and throughput benchmarking

  Primary project:
  - vLLM

  Comparison project:
  - SGLang

  Later systems perspective:
  - llama.cpp

  This is the right wedge. It is narrow enough to execute, but broad enough to matter.

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
- diffusion models 

## llama.cpp
Best for:
- local inference
- C/C++
- quantized inference
- device-side inference