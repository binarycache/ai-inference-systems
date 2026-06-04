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


For **LLM inference**, Transformers first uses `modeling_auto.py` and `tokenization_auto.py` to map `AutoModelForCausalLM` / `AutoTokenizer` to the correct architecture. Config is loaded through `configuration_utils.py` plus the model’s own `configuration_<model>.py`. Weights and model initialization are handled in `modeling_utils.py`. During generation, `generation/utils.py` runs `GenerationMixin.generate()`, chooses `_sample` or `_beam_search`, prepares cache from `cache_utils.py`, applies rules from `logits_process.py`, checks stops from `stopping_criteria.py`, and optionally streams tokens through `streamers.py`. The actual neural forward pass happens in `models/<model>/modeling_<model>.py`.

For **VLM inference**, the same text-generation loop is still used: `generation/utils.py`. The difference is preprocessing and model inputs. `processing_auto.py` selects the correct `AutoProcessor`; `processing_utils.py` defines processor behavior. Images are loaded/transformed using `image_utils.py`, `image_processing_utils.py`, and `image_transforms.py`; videos use `video_utils.py` and `video_processing_utils.py`. Model-specific multimodal logic lives in `models/<vlm>/processing_<vlm>.py`, `image_processing_<vlm>.py`, and especially `modeling_<vlm>.py`, where image/video features are fused with text before logits are returned.
