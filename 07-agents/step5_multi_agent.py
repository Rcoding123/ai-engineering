"""
Project 07 · Step 5 — Multiple agents

Objective:
Split the work: an orchestrator breaks the question into sub-questions and
hands each to a sub-agent, then combines their findings.

Requirements:
  - Sub-agents run with their own context and limits, and return a compact
    result, not their whole transcript.
  - Sub-agents may run in parallel.
  - Use a cheaper model for sub-agents if quality holds.
  - Compare against the single agent on the same 3 questions: quality, cost,
    wall time.

Done when:
  - The comparison table is written at the bottom of this file.

Questions (answer as comments at the bottom of this file):
  1. When is multi-agent worth its extra cost, and when is it not?
"""
