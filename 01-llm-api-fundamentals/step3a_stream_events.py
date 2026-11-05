"""
Project 01 · Step 3a — Look inside a stream

Objective:
Make one streaming call and look at the raw events a streamed response is
made of. Measure the two latency numbers that matter in a chat app:
    TTFT  (time to first token): how long the user stares at nothing
    total (time to last token):  how long the whole answer takes

Requirements:
  - One streaming call with a prompt that produces a few paragraphs.
  - Print the type of every event, one per line.
  - When a content block starts, print which kind of block it is.
  - As deltas arrive, print the thinking and the text as one continuous flow
    (no newline between pieces, flushed immediately).
  - Record the time of the first text delta and the time the stream ends,
    measured from just before the call.
  - After the stream ends, get the final message and print its stop_reason,
    input tokens and output tokens.
  - Print TTFT and total time in seconds, to 2 decimal places.

Experiments (answer as comments at the bottom of this file):
  1. List the event types in the order they arrived. Which appear once, and
     which appear many times?
  2. Run it three times and write down TTFT and total each time. Which of
     the two varies more?
  3. Ask for a one-line answer, then a long one. Does TTFT change? Does total?
"""
