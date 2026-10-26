"""
Project 04 · Step 2 — Embeddings

Objective:
Turn every item into a vector and understand what similarity between vectors
means. (Anthropic does not offer an embedding model; pick another provider's
or a local open-source one.)

Requirements:
  - Embed every corpus item, sending them in batches, and save the vectors
    next to the item ids so you never re-embed unchanged items.
  - Record: embedding dimensions, total time, and total cost (or "free/local").
  - Implement cosine similarity yourself (no library function for it).
  - Pick 3 pairs of items you expect to be similar and 3 you expect to be
    unrelated; print their similarity scores.

Done when:
  - Vectors are saved and your 6 similarity scores print.

Questions (answer as comments at the bottom of this file):
  1. Did the scores match your expectations? What surprised you?
  2. Why does it matter that a query and the documents use the same model?
"""
