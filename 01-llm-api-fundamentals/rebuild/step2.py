"""
Rebuild — Step 2: A chat that remembers

Objective:
Turn the single call from step 1 into a terminal chat loop with claude-haiku-5-5
that keeps the whole conversation history and sends it with every call, so
Claude remembers earlier turns. Typing quit or exit ends the chat. After every
turn, print that turn's input/output tokens and cost plus the running session
total; when the chat ends, print the number of turns and the total cost.
"""
