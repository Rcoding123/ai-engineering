"""
Project 02 · Step 2 — Extraction with prompting only

Objective:
Get a model to turn one raw document into a record matching your schema using
only prompt instructions: no special API features yet. Find out how reliable
plain prompting is.

Requirements:
  - Write a prompt that explains the task and the expected JSON shape, and
    includes at least one example (input document -> correct JSON).
  - Use clear separation between instructions and the document text.
  - Parse the model's reply as JSON and validate it against your schema.
  - Run it on all 50 documents. For each one record: valid / invalid JSON /
    schema error, plus the raw reply.
  - Store the prompt in its own file (prompts/v1.txt), not inside the code.

Done when:
  - You have a printed success rate for v1 and a log of every failure with
    its input, raw output and error.

Questions (answer as comments at the bottom of this file):
  1. What kinds of failures happened? (Not JSON at all? Extra text around
     the JSON? Wrong types? Missing fields? Made-up values?)
  2. Did any output pass validation but still contain wrong values?
     How would you even detect that? (Project 03 answers this.)
"""
