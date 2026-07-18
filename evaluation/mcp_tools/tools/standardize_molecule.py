"""MCP tool: standardize and validate a molecule with RDKit."""

from __future__ import annotations

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="standardize_molecule",
    description="Standardize a SMILES molecule with RDKit cleanup, fragment selection, and optional neutralization.",
    category="cheminformatics",
    backend="RDKit",
    dependencies=("rdkit",),
    tags=("smiles", "standardization", "validation"),
)


def standardize_molecule_core(smiles: str, neutralize: bool = True) -> dict:
    if not smiles.strip():
        raise ValueError("smiles must not be empty")
    if not module_available("rdkit"):
        return unavailable_result(
            "RDKit",
            reason="Python module rdkit is not installed",
            manual_action="Install rdkit in .toolbox_env.",
        )
    from rdkit import Chem
    from rdkit.Chem import Descriptors
    from rdkit.Chem import rdMolDescriptors
    from rdkit.Chem.MolStandardize import rdMolStandardize

    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    molecule = rdMolStandardize.Cleanup(molecule)
    molecule = rdMolStandardize.LargestFragmentChooser().choose(molecule)
    if neutralize:
        molecule = rdMolStandardize.Uncharger().uncharge(molecule)
    canonical = Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)
    return {
        "status": "success",
        "backend": "RDKit",
        "input_smiles": smiles,
        "canonical_smiles": canonical,
        "formula": rdMolDescriptors.CalcMolFormula(molecule),
        "molecular_weight": Descriptors.MolWt(molecule),
        "formal_charge": Chem.GetFormalCharge(molecule),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def standardize_molecule(smiles: str, neutralize: bool = True) -> dict:
        return execute_traced(
            TOOL_SPEC.name,
            {"smiles": smiles, "neutralize": neutralize},
            lambda: standardize_molecule_core(smiles, neutralize),
        )
