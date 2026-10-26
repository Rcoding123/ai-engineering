"""
Project 02 · Step 3 — Schema-enforced output

Objective:
Use the API's own structured-output support so the model's reply is
constrained to your schema, and compare reliability with step 2.

Requirements:
  - Extract all 50 documents using the API's structured-output feature with
    your schema.
  - Keep the same validation and logging as step 2.
  - Measure success rate, total cost and total time; compare with step 2 in
    a small printed table.

Done when:
  - You have side-by-side numbers for prompting-only vs schema-enforced.

Questions (answer as comments at the bottom of this file):
  1. Did invalid JSON disappear completely? Did wrong-but-valid values?
  2. What does schema enforcement guarantee, and what can it never guarantee?
"""
