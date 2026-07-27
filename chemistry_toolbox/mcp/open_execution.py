"""Auditable native-software and Agent-authored program execution tools."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from researchchem_toolbox.artifacts import ArtifactStore
from researchchem_toolbox.runtime import (
    runtime_environment,
    runtime_names,
    runtime_python,
)
from researchchem_toolbox.resource_budget import (
    ResourceBudgetExceeded,
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
    AnalysisJobRequest,
    ArtifactDeclarationRequest,
    JobCancelRequest,
    JobCollectRequest,
    JobStatusRequest,
    NativeJobRequest,
    StagedInput,
    WorkspaceTextReadRequest,
    WorkspaceTextWriteRequest,
)
from .software_catalog import native_command_guide
from .workspace import (
    relative_workspace_path,
    resolve_workspace_output_path,
    resolve_workspace_path,
    workspace_root,
)


JOB_ROOT = Path("outputs") / "execution_jobs"
TERMINAL_JOB_STATES = {"success", "failed", "timeout", "cancelled"}
SUPERVISOR_PATH = Path(__file__).with_name("job_supervisor.py")
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
    return {
        "status": "invalid_request",
        "valid": False,
        "error": exc.as_error(),
        "evaluation_resource_budget": resource_budget_record(),
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
    input_deck_validation = None
    if guide["software_id"] == "pysisyphus" and request.executable == "pysis":
        input_deck_validation = _validate_pysisyphus_input_deck(request, guide)
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
        "resource_limits": resources,
        "execution_timeout_policy": timeout_policy_record("compute"),
        "evaluation_resource_budget": resource_budget_record(),
        "invocation_guide": guide,
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
    *,
    job_type: str,
) -> dict[str, str]:
    inherited = {
        name: os.environ[name]
        for name in SAFE_INHERITED_ENVIRONMENT
        if os.environ.get(name)
    }
    environment = {**inherited, **runtime_environment(runtime)}
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
            selected = visible[:gpu_count] if visible else list(map(str, range(gpu_count)))
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
        }
    )
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
    metadata: dict[str, Any],
) -> dict[str, Any]:
    job_id = f"job_{uuid.uuid4().hex}"
    job_directory = _job_directory(job_id, must_exist=False)
    job_directory.mkdir(parents=True, exist_ok=False)
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
            "invocation_synopsis": guide.get("synopsis"),
            "execution_timeout_policy": timeout_policy_record("compute"),
        },
    )


def submit_analysis_program(request: AnalysisJobRequest) -> dict[str, Any]:
    if request.runtime not in set(runtime_names()):
        raise KeyError(f"Unknown analysis runtime {request.runtime!r}")
    python = runtime_python(request.runtime)
    if not python.is_file():
        return {
            "status": "unavailable",
            "runtime": request.runtime,
            "error": {
                "code": "runtime_python_missing",
                "message": f"Runtime Python does not exist: {python}",
            },
        }
    script = resolve_workspace_path(request.script_path, must_exist=True)
    if script.is_symlink() or not script.is_file():
        raise ValueError(f"Analysis program must be a regular non-symlink file: {request.script_path}")
    if script.suffix.lower() != ".py":
        raise ValueError("Analysis program source must be a .py file")
    _validate_argument_paths(request.arguments)
    staged = [
        StagedInput(
            source_path=request.script_path,
            target_path=request.script_target,
        ),
        *request.staged_inputs,
    ]
    try:
        resources = _compute_resource_limits(request.resource_limits)
    except ResourceBudgetExceeded as exc:
        return _resource_budget_error(exc)
    return _start_job(
        job_type="programmable_analysis",
        runtime=request.runtime,
        command=[str(python), request.script_target, *request.arguments],
        stdin_target=None,
        staged_inputs=staged,
        resource_limits=resources,
        metadata={
            "runtime": request.runtime,
            "script_source": relative_workspace_path(script),
            "script_target": request.script_target,
            "label": request.label,
            "execution_timeout_policy": timeout_policy_record("compute"),
            "security_boundary": (
                "Subprocess/resource/workspace convention only; deploy MCP inside an OS container "
                "or scheduler sandbox when executing untrusted programs."
            ),
        },
    )


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


def get_execution_job(request: JobStatusRequest) -> dict[str, Any]:
    directory, status = _read_status(request.job_id)
    stdout_path = directory / "stdout.log"
    stderr_path = directory / "stderr.log"
    return {
        "status": "success",
        "job": status,
        "stdout_tail": _tail(stdout_path, request.tail_chars),
        "stderr_tail": _tail(stderr_path, request.tail_chars),
        "terminal": status.get("status") in TERMINAL_JOB_STATES,
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


def collect_execution_job(request: JobCollectRequest) -> dict[str, Any]:
    directory, status = _read_status(request.job_id)
    if status.get("status") not in TERMINAL_JOB_STATES:
        return {
            "status": "success",
            "job_id": request.job_id,
            "job_status": status.get("status"),
            "ready": False,
            "outputs": [],
            "message": "Job is not terminal; poll get_execution_job before collecting outputs.",
        }
    request_record = json.loads((directory / "request.json").read_text(encoding="utf-8"))
    staged_targets = {
        str(item["target_path"]) for item in request_record.get("staged_inputs") or []
    }
    internal = {
        "request.json",
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
    manifest = {
        "schema_version": 1,
        "job_id": request.job_id,
        "job_status": status.get("status"),
        "collected_at": _now(),
        "include_inputs": request.include_inputs,
        "truncated": len(files) >= request.max_files,
        "outputs": files,
    }
    collection_path = directory / "collection.json"
    _atomic_json(collection_path, manifest)
    return {
        "status": "success",
        "ready": True,
        "job": status,
        "collection_manifest": relative_workspace_path(collection_path),
        **manifest,
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
    "submit_native_job",
    "validate_native_job",
    "write_workspace_text",
]
