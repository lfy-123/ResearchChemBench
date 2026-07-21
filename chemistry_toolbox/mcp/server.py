"""Unified FastMCP server exposing the complete atomic chemistry toolbox."""

from __future__ import annotations

import argparse
import logging
import os
import sys

from mcp.server.fastmcp import FastMCP

from researchchem_toolbox.catalog import agent_toolbox_overview

from .registry import load_tool_config, register_all_tools, register_catalog_resources
from .software_catalog import open_execution_prompt
from .workspace import workspace_root


def create_server(profile: str | None = None) -> FastMCP:
    """Create one full-catalog server; profile is accepted only for old callers."""

    del profile
    config = load_tool_config()
    server = FastMCP(
        name=str(config.get("server_name", "ResearchChem Atomic Chemistry Toolbox")),
        instructions=agent_toolbox_overview(include_health=True) + open_execution_prompt(),
    )
    register_all_tools(server)
    register_catalog_resources(server)
    return server


mcp = create_server()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable_http"],
        default="stdio",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9010)
    parser.add_argument(
        "--profile",
        default=None,
        help="Deprecated and ignored: profiles are backend runtimes, not tool filters.",
    )
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
