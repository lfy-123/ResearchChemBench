#!/usr/bin/env python3
"""List Chemistry MCP tools and optionally run a local no-network smoke flow."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import tempfile
from pathlib import Path


EXPECTED_TOOLS = {
    "calculator",
    "extract_output_json",
    "molecule_name_to_smiles",
    "run_ase",
    "smiles_to_coordinate_file",
}


def _require_success(name: str, result) -> None:
    if getattr(result, "is_error", False):
        raise RuntimeError(f"MCP smoke call failed: {name}: {result}")


async def run(*, smoke: bool = False) -> None:
    with tempfile.TemporaryDirectory(prefix="researchchembench-mcp-") as temporary:
        workspace = Path(temporary)
        (workspace / "outputs").mkdir()
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        os.environ["RESEARCHCHEMBENCH_RUN_ID"] = "mcp-tool-check"

        from fastmcp import Client
        from evaluation.mcp_tools.server import mcp

        async with Client(mcp) as client:
            tools = await client.list_tools()
            tool_names = {tool.name for tool in tools}
            missing = EXPECTED_TOOLS - tool_names
            if missing:
                raise RuntimeError(f"Missing expected MCP tools: {sorted(missing)}")
            print("Registered Chemistry MCP tools:")
            for tool in sorted(tools, key=lambda item: item.name):
                print(f"  - {tool.name}")

            if not smoke:
                return

            calculator = await client.call_tool(
                "calculator", {"expression": "(2 + 3) * 4"}
            )
            _require_success("calculator", calculator)
            coordinates = await client.call_tool(
                "smiles_to_coordinate_file",
                {
                    "smiles": "O",
                    "output_file": "outputs/water.xyz",
                    "seed": 2025,
                },
            )
            _require_success("smiles_to_coordinate_file", coordinates)
            ase_result = await client.call_tool(
                "run_ase",
                {
                    "params": {
                        "input_structure_file": "outputs/water.xyz",
                        "output_results_file": "outputs/water_energy.json",
                        "driver": "energy",
                        "calculator": {"calculator_type": "emt"},
                    }
                },
            )
            _require_success("run_ase", ase_result)
            extracted = await client.call_tool(
                "extract_output_json",
                {"json_file": "outputs/water_energy.json"},
            )
            _require_success("extract_output_json", extracted)

        trace_path = workspace / "_tool_trace.jsonl"
        events = [
            json.loads(line)
            for line in trace_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        expected_sequence = [
            "calculator",
            "smiles_to_coordinate_file",
            "run_ase",
            "extract_output_json",
        ]
        actual_sequence = [event.get("tool") for event in events]
        if actual_sequence != expected_sequence:
            raise RuntimeError(
                f"Unexpected trace sequence: expected {expected_sequence}, got {actual_sequence}"
            )
        if not (workspace / "outputs" / "water.xyz").is_file():
            raise RuntimeError("SMILES smoke call did not create water.xyz")
        if not (workspace / "outputs" / "water_energy.json").is_file():
            raise RuntimeError("ASE smoke call did not create water_energy.json")
        if not any((workspace / "_tool_artifacts").rglob("water_energy.json")):
            raise RuntimeError("MCP tracing did not snapshot water_energy.json")

        print("Local MCP smoke flow passed:")
        print("  calculator -> SMILES/XYZ -> ASE/EMT energy -> JSON extraction")
        print("  canonical trace, full results, and artifact snapshots verified")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help=(
            "Run a local water/EMT flow. This checks MCP, RDKit, ASE, tracing, and "
            "artifacts without PubChem network access or MACE/TBLite models."
        ),
    )
    args = parser.parse_args()
    asyncio.run(run(smoke=args.smoke))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
