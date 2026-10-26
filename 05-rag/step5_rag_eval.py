"""
Project 05 · Step 5 — Evaluate the RAG system

Objective:
Measure each part of the system separately, so every wrong answer can be
traced to its cause.

Requirements:
  - At least 30 questions with: the expected answer and the chunk(s) or
    passage(s) that contain it. Include some unanswerable questions.
  - Use your Project 03 harness to measure:
      * retrieval recall: was the needed chunk retrieved?
      * faithfulness: is every claim supported by the retrieved chunks?
      * correctness: does the answer match the expected one?
      * refusal accuracy on the unanswerable questions
  - Run it for: chunking A vs B, and reranking off vs on.
  - For every wrong answer, label the cause: chunking, retrieval or generation.

Done when:
  - A results table covers all four configurations and the failure causes are counted.

Questions (answer as comments at the bottom of this file):
  1. Which part of your system causes most failures?
  2. What would you fix first, and what do you expect it to change?
"""
