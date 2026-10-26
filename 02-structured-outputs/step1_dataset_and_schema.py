"""
Project 02 · Step 1 — Dataset and schema

Objective:
Pick one kind of messy real-world document (job posts, invoices, recipes,
product listings, or emails) and define exactly what a correct extraction looks
like before involving any model.

Requirements:
  - Collect at least 50 real raw documents of that kind as text files in a
    data folder. Real text from the web or your own files, not model-generated.
  - Include awkward cases on purpose: missing fields, odd formats, two items
    in one document, a different language, very long and very short documents.
  - Define the target record as a schema in code with a validation library
    (e.g. Pydantic). It must include:
      * required fields and optional fields
      * at least one enum (a fixed set of allowed values)
      * at least one nested object or list of objects
      * at least one field with a format rule (date, currency, range, ...)
  - Hand-write the correct record for 3 documents and prove your schema
    accepts them, and rejects 3 deliberately broken records with clear errors.

Done when:
  - Running this file validates the 3 good and 3 bad records and prints
    what passed and why the bad ones failed.

Questions (answer as comments at the bottom of this file):
  1. Which fields did you make optional, and why?
  2. Which document in your set do you expect a model to get wrong? Why?
"""
