"""MCP tool: query PubChem compound properties through PubChemPy."""

from __future__ import annotations

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="query_pubchem",
    description="Query PubChem by compound name, CID, SMILES, InChI, or InChIKey and return selected identifiers/properties.",
    category="external_data",
    backend="PubChem PUG-REST via PubChemPy",
    dependencies=("pubchempy",),
    tags=("pubchem", "compound", "identifiers", "properties"),
    requires_network=True,
    side_effects=("external PubChem request",),
)


def query_pubchem_core(
    identifier: str,
    namespace: str = "name",
    max_records: int = 5,
) -> dict:
    allowed = {"name", "cid", "smiles", "inchi", "inchikey", "formula"}
    if namespace not in allowed:
        raise ValueError(f"namespace must be one of {sorted(allowed)}")
    if not identifier.strip() or max_records < 1 or max_records > 20:
        raise ValueError("identifier must be non-empty and max_records must be 1..20")
    if not module_available("pubchempy"):
        return unavailable_result(
            "PubChem/PubChemPy",
            reason="pubchempy is not installed",
            manual_action="Install pubchempy and ensure PubChem network access.",
        )
    import pubchempy as pcp

    compounds = pcp.get_compounds(identifier.strip(), namespace)[:max_records]
    return {
        "status": "success",
        "backend": "PubChem PUG-REST via PubChemPy",
        "query": {"identifier": identifier, "namespace": namespace},
        "count": len(compounds),
        "records": [
            {
                "cid": compound.cid,
                "canonical_smiles": compound.canonical_smiles,
                "isomeric_smiles": compound.isomeric_smiles,
                "inchi": compound.inchi,
                "inchikey": compound.inchikey,
                "molecular_formula": compound.molecular_formula,
                "molecular_weight": compound.molecular_weight,
                "iupac_name": compound.iupac_name,
            }
            for compound in compounds
        ],
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def query_pubchem(identifier: str, namespace: str = "name", max_records: int = 5) -> dict:
        arguments = {"identifier": identifier, "namespace": namespace, "max_records": max_records}
        return execute_traced(TOOL_SPEC.name, arguments, lambda: query_pubchem_core(**arguments))

