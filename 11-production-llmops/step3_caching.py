"""
Project 11 · Step 3 — Caching

Objective:
Stop paying twice for the same work.

Requirements:
  - Prompt caching for the stable part of your prompts.
  - A response cache for repeated identical questions, with an expiry.
  - Stretch: a semantic cache for questions that are worded differently but
    mean the same.
  - Report: hit rate per cache, money saved, latency saved.

Done when:
  - A replay of 100 realistic requests shows hit rates and savings.

Questions (answer as comments at the bottom of this file):
  1. When would serving a cached answer be wrong?
"""
