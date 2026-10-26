"""
Project 03 · Step 3 — The harness

Objective:
Build one reusable tool that runs any pipeline on any dataset and scores it,
so every future change can be measured with one command.

Requirements:
  - Input: a pipeline (something that maps an input to an output), a dataset,
    and a list of metrics.
  - Output: per-example results and aggregate scores, saved under a unique
    run id together with the settings used (model, prompt version, date).
  - Tracks cost and latency per example and in total.
  - One command runs the full eval and prints a summary table.
  - Works on your Project 02 pipeline without changing that pipeline's code.

Done when:
  - Two runs with different prompt versions are saved and summarized.

Questions (answer as comments at the bottom of this file):
  1. What did you need to store about a run so that you could reproduce it
     a month from now?
"""
