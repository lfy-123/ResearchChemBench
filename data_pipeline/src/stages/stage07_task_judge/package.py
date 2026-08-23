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


_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from researchchembench_contracts import (  # noqa: E402
    COMPUTATIONAL_REFERENCE_SCHEMA_V1,
    PACKAGE_MANIFEST_SCHEMA_V1,
    SUBMISSION_SCHEMA_V1,
    TASK_INFO_SCHEMA_V1,
    TASK_PACKAGE_SCHEMA_V1,
    ComputationalScienceReferenceV1,
    PackageManifestV1,
    SubmissionSchemaV1,
    TaskInfoV1,
    is_document_binding_selector,
    materialize_result_schema_path,
    normalize_binding_artifact_paths,
    normalize_binding_contract,
    package_content_hash,
    package_payload_entries,
    validate_task_package,
)


TASK_PACKAGE_ASSEMBLER_VERSION = "stage07-task-package-v1-20260823"
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
    return f"{safe_component(task_family_id)}_{task_type}"


def _scope(value: Any) -> set[str] | None:
    if value is None:
        return None
    values = value if isinstance(value, list) else [value]
    normalized = {
        _MODE_ALIASES.get(str(item).strip().casefold(), "") for item in values
    }
    normalized.discard("")
    return normalized or set()


def _applies(value: dict[str, Any], task_type: str) -> bool:
    raw = value.get("applies_to_modes")
    if raw is None:
        raw = value.get("mode_scope")
    scope = _scope(raw)
    return scope is None or task_type in scope


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _normalize_binding_transport(binding: dict[str, Any]) -> dict[str, Any]:
    """Project known legacy binding spellings without choosing scientific meaning.

    Older Stage06/07 outputs occasionally put submission artifact paths in
    ``observed_fields`` and put the actual structured result keys in
    ``target_fields``.  The latter is an unambiguous transport alias: turn
    those keys into explicit JSONPath selectors.  Ambiguous bindings remain
    empty/invalid and are rejected by the typed contract instead of guessed.
    """

    return normalize_binding_contract(binding)


def _selected_binding(profile: dict[str, Any], task_type: str) -> dict[str, Any]:
    """Select one already-authored mode binding without inventing a mapping."""

    for key in ("mode_submission_bindings", "submission_bindings_by_mode"):
        matrix = profile.get(key)
        if isinstance(matrix, dict):
            for raw_mode, binding in matrix.items():
                if (
                    _MODE_ALIASES.get(str(raw_mode).strip().casefold()) == task_type
                    and isinstance(binding, dict)
                ):
                    return _normalize_binding_transport(binding)
    shared = profile.get("submission_binding")
    if not isinstance(shared, dict):
        return {}
    for key in ("mode_submission_bindings", "submission_bindings_by_mode"):
        matrix = shared.get(key)
        if isinstance(matrix, dict):
            for raw_mode, binding in matrix.items():
                if (
                    _MODE_ALIASES.get(str(raw_mode).strip().casefold()) == task_type
                    and isinstance(binding, dict)
                ):
                    return _normalize_binding_transport(binding)
    for raw_mode, binding in shared.items():
        if (
            _MODE_ALIASES.get(str(raw_mode).strip().casefold()) == task_type
            and isinstance(binding, dict)
        ):
            return _normalize_binding_transport(binding)
    # A shared binding is valid only when it is a binding object rather than a
    # nested mode map.  Scientific applicability was already decided upstream.
    if any(
        key in shared
        for key in (
            "artifact_paths",
            "artifact_path",
            "artifact",
            "artifacts",
            "observed_fields",
            "observed_field",
            "target_fields",
            "field",
            "document_target",
        )
    ):
        return _normalize_binding_transport(shared)
    return {}


def _profile_parameters(
    profile: dict[str, Any], answer: dict[str, Any]
) -> dict[str, Any]:
    for candidate in (
        profile.get("parameters"),
        profile.get("tolerance"),
        answer.get("acceptance_parameters"),
    ):
        if isinstance(candidate, dict) and candidate:
            return json.loads(json.dumps(candidate, ensure_ascii=False))
    values: dict[str, Any] = {}
    for key in (
        "unit",
        "absolute_tolerance",
        "relative_tolerance",
        "allowed_values",
        "expected_order",
        "expected_sign",
    ):
        if key in profile:
            values[key] = profile[key]
    return values


def _process_key_points(rows: Any) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(rows or [], start=1):
        if not isinstance(row, dict):
            continue
        identifier = str(
            row.get("id") or row.get("key_point_id") or f"process_key_point_{index}"
        ).strip()
        if not identifier or identifier in seen:
            continue
        seen.add(identifier)
        title = str(
            row.get("key_point") or row.get("name") or row.get("title") or identifier
        ).strip()
        description = str(row.get("description") or title).strip()
        evidence = _as_string_list(
            row.get("evidence_artifacts") or row.get("required_evidence")
        )
        metadata = {
            key: row[key]
            for key in ("criterion_type", "evidence_anchor")
            if key in row
        }
        values.append(
            {
                "key_point_id": identifier,
                "title": title,
                "description": description,
                "evidence_requirements": evidence,
                "metadata": metadata,
            }
        )
    return values


def _critical_failures(value: Any) -> list[str]:
    values: list[str] = []
    for item in value or []:
        if isinstance(item, str) and item.strip():
            values.append(item.strip())
        elif isinstance(item, dict):
            text = str(
                item.get("description")
                or item.get("statement")
                or item.get("failure")
                or ""
            ).strip()
            if text:
                values.append(text)
    return values


def project_computational_reference(
    *,
    hidden: dict[str, Any],
    task_type: str,
    task_id: str,
    process_rubric: Any,
) -> dict[str, Any]:
    """Create one clean, mode-specific scientific reference.

    This is a lossy transport projection by design: duplicate targets,
    evaluator score fields, legacy mode aliases, and canonical projections are
    removed.  No scientific answer, tolerance, proposition, or conclusion is
    invented or changed.
    """

    if task_type not in COMPUTATIONAL_TASK_TYPES:
        raise ValueError(f"unsupported task type: {task_type}")
    raw_answers = [
        row
        for row in hidden.get("ground_truth_items") or []
        if isinstance(row, dict) and _applies(row, task_type)
    ]
    raw_profiles = [
        row
        for row in hidden.get("acceptance_profiles") or []
        if isinstance(row, dict) and _applies(row, task_type)
    ]
    profiles_by_id = {
        str(row.get("acceptance_profile_id") or row.get("profile_id") or "").strip(): row
        for row in raw_profiles
        if str(row.get("acceptance_profile_id") or row.get("profile_id") or "").strip()
    }
    answers: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    answer_to_profile: dict[str, str] = {}
    final_answer_ids: set[str] = set()
    for answer in raw_answers:
        answer_id = str(answer.get("ground_truth_id") or answer.get("answer_id") or "").strip()
        profile_id = str(
            answer.get("acceptance_profile_id")
            or answer.get("acceptance_profile")
            or ""
        ).strip()
        if not answer_id or not profile_id or profile_id not in profiles_by_id:
            # Missing ownership is a technical contract defect.  Omitting it
            # here makes the strict reference validator fail rather than
            # fabricating an identity or binding.
            continue
        profile = profiles_by_id[profile_id]
        claim_role = str(answer.get("claim_role") or "intermediate").strip().casefold()
        if claim_role not in {"intermediate", "final"}:
            claim_role = "intermediate"
        if claim_role == "final":
            final_answer_ids.add(answer_id)
        metadata = {
            key: answer[key]
            for key in ("required_propositions", "forbidden_contradictions")
            if key in answer
        }
        answers.append(
            {
                "answer_id": answer_id,
                "kind": str(answer.get("kind") or answer.get("acceptance_type") or "result"),
                "canonical_answer": answer.get("canonical_answer"),
                "claim_role": claim_role,
                "evidence_grade": str(answer.get("evidence_grade") or ""),
                "evidence_ids": _as_string_list(answer.get("evidence_ids")),
                "metadata": metadata,
            }
        )
        acceptance_type = str(
            profile.get("acceptance_type")
            or profile.get("type")
            or answer.get("acceptance_type")
            or ""
        ).strip()
        profiles.append(
            {
                "acceptance_profile_id": profile_id,
                "answer_id": answer_id,
                "acceptance_type": acceptance_type,
                "parameters": _profile_parameters(profile, answer),
                "required_propositions": _as_string_list(
                    profile.get("required_propositions")
                    or answer.get("required_propositions")
                ),
                "forbidden_contradictions": _as_string_list(
                    profile.get("forbidden_contradictions")
                    or answer.get("forbidden_contradictions")
                ),
                "description": str(profile.get("description") or ""),
            }
        )
        binding = normalize_binding_contract(
            _selected_binding(profile, task_type),
            profile=profile,
            answer=answer,
        )
        artifact_paths = normalize_binding_artifact_paths(binding)
        observed_fields = _as_string_list(
            binding.get("observed_fields")
            or binding.get("observed_field")
            or binding.get("field")
        )
        document_binding = bool(
            binding.get("document_binding")
            or binding.get("document_target") is not None
            or any(
                is_document_binding_selector(
                    field,
                    artifact_paths,
                    document_binding=bool(binding.get("document_binding")),
                )
                for field in observed_fields
            )
        )
        bindings.append(
            {
                "binding_id": f"binding_{safe_component(profile_id)}",
                "acceptance_profile_id": profile_id,
                "artifact_paths": artifact_paths,
                "observed_fields": observed_fields,
                "comparison": str(
                    binding.get("comparison")
                    or binding.get("comparison_type")
                    or acceptance_type
                ).strip(),
                "document_binding": document_binding,
                "canonical_projection": binding.get("canonical_projection"),
            }
        )
        answer_to_profile[answer_id] = profile_id

    raw_conclusions = [
        row
        for row in hidden.get("scientific_conclusion_rubric") or []
        if isinstance(row, dict) and _applies(row, task_type)
    ]
    conclusions: list[dict[str, Any]] = []
    covered_final_answers: set[str] = set()
    answers_by_id = {row["answer_id"]: row for row in answers}
    for index, row in enumerate(raw_conclusions, start=1):
        answer_ids = [
            value
            for value in _as_string_list(
                row.get("ground_truth_ids") or row.get("answer_ids")
            )
            if value in final_answer_ids
        ]
        if not answer_ids:
            continue
        profile_ids = [
            answer_to_profile[answer_id]
            for answer_id in answer_ids
            if answer_id in answer_to_profile
        ]
        if not profile_ids:
            continue
        statement = row.get("statement")
        if len(answer_ids) == 1 and statement == answers_by_id[answer_ids[0]]["canonical_answer"]:
            statement = f"Evaluate the final scientific result identified by {answer_ids[0]}."
        conclusions.append(
            {
                "conclusion_id": str(
                    row.get("id") or row.get("conclusion_id") or f"conclusion_{index}"
                ),
                "statement": statement,
                "answer_ids": answer_ids,
                "acceptance_profile_ids": profile_ids,
                "required_evidence": _as_string_list(row.get("required_evidence")),
                "metadata": {
                    "acceptance_rule": row.get("acceptance_rule")
                }
                if row.get("acceptance_rule") is not None
                else {},
            }
        )
        covered_final_answers.update(answer_ids)
    for answer_id in sorted(final_answer_ids - covered_final_answers):
        profile_id = answer_to_profile.get(answer_id)
        if not profile_id:
            continue
        conclusions.append(
            {
                "conclusion_id": f"conclusion_{safe_component(answer_id)}",
                "statement": f"Evaluate the final scientific result identified by {answer_id}.",
                "answer_ids": [answer_id],
                "acceptance_profile_ids": [profile_id],
                "required_evidence": [],
                "metadata": {"derived_from_claim_role": "final"},
            }
        )

    constraints = {
        key: hidden[key]
        for key in (
            "managed_computation_policy",
            "evidence_gate_policy",
            "reference_conclusion_gate_policy",
        )
        if isinstance(hidden.get(key), dict) and hidden[key]
    }
    reference = {
        "schema_version": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
        "task_id": task_id,
        "task_type": task_type,
        "answer_items": answers,
        "acceptance_profiles": profiles,
        "submission_bindings": bindings,
        "process_key_points": _process_key_points(process_rubric),
        "final_conclusions": conclusions,
        "critical_failures": _critical_failures(hidden.get("critical_failures")),
        "private_evidence": (
            hidden.get("reference_evidence")
            if isinstance(hidden.get("reference_evidence"), dict)
            else {}
        ),
        "evaluation_constraints": constraints,
    }
    return ComputationalScienceReferenceV1.model_validate(reference).model_dump(
        mode="json"
    )


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
    data = source_info.get("data") if isinstance(source_info.get("data"), list) else []
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
        "reference_schema": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
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
    hidden_path = pair_root / "hidden_reference" / "ground_truth_common.json"
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
        hidden_path,
    ]
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
        reference = project_computational_reference(
            hidden=read_json(hidden_path),
            task_type=task_type,
            task_id=task_id,
            process_rubric=read_json(source / "process_rubric.json"),
        )
        submission = _submission_schema(
            source=read_json(source / "submission_contract.json"),
            task_info=task_info,
            task_id=task_id,
            bindings=reference.get("submission_bindings"),
        )
        write_json(staging / "submission_schema.json", submission)
        write_json(evaluation / "reference.json", reference)
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
            reference_schema=COMPUTATIONAL_REFERENCE_SCHEMA_V1,
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
                    set(validation.diagnostics + deliverable_diagnostics)
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
                set(validation.diagnostics + deliverable_diagnostics)
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
