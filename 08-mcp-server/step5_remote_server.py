"""
Project 08 · Step 5 (stretch) — Remote server with authentication

Objective:
Run your server over HTTP so clients on other machines can use it, and keep
strangers out.

Requirements:
  - HTTP transport instead of stdio.
  - Authentication: requests without valid credentials are rejected.
  - Deployed somewhere reachable (or a tunnel for testing).

Done when:
  - A client connects remotely with credentials, and a request without them fails.

Questions (answer as comments at the bottom of this file):
  1. What new risks appear once the server is on the internet?
"""
