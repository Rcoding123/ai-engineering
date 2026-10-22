"""
Rebuild — Step 1: The first call

Objective:
Send one message to Claude (claude-haiku-5-5) and inspect everything that
comes back, not just the text. Print the reply's text, the stop_reason,
the input and output token counts, and the dollar cost of the call.
"""
import anthropic

# Set CONST VALUES
MODEL = "claude-haiku-5-5"
MAX_TOKENS = 1000
INPUT_COST_PER_MILLION = 0.10
OUTPUT_COST_PER_MILLION = 0.50

# Set up client
client = anthropic.Anthropic()

# Start a message
response = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    messages=[{"role": "user", "content": "What is the diameter of the sun and mercury"}]
)

# Print the stop reason
if response.stop_reason == "max_tokens":
    print(f"WARNING: answer was cut off at {MAX_TOKENS} tokens ({response.stop_reason})")
elif response.stop_reason == "end_turn":
    print(f"END TURN: {response.stop_reason}")
else:
    print(f"Stopped for another reason: {response.stop_reason}")

# Read the response --> ensure to skip the thinking blocks
for block in response.content:
    if block.type == "text":
        print(f"Claude's response: {block.text}")

# Figure out the cost of usage (input and output)
input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
cost = ((input_tokens / 1_000_000) * INPUT_COST_PER_MILLION) + ((output_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION)

print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Final cost: ${cost:.6f}")
