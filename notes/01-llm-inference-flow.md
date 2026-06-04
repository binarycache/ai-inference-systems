# LLM Inference Flow

`GenerationMixin` is the generic generation engine in Hugging Face Transformers. Any model class that inherits it gets `.generate()`, so you can call:

```python
model.generate(...)
```

It does **not** define the neural network itself. The actual model class still defines `forward()`. `GenerationMixin` only manages the autoregressive inference process around that `forward()` call.

At a high level, `generate()` does this:

```text
1. Read generation config
2. Prepare input_ids / attention_mask / position_ids
3. Prepare cache
4. Choose decoding mode
5. Run generation loop
6. Repeatedly call model.forward(...)
7. Pick next token from logits
8. Stop on EOS, max length, stop strings, etc.
```

It supports greedy decoding, sampling, beam search, beam sampling, and assisted decoding. For greedy and sampling, it uses the internal `_sample()` loop; `do_sample=False` means argmax, while `do_sample=True` means sample from probabilities.

The class also prepares logits processors such as temperature, top-k, top-p, repetition penalty, bad-word filtering, forced EOS, and stopping criteria.

Models customize generation by overriding hook methods like:

```text
prepare_inputs_for_generation
_prepare_position_ids_for_generation
_expand_inputs_for_generation
_update_model_kwargs_for_generation
```

For VLMs, these hooks handle image/video tensors, multimodal position IDs, and avoiding reprocessing images after the first cached step.


## Facts

**`GenerationMixin.generate()` normally creates the default cache.** Hugging Face docs say `DynamicCache` is the default cache class for generation. ([GitHub][1])

In `GenerationMixin._prepare_cache_for_generation`, if the user did **not** pass `past_key_values`, `use_cache=True`, and the model supports default dynamic cache, it writes:

```text
model_kwargs["past_key_values"] = DynamicCache(...)
```

Then `prepare_inputs_for_generation()` passes that into `model.forward(...)`. After forward, `GenerationMixin` reads `outputs.past_key_values` and stores it back for the next token. The cache is therefore created by `GenerationMixin`, then updated by the model. ([GitHub][2])

[1]: https://github.com/huggingface/transformers/blob/main/docs/source/en/kv_cache.md?utm_source=chatgpt.com "transformers/docs/source/en/kv_cache.md at main · huggingface ... - GitHub"
[2]: https://github.com/huggingface/transformers/blob/main/src/transformers/generation/utils.py?utm_source=chatgpt.com "transformers/src/transformers/generation/utils.py at main · huggingface ..."

