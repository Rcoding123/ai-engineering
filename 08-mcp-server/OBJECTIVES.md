# 08 — Model Context Protocol (MCP) Server

**Build:** An MCP server that exposes a real system (your notes, a database, an issue tracker, or your RAG index) to any MCP-compatible AI client.

## Skills you will learn
- The MCP architecture: hosts, clients and servers
- Exposing tools, resources and prompts
- Transports (stdio vs HTTP)
- Auth and permission boundaries for AI-accessible systems
- Designing tool surfaces for models rather than humans

## Requirements
1. The server exposes at least three tools and one resource.
2. It works locally over stdio with an existing MCP client (e.g. Claude Code or Claude Desktop).
3. Every tool has input validation and clear error messages.
4. At least one write tool, with explicit guardrails.
5. Automated tests for each tool.

## Done when
- You can connect it to an AI client and complete a real task end to end using only your server's tools.

## Stretch
- Deploy it remotely over HTTP with authentication.
