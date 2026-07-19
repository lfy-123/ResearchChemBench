"""Shared model-loading helpers for explicit MLIP backends.

This module performs validation and loads exactly the model path and model branch
named by the agent.  It never searches the cache, chooses a pretrained model, or
downloads weights during a tool call.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import module_version, resolve_input_file
from ..resources import is_resource_reference, resource_reference_metadata


def _model_path(backend_id: str, value: Any) -> tuple[Path, dict[str, Any]]:
    metadata: dict[str, Any] = {}
    if is_resource_reference(value):
        metadata = resource_reference_metadata(value)
        compatible = set(metadata.get("compatible_backends") or [])
        if backend_id not in compatible:
            raise ValueError(
                f"Model resource {metadata.get('resource_id')!r} is not registered for "
                f"backend {backend_id!r}"
            )
    path = resolve_input_file(value)
    if not path.is_file():
        raise ValueError("MLIP model must resolve to one local model file")
    return path, metadata


def _nequip_mapping(value: Any) -> bool | dict[str, str]:
    if value == "identity":
        return True
    if isinstance(value, dict) and value:
        return {str(key): str(item) for key, item in value.items()}
    raise ValueError(
        "chemical_species_mapping must be 'identity' or an explicit element-to-model-type mapping"
    )


def _deepmd_head(
    path: Path,
    requested: Any,
    metadata: dict[str, Any],
) -> str | None:
    branch = str(requested).strip() if requested is not None else ""
    branches = [str(item) for item in metadata.get("model_branches") or []]
    aliases = {
        str(key): str(value)
        for key, value in dict(metadata.get("model_branch_aliases") or {}).items()
    }
    single_task = bool(metadata.get("single_task", False))

    if not metadata.get("registered") or (not branches and not single_task):
        from deepmd.infer import DeepEval

        inspection = DeepEval(str(path), head=0)
        definition = inspection.get_model_def_script()
        if "model_dict" in definition:
            branches = [str(item) for item in definition["model_dict"]]
        else:
            single_task = True

    if single_task:
        if branch != "single_task":
            raise ValueError(
                "A single-task DeePMD model requires model_branch='single_task' explicitly"
            )
        return None
    if not branch or branch == "single_task":
        raise ValueError(
            "A multitask DeePMD model requires an explicit named model_branch"
        )
    canonical = aliases.get(branch, branch)
    if branches and canonical not in branches:
        raise ValueError(
            f"Unknown DeePMD model_branch {branch!r}; registered branches are: "
            + ", ".join(branches)
        )
    return canonical


def build_calculator(
    backend_id: str,
    method: dict[str, Any],
) -> tuple[Any, str | None, dict[str, Any]]:
    """Load the exact local calculator requested by the agent."""

    path, metadata = _model_path(backend_id, method["model"])
    device = str(method["device"]).strip().lower()
    if device not in {"cpu", "cuda"} and not device.startswith("cuda:"):
        raise ValueError("device must be cpu, cuda, or cuda:<index>")

    provenance = {
        "model_path": str(path),
        "model_resource": metadata or None,
        "device": device,
    }
    if backend_id in {"nequip", "allegro"}:
        from nequip.integrations.ase import NequIPCalculator

        calculator = NequIPCalculator._from_saved_model(
            path,
            device=device,
            chemical_species_to_atom_type_map=_nequip_mapping(
                method["chemical_species_mapping"]
            ),
            allow_tf32=bool(method["allow_tf32"]),
            neighborlist_backend=str(method.get("neighborlist_backend", "matscipy")),
        )
        provenance["allow_tf32"] = bool(method["allow_tf32"])
        provenance["chemical_species_mapping"] = method["chemical_species_mapping"]
        return calculator, module_version("nequip"), provenance

    if backend_id == "deepmd":
        if device != "cpu":
            raise ValueError(
                "This configured DeePMD runtime is CPU-only; choose device='cpu'"
            )
        from deepmd.calculator import DP

        head = _deepmd_head(path, method["model_branch"], metadata)
        calculator = DP(model=str(path), head=head)
        provenance["model_branch"] = method["model_branch"]
        provenance["resolved_model_branch"] = head or "single_task"
        return calculator, module_version("deepmd-kit"), provenance

    raise ValueError(f"Unsupported MLIP backend: {backend_id}")


def prepare_atoms(backend_id: str, atoms: Any, method: dict[str, Any]) -> None:
    """Attach explicit per-frame model inputs without choosing chemistry."""

    if backend_id != "deepmd":
        return
    import numpy as np

    atoms.info["charge_spin"] = np.asarray(
        [[float(method["charge"]), float(method["spin"])]], dtype=float
    )
    if method.get("frame_parameters") is not None:
        atoms.info["fparam"] = np.asarray(method["frame_parameters"], dtype=float)
