"""
Project 05 · Step 6 (stretch) — Query rewriting and re-indexing

Objective:
Improve retrieval for vague or multi-part questions, and keep the index
current when documents change.

Requirements:
  - Before retrieval, rewrite the user's question into one or more better
    search queries; merge the results.
  - Measure the effect with your step 5 eval.
  - When a document is added, changed or deleted, update only the affected
    chunks and vectors, not the whole index.

Done when:
  - The eval shows the effect of rewriting, and editing one document updates
    the index without a full rebuild.

Questions (answer as comments at the bottom of this file):
  1. Which question types did rewriting help, and which did it hurt?
"""
