# 02 — Prompt Engineering & Structured Outputs

**Build:** An extraction pipeline that turns messy unstructured text (job posts, invoices or emails) into validated JSON records.

## Skills you will learn
- Prompt design: clear instructions, delimiters, few-shot examples, role framing
- Getting reliable structured output (JSON schema / tool-based extraction)
- Validating outputs with a schema library (e.g. Pydantic or Zod)
- Repair loops: re-prompting with the validation error
- Versioning prompts and comparing prompt variants

## Requirements
1. Define a schema with required, optional, enum and nested fields.
2. Process a folder of at least 50 real-world raw documents.
3. Validate every output against the schema; an invalid output triggers one automatic repair attempt.
4. Log failures with the input, raw output and error.
5. Keep at least three prompt versions in files and record the success rate of each.

## Done when
- The pipeline produces valid records for at least 95% of inputs, and you can show which prompt change moved the number.

## Stretch
- Batch processing with concurrency limits.
- Classify each document before extraction and route it to a type-specific prompt.
