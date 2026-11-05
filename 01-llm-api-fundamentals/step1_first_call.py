"""
Project 01 · Step 1 — Your first API call

Objective:
Send one message to Claude with the raw Anthropic SDK and inspect everything
that comes back, not just the text.

Requirements:
  - The API key comes from the environment (ANTHROPIC_API_KEY), never from
    your code.
  - Model: claude-haiku-5-5. Set max_tokens yourself.
  - Print the type of every content block in the response, and the text of
    each text block.
  - Print the stop_reason, the input tokens and the output tokens.
  - Compute and print the call's cost in dollars to 6 decimal places.
    Prices per 1M tokens for claude-haiku-5-5: $0.10 input / $0.50 output.
  - If the reply was cut off by max_tokens, print a clear warning.

Experiments (answer as comments at the bottom of this file):
  1. Set max_tokens to 20 and run again. What changes in stop_reason and in
     the text? Did you still pay for those tokens?
  2. Run the same prompt three times. Do the text and the token counts
     change between runs? Why?
  3. Ask a one-word question, then ask for a 300-word essay. Which count
     moved more, input or output, and what did that do to the cost?
"""
