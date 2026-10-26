"""
Project 03 · Step 2 — Deterministic metrics

Objective:
Score a predicted record against the expected one with metrics that need no
model and always give the same answer.

Requirements:
  - Exact match: whole record correct, yes or no.
  - Field-level scores: for each field, correct / wrong / missing / extra.
  - Precision, recall and F1 over fields, per example and aggregated.
  - Decide and document how you compare values that are "the same" but written
    differently (case, whitespace, number formats, dates).
  - Write tests for the metric functions using small hand-made cases,
    including edge cases (both empty, list order, missing optional field).

Done when:
  - Your tests pass and the metrics run on one pipeline output vs the golden set.

Questions (answer as comments at the bottom of this file):
  1. Why can exact match be misleading on its own?
  2. Which normalization decision changed the scores the most?
"""
