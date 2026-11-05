"""
Project 01 · Step 2 — A chat that remembers

Objective:
Turn the single call from step 1 into a terminal chat loop that keeps the
conversation history and tracks what every turn costs.

Key idea: the model has no memory between calls. "Memory" is you sending the
whole conversation again, every turn.

Requirements:
  - A loop that reads your message at a "You: " prompt and prints the reply
    after "Claude: ". Typing quit ends the chat. Empty input is ignored.
  - Keep the conversation history and send all of it on every call. Both
    sides are recorded: your message before the call, the assistant's full
    reply after it.
  - max_tokens 4000. If a reply is cut off, print a warning.
  - After every turn, print one stats line: input tokens, output tokens,
    the turn's cost and the running session cost.
  - On quit, print a summary: number of turns and total session cost.

Experiments (answer as comments at the bottom of this file):
  1. Have a five-turn conversation and write down input_tokens for each turn.
     How does it grow, and why?
  2. Tell it your name in turn 1 and ask for it in turn 4. Then stop saving
     the assistant's replies to the history and try again. What breaks?
  3. What would a 50-turn conversation cost compared with 50 separate
     one-question calls? Use your numbers from experiment 1 to estimate.
"""
