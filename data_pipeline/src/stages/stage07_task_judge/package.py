"""Assemble audited Stage07 modes into clean ResearchChemBench Task Package v1 trees."""

from __future__ import annotations

import json
import shutil
import sys
import uuid
from pathlib import Path
from typing import Any

from src.agents.workspace import atomic_commit_tree, make_writable, prepare_clean_directory
from src.contracts import read_json, safe_component, write_json
from src.stages.evaluator_reference import read_split_reference


_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from researchchembench_contracts import (  # noqa: E402
    PACKAGE_MANIFEST_SCHEMA_V1,
    SUBMISSION_SCHEMA_V1,
    TASK_INFO_SCHEMA_V1,
    TASK_PACKAGE_SCHEMA_V1,
    PackageManifestV1,
    SubmissionSchemaV1,
    TaskInfoV1,
    is_document_binding_selector,
    materialize_result_schema_path,
    package_content_hash,
    package_payload_entries,
    validate_task_package,
)


TASK_PACKAGE_ASSEMBLER_VERSION = "stage07-task-package-v1-unified-gate-20260824"
COMPUTATIONAL_TASK_TYPES = ("paper_reproduction", "autonomous_research")
_MODE_ALIASES = {
    "paper_reproduction": "paper_reproduction",
    "reproduction": "paper_reproduction",
    "guided_reproduction": "paper_reproduction",
    "autonomous_research": "autonomous_research",
    "autonomous": "autonomous_research",
    "open_discovery": "autonomous_research",
}


def canonical_mode_task_id(task_family_id: str, task_type: str) -> str:
    if task_type not in COMPUTATIONAL_TASK_TYPES:
        raise ValueError(f"unsupported computational task type: {task_type}")
    # Mode is encoded by the directory, so a mode-specific suffix would create
    # a second paper identity.  Both mode packages carry the same paper_id.
    return safe_component(task_family_id)


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _task_title(task_text: str, info: dict[str, Any], task_id: str) -> str:
    for value in (info.get("title"), info.get("task_title")):
        if str(value or "").strip():
            return str(value).strip()
    for line in task_text.splitlines():
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip()
    return task_id


def _required_capabilities(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                rows.append(item)
    elif isinstance(value, dict):
        for software in value.get("required_software") or []:
            rows.append(
                {
                    "software_id": software,
                    "reason": "Required by the audited scientific workflow.",
                }
            )
        for item in value.get("required_additions") or []:
            if isinstance(item, dict):
                rows.append(item)
    capabilities: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        software = str(
            row.get("software_id")
            or row.get("display_name")
            or row.get("family")
            or row.get("name")
            or ""
        ).strip()
        capability = str(row.get("capability") or (f"software:{software}" if software else "")).strip()
        if not capability or capability in seen:
            continue
        seen.add(capability)
        preferred = _as_string_list(row.get("preferred_software"))
        if software and software not in preferred:
            preferred.append(software)
        capabilities.append(
            {
                "capability": capability,
                "preferred_software": preferred,
                "required": bool(row.get("required", not row.get("non_blocking", False))),
                "purpose": str(
                    row.get("purpose")
                    or row.get("reason")
                    or row.get("required_by")
                    or ""
                ),
            }
        )
    return capabilities


def _normalize_required_deliverables(value: Any) -> tuple[list[dict[str, Any]], list[str]]:
    """Project the historical deliverable envelope onto TaskInfoV1.

    ``type: workspace_artifact`` was emitted by an older Stage07 prompt but
    is not part of the shared TaskInfoV1 contract.  It carries no information
    needed by the benchmark package, so it is removed at this explicit
    projection boundary and reported as a diagnostic.  Other unknown fields
    are retained so a genuinely divergent contract still fails loudly.
    """

    if not isinstance(value, list):
        return [], []
    normalized: list[dict[str, Any]] = []
    diagnostics: list[str] = []
    for index, item in enumerate(value):
        if isinstance(item, str):
            path = item.strip()
            if path:
                normalized.append(
                    {
                        "path": path,
                        "description": "Required task artifact.",
                        "allow_empty": False,
                    }
                )
            continue
        if not isinstance(item, dict):
            normalized.append(item)
            continue
        row = dict(item)
        if "type" in row and row.get("type") == "workspace_artifact":
            row.pop("type", None)
            diagnostics.append(
                f"required_deliverables_type_projected:{index}:workspace_artifact"
            )
        normalized.append(row)
    return normalized, diagnostics


def _task_info(
    *,
    source_info: dict[str, Any],
    task_text: str,
    task_id: str,
    task_family_id: str,
    task_type: str,
    runtime_readiness: str,
    toolbox_requirements: Any,
    required_deliverables: Any | None = None,
) -> dict[str, Any]:
    related_type = (
        "autonomous_research"
        if task_type == "paper_reproduction"
        else "paper_reproduction"
    )
    raw_data = source_info.get("data") if isinstance(source_info.get("data"), list) else []
    # TaskInfoV1 exposes only transport fields for public data assets.  Stage06
    # may retain private/provenance annotations such as ``role`` or
    # ``source_evidence_ids`` in its candidate metadata; discard those at this
    # package boundary rather than letting a scientifically approved task fail
    # during Pydantic serialization.
    data = []
    for item in raw_data:
        if not isinstance(item, dict):
            continue
        data.append(
            {
                key: item[key]
                for key in ("name", "path", "type", "description")
                if key in item
            }
        )
    deliverables = required_deliverables
    if deliverables is None:
        deliverables, _ = _normalize_required_deliverables(
            source_info.get("required_deliverables")
        )
    value = {
        "schema_version": TASK_INFO_SCHEMA_V1,
        "task_id": task_id,
        "task_family_id": task_family_id,
        "task_type": task_type,
        "source_id": str(
            source_info.get("source_id")
            or source_info.get("paper_id")
            or task_family_id
        ),
        "title": _task_title(task_text, source_info, task_id),
        "category": str(source_info.get("category") or "uncategorized"),
        "tags": _as_string_list(source_info.get("tags")),
        "runtime_readiness": runtime_readiness,
        "required_capabilities": _required_capabilities(toolbox_requirements),
        "data": data,
        "required_deliverables": deliverables,
        "related_task_ids": [canonical_mode_task_id(task_family_id, related_type)],
        "reference_schema": "researchchembench.split-evaluator.v1",
    }
    return TaskInfoV1.model_validate(value).model_dump(mode="json")


def _submission_schema(
    *,
    source: dict[str, Any],
    task_info: dict[str, Any],
    task_id: str,
    bindings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    required_files = _as_string_list(source.get("required_files"))
    if not required_files:
        required_files = [
            str(item.get("path") or "")
            for item in task_info.get("required_deliverables") or []
            if str(item.get("path") or "")
        ]
    primary = str(
        source.get("submission_path")
        or source.get("primary_result_file")
        or (required_files[0] if required_files else "")
    ).strip()
    result_schema = (
        json.loads(json.dumps(source.get("result_schema"), ensure_ascii=False))
        if isinstance(source.get("result_schema"), dict)
        else json.loads(json.dumps(source.get("results_schema"), ensure_ascii=False))
        if isinstance(source.get("results_schema"), dict)
        else {}
    )
    # Make already-declared open paths explicit at the package boundary.  This
    # is deterministic transport projection; it does not invent values or
    # alter the hidden reference.  Filter selectors and document selectors are
    # intentionally left to their dedicated validators.
    for binding in bindings or []:
        if not isinstance(binding, dict):
            continue
        projection = binding.get("canonical_projection")
        for field in _as_string_list(binding.get("observed_fields")):
            if is_document_binding_selector(
                field,
                _as_string_list(binding.get("artifact_paths")),
                document_binding=bool(binding.get("document_binding")),
            ):
                continue
            materialize_result_schema_path(result_schema, field, projection)
    value = {
        "schema_version": SUBMISSION_SCHEMA_V1,
        "task_id": task_id,
        "required_files": required_files,
        "primary_result_file": primary or None,
        "result_schema": result_schema,
        "allowed_extra_fields": bool(source.get("allowed_extra_fields", True)),
    }
    return SubmissionSchemaV1.model_validate(value).model_dump(mode="json")


def assemble_task_package(
    *,
    pair_root: Path,
    final_tasks_root: Path,
    task_family_id: str,
    task_type: str,
    runtime_readiness: str,
) -> dict[str, Any]:
    """Build, validate, and atomically publish one clean mode package."""

    pair_root = pair_root.expanduser().resolve()
    source = pair_root / task_type
    split_reference = read_split_reference(pair_root)
    task_id = canonical_mode_task_id(task_family_id, task_type)
    destination = final_tasks_root / task_type / task_id
    if not source.is_dir():
        return {
            "status": "failed",
            "task_id": task_id,
            "task_type": task_type,
            "path": "",
            "findings": ["source_mode_missing"],
        }
    required = [
        source / "task.md",
        source / "task_info.json",
        source / "submission_contract.json",
        source / "process_rubric.json",
    ]
    required.extend(
        pair_root / "evaluator_reference" / filename
        for filename in (
            "reference_key_points.json",
            "reference_conclusions.json",
            "scoring_rules.json",
            "evidence_map.json",
            "critical_failures.json",
        )
    )
    missing = [path.relative_to(pair_root).as_posix() for path in required if not path.is_file()]
    if missing:
        return {
            "status": "failed",
            "task_id": task_id,
            "task_type": task_type,
            "path": "",
            "findings": [f"source_file_missing:{path}" for path in missing],
        }
    staging_container = prepare_clean_directory(
        destination.parent
        / f".{task_id}.staging-{uuid.uuid4().hex[:8]}"
    )
    staging = staging_container / task_id
    staging.mkdir()
    try:
        task_text = (source / "task.md").read_text(encoding="utf-8")
        (staging / "task.md").write_text(task_text, encoding="utf-8")
        source_info = read_json(source / "task_info.json")
        toolbox_path = pair_root / "toolbox_requirements.json"
        toolbox_requirements = read_json(toolbox_path) if toolbox_path.is_file() else []
        deliverables, deliverable_diagnostics = _normalize_required_deliverables(
            source_info.get("required_deliverables")
        )
        task_info = _task_info(
            source_info=source_info,
            task_text=task_text,
            task_id=task_id,
            task_family_id=task_family_id,
            task_type=task_type,
            runtime_readiness=runtime_readiness,
            toolbox_requirements=toolbox_requirements,
            required_deliverables=deliverables,
        )
        write_json(staging / "task_info.json", task_info)
        source_data = source / "data"
        if source_data.is_dir():
            shutil.copytree(source_data, staging / "data")
        else:
            (staging / "data").mkdir()
        evaluation = staging / "evaluation"
        evaluation.mkdir()
        if split_reference is None:
            raise ValueError(
                "evaluator_reference_missing: split evaluator files are required"
            )
        submission = _submission_schema(
            source=read_json(source / "submission_contract.json"),
            task_info=task_info,
            task_id=task_id,
            bindings=None,
        )
        write_json(staging / "submission_schema.json", submission)
        for key, filename in {
            "reference_key_points": "reference_key_points.json",
            "reference_conclusions": "reference_conclusions.json",
            "scoring_rules": "scoring_rules.json",
            "evidence_map": "evidence_map.json",
            "critical_failures": "critical_failures.json",
        }.items():
            write_json(evaluation / filename, split_reference[key])
        entries = package_payload_entries(staging)
        public_allowlist = ["task.md", "submission_schema.json"]
        if any(entry.path.startswith("data/") for entry in entries):
            public_allowlist.append("data/**")
        manifest = PackageManifestV1(
            schema_version=PACKAGE_MANIFEST_SCHEMA_V1,
            package_schema=TASK_PACKAGE_SCHEMA_V1,
            task_id=task_id,
            task_family_id=task_family_id,
            task_type=task_type,
            reference_schema="researchchembench.split-evaluator.v1",
            assembler_version=TASK_PACKAGE_ASSEMBLER_VERSION,
            package_content_sha256=package_content_hash(entries),
            entries=entries,
            public_to_agent=public_allowlist,
            manifest_self_excluded=True,
        )
        write_json(staging / "package_manifest.json", manifest.model_dump(mode="json"))
        validation = validate_task_package(staging)
        if validation.status != "passed":
            return {
                "status": "failed",
                "task_id": task_id,
                "task_type": task_type,
                "path": "",
                "findings": validation.findings,
                "diagnostics": sorted(
                    set(
                        validation.diagnostics
                        + deliverable_diagnostics
                    )
                ),
            }
        atomic_commit_tree(staging, destination)
        return {
            "status": "passed",
            "task_id": task_id,
            "task_type": task_type,
            "path": str(destination),
            "package_content_sha256": manifest.package_content_sha256,
            "findings": [],
            "diagnostics": sorted(
                set(
                    validation.diagnostics
                    + deliverable_diagnostics
                )
            ),
        }
    except Exception as exc:
        return {
            "status": "failed",
            "task_id": task_id,
            "task_type": task_type,
            "path": "",
            "findings": [f"task_package_assembly_error:{type(exc).__name__}:{exc}"],
        }
    finally:
        if staging_container.exists():
            make_writable(staging_container)
            shutil.rmtree(staging_container, ignore_errors=True)


def assemble_task_packages(
    *,
    pair_root: Path,
    final_tasks_root: Path,
    task_family_id: str,
    runtime_readiness: str,
) -> dict[str, dict[str, Any]]:
    return {
        task_type: assemble_task_package(
            pair_root=pair_root,
            final_tasks_root=final_tasks_root,
            task_family_id=task_family_id,
            task_type=task_type,
            runtime_readiness=runtime_readiness,
        )
        for task_type in COMPUTATIONAL_TASK_TYPES
    }
