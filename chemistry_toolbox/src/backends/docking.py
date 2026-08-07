"""Docking action with explicit prepared inputs and search box."""

from __future__ import annotations

import re
from typing import Any

from .common import (
    command_artifacts,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    run_external,
    success,
    unavailable,
    unsupported,
)


ACTIONS = {"dock_ligand"}


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if action_id != "dock_ligand" or backend_id not in {"vina", "gnina"}:
        return unsupported(f"Unsupported docking action/backend combination: {action_id}/{backend_id}")
    inputs, method, settings = request_parts(request)
    receptor = resolve_input_file(inputs["receptor"])
    ligand = resolve_input_file(inputs["ligand"])
    search_space = inputs["search_space"]
    center = search_space["center_angstrom"]
    size = search_space["size_angstrom"]
    if len(center) != 3 or len(size) != 3 or any(float(value) <= 0 for value in size):
        raise ValueError("search_space center_angstrom/size_angstrom must contain three values and size must be positive")
    directory = output_directory(action_id, backend_id)
    poses = directory / "poses.pdbqt"
    arguments = [
        "--receptor", str(receptor), "--ligand", str(ligand),
        "--center_x", str(center[0]), "--center_y", str(center[1]), "--center_z", str(center[2]),
        "--size_x", str(size[0]), "--size_y", str(size[1]), "--size_z", str(size[2]),
        "--exhaustiveness", str(settings["exhaustiveness"]),
        "--num_modes", str(settings["num_modes"]),
        "--out", str(poses),
    ]
    if backend_id == "vina":
        arguments.extend(["--energy_range", str(settings["energy_range_kcal_mol"])])
    if backend_id == "gnina":
        cnn_model = str(method["cnn_model"]).strip()
        if cnn_model not in {"default", "builtin_default"}:
            arguments.extend(["--cnn", cnn_model])
        if method.get("cnn_scoring") is not None:
            arguments.extend(["--cnn_scoring", str(method["cnn_scoring"])])
        if method.get("scoring_function") is not None:
            arguments.extend(["--scoring", str(method["scoring_function"])])
        if bool(settings["use_gpu"]):
            if settings.get("gpu_device") is None:
                raise ValueError("GNINA use_gpu=true requires explicit gpu_device")
            arguments.extend(["--device", str(settings["gpu_device"])])
        else:
            arguments.append("--no_gpu")
        if settings.get("cpu") is not None:
            arguments.extend(["--cpu", str(settings["cpu"])])
        if settings.get("seed") is not None:
            arguments.extend(["--seed", str(settings["seed"])])
    completed = run_external(
        executable=backend_id,
        environment_variable="CHEMGRAPH_VINA_COMMAND" if backend_id == "vina" else "CHEMGRAPH_GNINA_COMMAND",
        arguments=arguments,
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 3600)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        install = "conda install -c conda-forge vina" if backend_id == "vina" else "Download GNINA and set CHEMGRAPH_GNINA_COMMAND"
        return unavailable(completed["stderr"], install=install)
    if completed["returncode"] != 0 or not poses.is_file():
        raise RuntimeError(f"{backend_id} docking failed: {completed['stderr'][-2000:]}")
    pose_text = poses.read_text(encoding="utf-8", errors="replace")
    score_matches = re.findall(r"REMARK VINA RESULT:\s+(-?\S+)\s+(-?\S+)\s+(-?\S+)", pose_text)
    scores = [
        {"pose_index": index + 1, "affinity_kcal_mol": float(values[0]), "rmsd_lb_angstrom": float(values[1]), "rmsd_ub_angstrom": float(values[2])}
        for index, values in enumerate(score_matches)
    ]
    if backend_id == "gnina" and not scores:
        models = re.findall(r"MODEL\s+(\d+)(.*?)(?:ENDMDL|\Z)", pose_text, flags=re.S)
        for model_index, block in models:
            affinity = re.search(r"REMARK\s+minimizedAffinity\s+([-+0-9.Ee]+)", block)
            cnn_score = re.search(r"REMARK\s+CNNscore\s+([-+0-9.Ee]+)", block)
            cnn_affinity = re.search(r"REMARK\s+CNNaffinity\s+([-+0-9.Ee]+)", block)
            if affinity or cnn_score or cnn_affinity:
                item: dict[str, Any] = {"pose_index": int(model_index)}
                if affinity:
                    item["affinity_kcal_mol"] = float(affinity.group(1))
                if cnn_score:
                    item["cnn_pose_score"] = float(cnn_score.group(1))
                if cnn_affinity:
                    item["cnn_affinity"] = float(cnn_affinity.group(1))
                scores.append(item)
    if not scores:
        table_matches = re.findall(r"^\s*(\d+)\s+(-?\d+\.\d+)\s+", completed["stdout"], re.M)
        scores = [{"pose_index": int(index), "affinity_kcal_mol": float(score)} for index, score in table_matches]
    result = {
        "poses_path": relative_workspace_path(poses),
        "scores": scores,
        "search_space": search_space,
    }
    if not scores:
        return partial_success(
            result,
            artifact_files=command_artifacts(directory),
            provenance={"command": completed["command"]},
            warnings=["Docking produced a pose file, but no affinity scores could be parsed."],
        )
    return success(
        result,
        artifact_files=command_artifacts(directory),
        provenance={"command": completed["command"]},
    )
