"""
Project 02 · Step 6 (stretch) — Classify, then route

Objective:
Mix two or three document types in one folder. Classify each document first,
then extract it with a type-specific schema and prompt.

Requirements:
  - A classification step that returns one of a fixed set of document types
    (plus "unknown").
  - Each type has its own schema and prompt.
  - "unknown" documents are reported, not forced into a schema.
  - Report classification accuracy against your own labels and the
    extraction success rate per type.

Done when:
  - A mixed folder is processed end to end and the per-type report prints.

Questions (answer as comments at the bottom of this file):
  1. Could a cheaper model do the classification step? Measure it.
"""
