#!/usr/bin/env python3
"""Validate the full MCP catalog and optionally run a no-network atomic smoke flow."""

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


def _require_success(name: str, result) -> None:
    if getattr(result, "is_error", False):
        raise RuntimeError(f"MCP smoke call failed: {name}: {result}")


async def run(*, smoke: bool = False) -> None:
    validate_catalog()
    with tempfile.TemporaryDirectory(prefix="researchchembench-mcp-") as temporary:
        workspace = Path(temporary)
        for name in ("outputs", "report", "tool_logs", "_tool_results", "_tool_artifacts"):
            (workspace / name).mkdir()
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        os.environ["RESEARCHCHEMBENCH_RUN_ID"] = "mcp-tool-check"

        from fastmcp import Client
        from chemistry_toolbox.mcp.server import create_server

        async with Client(create_server()) as client:
            tools = await client.list_tools()
            tool_names = {tool.name for tool in tools}
            if tool_names != set(action_specs()):
                raise RuntimeError(
                    f"Full catalog mismatch: missing={sorted(set(action_specs()) - tool_names)}, "
                    f"extra={sorted(tool_names - set(action_specs()))}"
                )
            print(f"Registered {len(tools)} complete-catalog Chemistry MCP tools")
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

        events = [
            json.loads(line)
            for line in (workspace / "_tool_trace.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        expected = [name for name, _arguments in calls]
        actual = [event["tool"] for event in events]
        if actual != expected:
            raise RuntimeError(f"Unexpected trace sequence: expected {expected}, got {actual}")
        if not (workspace / "_tool_artifacts" / "index.jsonl").is_file():
            raise RuntimeError("Semantic Artifact index was not created")
        print("Atomic MCP smoke passed: explicit tools, explicit backends, Artifact chain, trace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    asyncio.run(run(smoke=args.smoke))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
