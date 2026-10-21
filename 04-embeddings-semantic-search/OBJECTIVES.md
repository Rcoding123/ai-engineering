# 04 — Embeddings & Semantic Search

**Build:** A semantic search engine over a corpus you care about (notes, papers, docs, support tickets).

## Skills you will learn
- What embeddings are and how similarity (cosine / dot product) works
- Choosing an embedding model: dimensions, cost, batching
- Vector storage: brute-force numpy first, then a vector index or database (FAISS, pgvector, Chroma, etc.)
- Keyword search (BM25) vs semantic search vs hybrid
- Retrieval metrics: recall@k, MRR

## Requirements
1. Embed a corpus of at least 1,000 items and persist the vectors.
2. Implement search with plain numpy first, then with a vector index, and compare speed.
3. Implement BM25 keyword search and a hybrid of both.
4. Build a query set of 30+ queries with known relevant results.
5. Report recall@5 and MRR for keyword, semantic and hybrid search.

## Done when
- You can show, with metrics, when semantic search beats keyword search and when it does not.

## Stretch
- Compare two embedding models on your query set.
- Visualize the embedding space (UMAP or t-SNE) and explain the clusters.
