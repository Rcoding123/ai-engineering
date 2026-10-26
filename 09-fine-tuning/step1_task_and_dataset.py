"""
Project 09 · Step 1 — Task and dataset

Objective:
Pick one narrow task (your Project 02 extraction or a classifier) and build a
training dataset for it.

Requirements:
  - At least 500 examples of input -> correct output.
  - You may generate examples with a large model, but you must filter them for
    quality and check a random sample of 30 by hand.
  - Split into train / validation / test. The test set is never used for training
    or tuning, and has no near-duplicates of training examples.
  - Save the splits in the format your fine-tuning tool expects.

Done when:
  - The three splits are saved and their sizes and label balance print.

Questions (answer as comments at the bottom of this file):
  1. What fraction of generated examples did you throw away, and why?
  2. When is fine-tuning the right tool instead of prompting or RAG?
"""
