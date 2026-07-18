"""MCP tool: run an explicit machine-learning interatomic-potential backend."""

from __future__ import annotations

from ..adapters.runtime import module_available, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_mlip",
    description="Evaluate structure energy/forces with an explicit MACE or CHGNet backend; model downloads require opt-in.",
    category="mlip",
    backend="MACE/CHGNet",
    dependencies=("ase",),
    tags=("mlip", "mace", "chgnet", "energy", "forces"),
    requires_network=True,
)


def run_mlip_core(
    structure_file: str,
    backend: str,
    model: str = "",
    device: str = "cpu",
    allow_model_download: bool = False,
) -> dict:
    if backend not in {"mace", "chgnet", "nequip", "deepmd"}:
        raise ValueError("backend must be mace, chgnet, nequip, or deepmd")
    if device not in {"cpu", "cuda", "xpu"}:
        raise ValueError("device must be cpu, cuda, or xpu")
    if not module_available("ase"):
        return unavailable_result(
            "ASE",
            reason="ase is not installed",
            manual_action="Install the mlip MCP profile environment (.tool_envs/mlip).",
        )
    from ase.io import read

    atoms = read(safe_input_file(structure_file))
    if backend == "mace":
        if not module_available("mace"):
            return unavailable_result(
                "MACE",
                reason="mace is not installed",
                manual_action="Install the mlip MCP profile environment (.tool_envs/mlip).",
            )
        if not model and not allow_model_download:
            return unavailable_result(
                "MACE",
                reason="No model was supplied and automatic model download is disabled",
                manual_action="Provide a model path/name or set allow_model_download=true for an approved download.",
            )
        from mace.calculators import mace_mp

        atoms.calc = mace_mp(model=model or "medium", device=device, default_dtype="float64")
    elif backend == "chgnet":
        if not module_available("chgnet"):
            return unavailable_result(
                "CHGNet",
                reason="chgnet is not installed",
                manual_action="Install the mlip MCP profile environment (.tool_envs/mlip).",
            )
        if not allow_model_download:
            return unavailable_result(
                "CHGNet",
                reason="Pretrained model loading is disabled without allow_model_download",
                manual_action="Set allow_model_download=true after reviewing model provenance.",
            )
        from chgnet.model.dynamics import CHGNetCalculator

        atoms.calc = CHGNetCalculator(use_device=device)
    else:
        return unavailable_result(
            backend,
            reason="The backend requires a model-specific adapter that is not configured in this initial version",
            manual_action=f"Install {backend} and add a reviewed model adapter/path.",
        )
    return {
        "status": "success",
        "backend": backend,
        "model": model or "default",
        "energy_ev": float(atoms.get_potential_energy()),
        "forces_ev_per_angstrom": atoms.get_forces().tolist(),
        "atom_count": len(atoms),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_mlip(
        structure_file: str,
        backend: str,
        model: str = "",
        device: str = "cpu",
        allow_model_download: bool = False,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_mlip_core(**arguments))
