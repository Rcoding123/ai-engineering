"""
Project 07 · Step 2 — Traces

Objective:
Record every step of a run so you can understand it afterwards, especially
when it goes wrong.

Requirements:
  - Each run saves a trace file: every model call (input size, output,
    stop reason, tokens, cost, time) and every tool call (arguments, result size,
    time), in order.
  - A viewer command prints a readable timeline of any saved trace.
  - Run totals: steps, tokens, cost, wall time.

Done when:
  - You can open the trace of yesterday's run and follow every decision.

Questions (answer as comments at the bottom of this file):
  1. Read the trace of a run that went badly. At which step did it go wrong, and why?
"""
