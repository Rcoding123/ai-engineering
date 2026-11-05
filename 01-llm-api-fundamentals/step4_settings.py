import argparse
import os
import sys
from dotenv import load_dotenv
import anthropic

# Initialize environment configuration
load_dotenv()

# Price mapping per 1M tokens (input / output)
MODELS = {
    "claude-haiku-5-5": {"input": 0.10, "output": 0.50},
    "claude-sonnet-5-5": {"input": 2.00, "output": 10.00},
    "claude-opus-5-5": {"input": 4.00, "output": 20.00}
}

# Use a list to maintain exact alphabetical display order
MODEL_EFFORT = ["low", "medium", "high", "xhigh", "max"]
MAX_TOKENS = 4000

class ChatArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='AI-Chat',
            description='AI chat bot with selectable system prompt, model, and effort settings.',
        )
        self.parser.add_argument(
            "-p", "--system", 
            type=str, 
            default="", 
            help="Standing instructions that apply to the whole chat. Optional."
        )
        self.parser.add_argument(
            "-m", "--model", 
            type=self.validate_model, 
            default="claude-haiku-5-5", 
            help="The Claude model to use. Allowed values: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5."
        )
        self.parser.add_argument(
            "-e", "--effort", 
            type=self.validate_effort, 
            default="medium", 
            help="The reasoning effort level. Allowed values: low, medium, high, xhigh, max."
        )

    def validate_model(self, model: str) -> str:
        val = model.lower()
        if val not in MODELS:
            raise argparse.ArgumentTypeError(f"Invalid model '{model}'. Allowed values: {', '.join(MODELS.keys())}")
        return val

    def validate_effort(self, effort: str) -> str:
        val = effort.lower()
        if val not in MODEL_EFFORT:
            raise argparse.ArgumentTypeError(f"Invalid effort '{effort}'. Allowed values: {', '.join(MODEL_EFFORT)}")
        return val

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()


def print_startup_settings(args: argparse.Namespace) -> None:
    sys_prompt = args.system if args.system.strip() else "None"
    print("=" * 60)
    print(f"{'Active Model:':<20} {args.model}")
    print(f"{'Active Effort:':<20} {args.effort}")
    print(f"{'Active Sys Prompt:':<20} {sys_prompt}")
    print("=" * 60 + "\n")


def calculate_turn_cost(usage, model: str) -> float:
    rates = MODELS[model]
    input_cost = (usage.input_tokens / 1_000_000) * rates["input"]
    output_cost = (usage.output_tokens / 1_000_000) * rates["output"]
    return input_cost + output_cost


def conversation(args: argparse.Namespace, client: anthropic.Anthropic):
    memory = []
    
    total_turns = 0
    session_input = 0
    session_output = 0
    session_cost = 0.0

    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_text = input("You> ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_text:
            continue
        if user_text.lower() in ["quit", "exit"]:
            break

        # User block format mapping
        memory.append({"role": "user", "content": user_text})
        print("\nClaude> ", end="", flush=True)

        kwargs = {
            "model": args.model,
            "max_tokens": MAX_TOKENS,
            "messages": memory,
            "output_config": {"effort": args.effort}
        }
        
        if args.system.strip():
            kwargs["system"] = args.system

        try:
            with client.messages.stream(**kwargs) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                final = stream.get_final_message()
            print()
        except Exception as e:
            print(f"\n❌ API Error encountered: {e}\n")
            memory.pop()
            continue

        if final.stop_reason == "max_tokens":
            print(f"⚠️ [WARNING]: Response was cut off because it hit the MAX_TOKENS limit of {MAX_TOKENS} tokens.\n")

        # Properly append the structured content object blocks for correct turn 2 message framing
        memory.append({"role": "assistant", "content": final.content})

        # Telemetry calculations
        usage = final.usage
        turn_cost_val = calculate_turn_cost(usage, args.model)
        
        # Safe extraction of native thinking metrics from the explicit final object structure
        thinking_tokens = 0 if usage.output_tokens_details is None else usage.output_tokens_details.thinking_tokens
        did_think = "Yes" if thinking_tokens > 0 else "No"

        # Track session milestones
        total_turns += 1
        session_input += usage.input_tokens
        session_output += usage.output_tokens
        session_cost += turn_cost_val

        print(f"📊 [Turn Stats] Input: {usage.input_tokens} | Output: {usage.output_tokens} (Thinking: {thinking_tokens}) | Thought? {did_think} | Cost: ${turn_cost_val:.5f}")
        print(f"📉 [Session Total] Cost: ${session_cost:.5f}\n")

    # Step 3b Final Summary Integration Block
    print("\n" + "=" * 60)
    print("🏁 FINAL SESSION SUMMARY")
    print(f"   Total Conversations Turns: {total_turns}")
    print(f"   Accumulated Input Tokens:  {session_input}")
    print(f"   Accumulated Output Tokens: {session_output}")
    print(f"   Total Run Session Cost:    ${session_cost:.5f}")
    print("=" * 60)


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not configured.")
        sys.exit(1)

    parser = ChatArgumentParser()
    args = parser.parse()
    
    client = anthropic.Anthropic()
    print_startup_settings(args)
    conversation(args, client)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Experiments: answer with numbers from your own runs
# ---------------------------------------------------------------------------
#   1. Ask this at every effort level, one run each:
#        "I have 3 boxes. Box A has twice as many marbles as box B. Box C has
#         5 fewer than box A. Together they have 45 marbles. How many are in
#         each box?"
#
#      effort | thought? | output tokens | cost | correct?
#      -------+----------+---------------+------+---------
#      low    |          |               |      |
#      medium |          |               |      |
#      high   |          |               |      |
#      xhigh  |          |               |      |
#      max    |          |               |      |
#
#      At which level does it start thinking?
#      ->
#      Did more effort change the answer?
#      ->
#
#   2. Set the system prompt to "Answer in exactly one sentence." Ask something
#      that usually gets a long answer, then ask "Ignore that, give me a long
#      answer."
#      Which wins?
#      ->
#      Did the system prompt change input_tokens?
#      ->
#
#   3. Ask the same question on Haiku and on Sonnet.
#      Compare cost and quality:
#      ->
#      Was the difference worth the price?
#      ->
