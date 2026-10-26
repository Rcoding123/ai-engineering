"""
Project 01 · Step 6 — Errors and retries

Objective:
Make your chat survive failures. Some errors are temporary and worth
retrying; others will never succeed and should fail immediately with a clear
message. The user should never lose their conversation because one call failed.

Requirements:
  - Turn off the SDK's built-in automatic retries and implement your own, so
    you understand what the SDK normally does for you.
  - Classify failures into:
      transient -> retry: rate limited, server overloaded, server errors (5xx),
                   connection problems, timeouts
      permanent -> do not retry: bad request, invalid API key, model not found,
                   permission denied
  - Retries use exponential backoff with jitter, a maximum number of attempts,
    and print each attempt with its wait time.
  - If the server tells you how long to wait, respect that instead of your own
    backoff.
  - On a permanent error, print a clear one-line explanation a user could act on.
  - A failed turn must not corrupt the history: the next turn must work as if
    the failed one never happened (or let the user retry the same message).
  - A failure halfway through a stream must be handled too.

Done when:
  - You can trigger each case on purpose and show the program's behavior:
      * an invalid model name
      * an invalid API key (set a fake one for that run only)
      * a very short timeout
      * a network drop (disconnect Wi-Fi mid-answer)

Experiments (answer as comments at the bottom of this file):
  1. For each trigger above: which error class did you get, and did your
     program retry or fail fast? Was that the right call?
  2. Why is jitter added to the backoff? What goes wrong with 1,000 clients
     all retrying at exactly 1s, 2s, 4s?
  3. Turn the SDK's own retries back on. What did it already handle for you,
     and what did it not?
"""
