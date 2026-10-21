# 06 — Tool Use / Function Calling

**Build:** An assistant that answers questions by calling real tools, e.g. a calculator, a weather or finance API, a SQL database, and your Project 05 RAG search.

## Skills you will learn
- Defining tools: names, descriptions and input schemas the model can use well
- The tool-call loop: the model requests a call, you execute it, return the result, and the model continues
- Parallel tool calls
- Handling tool errors and bad arguments gracefully
- Safety: validating inputs, read-only vs side-effecting tools, confirmation for risky actions

## Requirements
1. Implement the tool-use loop yourself with the raw SDK (no agent framework).
2. Provide at least four tools, including one that queries a SQL database.
3. Validate tool arguments before execution and return structured errors to the model.
4. Any tool with side effects requires user confirmation.
5. Log every tool call with its arguments, result and latency.
6. Write 20 test questions and measure how often the right tools are chosen.

## Done when
- You can explain why the model picked (or failed to pick) a tool, and fix it by improving the tool descriptions.

## Stretch
- Rebuild it with a framework and compare what you gained and lost.
