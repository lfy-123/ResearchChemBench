"""MCP tool: generate one 3D molecular structure with an explicit backend."""

from __future__ import annotations

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="generate_3d_structure",
    description="Generate an optimized 3D structure from SMILES using an explicit RDKit backend.",
    category="cheminformatics",
    backend="RDKit",
    dependencies=("rdkit",),
    tags=("smiles", "3d", "coordinates"),
    side_effects=("writes SDF or XYZ structure file",),
)


def generate_3d_structure_core(
    smiles: str,
    output_file: str = "outputs/generated_3d.sdf",
    seed: int = 2025,
) -> dict:
    if not module_available("rdkit"):
        return unavailable_result("RDKit", reason="rdkit is not installed", manual_action="Install rdkit in .toolbox_env.")
    from rdkit import Chem
    from rdkit.Chem import AllChem

    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    molecule = Chem.AddHs(molecule)
    if AllChem.EmbedMolecule(molecule, randomSeed=seed) != 0:
        raise RuntimeError("RDKit failed to embed a 3D conformer")
    AllChem.MMFFOptimizeMolecule(molecule)
    destination = resolve_workspace_output_path(output_file)
    suffix = destination.suffix.lower()
    if suffix == ".sdf":
        writer = Chem.SDWriter(str(destination))
        writer.write(molecule)
        writer.close()
    elif suffix == ".xyz":
        destination.write_text(Chem.MolToXYZBlock(molecule), encoding="utf-8")
    else:
        raise ValueError("output_file must end in .sdf or .xyz")
    return {
        "status": "success",
        "backend": "RDKit",
        "smiles": smiles,
        "output_file": relative_workspace_path(destination),
        "atom_count": molecule.GetNumAtoms(),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def generate_3d_structure(
        smiles: str,
        output_file: str = "outputs/generated_3d.sdf",
        seed: int = 2025,
    ) -> dict:
        arguments = {"smiles": smiles, "output_file": output_file, "seed": seed}
        return execute_traced(TOOL_SPEC.name, arguments, lambda: generate_3d_structure_core(**arguments))

