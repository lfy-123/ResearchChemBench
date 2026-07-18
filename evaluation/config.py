"""Paths, environment variables, and agent presets for ResearchChemBench."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / "config.local.env", override=False)
# Backward compatibility for the original ResearchClawBench-style location.
load_dotenv(Path(__file__).parent / ".env", override=False)

TASKS_DIR = Path(os.environ.get("RESEARCHCHEMBENCH_TASKS_DIR", PROJECT_ROOT / "tasks")).resolve()
WORKSPACES_DIR = Path(
    os.environ.get("RESEARCHCHEMBENCH_WORKSPACES_DIR", PROJECT_ROOT / "workspaces")
).resolve()
WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)

CHEMGRAPH_ROOT = Path(
    os.environ.get("CHEMGRAPH_ROOT", PROJECT_ROOT.parent / "ChemGraph")
).resolve()
CHEMGRAPH_SRC = CHEMGRAPH_ROOT / "src"
CHEMGRAPH_PYTHON = os.environ.get("CHEMGRAPH_PYTHON", sys.executable)

JUDGE_MODEL_NAME = os.environ.get("JUDGE_MODEL_NAME", "")
JUDGE_API_BASE = os.environ.get("JUDGE_API_BASE", "")
JUDGE_API_KEY = os.environ.get("JUDGE_API_KEY", "")

DEFAULT_AGENT_TIMEOUT_SECONDS = int(
    os.environ.get("RESEARCHCHEMBENCH_AGENT_TIMEOUT_SECONDS", "7200")
)
DEFAULT_MAX_TURNS = int(os.environ.get("RESEARCHCHEMBENCH_MAX_TURNS", "200"))
OPENCODE_MODEL = os.environ.get(
    "RESEARCHCHEMBENCH_OPENCODE_MODEL", "deepseek/deepseek-v4-flash"
)
OPENCODE_BASE_URL = os.environ.get(
    "RESEARCHCHEMBENCH_OPENCODE_BASE_URL", "https://api.deepseek.com/v1"
)

_agents_path = Path(__file__).parent / "agents.json"
try:
    with _agents_path.open("r", encoding="utf-8") as _f:
        AGENT_PRESETS = json.load(_f)
except (FileNotFoundError, json.JSONDecodeError) as exc:
    print(f"Warning: failed to load agents.json: {exc}")
    AGENT_PRESETS = {}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}
MAX_PREVIEW_BYTES = 100_000


def chemistry_server_command() -> list[str]:
    """Return the command used to start the benchmark stdio MCP server."""

    specs = chemistry_server_specs()
    return list(specs[0]["command"])


def chemistry_server_specs() -> list[dict]:
    """Return the one full-catalog MCP server; profiles are backend workers only."""

    from evaluation.mcp_tools.profiles import public_server_spec, selected_profile_names

    configured = os.environ.get("RESEARCHCHEMBENCH_MCP_PROFILES", "").strip()
    if configured:
        # Retained only as an installation/probe selection compatibility check.
        selected_profile_names(configured)
    return [public_server_spec()]
