# 11 — Production & LLMOps

**Build:** Take one earlier project (RAG or the agent is recommended) and ship it as a production-grade web service.

## Skills you will learn
- Serving LLM features behind an API (e.g. FastAPI) with streaming
- Observability: tracing, logging prompts and responses, dashboards
- Caching: response caching, prompt caching, semantic caching
- Cost and latency optimization, and model routing (cheap model first, escalate when needed)
- Guardrails: prompt-injection defense, PII handling, output filtering, content moderation
- Rate limiting, fallbacks between providers, graceful degradation
- Containerization and deployment, with evals as a CI gate

## Requirements
1. A containerized API service deployed to a cloud host.
2. Full request tracing with token counts, latency and cost per request.
3. At least one caching layer with a measured hit rate and savings.
4. A prompt-injection test suite of 20+ attacks, documenting what is blocked.
5. Provider fallback when the primary model fails.
6. A CI pipeline that runs your eval suite and blocks deploys on regression.
7. A load test reporting p50/p95 latency and cost per 1,000 requests.

## Done when
- Someone else can use your service, and you can answer: how much does it cost, how fast is it, and how do we know it is still working?

## Stretch
- A/B test two prompts or models in production with real traffic.
