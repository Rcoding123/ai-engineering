"""
Project 11 · Step 8 — Load test

Objective:
Find out how the service behaves under real load and what it costs at scale.

Requirements:
  - A load test with realistic questions at increasing concurrency.
  - Report p50 and p95 latency, error rate and cost per 1,000 requests at
    each level.
  - Find the point where it breaks or slows down sharply, and explain why.

Done when:
  - The load report is written at the bottom of this file.

Questions (answer as comments at the bottom of this file):
  1. What is your bottleneck: your code, the model API's rate limits, or the host?
"""
