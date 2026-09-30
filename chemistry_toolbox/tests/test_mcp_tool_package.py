from __future__ import annotations

import asyncio
from pathlib import Path

from fastmcp import Client

from chemistry_toolbox.mcp.registry import (
    configuration_errors,
    discover_tools,
    discovered_module_stems,
)
from chemistry_toolbox.mcp.open_tools import OPEN_EXECUTION_TOOL_NAMES
from chemistry_toolbox.mcp.discovery_tools import PROGRESSIVE_DISCOVERY_TOOL_NAMES
from chemistry_toolbox.mcp.async_action_tools import ASYNC_ACTION_TOOL_NAMES
from chemistry_toolbox.mcp.server import create_server
from chemistry_toolbox.src.catalog import action_specs, validate_catalog


def test_registry_is_full_and_task_independent():
    validate_catalog()
    assert configuration_errors() == []
    assert discovered_module_stems() == sorted(action_specs())
    records = discover_tools(strict=True)
    assert len(records) == len(action_specs())
    assert all(record.enabled and record.error is None for record in records)


def test_progressive_server_registers_compact_surface_and_catalog_resources():
    async def collect():
        async with Client(create_server()) as client:
            return await client.list_tools(), await client.list_resources()

    tools, resources = asyncio.run(collect())
    expected_tools = (
        set(PROGRESSIVE_DISCOVERY_TOOL_NAMES)
        | set(OPEN_EXECUTION_TOOL_NAMES)
        | set(ASYNC_ACTION_TOOL_NAMES)
    )
    assert {tool.name for tool in tools} == expected_tools
    assert len(tools) == len(expected_tools)
    assert {str(resource.uri) for resource in resources} == {
        "researchchem://catalog",
        "researchchem://software",
        "researchchem://execution-policy",
    }
    for tool in tools:
        assert set(tool.inputSchema["properties"]) == {"request"}
        if tool.name == "validate_output_contract":
            assert tool.annotations.readOnlyHint is True
            assert tool.annotations.destructiveHint is False
        if tool.name == "execute_action":
            request_schema = next(
                value
                for key, value in tool.inputSchema["$defs"].items()
                if key == "ProgressiveActionRequest"
            )
            assert "action_id" in request_schema["properties"]
            assert "backend_id" in request_schema["properties"]


def test_full_compatibility_server_registers_every_action():
    async def collect():
        async with Client(create_server(discovery_mode="full")) as client:
            return await client.list_tools()

    tools = asyncio.run(collect())
    expected = (
        set(action_specs())
        | set(OPEN_EXECUTION_TOOL_NAMES)
        | set(ASYNC_ACTION_TOOL_NAMES)
        | {"validate_action"}
    )
    assert {tool.name for tool in tools} == expected


def test_legacy_public_tool_files_are_gone():
    directory = Path("chemistry_toolbox/mcp/tools")
    assert not directory.exists()
    assert not any(path.name.startswith("run_") for path in directory.glob("*.py"))
