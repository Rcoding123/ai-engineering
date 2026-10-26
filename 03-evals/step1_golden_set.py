"""
Project 03 · Step 1 — The golden set

Objective:
Create the ground truth that every later measurement depends on: correct
answers labeled by you, not by a model.

Requirements:
  - Hand-label at least 40 documents from Project 02 with the exact record
    you consider correct.
  - At least 10 of them must be hard cases (ambiguous, missing info, tricky
    formats). Tag each example with a category (e.g. easy / missing-field /
    multi-item / foreign-language).
  - Store the set as a data file (one example per line: id, input, expected
    output, category).
  - Running this file validates every expected output against the schema and
    prints counts per category.

Done when:
  - 40+ examples load, validate, and the category counts print.

Questions (answer as comments at the bottom of this file):
  1. Where were you unsure what the "correct" answer was? What did you decide,
     and why does that matter for an eval?
"""
