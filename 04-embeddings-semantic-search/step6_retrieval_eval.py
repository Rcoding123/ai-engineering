"""
Project 04 · Step 6 — Measure retrieval

Objective:
Stop judging search by eye. Build a query set with known answers and score
all three search modes.

Requirements:
  - At least 30 queries, each with the id(s) of the item(s) that should be
    found. Mix query types: exact terms, paraphrases, vague questions.
  - Compute recall@5 and MRR for keyword, semantic and hybrid.
  - Show results per query type as well as overall.

Done when:
  - A table shows recall@5 and MRR for all three modes.

Questions (answer as comments at the bottom of this file):
  1. Which mode wins overall? Which wins per query type?
  2. Stretch: compare two embedding models on the same query set.
"""
