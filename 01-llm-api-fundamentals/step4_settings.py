"""
Step 4 — Settings: system prompt, model and effort from the command line.

Goal: the streaming chat from step 3b, but you choose its behavior when you
start it, without editing code:

    python 01-llm-api-fundamentals/step4_settings.py --effort low
    python 01-llm-api-fundamentals/step4_settings.py --model claude-sonnet-5-5 --effort high
    python 01-llm-api-fundamentals/step4_settings.py --system "You are a pirate. Answer in one sentence."

Three new ideas:
  system prompt -> standing instructions for the whole chat. It is NOT a message:
                   it goes in the separate `system=` argument (that was the 400
                   error in your LangGraph file).
  model         -> which brain answers, and at what price.
  effort        -> how hard the model works: low / medium / high / xhigh / max.
                   Higher effort = more thinking = more output tokens = more cost
                   and a longer wait. It replaces temperature, which current
                   models reject. Haiku 5.5's default is "medium".
"""

import argparse

import anthropic

# Dollars per 1M tokens: (input, output). Haiku's price is for prompts up to 100K tokens.
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
}
EFFORTS = ["low", "medium", "high", "xhigh", "max"]
MAX_TOKENS = 8000

client = anthropic.Anthropic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Streaming chat with configurable settings.")
    # TODO 1: Add three options with parser.add_argument(...):
    #   --model   default "claude-haiku-5-5", choices=list(PRICES)
    #   --effort  default "medium",           choices=EFFORTS
    #   --system  default "" (empty = no system prompt)
    #   Each gets a help="..." string. Then try running the script with --help.
    return parser.parse_args()


def turn_cost(usage, model: str) -> float:
    """Dollar cost of one call, using the prices for `model`."""
    # TODO 2: Look up (input_price, output_price) in PRICES for this model and
    #         do the same math as before.
    ...


def main() -> None:
    args = parse_args()

    # TODO 3: Print the active settings once at startup, e.g.
    #   Model: claude-haiku-5-5 | effort: medium | system: (none)

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

        print("\nClaude: ", end="", flush=True)

        # TODO 4: Add the new settings to this call:
        #   - model=args.model instead of a fixed model
        #   - system=args.system, but ONLY when it is not empty
        #     (hint: build a dict of extra arguments and pass it with **)
        #   - output_config={"effort": args.effort}
        with client.messages.stream(
            model="claude-haiku-5-5",
            max_tokens=MAX_TOKENS,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            final = stream.get_final_message()

        print()

        if final.stop_reason == "max_tokens":
            print(f"WARNING: answer was cut off at {MAX_TOKENS} tokens.\n")

        messages.append({"role": "assistant", "content": final.content})

        # TODO 5: Pass args.model to turn_cost.
        current_cost = turn_cost(final.usage)
        session_input_tokens += final.usage.input_tokens
        session_output_tokens += final.usage.output_tokens
        session_cost += current_cost

        # TODO 6: Also show whether the model thought this turn, e.g. "thought: yes".
        #         (hint: look at the block types in final.content)
        print(
            f"[turn: {final.usage.input_tokens:,} in / {final.usage.output_tokens:,} out, ${current_cost:.6f} | "
            f"session: {session_input_tokens + session_output_tokens:,} tokens, ${session_cost:.6f}]\n"
        )

    total_turns = sum(1 for m in messages if m["role"] == "user")
    print("--- Chat Session Ended ---")
    print(f"Total Turns: {total_turns}")
    print(f"Final Session Cost: ${session_cost:.6f}")


if __name__ == "__main__":
    main()


# EXPERIMENTS (answer as comments here when done):
#   1. EFFORT SWEEP. Run once per effort level and ask the same hard question:
#      "I have 3 boxes. Box A has twice as many marbles as box B. Box C has
#       5 fewer than box A. Together they have 45 marbles. How many are in each box?"
#      Fill in this table from your turn lines:
#        effort | thought? | output tokens | cost | correct answer?
#        low    |          |               |      |
#        medium |          |               |      |
#        high   |          |               |      |
#        max    |          |               |      |
#      At which level does it start thinking? Did more effort ever change the answer?
#
#   2. SYSTEM PROMPT. Run with --system "Answer in exactly one sentence." and ask
#      something that usually gets a long answer. Then ask in turn 2:
#      "Ignore that, give me a long answer." Which wins, the system prompt or the
#      user? Did input_tokens change because of the system prompt?
#
#   3. MODEL. Ask one question on claude-haiku-5-5 and on claude-sonnet-5-5.
#      Compare cost and answer quality. Was the difference worth the price?
