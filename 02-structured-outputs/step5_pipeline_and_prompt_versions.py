"""
Project 02 · Step 5 — Full pipeline and prompt versions

Objective:
Turn the pieces into a pipeline you can run on a whole folder, and use it to
compare prompt versions with real numbers.

Requirements:
  - One command processes every document in the folder and writes one result
    per line to an output file (valid records and failures, clearly marked).
  - Documents are processed concurrently, with a limit on how many requests
    run at the same time.
  - At the end, print: success rate, failures by type, total cost, total time.
  - Create prompts v2 and v3 (each a deliberate change from the previous one)
    and run the pipeline once per version.

Done when:
  - Your success rate is at least 95%, and you can point to the prompt change
    that moved the number.

Questions (answer as comments at the bottom of this file):
  1. What changed in v2 and v3, and what did each change do to the numbers?
  2. What concurrency limit did you pick, and what happened when you raised it?
"""
