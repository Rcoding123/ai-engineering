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

from anthropic import Anthropic
import time

client = Anthropic()

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 4000

event_types = []

start = time.perf_counter()
first_text_time = None

with client.messages.stream(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[
        {
            "role": "user",
            "content": "Can you think of a science book which influenced many scientisits and write a 400 word summary on the advantages of that book?",
        }
    ],
) as stream:
    for event in stream:
        event_types.append(event.type)
        # Content block
        if event.type == "content_block_start":
            print(f"\nBlock start: {event.content_block.type}")
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                if first_text_time is None:
                    first_text_time = time.perf_counter()
                print(event.delta.text, end="", flush=True)

    end_time = time.perf_counter()
    final_message = stream.get_final_message()

print("\n")

# Every event, in the order it arrived
for event_type in event_types:
    print(f"Event type: {event_type}")

# Final message
print(f"Stop reason: {final_message.stop_reason}")
print(f"Input tokens: {final_message.usage.input_tokens}")
print(f"Output tokens: {final_message.usage.output_tokens}")

# Latency
ttft = first_text_time - start
total = end_time - start
print(f"TTFT: {ttft:.2f}s")
print(f"Total: {total:.2f}s")


# Experiment 1: event types in the order they arrived
#   message_start
#   content_block_start             (thinking block)
#   content_block_delta + thinking  (repeats)
#   signature
#   content_block_stop
#   content_block_start             (text block)
#   content_block_delta + text      (repeats)
#   content_block_stop
#   message_delta
#   message_stop
#   Once: message_start, signature, message_delta, message_stop.
#   Once per block (2 here): content_block_start, content_block_stop.
#   Many times: content_block_delta (287), text (154), thinking (132).
#   154 text + 132 thinking + 1 signature = 287 deltas. text and thinking are
#   SDK helper events, so each piece shows up twice in the list.
#
# Experiment 2: same prompt three times
#   run    | TTFT  | total
#    1     | 8.06s | 10.45s
#    2     | 8.12s | 10.07s
#    3     | 8.23s | 10.65s
#   spread | 0.17s |  0.58s
#   Total varied more, about 3x as much as TTFT. Only 3 runs, so a rough result.
#
# Experiment 3: one-line vs long answer, three runs each
#   prompt   | TTFT        | total        | after first text | output tokens
#   one line | 0.41-0.54s  | 0.64-0.78s   | about 0.24s      | 45-47
#   long     | 2.31-6.54s  | 8.75-13.67s  | 6.34-7.14s       | 1663-2739
#   Both changed, for different reasons. Total grew because a longer answer
#   takes longer to write. TTFT grew because of thinking, not answer length:
#   the one-line runs had no thinking block, the long runs thought first.
#   Not tested: TTFT with thinking off. My guess is it would barely change.
#   The amount of thinking changes between runs, so TTFT on the long prompt
#   ranged from 2.31s to 6.54s. The user sees nothing during that wait unless
#   you show the thinking.
