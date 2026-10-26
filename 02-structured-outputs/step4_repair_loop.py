"""
Project 02 · Step 4 — Repair loop

Objective:
When an output fails validation, give the model one chance to fix it by
showing it exactly what was wrong.

Requirements:
  - On a validation failure, send one follow-up request containing the
    original document, the invalid output and the validation error, and ask
    for a corrected record.
  - At most one repair attempt per document.
  - Log: first attempt result, repair attempt result, and the cost of each.
  - Report how many documents were rescued by the repair and what the
    repairs cost in total.

Done when:
  - Your success rate after repair is printed alongside the rate before repair.

Questions (answer as comments at the bottom of this file):
  1. Which kinds of errors did repair fix, and which did it not?
  2. Was the extra cost worth the rescued documents?
"""
