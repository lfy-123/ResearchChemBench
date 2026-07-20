from __future__ import annotations

import asyncio
from pathlib import Path

from fastmcp import Client

from evaluation.mcp_tools.registry import (
    configuration_errors,
    discover_tools,
    discovered_module_stems,
)
from evaluation.mcp_tools.server import create_server
from researchchem_toolbox.catalog import action_specs, validate_catalog


def test_registry_is_full_and_task_independent():
    validate_catalog()
    assert configuration_errors() == []
    assert discovered_module_stems() == sorted(action_specs())
    records = discover_tools(strict=True)
    assert len(records) == len(action_specs())
    assert all(record.enabled and record.error is None for record in records)


def test_server_registers_all_actions_and_catalog_resource():
    async def collect():
        async with Client(create_server()) as client:
            return await client.list_tools(), await client.list_resources()

    tools, resources = asyncio.run(collect())
    assert {tool.name for tool in tools} == set(action_specs())
    assert len(tools) == len(action_specs())
    assert {str(resource.uri) for resource in resources} == {"researchchem://catalog"}
    for tool in tools:
        assert set(tool.inputSchema["properties"]) == {"request"}
        assert "backend_id" in tool.inputSchema["$defs"]["ActionRequest"]["properties"]


def test_legacy_public_tool_files_are_gone():
    directory = Path("evaluation/mcp_tools/tools")
    assert sorted(path.name for path in directory.glob("*.py")) == ["__init__.py"]
    assert not any(path.name.startswith("run_") for path in directory.glob("*.py"))
