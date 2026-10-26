"""
Project 04 · Step 5 — Keyword search and hybrid search

Objective:
Add classic keyword search (BM25) and a hybrid that combines it with
semantic search.

Requirements:
  - BM25 search over the same corpus with the same output format.
  - A hybrid mode that merges the keyword and semantic result lists into one
    ranking. Research a standard way to merge rankings and use it.
  - A command-line switch to choose: keyword, semantic or hybrid.

Done when:
  - All three modes run on the same queries.

Questions (answer as comments at the bottom of this file):
  1. Find a query where keyword search wins (hint: exact names, codes, rare words).
  2. Find one where semantic search wins.
"""
