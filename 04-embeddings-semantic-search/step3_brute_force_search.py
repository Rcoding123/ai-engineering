"""
Project 04 · Step 3 — Semantic search by brute force

Objective:
Search the corpus by meaning using nothing but arrays and math.

Requirements:
  - Take a query from the command line, embed it, compare it with every item
    vector, and print the top 5 items with their scores.
  - The comparison over all items is done in one vectorized operation, not a
    Python loop over items.
  - Print how long the search took (excluding embedding the query).

Done when:
  - Five different queries return sensible results.

Questions (answer as comments at the bottom of this file):
  1. Find a query where semantic search finds a result that shares no words
     with the query. Write it down.
"""
