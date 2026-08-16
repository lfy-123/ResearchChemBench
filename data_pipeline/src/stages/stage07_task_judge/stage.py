from __future__ import annotations

import json
import re
import shutil
import time
import uuid
from pathlib import Path
from typing import Any

import jsonschema

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.schemas import STAGE07_AUDIT_SCHEMA
from src.agents.workspace import (
    IGNORED_MANIFEST_NAMES,
    agent_recovery_context,
    atomic_commit_tree,
    copy_recovery_artifacts,
    copytree_exact,
    directory_manifest,
    input_fingerprint,
    make_read_only,
    make_writable,
    prepare_clean_directory,
    recovery_instructions,
    validate_relative_path,
    write_manifest,
)
from src.contracts import (
    canonical_hash,
    decision_counts,
    now_utc,
    read_json,
    record_header,
    safe_component,
    write_json,
    write_jsonl,
)
from src.core.concurrency import ordered_parallel_map
from src.stages.stage07_task_judge.prompts import (
    STAGE07_AUDIT_VERSION,
    audit_instructions,
)
from src.stages.stage07_task_judge.validation import (
    deterministic_stage07_audit,
    validate_agent_audit,
)

STAGE07_IMPLEMENTATION_VERSION = "v5-repair-first-audit-redesign-20260816-r10"
STAGE07_DIRECTORY = "stage_07_task_audit"
STAGE07_IGNORED_PAIR_FILES = {*IGNORED_MANIFEST_NAMES, "construction_record.json"}
STAGE07_APPROVED_DECISIONS = {
    "approved",
    "approved_with_repairs",
    "approved_after_workflow_redesign",
}
STAGE07_ELIGIBLE_STAGE06_DECISIONS = {
    "provisional_constructed",
    "provisional_not_constructible",
    "constructed",
}


def run_stage07(*, build_records, documents, config, model, workspace: Path, run_id: str):
    stage_root = workspace / STAGE07_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    eligible = [
        row
        for row in build_records
        if row.get("decision") in STAGE07_ELIGIBLE_STAGE06_DECISIONS
        and row.get("handoff_ready", True)
    ]
    documents_by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass" and document.get("paper_id"):
            documents_by_paper.setdefault(str(document["paper_id"]), []).append(document)
    model_config = dict(getattr(model, "config", {}) or {})
    harness_name = str(config.get("harness") or "codex")
    harness = create_agent_harness(
        harness_name,
        config=config,
        model_config=model_config,
        model_client=model,
    )

    def audit(record: dict[str, Any]) -> dict[str, Any]:
        paper_id = str(record["paper_id"])
        task_pair_id = str(record.get("task_pair_id") or f"{paper_id}-provisional")
        handoff_value = record.get("handoff_path") or record.get("task_pair_path")
        try:
            if not handoff_value:
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "stage06_handoff_missing",
                    "Stage06 did not provide a handoff path.",
                )
            handoff_root = Path(str(handoff_value)).expanduser().resolve()
            if not handoff_root.is_dir():
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "stage06_handoff_missing",
                    f"Stage06 handoff directory is missing: {handoff_root}",
                )
            source_root = _resolve_stage07_source_root(
                record=record,
                paper_id=paper_id,
                documents=documents_by_paper.get(paper_id, []),
                stage_root=stage_root,
                config=config,
            )
            source_stage06_decision = (
                "provisional_constructed"
                if record.get("decision") == "constructed"
                else str(record["decision"])
            )
            response, agent_run, artifact_root = _run_audit_repair_agent(
                harness=harness,
                stage_root=stage_root,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                source_stage06_decision=source_stage06_decision,
                handoff_root=handoff_root,
                source_root=source_root,
                stage06_record=record,
                config=config,
            )
            decision = str(response["audit_decision"])
            if decision == "objective_failure_retryable":
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "agent_reported_objective_failure",
                    str(response.get("summary") or "Stage07 could not complete the audit."),
                    agent_run=agent_run,
                )
            final_task_pair_id = str(response.get("final_task_pair_id") or task_pair_id)
            final_path: str | None = None
            if decision in STAGE07_APPROVED_DECISIONS:
                task_root = _stage07_approved_artifact(response, artifact_root)
                target = stage_root / "audited_tasks" / safe_component(paper_id)
                atomic_commit_tree(task_root, target)
                write_json(target / "stage07_audit.json", response)
                write_json(target / "stage06_handoff_record.json", record)
                write_manifest(target, target / "audit_manifest.json")
                final_path = str(target)
            else:
                target = _publish_stage07_rejection(
                    stage_root=stage_root,
                    paper_id=paper_id,
                    response=response,
                    stage06_record=record,
                    handoff_root=handoff_root,
                )
            return {
                **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                "task_pair_id": final_task_pair_id or task_pair_id,
                "original_task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": decision,
                "audit_decision": decision,
                "audit_summary": decision,
                "passed": decision in STAGE07_APPROVED_DECISIONS,
                "selected_workflow_preserved": response.get(
                    "selected_workflow_preserved"
                ),
                "repair_count": len(response.get("repairs") or []),
                "workflow_redesign": response.get("workflow_redesign") or {},
                "toolbox_status": response.get("toolbox_status"),
                "required_additions": response.get("required_additions") or [],
                "resource_status": response.get("resource_status"),
                "task_pair_path": final_path,
                "audit_path": str(target),
                "agent_harness": harness.name,
                "agent_model": harness.model,
            }
        except AgentExecutionError as exc:
            return _audit_failure(
                run_id,
                paper_id,
                task_pair_id,
                exc.failure_class,
                str(exc),
                agent_run=exc.result.audit_record() if exc.result else None,
                retryable=exc.retryable,
            )
        except (FileNotFoundError, OSError) as exc:
            return _audit_failure(
                run_id,
                paper_id,
                task_pair_id,
                "audit_input_unavailable",
                f"{type(exc).__name__}: {exc}",
            )
        except Exception as exc:
            return _audit_failure(
                run_id,
                paper_id,
                task_pair_id,
                "audit_processing_error",
                f"{type(exc).__name__}: {exc}",
            )

    records = ordered_parallel_map(
        audit,
        eligible,
        max_workers=int(config.get("workers", 1)),
    )
    write_jsonl(stage_root / "audit_results.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage07"),
        "implementation_version": STAGE07_IMPLEMENTATION_VERSION,
        "task_pairs": len(records),
        "approved": sum(row.get("audit_decision") == "approved" for row in records),
        "approved_with_repairs": sum(
            row.get("audit_decision") == "approved_with_repairs" for row in records
        ),
        "approved_after_workflow_redesign": sum(
            row.get("audit_decision") == "approved_after_workflow_redesign"
            for row in records
        ),
        "rejected_scientific_unrepairable": sum(
            row.get("audit_decision") == "rejected_scientific_unrepairable"
            for row in records
        ),
        "objective_failure_retryable": sum(
            row.get("audit_decision") == "objective_failure_retryable" for row in records
        ),
        "needs_software": sum(row.get("toolbox_status") == "needs_software" for row in records),
        "decisions": decision_counts(records, "audit_decision"),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _run_audit_repair_agent(
    *,
    harness,
    stage_root: Path,
    paper_id: str,
    task_pair_id: str,
    source_stage06_decision: str,
    handoff_root: Path,
    source_root: Path,
    stage06_record: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], Path]:
    handoff_manifest = directory_manifest(handoff_root)
    source_manifest = directory_manifest(source_root)
    toolbox = _stage07_toolbox_snapshot(source_root, handoff_root, config)
    resource_policy = _stage07_resource_policy(source_root, config)
    fingerprint = input_fingerprint(
        {
            "handoff_manifest_hash": handoff_manifest["content_hash"],
            "source_manifest_hash": source_manifest["content_hash"],
            "source_stage06_decision": source_stage06_decision,
            "toolbox": toolbox,
            "resource_policy": resource_policy,
            "prompt_version": STAGE07_AUDIT_VERSION,
            "receipt_schema": canonical_hash(STAGE07_AUDIT_SCHEMA),
            "harness": harness.name,
            "model": harness.model,
        }
    )
    artifact_root = (
        stage_root
        / "phase_artifacts"
        / safe_component(paper_id)
        / "audit_repair"
        / fingerprint[:16]
    )
    checkpoint = (
        stage_root / "checkpoints" / safe_component(paper_id) / "audit_repair.json"
    )
    failure_checkpoint = checkpoint.with_suffix(".failure.json")
    if bool(config.get("resume", True)) and checkpoint.is_file() and artifact_root.is_dir():
        cached = read_json(checkpoint)
        if cached.get("input_fingerprint") == fingerprint:
            response = cached.get("response") or {}
            jsonschema.validate(response, STAGE07_AUDIT_SCHEMA)
            if response.get("audit_decision") in STAGE07_APPROVED_DECISIONS:
                _stage07_approved_artifact(response, artifact_root)
            return (
                response,
                {**(cached.get("agent_run") or {}), "cache_hit": True},
                artifact_root,
            )

    attempts = max(1, int(config.get("max_attempts", 3)))
    last_error: AgentExecutionError | None = None
    recovery_context: str | None = None
    recovery_workspace: Path | None = None
    for attempt in range(1, attempts + 1):
        root = prepare_clean_directory(
            stage_root
            / "workspaces"
            / safe_component(paper_id)
            / "audit_repair"
            / f"attempt-{attempt:02d}-{uuid.uuid4().hex[:8]}"
        )
        inputs = root / "inputs"
        inputs.mkdir(parents=True, exist_ok=True)
        copytree_exact(handoff_root, inputs / "stage06_candidate")
        copytree_exact(source_root, inputs / "source_materials")
        write_json(inputs / "stage06_record.json", stage06_record)
        write_json(inputs / "toolbox_snapshot.json", toolbox)
        write_json(inputs / "resource_policy.json", resource_policy)
        write_json(
            inputs / "input_manifest.json",
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "source_stage06_decision": source_stage06_decision,
                "handoff_manifest_hash": handoff_manifest["content_hash"],
                "source_manifest_hash": source_manifest["content_hash"],
                "input_fingerprint": fingerprint,
            },
        )
        make_read_only(inputs)
        outputs = root / "outputs"
        outputs.mkdir(parents=True, exist_ok=True)
        copytree_exact(handoff_root, outputs / "task_pair")
        make_writable(outputs)
        if recovery_context:
            (root / "RECOVERY_CONTEXT.md").write_text(
                recovery_context, encoding="utf-8"
            )
            copy_recovery_artifacts(
                recovery_workspace,
                root,
                directory_names=("outputs",),
                include_evidence_trace=True,
            )
            # A failed Agent may have redundantly copied the immutable handoff
            # inside the task tree. It is never a valid deliverable and would
            # otherwise be carried into every recovery attempt.
            redundant_candidate = outputs / "task_pair" / "stage06_candidate"
            if redundant_candidate.is_dir():
                shutil.rmtree(redundant_candidate)
            elif redundant_candidate.exists():
                redundant_candidate.unlink()
            make_writable(outputs)
        max_tool_calls = max(
            4,
            int(
                config.get(
                    "audit_repair_max_tool_calls",
                    config.get("audit_max_tool_calls", config.get("max_tool_calls", 48)),
                )
            ),
        )
        if recovery_context:
            max_tool_calls = max(
                4,
                min(
                    max_tool_calls,
                    int(
                        config.get(
                            "audit_repair_recovery_max_tool_calls",
                            config.get("recovery_max_tool_calls", 16),
                        )
                    ),
                ),
            )
        finalization_reserve = min(
            max_tool_calls - 1,
            max(
                2,
                int(
                    config.get(
                        "audit_repair_finalization_reserve",
                        config.get("finalization_reserve", 8),
                    )
                ),
            ),
        )
        instructions = audit_instructions(
            paper_id=paper_id,
            task_pair_id=task_pair_id,
            manifest_hash=fingerprint,
            max_tool_calls=max_tool_calls,
            finalization_reserve=finalization_reserve,
            source_stage06_decision=source_stage06_decision,
        )
        if recovery_context:
            instructions += recovery_instructions(
                "stage07_audit_repair", max_tool_calls=max_tool_calls
            )
        request = AgentRunRequest(
            phase="stage07_audit_repair",
            record_id=task_pair_id,
            workspace=root,
            instructions=instructions,
            output_schema=STAGE07_AUDIT_SCHEMA,
            prompt_version=STAGE07_AUDIT_VERSION,
            timeout_seconds=int(config.get("timeout_seconds", 7200)),
            metadata={
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "source_stage06_decision": source_stage06_decision,
                "max_tool_calls": max_tool_calls,
                "finalization_reserve": finalization_reserve,
                "inline_contract": False,
                "structured_artifact_path": "outputs/stage07_audit.json",
                "recovery_attempt": bool(recovery_context),
            },
        )
        try:
            result = harness.run(request)
            response = result.response or {}
            _apply_autonomous_public_surface_guard(
                response=response,
                workspace=root,
            )
            write_json(outputs / "stage07_audit.json", response)
            _require_stage07_artifact_delivery(response, root, result)
        except AgentExecutionError as exc:
            last_error = exc
            recovery_context = agent_recovery_context(exc.result)
            recovery_workspace = (
                Path(exc.result.workspace)
                if exc.result is not None and exc.result.workspace
                else None
            )
            if not exc.retryable or attempt >= attempts:
                write_json(
                    failure_checkpoint,
                    {
                        "paper_id": paper_id,
                        "task_pair_id": task_pair_id,
                        "input_fingerprint": fingerprint,
                        "failure_class": exc.failure_class,
                        "retryable": exc.retryable,
                        "agent_run": exc.result.audit_record() if exc.result else None,
                        "failed_at": now_utc(),
                    },
                )
                raise
            delay = min(
                float(config.get("retry_max_seconds", 30)),
                float(config.get("retry_backoff_seconds", 2)) * (2 ** (attempt - 1)),
            )
            if delay > 0:
                time.sleep(delay)
            continue
        staging = prepare_clean_directory(
            artifact_root.parent / f".{artifact_root.name}-{uuid.uuid4().hex[:8]}"
        )
        copytree_exact(outputs, staging / "outputs")
        atomic_commit_tree(staging, artifact_root)
        write_json(
            checkpoint,
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "input_fingerprint": fingerprint,
                "prompt_version": STAGE07_AUDIT_VERSION,
                "response": response,
                "agent_run": result.audit_record(),
                "artifact_manifest_hash": directory_manifest(artifact_root)[
                    "content_hash"
                ],
                "completed_at": now_utc(),
            },
        )
        failure_checkpoint.unlink(missing_ok=True)
        return response, {**result.audit_record(), "cache_hit": False}, artifact_root
    if last_error is not None:
        raise last_error
    raise RuntimeError("Stage07 audit-repair Agent did not execute")


_AUTONOMOUS_PUBLIC_REPLACEMENTS = (
    ("preferred_pathway", "selected_hypothesis"),
    ("preferred pathway", "selected hypothesis"),
    ("intramolecular", "pathway-A"),
    ("bimolecular", "pathway-B"),
    ("intra-molecular", "pathway-A"),
    ("bi-molecular", "pathway-B"),
    ("Int-1", "state-A"),
    ("Int-2", "state-B"),
    ("TS-1a", "transition-A"),
    ("TS-1b", "transition-B"),
    ("wf-nh3-mechanism", "workflow-main"),
    ("claim-1", "claim-main-1"),
    ("claim-2", "claim-main-2"),
    ("claim-3", "claim-main-3"),
    ("Gibbs free energy barriers", "activation free-energy differences"),
    ("PBE0-D3BJ", "an appropriate electronic-structure method"),
    ("def2-TZVP", "a higher-quality basis set"),
    ("def2-SVP", "an optimization basis set"),
    ("Gaussian 16", "a supported quantum-chemistry package"),
    ("SMD(THF)", "implicit solvation"),
    ("SMD", "implicit solvation"),
    ("G70%", "a solution-phase free-energy estimate"),
)
_NEUTRAL_XYZ_NAME_RE = re.compile(r"^structure-(\d{3,})\.xyz$", re.IGNORECASE)


def _xyz_payload(path: Path) -> bytes:
    """Return XYZ content without its free-text comment line.

    Recovery attempts can leave an original file beside the neutral copy and
    the two files can differ only in the comment.  Comparing the scientific
    payload lets the delivery guard remove that duplicate without changing an
    atom count or coordinate record.
    """

    try:
        lines = path.read_bytes().splitlines(keepends=True)
    except OSError:
        return b""
    if len(lines) < 2:
        return b"".join(lines)
    return b"".join((lines[0], *lines[2:]))


def _normalize_public_xyz_inputs(
    *, task_root: Path, note: Any
) -> dict[str, str]:
    """Make every public XYZ input neutral and keep both modes in lockstep.

    The Agent is allowed to rename files, and an interrupted recovery can
    leave both the old and new names in its writable tree.  This routine is a
    deterministic delivery safeguard: it preserves all distinct coordinate
    payloads, removes only duplicate old-name copies, assigns stable
    ``structure-NNN.xyz`` names to every remaining XYZ file, and rewrites the
    second (comment) line.  It returns task-pair-relative old->new path
    mappings so receipts can describe the actual delivered files.
    """

    mode_inputs = {
        mode: task_root / mode / "data" / "inputs"
        for mode in ("paper_reproduction", "autonomous_research")
    }
    all_paths: set[str] = set()
    for inputs in mode_inputs.values():
        if inputs.is_dir():
            all_paths.update(
                path.relative_to(inputs).as_posix()
                for path in inputs.rglob("*.xyz")
                if path.is_file()
            )
    if not all_paths:
        return {}

    # Preserve already-neutral names and assign new numbers to every old name
    # in a stable union order.  A number is reserved globally so the two modes
    # cannot diverge after a recovery copy.
    used_numbers = {
        int(match.group(1))
        for relative in all_paths
        if (match := _NEUTRAL_XYZ_NAME_RE.match(Path(relative).name))
    }
    neutral_by_payload: dict[bytes, str] = {}
    for relative in sorted(all_paths):
        if not _NEUTRAL_XYZ_NAME_RE.match(Path(relative).name):
            continue
        for inputs in mode_inputs.values():
            candidate = inputs / relative
            if candidate.is_file():
                neutral_by_payload.setdefault(_xyz_payload(candidate), relative)
                break
    next_number = max(used_numbers or {0}) + 1
    path_map: dict[str, str] = {}
    for relative in sorted(all_paths):
        if _NEUTRAL_XYZ_NAME_RE.match(Path(relative).name):
            continue
        matching_neutral: str | None = None
        for inputs in mode_inputs.values():
            candidate = inputs / relative
            if candidate.is_file():
                matching_neutral = neutral_by_payload.get(_xyz_payload(candidate))
                if matching_neutral:
                    break
        if matching_neutral:
            path_map[relative] = matching_neutral
            continue
        parent = Path(relative).parent.as_posix()
        while next_number in used_numbers:
            next_number += 1
        target_name = f"structure-{next_number:03d}.xyz"
        used_numbers.add(next_number)
        next_number += 1
        path_map[relative] = (
            f"{parent}/{target_name}" if parent not in {"", "."} else target_name
        )

    # Stage all renames through temporary names to avoid collisions with an
    # existing neutral file.  The same mapping is applied to both modes.
    for inputs in mode_inputs.values():
        if not inputs.is_dir():
            continue
        staged: list[tuple[Path, Path, str]] = []
        for old_relative, new_relative in path_map.items():
            old_path = inputs / old_relative
            if not old_path.is_file():
                continue
            target_path = inputs / new_relative
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if target_path.exists():
                if _xyz_payload(old_path) == _xyz_payload(target_path):
                    old_path.unlink()
                    note(old_path)
                    continue
                # A genuine distinct payload already occupies the proposed
                # name.  Keep the old payload under a fresh neutral name and
                # update the mapping for this mode-independent path.
                suffix = 1
                candidate = target_path.with_name(
                    f"{target_path.stem}-{suffix}{target_path.suffix}"
                )
                while candidate.exists():
                    suffix += 1
                    candidate = target_path.with_name(
                        f"{target_path.stem}-{suffix}{target_path.suffix}"
                    )
                target_path = candidate
                new_relative = target_path.relative_to(inputs).as_posix()
                path_map[old_relative] = new_relative
            temporary = old_path.with_name(
                f".{old_path.name}.neutralize-{uuid.uuid4().hex[:8]}"
            )
            old_path.rename(temporary)
            staged.append((temporary, target_path, old_relative))
            note(target_path)
            note(old_path)
        for temporary, target_path, _ in staged:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            temporary.rename(target_path)

    # Normalize comments after all renames.  This is metadata-only; atom and
    # coordinate lines remain byte-for-byte unchanged.
    for inputs in mode_inputs.values():
        if not inputs.is_dir():
            continue
        for path in sorted(inputs.rglob("*.xyz")):
            if not path.is_file():
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines(
                    keepends=True
                )
            except OSError:
                continue
            if len(lines) < 2:
                continue
            neutral_comment = f"# {path.stem}\n"
            if lines[1] != neutral_comment:
                lines[1] = neutral_comment
                path.write_text("".join(lines), encoding="utf-8")
                note(path)

    # A recovery may have copied a stale manifest containing old paths.  The
    # caller rewrites manifests after this function; returning the mapping is
    # enough to repair receipts and textual references first.
    return path_map


def _rewrite_public_xyz_references(
    *, task_root: Path, path_map: dict[str, str], note: Any
) -> None:
    if not path_map:
        return
    for path in sorted(task_root.rglob("*")):
        if not path.is_file() or path.name in {"public_manifest.json", "task_pair_manifest.json"}:
            continue
        if path.suffix.casefold() not in {".json", ".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        updated = text
        for old_relative, new_relative in path_map.items():
            updated = updated.replace(old_relative, new_relative)
            updated = updated.replace(old_relative.replace("/", "\\"), new_relative)
            old_coords = f"coordinates/{Path(old_relative).name}"
            new_coords = f"coordinates/{Path(new_relative).name}"
            updated = updated.replace(old_coords, new_coords)
            # Autonomous text must not retain a bare route-specific filename.
            # Reproduction route prose may retain author labels, but path-like
            # references still use the neutral asset name.
            if "autonomous_research" in path.relative_to(task_root).parts:
                updated = updated.replace(Path(old_relative).name, Path(new_relative).name)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            note(path)


def _normalize_reported_change_paths(
    *, response: dict[str, Any], task_root: Path, path_map: dict[str, str]
) -> None:
    """Convert Agent pre-rename receipt paths to delivered neutral paths."""

    def normalize(raw: Any) -> str | None:
        try:
            relative = validate_relative_path(str(raw))
        except ValueError:
            return None
        mapped = relative
        for mode in ("paper_reproduction", "autonomous_research"):
            prefix = f"{mode}/data/inputs/"
            if relative.startswith(prefix):
                inner = relative[len(prefix) :]
                mapped_inner = path_map.get(inner, inner)
                mapped = prefix + mapped_inner
                break
        candidate = task_root / mapped
        if candidate.exists():
            return mapped
        # Deleted old paths are represented by their delivered replacement.
        if mapped != relative and (task_root / mapped).exists():
            return mapped
        return None

    for repair in response.get("repairs") or []:
        if not isinstance(repair, dict):
            continue
        repair["changed_files"] = list(
            dict.fromkeys(
                value
                for value in (normalize(raw) for raw in repair.get("changed_files") or [])
                if value
            )
        )
    redesign = response.get("workflow_redesign")
    if isinstance(redesign, dict):
        redesign["changed_files"] = list(
            dict.fromkeys(
                value
                for value in (normalize(raw) for raw in redesign.get("changed_files") or [])
                if value
            )
        )


def _apply_autonomous_public_surface_guard(
    *, response: dict[str, Any], workspace: Path
) -> list[str]:
    """Enforce the non-negotiable public/private boundary after Agent approval.

    This is deliberately a narrow delivery guard rather than a scientific
    validator.  Stage07's Agent remains responsible for workflow selection,
    completeness, and scientific repairs.  The guard only removes known route
    identifiers/method metadata that must never reach an autonomous task, keeps
    both input trees aligned, and refreshes their manifests when a low-cost Agent
    forgot to do so.
    """

    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return []
    relative = str(response.get("artifact_path") or "")
    try:
        relative = validate_relative_path(relative)
    except ValueError:
        return []
    if relative != "outputs/task_pair":
        return []
    task_root = (workspace / relative).resolve()
    autonomous = task_root / "autonomous_research"
    reproduction = task_root / "paper_reproduction"
    if not autonomous.is_dir():
        return []

    changed: list[str] = []

    def note(path: Path) -> None:
        rel = path.relative_to(task_root).as_posix()
        if rel not in changed:
            changed.append(rel)

    def replace_text(value: str) -> str:
        output = value
        for old, new in _AUTONOMOUS_PUBLIC_REPLACEMENTS:
            output = re.sub(re.escape(old), new, output, flags=re.IGNORECASE)
        return output

    def scrub_json(value: Any) -> tuple[Any, bool]:
        dirty = False
        if isinstance(value, dict):
            output: dict[str, Any] = {}
            for raw_key, raw_value in value.items():
                key = str(raw_key)
                lowered = key.casefold()
                if lowered in {"included_workflow_ids", "included_claim_ids"}:
                    dirty = True
                    continue
                new_key = replace_text(key)
                if new_key != key:
                    dirty = True
                new_value, value_dirty = scrub_json(raw_value)
                dirty = dirty or value_dirty
                output[new_key] = new_value
            return output, dirty
        if isinstance(value, list):
            output_list = []
            for item in value:
                new_item, item_dirty = scrub_json(item)
                dirty = dirty or item_dirty
                output_list.append(new_item)
            return output_list, dirty
        if isinstance(value, str):
            output = replace_text(value)
            return output, output != value
        return value, False

    # Normalize every XYZ input, not only the handful of names seen in an
    # earlier pilot.  This also repairs recovery trees that contain both an
    # old route-specific file and a neutral copy.
    xyz_path_map = _normalize_public_xyz_inputs(task_root=task_root, note=note)
    _rewrite_public_xyz_references(
        task_root=task_root,
        path_map=xyz_path_map,
        note=note,
    )

    # Rewrite all autonomous JSON/Markdown public surfaces.  Do not touch hidden
    # references or the reproduction route text.
    for path in sorted(autonomous.rglob("*")):
        if not path.is_file() or path.name in {"public_manifest.json"}:
            continue
        if path.suffix.casefold() == ".json":
            try:
                original = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            scrubbed, dirty = scrub_json(original)
            if dirty:
                path.write_text(
                    json.dumps(scrubbed, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                note(path)
        elif path.suffix.casefold() in {".md", ".txt"}:
            try:
                original_text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            scrubbed_text = replace_text(original_text)
            if scrubbed_text != original_text:
                path.write_text(scrubbed_text, encoding="utf-8")
                note(path)

    # A route bundle has no place in autonomous public inputs, even if an Agent
    # accidentally retained it while copying the reproduction task.
    for forbidden_name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
        path = autonomous / forbidden_name
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            note(path)

    # Refresh mode manifests after deterministic edits.  directory_manifest
    # excludes the manifest itself, matching Stage06's public-manifest contract.
    for mode_root in (reproduction, autonomous):
        if not mode_root.is_dir():
            continue
        manifest_path = mode_root / "public_manifest.json"
        before = manifest_path.read_bytes() if manifest_path.is_file() else None
        write_json(manifest_path, directory_manifest(mode_root))
        if before != manifest_path.read_bytes():
            note(manifest_path)
    pair_manifest = task_root / "task_pair_manifest.json"
    before_pair = pair_manifest.read_bytes() if pair_manifest.is_file() else None
    write_manifest(task_root, pair_manifest)
    if before_pair != pair_manifest.read_bytes():
        note(pair_manifest)

    # Agent receipts are written before deterministic delivery edits and may
    # therefore mention the pre-rename paths.  Translate those claims to the
    # files that actually exist in the delivered tree before the objective
    # delivery gate runs.
    _normalize_reported_change_paths(
        response=response,
        task_root=task_root,
        path_map=xyz_path_map,
    )

    # Deleted old names are useful internally for the guard, but a receipt must
    # list delivered paths.  Keep only paths that exist after normalization.
    changed = [
        relative
        for relative in changed
        if (task_root / relative).exists()
    ]

    if changed:
        response["audit_decision"] = (
            "approved_with_repairs"
            if decision == "approved"
            else decision
        )
        response["repair_origin"] = response.get("repair_origin") or "stage07_public_surface_guard"
        repairs = response.setdefault("repairs", [])
        repairs.append(
            {
                "category": "autonomous_public_surface_guard",
                "details": (
                    "Deterministically removed residual route/method identifiers from the "
                    "autonomous public surface, normalized public input names/comments, and "
                    "refreshed mode and pair manifests."
                ),
                "source_evidence_ids": [],
                "changed_files": changed,
            }
        )
        response["summary"] = (
            str(response.get("summary") or "").rstrip()
            + " A deterministic public-surface guard removed residual route metadata and "
            "refreshed manifests after the Agent write."
        ).strip()
    return changed


def _require_stage07_artifact_delivery(
    response: dict[str, Any], workspace: Path, result: Any
) -> None:
    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return
    try:
        relative = validate_relative_path(str(response.get("artifact_path") or ""))
        artifact = (workspace.resolve() / relative).resolve()
        artifact.relative_to(workspace.resolve())
        if relative != "outputs/task_pair":
            raise ValueError("approved artifact_path must be outputs/task_pair")
        if not artifact.is_dir() or not any(path.is_file() for path in artifact.rglob("*")):
            raise FileNotFoundError("approved task-pair directory is empty or missing")
        if (artifact / "stage06_candidate").exists():
            raise ValueError(
                "approved task-pair contains a redundant stage06_candidate source copy"
            )
        _require_reported_stage07_changes(
            response=response,
            artifact=artifact,
            baseline=workspace / "inputs" / "stage06_candidate",
        )
        return
    except (FileNotFoundError, OSError, ValueError) as exc:
        message = f"Stage07 approved a task but did not deliver its task tree: {exc}"
        result.status = "failed"
        result.failure_class = "missing_agent_artifact"
        result.retryable = True
        result.error = {"error_type": "MissingAgentArtifact", "message": message}
        write_json(workspace / "agent_run.json", result.audit_record())
        raise AgentExecutionError(
            message,
            failure_class="missing_agent_artifact",
            retryable=True,
            result=result,
        ) from exc


def _require_reported_stage07_changes(
    *, response: dict[str, Any], artifact: Path, baseline: Path
) -> None:
    """Verify only the objective fact that claimed file edits were delivered.

    This intentionally does not judge scientific validity or task quality. It
    prevents an interrupted tool turn from publishing an audit that says files
    were repaired while returning the unchanged Stage06 tree.
    """

    decision = str(response.get("audit_decision") or "")
    reported: list[str] = []
    for repair in response.get("repairs") or []:
        if isinstance(repair, dict):
            reported.extend(str(path) for path in repair.get("changed_files") or [])
    redesign = response.get("workflow_redesign") or {}
    if isinstance(redesign, dict):
        reported.extend(str(path) for path in redesign.get("changed_files") or [])
    reported = list(dict.fromkeys(path for path in reported if path.strip()))

    if decision == "approved_with_repairs" and not reported:
        raise ValueError("approved_with_repairs did not report any changed task file")

    unchanged: list[str] = []
    missing: list[str] = []
    for raw_path in reported:
        relative = validate_relative_path(raw_path)
        delivered = (artifact / relative).resolve()
        delivered.relative_to(artifact.resolve())
        original = (baseline / relative).resolve()
        original.relative_to(baseline.resolve())
        if not delivered.exists():
            missing.append(relative)
            continue
        if original.exists() and _stage07_paths_equal(original, delivered):
            unchanged.append(relative)
    if missing:
        raise ValueError(
            "Stage07 reported changed files that were not delivered: " + ", ".join(missing)
        )

    # Low-cost Agents occasionally include a file in ``changed_files`` after
    # inspecting it but leave its bytes untouched (for example, a reproduction
    # route file that was already normalized by Stage06).  This is an objective
    # receipt issue, not a scientific audit failure.  Remove those stale claims
    # from the receipt while retaining the hard requirement that at least one
    # actual repair was delivered for ``approved_with_repairs``.
    if unchanged:
        unchanged_set = set(unchanged)
        filtered_repairs: list[tuple[dict[str, Any], list[str]]] = []
        for repair in response.get("repairs") or []:
            if not isinstance(repair, dict):
                continue
            filtered_repairs.append((repair, [
                str(path)
                for path in repair.get("changed_files") or []
                if validate_relative_path(str(path)) not in unchanged_set
            ]))
        filtered_redesign: list[str] = []
        if isinstance(response.get("workflow_redesign"), dict):
            redesign = response["workflow_redesign"]
            filtered_redesign = [
                str(path)
                for path in redesign.get("changed_files") or []
                if validate_relative_path(str(path)) not in unchanged_set
            ]
        remaining_reported = [
            str(path)
            for _, paths in filtered_repairs
            for path in paths
        ]
        remaining_reported.extend(filtered_redesign)
        if decision == "approved_with_repairs" and not remaining_reported:
            raise ValueError(
                "Stage07 approved_with_repairs delivered no file that differs from the baseline"
            )
        for repair, paths in filtered_repairs:
            repair["changed_files"] = paths
        if isinstance(response.get("workflow_redesign"), dict):
            response["workflow_redesign"]["changed_files"] = filtered_redesign


def _stage07_paths_equal(left: Path, right: Path) -> bool:
    if left.is_file() and right.is_file():
        return left.read_bytes() == right.read_bytes()
    if left.is_dir() and right.is_dir():
        return directory_manifest(left)["content_hash"] == directory_manifest(right)[
            "content_hash"
        ]
    return False


def _stage07_approved_artifact(response: dict[str, Any], artifact_root: Path) -> Path:
    relative = validate_relative_path(str(response.get("artifact_path") or ""))
    if relative != "outputs/task_pair":
        raise ValueError("approved Stage07 artifact_path must be outputs/task_pair")
    path = (artifact_root.resolve() / relative).resolve()
    path.relative_to(artifact_root.resolve())
    if not path.is_dir() or not any(item.is_file() for item in path.rglob("*")):
        raise FileNotFoundError(f"Stage07 task artifact is missing or empty: {path}")
    return path


def _publish_stage07_rejection(
    *,
    stage_root: Path,
    paper_id: str,
    response: dict[str, Any],
    stage06_record: dict[str, Any],
    handoff_root: Path,
) -> Path:
    staging = prepare_clean_directory(
        stage_root / "staging" / safe_component(paper_id) / f"rejected-{uuid.uuid4().hex[:8]}"
    )
    for name in (
        "paper_info.json",
        "workflow_review.json",
        "construction_receipt.json",
        "stage06_handoff.json",
    ):
        source = handoff_root / name
        if source.is_file():
            shutil.copy2(source, staging / name)
    write_json(staging / "stage06_handoff_record.json", stage06_record)
    write_json(staging / "stage07_audit.json", response)
    write_manifest(staging, staging / "audit_manifest.json")
    target = stage_root / "rejected_tasks" / safe_component(paper_id)
    atomic_commit_tree(staging, target)
    return target


def _resolve_stage07_source_root(
    *,
    record: dict[str, Any],
    paper_id: str,
    documents: list[dict[str, Any]],
    stage_root: Path,
    config: dict[str, Any],
) -> Path:
    source_value = record.get("source_snapshot_path")
    if source_value:
        source = Path(str(source_value)).expanduser().resolve()
        if source.is_dir():
            return source
    return _prepare_stage07_fallback_source(
        paper_id=paper_id,
        documents=documents,
        stage_root=stage_root,
        config=config,
    )


def _prepare_stage07_fallback_source(
    *,
    paper_id: str,
    documents: list[dict[str, Any]],
    stage_root: Path,
    config: dict[str, Any],
) -> Path:
    if not documents:
        raise FileNotFoundError(f"No Stage04 source documents are available for {paper_id}")
    identity = canonical_hash(
        [
            {
                "document_id": row.get("document_id"),
                "sha256": row.get("sha256"),
                "source_path": row.get("source_path"),
                "normalized_markdown_path": row.get("normalized_markdown_path"),
                "content_blocks_path": row.get("content_blocks_path"),
            }
            for row in documents
        ]
    )
    root = stage_root / "source_snapshots" / safe_component(paper_id) / identity[:16]
    complete = root / "snapshot_complete.json"
    if complete.is_file():
        return root
    prepare_clean_directory(root)
    source_manifest: list[dict[str, Any]] = []
    for document in sorted(documents, key=lambda row: str(row.get("document_id") or "")):
        document_id = safe_component(str(document.get("document_id") or "document"))
        document_root = root / "documents" / document_id
        document_root.mkdir(parents=True, exist_ok=True)
        copied: list[str] = []
        for key, name in (
            ("normalized_markdown_path", "normalized_document.md"),
            ("content_blocks_path", "content_blocks.jsonl"),
            ("layout_text_path", "layout_text.txt"),
            ("pypdf_layout_path", "pypdf_layout.txt"),
            ("tables_path", "tables.json"),
        ):
            value = document.get(key)
            if not value:
                continue
            source = Path(str(value)).expanduser().resolve()
            if source.is_file():
                shutil.copy2(source, document_root / name)
                copied.append(f"documents/{document_id}/{name}")
        source_value = document.get("source_path")
        if source_value:
            source_pdf = Path(str(source_value)).expanduser().resolve()
            if source_pdf.is_file() and source_pdf.suffix.casefold() == ".pdf":
                if str(document.get("document_role") or "") == "main_paper":
                    target = root / "main_paper.pdf"
                else:
                    target = root / "supplementary" / f"{document_id}.pdf"
                    target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_pdf, target)
                copied.append(target.relative_to(root).as_posix())
        write_json(document_root / "source_metadata.json", document)
        source_manifest.append(
            {
                "document_id": document.get("document_id"),
                "document_role": document.get("document_role"),
                "materials": copied,
            }
        )
    write_json(root / "source_manifest.json", source_manifest)
    toolbox_path = config.get("toolbox_capabilities")
    if toolbox_path and Path(str(toolbox_path)).expanduser().is_file():
        shutil.copy2(Path(str(toolbox_path)).expanduser(), root / "toolbox_snapshot.json")
    else:
        write_json(root / "toolbox_snapshot.json", {"snapshot_status": "unavailable"})
    write_json(root / "resource_policy.json", config.get("resource_policy") or {})
    write_json(
        complete,
        {"paper_id": paper_id, "identity": identity, "created_at": now_utc()},
    )
    make_read_only(root)
    return root


def _stage07_toolbox_snapshot(
    source_root: Path, handoff_root: Path, config: dict[str, Any]
) -> dict[str, Any]:
    for path in (
        source_root / "toolbox_snapshot.json",
        Path(str(config.get("toolbox_capabilities") or "" )).expanduser(),
    ):
        if str(path) and path.is_file():
            return read_json(path)
    requirements = handoff_root / "toolbox_requirements.json"
    return {
        "snapshot_status": "requirements_only",
        "requirements": read_json(requirements) if requirements.is_file() else [],
    }


def _stage07_resource_policy(source_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path = source_root / "resource_policy.json"
    if path.is_file():
        value = read_json(path)
        if isinstance(value, dict):
            return value
    return dict(config.get("resource_policy") or {})


def _run_audit_agent(
    *,
    harness,
    stage_root: Path,
    paper_id: str,
    task_pair_id: str,
    pair_root: Path,
    pair_manifest: dict[str, Any],
    deterministic: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    toolbox = _toolbox_snapshot_from_pair(pair_root, config)
    resource_policy = config.get("resource_policy") or {}
    fingerprint = input_fingerprint(
        {
            "pair_manifest_hash": pair_manifest["content_hash"],
            "deterministic": deterministic,
            "toolbox": toolbox,
            "resource_policy": resource_policy,
            "prompt_version": STAGE07_AUDIT_VERSION,
            "harness": harness.name,
            "model": harness.model,
        }
    )
    checkpoint = stage_root / "checkpoints" / safe_component(paper_id) / "objective_audit.json"
    if bool(config.get("resume", True)) and checkpoint.is_file():
        cached = read_json(checkpoint)
        cached_fingerprint = cached.get("input_fingerprint")
        legacy_fingerprint = input_fingerprint(
            {
                "pair_manifest_hash": directory_manifest(pair_root)["content_hash"],
                "deterministic": deterministic,
                "prompt_version": STAGE07_AUDIT_VERSION,
                "harness": harness.name,
                "model": harness.model,
            }
        )
        stable_input_match = _cached_audit_inputs_match(
            cached,
            stage_root=stage_root,
            pair_manifest_hash=str(pair_manifest["content_hash"]),
            toolbox=toolbox,
            resource_policy=resource_policy,
            harness_name=harness.name,
            model_name=harness.model,
        )
        if cached_fingerprint in {fingerprint, legacy_fingerprint} or stable_input_match:
            response = cached.get("response")
            jsonschema.validate(response, STAGE07_AUDIT_SCHEMA)
            if cached_fingerprint != fingerprint:
                cached["input_fingerprint"] = fingerprint
                write_json(checkpoint, cached)
            return response, {**(cached.get("agent_run") or {}), "cache_hit": True}

    attempts = max(1, int(config.get("max_attempts", 3)))
    last_error: AgentExecutionError | None = None
    recovery_context: str | None = None
    recovery_workspace: Path | None = None
    for attempt in range(1, attempts + 1):
        root = prepare_clean_directory(
            stage_root
            / "workspaces"
            / safe_component(paper_id)
            / "objective_audit"
            / f"attempt-{attempt:02d}-{uuid.uuid4().hex[:8]}"
        )
        inputs = root / "inputs"
        inputs.mkdir(parents=True, exist_ok=True)
        copytree_exact(pair_root, inputs / "task_pair")
        audit_packet = _stage07_audit_packet(
            pair_root=pair_root,
            pair_manifest=pair_manifest,
            deterministic=deterministic,
            toolbox=toolbox,
            resource_policy=resource_policy,
        )
        write_json(inputs / "toolbox_snapshot.json", toolbox)
        write_json(inputs / "resource_policy.json", resource_policy)
        write_json(inputs / "deterministic_audit.json", deterministic)
        write_json(inputs / "audit_packet.json", audit_packet)
        write_json(
            inputs / "objective_audit_scaffold.json",
            _stage07_audit_scaffold(deterministic, audit_packet),
        )
        (inputs / "initialize_objective_audit.py").write_text(
            _stage07_audit_initializer_script(), encoding="utf-8"
        )
        make_read_only(inputs)
        max_tool_calls = int(
            config.get("audit_max_tool_calls", config.get("max_tool_calls", 16))
        )
        if recovery_context:
            max_tool_calls = min(
                max_tool_calls,
                int(
                    config.get(
                        "audit_recovery_max_tool_calls",
                        config.get("recovery_max_tool_calls", 8),
                    )
                ),
            )
        max_tool_calls = max(2, max_tool_calls)
        finalization_reserve = min(
            max_tool_calls - 1,
            max(
                1,
                int(config.get("audit_finalization_reserve", max_tool_calls - 1)),
            ),
        )
        instructions = audit_instructions(
            paper_id=paper_id,
            task_pair_id=task_pair_id,
            manifest_hash=pair_manifest["content_hash"],
            max_tool_calls=max_tool_calls,
            finalization_reserve=finalization_reserve,
        )
        if recovery_context:
            (root / "RECOVERY_CONTEXT.md").write_text(recovery_context, encoding="utf-8")
            copy_recovery_artifacts(recovery_workspace, root)
            instructions += recovery_instructions(
                "stage07_objective_audit", max_tool_calls=max_tool_calls
            )
        request = AgentRunRequest(
            phase="stage07_objective_audit",
            record_id=task_pair_id,
            workspace=root,
            instructions=instructions,
            output_schema=STAGE07_AUDIT_SCHEMA,
            prompt_version=STAGE07_AUDIT_VERSION,
            timeout_seconds=int(config.get("timeout_seconds", 3600)),
            metadata={
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "max_tool_calls": max_tool_calls,
                "finalization_reserve": finalization_reserve,
                "inline_contract": False,
                "structured_artifact_path": "outputs/objective_audit.json",
                "recovery_attempt": bool(recovery_context),
            },
        )
        try:
            result = harness.run(request)
            semantic_findings = validate_agent_audit(result.response or {})
            if semantic_findings:
                message = (
                    "Stage07 Agent contract failed semantic validation: "
                    + ", ".join(semantic_findings)
                )
                result.status = "failed"
                result.failure_class = "invalid_phase_contract"
                result.retryable = True
                result.error = {
                    "error_type": "InvalidPhaseContract",
                    "message": message[:4000],
                }
                write_json(root / "agent_run.json", result.audit_record())
                raise AgentExecutionError(
                    message,
                    failure_class="invalid_phase_contract",
                    retryable=True,
                    result=result,
                )
        except AgentExecutionError as exc:
            last_error = exc
            if not exc.retryable or attempt >= attempts:
                raise
            recovery_context = agent_recovery_context(exc.result)
            recovery_workspace = (
                Path(exc.result.workspace) if exc.result and exc.result.workspace else None
            )
            delay = min(
                float(config.get("retry_max_seconds", 30)),
                float(config.get("retry_backoff_seconds", 2)) * (2 ** (attempt - 1)),
            )
            if delay > 0:
                time.sleep(delay)
            continue
        write_json(
            checkpoint,
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "input_fingerprint": fingerprint,
                "prompt_version": STAGE07_AUDIT_VERSION,
                "response": result.response,
                "agent_run": result.audit_record(),
                "completed_at": now_utc(),
            },
        )
        return result.response or {}, {**result.audit_record(), "cache_hit": False}
    if last_error is not None:
        raise last_error
    raise RuntimeError("Stage07 Agent audit did not execute")


def _audit_pair_manifest(pair_root: Path) -> dict[str, Any]:
    """Hash task semantics without volatile Stage06 execution provenance."""

    manifest = directory_manifest(
        pair_root,
        ignored_names=STAGE07_IGNORED_PAIR_FILES,
    )
    semantic_files: list[dict[str, str]] = []
    for row in manifest["files"]:
        semantic_hash = str(row["sha256"])
        if row["path"] == "paper_info.json":
            paper_info = read_json(pair_root / "paper_info.json")
            paper_info.pop("constructed_at", None)
            semantic_hash = canonical_hash(paper_info)
        semantic_files.append({"path": str(row["path"]), "semantic_hash": semantic_hash})
    manifest["format"] = "researchchembench.audit-input-manifest.v1"
    manifest["content_hash"] = canonical_hash(semantic_files)
    manifest["normalizations"] = {
        "ignored_files": ["construction_record.json"],
        "ignored_fields": ["paper_info.json#/constructed_at"],
    }
    return manifest


def _cached_audit_inputs_match(
    cached: dict[str, Any],
    *,
    stage_root: Path,
    pair_manifest_hash: str,
    toolbox: dict[str, Any],
    resource_policy: dict[str, Any],
    harness_name: str,
    model_name: str,
) -> bool:
    """Safely migrate a pre-stable-fingerprint Stage07 checkpoint."""

    if cached.get("prompt_version") != STAGE07_AUDIT_VERSION:
        return False
    agent_run = cached.get("agent_run") or {}
    if agent_run.get("harness") != harness_name or agent_run.get("model") != model_name:
        return False
    try:
        previous_workspace = Path(str(agent_run["workspace"])).expanduser().resolve()
        previous_workspace.relative_to((stage_root / "workspaces").resolve())
        previous_pair = previous_workspace / "inputs" / "task_pair"
        if _audit_pair_manifest(previous_pair)["content_hash"] != pair_manifest_hash:
            return False
        if read_json(previous_workspace / "inputs" / "toolbox_snapshot.json") != toolbox:
            return False
        if read_json(previous_workspace / "inputs" / "resource_policy.json") != resource_policy:
            return False
    except (KeyError, FileNotFoundError, OSError, ValueError, json.JSONDecodeError):
        return False
    return True


def deterministic_judge_audit(pair: Any) -> dict[str, Any]:
    """Compatibility entry point with support for the new task-pair directory."""

    if isinstance(pair, (str, Path)):
        return deterministic_stage07_audit(Path(pair))
    findings = []
    for mode in ("autonomous", "reproduction"):
        if not pair.get(mode, {}).get("task_info") or not pair.get(mode, {}).get("task_markdown"):
            findings.append(f"{mode}_incomplete")
    if (
        not pair.get("scientific_record")
        or not pair.get("hidden_reference")
        or not pair.get("evidence_map")
    ):
        findings.append("shared_record_incomplete")
    return {"passed": not findings, "findings": findings}


def run_gold(record, config, stage_root):
    """Deprecated boundary marker: Stage07 no longer executes Gold Runs."""

    return {"status": "not_run", "reason": "gold_run_moved_outside_stage07"}


def _toolbox_snapshot_from_pair(pair_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path_value = config.get("toolbox_capabilities")
    if path_value:
        path = Path(str(path_value)).expanduser().resolve()
        if path.is_file():
            return read_json(path)
    requirements = pair_root / "toolbox_requirements.json"
    return {
        "snapshot_status": "requirements_only",
        "requirements": read_json(requirements) if requirements.is_file() else [],
    }


def _stage07_audit_packet(
    *,
    pair_root: Path,
    pair_manifest: dict[str, Any],
    deterministic: dict[str, Any],
    toolbox: dict[str, Any],
    resource_policy: dict[str, Any],
) -> dict[str, Any]:
    autonomous_info = read_json(pair_root / "autonomous_research" / "task_info.json")
    autonomous_spec = read_json(pair_root / "autonomous_research" / "task_spec.json")
    reproduction_info = read_json(pair_root / "paper_reproduction" / "task_info.json")
    reproduction_spec = read_json(pair_root / "paper_reproduction" / "task_spec.json")
    workflow = read_json(pair_root / "paper_reproduction" / "workflow_spec.json")
    submission = read_json(pair_root / "autonomous_research" / "submission_contract.json")
    hidden = read_json(pair_root / "hidden_reference" / "ground_truth_common.json")
    paper_info = read_json(pair_root / "paper_info.json")
    workflow_review_path = pair_root / "workflow_review.json"
    workflow_review = read_json(workflow_review_path) if workflow_review_path.is_file() else {}
    requirements_path = pair_root / "toolbox_requirements.json"
    requirements = read_json(requirements_path) if requirements_path.is_file() else []
    mode_fields = (
        "task_id",
        "task_pair_id",
        "task_mode",
        "scientific_mode",
        "method_disclosure",
        "pathway_disclosure",
        "category",
        "benchmark_family",
    )
    shared_spec_fields = (
        "scientific_question",
        "target_definition",
        "boundary_conditions",
        "input_assets",
        "workflow_scope",
        "complexity_profile",
        "resources",
        "resource_policy",
        "required_outputs",
    )
    profiles = hidden.get("acceptance_profiles") or []
    rubric = hidden.get("scientific_conclusion_rubric") or []
    workflow_steps = next(
        (
            workflow.get(key)
            for key in ("workflow_steps", "steps", "route_steps")
            if workflow.get(key)
        ),
        [],
    )
    workflow_summary = {
        key: workflow.get(key)
        for key in ("software", "method", "method_parameters", "validation_procedure")
        if workflow.get(key) not in (None, [], {}, "")
    }
    workflow_summary["steps"] = workflow_steps
    return {
        "pair_manifest_hash": pair_manifest["content_hash"],
        "deterministic_audit": deterministic,
        "mode_summaries": {
            "shared_task_spec": {
                key: autonomous_spec.get(key)
                for key in shared_spec_fields
                if key in autonomous_spec
            },
            "autonomous_research": {
                "task_info": {
                    key: autonomous_info.get(key) for key in mode_fields if key in autonomous_info
                },
                "task_spec": {"mode": autonomous_spec.get("mode")},
            },
            "paper_reproduction": {
                "task_info": {
                    key: reproduction_info.get(key)
                    for key in mode_fields
                    if key in reproduction_info
                },
                "task_spec": {"mode": reproduction_spec.get("mode")},
            },
        },
        "workflow_summary": workflow_summary,
        "workflow_selection": {
            "workflow_scope": workflow_review.get("workflow_scope")
            or paper_info.get("workflow_scope")
            or autonomous_spec.get("workflow_scope")
            or {},
            "complexity_profile": workflow_review.get("complexity_profile")
            or paper_info.get("complexity_profile")
            or autonomous_spec.get("complexity_profile")
            or {},
            "paper_workflow_inventory_complete": workflow_review.get(
                "paper_workflow_inventory_complete"
            ),
            "full_paper_workflow_checked": workflow_review.get(
                "full_paper_workflow_checked"
            ),
            "alternative_scope_search_complete": workflow_review.get(
                "alternative_scope_search_complete"
            ),
            "workflow_inventory": workflow_review.get("workflow_inventory") or [],
            "stage05_candidate_disposition": workflow_review.get(
                "stage05_candidate_disposition"
            ),
        },
        "submission_contract": {
            "required_files": submission.get("required_files") or [],
            "artifact_paths": submission.get("artifact_paths") or {},
            "result_schema_names": sorted(
                key for key in submission if "schema" in str(key).casefold()
            ),
        },
        "hidden_scoring_summary": {
            "ground_truth_items": [
                {
                    key: item.get(key)
                    for key in (
                        "ground_truth_id",
                        "kind",
                        "acceptance_type",
                        "acceptance_profile_id",
                        "evidence_grade",
                        "evidence_ids",
                        "claim_role",
                        "applies_to_modes",
                    )
                }
                for item in hidden.get("ground_truth_items") or []
            ],
            "acceptance_profiles": [
                {
                    "acceptance_profile_id": profile.get("acceptance_profile_id"),
                    "type": profile.get("type"),
                    "submission_binding": {
                        key: (profile.get("submission_binding") or {}).get(key)
                        for key in ("artifact_paths", "observed_fields")
                        if key in (profile.get("submission_binding") or {})
                    },
                    "comparison_rule_present": bool(
                        (profile.get("submission_binding") or {}).get("comparison")
                    ),
                }
                for profile in profiles
            ],
            "scientific_conclusion_rubric": [
                {
                    key: criterion.get(key)
                    for key in (
                        "id",
                        "max_score",
                        "ground_truth_ids",
                        "acceptance_profile_ids",
                        "required_evidence",
                    )
                }
                for criterion in rubric
            ],
        },
        "provenance_summary": {
            **{
                key: paper_info.get(key)
                for key in ("paper_id", "task_pair_id", "doi", "title", "journal")
                if key in paper_info
            },
            "documents": [
                {
                    key: document.get(key)
                    for key in (
                        "document_id",
                        "document_role",
                        "file_name",
                        "sha256",
                        "size_bytes",
                        "source_remote_uri",
                        "selected_parser",
                    )
                    if key in document
                }
                for document in paper_info.get("documents") or []
                if isinstance(document, dict)
            ],
        },
        "source_evidence_bundle": _stage07_source_evidence_bundle(
            pair_root, workflow_review=workflow_review, hidden=hidden
        ),
        "toolbox_requirements": requirements,
        "toolbox_focus": _focused_toolbox_view(toolbox, requirements),
        "resource_policy": resource_policy,
        "unresolved_questions": [
            "Was a larger complete computational scope available but not selected?",
            "Does the task provide genuine medium/high scientific complexity rather than split non-core steps?",
            "Are requirements marked unknown actually unsupported, or only unverified?",
            "Is the requested workflow obviously infeasible under the stated resource policy?",
        ],
        "targeted_fallback_paths": [
            "inputs/task_pair/paper_reproduction/workflow_spec.json",
            "inputs/task_pair/workflow_review.json",
            "inputs/task_pair/toolbox_requirements.json",
            "inputs/task_pair/hidden_reference/acceptance_profiles.json",
            "inputs/task_pair/paper_info.json",
        ],
    }


def _focused_toolbox_view(
    toolbox: dict[str, Any], requirements: list[dict[str, Any]]
) -> dict[str, Any]:
    names = {
        str(
            row.get("software")
            or row.get("tool")
            or row.get("normalized_backend")
            or ""
        ).casefold()
        for row in requirements
        if isinstance(row, dict)
    }
    names.discard("")
    focused: dict[str, Any] = {
        key: toolbox.get(key)
        for key in (
            "schema_version",
            "profile_id",
            "catalog_hash",
            "runtime_profile_hash",
            "snapshot_status",
            "unknown_field_policy",
            "execution_layers",
        )
        if key in toolbox
    }
    for section in ("backends", "native_software", "python_packages"):
        rows = toolbox.get(section)
        if not isinstance(rows, dict):
            continue
        selected = {
            name: value
            for name, value in rows.items()
            if str(name).casefold() in names
            or any(alias in str(name).casefold() for alias in names)
        }
        if selected:
            focused[section] = selected
    if toolbox.get("requirements") is not None:
        focused["requirements"] = toolbox.get("requirements")
    return focused


def _stage07_source_evidence_bundle(
    pair_root: Path,
    *,
    workflow_review: dict[str, Any],
    hidden: dict[str, Any],
    limit: int = 80,
) -> dict[str, Any]:
    evidence_path = pair_root / "evidence_index.json"
    if not evidence_path.is_file():
        return {"status": "missing", "records": []}
    records = read_json(evidence_path)
    by_id = {
        str(row.get("evidence_id")): row
        for row in records
        if isinstance(row, dict) and row.get("evidence_id")
    }
    requested: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            singular = value.get("evidence_id")
            if singular not in (None, ""):
                requested.append(str(singular))
            plural = value.get("evidence_ids")
            if isinstance(plural, list):
                requested.extend(str(item) for item in plural if item not in (None, ""))
            for key, nested in value.items():
                if key not in {"evidence_id", "evidence_ids"}:
                    collect(nested)
        elif isinstance(value, list):
            for nested in value:
                collect(nested)

    collect(
        {
            "workflow_scope": workflow_review.get("workflow_scope") or {},
            "workflow_inventory": workflow_review.get("workflow_inventory") or [],
            "workflow_steps": workflow_review.get("workflow_steps") or [],
            "paper_route": workflow_review.get("paper_route") or {},
            "ground_truth_items": hidden.get("ground_truth_items") or [],
        }
    )
    unique = list(dict.fromkeys(requested))
    selected = []
    for evidence_id in unique[:limit]:
        row = by_id.get(evidence_id)
        if row is None:
            selected.append({"evidence_id": evidence_id, "status": "unresolved"})
            continue
        selected.append(
            {
                "evidence_id": evidence_id,
                "document_id": row.get("document_id"),
                "document_role": row.get("document_role"),
                "page": row.get("page"),
                "section_path": row.get("section_path") or [],
                "block_type": row.get("block_type"),
                "text": str(row.get("text") or "")[:4000],
                "source_ref": row.get("source_ref"),
            }
        )
    return {
        "status": "complete" if len(unique) <= limit else "truncated",
        "requested_count": len(unique),
        "included_count": len(selected),
        "records": selected,
    }


def _stage07_audit_scaffold(
    deterministic: dict[str, Any], packet: dict[str, Any]
) -> dict[str, Any]:
    outcomes = json.loads(json.dumps(deterministic.get("outcomes") or []))
    pair_audit = deterministic.get("pair_audit") or {}
    return {
        "audit_summary": "issues_found" if outcomes else "passed_audit",
        "outcomes": outcomes,
        "checks": [
            {
                "check": "deterministic_task_pair_validation",
                "status": "passed" if pair_audit.get("passed") else "failed",
                "evidence_refs": ["inputs/audit_packet.json#/deterministic_audit"],
            },
            {
                "check": "mode_input_hash_equality",
                "status": (
                    "passed"
                    if pair_audit.get("autonomous_input_hash")
                    == pair_audit.get("reproduction_input_hash")
                    else "failed"
                ),
                "evidence_refs": ["inputs/audit_packet.json#/deterministic_audit/pair_audit"],
            },
        ],
        "toolbox_assessment": {
            "status": "AGENT_REQUIRED: assess required capabilities",
            "requirements": packet.get("toolbox_requirements") or [],
        },
        "cost_assessment": {
            "status": "AGENT_REQUIRED: assess obvious feasibility",
            "resource_policy": packet.get("resource_policy") or {},
        },
        "rationale": "AGENT_REQUIRED: concise objective audit rationale",
    }


def _stage07_audit_initializer_script() -> str:
    return r'''from __future__ import annotations

import json
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "inputs" / "objective_audit_scaffold.json"
destination = root / "outputs" / "objective_audit.json"
destination.parent.mkdir(parents=True, exist_ok=True)
value = json.loads(source.read_text(encoding="utf-8"))
temporary = destination.with_suffix(".json.tmp")
temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
json.loads(temporary.read_text(encoding="utf-8"))
os.replace(temporary, destination)
print(json.dumps({
    "artifact": "outputs/objective_audit.json",
    "deterministic_outcome_count": len(value["outcomes"]),
    "fields_to_replace": ["toolbox_assessment.status", "cost_assessment.status", "rationale"],
}))
'''


def _public_audit_report(task_pair_id: str, summary: str, outcomes: list[dict[str, Any]]) -> str:
    lines = [f"# Stage07 audit: {task_pair_id}", "", f"Result: `{summary}`", ""]
    if not outcomes:
        lines.append("No objective task-integrity, toolbox, or cost issue was identified.")
    else:
        lines.append("Observed outcomes:")
        lines.append("")
        for outcome in outcomes:
            lines.append(
                f"- `{outcome.get('type')}` ({outcome.get('severity')}, "
                f"{outcome.get('scope')})"
            )
    lines.append("")
    return "\n".join(lines)


def _outcome_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        for outcome in record.get("outcomes") or []:
            name = str(outcome.get("type") or "missing")
            counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def _audit_failure(
    run_id: str,
    paper_id: str,
    task_pair_id: str,
    failure_class: str,
    message: str,
    *,
    agent_run: dict[str, Any] | None = None,
    retryable: bool = True,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
        "task_pair_id": task_pair_id,
        "processing_status": "failed",
        "decision": "objective_failure_retryable",
        "audit_decision": "objective_failure_retryable",
        "audit_summary": "objective_failure_retryable",
        "passed": False,
        "retryable": retryable,
        "failure_class": failure_class,
        "outcomes": [],
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }
