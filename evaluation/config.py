"""Paths, environment variables, and agent presets for ResearchChemBench."""

from __future__ import annotations

import json
import os
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

JUDGE_MODEL_NAME = os.environ.get("JUDGE_MODEL_NAME", "")
JUDGE_API_BASE = os.environ.get("JUDGE_API_BASE", "")
JUDGE_API_KEY = os.environ.get("JUDGE_API_KEY", "")

DEFAULT_AGENT_TIMEOUT_SECONDS = int(
    os.environ.get("RESEARCHCHEMBENCH_AGENT_TIMEOUT_SECONDS", "14400")
)
DEFAULT_MCP_TOOL_TIMEOUT_MS = int(
    # Keep the client deadline beyond the toolbox's 7200 s synchronous ORCA
    # ceiling so a valid backend result is not misreported as a client timeout.
    os.environ.get("RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS", "7500000")
)
DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS = int(
    os.environ.get("RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS", "7200")
)
DEFAULT_FAST_ACTION_TIMEOUT_SECONDS = int(
    os.environ.get("RESEARCHCHEMBENCH_FAST_ACTION_TIMEOUT_SECONDS", "60")
)
DEFAULT_AVAILABLE_CPU_CORES = int(
    os.environ.get("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "48")
)
DEFAULT_AVAILABLE_MEMORY_MB = int(
    os.environ.get("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "204800")
)
DEFAULT_AVAILABLE_GPU_COUNT = int(
    os.environ.get("RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT", "0")
)
DEFAULT_MAX_TURNS = int(os.environ.get("RESEARCHCHEMBENCH_MAX_TURNS", "200"))
DEFAULT_LIVE_PROGRESS = os.environ.get(
    "RESEARCHCHEMBENCH_LIVE_PROGRESS", "1"
).strip().casefold() not in {"0", "false", "no", "off"}
DEFAULT_PROGRESS_CONSOLE = os.environ.get(
    "RESEARCHCHEMBENCH_PROGRESS_CONSOLE", "0"
).strip().casefold() not in {"0", "false", "no", "off"}
DEFAULT_PROGRESS_MAX_CHARS = max(
    80, int(os.environ.get("RESEARCHCHEMBENCH_PROGRESS_MAX_CHARS", "600"))
)
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


def chemistry_server_specs(discovery_mode: str | None = None) -> list[dict]:
    """Return one server over the complete catalog; only its discovery surface varies."""

    from chemistry_toolbox.mcp.profiles import public_server_spec, selected_profile_names

    configured = os.environ.get("RESEARCHCHEMBENCH_MCP_PROFILES", "").strip()
    if configured:
        # Retained only as an installation/probe selection compatibility check.
        selected_profile_names(configured)
    return [public_server_spec(discovery_mode)]
