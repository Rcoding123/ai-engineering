"""
Project 11 · Step 2 — Observability

Objective:
Know what your service is doing: every request traced, with cost and latency.

Requirements:
  - Each request gets an id and a trace: model calls, tool/retrieval calls,
    tokens, cost, latency of each stage.
  - Traces and logs are stored and searchable.
  - A dashboard (or report command) shows: requests, errors, p50/p95 latency,
    cost per request, cost per day.
  - Sensitive data in prompts is not stored in plain logs.

Done when:
  - After 50 requests, the dashboard answers "how much did today cost, and
    which request was slowest and why?"

Questions (answer as comments at the bottom of this file):
  1. Which single stage dominates your latency?
"""
