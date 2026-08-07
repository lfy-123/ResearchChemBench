"""Backward-compatible entry point for ``python -m evaluation.cli_eval``."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
