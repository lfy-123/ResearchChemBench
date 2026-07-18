"""MCP tool: convert a molecule name to canonical SMILES."""

from __future__ import annotations

from ..models import ToolSpec
from ..settings import ensure_chemgraph_on_path
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="molecule_name_to_smiles",
    description="Convert a molecule name to canonical SMILES using ChemGraph/PubChem.",
    category="cheminformatics",
    backend="ChemGraph/PubChem",
    dependencies=("pubchempy",),
    tags=("smiles", "lookup", "network"),
    requires_network=True,
    side_effects=("external PubChem request",),
)


def register(mcp) -> None:
    ensure_chemgraph_on_path()
    from chemgraph.tools.cheminformatics_core import molecule_name_to_smiles_core

    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def molecule_name_to_smiles(name: str) -> str:
        return execute_traced(
            TOOL_SPEC.name,
            {"name": name},
            lambda: molecule_name_to_smiles_core(name),
        )
