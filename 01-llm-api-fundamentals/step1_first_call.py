"""
Project 01 · Step 1 — Your first API call

Objective:
Send one message to Claude with the raw Anthropic SDK and inspect everything
that comes back, not just the text.

Requirements:
  - The API key comes from the environment (ANTHROPIC_API_KEY), never from
    your code.   d
  - Model: claude-haiku-5-5. Set max_tokens yourself.  d
  - Print the type of every content block in the response, and the text of
    each text block.  d
  - Print the stop_reason, the input tokens and the output tokens.  d
  - Compute and print the call's cost in dollars to 6 decimal places.
    Prices per 1M tokens for claude-haiku-5-5: $0.10 input / $0.50 output. d
  - If the reply was cut off by max_tokens, print a clear warning.

Experiments (answer as comments at the bottom of this file):
  1. Set max_tokens to 20 and run again. What changes in stop_reason and in
     the text? Did you still pay for those tokens?
  2. Run the same prompt three times. Do the text and the token counts
     change between runs? Why?
  3. Ask a one-word question, then ask for a 300-word essay. Which count
     moved more, input or output, and what did that do to the cost?
"""

from anthropic import Anthropic

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 1000
INPUT_RATE = 0.10 / 1_000_000  # dollars per input token
OUTPUT_RATE = 0.50 / 1_000_000  # dollars per output token

client = Anthropic()


def call_details(message: str) -> None:
    # Create a message
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": message}],
    )

    # Blocks
    for block in response.content:
        print(f"Block type: {block.type}")
        if block.type == "text":
            print(block.text)

    # Stop reason
    print(f"Stop reason: {response.stop_reason}")

    # Input and output tokens
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")

    # Total cost
    cost = input_tokens * INPUT_RATE + output_tokens * OUTPUT_RATE
    print(f"Total cost: ${cost:.6f}")

    if response.stop_reason == "max_tokens":
        print(f"WARNING: reply was cut off at the {MAX_TOKENS} token limit")


if __name__ == "__main__":
    call_details("Hi")


# Experiment 1: max_tokens = 20, "Tell me the weather in NYC"
#   stop_reason changed from end_turn to max_tokens.
#   The text stopped mid-sentence: "...so I can't check current weather in"
#   Yes, I still paid: 19 input + 20 output tokens = $0.000012.
#   Always check stop_reason before trusting the text.
#
# Experiment 2: same prompt three times, max_tokens = 1000
#   run | input | output | opening words
#    1  |  19   |  174   | "I don't have access to real-time data..."
#    2  |  19   |  147   | "I can't check live weather, so I don't have today's..."
#    3  |  19   |  168   | "I can't check live weather, so I don't have current..."
#   Input never changes: the same prompt always becomes the same tokens.
#   Text and output count change: the weights are fixed, but at each step the
#   model samples the next token from a set of probabilities, so the wording
#   and the length differ between runs.
#
# Experiment 3: short question vs essay
#   prompt      | input | output | cost
#   "Hi"        |  11   |   14   | $0.000008
#   300w essay  |  21   |  595   | $0.000300
#   Input grew about 2x, output about 42x, and the cost about 37x.
#   Output drove the cost: $0.000297 of the $0.000300. There were more output
#   tokens, and each one costs 5x an input token.
