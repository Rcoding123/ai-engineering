"""
Project 11 · Step 5 — Resilience

Objective:
Keep working when things go wrong upstream or too many users arrive.

Requirements:
  - Rate limiting per client.
  - Fallback: when the primary model fails or is overloaded, use a backup
    model or provider; the response says which one answered.
  - Model routing: a cheap model answers easy requests, harder ones go to a
    stronger model. Define and measure what "easy" means.
  - Graceful degradation: a clear message instead of a crash when everything fails.

Done when:
  - You can simulate a primary-model outage and the service keeps answering.

Questions (answer as comments at the bottom of this file):
  1. How much did routing save, and did quality drop?
"""
