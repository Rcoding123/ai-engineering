"""
Step 2 — A chat that remembers.

Goal: turn the single call from step 1 into a terminal chat loop that keeps
the conversation history, and track what every turn costs.

Key idea: the model has NO memory between calls. "Memory" is just you
sending the whole conversation again, every single turn.

Run it with:
    python 01-llm-api-fundamentals/step2_chat.py
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
    # TODO 1: Same math as step 1, wrapped in a function so you can reuse it.
    # Note: Anthropic's usage object uses dot-notation access (.input_tokens).
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

        # TODO 2: If the user typed nothing, skip this loop iteration.
        #         If they typed "quit" or "exit", break out of the loop.
        if not user_text:
            continue
        if user_text.lower() in ["quit", "exit"]:
            break

        # TODO 3: Append the user's message to `messages`.
        #         Shape: {"role": "user", "content": user_text}
        messages.append({"role": "user", "content": user_text})

        # TODO 4: Call the API, sending the WHOLE `messages` list.
        #         Use max_tokens=4000 so thinking doesn't eat the answer.
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages
        )

        # TODO 5: Print Claude's text (same loop as step 1), prefixed "Claude: ".
        #         If stop_reason is "max_tokens", also print a warning that the
        #         answer was cut off.
        full_response_text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        print(f"\nClaude: {full_response_text}\n")

        if response.stop_reason == "max_tokens":
            print(f"⚠️ [WARNING]: Response was cut off because it hit the MAX_TOKENS limit of {MAX_TOKENS} tokens.\n")

        # TODO 6: Append Claude's reply to `messages` so the next turn
        #         remembers it. Shape: {"role": "assistant", "content": ...}
        #         Use response.content (ALL the blocks, thinking included),
        #         not just the text. The API expects thinking blocks to be
        #         sent back unchanged.
        messages.append({"role": "assistant", "content": response.content})

        # TODO 7: Update the three session totals, then print one line like:
        #   [turn: 412 in / 96 out, $0.003568 | session: 1,203 tokens, $0.009120]
        #   Tip: f"{n:,}" adds thousands separators.
        current_cost = turn_cost(response.usage)
        
        session_input_tokens += response.usage.input_tokens
        session_output_tokens += response.usage.output_tokens
        session_cost += current_cost
        
        total_session_tokens = session_input_tokens + session_output_tokens

        # Avoid nested quotes syntax errors by using single quotes inside double-quoted f-strings
        print(
            f"[turn: {response.usage.input_tokens:,} in / {response.usage.output_tokens:,} out, ${current_cost:,.6f} | "
            f"session: {total_session_tokens:,} tokens, ${session_cost:,.6f}]\n"
        )

    # TODO 8: After the loop, print a final summary: number of turns
    #         (hint: how many user messages are in `messages`?) and total cost.
    total_turns = sum(1 for m in messages if m["role"] == "user")
    print("--- Chat Session Ended ---")
    print(f"Total Turns: {total_turns}")
    print(f"Final Session Cost: ${session_cost:,.6f}")


if __name__ == "__main__":
    main()


# EXPERIMENT ANSWERS:
#   1. What pattern do you see with input_tokens, and why?
#      - Pattern: The input_tokens increase steadily with each subsequent turn.
#      - Why: Since LLM calls are stateless, we append the entire prior history 
#        (User + Claude) into the prompt array on every new round. You are actively 
#        re-submitting previous data, which grows larger over time.
#
#   2. What happens when sending ONLY the latest message, and why?
#      - What happens: Claude forgets your name and acts like a brand new chat.
#      - Why: Because the conversation history array was dropped. The LLM has no server-side 
#        memory. Without sending the prior messages list, the context no longer exists.
#      - Input_tokens: They drop back down significantly because you are only paying 
#        for a single isolated sentence instead of the accumulated conversation history.
#
#   3. If this chat ran for 100 turns, what would happen to the cost and what breaks?
#      - Cost: The price per turn scales quadratically/compounds aggressively because you pay for 
#        the same aging text over and over again on turn 98, 99, and 100.
#      - What breaks: Eventually, the chat history will completely fill up the model's 
#        maximum context window limit (or your token/budget cap), causing the API to throw a 
#        400 error and fail outright unless you implement an automated slicing/truncation strategy.
