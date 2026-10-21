# 07 — Agents

**Build:** An autonomous research agent that takes a question, plans, searches the web and reads sources, and writes a cited report.

## Skills you will learn
- Agent loops: plan, act, observe, reflect
- Context management over long tasks (summarizing, scratchpads, memory)
- Stopping conditions, step budgets and cost limits
- Multi-agent patterns: an orchestrator with sub-agents
- Agent failure modes (loops, hallucinated progress, drift) and how to detect them
- Tracing and debugging agent runs

## Requirements
1. The agent writes a plan before acting and updates it as it goes.
2. Enforce a maximum step count and maximum cost per run.
3. Keep a trace of every step (thought, action, observation) that can be viewed after the run.
4. The final report cites sources for each key claim.
5. Build one multi-agent version (e.g. an orchestrator delegating sub-questions) and compare its quality, cost and time with the single-agent version.
6. Evaluate on 10 research questions with a rubric.

## Done when
- You can read the trace of a failed run and identify exactly where and why it went wrong.

## Stretch
- Human-in-the-loop checkpoints.
- Persistent memory across runs.
