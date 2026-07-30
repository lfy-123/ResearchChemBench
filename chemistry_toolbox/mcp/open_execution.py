"""Auditable native-software and Agent-authored program execution tools."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from packaging.specifiers import SpecifierSet

from researchchem_toolbox.artifacts import ArtifactStore
from researchchem_toolbox.runtime import (
    runtime_environment,
    runtime_names,
    runtime_python,
)
from researchchem_toolbox.resource_budget import (
    ResourceBudgetExceeded,
    active_resource_jobs,
    active_resource_usage,
    normalize_resource_limits,
    reserve_resources,
    resource_budget_record,
    validate_resource_limits,
)
from researchchem_toolbox.timeout_policy import (
    timeout_policy_record,
    timeout_seconds_for,
)

from .execution_models import (
    AnalysisInputInspectionRequest,
    AnalysisJobRequest,
    ArtifactDeclarationRequest,
    ExecutionResourceRequest,
    JobCancelRequest,
    JobCollectRequest,
    JobStatusRequest,
    NativeJobRequest,
    StagedInput,
    WorkspaceTextReadRequest,
    WorkspaceTextWriteRequest,
)
from .software_catalog import native_command_guide, software_documentation_recovery
from .workspace import (
    relative_workspace_path,
    resolve_workspace_output_path,
    resolve_workspace_path,
    workspace_root,
)


JOB_ROOT = Path("outputs") / "execution_jobs"
TERMINAL_JOB_STATES = {"success", "failed", "timeout", "cancelled"}
SUPERVISOR_PATH = Path(__file__).with_name("job_supervisor.py")
JOB_CONTEXT_PATH = Path(__file__).with_name("researchchem_job.py")
SAFE_INHERITED_ENVIRONMENT = (
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TZ",
    "CUDA_VISIBLE_DEVICES",
    "ROCR_VISIBLE_DEVICES",
    "SLURM_JOB_ID",
    "SLURM_JOB_NODELIST",
    "SLURM_CPUS_PER_TASK",
    "SLURM_GPUS",
    "LM_LICENSE_FILE",
    "MLM_LICENSE_FILE",
)
MAX_INSPECTION_JSON_BYTES = 50 * 1024 * 1024


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _maximum_staged_bytes() -> int:
    raw = os.environ.get("RESEARCHCHEM_MAX_STAGED_INPUT_BYTES", "10737418240")
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError("RESEARCHCHEM_MAX_STAGED_INPUT_BYTES must be an integer") from exc
    if value <= 0:
        raise ValueError("RESEARCHCHEM_MAX_STAGED_INPUT_BYTES must be positive")
    return value


def _job_directory(job_id: str, *, must_exist: bool = True) -> Path:
    path = resolve_workspace_output_path(str(JOB_ROOT / job_id))
    if must_exist and not path.is_dir():
        raise KeyError(f"Unknown execution job {job_id!r}")
    return path


def _validate_argument_paths(arguments: list[str]) -> None:
    """Reject explicit host paths while allowing ordinary non-shell CLI syntax."""

    for argument in arguments:
        candidate = argument.split("=", 1)[1] if argument.startswith("-") and "=" in argument else argument
        candidate = candidate.strip()
        if not candidate:
            continue
        path = PurePosixPath(candidate.replace("\\", "/"))
        if path.is_absolute() or candidate.startswith("~") or ".." in path.parts:
            raise ValueError(
                f"Native arguments cannot reference absolute paths or '..': {argument!r}; "
                "stage the file and use its target_path instead"
            )


def _compute_resource_limits(request_limits) -> dict[str, Any]:
    resources = normalize_resource_limits(request_limits)
    validate_resource_limits(resources)
    resources["walltime_seconds"] = timeout_seconds_for("compute")
    return resources


def _resource_budget_error(exc: ResourceBudgetExceeded) -> dict[str, Any]:
    error = exc.as_error()
    availability = _resource_availability()
    error["blocking_resources"] = [
        name
        for name in ("cpu_cores", "memory_mb", "gpu_count")
        if int(error["requested"].get(name, 0)) > int(error["available"].get(name, 0))
    ]
    error["retry_condition"] = (
        "Retry after one of the listed active jobs reaches a terminal state, or submit a request "
        "that fits the reported available resources."
        if exc.aggregate
        else "Lower the request so every resource fits the fixed per-task budget."
    )
    return {
        "status": "invalid_request",
        "valid": False,
        "error": error,
        "evaluation_resource_budget": resource_budget_record(),
        "resource_availability": availability,
    }


def _analysis_failure(
    *,
    stage: str,
    code: str,
    message: str,
    file: str | None = None,
    line: int | None = None,
    evidence: str | None = None,
    candidate_fixes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "status": "invalid_request",
        "valid": False,
        "error": {
            "stage": stage,
            "code": code,
            "message": message,
            "file": file,
            "line": line,
            "evidence": evidence,
            "likely_cause": message,
            "candidate_fixes": candidate_fixes or [],
            "retryable": True,
        },
        "automatic_fallback": False,
    }


def _stage_inputs(job_directory: Path, items: list[Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    total_bytes = 0
    maximum = _maximum_staged_bytes()
    for item in items:
        source = resolve_workspace_path(item.source_path, must_exist=True)
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Staged input must be a regular non-symlink file: {item.source_path}")
        size = source.stat().st_size
        total_bytes += size
        if total_bytes > maximum:
            raise ValueError(
                f"Staged inputs exceed RESEARCHCHEM_MAX_STAGED_INPUT_BYTES={maximum}"
            )
        target = job_directory.joinpath(*PurePosixPath(item.target_path).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise ValueError(f"Duplicate or pre-existing staged target: {item.target_path}")
        shutil.copy2(source, target)
        records.append(
            {
                "source_path": relative_workspace_path(source),
                "target_path": item.target_path,
                "size_bytes": size,
                "sha256": _sha256(target),
            }
        )
    return records


def write_workspace_text(request: WorkspaceTextWriteRequest) -> dict[str, Any]:
    path = resolve_workspace_output_path(request.path)
    relative = Path(relative_workspace_path(path))
    if relative.parts[:2] == ("outputs", "execution_jobs"):
        raise ValueError(
            "Execution job directories are immutable through write_workspace_text; "
            "stage all inputs when submitting a new job"
        )
    if path.exists() and not request.overwrite:
        raise FileExistsError(
            f"Workspace file already exists: {relative_workspace_path(path)}; set overwrite=true explicitly"
        )
    if path.exists() and not path.is_file():
        raise ValueError(f"Workspace text target is not a regular file: {request.path}")
    temporary = path.with_name(path.name + f".tmp-{uuid.uuid4().hex}")
    temporary.write_text(request.content, encoding="utf-8")
    os.replace(temporary, path)
    return {
        "status": "success",
        "path": relative_workspace_path(path),
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "encoding": "utf-8",
    }


def read_workspace_text(request: WorkspaceTextReadRequest) -> dict[str, Any]:
    path = resolve_workspace_path(request.path, must_exist=True)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Workspace text source is not a regular file: {request.path}")
    text = path.read_text(encoding="utf-8")
    truncated = len(text) > request.max_chars
    return {
        "status": "success",
        "path": relative_workspace_path(path),
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "encoding": "utf-8",
        "truncated": truncated,
        "content": text[: request.max_chars],
    }


def _validate_pysisyphus_input_deck(
    request: NativeJobRequest,
    guide: dict[str, Any],
) -> dict[str, Any]:
    """Validate pysisyphus' versioned YAML mechanics without choosing chemistry."""

    staged = {item.target_path: item.source_path for item in request.staged_inputs}
    config_targets = [
        argument
        for argument in request.arguments
        if argument in staged and PurePosixPath(argument).suffix.lower() in {".yaml", ".yml"}
    ]
    if len(config_targets) != 1:
        raise ValueError(
            "pysisyphus/pysis requires exactly one staged .yaml or .yml argument; "
            "the argument must equal that file's staged target_path"
        )
    config_target = config_targets[0]
    source = resolve_workspace_path(staged[config_target], must_exist=True)
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"pysisyphus config must be a regular non-symlink file: {source}")
    if source.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("pysisyphus config exceeds the 10 MiB structural-validation limit")
    try:
        value = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"pysisyphus config is not valid UTF-8 YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("pysisyphus config must be a YAML mapping at the top level")

    contract = guide.get("configuration_contract") or {}
    allowed = set(contract.get("valid_top_level_sections") or [])
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError(
            "pysisyphus 1.0.0 config has invalid top-level section(s) "
            f"{unknown}; endpoint structures belong in geom.fn, not an endpoints section"
        )
    geom = value.get("geom")
    if not isinstance(geom, dict) or not geom.get("fn"):
        raise ValueError(
            "pysisyphus 1.0.0 requires geom.fn to name one structure, a trajectory, "
            "or a list of endpoint structures"
        )

    cos = value.get("cos")
    if cos is not None:
        if not isinstance(cos, dict):
            raise ValueError("pysisyphus cos must be a YAML mapping")
        invalid_cos = sorted(set(cos) & {"images", "endpoints", "fixendpoints"})
        if invalid_cos:
            raise ValueError(
                "pysisyphus 1.0.0 cos contains unsupported field(s) "
                f"{invalid_cos}; put images/endpoints in geom.fn and use fix_first/fix_last"
            )
        opt = value.get("opt")
        if not isinstance(opt, dict) or not opt.get("type"):
            raise ValueError("a pysisyphus chain-of-states config requires opt.type")
        path_optimizers = set(
            (contract.get("common_exact_values") or {}).get("path_optimizer_types") or []
        )
        if path_optimizers and opt["type"] not in path_optimizers:
            raise ValueError(
                f"pysisyphus opt.type={opt['type']!r} is not a supported path optimizer; "
                f"select explicitly from {sorted(path_optimizers)}"
            )

    references = geom["fn"] if isinstance(geom["fn"], list) else [geom["fn"]]
    missing = []
    for reference in references:
        if not isinstance(reference, str):
            continue
        suffix = PurePosixPath(reference).suffix.lower()
        if suffix in {".xyz", ".trj", ".pdb", ".mol", ".sdf", ".cif"} and reference not in staged:
            missing.append(reference)
    if missing:
        raise ValueError(
            "pysisyphus geom.fn references files absent from staged_inputs: "
            f"{sorted(missing)}"
        )
    return {
        "software_version": str(contract.get("tested_version") or "unknown"),
        "config_target": config_target,
        "top_level_sections": sorted(value),
        "referenced_geometry_targets": references,
    }


def _staged_sources(request: NativeJobRequest) -> dict[str, Path]:
    return {
        item.target_path: resolve_workspace_path(item.source_path, must_exist=True)
        for item in request.staged_inputs
    }


def _read_staged_text(
    sources: dict[str, Path], target: str, *, software_id: str
) -> str:
    source = sources.get(target)
    if source is None:
        raise ValueError(
            f"{software_id}_missing_staged_input: {target!r} must be present in staged_inputs"
        )
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"{software_id}_invalid_input_file: {target!r} is not a regular file")
    if source.stat().st_size > 10 * 1024 * 1024:
        raise ValueError(f"{software_id}_input_too_large: {target!r} exceeds 10 MiB lint limit")
    try:
        return source.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{software_id}_input_encoding: {target!r} must be UTF-8 text") from exc


def _validate_orca_input_deck(request: NativeJobRequest) -> dict[str, Any]:
    sources = _staged_sources(request)
    targets = [argument for argument in request.arguments if argument in sources]
    if len(targets) != 1 or PurePosixPath(targets[0]).suffix.casefold() != ".inp":
        raise ValueError(
            "orca_input_argument: ORCA requires exactly one staged .inp argument matching target_path"
        )
    target = targets[0]
    text = _read_staged_text(sources, target, software_id="orca")
    lines = [line.strip() for line in text.splitlines()]
    first = next((line for line in lines if line), "")
    if not first.startswith("!"):
        raise ValueError("orca_keyword_line: first non-empty input line must start with '!'")
    block_names = {
        "basis", "casscf", "cpcm", "elprop", "freq", "geom", "mdci", "method",
        "output", "pal", "plots", "rel", "scf", "tddft",
    }
    stack: list[tuple[str, int]] = []
    for line_number, line in enumerate(lines, start=1):
        match = re.match(r"^%([a-z0-9_]+)\b(.*)$", line, flags=re.IGNORECASE)
        if match and match.group(1).casefold() in block_names:
            if re.search(r"\bend\s*$", match.group(2), flags=re.IGNORECASE):
                continue
            stack.append((match.group(1).casefold(), line_number))
        elif line.casefold() == "end" and stack:
            stack.pop()
    if stack:
        name, line_number = stack[-1]
        raise ValueError(
            f"orca_unclosed_block: %{name} opened on line {line_number} has no matching end"
        )
    coordinate_headers = [index for index, line in enumerate(lines) if re.match(r"^\*\s+xyz(file)?\b", line, re.I)]
    for index in coordinate_headers:
        if not any(line == "*" for line in lines[index + 1 :]):
            raise ValueError(
                f"orca_unclosed_coordinates: coordinate section opened on line {index + 1} has no final '*'"
            )
    parallel = re.search(r"%pal\s+.*?nprocs\s+(\d+)", text, flags=re.I | re.S)
    if parallel and int(parallel.group(1)) > request.resource_limits.cpu_cores:
        raise ValueError(
            "orca_cpu_mismatch: %pal nprocs exceeds resource_limits.cpu_cores"
        )
    keyword_text = first.casefold()
    has_frequency = bool(re.search(r"\bfreq\b", keyword_text))
    has_transition_state = bool(re.search(r"\boptts\b", keyword_text))
    has_optimization = has_transition_state or bool(re.search(r"\bopt\b", keyword_text))
    if has_transition_state:
        calculation_intent = "transition_state"
    elif has_optimization and has_frequency:
        calculation_intent = "optimization_frequency"
    elif has_optimization:
        calculation_intent = "geometry_optimization"
    elif has_frequency:
        calculation_intent = "frequency"
    else:
        calculation_intent = "single_point"
    return {
        "lint_profile": "orca_high_frequency_v1",
        "input_target": target,
        "keyword_line": first,
        "calculation_intent": calculation_intent,
        "coordinate_section_count": len(coordinate_headers),
        "checks": ["keyword_line", "block_closure", "coordinate_closure", "cpu_mapping"],
    }


def _gaussian_segment_sections(segment: str, segment_number: int) -> dict[str, Any]:
    lines = segment.splitlines()
    route_start = next((index for index, line in enumerate(lines) if line.lstrip().startswith("#")), None)
    if route_start is None:
        raise ValueError(f"gaussian_route_missing: Link1 segment {segment_number} has no route section")
    route_end = next((index for index in range(route_start + 1, len(lines)) if not lines[index].strip()), None)
    if route_end is None:
        raise ValueError(
            f"gaussian_route_separator: Link1 segment {segment_number} needs a blank line after the route"
        )
    route = " ".join(line.strip() for line in lines[route_start:route_end])
    route_normalized = route.casefold()
    has_frequency = bool(re.search(r"(?:^|[\s,])freq(?:\b|=)", route_normalized))
    has_optimization = bool(re.search(r"(?:^|[\s,])opt(?:\b|=)", route_normalized))
    has_transition_state = has_optimization and bool(
        re.search(r"opt\s*=\s*(?:\([^)]*\bts\b|ts\b)", route_normalized)
    )
    if has_transition_state:
        calculation_intent = "transition_state"
    elif has_optimization and has_frequency:
        calculation_intent = "optimization_frequency"
    elif has_optimization:
        calculation_intent = "geometry_optimization"
    elif has_frequency:
        calculation_intent = "frequency"
    else:
        calculation_intent = "single_point"
    if "geom=allcheck" in route_normalized:
        return {
            "route": route,
            "geometry_source": "checkpoint",
            "calculation_intent": calculation_intent,
        }
    cursor = route_end + 1
    title_start = next((index for index in range(cursor, len(lines)) if lines[index].strip()), None)
    if title_start is None:
        raise ValueError(f"gaussian_title_missing: Link1 segment {segment_number} has no title")
    title_end = next((index for index in range(title_start + 1, len(lines)) if not lines[index].strip()), None)
    if title_end is None:
        raise ValueError(
            f"gaussian_title_separator: Link1 segment {segment_number} needs a blank line after the title"
        )
    molecule_start = next((index for index in range(title_end + 1, len(lines)) if lines[index].strip()), None)
    if molecule_start is None or not re.fullmatch(r"[+-]?\d+\s+\d+", lines[molecule_start].strip()):
        raise ValueError(
            f"gaussian_charge_multiplicity: Link1 segment {segment_number} needs 'charge multiplicity'"
        )
    coordinate_end = next(
        (index for index in range(molecule_start + 1, len(lines)) if not lines[index].strip()),
        None,
    )
    if coordinate_end is None or coordinate_end == molecule_start + 1:
        raise ValueError(
            f"gaussian_coordinate_separator: Link1 segment {segment_number} needs coordinates and a final blank line"
        )
    return {
        "route": route,
        "geometry_source": "coordinates",
        "calculation_intent": calculation_intent,
    }


def _validate_gaussian_input_deck(request: NativeJobRequest) -> dict[str, Any]:
    if request.stdin_target is None:
        raise ValueError("gaussian_stdin: g16 requires stdin_target")
    sources = _staged_sources(request)
    text = _read_staged_text(sources, request.stdin_target, software_id="gaussian")
    if not text.endswith("\n"):
        raise ValueError("gaussian_final_newline: Gaussian input must end with a newline")
    segments = re.split(r"^[ \t]*--Link1--[ \t]*$", text, flags=re.MULTILINE)
    parsed = [
        _gaussian_segment_sections(segment, index)
        for index, segment in enumerate(segments, start=1)
    ]
    nproc = re.findall(r"^\s*%NProcShared\s*=\s*(\d+)", text, flags=re.I | re.M)
    if any(int(value) > request.resource_limits.cpu_cores for value in nproc):
        raise ValueError(
            "gaussian_cpu_mismatch: %NProcShared exceeds resource_limits.cpu_cores"
        )
    memory = re.findall(r"^\s*%Mem\s*=\s*(\d+(?:\.\d+)?)\s*(KB|MB|GB|TB)", text, flags=re.I | re.M)
    factors = {"KB": 1 / 1024, "MB": 1, "GB": 1024, "TB": 1024 * 1024}
    if any(float(value) * factors[unit.upper()] > request.resource_limits.memory_mb for value, unit in memory):
        raise ValueError("gaussian_memory_mismatch: %Mem exceeds resource_limits.memory_mb")
    step_intents = [item["calculation_intent"] for item in parsed]
    if "transition_state" in step_intents:
        calculation_intent = "transition_state"
    elif "optimization_frequency" in step_intents or {
        "geometry_optimization",
        "frequency",
    }.issubset(step_intents):
        calculation_intent = "optimization_frequency"
    elif "geometry_optimization" in step_intents:
        calculation_intent = "geometry_optimization"
    elif "frequency" in step_intents:
        calculation_intent = "frequency"
    else:
        calculation_intent = "single_point"
    return {
        "lint_profile": "gaussian_high_frequency_v1",
        "input_target": request.stdin_target,
        "link1_segment_count": len(parsed),
        "segments": parsed,
        "calculation_intent": calculation_intent,
        "checks": ["route", "blank_lines", "title", "molecule", "cpu_mapping", "memory_mapping"],
    }


def _validate_crest_invocation(request: NativeJobRequest) -> dict[str, Any]:
    sources = _staged_sources(request)
    xyz_targets = [
        argument
        for argument in request.arguments
        if argument in sources and PurePosixPath(argument).suffix.casefold() == ".xyz"
    ]
    if len(xyz_targets) != 1:
        raise ValueError(
            "crest_xyz_argument: CREST requires exactly one staged XYZ positional argument"
        )
    intent_by_flag = {
        "-protonate": "protonation",
        "--protonate": "protonation",
        "-deprotonate": "deprotonation",
        "--deprotonate": "deprotonation",
        "-tautomerize": "tautomerization",
        "--tautomerize": "tautomerization",
    }
    selected_flags = sorted(
        set(intent_by_flag) & {item.casefold() for item in request.arguments}
    )
    selected_intents = sorted({intent_by_flag[item] for item in selected_flags})
    if len(selected_intents) > 1:
        raise ValueError(
            f"crest_conflicting_modes: choose only one of {selected_flags}"
        )
    for flag in ("--t", "-t"):
        lowered = [item.casefold() for item in request.arguments]
        if flag in lowered:
            index = lowered.index(flag)
            if index + 1 >= len(request.arguments) or not request.arguments[index + 1].isdigit():
                raise ValueError("crest_thread_argument: --T requires a positive integer")
            if int(request.arguments[index + 1]) > request.resource_limits.cpu_cores:
                raise ValueError("crest_cpu_mismatch: --T exceeds resource_limits.cpu_cores")
    text = _read_staged_text(sources, xyz_targets[0], software_id="crest")
    lines = text.splitlines()
    if not lines or not lines[0].strip().isdigit() or len(lines) < int(lines[0]) + 2:
        raise ValueError("crest_xyz_format: XYZ atom count does not match the coordinate records")
    calculation_intent = selected_intents[0] if selected_intents else "conformer_search"
    return {
        "lint_profile": "crest_high_frequency_v1",
        "input_target": xyz_targets[0],
        "selected_mode": selected_flags[0] if selected_flags else "conformer_search",
        "calculation_intent": calculation_intent,
        "checks": ["xyz_format", "mode_exclusivity", "cpu_mapping"],
    }


def _validate_goodvibes_invocation(request: NativeJobRequest) -> dict[str, Any]:
    if any(
        argument.casefold() in {"-h", "--help", "-v", "--version"}
        for argument in request.arguments
    ):
        return {
            "lint_profile": "goodvibes_native_v1",
            "input_targets": [],
            "calculation_intent": "startup_probe",
            "checks": ["help_or_version_probe"],
        }
    sources = _staged_sources(request)
    positional_targets = [argument for argument in request.arguments if argument in sources]
    if not positional_targets:
        raise ValueError(
            "goodvibes_input_argument: GoodVibes requires at least one explicitly staged "
            "quantum-output positional argument"
        )
    unsafe = [
        target
        for target in positional_targets
        if PurePosixPath(target).parent != PurePosixPath(".")
        or not re.fullmatch(r"[A-Za-z0-9_.+,-]+", target)
    ]
    if unsafe:
        raise ValueError(
            "goodvibes_unsafe_staged_target: GoodVibes performs its own filename pattern "
            f"handling and cannot reliably consume staged targets {unsafe}. Stage each input "
            "under a flat basename containing only letters, digits, dot, underscore, plus, "
            "comma, or hyphen, then pass that exact target in arguments."
        )
    return {
        "lint_profile": "goodvibes_native_v1",
        "input_targets": positional_targets,
        "calculation_intent": "other",
        "checks": ["staged_positional_inputs", "safe_flat_basenames"],
    }


def _require_fixed_targets(
    request: NativeJobRequest, software_id: str, required: set[str]
) -> dict[str, Path]:
    sources = _staged_sources(request)
    missing = sorted(required - set(sources))
    if missing:
        raise ValueError(
            f"{software_id}_missing_fixed_files: stage exact target names {missing}"
        )
    empty = sorted(target for target in required if sources[target].stat().st_size == 0)
    if empty:
        raise ValueError(f"{software_id}_empty_fixed_files: {empty}")
    return sources


def _validate_vasp_inputs(request: NativeJobRequest) -> dict[str, Any]:
    sources = _require_fixed_targets(request, "vasp", {"INCAR", "POSCAR", "POTCAR", "KPOINTS"})
    incar_text = _read_staged_text(sources, "INCAR", software_id="vasp")
    poscar = _read_staged_text(sources, "POSCAR", software_id="vasp").splitlines()
    if len(poscar) < 8:
        raise ValueError("vasp_poscar_structure: POSCAR is too short")
    species = poscar[5].split()
    counts_line = poscar[6].split()
    if species and all(re.fullmatch(r"[+-]?\d+", item) for item in species):
        counts_line = species
        species = []
    if not counts_line or not all(item.isdigit() and int(item) > 0 for item in counts_line):
        raise ValueError("vasp_poscar_counts: POSCAR species counts are invalid")
    if species and len(species) != len(counts_line):
        raise ValueError("vasp_poscar_species: element and count fields have different lengths")
    potcar = _read_staged_text(sources, "POTCAR", software_id="vasp")
    datasets = max(len(re.findall(r"^\s*TITEL\s*=", potcar, flags=re.M)), len(re.findall(r"^\s*VRHFIN\s*=", potcar, flags=re.M)))
    if species and datasets and datasets != len(species):
        raise ValueError(
            "vasp_potcar_order: POTCAR dataset count does not match POSCAR element count"
        )
    incar_values: dict[str, str] = {}
    for raw_line in incar_text.splitlines():
        active = raw_line.split("!", 1)[0].split("#", 1)[0].strip()
        if "=" not in active:
            continue
        key, value = active.split("=", 1)
        incar_values[key.strip().upper()] = value.strip()
    try:
        ibrion = int(float(incar_values.get("IBRION", "-1")))
        nsw = int(float(incar_values.get("NSW", "0")))
    except ValueError as exc:
        raise ValueError("vasp_incar_integer: IBRION and NSW must be integer values") from exc
    if ibrion in {5, 6, 7, 8}:
        calculation_intent = "frequency"
    elif nsw > 0 and ibrion >= 0:
        calculation_intent = "ionic_relaxation"
    else:
        calculation_intent = "single_point"
    return {
        "lint_profile": "vasp_high_frequency_v1",
        "required_targets": sorted(sources),
        "species": species,
        "atom_count": sum(int(item) for item in counts_line),
        "potcar_dataset_count": datasets,
        "incar_ibrion": ibrion,
        "incar_nsw": nsw,
        "calculation_intent": calculation_intent,
        "checks": ["fixed_files", "poscar_counts", "potcar_dataset_count"],
    }


def _validate_lobster_inputs(request: NativeJobRequest) -> dict[str, Any]:
    required = {
        "lobsterin", "POSCAR", "POTCAR", "WAVECAR", "CONTCAR", "KPOINTS",
        "OUTCAR", "vasprun.xml",
    }
    sources = _require_fixed_targets(request, "lobster", required)
    lobsterin = _read_staged_text(sources, "lobsterin", software_id="lobster")
    if not any(line.strip() and not line.lstrip().startswith(("!", "#")) for line in lobsterin.splitlines()):
        raise ValueError("lobster_input_empty: lobsterin contains no active directives")
    return {
        "lint_profile": "lobster_high_frequency_v1",
        "required_targets": sorted(required),
        "wavecar_size_bytes": sources["WAVECAR"].stat().st_size,
        "calculation_intent": "projection",
        "checks": ["fixed_files", "nonempty_wavecar", "active_lobsterin"],
        "compatibility_boundary": (
            "File presence is validated mechanically. VASP/LOBSTER version, PAW basis, band, "
            "k-point, and projection compatibility still require software output checks."
        ),
    }


def _validate_native_input_deck(
    request: NativeJobRequest, guide: dict[str, Any]
) -> dict[str, Any] | None:
    key = (guide["software_id"], request.executable)
    if key == ("pysisyphus", "pysis"):
        return _validate_pysisyphus_input_deck(request, guide)
    if key == ("orca", "orca"):
        return _validate_orca_input_deck(request)
    if key == ("gaussian", "g16"):
        return _validate_gaussian_input_deck(request)
    if key == ("crest", "crest"):
        return _validate_crest_invocation(request)
    if key == ("vasp", "vasp_std"):
        return _validate_vasp_inputs(request)
    if key == ("lobster", "lobster-5.1.0"):
        return _validate_lobster_inputs(request)
    if key == ("goodvibes", "goodvibes"):
        return _validate_goodvibes_invocation(request)
    return None


def _intent_is_compatible(
    software_id: str, declared: str, inferred: str
) -> bool:
    if declared in {"other", inferred}:
        return True
    aliases = {
        ("vasp", "geometry_optimization", "ionic_relaxation"),
        ("vasp", "ionic_relaxation", "geometry_optimization"),
    }
    return (software_id, declared, inferred) in aliases


def validate_native_job(request: NativeJobRequest) -> dict[str, Any]:
    guide = native_command_guide(request.software_id, request.executable)
    if not guide.get("resolved_path"):
        return {
            "status": "unavailable",
            "software_id": guide["software_id"],
            "executable": request.executable,
            "runtime": guide["runtime"],
            "error": {
                "code": "executable_missing",
                "message": (
                    f"Configured executable {request.executable!r} is not available in "
                    f"runtime {guide['runtime']!r}"
                ),
            },
            "invocation_guide": guide,
            "documentation_recovery": software_documentation_recovery(
                guide["software_id"], failed=True
            ),
        }
    _validate_argument_paths(request.arguments)
    targets = {item.target_path for item in request.staged_inputs}
    input_mode = str(guide.get("input_mode") or "")
    if input_mode in {"stdin_file", "arguments_and_stdin_file"} and request.stdin_target is None:
        raise ValueError(
            f"{request.software_id}/{request.executable} uses {input_mode}; stdin_target is required"
        )
    if request.stdin_target is not None and request.stdin_target not in targets:
        raise ValueError("stdin_target must be one of the explicitly staged target paths")
    input_deck_validation = _validate_native_input_deck(request, guide)
    inferred_intent = (
        str(input_deck_validation.get("calculation_intent"))
        if input_deck_validation and input_deck_validation.get("calculation_intent")
        else None
    )
    if (
        request.calculation_intent
        and inferred_intent
        and not _intent_is_compatible(
            request.software_id, request.calculation_intent, inferred_intent
        )
    ):
        raise ValueError(
            "calculation_intent_mismatch: declared calculation_intent "
            f"{request.calculation_intent!r} conflicts with inferred intent {inferred_intent!r}. "
            f"Use calculation_intent={inferred_intent!r}, omit calculation_intent to accept "
            "the validated inference, or correct the input deck if the inference is wrong."
        )
    calculation_intent = inferred_intent or request.calculation_intent or "unknown"
    try:
        resources = _compute_resource_limits(request.resource_limits)
    except ResourceBudgetExceeded as exc:
        return _resource_budget_error(exc)
    return {
        "status": "success",
        "valid": True,
        "software_id": guide["software_id"],
        "runtime": guide["runtime"],
        "resolved_executable": guide["resolved_path"],
        "command": [guide["resolved_path"], *request.arguments],
        "staged_targets": sorted(targets),
        "stdin_target": request.stdin_target,
        "input_deck_validation": input_deck_validation,
        "calculation_intent": calculation_intent,
        "resource_limits": resources,
        "execution_timeout_policy": timeout_policy_record("compute"),
        "evaluation_resource_budget": resource_budget_record(),
        "resource_availability": _resource_availability(),
        "invocation_guide": guide,
        "documentation_recovery": software_documentation_recovery(
            guide["software_id"]
        ),
        "validation_boundary": (
            "Validation confirms the allowlisted executable, argv/path safety, staging map, "
            "stdin contract, mechanical resources, and any declared version-specific input-deck "
            "syntax. It does not judge scientific correctness or add missing scientific settings."
        ),
    }


def _job_environment(
    runtime: str,
    job_id: str,
    job_directory: Path,
    resources: dict[str, Any],
    resource_allocation: dict[str, Any],
    *,
    job_type: str,
) -> dict[str, str]:
    inherited = {
        name: os.environ[name]
        for name in SAFE_INHERITED_ENVIRONMENT
        if os.environ.get(name)
    }
    environment = {**inherited, **runtime_environment(runtime)}
    allocated_cpu_ids = [
        int(item) for item in resource_allocation.get("cpu_ids") or []
    ]
    if allocated_cpu_ids:
        allocated_cpu_list = ",".join(str(item) for item in allocated_cpu_ids)
        environment["OMPI_MCA_hwloc_base_cpu_list"] = allocated_cpu_list
        environment["PRTE_MCA_hwloc_default_cpu_list"] = allocated_cpu_list
    cpu_cores = resources.get("cpu_cores")
    if cpu_cores is not None:
        threads = str(max(1, int(cpu_cores)))
        for variable in (
            "OMP_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
        ):
            environment[variable] = threads
        if job_type == "native_software":
            # Native chemistry programs receive their explicit process/thread
            # count in the Agent-authored argv/input and through OMP.  A second
            # OpenBLAS/NumExpr pool is nested parallelism rather than additional
            # requested capacity, so keep it serial inside that outer pool.
            environment["OPENBLAS_NUM_THREADS"] = "1"
            environment["NUMEXPR_NUM_THREADS"] = "1"
    gpu_count = int(resources.get("gpu_count") or 0)
    allocated_gpu_ids = [
        str(item) for item in resource_allocation.get("gpu_ids") or []
    ]
    if gpu_count == 0:
        environment["CUDA_VISIBLE_DEVICES"] = ""
        environment["ROCR_VISIBLE_DEVICES"] = ""
    else:
        for variable in ("CUDA_VISIBLE_DEVICES", "ROCR_VISIBLE_DEVICES"):
            visible = [
                item.strip()
                for item in environment.get(variable, "").split(",")
                if item.strip()
            ]
            selected = allocated_gpu_ids or (
                visible[:gpu_count] if visible else list(map(str, range(gpu_count)))
            )
            environment[variable] = ",".join(selected)
    temporary = job_directory / ".tmp"
    home = job_directory / ".home"
    temporary.mkdir(parents=True, exist_ok=True)
    home.mkdir(parents=True, exist_ok=True)
    environment.setdefault("HOME", str(home))
    environment.update(
        {
            "TMPDIR": str(temporary),
            "MPLCONFIGDIR": str(temporary / "matplotlib"),
            "RESEARCHCHEM_EXECUTION_JOB_ID": job_id,
            "RESEARCHCHEM_EXECUTION_JOB_DIRECTORY": str(job_directory),
            "RESEARCHCHEM_JOB_ROOT": str(job_directory),
            "RESEARCHCHEM_JOB_INPUTS": str(job_directory / "inputs"),
            "RESEARCHCHEM_JOB_OUTPUTS": str(job_directory / "outputs"),
            "RESEARCHCHEM_JOB_REPORT": str(job_directory / "report"),
        }
    )
    if job_type == "programmable_analysis":
        framework_paths = []
        for raw_path in environment.get("PYTHONPATH", "").split(os.pathsep):
            if not raw_path:
                continue
            normalized = raw_path.replace("\\", "/").casefold()
            if (
                "site-packages" in normalized
                or "/.tool_env" in normalized
                or "/.venv" in normalized
            ):
                continue
            if raw_path not in framework_paths:
                framework_paths.append(raw_path)
        environment["PYTHONPATH"] = os.pathsep.join(
            [str(job_directory), *framework_paths]
        )
        environment["PYTHONNOUSERSITE"] = "1"
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def _start_job(
    *,
    job_type: str,
    runtime: str,
    command: list[str],
    stdin_target: str | None,
    staged_inputs: list[Any],
    resource_limits: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    try:
        reservation = reserve_resources(
            resource_limits,
            kind=job_type,
            label=str(metadata.get("label") or command[0]),
        )
    except ResourceBudgetExceeded as exc:
        return _resource_budget_error(exc)
    try:
        return _start_reserved_job(
            job_type=job_type,
            runtime=runtime,
            command=command,
            stdin_target=stdin_target,
            staged_inputs=staged_inputs,
            resource_limits=reservation.resource_limits
            | {"walltime_seconds": resource_limits["walltime_seconds"]},
            resource_allocation=reservation.resource_allocation,
            metadata={
                **metadata,
                "evaluation_resource_budget": resource_budget_record(),
            },
        )
    finally:
        reservation.release()


def _start_reserved_job(
    *,
    job_type: str,
    runtime: str,
    command: list[str],
    stdin_target: str | None,
    staged_inputs: list[Any],
    resource_limits: dict[str, Any],
    resource_allocation: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    job_id = f"job_{uuid.uuid4().hex}"
    job_directory = _job_directory(job_id, must_exist=False)
    job_directory.mkdir(parents=True, exist_ok=False)
    if job_type == "programmable_analysis":
        for name in ("code", "inputs", "outputs", "report", "logs"):
            (job_directory / name).mkdir()
        shutil.copy2(JOB_CONTEXT_PATH, job_directory / "researchchem_job.py")
        _atomic_json(
            job_directory / "analysis_contract.json",
            dict(metadata.get("analysis_contract") or {}),
        )
    try:
        staged_records = _stage_inputs(job_directory, staged_inputs)
    except Exception:
        shutil.rmtree(job_directory, ignore_errors=True)
        raise
    stdin_path = str(job_directory / stdin_target) if stdin_target else None
    stdout_path = job_directory / "stdout.log"
    stderr_path = job_directory / "stderr.log"
    stdout_path.touch()
    stderr_path.touch()
    submitted_at = _now()
    request_record = {
        "schema_version": 1,
        "job_id": job_id,
        "job_type": job_type,
        "runtime": runtime,
        "command": command,
        "stdin_target": stdin_target,
        "staged_inputs": staged_records,
        "resource_limits": resource_limits,
        "resource_allocation": resource_allocation,
        "metadata": metadata,
        "submitted_at": submitted_at,
        "automatic_fallback": False,
        "shell": False,
    }
    request_path = job_directory / "request.json"
    _atomic_json(request_path, request_record)
    status_path = job_directory / "status.json"
    relative_directory = relative_workspace_path(job_directory)
    status = {
        "schema_version": 1,
        "job_id": job_id,
        "job_type": job_type,
        "status": "queued",
        "supervisor_pid": None,
        "command": command,
        "job_directory": relative_directory,
        "stdout_path": relative_workspace_path(stdout_path),
        "stderr_path": relative_workspace_path(stderr_path),
        "resource_limits": resource_limits,
        "resource_allocation": resource_allocation,
        "submitted_at": submitted_at,
        "metadata": metadata,
    }
    _atomic_json(status_path, status)
    supervisor_spec = {
        **request_record,
        "evaluation_resource_budget": resource_budget_record(),
        "job_directory": str(job_directory),
        "relative_job_directory": relative_directory,
        "status_path": str(status_path),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "relative_stdout_path": relative_workspace_path(stdout_path),
        "relative_stderr_path": relative_workspace_path(stderr_path),
        "stdin_path": stdin_path,
    }
    spec_path = job_directory / "supervisor_spec.json"
    _atomic_json(spec_path, supervisor_spec)
    environment = _job_environment(
        runtime,
        job_id,
        job_directory,
        resource_limits,
        resource_allocation,
        job_type=job_type,
    )
    try:
        supervisor = subprocess.Popen(
            [sys.executable, str(SUPERVISOR_PATH), str(spec_path)],
            cwd=job_directory,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=environment,
            shell=False,
            start_new_session=True,
            close_fds=True,
        )
    except Exception as exc:
        status.update(
            {
                "status": "failed",
                "finished_at": _now(),
                "error": {"code": "supervisor_start_failed", "message": str(exc)},
            }
        )
        _atomic_json(status_path, status)
        return {"status": "failed", **status}
    return {
        "status": "success",
        "job_id": job_id,
        "job_status": "queued",
        "job_type": job_type,
        "runtime": runtime,
        "job_directory": relative_directory,
        "status_path": relative_workspace_path(status_path),
        "stdout_path": relative_workspace_path(stdout_path),
        "stderr_path": relative_workspace_path(stderr_path),
        "command": command,
        "staged_inputs": staged_records,
        "resource_limits": resource_limits,
        "resource_allocation": resource_allocation,
        "supervisor_pid": supervisor.pid,
        "automatic_fallback": False,
        "evaluation_resource_budget": resource_budget_record(),
        "next_step": "Call get_execution_job with this exact job_id to inspect state and logs.",
    }


def submit_native_job(request: NativeJobRequest) -> dict[str, Any]:
    validation = validate_native_job(request)
    if validation["status"] != "success":
        return validation
    guide = validation["invocation_guide"]
    return _start_job(
        job_type="native_software",
        runtime=validation["runtime"],
        command=validation["command"],
        stdin_target=request.stdin_target,
        staged_inputs=request.staged_inputs,
        resource_limits=dict(validation["resource_limits"]),
        metadata={
            "software_id": validation["software_id"],
            "executable": request.executable,
            "label": request.label,
            "parent_job_id": request.parent_job_id,
            "calculation_intent": validation["calculation_intent"],
            "input_deck_validation": validation["input_deck_validation"],
            "invocation_synopsis": guide.get("synopsis"),
            "execution_timeout_policy": timeout_policy_record("compute"),
        },
    )


def _analysis_imports(tree: ast.AST) -> list[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return sorted(names)


def _attribute_chain(node: ast.AST) -> list[str]:
    values: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        values.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        values.append(current.id)
    return list(reversed(values))


def _job_context_compliance(
    tree: ast.AST, request: AnalysisJobRequest
) -> dict[str, Any]:
    imported = False
    context_names: set[str] = set()
    helper_calls: dict[str, set[str]] = {
        "input": set(),
        "output": set(),
        "write_json": set(),
        "register_output": set(),
    }
    bypass_findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "researchchem_job":
            imported = imported or any(alias.name == "JobContext" for alias in node.names)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            chain = _attribute_chain(node.value.func)
            if chain[-2:] == ["JobContext", "load"]:
                context_names.update(
                    target.id for target in node.targets if isinstance(target, ast.Name)
                )
        chain = _attribute_chain(node)
        if (
            len(chain) >= 3
            and chain[0] in context_names
            and chain[1] == "root"
            and chain[2] in {"parent", "parents"}
        ):
            bypass_findings.append(
                {
                    "line": getattr(node, "lineno", None),
                    "expression": ".".join(chain),
                    "reason": "walks from the isolated job root toward the benchmark workspace",
                }
            )
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        call_chain = _attribute_chain(node.func)
        if len(call_chain) != 2 or call_chain[0] not in context_names:
            continue
        helper = call_chain[1]
        if helper not in helper_calls or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            helper_calls[helper].add(first.value)

    declared_inputs = {item.name for item in request.inputs}
    declared_outputs = {item.name for item in request.outputs}
    used_outputs = (
        helper_calls["output"]
        | helper_calls["write_json"]
        | helper_calls["register_output"]
    )
    missing_input_helpers = sorted(declared_inputs - helper_calls["input"])
    missing_output_helpers = sorted(declared_outputs - used_outputs)
    unknown_input_helpers = sorted(helper_calls["input"] - declared_inputs)
    unknown_output_helpers = sorted(used_outputs - declared_outputs)
    if not imported:
        status = "not_adopted"
    elif bypass_findings:
        status = "bypassed"
    elif unknown_input_helpers or unknown_output_helpers:
        status = "invalid"
    elif not missing_input_helpers and not missing_output_helpers:
        status = "compliant"
    else:
        status = "partial"
    warnings = []
    if status == "not_adopted":
        warnings.append(
            "Use JobContext.input/output helpers for declared paths to reduce isolated-job path errors."
        )
    if missing_input_helpers:
        warnings.append(
            f"Declared inputs not statically observed through JobContext.input: {missing_input_helpers}."
        )
    if missing_output_helpers:
        warnings.append(
            f"Declared outputs not statically observed through JobContext helpers: {missing_output_helpers}."
        )
    if unknown_input_helpers:
        warnings.append(
            f"JobContext.input names absent from the request contract: {unknown_input_helpers}."
        )
    if unknown_output_helpers:
        warnings.append(
            f"JobContext output names absent from the request contract: {unknown_output_helpers}."
        )
    if bypass_findings:
        warnings.append(
            "JobContext was imported but code walks above ctx.root; this bypasses the declared path contract."
        )
    return {
        "status": status,
        "job_context_imported": imported,
        "context_variables": sorted(context_names),
        "helper_calls": {key: sorted(value) for key, value in helper_calls.items()},
        "missing_input_helpers": missing_input_helpers,
        "missing_output_helpers": missing_output_helpers,
        "unknown_input_helpers": unknown_input_helpers,
        "unknown_output_helpers": unknown_output_helpers,
        "bypass_findings": bypass_findings,
        "warnings": warnings,
        "enforcement_boundary": (
            "Static reliability audit only; ordinary Python file and library access is not blocked."
        ),
    }


def _runtime_path_injection_findings(tree: ast.AST) -> list[dict[str, Any]]:
    """Find attempts to splice another Python environment into the selected runtime."""

    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        kind = None
        evidence = None
        if isinstance(node, ast.Call):
            chain = _attribute_chain(node.func)
            if chain in (
                ["sys", "path", "insert"],
                ["sys", "path", "append"],
                ["sys", "path", "extend"],
            ):
                kind = "sys_path_mutation"
                evidence = ".".join(chain)
            elif chain == ["site", "addsitedir"]:
                kind = "site_directory_injection"
                evidence = ".".join(chain)
            elif chain == ["os", "putenv"] and node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and str(first.value).upper() == "PYTHONPATH":
                    kind = "pythonpath_environment_mutation"
                    evidence = "os.putenv('PYTHONPATH', ...)"
        elif isinstance(node, (ast.Assign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                chain = _attribute_chain(target)
                if chain == ["sys", "path"]:
                    kind = "sys_path_assignment"
                    evidence = "sys.path"
                    break
                if (
                    isinstance(target, ast.Subscript)
                    and _attribute_chain(target.value) == ["os", "environ"]
                    and isinstance(target.slice, ast.Constant)
                    and str(target.slice.value).upper() == "PYTHONPATH"
                ):
                    kind = "pythonpath_environment_mutation"
                    evidence = "os.environ['PYTHONPATH']"
                    break
        if kind:
            findings.append(
                {
                    "line": getattr(node, "lineno", None),
                    "kind": kind,
                    "evidence": evidence,
                }
            )
    return sorted(findings, key=lambda item: (item["line"] or 0, item["kind"]))


def _external_execution_findings(tree: ast.AST) -> list[dict[str, Any]]:
    module_aliases: dict[str, str] = {}
    function_aliases: dict[str, str] = {}
    external_ase_modules = {
        "abinit", "aims", "castep", "cp2k", "dftb", "espresso", "exciting",
        "gaussian", "lammpsrun", "nwchem", "octopus", "orca", "siesta", "vasp",
    }
    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_aliases[alias.asname or alias.name.split(".", 1)[0]] = alias.name
                if alias.name.startswith("ase.calculators."):
                    calculator = alias.name.split(".")[2]
                    if calculator in external_ase_modules:
                        findings.append(
                            {
                                "line": node.lineno,
                                "kind": "ase_external_calculator_import",
                                "evidence": alias.name,
                            }
                        )
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "subprocess":
                for alias in node.names:
                    function_aliases[alias.asname or alias.name] = f"subprocess.{alias.name}"
            if node.module.startswith("ase.calculators."):
                calculator = node.module.split(".")[2]
                if calculator in external_ase_modules:
                    findings.append(
                        {
                            "line": node.lineno,
                            "kind": "ase_external_calculator_import",
                            "evidence": node.module,
                        }
                    )
    subprocess_calls = {"run", "Popen", "call", "check_call", "check_output"}
    os_calls = {"system", "popen", "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        evidence = None
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            module = module_aliases.get(node.func.value.id, node.func.value.id)
            if module == "subprocess" and node.func.attr in subprocess_calls:
                evidence = f"subprocess.{node.func.attr}"
            elif module == "os" and node.func.attr in os_calls:
                evidence = f"os.{node.func.attr}"
        elif isinstance(node.func, ast.Name) and node.func.id in function_aliases:
            evidence = function_aliases[node.func.id]
        if evidence:
            findings.append(
                {"line": node.lineno, "kind": "direct_process_launch", "evidence": evidence}
            )
    return sorted(findings, key=lambda item: (item["line"], item["kind"], item["evidence"]))


def _probe_runtime_modules(
    runtime: str,
    modules: list[str],
    *,
    local_modules: set[str],
    required_symbols: dict[str, list[str]],
) -> tuple[dict[str, bool], dict[str, dict[str, Any]]]:
    if not modules:
        return {}, {}
    python = runtime_python(runtime)
    probe_modules = [
        name for name in modules if name.split(".", 1)[0] not in local_modules
    ]
    details = {
        name: {
            "available": True,
            "importable": True,
            "source": "staged_or_framework_module",
            "version": None,
            "missing_symbols": [],
        }
        for name in modules
        if name not in probe_modules
    }
    if not probe_modules:
        return {name: True for name in modules}, details
    program = r'''
import contextlib
import importlib
import importlib.metadata
import io
import json
import sys

requirements = json.loads(sys.argv[1])
package_map = importlib.metadata.packages_distributions()
results = {}
for name, symbols in requirements.items():
    try:
        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            module = importlib.import_module(name)
        distributions = package_map.get(name.split('.', 1)[0], [])
        versions = {}
        for distribution in distributions:
            try:
                versions[distribution] = importlib.metadata.version(distribution)
            except importlib.metadata.PackageNotFoundError:
                pass
        module_version = getattr(module, '__version__', None)
        missing_symbols = []
        for symbol in symbols:
            value = module
            try:
                for part in symbol.split('.'):
                    value = getattr(value, part)
            except AttributeError:
                missing_symbols.append(symbol)
        results[name] = {
            'available': True,
            'importable': True,
            'source': 'runtime_import',
            'version': str(module_version) if module_version is not None else None,
            'distribution_versions': versions,
            'missing_symbols': missing_symbols,
            'captured_stdout': captured_stdout.getvalue()[-1000:],
            'captured_stderr': captured_stderr.getvalue()[-1000:],
        }
    except BaseException as exc:
        results[name] = {
            'available': False,
            'importable': False,
            'source': 'runtime_import',
            'version': None,
            'distribution_versions': {},
            'missing_symbols': list(symbols),
            'error': f'{type(exc).__name__}: {exc}',
        }
print('__RESEARCHCHEM_MODULE_PROBE__' + json.dumps(results, sort_keys=True))
'''
    environment = runtime_environment(runtime)
    completed = subprocess.run(
        [
            str(python),
            "-c",
            program,
            json.dumps(
                {name: required_symbols.get(name, []) for name in probe_modules},
                sort_keys=True,
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        env=environment,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Runtime module probe failed with exit code {completed.returncode}: "
            f"{completed.stderr[-2000:]}"
        )
    marker = "__RESEARCHCHEM_MODULE_PROBE__"
    line = next(
        (item for item in reversed(completed.stdout.splitlines()) if item.startswith(marker)),
        None,
    )
    if line is None:
        raise RuntimeError("Runtime module probe returned no structured result")
    details.update(json.loads(line[len(marker) :]))
    result = {
        name: bool(item.get("importable")) and not item.get("missing_symbols")
        for name, item in details.items()
    }
    return result, details


def _isolated_workspace_path_findings(tree: ast.AST) -> list[dict[str, Any]]:
    """Find literal workspace-relative inputs that are absent from an isolated job."""

    roots = {"data", "_tool_artifacts"}
    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        else:
            function_name = ""
        if not (
            function_name in {"Path", "open"}
            or function_name.startswith("read_")
            or function_name.startswith("load")
            or function_name in {"from_file", "read_text", "read_bytes"}
        ):
            continue
        candidates = [*node.args, *(keyword.value for keyword in node.keywords)]
        for candidate in candidates:
            if not isinstance(candidate, ast.Constant) or not isinstance(candidate.value, str):
                continue
            normalized = candidate.value.strip().replace("\\", "/")
            if not normalized:
                continue
            path = PurePosixPath(normalized)
            if path.is_absolute() or not path.parts or path.parts[0] not in roots:
                continue
            findings.append(
                {
                    "line": getattr(candidate, "lineno", getattr(node, "lineno", None)),
                    "path": normalized,
                    "workspace_root": path.parts[0],
                    "function": function_name,
                }
            )
    return sorted(findings, key=lambda item: (item["line"] or 0, item["path"]))


def _value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _json_shape(
    value: Any,
    *,
    depth: int,
    max_depth: int,
    max_fields: int,
    include_scalar_samples: bool,
) -> dict[str, Any]:
    value_type = _value_type(value)
    result: dict[str, Any] = {"type": value_type}
    if value_type == "object":
        keys = list(value)
        result["field_count"] = len(keys)
        result["fields"] = keys[:max_fields]
        result["truncated_fields"] = len(keys) > max_fields
        if depth < max_depth:
            result["field_shapes"] = {
                str(key): _json_shape(
                    value[key],
                    depth=depth + 1,
                    max_depth=max_depth,
                    max_fields=max_fields,
                    include_scalar_samples=include_scalar_samples,
                )
                for key in keys[:max_fields]
            }
    elif value_type == "array":
        result["length"] = len(value)
        result["item_types"] = sorted({_value_type(item) for item in value})
        result["null_count"] = sum(item is None for item in value)
        sampled_items = value[: min(len(value), 50)]
        if sampled_items and all(isinstance(item, dict) for item in sampled_items):
            sampled_fields = list(
                dict.fromkeys(
                    str(key) for item in sampled_items for key in item.keys()
                )
            )[:max_fields]
            result["object_field_profiles"] = {
                field: {
                    "presence_count": sum(field in item for item in sampled_items),
                    "null_count": sum(item.get(field) is None for item in sampled_items),
                    "types": sorted(
                        {
                            _value_type(item[field])
                            for item in sampled_items
                            if field in item
                        }
                    ),
                }
                for field in sampled_fields
            }
            result["profiled_item_count"] = len(sampled_items)
        if value and depth < max_depth:
            result["first_item_shape"] = _json_shape(
                value[0],
                depth=depth + 1,
                max_depth=max_depth,
                max_fields=max_fields,
                include_scalar_samples=include_scalar_samples,
            )
    elif include_scalar_samples and value is not None:
        result["sample"] = value if not isinstance(value, str) else value[:200]
    return result


def _infer_text_column(values: list[str]) -> dict[str, Any]:
    nonempty = [value.strip() for value in values if value.strip()]
    if not nonempty:
        inferred = "empty"
    else:
        try:
            parsed = [float(value) for value in nonempty]
        except ValueError:
            lowered = {value.casefold() for value in nonempty}
            inferred = "boolean" if lowered <= {"true", "false"} else "string"
        else:
            inferred = (
                "integer"
                if all(number.is_integer() for number in parsed)
                else "number"
            )
    return {
        "inferred_type": inferred,
        "observed_rows": len(values),
        "nonempty_count": len(nonempty),
        "empty_count": len(values) - len(nonempty),
    }


def _inspect_input_path(
    path: Path,
    *,
    max_depth: int,
    max_fields: int,
    max_rows: int,
    include_scalar_samples: bool,
) -> dict[str, Any]:
    base = {
        "path": relative_workspace_path(path),
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "suffix": path.suffix.casefold(),
    }
    suffix = path.suffix.casefold()
    if suffix == ".json":
        if path.stat().st_size > MAX_INSPECTION_JSON_BYTES:
            return {
                **base,
                "format": "json",
                "valid": None,
                "inspection_status": "skipped_size_limit",
                "maximum_parse_bytes": MAX_INSPECTION_JSON_BYTES,
            }
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            return {**base, "format": "json", "valid": False, "error": str(exc)}
        return {
            **base,
            "format": "json",
            "valid": True,
            "shape": _json_shape(
                value,
                depth=0,
                max_depth=max_depth,
                max_fields=max_fields,
                include_scalar_samples=include_scalar_samples,
            ),
        }
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle, delimiter=delimiter)
                fieldnames = list(reader.fieldnames or [])
                rows = [row for _, row in zip(range(max_rows), reader)]
        except (UnicodeDecodeError, csv.Error) as exc:
            return {**base, "format": "table", "valid": False, "error": str(exc)}
        return {
            **base,
            "format": "table",
            "valid": bool(fieldnames),
            "columns": fieldnames[:max_fields],
            "truncated_columns": len(fieldnames) > max_fields,
            "observed_rows": len(rows),
            "row_limit": max_rows,
            "column_profiles": {
                name: _infer_text_column([str(row.get(name) or "") for row in rows])
                for name in fieldnames[:max_fields]
            },
        }
    return {**base, "format": "opaque", "valid": True}


def inspect_analysis_inputs(request: AnalysisInputInspectionRequest) -> dict[str, Any]:
    summaries = []
    for item in request.inputs:
        path = resolve_workspace_path(item.source_path, must_exist=True)
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Analysis input must be a regular file: {item.source_path}")
        summaries.append(
            {
                "name": item.name,
                "semantic_type": item.semantic_type,
                **_inspect_input_path(
                    path,
                    max_depth=request.max_depth,
                    max_fields=request.max_fields,
                    max_rows=request.max_rows,
                    include_scalar_samples=request.include_scalar_samples,
                ),
            }
        )
    return {
        "status": "success",
        "inputs": summaries,
        "inspection_boundary": (
            "This is bounded structural inspection, not validation of scientific meaning. "
            "Programs must still handle missing, null, and heterogeneous values explicitly."
        ),
    }


def validate_analysis_program(request: AnalysisJobRequest) -> dict[str, Any]:
    if request.runtime not in set(runtime_names()):
        raise KeyError(f"Unknown analysis runtime {request.runtime!r}")
    python = runtime_python(request.runtime)
    if not python.is_file():
        return {
            "status": "unavailable",
            "valid": False,
            "runtime": request.runtime,
            "error": {
                "stage": "preflight",
                "code": "runtime_python_missing",
                "message": f"Runtime Python does not exist: {python}",
                "retryable": False,
            },
        }
    script = resolve_workspace_path(request.script_path, must_exist=True)
    if script.is_symlink() or not script.is_file():
        raise ValueError(f"Analysis program must be a regular non-symlink file: {request.script_path}")
    if script.suffix.lower() != ".py":
        raise ValueError("Analysis program source must be a .py file")
    try:
        source = script.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return _analysis_failure(
            stage="preflight",
            code="python_source_encoding",
            message="Analysis program must be UTF-8 text",
            file=request.script_path,
            evidence=str(exc),
            candidate_fixes=["Save the program as UTF-8 without binary content."],
        )
    try:
        tree = ast.parse(source, filename=request.script_path)
        compile(tree, request.script_path, "exec")
    except SyntaxError as exc:
        return _analysis_failure(
            stage="preflight",
            code="python_syntax_error",
            message=str(exc.msg),
            file=request.script_path,
            line=exc.lineno,
            evidence=exc.text.strip() if exc.text else None,
            candidate_fixes=["Correct the reported Python syntax before submission."],
        )
    for item in request.inputs:
        path = resolve_workspace_path(item.source_path, must_exist=True)
        if path.is_symlink() or not path.is_file():
            return _analysis_failure(
                stage="input",
                code="analysis_input_invalid",
                message=f"Declared input {item.name!r} is not a regular file",
                file=item.source_path,
                candidate_fixes=["Create the input in the workspace and declare its exact source_path."],
            )
    for item in request.staged_inputs:
        resolve_workspace_path(item.source_path, must_exist=True)
    imports = _analysis_imports(tree)
    external_findings = _external_execution_findings(tree)
    if external_findings:
        return _analysis_failure(
            stage="preflight",
            code="external_execution_not_audited",
            message=(
                "Programmable jobs cannot directly launch external executables; use the native "
                "job runner so each software call has its own resources, timeout, status, and provenance"
            ),
            file=request.script_path,
            line=external_findings[0]["line"],
            evidence=json.dumps(external_findings, sort_keys=True),
            candidate_fixes=[
                "Remove direct subprocess/os process launches from the analysis program.",
                "Submit the external executable with validate_native_job and submit_native_job.",
                "Set parent_job_id on the native request to link the orchestration provenance.",
            ],
        )
    runtime_path_findings = _runtime_path_injection_findings(tree)
    if runtime_path_findings:
        return _analysis_failure(
            stage="preflight",
            code="cross_runtime_path_injection",
            message=(
                "The program mutates Python import paths and may mix binary packages from a "
                "different runtime"
            ),
            file=request.script_path,
            line=runtime_path_findings[0]["line"],
            evidence=json.dumps(runtime_path_findings, sort_keys=True),
            candidate_fixes=[
                "Remove sys.path, site.addsitedir, and PYTHONPATH mutations.",
                "Select one runtime that already provides every required module.",
                "Declare required_modules, versions, and symbols so preflight verifies that runtime.",
            ],
        )
    isolated_path_findings = _isolated_workspace_path_findings(tree)
    if isolated_path_findings:
        return _analysis_failure(
            stage="input",
            code="unstaged_workspace_relative_path",
            message=(
                "The program contains workspace-relative input paths that will not exist in "
                "the isolated analysis job directory"
            ),
            file=request.script_path,
            line=isolated_path_findings[0]["line"],
            evidence=json.dumps(isolated_path_findings, sort_keys=True),
            candidate_fixes=[
                "Declare each required file in inputs and read it with JobContext.input(name).",
                "Alternatively map each file through staged_inputs and use its target_path inside the job.",
                "Do not assume the program starts in the benchmark workspace root.",
            ],
        )
    local_modules: set[str] = {"researchchem_job"}
    local_module_details: dict[str, dict[str, Any]] = {
        "researchchem_job": {
            "available": True,
            "importable": True,
            "source": "framework_module",
            "version": None,
            "missing_symbols": [],
        }
    }
    for item in request.staged_inputs:
        target = PurePosixPath(item.target_path)
        if target.suffix.casefold() != ".py":
            continue
        local_name = target.stem
        local_source = resolve_workspace_path(item.source_path, must_exist=True)
        try:
            local_text = local_source.read_text(encoding="utf-8")
            local_tree = ast.parse(local_text, filename=item.source_path)
            compile(local_tree, item.source_path, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            return _analysis_failure(
                stage="preflight",
                code="staged_python_syntax_error",
                message=f"Staged Python module {local_name!r} is not valid Python",
                file=item.source_path,
                line=getattr(exc, "lineno", None),
                evidence=str(exc),
                candidate_fixes=["Correct or remove the staged Python module before submission."],
            )
        declared_names = {
            node.name
            for node in local_tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        for node in local_tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                declared_names.update(
                    target_node.id
                    for target_node in targets
                    if isinstance(target_node, ast.Name)
                )
        missing_symbols = [
            symbol
            for symbol in request.required_symbols.get(local_name, [])
            if "." in symbol or symbol not in declared_names
        ]
        local_modules.add(local_name)
        local_module_details[local_name] = {
            "available": True,
            "importable": True,
            "source": "staged_python_syntax_and_symbols",
            "version": None,
            "missing_symbols": missing_symbols,
            "source_sha256": _sha256(local_source),
        }
    modules = sorted(
        set(imports)
        | set(request.required_modules)
        | set(request.required_module_versions)
        | set(request.required_symbols)
    )
    try:
        module_status, module_details = _probe_runtime_modules(
            request.runtime,
            modules,
            local_modules=local_modules,
            required_symbols=request.required_symbols,
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return _analysis_failure(
            stage="import",
            code="runtime_module_probe_failed",
            message="Could not inspect modules in the selected runtime",
            file=str(python),
            evidence=str(exc),
            candidate_fixes=["Inspect the runtime and retry with an available configured environment."],
        )
    module_details.update(local_module_details)
    module_status.update(
        {
            name: not details.get("missing_symbols")
            for name, details in local_module_details.items()
            if name in modules or name == "researchchem_job"
        }
    )
    missing = sorted(
        name
        for name, details in module_details.items()
        if name in modules and not details.get("importable")
    )
    if missing:
        return _analysis_failure(
            stage="import",
            code="runtime_modules_missing",
            message=f"Selected runtime lacks imported or required modules: {missing}",
            file=request.script_path,
            evidence=json.dumps(module_status, sort_keys=True),
            candidate_fixes=[
                "Select a runtime returned by list_analysis_runtimes that provides every module.",
                "Remove unused imports or declare and stage a local Python module explicitly.",
            ],
        )
    missing_symbols = {
        name: list(details.get("missing_symbols") or [])
        for name, details in module_details.items()
        if details.get("missing_symbols")
    }
    if missing_symbols:
        return _analysis_failure(
            stage="import",
            code="runtime_symbols_missing",
            message=f"Selected runtime modules lack required symbols: {missing_symbols}",
            file=request.script_path,
            evidence=json.dumps(module_details, sort_keys=True),
            candidate_fixes=[
                "Use symbols provided by the selected runtime version or select another runtime."
            ],
        )
    version_mismatches: dict[str, dict[str, Any]] = {}
    for name, specifier_text in request.required_module_versions.items():
        details = module_details[name]
        versions = list((details.get("distribution_versions") or {}).values())
        if details.get("version"):
            versions.append(str(details["version"]))
        unique_versions = list(dict.fromkeys(versions))
        specifier = SpecifierSet(specifier_text)
        if not unique_versions or not any(version in specifier for version in unique_versions):
            version_mismatches[name] = {
                "required": specifier_text,
                "detected": unique_versions,
            }
    if version_mismatches:
        return _analysis_failure(
            stage="import",
            code="runtime_module_version_mismatch",
            message=f"Selected runtime does not satisfy module versions: {version_mismatches}",
            file=request.script_path,
            evidence=json.dumps(module_details, sort_keys=True),
            candidate_fixes=[
                "Select a runtime with a compatible module version or update the declared constraint."
            ],
        )
    _validate_argument_paths(request.arguments)
    job_context_compliance = _job_context_compliance(tree, request)
    if (
        job_context_compliance["unknown_input_helpers"]
        or job_context_compliance["unknown_output_helpers"]
    ):
        return _analysis_failure(
            stage="input",
            code="job_context_declaration_mismatch",
            message=(
                "The program uses JobContext names that are absent from the declared input/output "
                "contract"
            ),
            file=request.script_path,
            evidence=json.dumps(job_context_compliance, sort_keys=True),
            candidate_fixes=[
                "Make every JobContext.input(name) match one inputs[].name exactly.",
                "Make every JobContext output helper name match one outputs[].name exactly.",
                "Prefer copying names from the request contract instead of inventing aliases.",
            ],
        )
    input_inspection = (
        inspect_analysis_inputs(
            AnalysisInputInspectionRequest(
                inputs=request.inputs,
                max_depth=2,
                max_fields=20,
                max_rows=100,
            )
        )
        if request.inputs
        else {"status": "success", "inputs": []}
    )
    try:
        resources = _compute_resource_limits(request.resource_limits)
    except ResourceBudgetExceeded as exc:
        return _resource_budget_error(exc)
    contract = {
        "schema_version": 1,
        "layout": {
            "code": "code/",
            "inputs": "inputs/",
            "outputs": "outputs/",
            "report": "report/",
            "logs": "logs/",
        },
        "inputs": [item.model_dump(mode="json") for item in request.inputs],
        "outputs": [item.model_dump(mode="json") for item in request.outputs],
        "execution_policy": request.execution_policy,
        "external_execution": request.external_execution,
        "job_context_boundary": (
            "JobContext validates declared names and paths but cannot prevent direct open(), "
            "absolute paths, subprocesses, or other library access."
        ),
        "job_context_compliance": job_context_compliance,
    }
    return {
        "status": "success",
        "valid": True,
        "runtime": request.runtime,
        "runtime_python": str(python),
        "script_source": relative_workspace_path(script),
        "script_target": request.script_target,
        "discovered_imports": imports,
        "required_modules": request.required_modules,
        "required_module_versions": request.required_module_versions,
        "required_symbols": request.required_symbols,
        "module_status": module_status,
        "module_details": module_details,
        "input_inspection": input_inspection,
        "external_execution_findings": external_findings,
        "runtime_path_injection_findings": runtime_path_findings,
        "job_context_compliance": job_context_compliance,
        "script_sha256": _sha256(script),
        "analysis_contract": contract,
        "resource_limits": resources,
        "execution_timeout_policy": timeout_policy_record("compute"),
        "evaluation_resource_budget": resource_budget_record(),
        "resource_availability": _resource_availability(),
    }


def submit_analysis_program(request: AnalysisJobRequest) -> dict[str, Any]:
    validation = validate_analysis_program(request)
    if validation["status"] != "success":
        return validation
    python = Path(validation["runtime_python"])
    script = resolve_workspace_path(request.script_path, must_exist=True)
    staged = [
        StagedInput(
            source_path=request.script_path,
            target_path=request.script_target,
        ),
        *request.staged_inputs,
        *[
            StagedInput(source_path=item.source_path, target_path=str(item.target_path))
            for item in request.inputs
        ],
    ]
    submitted = _start_job(
        job_type="programmable_analysis",
        runtime=request.runtime,
        command=[str(python), request.script_target, *request.arguments],
        stdin_target=None,
        staged_inputs=staged,
        resource_limits=dict(validation["resource_limits"]),
        metadata={
            "runtime": request.runtime,
            "script_source": relative_workspace_path(script),
            "script_target": request.script_target,
            "label": request.label,
            "execution_timeout_policy": timeout_policy_record("compute"),
            "analysis_contract": validation["analysis_contract"],
            "parent_job_id": request.parent_job_id,
            "script_sha256": validation["script_sha256"],
            "preflight": {
                "discovered_imports": validation["discovered_imports"],
                "required_modules": validation["required_modules"],
                "required_module_versions": validation["required_module_versions"],
                "required_symbols": validation["required_symbols"],
                "module_status": validation["module_status"],
                "module_details": validation["module_details"],
                "input_inspection": validation["input_inspection"],
                "external_execution_findings": validation[
                    "external_execution_findings"
                ],
                "job_context_compliance": validation["job_context_compliance"],
            },
            "security_boundary": (
                "Subprocess/resource/workspace convention only; deploy MCP inside an OS container "
                "or scheduler sandbox when executing untrusted programs."
            ),
        },
    )
    submitted["job_context_compliance"] = validation["job_context_compliance"]
    return submitted


def _read_status(job_id: str) -> tuple[Path, dict[str, Any]]:
    directory = _job_directory(job_id)
    path = directory / "status.json"
    if not path.is_file():
        raise RuntimeError(f"Execution job has no status record: {job_id}")
    return directory, json.loads(path.read_text(encoding="utf-8"))


def _tail(path: Path, characters: int) -> str:
    if characters <= 0 or not path.is_file():
        return ""
    with path.open("rb") as handle:
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        handle.seek(max(0, size - characters * 4))
        data = handle.read()
    return data.decode("utf-8", errors="replace")[-characters:]


def _bounded_text(path: Path, maximum_bytes: int = 8 * 1024 * 1024) -> str:
    if not path.is_file():
        return ""
    with path.open("rb") as handle:
        data = handle.read(maximum_bytes)
    return data.decode("utf-8", errors="replace")


def _program_failure_diagnostic(
    directory: Path, status: dict[str, Any]
) -> dict[str, Any] | None:
    if (
        status.get("job_type") != "programmable_analysis"
        or status.get("status") != "failed"
    ):
        return None
    diagnostic_path = directory / "failure_diagnostic.json"
    if diagnostic_path.is_file():
        try:
            return json.loads(diagnostic_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    stderr = _bounded_text(directory / "stderr.log", maximum_bytes=2 * 1024 * 1024)
    exception_type = None
    message = None
    exception_match = None
    for line in reversed(stderr.splitlines()):
        candidate = re.match(
            r"^(?P<type>[A-Za-z_][A-Za-z0-9_.]*(?:Error|Exception)):\s*(?P<message>.*)$",
            line.strip(),
        )
        if candidate:
            exception_match = candidate
            break
    if exception_match:
        exception_type = exception_match.group("type")
        message = exception_match.group("message")
    frames = re.findall(r'File "([^"]+)", line (\d+)(?:, in ([^\n]+))?', stderr)
    source_file = None
    source_line = None
    function = None
    for raw_file, raw_line, raw_function in reversed(frames):
        candidate = Path(raw_file)
        if not candidate.is_absolute():
            candidate = directory / candidate
        try:
            candidate.resolve().relative_to(directory.resolve())
        except ValueError:
            continue
        if candidate.is_file() and candidate.suffix == ".py":
            source_file = candidate
            source_line = int(raw_line)
            function = raw_function.strip() or None
            break
    source_context = None
    if source_file is not None and source_line is not None:
        lines = source_file.read_text(encoding="utf-8", errors="replace").splitlines()
        start = max(0, source_line - 3)
        stop = min(len(lines), source_line + 2)
        source_context = [
            {"line": index + 1, "text": lines[index]}
            for index in range(start, stop)
        ]

    lowered = (message or stderr[-1000:]).casefold()
    classification = "nonzero_exit"
    candidate_fixes = [
        "Read the structured input summary and the failing source line before revising the program.",
        "Validate intermediate values and declared output schemas before resubmission.",
    ]
    details: dict[str, Any] = {}
    if exception_type == "KeyError":
        classification = "missing_mapping_key"
        missing_key = (message or "").strip().strip("'\"")
        details["missing_key"] = missing_key or None
        candidate_fixes = [
            "Inspect the actual JSON/object keys with inspect_analysis_inputs.",
            "Use the existing field name or handle the field as optional with an explicit fallback.",
        ]
    elif "unknown input name" in lowered or "unknown output name" in lowered:
        classification = "job_context_name_mismatch"
        candidate_fixes = [
            "Make the JobContext helper name exactly match the submitted contract name.",
            "Run validate_analysis_program again before resubmission.",
        ]
    elif exception_type == "NameError":
        classification = "undefined_name"
        candidate_fixes = [
            "Define the reported variable on every control-flow path before it is used.",
            "Run a focused unit calculation on one input record before processing the full dataset.",
        ]
    elif "nonetype" in lowered or (
        "none" in lowered and exception_type == "TypeError"
    ):
        classification = "unexpected_null_value"
        candidate_fixes = [
            "Check for null/None before arithmetic or numeric formatting.",
            "Decide explicitly whether a missing value should be skipped, rejected, or replaced.",
        ]
    elif "unpack" in lowered or "values to unpack" in lowered:
        classification = "unpack_shape_mismatch"
        candidate_fixes = [
            "Inspect the sequence or mapping shape before unpacking it.",
            "Use indexed or named access when the input record length is not guaranteed.",
        ]
    diagnostic = {
        "schema_version": 1,
        "job_id": status.get("job_id"),
        "classification": classification,
        "exception_type": exception_type,
        "message": message,
        "source_file": (
            str(source_file.resolve().relative_to(directory.resolve()))
            if source_file is not None
            else None
        ),
        "source_line": source_line,
        "function": function,
        "source_context": source_context,
        "details": details,
        "candidate_fixes": candidate_fixes,
        "diagnostic_boundary": (
            "This classifies the Python failure mechanically; it does not determine the correct "
            "scientific interpretation or choose replacement data."
        ),
    }
    _atomic_json(diagnostic_path, diagnostic)
    return diagnostic


def _process_axis(job_status: str) -> str:
    return {
        "queued": "queued",
        "running": "running",
        "success": "completed",
        "failed": "failed",
        "timeout": "timed_out",
        "cancelled": "cancelled",
    }.get(job_status, "unknown")


def _native_scientific_axes(
    directory: Path, status: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    metadata = status.get("metadata") or {}
    software_id = str(metadata.get("software_id") or "")
    calculation_intent = str(metadata.get("calculation_intent") or "unknown")
    process_ok = status.get("status") == "success"
    stdout = _bounded_text(directory / "stdout.log")
    software = {"status": "not_checked", "evidence": []}
    convergence = {"status": "not_checked", "evidence": []}
    artifacts = {"status": "not_declared", "evidence": []}
    if not process_ok:
        software = {"status": "not_reached", "evidence": [status.get("status")]}
        convergence = {"status": "not_reached", "evidence": []}
        artifacts = {"status": "not_validated", "evidence": []}
        return software, convergence, artifacts
    if software_id == "orca":
        normal = "ORCA TERMINATED NORMALLY" in stdout
        software = {
            "status": "normal_termination" if normal else "failed",
            "evidence": ["ORCA TERMINATED NORMALLY"] if normal else ["normal termination marker missing"],
        }
        scf_converged = "SCF CONVERGED" in stdout
        optimization_converged = "THE OPTIMIZATION HAS CONVERGED" in stdout
        frequency_complete = "VIBRATIONAL FREQUENCIES" in stdout
        frequencies = [
            float(value)
            for value in re.findall(
                r"^\s*\d+:\s*(-?\d+(?:\.\d+)?)\s+cm\*\*-1",
                stdout,
                flags=re.MULTILINE,
            )
        ]
        imaginary_count = sum(value < -1.0 for value in frequencies)
        requirements = {
            "single_point": scf_converged,
            "geometry_optimization": optimization_converged,
            "frequency": scf_converged and frequency_complete,
            "optimization_frequency": optimization_converged and frequency_complete,
            "transition_state": (
                optimization_converged and frequency_complete and imaginary_count == 1
            ),
        }
        converged = requirements.get(calculation_intent)
        markers = [
            marker
            for marker, present in (
                ("SCF CONVERGED", scf_converged),
                ("THE OPTIMIZATION HAS CONVERGED", optimization_converged),
                ("VIBRATIONAL FREQUENCIES", frequency_complete),
            )
            if present
        ]
        if frequency_complete:
            markers.append(f"imaginary_frequency_count={imaginary_count}")
        convergence = {
            "status": (
                "not_checked"
                if converged is None
                else "converged" if converged else "failed"
            ),
            "evidence": markers,
            "calculation_intent": calculation_intent,
        }
        artifacts = {
            "status": "valid" if normal and (directory / "stdout.log").stat().st_size else "invalid",
            "evidence": ["stdout.log"],
        }
    elif software_id == "gaussian":
        normal = "Normal termination of Gaussian" in stdout and "Error termination" not in stdout
        software = {
            "status": "normal_termination" if normal else "failed",
            "evidence": ["Normal termination of Gaussian"] if normal else ["normal termination marker missing"],
        }
        scf_converged = "SCF Done:" in stdout
        optimization_converged = "Optimization completed" in stdout
        nimag_matches = re.findall(r"NImag=\s*(\d+)", stdout)
        imaginary_count = int(nimag_matches[-1]) if nimag_matches else None
        frequency_complete = imaginary_count is not None or "Harmonic frequencies" in stdout
        requirements = {
            "single_point": scf_converged,
            "geometry_optimization": optimization_converged,
            "frequency": scf_converged and frequency_complete,
            "optimization_frequency": optimization_converged and frequency_complete,
            "transition_state": (
                optimization_converged and frequency_complete and imaginary_count == 1
            ),
        }
        converged = requirements.get(calculation_intent)
        markers = [
            marker
            for marker, present in (
                ("SCF Done:", scf_converged),
                ("Optimization completed", optimization_converged),
                ("frequency calculation completed", frequency_complete),
            )
            if present
        ]
        if imaginary_count is not None:
            markers.append(f"imaginary_frequency_count={imaginary_count}")
        convergence = {
            "status": (
                "not_checked"
                if converged is None
                else "converged" if converged else "failed"
            ),
            "evidence": markers,
            "calculation_intent": calculation_intent,
        }
        artifacts = {"status": "valid" if normal else "invalid", "evidence": ["stdout.log"]}
    elif software_id == "crest":
        normal = "CREST terminated normally" in stdout
        software = {
            "status": "normal_termination" if normal else "failed",
            "evidence": ["CREST terminated normally"] if normal else ["normal termination marker missing"],
        }
        expected_by_intent = {
            "conformer_search": "crest_conformers.xyz",
            "protonation": "protonated.xyz",
            "deprotonation": "deprotonated.xyz",
            "tautomerization": "tautomers.xyz",
        }
        expected_name = expected_by_intent.get(calculation_intent)
        expected = directory / expected_name if expected_name else None
        valid = bool(expected and expected.is_file() and expected.stat().st_size)
        convergence = {
            "status": (
                "not_checked"
                if expected is None
                else "converged" if normal and valid else "failed"
            ),
            "evidence": [expected_name] if valid and expected_name else [],
            "calculation_intent": calculation_intent,
        }
        artifacts = {
            "status": "not_checked" if expected is None else "valid" if valid else "invalid",
            "evidence": [expected_name] if valid and expected_name else [],
        }
    elif software_id == "vasp":
        outcar = _bounded_text(directory / "OUTCAR")
        normal = "General timing and accounting informations for this job" in outcar
        electronic_converged = "aborting loop because EDIFF is reached" in outcar
        ionic_converged = "reached required accuracy" in outcar
        frequency_complete = "Eigenvectors and eigenvalues of the dynamical matrix" in outcar
        requirements = {
            "single_point": electronic_converged,
            "ionic_relaxation": electronic_converged and ionic_converged,
            "frequency": electronic_converged and frequency_complete,
        }
        converged = requirements.get(calculation_intent)
        software = {
            "status": "normal_termination" if normal else "failed",
            "evidence": ["General timing and accounting informations for this job"] if normal else ["OUTCAR timing footer missing"],
        }
        convergence = {
            "status": (
                "not_checked"
                if converged is None
                else "converged" if converged else "failed"
            ),
            "evidence": [
                marker
                for marker, present in (
                    ("electronic EDIFF reached", electronic_converged),
                    ("ionic relaxation reached required accuracy", ionic_converged),
                    ("dynamical matrix frequencies completed", frequency_complete),
                )
                if present
            ],
            "calculation_intent": calculation_intent,
        }
        required = ["OUTCAR", "vasprun.xml"]
        valid = all((directory / item).is_file() and (directory / item).stat().st_size for item in required)
        artifacts = {"status": "valid" if valid else "invalid", "evidence": required}
    elif software_id == "lobster":
        lobsterout = _bounded_text(directory / "lobsterout") or stdout
        normal = "finished in" in lobsterout and not re.search(r"^ERROR:", lobsterout, flags=re.M)
        software = {
            "status": "normal_termination" if normal else "failed",
            "evidence": ["finished in"] if normal else ["LOBSTER ERROR marker or missing finish marker"],
        }
        spilling = re.search(r"abs\. charge spilling:\s*([0-9.]+)%", lobsterout)
        convergence = {
            "status": "projection_complete" if normal else "failed",
            "evidence": ([f"absolute_charge_spilling_percent={spilling.group(1)}"] if spilling else []),
            "calculation_intent": calculation_intent,
        }
        required = ["lobsterout", "COHPCAR.lobster"]
        valid = all((directory / item).is_file() and (directory / item).stat().st_size for item in required)
        artifacts = {"status": "valid" if valid else "invalid", "evidence": required}
    return software, convergence, artifacts


def _execution_status_axes(
    directory: Path,
    status: dict[str, Any],
    *,
    analysis_artifact_status: str | None = None,
) -> dict[str, Any]:
    request_status = "accepted"
    process_status = _process_axis(str(status.get("status") or ""))
    if status.get("job_type") == "native_software":
        software, convergence, artifacts = _native_scientific_axes(directory, status)
    else:
        software = {"status": "not_applicable", "evidence": []}
        convergence = {"status": "not_declared", "evidence": []}
        artifact_value = analysis_artifact_status
        if artifact_value is None:
            artifact_value = (
                "pending_collection"
                if status.get("status") in TERMINAL_JOB_STATES
                else "pending_execution"
            )
        artifacts = {"status": artifact_value, "evidence": ["artifact_manifest.json"] if analysis_artifact_status else []}
    if process_status != "completed":
        scientific = "not_reached"
    elif (
        software["status"] == "failed"
        or convergence["status"] == "failed"
        or artifacts["status"] == "invalid"
    ):
        scientific = "mechanically_invalid"
    elif convergence["status"] in {"converged", "projection_complete"} and artifacts["status"] == "valid":
        scientific = "mechanically_valid"
    elif status.get("job_type") == "programmable_analysis" and artifacts["status"] == "valid":
        scientific = "mechanically_valid"
    else:
        scientific = "not_checked"
    return {
        "request_status": request_status,
        "process_status": process_status,
        "software_status": software["status"],
        "convergence_status": convergence["status"],
        "artifact_status": artifacts["status"],
        "scientific_validation_status": scientific,
        "details": {
            "software": software,
            "convergence": convergence,
            "artifacts": artifacts,
            "scientific_validation_boundary": (
                "Mechanical validation does not judge whether the Agent's final scientific "
                "interpretation or paper conclusion is correct; that remains the Judger's role."
            ),
        },
    }


def _resource_availability() -> dict[str, Any]:
    budget = resource_budget_record()
    try:
        reserved = active_resource_usage()
        active_jobs = active_resource_jobs()
        tracking = "workspace_reservations"
    except RuntimeError:
        reserved = {"cpu_cores": 0, "memory_mb": 0, "gpu_count": 0}
        active_jobs = []
        tracking = "unavailable_without_workspace"
    available = {
        name: max(0, int(budget[name]) - int(reserved[name]))
        for name in ("cpu_cores", "memory_mb", "gpu_count")
    }
    return {
        "budget": budget,
        "currently_reserved": reserved,
        "available": available,
        "active_jobs": active_jobs,
        "active_job_count": len(active_jobs),
        "reservation_tracking": tracking,
    }


def get_execution_resources(_request: ExecutionResourceRequest) -> dict[str, Any]:
    return {"status": "success", **_resource_availability()}


def get_execution_job(request: JobStatusRequest) -> dict[str, Any]:
    directory, status = _read_status(request.job_id)
    stdout_path = directory / "stdout.log"
    stderr_path = directory / "stderr.log"
    axes = _execution_status_axes(directory, status)
    failure_diagnostic = _program_failure_diagnostic(directory, status)
    return {
        "status": "success",
        "job": status,
        "stdout_tail": _tail(stdout_path, request.tail_chars),
        "stderr_tail": _tail(stderr_path, request.tail_chars),
        "failure_diagnostic": failure_diagnostic,
        "terminal": status.get("status") in TERMINAL_JOB_STATES,
        **{key: value for key, value in axes.items() if key != "details"},
        "execution_status_details": axes["details"],
        "resource_availability": _resource_availability(),
    }


def cancel_execution_job(request: JobCancelRequest) -> dict[str, Any]:
    _directory, status = _read_status(request.job_id)
    if status.get("status") in TERMINAL_JOB_STATES:
        return {
            "status": "success",
            "job_id": request.job_id,
            "job_status": status.get("status"),
            "cancellation_sent": False,
            "message": "Job was already terminal; no signal was sent.",
        }
    supervisor_pid = status.get("supervisor_pid")
    if not isinstance(supervisor_pid, int):
        spec_path = _job_directory(request.job_id) / "supervisor_spec.json"
        if spec_path.is_file():
            # A just-submitted job may still be between queued and running. The
            # detached supervisor records its own PID as soon as it starts; do
            # not guess or signal another process in that short interval.
            return {
                "status": "failed",
                "job_id": request.job_id,
                "job_status": status.get("status"),
                "cancellation_sent": False,
                "error": {
                    "code": "supervisor_not_started",
                    "message": "Supervisor has not published its PID yet; poll once and retry cancellation.",
                },
            }
    if not isinstance(supervisor_pid, int) or supervisor_pid <= 0:
        raise RuntimeError(f"Job {request.job_id} has no live supervisor pid")
    try:
        os.kill(supervisor_pid, signal.SIGTERM)
    except ProcessLookupError:
        return {
            "status": "failed",
            "job_id": request.job_id,
            "job_status": status.get("status"),
            "cancellation_sent": False,
            "error": {
                "code": "supervisor_missing",
                "message": "Supervisor process no longer exists; inspect job status again.",
            },
        }
    return {
        "status": "success",
        "job_id": request.job_id,
        "job_status": status.get("status"),
        "cancellation_sent": True,
        "message": "Cancellation signal sent; poll get_execution_job until terminal.",
    }


def _reject_nonfinite(value: Any, *, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"non-finite numeric value at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite(item, path=f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _reject_nonfinite(item, path=f"{path}.{key}")


def _validate_declared_output(path: Path, declaration: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    media_type = str(declaration.get("media_type") or "application/octet-stream")
    try:
        if media_type == "application/json" or path.suffix.casefold() == ".json":
            value = json.loads(
                path.read_text(encoding="utf-8"),
                parse_constant=lambda token: (_ for _ in ()).throw(
                    ValueError(f"non-standard JSON constant {token}")
                ),
            )
            _reject_nonfinite(value)
            if declaration.get("json_schema"):
                from jsonschema import validate as validate_json_schema

                validate_json_schema(value, declaration["json_schema"])
        elif media_type in {"text/csv", "text/tab-separated-values"} or path.suffix.casefold() in {".csv", ".tsv"}:
            delimiter = "\t" if media_type == "text/tab-separated-values" or path.suffix.casefold() == ".tsv" else ","
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle, delimiter=delimiter))
            if not rows:
                raise ValueError("table contains no rows")
            for row_index, row in enumerate(rows):
                for column_index, cell in enumerate(row):
                    if cell.strip().casefold() in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity"}:
                        raise ValueError(
                            f"non-finite table value at row {row_index + 1}, column {column_index + 1}"
                        )
        elif media_type.startswith("image/"):
            prefix = path.read_bytes()[:16]
            signatures = {
                "image/png": b"\x89PNG\r\n\x1a\n",
                "image/jpeg": b"\xff\xd8\xff",
                "image/gif": b"GIF8",
            }
            expected = signatures.get(media_type)
            if expected and not prefix.startswith(expected):
                raise ValueError(f"file does not have a valid {media_type} signature")
    except Exception as exc:
        errors.append(str(exc))
    return errors


def _first_present(mapping: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if name in mapping:
            return mapping[name]
    return None


def _validate_scientific_output(
    path: Path, declaration: dict[str, Any]
) -> dict[str, Any]:
    semantic = str(declaration.get("semantic_type") or "").casefold()
    checks: list[str] = []
    errors: list[str] = []
    if not any(token in semantic for token in ("hessian", "equationofstate", "equation_of_state", "eos")):
        return {"status": "not_applicable", "checks": [], "errors": []}
    try:
        if path.suffix.casefold() == ".json" or declaration.get("media_type") == "application/json":
            value = json.loads(path.read_text(encoding="utf-8"))
            _reject_nonfinite(value)
        else:
            value = None

        if "hessian" in semantic:
            if not isinstance(value, dict) or not isinstance(value.get("matrix"), list):
                raise ValueError("Hessian output requires a JSON object with a dense matrix")
            matrix = value["matrix"]
            dimension = len(matrix)
            if dimension == 0 or any(not isinstance(row, list) or len(row) != dimension for row in matrix):
                raise ValueError("Hessian matrix must be non-empty, square, and fully populated")
            maximum_asymmetry = 0.0
            for row in range(dimension):
                for column in range(dimension):
                    entry = float(matrix[row][column])
                    if not math.isfinite(entry):
                        raise ValueError(f"Hessian contains non-finite value at [{row}][{column}]")
                    maximum_asymmetry = max(
                        maximum_asymmetry,
                        abs(entry - float(matrix[column][row])),
                    )
            if maximum_asymmetry > 1e-6:
                raise ValueError(
                    f"Hessian is not symmetric within 1e-6; maximum asymmetry={maximum_asymmetry:.6g}"
                )
            checks.extend(
                [
                    f"dense_square_dimension={dimension}",
                    f"finite_value_count={dimension * dimension}",
                    f"maximum_asymmetry={maximum_asymmetry:.6g}",
                ]
            )

        if any(token in semantic for token in ("equationofstate", "equation_of_state", "eos")):
            points: list[dict[str, Any]] = []
            fit: dict[str, Any] | None = None
            if isinstance(value, dict):
                candidate = value.get("points") or value.get("data") or value.get("samples")
                if isinstance(candidate, list):
                    points = [item for item in candidate if isinstance(item, dict)]
                fit_value = value.get("fit")
                fit = fit_value if isinstance(fit_value, dict) else value
            elif value is None:
                delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
                with path.open("r", encoding="utf-8", newline="") as handle:
                    points = list(csv.DictReader(handle, delimiter=delimiter))
            volumes = []
            energies = []
            for index, point in enumerate(points):
                volume = _first_present(
                    point, ("volume", "volume_ang3", "volume_a3", "volume_per_formula_unit")
                )
                energy = _first_present(
                    point, ("energy", "energy_ev", "total_energy", "energy_per_formula_unit")
                )
                if volume is None or energy is None:
                    raise ValueError(
                        f"EOS point {index} lacks a recognized volume or energy field"
                    )
                volume_value = float(volume)
                energy_value = float(energy)
                if not math.isfinite(volume_value) or not math.isfinite(energy_value):
                    raise ValueError(f"EOS point {index} contains a non-finite value")
                volumes.append(volume_value)
                energies.append(energy_value)
            if len(points) < 4 or len(set(volumes)) < 4:
                raise ValueError("EOS validation requires at least four unique volume-energy points")
            checks.extend(
                [
                    f"volume_energy_point_count={len(points)}",
                    f"unique_volume_count={len(set(volumes))}",
                ]
            )
            if "result" in semantic:
                fit_status = str(
                    _first_present(fit or {}, ("status", "fit_status", "convergence_status"))
                    or ""
                ).casefold()
                if fit_status not in {"success", "converged", "valid"}:
                    raise ValueError("EOS result requires an explicit successful fit status")
                residual = _first_present(
                    fit or {}, ("rmse", "residual_rms", "max_abs_residual", "residual")
                )
                if residual is None or not math.isfinite(float(residual)):
                    raise ValueError("EOS result requires one finite residual metric")
                checks.extend(
                    [f"fit_status={fit_status}", f"fit_residual={float(residual):.6g}"]
                )
    except Exception as exc:
        errors.append(str(exc))
    return {
        "status": "valid" if not errors else "invalid",
        "checks": checks,
        "errors": errors,
        "boundary": (
            "This validates mechanical completeness and finite fit evidence only; scientific "
            "model choice and conclusions remain the Judger's responsibility."
        ),
    }


def _analysis_artifact_manifest(
    directory: Path,
    status: dict[str, Any],
    request_record: dict[str, Any],
) -> dict[str, Any] | None:
    if status.get("job_type") != "programmable_analysis":
        return None
    contract = (request_record.get("metadata") or {}).get("analysis_contract") or {}
    registration_path = directory / "runtime_output_registrations.json"
    registrations = (
        json.loads(registration_path.read_text(encoding="utf-8")).get("outputs", {})
        if registration_path.is_file()
        else {}
    )
    declarations = list(contract.get("outputs") or [])
    artifacts = []
    required_failures = 0
    for declaration in declarations:
        relative = str(declaration["path"])
        path = directory.joinpath(*PurePosixPath(relative).parts)
        required = bool(declaration.get("required", True))
        validation_errors: list[str] = []
        scientific_validation = {"status": "not_checked", "checks": [], "errors": []}
        if path.is_symlink() or not path.is_file():
            validation_status = "missing_required" if required else "missing_optional"
            if required:
                required_failures += 1
        else:
            if path.stat().st_size == 0:
                validation_errors.append("file is empty")
            validation_errors.extend(_validate_declared_output(path, declaration))
            scientific_validation = _validate_scientific_output(path, declaration)
            validation_errors.extend(scientific_validation["errors"])
            validation_status = "valid" if not validation_errors else "invalid"
            if required and validation_errors:
                required_failures += 1
        artifacts.append(
            {
                "name": declaration["name"],
                "path": relative,
                "workspace_path": relative_workspace_path(path),
                "semantic_type": declaration["semantic_type"],
                "media_type": declaration["media_type"],
                "size_bytes": path.stat().st_size if path.is_file() else None,
                "sha256": _sha256(path) if path.is_file() else None,
                "producer": f"programmable_analysis:{status['job_id']}",
                "parent_artifacts": list(declaration.get("parent_artifact_ids") or []),
                "required": required,
                "validation_status": validation_status,
                "validation_errors": validation_errors,
                "runtime_registration": registrations.get(declaration["name"]),
                "scientific_validation": (
                    scientific_validation
                ),
            }
        )
    if not declarations:
        artifact_status = "not_declared"
    elif required_failures:
        artifact_status = "invalid"
    else:
        artifact_status = "valid"
    manifest = {
        "schema_version": 1,
        "job_id": status["job_id"],
        "artifact_status": artifact_status,
        "generated_at": _now(),
        "artifacts": artifacts,
    }
    _atomic_json(directory / "artifact_manifest.json", manifest)
    return manifest


def collect_execution_job(request: JobCollectRequest) -> dict[str, Any]:
    directory, status = _read_status(request.job_id)
    if status.get("status") not in TERMINAL_JOB_STATES:
        axes = _execution_status_axes(directory, status)
        return {
            "status": "success",
            "job_id": request.job_id,
            "job_status": status.get("status"),
            "ready": False,
            "outputs": [],
            **{key: value for key, value in axes.items() if key != "details"},
            "execution_status_details": axes["details"],
            "message": "Job is not terminal; poll get_execution_job before collecting outputs.",
        }
    request_record = json.loads((directory / "request.json").read_text(encoding="utf-8"))
    staged_targets = {
        str(item["target_path"]) for item in request_record.get("staged_inputs") or []
    }
    internal = {
        "analysis_contract.json",
        "artifact_manifest.json",
        "request.json",
        "researchchem_job.py",
        "runtime_output_registrations.json",
        "status.json",
        "supervisor_spec.json",
        "collection.json",
    }
    files: list[dict[str, Any]] = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative = str(path.relative_to(directory))
        if relative in internal or relative.startswith(".tmp/") or relative.startswith(".home/"):
            continue
        if not request.include_inputs and relative in staged_targets:
            continue
        files.append(
            {
                "path": relative_workspace_path(path),
                "job_relative_path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "kind": "log" if relative in {"stdout.log", "stderr.log"} else "output",
            }
        )
        if len(files) >= request.max_files:
            break
    artifact_manifest = _analysis_artifact_manifest(directory, status, request_record)
    axes = _execution_status_axes(
        directory,
        status,
        analysis_artifact_status=(
            artifact_manifest["artifact_status"] if artifact_manifest else None
        ),
    )
    manifest = {
        "schema_version": 1,
        "job_id": request.job_id,
        "job_status": status.get("status"),
        "collected_at": _now(),
        "include_inputs": request.include_inputs,
        "truncated": len(files) >= request.max_files,
        "outputs": files,
        **{key: value for key, value in axes.items() if key != "details"},
        "execution_status_details": axes["details"],
        "declared_artifacts": artifact_manifest["artifacts"] if artifact_manifest else [],
    }
    collection_path = directory / "collection.json"
    _atomic_json(collection_path, manifest)
    return {
        "status": "success",
        "ready": True,
        "job": status,
        "collection_manifest": relative_workspace_path(collection_path),
        **manifest,
        "artifact_manifest": (
            relative_workspace_path(directory / "artifact_manifest.json")
            if artifact_manifest
            else None
        ),
        "next_step": (
            "Inspect the files and call declare_scientific_artifact for each scientifically "
            "meaningful output that should enter an Action or later job with explicit lineage."
        ),
    }


def declare_scientific_artifact(request: ArtifactDeclarationRequest) -> dict[str, Any]:
    path = resolve_workspace_path(request.path, must_exist=True)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Artifact source must be a regular non-symlink file: {request.path}")
    producer = f"{request.producer_layer}:{request.producer_id}"
    reference = ArtifactStore().register_file(
        path,
        semantic_type=request.semantic_type,
        media_type=request.media_type,
        producer_action=producer,
        producer_backend=(
            request.producer_id if request.producer_layer == "native_software" else None
        ),
        parent_artifact_ids=request.parent_artifact_ids,
    )
    return {
        "status": "success",
        "artifact": reference.model_dump(mode="json"),
        "lineage_note": (
            "This declaration records semantics and parent ids supplied by the Agent; it does not "
            "infer or alter scientific meaning."
        ),
    }


__all__ = [
    "cancel_execution_job",
    "collect_execution_job",
    "declare_scientific_artifact",
    "get_execution_job",
    "read_workspace_text",
    "submit_analysis_program",
    "get_execution_resources",
    "inspect_analysis_inputs",
    "submit_native_job",
    "validate_analysis_program",
    "validate_native_job",
    "write_workspace_text",
]
