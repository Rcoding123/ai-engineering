# 03 — Evaluation

**Build:** A reusable evaluation harness, applied first to your Project 02 pipeline.

## Skills you will learn
- Why "it looks good" is not an eval, and how to build golden datasets
- Deterministic metrics (exact match, field-level precision/recall, F1)
- LLM-as-judge with rubrics, and checking the judge against human labels
- Regression testing prompts and models
- Reading eval results: error analysis, slicing by category

## Requirements
1. Hand-label a golden set of at least 40 examples, including hard edge cases.
2. The harness runs any pipeline on any dataset and outputs per-example and aggregate scores.
3. At least two deterministic metrics and one LLM-as-judge metric with a written rubric.
4. Measure the judge's agreement with your own labels on 20+ examples.
5. Store each run's results so two runs can be diffed (what improved, what regressed).
6. One command runs the full eval.

## Done when
- You change a prompt or model, run the eval, and can say with evidence whether it got better, and where it got worse.

## Stretch
- Run evals in CI on every prompt change.
- Track cost and latency per run alongside quality.
