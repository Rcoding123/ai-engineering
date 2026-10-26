"""
Project 05 · Step 3 — Answer with citations

Objective:
The core of RAG: retrieve relevant chunks for a question and have the model
answer from them, citing exactly where each claim came from.

Requirements:
  - Embed the chunks and retrieve the top-k for each question (reuse your
    Project 04 code).
  - The model answers using only the retrieved chunks, and cites chunk ids
    for its claims. Citations must be checkable: print the cited chunks'
    sources below the answer.
  - When the retrieved chunks do not contain the answer, the system says it
    does not know instead of guessing.
  - Interactive: ask questions in a loop.

Done when:
  - 5 answerable questions get correct, cited answers and 3 unanswerable ones
    get "I don't know".

Questions (answer as comments at the bottom of this file):
  1. Did the model ever cite a chunk that did not support the claim?
  2. What decides "nothing relevant was found"? How did you set it?
"""
