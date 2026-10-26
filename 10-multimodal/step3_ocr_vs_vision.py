"""
Project 10 · Step 3 — OCR + LLM vs native vision

Objective:
Compare two approaches on the same documents: classic OCR to text and then
an LLM, vs sending the image straight to a vision model.

Requirements:
  - 30 documents, with correct records labeled by you.
  - Pipeline A: OCR -> text -> LLM extraction.
  - Pipeline B: image -> vision model extraction.
  - Score both with your harness: accuracy, latency, cost, per document type.

Done when:
  - A comparison table by document type exists.

Questions (answer as comments at the bottom of this file):
  1. Where did OCR win, and where did vision win? Why?
"""
