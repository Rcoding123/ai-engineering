"""
Step 3b — A chat that streams.

Goal: your step 2 chat, but every reply appears word by word.
Two loops: the OUTER `while` is one pass per turn (step 2),
the INNER `for` is one pass per piece of the reply (step 3a).

Everything except the API call is copied from your step2_chat.py.

Run it with:
    python 01-llm-api-fundamentals/step3b_chat_stream.py
"""

import anthropic
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Model
MODEL = "claude-haiku-5-5"

# Max Tokens
MAX_TOKENS = 4000

# Prices for MODEL, in dollars per 1M tokens (for prompts up to 100K tokens;
# Haiku 5.5 charges $0.50 / $2.50 above that).
INPUT_RATE_PER_MILLION = 0.10
OUTPUT_RATE_PER_MILLION = 0.50

client = anthropic.Anthropic()


def turn_cost(usage) -> float:
    """Return the dollar cost of one API call, given response.usage."""
    input_cost = (usage.input_tokens / 1_000_000) * INPUT_RATE_PER_MILLION
    output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_RATE_PER_MILLION
    return input_cost + output_cost


def main() -> None:
    # The whole conversation lives in this list. It only ever grows.
    messages = []

    session_input_tokens = 0
    session_output_tokens = 0
    session_cost = 0.0

    print("Chat started. Type 'quit' to exit.\n")

    while True:
        user_text = input("You: ").strip()

        if not user_text:
            continue
        if user_text.lower() in ["quit", "exit"]:
            break

        messages.append({"role": "user", "content": user_text})

        # Label first, no newline: the reply streams in right after it.
        # flush=True so "Claude: " shows before the first piece arrives.
        print("\nClaude: ", end="", flush=True)

        # Same arguments as create(), but the connection stays open and the
        # reply arrives in pieces. text_stream yields only the answer text
        # (thinking is skipped).
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

            # The full reply, assembled by the SDK: the same Message object
            # create() returns.
            final = stream.get_final_message()

        # Streamed text never ends in a newline; end the line ourselves.
        print()

        if final.stop_reason == "max_tokens":
            print(f"⚠️ [WARNING]: Response was cut off because it hit the MAX_TOKENS limit of {MAX_TOKENS} tokens.\n")

        # All blocks (thinking included) go back into the history unchanged.
        messages.append({"role": "assistant", "content": final.content})

        current_cost = turn_cost(final.usage)

        session_input_tokens += final.usage.input_tokens
        session_output_tokens += final.usage.output_tokens
        session_cost += current_cost

        total_session_tokens = session_input_tokens + session_output_tokens

        print(
            f"[turn: {final.usage.input_tokens:,} in / {final.usage.output_tokens:,} out, ${current_cost:,.6f} | "
            f"session: {total_session_tokens:,} tokens, ${session_cost:,.6f}]\n"
        )

    total_turns = sum(1 for m in messages if m["role"] == "user")
    print("--- Chat Session Ended ---")
    print(f"Total Turns: {total_turns}")
    print(f"Final Session Cost: ${session_cost:,.6f}")


if __name__ == "__main__":
    main()


# EXPERIMENTS
#   1. Ask for something long ("Write a 300-word story about a robot").
#      How does it FEEL compared to step 2, where the whole reply appeared at once?
#      -> Much better: I start reading almost immediately. Streaming cuts TTFT
#         (time to first token), but total time to the last word stays about
#         the same. The model isn't faster; I just stop waiting for all of it.
#
#   2. Compare the turn cost line with a similar question in step 2.
#      Did streaming change the cost? Why or why not?
#      -> No. Measured with the same question in both scripts:
#           step2_chat.py          [turn: 29 in / 11 out, $0.000008]
#           step3b_chat_stream.py  [turn: 29 in / 11 out, $0.000008]
#         Billing is per token. Streaming sends the same request and gets the
#         same tokens back; only the delivery changes. (Small differences on
#         long answers are normal run-to-run variation, not streaming.)
#
#   3. Ask a hard question (e.g. the marbles puzzle from step 3a). There's a
#      pause after "Claude: " before any text appears. What is happening
#      during that pause, and why doesn't text_stream show it?
#      -> The model is thinking. Two things hide it:
#         - text_stream only yields text_delta pieces; thinking_delta is skipped.
#         - By default the thinking text is empty anyway (it only has text
#           with thinking={"type": "adaptive", "display": "summarized"}).
#         Those thinking tokens are still billed as output: the pause costs
#         time AND money for something the user never sees.
