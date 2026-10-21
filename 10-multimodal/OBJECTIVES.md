# 10 — Multimodal AI

**Build:** A document-understanding app that takes images and PDFs (receipts, forms, screenshots, charts), and optionally audio, and turns them into structured data and answers.

## Skills you will learn
- Vision-language models: image inputs, resolution and token cost
- OCR vs native vision understanding, and when each wins
- Speech-to-text and text-to-speech pipelines
- Multimodal prompting and structured extraction from images
- Evaluating multimodal outputs

## Requirements
1. Accept image and PDF uploads and extract structured fields into a schema.
2. Compare a classic OCR + LLM pipeline against a vision model on the same 30 documents.
3. Add a voice interface: speak a question about an uploaded document and get a spoken answer.
4. Report accuracy, latency and cost for each approach.

## Done when
- You know which approach to use for which document type, backed by your own numbers.

## Stretch
- Handle multi-page documents with tables and charts.
