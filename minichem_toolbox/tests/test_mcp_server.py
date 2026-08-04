from __future__ import annotations

import asyncio

from fastmcp import Client

from minichem_mcp_tools.async_action_tools import ASYNC_ACTION_TOOL_NAMES
from minichem_mcp_tools.discovery_tools import PROGRESSIVE_DISCOVERY_TOOL_NAMES
from minichem_mcp_tools.open_tools import OPEN_EXECUTION_TOOL_NAMES
from minichem_mcp_tools.server import create_server


def test_progressive_mcp_server_registers_three_layer_surface() -> None:
    async def collect():
        async with Client(create_server()) as client:
            return await client.list_tools(), await client.list_resources()

    tools, resources = asyncio.run(collect())
    expected = (
        set(PROGRESSIVE_DISCOVERY_TOOL_NAMES)
        | set(OPEN_EXECUTION_TOOL_NAMES)
        | set(ASYNC_ACTION_TOOL_NAMES)
    )
    assert {item.name for item in tools} == expected
    assert {str(item.uri) for item in resources} == {
        "minichem://catalog",
        "minichem://software",
        "minichem://execution-policy",
    }
