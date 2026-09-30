#!/usr/bin/env python3
"""Compatibility entry point for the installed evaluation run controller."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.execution.control import main, refresh_batch

if __name__ == "__main__":
    raise SystemExit(main())
