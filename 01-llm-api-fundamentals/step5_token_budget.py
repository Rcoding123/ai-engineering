"""
Project 01 · Step 5 — Token budget: trim or summarize old history

Objective:
Extend your step 4 chat so the conversation never grows past a token budget
you choose. Long chats get expensive (and eventually stop fitting the model);
this step keeps the cost per turn bounded.

Requirements:
  - A configurable token budget for the history sent to the model. Use a
    small value while testing (around 1,500 tokens) so you hit it quickly.
  - Before each call, know how many input tokens the request will use. Use an
    exact count from the API, not a characters-divided-by-4 estimate.
  - When the request would exceed the budget, reduce the history using one of
    two strategies, chosen when the program starts:
      a) trim:      drop the oldest turns
      b) summarize: replace the oldest turns with a short model-written
                    summary of them
  - Never break a turn apart: a user message and the assistant reply to it
    are removed or summarized together. The history sent must still start
    with a user message.
  - The system prompt is never trimmed or summarized.
  - Every time the history is reduced, print one line saying which strategy
    ran and the token count before and after.
  - The cost of any summarizing call counts toward the turn and session cost.

Done when:
  - A 15-turn chat with a 1,500-token budget never sends more than the budget,
    and the stats lines prove it.

Experiments (answer as comments at the bottom of this file):
  1. Tell the chat your name in turn 1, chat about other things for 12+ turns,
     then ask your name. Do this once with trim and once with summarize.
     Which one remembered? Why?
  2. Compare total session cost for the same 15-turn conversation with
     no budget, trim, and summarize. Which is cheapest, and why is summarize
     not free?
  3. How did the per-turn input tokens behave once the budget kicked in,
     compared with the linear growth you saw in step 2?
"""
