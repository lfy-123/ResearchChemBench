"""MCP tool: generate a deterministic RDKit conformer ensemble."""

from __future__ import annotations

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="generate_conformers_rdkit",
    description="Generate and MMFF-rank a conformer ensemble from SMILES with RDKit ETKDG.",
    category="conformer_search",
    backend="RDKit ETKDG/MMFF",
    dependencies=("rdkit",),
    tags=("conformers", "etkdg", "mmff"),
    side_effects=("writes multi-conformer SDF file",),
)


def generate_conformers_rdkit_core(
    smiles: str,
    output_file: str = "outputs/conformers.sdf",
    max_conformers: int = 20,
    seed: int = 2025,
) -> dict:
    if max_conformers < 1 or max_conformers > 500:
        raise ValueError("max_conformers must be between 1 and 500")
    if not module_available("rdkit"):
        return unavailable_result("RDKit", reason="rdkit is not installed", manual_action="Install rdkit in .toolbox_env.")
    from rdkit import Chem
    from rdkit.Chem import AllChem

    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    molecule = Chem.AddHs(molecule)
    parameters = AllChem.ETKDGv3()
    parameters.randomSeed = seed
    conformer_ids = list(AllChem.EmbedMultipleConfs(molecule, numConfs=max_conformers, params=parameters))
    if not conformer_ids:
        raise RuntimeError("RDKit did not generate any conformers")
    optimization = AllChem.MMFFOptimizeMoleculeConfs(molecule)
    energies = [float(item[1]) for item in optimization]
    destination = resolve_workspace_output_path(output_file)
    writer = Chem.SDWriter(str(destination))
    for index, conformer_id in enumerate(conformer_ids):
        molecule.SetProp("conformer_index", str(index))
        molecule.SetProp("mmff_energy", str(energies[index]))
        writer.write(molecule, confId=conformer_id)
    writer.close()
    return {
        "status": "success",
        "backend": "RDKit ETKDG/MMFF",
        "output_file": relative_workspace_path(destination),
        "conformer_count": len(conformer_ids),
        "energies_kcal_mol": energies,
        "lowest_energy_index": min(range(len(energies)), key=energies.__getitem__),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def generate_conformers_rdkit(
        smiles: str,
        output_file: str = "outputs/conformers.sdf",
        max_conformers: int = 20,
        seed: int = 2025,
    ) -> dict:
        arguments = {
            "smiles": smiles,
            "output_file": output_file,
            "max_conformers": max_conformers,
            "seed": seed,
        }
        return execute_traced(TOOL_SPEC.name, arguments, lambda: generate_conformers_rdkit_core(**arguments))
