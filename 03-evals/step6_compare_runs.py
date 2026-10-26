"""
Project 03 · Step 6 — Compare runs, find regressions

Objective:
A change rarely makes everything better. Show exactly which examples improved
and which got worse between two runs.

Requirements:
  - Given two run ids, list: improved examples, regressed examples, unchanged.
  - Break the scores down by category from your golden set.
  - Show the change in cost and latency.
  - Use it on a real change (new prompt version or a different model).

Done when:
  - You make a change, run the eval, and can say with evidence whether it was
    better overall and where it was worse.

Questions (answer as comments at the bottom of this file):
  1. Did any change improve the average but hurt one category? Would you ship it?
  2. Stretch: how would you run this automatically on every prompt change?
"""
