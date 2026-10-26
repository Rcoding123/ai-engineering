# AI Engineering

A 12-project path from raw LLM API calls to shipping a production AI product, written in Python against the Anthropic SDK.

Each project is broken into steps. Each step file starts with only the objective, the requirements and a "done when" check. There is no starter code. I write the implementation, run it, and answer the step's experiments at the bottom of the file with numbers from my own runs.

## Projects

| # | Project | What gets built | Status |
|---|---------|-----------------|--------|
| 01 | [LLM API Fundamentals](01-llm-api-fundamentals/) | Command-line streaming chat assistant on the raw SDK, with no frameworks | In progress (steps 1–3 done, step 4 underway) |
| 02 | [Structured Outputs](02-structured-outputs/) | Pipeline that turns messy text into validated JSON records | Planned |
| 03 | [Evaluation](03-evals/) | Reusable eval harness with metrics and an LLM judge | Planned |
| 04 | [Embeddings & Semantic Search](04-embeddings-semantic-search/) | Semantic search engine with vector, keyword and hybrid retrieval | Planned |
| 05 | [RAG](05-rag/) | Question answering over documents, with citations | Planned |
| 06 | [Tool Use](06-tool-use/) | Assistant that calls real tools (calculator, APIs, SQL, RAG search) | Planned |
| 07 | [Agents](07-agents/) | Autonomous research agent that writes cited reports | Planned |
| 08 | [MCP Server](08-mcp-server/) | Model Context Protocol server exposing a real system to AI clients | Planned |
| 09 | [Fine-Tuning](09-fine-tuning/) | LoRA fine-tune of a small open model, compared against an API model | Planned |
| 10 | [Multimodal](10-multimodal/) | Image, PDF and audio understanding into structured data | Planned |
| 11 | [Production & LLMOps](11-production-llmops/) | An earlier project shipped as a service: observability, caching, guardrails, CI eval gate, load tests | Planned |
| 12 | [Capstone](12-capstone/) | End-to-end AI product with real users | Planned |

Each folder's `OBJECTIVES.md` lists the skills, requirements and stretch goals for that project.

## Measured so far (Project 01)

All runs use `claude-haiku-5-5`.

**Effort vs. thinking.** I asked the same marbles word problem at each effort level.
- At `low` and `medium` the model answered directly, with no thinking.
- At `high`, `xhigh` and `max` it produced a thinking block before answering.
- Output tokens rose from 91 to 160 across the levels.

**Streaming latency.** Time to first text versus total time:

| Prompt | First text | Total |
|--------|-----------:|------:|
| Easy (no thinking) | 0.47–0.67 s | 1.61–1.97 s |
| Hard (thinks first) | 1.63–1.94 s | 1.64–1.95 s |

Streaming improves what the user feels, which is time to first text, but not total time. When the model thinks first, it can triple the time to first text.

**Conversation memory cost.** The API is stateless, so every turn resends the full history.
- Input tokens per turn grow linearly with the length of the chat.
- Total tokens over a session grow quadratically.
- A long chat eventually hits the context window unless history is trimmed. Project 01, step 5 handles this.

## Repository layout

```
01-llm-api-fundamentals/
  OBJECTIVES.md        project goals
  step*_*.py           one file per step: objectives, my code, experiment answers
  rebuild/             steps 1–2 rewritten from scratch from objectives only
02-… 12-…              later projects, same structure
Agents-LangGraph/      early ReAct agent experiment, to be reworked in Project 07
notes/                 LaTeX study notes, one chapter per project (built PDF in notes/)
```

## Running it

Requires Python 3.11+ and an Anthropic API key.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install anthropic python-dotenv loguru
export ANTHROPIC_API_KEY=...     # or put it in a .env file (git-ignored)
python 01-llm-api-fundamentals/step3b_chat_stream.py
```

## Notes

Study notes for each project are kept as a LaTeX book in [`notes/latex`](notes/latex/). The compiled PDF is [`notes/AI-Engineering-Notes.pdf`](notes/AI-Engineering-Notes.pdf).
