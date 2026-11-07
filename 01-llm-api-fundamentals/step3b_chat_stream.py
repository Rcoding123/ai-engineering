"""
Project 01 · Step 3b — A chat that streams

Objective:
Build the step 2 chat again, but every reply appears word by word as it is
generated, instead of all at once at the end.

Requirements:
  - Everything from step 2 still works: memory, quit, empty-input skip,
    max_tokens warning, per-turn stats line, session summary on quit.
  - Each reply is printed piece by piece as it streams, flushed immediately.
  - Usage, stop_reason and the content saved to the history all come from
    the final message, once the stream has finished.

Experiments (answer as comments at the bottom of this file):
  1. Ask for a long answer here and in step 2. Which feels faster? Did the
     total time actually change?
  2. Have the same three-turn conversation here and in step 2. Compare the
     token counts and the cost. Does streaming cost more?
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

        print("Claude: ", end="", flush=True)
        with client.messages.stream(
            model=MODEL, max_tokens=MAX_TOKENS, messages=message_history
        ) as stream:
            for event in stream:
                if event.type == "text":
                    print(event.text, end="", flush=True)

            # Get final message
            print()
            final_message = stream.get_final_message()

        # Add response to message_history. There needs to be a text reply
        if any(block.type == "text" for block in final_message.content):
            message_history.append(
                {"role": "assistant", "content": final_message.content}
            )
        else:
            message_history.pop()
            print("WARNING: the reply had no text, so this turn was not saved")

        # Max tokens warning
        if final_message.stop_reason == "max_tokens":
            print(f"WARNING: reply was cut off at the {MAX_TOKENS} token limit")

        # Update session variables
        input_tokens = final_message.usage.input_tokens
        output_tokens = final_message.usage.output_tokens
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


# Experiment 1: long answer, step 2 vs here (3 runs each)
#   "Explain how a black hole forms, in about 500 words."
#   version | first words | total  | output tokens
#   step 2  |  9.72s      |  9.72s | 2061
#   step 2  | 10.11s      | 10.11s | 2150
#   step 2  |  5.32s      |  5.32s |  945
#   step 3b |  1.26s      |  5.73s | 1070
#   step 3b |  1.91s      |  6.37s | 1170
#   step 3b |  1.99s      |  6.64s | 1231
#   Streaming feels much faster: the first words show up in about 1-2s.
#   In step 2 you stare at nothing until the whole answer appears at once.
#   Total time did not change because of streaming. It follows the output
#   tokens: step 2 run 3 (945 tokens, 5.32s) and step 3b run 1 (1070 tokens,
#   5.73s) are close. Streaming shows the same work sooner, it isn't faster.
#
# Experiment 2: same three-turn chat in both
#   turn | step 2 in/out | step 3b in/out
#    1   |   18 / 23     |   18 / 23
#    2   |   52 / 11     |   52 / 11
#    3   |   70 / 25     |   70 / 23
#   Session cost: step 2 $0.000044, step 3b $0.000043.
#   Streaming does not cost more. Input was identical. The tiny difference is
#   2 output tokens on turn 3: replies vary in length because of sampling, not
#   because of how they are delivered.
