"""A bounded, science-preserving Stage07B contract repair Agent.

Stage07B is intentionally small. It is not a second scientific judge and it is not a fallback
constructor. It can run only after a scientific approval and only for explicitly allowlisted
transport findings. Any science-content change invalidates the candidate and leaves Stage07 in a
visible technical-blocked state.
"""

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from pathlib import Path
from typing import Any

import jsonschema

from src.agents import AgentRunRequest, create_agent_harness
from src.agents.schemas import STRING, STRING_ARRAY, object_schema
from src.agents.workspace import (
    atomic_commit_tree,
    copytree_exact,
    directory_manifest,
    make_read_only,
    make_writable,
    prepare_clean_directory,
    write_manifest,
)
from src.contracts import read_json, safe_component, write_json
from .prompts import STAGE07B_REPAIR_VERSION, contract_repair_instructions

_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))
from researchchembench_contracts import normalize_binding_contract  # noqa: E402


STAGE07B_REPAIR_SCHEMA = object_schema(
    ["status", "changed_files", "findings_before", "findings_after", "summary"],
    {
        "status": {"enum": ["repaired", "unresolved", "rejected_scope"]},
        "changed_files": STRING_ARRAY,
        "findings_before": STRING_ARRAY,
        "findings_after": STRING_ARRAY,
        "science_hash_before": STRING,
        "science_hash_after": STRING,
        "summary": STRING,
        "repair_origin": STRING,
        "agent_run": {"type": "object", "additionalProperties": True},
    },
)


# This is a deliberately closed list. Unknown findings stay blocked for a future
# Stage07A decision instead of being handed to a repair Agent with too much power.
_TECHNICAL_PREFIXES = (
    "evaluator_acceptance_profile_contract_invalid:",
    "evaluator_submission_binding_",
    "evaluator_binding_",
    "evaluator_artifact_path_",
    "evaluator_result_schema_",
    # The v1 package validator reports an explicit structured binding that
    # walks through an otherwise open object schema with this prefix.  It is
    # still a transport-only finding: the field is already named by the
    # audited binding; Stage07B may only make that declaration explicit.
    "binding_schema_path_open:",
    "evaluator_document_binding_",
    "evaluator_binding_path_",
    "acceptance_submission_binding_ambiguous:",
    "submission_required_files_",
    "submission_results_schema_",
    "unsafe_required_path:",
    "mode_pair_submission_contract_shape_diff",
    "mode_contract_mismatch:",
    "task_mode_contract_mismatch:",
    "task_id_suffix_mismatch:",
    "task_spec_mode_mismatch:",
    "unreadable_mode_json:",
    "public_allowlist_",
    "manifest_",
    "normalization_",
    "submission_contract_",
)

# A malformed selector has no deterministic transport repair: changing it can
# change which scientific result is scored.  Keep it out of Stage07B so the
# scientific audit (or a future explicit mapping repair) remains the owner.
_UNSUPPORTED_TECHNICAL_PREFIXES = (
    "evaluator_binding_path_invalid:",
    "evaluator_binding_filter_invalid:",
)


# Contract files are the only files Stage07B may change. Science files remain
# in the fingerprint even if an Agent attempts to touch them.
_MUTABLE_CONTRACT_NAMES = {
    "task_info.json",
    "submission_contract.json",
    "public_manifest.json",
    "task_pair_manifest.json",
    "audit_manifest.json",
    "published_manifest.json",
    "orchestrator_normalizations.json",
    "stage07b_repair.json",
}

_HIDDEN_BINDING_KEYS = {
    "submission_binding",
    "mode_submission_bindings",
    "submission_bindings_by_mode",
    "canonical_projection",
}


def classify_technical_findings(findings: list[str] | None) -> dict[str, Any]:
    values = [str(item).strip() for item in findings or [] if str(item).strip()]
    allowed = [
        item
        for item in values
        if any(item.startswith(prefix) for prefix in _TECHNICAL_PREFIXES)
        and not any(item.startswith(prefix) for prefix in _UNSUPPORTED_TECHNICAL_PREFIXES)
    ]
    unsupported = [item for item in values if item not in allowed]
    return {
        "eligible": bool(values) and not unsupported,
        "allowed": sorted(set(allowed)),
        "unsupported": sorted(set(unsupported)),
    }


def _safe_ambiguous_binding_findings(
    audited_root: Path, findings: list[str]
) -> tuple[list[str], list[str]]:
    """Allow shared-binding cleanup only when a complete equivalent mode matrix exists."""

    ambiguous = [
        value
        for value in findings
        if value.startswith("acceptance_submission_binding_ambiguous:")
    ]
    if not ambiguous:
        return [], []
    try:
        hidden = read_json(
            audited_root / "hidden_reference" / "ground_truth_common.json"
        )
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return [], ambiguous
    profiles = {
        str(row.get("acceptance_profile_id") or row.get("profile_id") or ""): row
        for row in hidden.get("acceptance_profiles") or []
        if isinstance(row, dict)
    }
    allowed: list[str] = []
    unsupported: list[str] = []
    mode_aliases = {
        "paper_reproduction": "paper_reproduction",
        "guided_reproduction": "paper_reproduction",
        "reproduction": "paper_reproduction",
        "autonomous_research": "autonomous_research",
        "open_discovery": "autonomous_research",
        "autonomous": "autonomous_research",
    }

    def canonical_binding(value: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
        normalized = normalize_binding_contract(value, profile=profile)
        # Remove only serialization aliases already projected onto canonical
        # fields by normalize_binding_contract.  Unknown keys stay in the
        # equality comparison, making the safety test conservative.
        for key in (
            "artifact_path",
            "artifact",
            "artifacts",
            "field",
            "fields",
            "result_field",
            "result_fields",
            "json_path",
            "json_paths",
            "projection",
            "comparison_type",
            "document_target",
        ):
            normalized.pop(key, None)
        return normalized

    for finding in ambiguous:
        profile_id = finding.split(":", 1)[1]
        profile = profiles.get(profile_id)
        matrix = profile.get("mode_submission_bindings") if profile else None
        scope = profile.get("applies_to_modes") if profile else None
        normalized_matrix = {
            mode_aliases.get(str(mode), str(mode)): binding
            for mode, binding in (matrix.items() if isinstance(matrix, dict) else [])
        }
        applicable = (
            {
                mode_aliases.get(str(mode), str(mode))
                for mode in scope
            }
            if isinstance(scope, list)
            else {"paper_reproduction", "autonomous_research"}
        )
        shared = profile.get("submission_binding") if profile else None
        shared_canonical = (
            canonical_binding(shared, profile)
            if isinstance(shared, dict) and isinstance(profile, dict)
            else None
        )
        matrix_canonical = {
            mode: canonical_binding(binding, profile)
            for mode, binding in normalized_matrix.items()
            if isinstance(binding, dict) and isinstance(profile, dict)
        }
        if (
            profile
            and shared_canonical
            and applicable.issubset(matrix_canonical)
            and all(
                matrix_canonical.get(mode) == shared_canonical
                for mode in applicable
            )
        ):
            allowed.append(finding)
        else:
            unsupported.append(finding)
    return allowed, unsupported


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def science_fingerprint(pair_root: str | Path) -> str:
    """Hash every non-contract artifact so Stage07B cannot alter science silently."""

    root = Path(pair_root).expanduser().resolve()
    records: list[tuple[str, str, int]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if _contract_path_allowed(relative):
            # Task metadata contains a few transport aliases that the
            # orchestrator may normalize (task id, mode aliases, schema
            # version). Preserve the scientific/task identity fields in the
            # freeze while allowing only those aliases to move.
            if relative == "hidden_reference/ground_truth_common.json":
                try:
                    value = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError, json.JSONDecodeError):
                    content = path.read_bytes()
                else:
                    if isinstance(value, dict):
                        # Binding paths/comparison/projection are transport
                        # contract fields. Keep answers, tolerances, propositions,
                        # evidence IDs, and mode scope in the frozen payload.
                        normalized = json.loads(json.dumps(value, ensure_ascii=False))
                        normalized.pop("task_pair_id", None)
                        # ``applies_to_modes`` is a set-valued contract.  Transport
                        # normalization may canonicalize its serialization order;
                        # freeze membership while avoiding a false science change
                        # caused only by list ordering.
                        for collection_name in (
                            "ground_truth_items",
                            "acceptance_profiles",
                        ):
                            for row in normalized.get(collection_name, []) or []:
                                if isinstance(row, dict) and isinstance(
                                    row.get("applies_to_modes"), list
                                ):
                                    row["applies_to_modes"] = sorted(
                                        row["applies_to_modes"], key=str
                                    )
                        for profile in normalized.get("acceptance_profiles", []) or []:
                            if isinstance(profile, dict):
                                # Binding paths and legacy container spellings are
                                # transport metadata, but canonical projections can
                                # contain answer-bearing values/propositions. Freeze
                                # the unique projection values independently of
                                # whether an equivalent shared binding or mode matrix
                                # carries them, then remove the mutable containers.
                                projections: list[str] = []

                                def collect_projections(node: Any) -> None:
                                    if isinstance(node, dict):
                                        if "canonical_projection" in node:
                                            projections.append(
                                                json.dumps(
                                                    node["canonical_projection"],
                                                    ensure_ascii=False,
                                                    sort_keys=True,
                                                    separators=(",", ":"),
                                                )
                                            )
                                        for nested_key, nested in node.items():
                                            if nested_key != "canonical_projection":
                                                collect_projections(nested)
                                    elif isinstance(node, list):
                                        for nested in node:
                                            collect_projections(nested)

                                for key in _HIDDEN_BINDING_KEYS:
                                    if key in profile:
                                        collect_projections({key: profile[key]})
                                if projections:
                                    profile["_binding_canonical_projections"] = sorted(
                                        set(projections)
                                    )
                                for key in _HIDDEN_BINDING_KEYS:
                                    profile.pop(key, None)
                        content = json.dumps(
                            normalized,
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                        ).encode("utf-8")
                    else:
                        content = path.read_bytes()
            elif path.name == "task_info.json":
                try:
                    value = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError, json.JSONDecodeError):
                    content = path.read_bytes()
                else:
                    if isinstance(value, dict):
                        semantic = {
                            key: item
                            for key, item in value.items()
                            if key
                            not in {
                                "task_id",
                                "task_pair_id",
                                "task_mode",
                                "scientific_mode",
                                "method_disclosure",
                                "pathway_disclosure",
                                "schema_version",
                            }
                        }
                        content = json.dumps(
                            semantic,
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                        ).encode("utf-8")
                    else:
                        content = path.read_bytes()
            else:
                continue
        elif relative.endswith("/stage07_audit.json") or relative in {
            "stage07_audit.json",
            "mechanical_pre_publish_report.json",
        }:
            continue
        else:
            content = path.read_bytes()
        records.append((relative, _hash_bytes(content), len(content)))
    encoded = json.dumps(records, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return _hash_bytes(encoded)


def _changed_files(before: Path, after: Path) -> list[str]:
    before_manifest = {
        item["path"]: item
        for item in directory_manifest(before).get("files", [])
    }
    after_manifest = {
        item["path"]: item
        for item in directory_manifest(after).get("files", [])
    }
    values = []
    for path in sorted(set(before_manifest) | set(after_manifest)):
        if before_manifest.get(path) != after_manifest.get(path):
            values.append(path)
    return values


def _contract_path_allowed(relative: str) -> bool:
    path = Path(relative)
    if relative == "hidden_reference/ground_truth_common.json":
        return True
    if path.parts and path.parts[0] in {"paper_reproduction", "autonomous_research"}:
        return path.name in _MUTABLE_CONTRACT_NAMES
    return path.name in {
        "task_pair_manifest.json",
        "audit_manifest.json",
        "published_manifest.json",
        "orchestrator_normalizations.json",
        "stage07b_repair.json",
    }


def _receipt(response: dict[str, Any], *, before: list[str], before_hash: str) -> dict[str, Any]:
    value = dict(response or {})
    value.setdefault("status", "unresolved")
    value.setdefault("changed_files", [])
    value.setdefault("findings_before", before)
    value.setdefault("findings_after", [])
    value.setdefault("science_hash_before", before_hash)
    value.setdefault("science_hash_after", "")
    value.setdefault("summary", "")
    return value


def run_stage07b_repair(
    *,
    harness,
    stage_root: Path,
    paper_id: str,
    task_pair_id: str,
    audited_root: Path,
    findings: list[str],
    config: dict[str, Any],
) -> dict[str, Any]:
    classification = classify_technical_findings(findings)
    safe_ambiguous, unsafe_ambiguous = _safe_ambiguous_binding_findings(
        audited_root, findings
    )
    ambiguous_values = {
        value
        for value in findings
        if value.startswith("acceptance_submission_binding_ambiguous:")
    }
    classification["allowed"] = sorted(
        (set(classification["allowed"]) - ambiguous_values) | set(safe_ambiguous)
    )
    if unsafe_ambiguous:
        classification["allowed"] = sorted(
            set(classification["allowed"]) - set(unsafe_ambiguous)
        )
        classification["unsupported"] = sorted(
            set(classification["unsupported"]) | set(unsafe_ambiguous)
        )
    classification["eligible"] = bool(classification["allowed"]) and not bool(
        classification["unsupported"]
    )
    before_hash = science_fingerprint(audited_root)
    base_report: dict[str, Any] = {
        "schema_version": "stage07b-contract-repair/v1",
        "implementation_version": STAGE07B_REPAIR_VERSION,
        "paper_id": paper_id,
        "task_pair_id": task_pair_id,
        "status": "not_run",
        "findings_before": classification["allowed"],
        "unsupported_findings": classification["unsupported"],
        "science_hash_before": before_hash,
        "science_hash_after": before_hash,
    }
    if not classification["eligible"]:
        base_report["status"] = "not_eligible"
        base_report["reason"] = (
            "Unsupported or scientifically ambiguous findings require Stage07A review."
            if classification["unsupported"]
            else "No allowlisted technical findings were present."
        )
        return base_report
    if not bool(config.get("stage07b_enabled", True)):
        base_report["status"] = "disabled"
        return base_report

    attempt = uuid.uuid4().hex[:8]
    root = prepare_clean_directory(
        stage_root / "workspaces" / safe_component(paper_id) / "stage07b" / f"attempt-{attempt}"
    )
    inputs = root / "inputs"
    outputs = root / "outputs"
    inputs.mkdir(parents=True, exist_ok=True)
    outputs.mkdir(parents=True, exist_ok=True)
    copytree_exact(audited_root, outputs / "task_pair")
    write_json(inputs / "mechanical_findings.json", classification)
    write_json(
        inputs / "repair_contract.json",
        {
            "paper_id": paper_id,
            "task_pair_id": task_pair_id,
            "science_hash_before": before_hash,
            "allowed_files": sorted(_MUTABLE_CONTRACT_NAMES),
        },
    )
    write_json(inputs / "stage07_audit.json", read_json(audited_root / "stage07_audit.json") if (audited_root / "stage07_audit.json").is_file() else {})
    make_read_only(inputs)
    make_writable(outputs)
    max_tool_calls = max(4, int(config.get("stage07b_max_tool_calls", 40)))
    request = AgentRunRequest(
        phase="stage07b_contract_repair",
        record_id=task_pair_id,
        workspace=root,
        instructions=contract_repair_instructions(
            paper_id=paper_id,
            task_pair_id=task_pair_id,
            findings=classification["allowed"],
            science_hash=before_hash,
            max_tool_calls=max_tool_calls,
        ),
        output_schema=STAGE07B_REPAIR_SCHEMA,
        prompt_version=STAGE07B_REPAIR_VERSION,
        timeout_seconds=int(config.get("stage07b_timeout_seconds", 1800)),
        metadata={
            "paper_id": paper_id,
            "task_pair_id": task_pair_id,
            "stage07b": True,
            "max_tool_calls": max_tool_calls,
            "inline_contract": True,
            "structured_artifact_path": "outputs/stage07b_repair.json",
        },
    )
    try:
        result = harness.run(request)
        response = _receipt(result.response or {}, before=classification["allowed"], before_hash=before_hash)
        jsonschema.validate(response, STAGE07B_REPAIR_SCHEMA)
    except Exception as exc:
        base_report.update(
            {
                "status": "agent_failure",
                "reason": f"{type(exc).__name__}: {exc}",
                "agent_run": result.audit_record() if "result" in locals() else {},
            }
        )
        return base_report

    candidate = outputs / "task_pair"
    # Stage07B may write an accepted legacy alias.  Apply the same explicit,
    # provenance-recorded transport projection used before the final Gate;
    # any resulting change outside Stage07B's allowlist is still rejected by
    # the changed-file and science-fingerprint checks below.
    from src.stages.stage07_task_judge.validation import (
        normalize_stage07_transport_contract,
        stage07_mechanical_pre_publish_check,
    )

    normalization = normalize_stage07_transport_contract(
        candidate, task_pair_id=task_pair_id
    )
    after_hash = science_fingerprint(candidate)
    changed = _changed_files(audited_root, candidate)
    illegal = [path for path in changed if not _contract_path_allowed(path)]
    status = str(response.get("status") or "unresolved")
    report = {
        **base_report,
        "status": status,
        "changed_files": changed,
        "illegal_changed_files": illegal,
        "science_hash_after": after_hash,
        "agent_response": response,
        "agent_run": result.audit_record(),
        "orchestrator_normalization": normalization,
    }
    if after_hash != before_hash:
        report["status"] = "technical_blocked"
        report["reason"] = "science_fingerprint_changed"
        return report
    if illegal:
        report["status"] = "technical_blocked"
        report["reason"] = "stage07b_changed_non_contract_files"
        return report
    if status != "repaired":
        report["status"] = "unresolved"
        report["reason"] = response.get("summary") or "Stage07B did not repair all findings."
        return report

    mechanical = stage07_mechanical_pre_publish_check(
        candidate, task_pair_id=task_pair_id
    )
    report["mechanical_after"] = mechanical
    if mechanical.get("mechanical_pre_publish_status") != "passed":
        report["status"] = "technical_blocked"
        report["reason"] = "mechanical_findings_remain"
        return report

    atomic_commit_tree(candidate, audited_root)
    report["status"] = "repaired"
    report["committed"] = True
    write_json(audited_root / "stage07b_repair.json", report)
    write_manifest(audited_root, audited_root / "audit_manifest.json")
    return report


__all__ = [
    "STAGE07B_REPAIR_SCHEMA",
    "classify_technical_findings",
    "run_stage07b_repair",
    "science_fingerprint",
]
