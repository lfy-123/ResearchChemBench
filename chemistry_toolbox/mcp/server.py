"""Unified FastMCP server with progressive or full chemistry-tool discovery."""

from __future__ import annotations

import argparse
import logging
import os
import sys

from .feedback_server import FeedbackFastMCP as FastMCP

from chemistry_toolbox.src.catalog import resolve_tool_discovery_mode, toolbox_overview

from .registry import load_tool_config, register_catalog_resources, register_public_tools
from .software_catalog import open_execution_prompt
from .workspace import workspace_root


def create_server(
    profile: str | None = None,
    discovery_mode: str | None = None,
    wait_only: bool = False,
) -> FastMCP:
    """Create one server over the complete catalog using the selected surface."""

    del profile
    if wait_only:
        from .open_tools import wait_execution_jobs, TOOL_DESCRIPTIONS
        from .async_action_tools import wait_execution_events
        server = FastMCP(name="ResearchChem managed waits", instructions="These calls hold until a meaningful computation event. No periodic model polling is needed.")
        server.tool(name="wait_execution_jobs", description=TOOL_DESCRIPTIONS["wait_execution_jobs"])(wait_execution_jobs)
        server.tool(name="wait_execution_events")(wait_execution_events)
        return server
    config = load_tool_config()
    mode = resolve_tool_discovery_mode(discovery_mode)
    server = FastMCP(
        name=str(config.get("server_name", "ResearchChem Atomic Chemistry Toolbox")),
        instructions=(
            toolbox_overview(
                discovery_mode=mode,
                include_health=mode == "full",
            )
            + open_execution_prompt(include_command_index=mode == "full")
        ),
    )
    register_public_tools(server, mode)
    register_catalog_resources(server, mode)
    return server


mcp = create_server()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wait-only", action="store_true")
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
    parser.add_argument(
        "--discovery-mode",
        choices=["progressive", "full"],
        default=None,
        help=(
            "MCP surface: progressive discovery (default) or the historical full "
            "one-tool-per-Action compatibility mode."
        ),
    )
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    root = workspace_root()
    os.environ.setdefault("RESEARCHCHEM_TOOL_LOG_DIR", str(root / "tool_logs"))
    os.chdir(root)
    server = create_server(discovery_mode=args.discovery_mode, wait_only=args.wait_only)
    if args.transport == "streamable_http":
        import uvicorn

        uvicorn.run(server.streamable_http_app(), host=args.host, port=args.port)
    else:
        server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
