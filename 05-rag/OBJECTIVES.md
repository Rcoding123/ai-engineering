# 05 — Retrieval-Augmented Generation (RAG)

**Build:** A question-answering assistant over a document collection that cites its sources.

## Skills you will learn
- Document ingestion: parsing PDF, HTML and Markdown, cleaning text
- Chunking strategies (fixed, recursive, semantic) and chunk-size trade-offs
- Retrieval plus reranking
- Grounded generation with citations, and refusing when the answer is not in the docs
- Evaluating RAG: retrieval quality vs answer faithfulness vs answer correctness

## Requirements
1. Ingest at least 20 real documents of mixed formats.
2. Implement at least two chunking strategies and compare them.
3. Answers cite the specific chunks used, and the citations can be checked.
4. The system says "I don't know" when retrieval finds nothing relevant.
5. Add a reranking step and measure its impact.
6. Use your Project 03 harness to evaluate retrieval recall, faithfulness and correctness on 30+ questions.

## Done when
- You can trace any wrong answer to its cause: bad chunking, bad retrieval or bad generation.

## Stretch
- Query rewriting / multi-query retrieval.
- Incremental re-indexing when documents change.
