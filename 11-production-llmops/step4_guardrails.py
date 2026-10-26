"""
Project 11 · Step 4 — Guardrails and prompt injection

Objective:
Defend the service against hostile input and protect user data.

Requirements:
  - A test suite of at least 20 prompt-injection attacks: direct ("ignore
    your instructions..."), indirect (instructions hidden inside documents your
    system retrieves), and data exfiltration attempts.
  - Defenses of your own design; measure which attacks are blocked.
  - Personal data (emails, phone numbers, ...) is detected and handled
    according to a rule you write down.
  - Output filtering for things the service must never return.

Done when:
  - A table lists every attack and whether it was blocked, before and after
    your defenses.

Questions (answer as comments at the bottom of this file):
  1. Which attacks still get through, and why are they hard to stop?
"""
