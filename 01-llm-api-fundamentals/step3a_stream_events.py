"""
Step 3a — Look inside a stream.

Goal: see the raw events a streaming response is made of, and measure the
two latency numbers that matter in a chat app:
    TTFT  (time to first token)  -> how long the user stares at nothing
    total (time to last token)   -> how long the whole answer takes

Run it with:
    python 01-llm-api-fundamentals/step3a_stream_events.py
"""

import time

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"
client = anthropic.Anthropic()

# Haiku answers EASY straight away, but thinks before answering HARD.
# Run the script once with each and compare.
EASY = "Explain in one paragraph why the sky is blue, then give a one-line summary."
HARD = (
    "I have 3 boxes. Box A has twice as many marbles as box B. Box C has 5 fewer "
    "than box A. Together they have 45 marbles. How many are in each box?"
)
PROMPT = HARD

start = time.perf_counter()
first_token_at = None

# client.messages.stream(...) takes the SAME arguments as messages.create(),
# but returns a context manager. Inside the `with`, the HTTP connection stays
# open and events arrive one by one.
with client.messages.stream(
    model=MODEL,
    max_tokens=4000,
    # Ask for a readable summary of the thinking, so thinking deltas carry text.
    # (By default thinking streams with empty text.)
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[{"role": "user", "content": PROMPT}],
) as stream:
    for event in stream:
        # TODO 1: Print event.type for EVERY event, one per line.
        #         Run it once like that and look at the order of events.
        #         Heads-up: besides the API's own events (message_start,
        #         content_block_delta, ...), the SDK adds convenience events
        #         named "text", "thinking" and "signature" that repeat the
        #         same data. Which ones are real API events? (See the
        #         "Stream Event Types" table in the Anthropic streaming docs.)
        # print(f"Event type: {event.type}")

        # TODO 2: When event.type == "content_block_start", print which kind of
        #         block is starting: event.content_block.type
        if event.type == "content_block_start":
            print(f"Event content block type: {event.content_block.type}")

        # TODO 3: When event.type == "content_block_delta", look at event.delta.type:
        #         - "thinking_delta" -> the new text is in event.delta.thinking
        #         - "text_delta"     -> the new text is in event.delta.text
        #         - "signature_delta" -> a checksum that seals the thinking
        #                               block; nothing to print, just skip it
        #         Print the new text with print(..., end="", flush=True)
        #         (Then remove the TODO 1 print — it makes this unreadable.)
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(f"{event.delta.thinking}", end="", flush=True)
            elif event.delta.type == "text_delta":
                print(f"{event.delta.text}", end="", flush=True)

                if first_token_at is None:
                                    first_token_at = time.perf_counter()

        # TODO 4: The first time you see a "text_delta", record
        #         first_token_at = time.perf_counter()


    # After the loop, the SDK has assembled the full response for you.
    # It's the same Message object messages.create() returns.
    final = stream.get_final_message()

end = time.perf_counter()

# TODO 5: Print:
#   - TTFT in seconds (first_token_at - start)
#   - total time in seconds (end - start)
#   - final.stop_reason, final.usage.input_tokens, final.usage.output_tokens
print(f"First token at: {first_token_at - start}")
print(f"Total time: {end - start}")
print(f"Final stop: {final.stop_reason} | Final usage (input): {final.usage.input_tokens} | Final usage (output): {final.usage.output_tokens}")

# QUESTIONS
#   1. In what order do the event types arrive? Which ones appear once,
#      and which appear many times?
#      -> message_start                      once, at the beginning
#         then for EACH content block (thinking, then text):
#             content_block_start            once per block
#             content_block_delta            many times (the actual pieces)
#             content_block_stop             once per block
#         message_delta                      once: stop_reason + final usage
#         message_stop                       once, at the end
#         The "text", "thinking" and "signature" events are NOT from the API.
#         The SDK adds them as shortcuts that repeat the delta data (a raw curl
#         call shows only the API events, plus "ping" keep-alives).
#
#   2. Does thinking stream before or after the text? What does that mean for
#      TTFT on a hard question vs an easy one?
#      -> Before. The thinking block always comes first, so no answer text can
#         arrive until thinking is finished. Measured on Haiku 5.5 (2 runs each):
#           EASY (no thinking):  first text 0.47-0.67s, total 1.61-1.97s
#           HARD (thinks first): first text 1.63-1.94s, total 1.64-1.95s
#         On HARD, nothing at all arrived for ~1.6-1.9s, then the thinking
#         summary and the answer came in one burst. A hard question can
#         triple TTFT, and the user sees a frozen screen while the model thinks.
#
#   3. Is TTFT or total time the number a chat user "feels"? Why does
#      streaming improve one of them but not the other?
#      -> TTFT. The wait before anything appears is what feels slow; once text
#         is flowing, people read along. Streaming only changes delivery: the
#         first pieces are sent as soon as they exist. The model generates at
#         the same speed either way, so total time stays about the same.
