"""MCP tool: run a workspace-confined ChemGraph ASE calculation."""

from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

from ..models import ToolSpec
from ..settings import ensure_chemgraph_on_path
from ..tracing import execute_traced
from ..workspace import (
    relative_workspace_path,
    resolve_workspace_output_path,
    resolve_workspace_path,
)


TOOL_SPEC = ToolSpec(
    name="run_ase",
    description=(
        "Run a ChemGraph ASE calculation. Drivers include energy, dipole, opt, "
        "vib, ir, and thermo. Files stay inside the active workspace."
    ),
    category="simulation",
    backend="ChemGraph/ASE",
    dependencies=("ase",),
    tags=("energy", "optimization", "vibration", "thermochemistry", "dipole"),
    side_effects=("runs chemistry calculation", "writes result and calculator files"),
)


def _looks_like_path(value: str) -> bool:
    return (
        Path(value).is_absolute()
        or "/" in value
        or "\\" in value
        or value.startswith(".")
    )


def _sanitize_calculator(calculator: object) -> object:
    """Confine calculator workdirs/models and reject agent-supplied commands."""

    if not isinstance(calculator, dict):
        return calculator
    safe = dict(calculator)
    calculator_type = str(safe.get("calculator_type", "")).lower()

    if calculator_type == "nwchem" and safe.get("command"):
        raise ValueError(
            "Agent-supplied NWChem commands are disabled; configure the executable "
            "in the MCP server environment"
        )
    if calculator_type == "orca" and safe.get("profile"):
        raise ValueError(
            "Agent-supplied ORCA profiles are disabled; configure ORCA on the MCP "
            "server PATH"
        )

    if calculator_type in {"nwchem", "orca"}:
        directory = str(safe.get("directory") or ".")
        if directory in {"", "."}:
            directory = f"tool_logs/{calculator_type}"
        probe = resolve_workspace_output_path(str(Path(directory) / ".workdir"))
        probe.parent.mkdir(parents=True, exist_ok=True)
        safe["directory"] = str(probe.parent)

    model = safe.get("model")
    if isinstance(model, str) and model and _looks_like_path(model):
        safe["model"] = str(resolve_workspace_path(model, must_exist=True))
    return safe


def register(mcp) -> None:
    global ASEInputSchema

    ensure_chemgraph_on_path()
    from chemgraph.schemas.ase_input import ASEInputSchema as _ASEInputSchema
    from chemgraph.tools.ase_core import run_ase_core

    # FastMCP resolves postponed annotations through module globals.
    ASEInputSchema = _ASEInputSchema

    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_ase(params: ASEInputSchema) -> dict:
        raw = params.model_dump(mode="json")
        safe = dict(raw)
        safe["calculator"] = _sanitize_calculator(raw.get("calculator"))
        safe["input_structure_file"] = str(
            resolve_workspace_path(raw["input_structure_file"], must_exist=True)
        )
        safe["output_results_file"] = str(
            resolve_workspace_output_path(
                raw.get("output_results_file", "outputs/output.json")
            )
        )
        validated = ASEInputSchema.model_validate(safe)

        def call() -> dict:
            captured = io.StringIO()
            with redirect_stdout(captured):
                result = run_ase_core(validated)
            if isinstance(result, dict):
                result = dict(result)
                result["captured_stdout"] = captured.getvalue()[-4000:]
                for key in ("output_results_file", "result_file"):
                    value = result.get(key)
                    if value:
                        try:
                            result[key] = relative_workspace_path(value)
                        except (ValueError, OSError):
                            pass
            return result

        return execute_traced(TOOL_SPEC.name, {"params": raw}, call)
