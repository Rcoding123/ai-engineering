"""
Project 01 · Step 7 (stretch) — Prompt caching

Objective:
Long chats re-send the same prefix (system prompt + old turns) every turn.
Use the API's prompt caching so that repeated prefix is billed at the cheaper
cache-read rate, and measure the savings.

Requirements:
  - Enable prompt caching in your chat so the conversation history is cached
    between turns.
  - Use a system prompt long enough to be cacheable (check the minimum
    cacheable length for your model in the docs).
  - Each turn's stats line shows: tokens written to cache, tokens read from
    cache, uncached input tokens.
  - Cost calculation accounts for cache writes and cache reads at their own
    prices (look them up for your model).

Done when:
  - From turn 2 onward, most input tokens are cache reads, and your cost
    numbers show the saving.

Experiments (answer as comments at the bottom of this file):
  1. Run the same 10-turn chat with and without caching. Compare total cost
     and the time to first token.
  2. Put the current date and time inside the system prompt. What happens to
     cache reads, and why?
  3. Wait longer than the cache lifetime between two turns. What happens?
"""
