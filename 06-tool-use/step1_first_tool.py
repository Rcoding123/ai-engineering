"""
Project 06 · Step 1 — Your first tool

Objective:
Give the model one tool and run the tool-call loop yourself: the model asks
for a tool, your code runs it, you send the result back, the model continues.

Requirements:
  - One tool: a calculator that evaluates arithmetic expressions safely.
    It must NOT run arbitrary Python (no eval/exec on model output).
  - Use the API's native tool-use feature (not parsing actions out of
    the model's text).
  - Write the loop yourself with the raw SDK, no helper that runs it for you.
  - The loop ends when the model stops asking for tools, with a maximum number
    of iterations as a safety limit.
  - Print every step: what the model asked for, the arguments, the result.

Done when:
  - "What is 17.5% of 2,340, plus 99?" is answered correctly using the tool.

Questions (answer as comments at the bottom of this file):
  1. Which stop_reason told you the model wanted a tool?
  2. What does the message list look like after one full tool round?
     Draw the shape of each message (role and block types).
"""
