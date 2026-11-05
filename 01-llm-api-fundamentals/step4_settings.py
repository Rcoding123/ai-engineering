"""
Step 4 — Settings: system prompt, model and effort from the command line.

Objective:
Build the streaming chat from step 3b again, but make three settings
choosable when the program starts, without editing code:

  1. System prompt: standing instructions that apply to the whole chat.
     Optional; when none is given, the chat behaves as before.
  2. Model: claude-haiku-5-5, claude-sonnet-5-5 or claude-opus-5-5.
     Default: claude-haiku-5-5.
  3. Effort: low, medium, high, xhigh or max. Default: medium.

Requirements:
  - Running the program with a help flag lists the three settings and their
    allowed values. An invalid value is rejected before the chat starts.
  - At startup, print the active model, effort and system prompt.
  - Cost must be correct for whichever model is chosen.
    Prices per 1M tokens (input / output):
        claude-haiku-5-5    $0.10 / $0.50   (prompts up to 100K tokens)
        claude-sonnet-5-5   $2.00 / $10.00
        claude-opus-5-5     $4.00 / $20.00
  - Each turn's stats line also shows whether the model thought that turn.
  - Everything from step 3b still works: streaming, memory, max_tokens
    warning, per-turn and session cost, final summary.

Experiments (answer as comments at the bottom of this file):
  1. Ask this at every effort level, one run each:
       "I have 3 boxes. Box A has twice as many marbles as box B. Box C has
        5 fewer than box A. Together they have 45 marbles. How many are in
        each box?"
     Make a table: effort | thought? | output tokens | cost | correct?
     At which level does it start thinking? Did more effort change the answer?
  2. Set the system prompt to "Answer in exactly one sentence." Ask something
     that usually gets a long answer, then ask "Ignore that, give me a long
     answer." Which wins? Did the system prompt change input_tokens?
  3. Ask the same question on Haiku and on Sonnet. Compare cost and quality.
     Was the difference worth the price?
"""
