"""
Project 07 · Step 3 — Context management on long tasks

Objective:
Long research fills the context with page contents. Keep the agent effective
when there is more material than it should carry.

Requirements:
  - Give the agent a task that needs 10+ pages.
  - Keep the context under a token budget you set. Design the approach
    yourself; the agent must still be able to use what it learned earlier.
  - The plan is updated as the agent learns things.
  - Compare final quality and cost with and without your context management.

Done when:
  - The long task finishes within budget with an answer at least as good.

Questions (answer as comments at the bottom of this file):
  1. What did the agent lose when old material was removed, and did it matter?
"""
