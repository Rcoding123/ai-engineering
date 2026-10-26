"""
Project 09 · Step 3 — LoRA fine-tuning

Objective:
Fine-tune the small model on your training set with a parameter-efficient
method (LoRA or QLoRA).

Requirements:
  - Train on the train split, watch the validation loss, and stop before it
    overfits.
  - Log training and validation loss per step and plot them.
  - Write down the hardware you used and how long training took (a free cloud
    GPU notebook is fine if your machine has no suitable GPU).
  - Save the trained adapter.

Done when:
  - The loss plot is saved and the adapter loads for inference.

Questions (answer as comments at the bottom of this file):
  1. Where in the plot would you say overfitting starts?
  2. Which hyperparameter change made the biggest difference?
"""
