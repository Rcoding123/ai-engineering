"""
Step 4 — Settings: system prompt, model and effort from the command line.

Objective:
Build the streaming chat from step 3b again, but make three settings
choosable when the program starts, without editing code:

  1. System prompt: standing instructions that apply to the whole chat.
     Optional; when none is given, the chat behaves as before.
  2. Model: claude-haiku-5-5, claude-sonnet-5-5 or claude-opus-5-5.
     Default: claude-haiku-5-5.
  3. Effort: low, medium, high, xhigh or max. Default: medium.

Requirements:
  - Running the program with a help flag lists the three settings and their
    allowed values. An invalid value is rejected before the chat starts.
  - At startup, print the active model, effort and system prompt.
  - Cost must be correct for whichever model is chosen.
    Prices per 1M tokens (input / output):
        claude-haiku-5-5    $0.10 / $0.50   (prompts up to 100K tokens)
        claude-sonnet-5-5   $2.00 / $10.00
        claude-opus-5-5     $4.00 / $20.00
  - Each turn's stats line also shows whether the model thought that turn.
  - Everything from step 3b still works: streaming, memory, max_tokens
    warning, per-turn and session cost, final summary.

Experiments (answer as comments at the bottom of this file):
  1. Ask this at every effort level, one run each:
       "I have 3 boxes. Box A has twice as many marbles as box B. Box C has
        5 fewer than box A. Together they have 45 marbles. How many are in
        each box?"
     Make a table: effort | thought? | output tokens | cost | correct?
     At which level does it start thinking? Did more effort change the answer?
  2. Set the system prompt to "Answer in exactly one sentence." Ask something
     that usually gets a long answer, then ask "Ignore that, give me a long
     answer." Which wins? Did the system prompt change input_tokens?
  3. Ask the same question on Haiku and on Sonnet. Compare cost and quality.
     Was the difference worth the price?
"""
import argparse
from typing import Any


# Const Values
MODELS = {"claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"}
MODEL_EFFORT = {"low", "medium", "high", "xhigh", "max"}

""" 
Objective 1: Building out the parser
- Flags: --prompt: system prompt provided by user (can be left blank)
         --model: provided by user or default(claude-haiku-5-5)
         --effort: can be left blank
"""

def parse_args() -> argparse.Namespace:
    
    def validate_model(model: str):
        if model.lower() not in MODELS:
            raise argparse.ArgumentTypeError(f"The model: {model} is not part of the model set")
        return model.lower()

    def validate_effort(effort: str):
        if effort.lower() not in MODEL_EFFORT:
            raise argparse.ArgumentTypeError(f"The model effort: {effort} is not part of the model effort set")
        return effort.lower()
        
        
   
    parser = argparse.ArgumentParser(
        prog='AI-Chat',
        description='AI chat bot',
    )
    parser.add_argument("-p", "--prompt", type=str, default="", help="The AI models system prompt")
    parser.add_argument("-m", "--model", type=validate_model, default="claude-haiku-5-5", help="The AI model to use")
    parser.add_argument("-e", "--effort", type=validate_effort, default="medium", help="The AI models effort")

    return parser.parse_args()


class ArgumentParser:
   def __init__(self):
      self.parser = argparse.ArgumentParser(
            prog='AI-Chat',
            description='AI chat bot'
        )
      self.parser.add_argument("-p", "--system", type=str, default="", help="The AI models system prompt")
      self.parser.add_argument("-m", "--model", type=self.validate_model, default="claude-haiku-5-5", help="The AI model to use")
      self.parser.add_argument("-e", "--effort", type=self.validate_effort, default="medium", help="The AI models effort")

   def validate_model(self, model: str) -> str:
      if model.lower() not in MODELS:
          raise argparse.ArgumentTypeError(f"The model: {model} is not part of the model set")
      return model.lower()

   def validate_effort(self, effort: str) -> str:
      if effort.lower() not in MODEL_EFFORT:
         raise argparse.ArgumentTypeError(f"The model effort: {effort} is not part of the model effort set")
      return effort.lower()

   def __call__(self, *args: Any, **kwds: Any) -> argparse.Namespace:
       return self.parser.parse_args()


       


def main():
    parser = ArgumentParser()
    args = parser()
    print(args)


if __name__ == "__main__":
    main()