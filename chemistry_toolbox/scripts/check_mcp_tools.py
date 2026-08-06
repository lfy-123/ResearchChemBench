#!/usr/bin/env python3
"""Validate all three MCP layers and optionally run a no-network Action smoke flow."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import action_specs, validate_catalog
from chemistry_toolbox.mcp.async_action_tools import ASYNC_ACTION_TOOL_NAMES
from chemistry_toolbox.mcp.open_tools import OPEN_EXECUTION_TOOL_NAMES


def _require_success(name: str, result) -> None:
    if getattr(result, "is_error", False):
        raise RuntimeError(f"MCP smoke call failed: {name}: {result}")
    data = getattr(result, "data", None)
    if isinstance(data, dict) and data.get("status") not in {"success", "partial_success"}:
        raise RuntimeError(f"MCP smoke call returned {data.get('status')}: {name}: {data}")


async def run(*, smoke: bool = False) -> None:
    validate_catalog()
    with tempfile.TemporaryDirectory(prefix="researchchembench-mcp-") as temporary:
        workspace = Path(temporary)
        for name in ("code", "outputs", "report", "tool_logs", "_tool_results", "_tool_artifacts"):
            (workspace / name).mkdir()
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        os.environ["RESEARCHCHEMBENCH_RUN_ID"] = "mcp-tool-check"

        from fastmcp import Client
        from chemistry_toolbox.mcp.server import create_server

        # This script validates the historical one-tool-per-Action surface.
        # Benchmark workspaces use progressive discovery by default and are
        # covered separately by the MCP profile tests.
        async with Client(create_server(discovery_mode="full")) as client:
            tools = await client.list_tools()
            tool_names = {tool.name for tool in tools}
            expected_tools = (
                set(action_specs())
                | set(OPEN_EXECUTION_TOOL_NAMES)
                | set(ASYNC_ACTION_TOOL_NAMES)
            )
            if tool_names != expected_tools:
                raise RuntimeError(
                    f"Full three-layer catalog mismatch: "
                    f"missing={sorted(expected_tools - tool_names)}, "
                    f"extra={sorted(tool_names - expected_tools)}"
                )
            print(
                f"Registered {len(action_specs())} Actions and "
                f"{len(OPEN_EXECUTION_TOOL_NAMES)} open-execution plus "
                f"{len(ASYNC_ACTION_TOOL_NAMES)} async MCP tools"
            )
            if not smoke:
                return
            calls = [
                (
                    "standardize_structure",
                    {
                        "request": {
                            "backend_id": "rdkit",
                            "inputs": {"structure": "CC(=O)[O-].[Na+]"},
                            "method_spec": {},
                            "action_settings": {
                                "largest_fragment": True,
                                "neutralize": False,
                                "canonical_tautomer": False,
                            },
                        }
                    },
                ),
                (
                    "generate_3d_structure",
                    {
                        "request": {
                            "backend_id": "rdkit",
                            "inputs": {"molecule": "O"},
                            "method_spec": {},
                            "action_settings": {"random_seed": 20260718},
                        }
                    },
                ),
                (
                    "calculate_energy",
                    {
                        "request": {
                            "backend_id": "ase_emt",
                            "inputs": {
                                "structure": {
                                    "atoms": [
                                        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
                                        {"element": "H", "position_angstrom": [0.0, 0.0, 0.74]},
                                    ],
                                    "charge": 0,
                                    "multiplicity": 1,
                                    "pbc": [False, False, False],
                                }
                            },
                            "method_spec": {},
                            "action_settings": {},
                        }
                    },
                ),
                (
                    "rank_conformers_from_results",
                    {
                        "request": {
                            "backend_id": "internal_statistics",
                            "inputs": {
                                "ensemble": [{"conformer_id": "a"}, {"conformer_id": "b"}],
                                "scores": [{"value": 0.0}, {"value": 1.0}],
                            },
                            "method_spec": {},
                            "action_settings": {
                                "temperature_kelvin": 298.15,
                                "score_unit": "kcal_mol",
                            },
                        }
                    },
                ),
            ]
            for name, arguments in calls:
                _require_success(name, await client.call_tool(name, arguments))

            open_trace = []
            result = await client.call_tool(
                "inspect_software", {"request": {"software_id": "cp2k"}}
            )
            _require_success("inspect_software", result)
            if not result.data["native_invocation_guides"]:
                raise RuntimeError("CP2K native invocation guide was not returned")
            open_trace.append("inspect_software")

            result = await client.call_tool(
                "write_workspace_text",
                {
                    "request": {
                        "path": "code/mcp_smoke.py",
                        "content": (
                            "from pathlib import Path\n"
                            "print('open-layer-ok')\n"
                            "Path('open_result.json').write_text('{\\\"ok\\\": true}\\n')\n"
                        ),
                    }
                },
            )
            _require_success("write_workspace_text", result)
            open_trace.append("write_workspace_text")

            result = await client.call_tool(
                "submit_analysis_program",
                {
                    "request": {
                        "runtime": "core",
                        "script_path": "code/mcp_smoke.py",
                        "resource_limits": {
                            "memory_mb": 512,
                            "cpu_cores": 1,
                            "gpu_count": 0,
                        },
                    }
                },
            )
            _require_success("submit_analysis_program", result)
            open_trace.append("submit_analysis_program")
            job_id = result.data["job_id"]
            job = None
            for _attempt in range(100):
                result = await client.call_tool(
                    "get_execution_job",
                    {"request": {"job_id": job_id, "tail_chars": 1000}},
                )
                _require_success("get_execution_job", result)
                open_trace.append("get_execution_job")
                job = result.data
                if job["terminal"]:
                    break
                await asyncio.sleep(0.05)
            if not job or job["job"]["status"] != "success":
                raise RuntimeError(f"Programmable MCP smoke did not succeed: {job}")

            result = await client.call_tool(
                "collect_execution_job",
                {"request": {"job_id": job_id, "tail_chars": 0}},
            )
            _require_success("collect_execution_job", result)
            open_trace.append("collect_execution_job")
            output = next(
                item
                for item in result.data["outputs"]
                if item["job_relative_path"] == "open_result.json"
            )
            result = await client.call_tool(
                "declare_scientific_artifact",
                {
                    "request": {
                        "path": output["path"],
                        "semantic_type": "mcp_open_execution_smoke",
                        "media_type": "application/json",
                        "producer_layer": "programmable_analysis",
                        "producer_id": "core:mcp_smoke.py",
                    }
                },
            )
            _require_success("declare_scientific_artifact", result)
            open_trace.append("declare_scientific_artifact")

        events = [
            json.loads(line)
            for line in (workspace / "_tool_trace.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        expected = [name for name, _arguments in calls] + open_trace
        actual = [event["tool"] for event in events]
        if actual != expected:
            raise RuntimeError(f"Unexpected trace sequence: expected {expected}, got {actual}")
        if not (workspace / "_tool_artifacts" / "index.jsonl").is_file():
            raise RuntimeError("Semantic Artifact index was not created")
        print(
            "Three-layer MCP smoke passed: explicit Actions/backends, software guide, "
            "Agent program, persistent job, Artifact chain, trace"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    asyncio.run(run(smoke=args.smoke))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
