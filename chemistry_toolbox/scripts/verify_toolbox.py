#!/usr/bin/env python3
"""Verify the atomic toolbox and write health/install reports."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chemistry_toolbox.mcp.profiles import load_profile_config
from chemistry_toolbox.mcp.discovery_tools import PROGRESSIVE_DISCOVERY_TOOL_NAMES
from chemistry_toolbox.mcp.open_tools import OPEN_EXECUTION_TOOL_NAMES
from chemistry_toolbox.mcp.software_catalog import (
    list_analysis_runtimes,
    load_native_guides,
    validate_native_guides,
)
from chemistry_toolbox.mcp.execution_models import AnalysisRuntimeListRequest
from chemistry_toolbox.mcp.tool_manager import installation_report
from researchchem_toolbox.backends import (
    cheminformatics,
    data,
    docking,
    dynamics,
    electronic,
    interchange,
    periodic,
    reaction,
    structure,
)
from researchchem_toolbox.catalog import action_specs, backend_specs, catalog_snapshot, validate_catalog
from researchchem_toolbox.discovery import _action_search_documents, _action_search_fields
from researchchem_toolbox.semantic_embeddings import semantic_scores
from researchchem_toolbox.service import execute_action


JSON_PATH = TOOLBOX_ROOT / "docs" / "TOOLBOX_STATUS.json"
MARKDOWN_PATH = TOOLBOX_ROOT / "docs" / "TOOLBOX_STATUS.md"


def structural_checks() -> list[dict[str, Any]]:
    checks = []
    try:
        validate_catalog()
        checks.append({"name": "catalog", "status": "pass"})
    except Exception as exc:
        checks.append({"name": "catalog", "status": "fail", "error": str(exc)})
    try:
        load_profile_config()
        checks.append({"name": "runtime_profiles", "status": "pass"})
    except Exception as exc:
        checks.append({"name": "runtime_profiles", "status": "fail", "error": str(exc)})
    try:
        validate_native_guides()
        checks.append({"name": "native_invocation_guides", "status": "pass"})
    except Exception as exc:
        checks.append(
            {"name": "native_invocation_guides", "status": "fail", "error": str(exc)}
        )
    try:
        documents = _action_search_documents(
            _action_search_fields(list(action_specs().values()), backend_specs())
        )
        scores, semantic_status = semantic_scores("single point electronic energy", documents)
        if semantic_status != "available" or not scores:
            raise RuntimeError(
                f"MiniLM semantic retrieval is not ready: {semantic_status}; "
                "run chemistry_toolbox/scripts/cache_minilm_model.py"
            )
        checks.append(
            {
                "name": "semantic_retrieval",
                "status": "pass",
                "semantic_status": semantic_status,
                "indexed_documents": len(scores),
            }
        )
    except Exception as exc:
        checks.append(
            {"name": "semantic_retrieval", "status": "fail", "error": str(exc)}
        )
    handled = set().union(
        interchange.ACTIONS,
        structure.ACTIONS,
        cheminformatics.ACTIONS,
        electronic.ACTIONS,
        reaction.ACTIONS,
        dynamics.ACTIONS,
        periodic.ACTIONS,
        docking.ACTIONS,
        data.ACTIONS,
    )
    checks.append(
        {
            "name": "handler_coverage",
            "status": "pass" if handled == set(action_specs()) else "fail",
            "missing": sorted(set(action_specs()) - handled),
            "extra": sorted(handled - set(action_specs())),
        }
    )
    legacy_files = sorted(
        path.name
        for path in (ROOT / "evaluation" / "mcp_tools" / "tools").glob("*.py")
        if path.name != "__init__.py"
    )
    checks.append(
        {
            "name": "legacy_public_tools_removed",
            "status": "pass" if not legacy_files else "fail",
            "files": legacy_files,
        }
    )
    return checks


def smoke_results() -> list[dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="researchchem-verify-") as temporary:
        workspace = Path(temporary)
        (workspace / "outputs").mkdir()
        (workspace / "packmol_solute.pdb").write_text(
            "HETATM    1  C   MOL A   1       0.000   0.000   0.000  1.00  0.00           C\nEND\n",
            encoding="utf-8",
        )
        (workspace / "packmol_water.pdb").write_text(
            "HETATM    1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O\n"
            "HETATM    2  H1  HOH A   1       0.957   0.000   0.000  1.00  0.00           H\n"
            "HETATM    3  H2  HOH A   1      -0.240   0.927   0.000  1.00  0.00           H\nEND\n",
            encoding="utf-8",
        )
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        cases = [
            (
                "standardize_structure",
                {
                    "backend_id": "rdkit",
                    "inputs": {"structure": "CCO"},
                    "method_spec": {},
                    "action_settings": {
                        "largest_fragment": True,
                        "neutralize": False,
                        "canonical_tautomer": False,
                    },
                },
            ),
            (
                "generate_3d_structure",
                {
                    "backend_id": "rdkit",
                    "inputs": {"molecule": "O"},
                    "method_spec": {},
                    "action_settings": {"random_seed": 20260718},
                },
            ),
            (
                "calculate_energy",
                {
                    "backend_id": "ase_emt",
                    "inputs": {
                        "structure": {
                            "atoms": [
                                {"element": "H", "position_angstrom": [0, 0, 0]},
                                {"element": "H", "position_angstrom": [0, 0, 0.74]},
                            ]
                        }
                    },
                    "method_spec": {},
                    "action_settings": {},
                },
            ),
            (
                "integrate_reaction_network",
                {
                    "backend_id": "scipy",
                    "inputs": {
                        "network": {
                            "species": ["A", "B"],
                            "reactions": [
                                {
                                    "reactants": {"A": 1},
                                    "products": {"B": 1},
                                    "forward_rate_constant": 1.0,
                                }
                            ],
                        },
                        "initial_state": {"A": 1.0, "B": 0.0},
                    },
                    "method_spec": {},
                    "action_settings": {"time_end_seconds": 1.0, "num_points": 5},
                },
            ),
            (
                "assign_partial_charges",
                {
                    "backend_id": "openff_am1bcc",
                    "inputs": {"structure": {"smiles": "CCO"}},
                    "method_spec": {"charge_model": "am1bcc"},
                    "action_settings": {},
                },
            ),
            (
                "assign_force_field_parameters",
                {
                    "backend_id": "openff",
                    "inputs": {"structure": {"smiles": "CCO"}},
                    "method_spec": {
                        "force_field": "openff_unconstrained-2.3.0.offxml"
                    },
                    "action_settings": {},
                },
            ),
            (
                "solvate_molecular_system",
                {
                    "backend_id": "packmol",
                    "inputs": {
                        "system": {
                            "solute_path": "packmol_solute.pdb",
                            "force_field": "smoke-test",
                            "solvated": False,
                        }
                    },
                    "method_spec": {},
                    "action_settings": {
                        "box_shape": "cubic",
                        "box_size_angstrom": [20, 20, 20],
                        "solvent_model": "explicit_water",
                        "solvent_path": "packmol_water.pdb",
                        "molecule_counts": {"solvent": 3},
                        "tolerance_angstrom": 2.0,
                    },
                },
            ),
        ]
        results = []
        for action_id, request in cases:
            result = execute_action(action_id, request)
            results.append(
                {
                    "action": action_id,
                    "backend": request["backend_id"],
                    "status": result["status"],
                    "error": result.get("error"),
                }
            )
        return results


def markdown(payload: dict[str, Any]) -> str:
    health = {item["id"]: item["health"] for item in payload["catalog"]["backends"]}
    available = [name for name, item in health.items() if item and item.get("available")]
    unavailable = [name for name, item in health.items() if not item or not item.get("available")]
    install = payload["installation"]
    lines = [
        "# ResearchChem Three-Layer Toolbox Status",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"Catalog hash: `{payload['catalog']['catalog_hash']}`",
        "",
        "## Summary",
        "",
        f"- Scientific Actions: {payload['scientific_actions']}",
        f"- Data Actions: {payload['data_actions']}",
        f"- BackendSpecs: {payload['backend_count']}",
        f"- Open execution MCP tools: {payload['open_execution_tool_count']}",
        f"- Progressive discovery/dispatch MCP tools: {payload['progressive_tool_count']}",
        f"- Native software invocation guides: {payload['native_software_count']}",
        f"- Native command guides: {payload['native_command_count']}",
        f"- Available programmable runtimes: {payload['analysis_runtime_count']}",
        f"- Available backends: {len(available)}",
        f"- Unavailable backends: {len(unavailable)}",
        "- Exposure: complete task-independent catalog through progressive discovery",
        "- Compatibility: full one-tool-per-Action mode remains available",
        "- Backend selection: Agent required",
        "- Automatic fallback: disabled",
        "- Layers: predefined Actions, native software, programmable analysis",
        "",
        "## Structural checks",
        "",
    ]
    lines.extend(
        f"- {item['name']}: **{item['status']}**" + (f" — {item.get('error')}" if item.get("error") else "")
        for item in payload["checks"]
    )
    lines.extend(["", "## Unavailable backends", ""])
    lines.extend(f"- `{name}`" for name in unavailable)
    lines.extend(["", "## Remaining installations", ""])
    lines.append("Conda: " + (", ".join(install["conda_packages"]) or "none"))
    lines.append("")
    lines.append("Pip: " + (", ".join(install["pip_packages"]) or "none"))
    if install.get("registered_scientific_resources"):
        lines.extend(["", "## Registered external scientific resources", ""])
        for item in install["registered_scientific_resources"]:
            lines.append(
                f"- `{item['resource_id']}` / {', '.join(item['compatible_backends'])}: "
                f"**{'available' if item['available'] else 'missing'}**; "
                f"selection `{item['selection_syntax']}`"
            )
    if install["missing_credentials"]:
        lines.extend(["", "Missing credentials:", ""])
        for item in install["missing_credentials"]:
            lines.append(f"- `{item['backend_id']}`: {', '.join(item['environment_variables'])}")
    if install["manual_installations"]:
        lines.extend(["", "Manual/licensed:", ""])
        for item in install["manual_installations"]:
            lines.append(f"- `{item['backend_id']}`: {item['install_notes']}")
    if payload.get("smoke") is not None:
        lines.extend(["", "## Smoke", ""])
        for item in payload["smoke"]:
            lines.append(f"- `{item['action']}` / `{item['backend']}`: **{item['status']}**")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    checks = structural_checks()
    catalog = catalog_snapshot(include_health=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scientific_actions": sum(not item.data_action for item in action_specs().values()),
        "data_actions": sum(item.data_action for item in action_specs().values()),
        "backend_count": len(backend_specs()),
        "open_execution_tool_count": len(OPEN_EXECUTION_TOOL_NAMES),
        "progressive_tool_count": len(PROGRESSIVE_DISCOVERY_TOOL_NAMES),
        "native_software_count": len(load_native_guides()["software"]),
        "native_command_count": sum(
            len(item["commands"])
            for item in load_native_guides()["software"].values()
        ),
        "analysis_runtime_count": list_analysis_runtimes(
            AnalysisRuntimeListRequest(available_only=True)
        )["count"],
        "checks": checks,
        "catalog": catalog,
        "installation": installation_report(),
        "smoke": smoke_results() if args.smoke else None,
    }
    if not args.no_write:
        JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        MARKDOWN_PATH.write_text(markdown(payload), encoding="utf-8")
        print(JSON_PATH)
        print(MARKDOWN_PATH)
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if any(item["status"] == "fail" for item in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
