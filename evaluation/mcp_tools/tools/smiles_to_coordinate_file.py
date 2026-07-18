"""MCP tool: generate a 3D coordinate file from SMILES."""

from __future__ import annotations

from typing import Literal

from ..models import ToolSpec
from ..settings import ensure_chemgraph_on_path
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="smiles_to_coordinate_file",
    description="Generate a 3D XYZ coordinate file from SMILES inside the active workspace.",
    category="cheminformatics",
    backend="ChemGraph/RDKit/ASE",
    dependencies=("rdkit", "ase"),
    tags=("smiles", "coordinates", "xyz"),
    side_effects=("writes coordinate file",),
)


def register(mcp) -> None:
    ensure_chemgraph_on_path()
    from chemgraph.tools.cheminformatics_core import smiles_to_coordinate_file_core

    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def smiles_to_coordinate_file(
        smiles: str,
        output_file: str = "outputs/molecule.xyz",
        seed: int = 2025,
        fmt: Literal["xyz"] = "xyz",
    ) -> dict:
        safe_output = resolve_workspace_output_path(output_file)

        def call() -> dict:
            result = smiles_to_coordinate_file_core(
                smiles,
                output_file=str(safe_output),
                seed=seed,
                fmt=fmt,
            )
            if isinstance(result, dict):
                result = dict(result)
                for key in ("path", "output_file", "file_path"):
                    value = result.get(key)
                    if value:
                        try:
                            result[key] = relative_workspace_path(value)
                        except (ValueError, OSError):
                            pass
            return result

        return execute_traced(
            TOOL_SPEC.name,
            {
                "smiles": smiles,
                "output_file": output_file,
                "seed": seed,
                "fmt": fmt,
            },
            call,
        )
