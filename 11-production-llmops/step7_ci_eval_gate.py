"""
Project 11 · Step 7 — Evals in CI

Objective:
No change ships if it makes quality worse.

Requirements:
  - A CI pipeline that, on every change, runs tests and your eval suite.
  - Thresholds: if quality drops below them (or cost rises above them), the
    pipeline fails and blocks the deploy.
  - Prove it: make a change that should be blocked and show that it is.

Done when:
  - One passing and one blocked pipeline run exist.

Questions (answer as comments at the bottom of this file):
  1. How do you keep the eval suite cheap and fast enough to run on every change?
"""
