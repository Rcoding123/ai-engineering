"""
Step 1 — Your first API call.

Goal: send one message to Claude and inspect EVERYTHING that comes back,
not just the text.

Run it with:
    python 01-llm-api-fundamentals/step1_first_call.py
"""

import anthropic
from dotenv import load_dotenv

# Loads ANTHROPIC_API_KEY from the .env file at the repo root into the
# environment, so the key never appears in your code.
load_dotenv()

MODEL = "claude-haiku-5-5"

# Prices for MODEL, in dollars per 1M tokens. They change per model.
# (Step 1 was first run on claude-opus-5-5 at $4.00 / $20.00.)
INPUT_RATE_PER_MILLION = 0.10
OUTPUT_RATE_PER_MILLION = 0.50

# TODO 1: Create a client. Hint: anthropic.Anthropic() reads the key from
#         the environment by itself — don't pass the key in.
client = anthropic.Anthropic()

# TODO 2: Call client.messages.create(...) with three required arguments:
#         - model:      MODEL
#         - max_tokens: the most tokens the reply may use (try 1000)
#         - messages:   a list of {"role": ..., "content": ...} dicts
#         Ask it something you can check, e.g. "Explain what a token is in 2 sentences."
response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    messages=[{"role": "user", "content": "Explain what a token is in 2 sentences"}],
)

# TODO 3: Print the reply's text.
#         Careful: response.content is a LIST of blocks, and with this model
#         the first block is often NOT text. Loop over the blocks and only
#         print the ones whose .type == "text".
for block in response.content:
    print(block.type)
    if block.type == "text":
        print(f"Final response: {block.text}")

# TODO 4: Print these and write down what each one means in your own words:
#   stop_reason:   why the model stopped generating. end_turn = finished
#                  normally, max_tokens = cut off by the cap, tool_use = wants
#                  me to run a tool, refusal = declined.
#   input_tokens:  everything I sent (system prompt + full history + overhead),
#                  not just my latest prompt.
#   output_tokens: everything the model generated, INCLUDING thinking,
#                  not just the visible text.
input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens

print(f"stop_reason:   {response.stop_reason}")
print(f"input_tokens:  {input_tokens}")
print(f"output_tokens: {output_tokens}")

call_cost = (
    input_tokens / 1_000_000 * INPUT_RATE_PER_MILLION
    + output_tokens / 1_000_000 * OUTPUT_RATE_PER_MILLION
)
print(f"Call cost:     ${call_cost:.6f}")

# TODO 5 (experiment): Set max_tokens to 20 and run again.
#         What changes in stop_reason and in the text? Why?
#   With max_tokens=20 the stop_reason is max_tokens AND there is no text at
#   all: thinking used up the whole budget before the answer started. I still
#   paid for those 20 output tokens. Always check stop_reason before trusting
#   the output.

