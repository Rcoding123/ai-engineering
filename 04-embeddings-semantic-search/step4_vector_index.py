"""
Project 04 · Step 4 — A vector index

Objective:
Move the same search into a vector index or vector database and compare it
with brute force.

Requirements:
  - Load all vectors into a vector index/database of your choice.
  - Same query interface and output as step 3.
  - Measure search latency for both approaches over the same 20 queries.
  - Check whether the top 5 results ever differ between the two.

Done when:
  - A small table compares latency and result overlap for both approaches.

Questions (answer as comments at the bottom of this file):
  1. If results differed, why? (Look up exact vs approximate nearest neighbor.)
  2. At what corpus size would brute force stop being good enough?
"""
