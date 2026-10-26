"""
Project 05 · Step 4 — Reranking

Objective:
Retrieve more candidates than you need, then reorder them with a more
precise (and slower) relevance step before answering.

Requirements:
  - Retrieve a larger candidate set (e.g. top 20), rerank it, keep the best few.
  - The reranker is either a dedicated reranking model or an LLM scoring each
    candidate; your choice, but measure its cost and latency.
  - A switch turns reranking on and off.

Done when:
  - You can run the same questions with and without reranking.

Questions (answer as comments at the bottom of this file):
  1. Show one question where reranking changed the answer. Better or worse?
"""
