# LLM Inference Flow


## Generation Loop
- A user sends a prompt to the model.
- The tokenizer converts the text into token IDs that the model can process.
- The token IDs are passed through the model in a forward pass.
- The model produces logits, which represent scores for all possible next tokens.
- A token selection method (such as greedy decoding or sampling) chooses the next token.
- The selected token is appended to the existing sequence.
- The model repeats the process until a stopping condition is reached, such as generating an end-of-sequence token or reaching a maximum token limit.

## Questions

1. Why does inference not update weights?

Inference uses a trained model to generate outputs. It only performs forward passes through the network. Unlike training, inference does not compute gradients, perform backpropagation, or update model weights. The model parameters remain fixed.

2. Why does generation happen token by token?

Each generated token depends on all previous tokens in the sequence. The model must first determine token n before it can compute token n+1. Because of this dependency, output generation is sequential.

3. Why is long output slower than short output?

Generating more output tokens requires more decoding steps. Each new token requires another forward pass through the model. Therefore, a request that generates 500 tokens requires many more decoding iterations than a request that generates 50 tokens.

4. What is the difference between prompt tokens and generated tokens?

Prompt tokens are the tokens provided by the user as input. They are processed during the prefill phase. Generated tokens are created by the model during the decode phase and are produced one at a time after the prompt has been processed.


## Flow 

```bash
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
