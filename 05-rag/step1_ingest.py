"""
Project 05 · Step 1 — Ingest documents

Objective:
Turn a pile of real documents in different formats into clean text with
source information attached.

Requirements:
  - At least 20 real documents across at least three formats (PDF, HTML,
    Markdown, plain text, ...). Pick a topic you could ask real questions about.
  - Extract the text from each, keeping: source file, page or section, title.
  - Clean out headers/footers, navigation, and repeated boilerplate.
  - Save the result so later steps do not re-parse the files.
  - Report anything that failed to parse instead of silently skipping it.

Done when:
  - All documents are parsed (or reported), and you can print any page of any
    document from the saved output.

Questions (answer as comments at the bottom of this file):
  1. Which format was hardest to get clean text from, and what got lost?
"""
