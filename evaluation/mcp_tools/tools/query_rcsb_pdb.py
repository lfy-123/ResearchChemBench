"""MCP tool: query RCSB PDB entry metadata."""

from __future__ import annotations

from ..adapters.http import get_json
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="query_rcsb_pdb",
    description="Retrieve normalized entry metadata for one four-character RCSB PDB identifier.",
    category="external_data",
    backend="RCSB PDB Data API",
    tags=("pdb", "protein", "structure", "metadata"),
    requires_network=True,
    side_effects=("external RCSB PDB request",),
)


def query_rcsb_pdb_core(pdb_id: str) -> dict:
    normalized = pdb_id.strip().upper()
    if len(normalized) != 4 or not normalized.isalnum():
        raise ValueError("pdb_id must be a four-character alphanumeric identifier")
    value = get_json(f"https://data.rcsb.org/rest/v1/core/entry/{normalized}")
    struct = value.get("struct", {})
    info = value.get("rcsb_entry_info", {})
    accession = value.get("rcsb_accession_info", {})
    return {
        "status": "success",
        "backend": "RCSB PDB Data API",
        "pdb_id": normalized,
        "title": struct.get("title"),
        "experimental_method": [item.get("method") for item in value.get("exptl", [])],
        "resolution_combined": info.get("resolution_combined"),
        "polymer_entity_count": info.get("polymer_entity_count"),
        "nonpolymer_entity_count": info.get("nonpolymer_entity_count"),
        "deposit_date": accession.get("deposit_date"),
        "initial_release_date": accession.get("initial_release_date"),
        "raw": value,
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def query_rcsb_pdb(pdb_id: str) -> dict:
        return execute_traced(TOOL_SPEC.name, {"pdb_id": pdb_id}, lambda: query_rcsb_pdb_core(pdb_id))

