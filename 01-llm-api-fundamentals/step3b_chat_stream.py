"""
Project 01 · Step 3b — A chat that streams

Objective:
Build the step 2 chat again, but every reply appears word by word as it is
generated, instead of all at once at the end.

Requirements:
  - Everything from step 2 still works: memory, quit, empty-input skip,
    max_tokens warning, per-turn stats line, session summary on quit.
  - Each reply is printed piece by piece as it streams, flushed immediately.
  - Usage, stop_reason and the content saved to the history all come from
    the final message, once the stream has finished.

Experiments (answer as comments at the bottom of this file):
  1. Ask for a long answer here and in step 2. Which feels faster? Did the
     total time actually change?
  2. Have the same three-turn conversation here and in step 2. Compare the
     token counts and the cost. Does streaming cost more?
"""
