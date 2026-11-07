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

from anthropic import Anthropic

client = Anthropic()

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 4000
INPUT_RATE = 0.10
OUTPUT_RATE = 0.5


def turn_cost(
    input_rate: float, output_rate: float, input_tokens: int, output_tokens: int
) -> float:
    """Calculate the turn cost of a user input and model response"""
    return ((input_rate / 1_000_000) * input_tokens) + (
        (output_rate / 1_000_000) * output_tokens
    )


def main():
    # Memory
    message_history = []

    # Number of turns
    turns = 0
    # Total cost
    session_cost = 0.0

    while True:
        user_input = input("You: ").strip()

        if user_input == "":
            continue

        if user_input == "quit":
            break

        message_history.append({"role": "user", "content": user_input})

        # Make the model call
        response = client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS, messages=message_history
        )

        # Print out the response
        for block in response.content:
            if block.type == "text":
                print(f"Claude: {block.text}")

        # Add response to message_history. A reply with no text can't be saved,
        # so drop the user message too: the history keeps whole turns only.
        if any(block.type == "text" for block in response.content):
            message_history.append({"role": "assistant", "content": response.content})
        else:
            message_history.pop()
            print("WARNING: the reply had no text, so this turn was not saved")

        # Max tokens warning
        if response.stop_reason == "max_tokens":
            print(f"WARNING: reply was cut off at the {MAX_TOKENS} token limit")

        # Update session variables
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = turn_cost(INPUT_RATE, OUTPUT_RATE, input_tokens, output_tokens)
        turns += 1
        session_cost += cost

        # One line summary of cost
        print(
            f"Input tokens: {input_tokens} | Output tokens: {output_tokens} | "
            f"Turn cost: ${cost:.6f} | Session cost: ${session_cost:.6f}"
        )

    # Overall summary
    print(
        f"Session Summary:\nNumber of turns: {turns} | Total session cost: ${session_cost:.6f}"
    )


if __name__ == "__main__":
    main()


# Experiment 1: five-turn conversation
#   turn   |  1 |  2 |  3 |  4 |   5
#   input  | 18 | 52 | 71 | 84 | 107
#   output | 23 | 11 |  6 | 10 |   8
#   Each turn's input = last turn's input + last turn's output + the new message.
#   Turn 2: 18 + 23 + about 11 = 52. The whole history is re-sent every turn.
#
# Experiment 2: stop saving the assistant's replies
#   Nothing crashes, and the name is still remembered, because it was in MY
#   message and those are still saved. What breaks is silent: the model can't
#   see its own replies, so old questions look unanswered and it answers them
#   again. Turn 4 reply: "2 + 2 is 4. A colour is blue. Your name is Sam."
#   It also can't refer back to anything it said.
#
# Experiment 3: one 50-turn chat vs 50 separate calls (estimate from experiment 1)
#   Input grows by about 22 tokens per turn: (107 - 18) / 4.
#   Chat input:     50 * 18 + 22 * (0 + 1 + ... + 49) = about 28,000 tokens = $0.0028
#   Separate input: 50 * 18                           = about    900 tokens = $0.00009
#   Output is the same either way: 50 * 12 = about 600 tokens = $0.0003
#   Total: chat about $0.0031, separate about $0.0004, so roughly 8x more.
#   Input alone is about 30x more. Each turn grows steadily, but the total grows
#   fast because you pay for the whole history again on every turn.
