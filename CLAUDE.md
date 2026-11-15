# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the game
uv run dungeon-game

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/path/to/test_file.py::test_name

# Lint / format
uv run ruff check .
uv run ruff format .
```

## Architecture

This is a Python project managed with `uv`. Source code lives in `src/dungeon_game/` with a single entry point: `dungeon_game:main` (called via the `dungeon-game` CLI script).

The project is currently a skeleton — `src/dungeon_game/__init__.py` contains only the `main()` function.
