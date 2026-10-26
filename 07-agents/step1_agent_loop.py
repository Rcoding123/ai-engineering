"""
Project 07 · Step 1 — The agent loop

Objective:
Build a research agent that takes a question, works out its own steps,
searches the web and reads pages, and stops when it has an answer.

Requirements:
  - The agent can search the web and fetch pages (via API tools or your own).
  - The agent writes a short plan before acting.
  - Hard limits: maximum number of steps and maximum cost per run. When a
    limit is hit, the agent stops and returns what it has, saying it was cut short.
  - Print each step as it happens.

Done when:
  - The agent answers a research question that needs at least 3 searches.

Questions (answer as comments at the bottom of this file):
  1. How is this different from your Project 06 assistant? Where exactly does
     the "agency" come from?
"""
