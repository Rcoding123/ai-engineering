"""
Project 11 · Step 1 — Serve it as an API

Objective:
Take your RAG system (Project 05) or agent (Project 07) and put it behind a
web API that other programs can call.

Requirements:
  - An HTTP endpoint that accepts a question and returns an answer.
  - A streaming endpoint that sends the answer as it is generated.
  - Input validation and clear error responses.
  - Configuration (keys, model, limits) from the environment, never in code.

Done when:
  - You can call both endpoints with curl and get correct answers.

Questions (answer as comments at the bottom of this file):
  1. What happens when two requests arrive at the same moment?
"""
