"""MCP tool: run a bounded PySCF single-point calculation."""

from __future__ import annotations

import json

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="run_pyscf",
    description="Run an explicit PySCF RHF/UHF/RKS/UKS molecular single-point calculation from an atom specification.",
    category="quantum_chemistry",
    backend="PySCF",
    dependencies=("pyscf",),
    tags=("pyscf", "hartree_fock", "dft", "energy"),
    side_effects=("runs PySCF", "writes structured result JSON"),
)


def run_pyscf_core(
    atom_spec: str,
    basis: str = "sto-3g",
    method: str = "rhf",
    charge: int = 0,
    spin: int = 0,
    xc: str = "pbe",
    output_file: str = "outputs/pyscf_result.json",
) -> dict:
    if method not in {"rhf", "uhf", "rks", "uks"}:
        raise ValueError("method must be rhf, uhf, rks, or uks")
    if not atom_spec.strip() or len(atom_spec) > 100_000:
        raise ValueError("atom_spec must be a non-empty bounded string")
    if not module_available("pyscf"):
        return unavailable_result(
            "PySCF",
            reason="pyscf is not installed",
            manual_action="Install the quantum MCP profile environment (.tool_envs/quantum).",
        )
    from pyscf import dft, gto, scf

    molecule = gto.M(atom=atom_spec, basis=basis, charge=charge, spin=spin, unit="Angstrom", verbose=0)
    calculation = {
        "rhf": scf.RHF,
        "uhf": scf.UHF,
        "rks": dft.RKS,
        "uks": dft.UKS,
    }[method](molecule)
    if method in {"rks", "uks"}:
        calculation.xc = xc
    energy = float(calculation.kernel())
    result = {
        "status": "success" if calculation.converged else "error",
        "backend": "PySCF",
        "method": method,
        "basis": basis,
        "xc": xc if method in {"rks", "uks"} else None,
        "converged": bool(calculation.converged),
        "energy_hartree": energy,
        "electron_count": molecule.nelectron,
    }
    destination = resolve_workspace_output_path(output_file)
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result["output_file"] = relative_workspace_path(destination)
    return result


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_pyscf(
        atom_spec: str,
        basis: str = "sto-3g",
        method: str = "rhf",
        charge: int = 0,
        spin: int = 0,
        xc: str = "pbe",
        output_file: str = "outputs/pyscf_result.json",
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_pyscf_core(**arguments))
