"""MCP tool: repair a PDB structure with PDBFixer for MD preparation."""

from __future__ import annotations

from ..adapters.runtime import module_available, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="prepare_md_system",
    description="Repair a PDB with PDBFixer, add missing atoms/hydrogens, and write a workspace-confined prepared PDB.",
    category="molecular_dynamics",
    backend="PDBFixer/OpenMM",
    dependencies=("pdbfixer", "openmm"),
    tags=("pdbfixer", "pdb", "md_preparation"),
    side_effects=("writes prepared PDB file",),
)


def prepare_md_system_core(
    input_pdb: str,
    output_pdb: str = "outputs/prepared.pdb",
    ph: float = 7.0,
    add_missing_residues: bool = False,
) -> dict:
    if ph < 0 or ph > 14:
        raise ValueError("ph must be between 0 and 14")
    if not module_available("pdbfixer") or not module_available("openmm"):
        return unavailable_result(
            "PDBFixer/OpenMM",
            reason="pdbfixer and/or openmm is not installed",
            manual_action="Install the md MCP profile environment (.tool_envs/md).",
        )
    from openmm.app import PDBFile
    from pdbfixer import PDBFixer

    source = safe_input_file(input_pdb)
    destination = resolve_workspace_output_path(output_pdb)
    fixer = PDBFixer(filename=str(source))
    fixer.findMissingResidues()
    if not add_missing_residues:
        fixer.missingResidues = {}
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.removeHeterogens(keepWater=True)
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(ph)
    with destination.open("w", encoding="utf-8") as handle:
        PDBFile.writeFile(fixer.topology, fixer.positions, handle, keepIds=True)
    return {
        "status": "success",
        "backend": "PDBFixer/OpenMM",
        "input_pdb": relative_workspace_path(source),
        "output_pdb": relative_workspace_path(destination),
        "atom_count": fixer.topology.getNumAtoms(),
        "residue_count": fixer.topology.getNumResidues(),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def prepare_md_system(input_pdb: str, output_pdb: str = "outputs/prepared.pdb", ph: float = 7.0, add_missing_residues: bool = False) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: prepare_md_system_core(**arguments))
