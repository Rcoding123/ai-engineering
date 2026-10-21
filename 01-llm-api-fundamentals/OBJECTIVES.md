# 01 — LLM API Fundamentals

**Build:** A command-line chat assistant that talks to an LLM API directly (no frameworks).

## Skills you will learn
- Calling a model API with the raw SDK: messages, roles, system prompts
- Tokens and context windows, and how they drive cost and latency
- Sampling parameters (temperature, max tokens, stop sequences) and their effect
- Streaming responses
- Error handling: rate limits, timeouts, retries with exponential backoff
- Managing API keys safely (env vars, never in code)

## Requirements
1. Multi-turn chat in the terminal that keeps conversation history.
2. Streams tokens to the screen as they arrive.
3. Configurable system prompt, model and temperature via CLI flags.
4. Prints token usage and estimated cost after every turn, plus a session total.
5. Trims or summarizes old history when it nears a token budget you set.
6. Retries transient failures with backoff; fails clearly on permanent ones.

## Done when
- You can explain what happens to cost and quality when you change model, temperature and history length, using numbers from your own runs.

## Stretch
- Support two providers behind one interface and compare them on the same prompts.
- Add prompt caching and measure the cost and latency difference.
