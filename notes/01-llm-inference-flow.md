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


model.generate calls _sample() from GenerationMixin class which has two stages one prefill and Decode , prefill stage differs for LLM and VLM mainly due to preprocessing and Decode stage is identical including KV cache . 


By default Dynamic Cache is used in Hugging face transformers which does torch.cat operation on previous KV cache and new token KV which in turn allocates new memory and copies contents there this causes peak memory to be much higher . Same problem arises in Beam search . 

General **Vision-Language Model inference flow** looks like this:

1. **User provides image + text prompt**, for example: “Describe this image.”

2. The **processor/chat template** converts the conversation into model inputs.

3. The text part becomes `input_ids`, containing normal text tokens and special image placeholder tokens.

4. The image itself does **not** become `input_ids`.

5. The actual image is resized, normalized, and stored separately as `pixel_values`.

6. Extra metadata like `image_grid_thw` tells the model how many visual patches/tokens the image corresponds to.

7. `mm_token_type_ids` or similar masks mark which positions in `input_ids` are image placeholders and which are text tokens.

8. During the model forward pass, text token IDs are converted into normal text embeddings.

9. Separately, `pixel_values` are passed through the vision encoder.

10. The vision encoder converts the image into visual patch features.

11. These visual features are passed through a projector/adapter to match the LLM hidden size.

12. The projected visual embeddings are inserted into the positions of the image placeholder tokens.

13. Now the model has one combined embedding sequence: text embeddings + image embeddings + text embeddings.

14. The transformer runs prefill on this full sequence and builds a KV cache containing both text and image context.

15. Then decoding happens like a normal LLM: the model generates output tokens one by one while attending to the cached text and image information.

## General LLM Inference Flow:

1. User provides a text prompt.

2. The tokenizer converts the prompt into `input_ids`.

3. Special tokens, such as system/user/assistant tokens, may be added by the chat template.

4. An `attention_mask` is created to mark valid tokens and ignore padding.

5. The model converts each token ID into a text embedding.

6. Positional information is applied so the model understands token order.

7. The full prompt is passed through transformer layers in the **prefill stage**.

8. During prefill, the model creates a **KV cache** for all prompt tokens.

9. The model predicts logits for the next token, and a decoding strategy selects one token.

10. The selected token is appended, and the model keeps generating one token at a time using the KV cache until it stops.
