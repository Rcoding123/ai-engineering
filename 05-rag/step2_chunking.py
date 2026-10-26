"""
Project 05 · Step 2 — Chunking

Objective:
Split documents into chunks that retrieval can return. Build two strategies
and compare them.

Requirements:
  - Strategy A: fixed-size chunks with overlap.
  - Strategy B: chunks that follow the document's structure (paragraphs,
    headings, sections), with a maximum size.
  - Every chunk keeps a stable id and its source (document, page/section).
  - Print stats per strategy: number of chunks, size distribution, and 3
    example chunks.

Done when:
  - Both chunk sets are saved and their stats print.

Questions (answer as comments at the bottom of this file):
  1. Find a chunk from strategy A that cuts an important idea in half.
  2. What chunk size did you choose, and what is the trade-off?
"""
