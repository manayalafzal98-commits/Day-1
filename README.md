# day1-starter

Glosix Agentic AI Developer Internship, Week 1 Day 1.

A small typed Python project that checks your workstation is ready
(Python 3.12+, Git, uv, Git identity, plus optional Docker, Ollama, VS Code, gh).
It also shows the Week 1 habits: a `uv` project, type hints, dataclasses,
`.env` kept out of Git, and pytest tests.

## Run it

```bash
uv sync                 # create .venv and install dev tools
uv run setup-check      # prints OK / FAIL / TODO for each tool
uv run pytest           # 9 tests should pass
```

`FAIL` means a required tool is missing. `TODO` items are optional today
but needed later in the program (Docker in Week 10, Ollama in Week 2).

## Secrets

Copy `.env.example` to `.env` and put API keys there. `.env` is in
`.gitignore`, so it is never committed.
