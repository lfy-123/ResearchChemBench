"""FastMCP server assembled from enabled, automatically discovered tool files."""

from __future__ import annotations

import argparse
import logging
import os
import sys

from mcp.server.fastmcp import FastMCP

from .registry import load_tool_config, register_all_tools
from .profiles import PROFILE_ENV, apply_profile, get_profile, profile_names
from .workspace import workspace_root


def create_server(profile: str | None = None) -> FastMCP:
    config = load_tool_config()
    selected = profile or os.environ.get(PROFILE_ENV, "").strip() or None
    profile_config = apply_profile(selected) if selected else None
    server = FastMCP(
        name=str(
            profile_config.get("server_name")
            if profile_config
            else config.get("server_name", "ResearchChem Chemistry Tools")
        ),
        instructions=str(
            profile_config.get("description")
            if profile_config
            else config.get("server_instructions", "")
        ),
    )
    register_all_tools(server)
    return server


def _profile_from_argv() -> str | None:
    try:
        index = sys.argv.index("--profile")
    except ValueError:
        return None
    return sys.argv[index + 1] if index + 1 < len(sys.argv) else None


mcp = create_server(_profile_from_argv())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable_http"],
        default="stdio",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9010)
    parser.add_argument("--profile", choices=profile_names())
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    root = workspace_root()
    os.environ.setdefault("CHEMGRAPH_LOG_DIR", str(root / "tool_logs"))
    os.chdir(root)
    server = mcp
    if args.transport == "streamable_http":
        import uvicorn

        uvicorn.run(server.streamable_http_app(), host=args.host, port=args.port)
    else:
        server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
