# 09 — Fine-Tuning Small Models

**Build:** A fine-tuned small open-weight model that does one narrow task (e.g. your Project 02 extraction, or a classifier) about as well as a large API model, at a fraction of the cost.

## Skills you will learn
- When to fine-tune vs prompt vs use RAG
- Building a training dataset, including synthetic data generated with a larger model
- Parameter-efficient fine-tuning (LoRA / QLoRA)
- Train/validation/test splits, overfitting, hyperparameters
- Running models locally (e.g. Ollama, llama.cpp, vLLM) and quantization

## Requirements
1. Create a dataset of at least 500 examples with a held-out test set.
2. Establish baselines: the base small model (zero/few-shot) and a large API model.
3. Fine-tune with LoRA and track training and validation loss.
4. Evaluate all three on the same test set using your Project 03 harness.
5. Compare quality, latency and cost per 1,000 requests.

## Done when
- You can make a data-backed recommendation on whether to use the fine-tuned small model or the API model for this task, and explain why.

## Stretch
- Quantize the fine-tuned model and measure the quality drop.
- Distillation: train the small model on the large model's outputs.
