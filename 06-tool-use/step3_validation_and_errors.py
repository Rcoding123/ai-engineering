"""
Project 06 · Step 3 — Bad arguments and failing tools

Objective:
Tools fail and models send bad arguments. Handle both without crashing, and
let the model recover.

Requirements:
  - Validate every tool's arguments before running it.
  - Invalid arguments or a tool error produce a structured error result sent
    back to the model, marked as an error, explaining what was wrong.
  - Exceptions inside tools never crash the program.
  - Force each failure on purpose: a SQL syntax error, a city that does not
    exist, a web API timeout.

Done when:
  - For each forced failure, the model reads the error and recovers or
    explains the problem to the user.

Questions (answer as comments at the bottom of this file):
  1. What happens if you raise the exception instead of returning it as an error result?
"""
