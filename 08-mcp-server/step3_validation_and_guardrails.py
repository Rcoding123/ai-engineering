"""
Project 08 · Step 3 — Validation and a guarded write tool

Objective:
Add a tool that changes data, safely.

Requirements:
  - Every tool validates its input and returns clear error messages.
  - Add one write tool (create or update something).
  - Guardrails on the write tool: it cannot touch anything outside an allowed
    area, it cannot delete, and every write is logged.
  - Try to make the client misuse it (path tricks, huge inputs, odd
    characters) and confirm the guardrails hold.

Done when:
  - Your misuse attempts are listed at the bottom with the result of each.

Questions (answer as comments at the bottom of this file):
  1. Which attempt came closest to getting through?
"""
