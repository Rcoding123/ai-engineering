"""
Project 03 · Step 4 — LLM as judge

Objective:
Some outputs cannot be checked with exact rules (a summary, a tone, an
explanation). Use a model as a grader with a written rubric.

Requirements:
  - Add a free-text field to your task that has no single correct answer
    (e.g. a one-sentence summary of each document).
  - Write a rubric: what scores 1, 2, 3, 4 and 5, with concrete descriptions.
  - The judge returns a score and a short reason in a structured format.
  - The judge is a metric your harness can use like any other.
  - Record the judge's own cost separately.

Done when:
  - The harness reports an average judge score with the reasons saved per example.

Questions (answer as comments at the bottom of this file):
  1. Run the judge twice on the same outputs. How stable are the scores?
  2. What does the judge reward that you did not intend?
"""
