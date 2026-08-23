from __future__ import annotations

import json
from pathlib import Path

from researchchembench_contracts import (
    COMPUTATIONAL_REFERENCE_SCHEMA_V1,
    PACKAGE_MANIFEST_SCHEMA_V1,
    SUBMISSION_SCHEMA_V1,
    TASK_INFO_SCHEMA_V1,
    TASK_PACKAGE_SCHEMA_V1,
    package_content_hash,
    package_payload_entries,
    validate_task_package,
)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _package(tmp_path: Path, *, task_id: str = "fixture_reproduction") -> Path:
    root = tmp_path / task_id
    (root / "data" / "inputs").mkdir(parents=True)
    (root / "evaluation").mkdir()
    (root / "task.md").write_text("# Run the declared workflow\n", encoding="utf-8")
    (root / "data" / "inputs" / "structure.xyz").write_text(
        "1\nfixture\nH 0 0 0\n", encoding="utf-8"
    )
    _write_json(
        root / "task_info.json",
        {
            "schema_version": TASK_INFO_SCHEMA_V1,
            "task_id": task_id,
            "task_family_id": "fixture_family",
            "task_type": "paper_reproduction",
            "source_id": "source_fixture",
            "title": "Fixture reproduction",
            "category": "test",
            "tags": [],
            "runtime_readiness": "ready",
            "required_capabilities": [],
            "data": [
                {
                    "name": "Input structure",
                    "path": "data/inputs/structure.xyz",
                    "type": "chemical/x-xyz",
                    "description": "Synthetic contract fixture.",
                }
            ],
            "required_deliverables": [
                {
                    "path": "report/results.json",
                    "description": "Structured results.",
                    "allow_empty": False,
                },
                {
                    "path": "report/report.md",
                    "description": "Scientific report.",
                    "allow_empty": False,
                },
            ],
            "related_task_ids": [],
            "reference_schema": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
        },
    )
    _write_json(
        root / "submission_schema.json",
        {
            "schema_version": SUBMISSION_SCHEMA_V1,
            "task_id": task_id,
            "required_files": ["report/results.json", "report/report.md"],
            "primary_result_file": "report/results.json",
            "result_schema": {
                "type": "object",
                "properties": {"value": {"type": "number"}},
                "required": ["value"],
                "additionalProperties": True,
            },
            "allowed_extra_fields": True,
        },
    )
    _write_json(
        root / "evaluation" / "reference.json",
        {
            "schema_version": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
            "task_id": task_id,
            "task_type": "paper_reproduction",
            "answer_items": [
                {
                    "answer_id": "answer_value",
                    "kind": "numeric_final_result",
                    "canonical_answer": 1.5,
                    "claim_role": "final",
                    "evidence_grade": "A",
                    "evidence_ids": ["evidence_fixture"],
                    "metadata": {},
                }
            ],
            "acceptance_profiles": [
                {
                    "acceptance_profile_id": "profile_value",
                    "answer_id": "answer_value",
                    "acceptance_type": "numeric_tolerance",
                    "parameters": {"absolute_tolerance": 0.1, "unit": "arb"},
                    "required_propositions": [],
                    "forbidden_contradictions": [],
                    "description": "Fixture tolerance.",
                }
            ],
            "submission_bindings": [
                {
                    "binding_id": "binding_value",
                    "acceptance_profile_id": "profile_value",
                    "artifact_paths": ["report/results.json"],
                    "observed_fields": ["$.value"],
                    "comparison": "numeric_tolerance",
                    "document_binding": False,
                }
            ],
            "process_key_points": [
                {
                    "key_point_id": "execute",
                    "title": "Execute",
                    "description": "Perform the declared calculation.",
                    "evidence_requirements": ["report/results.json"],
                    "metadata": {},
                }
            ],
            "final_conclusions": [
                {
                    "conclusion_id": "conclusion_value",
                    "statement": "Report the resulting value.",
                    "answer_ids": ["answer_value"],
                    "acceptance_profile_ids": ["profile_value"],
                    "required_evidence": ["report/results.json"],
                    "metadata": {},
                }
            ],
            "critical_failures": [],
            "private_evidence": {},
            "evaluation_constraints": {},
        },
    )
    entries = package_payload_entries(root)
    _write_json(
        root / "package_manifest.json",
        {
            "schema_version": PACKAGE_MANIFEST_SCHEMA_V1,
            "package_schema": TASK_PACKAGE_SCHEMA_V1,
            "task_id": task_id,
            "task_family_id": "fixture_family",
            "task_type": "paper_reproduction",
            "reference_schema": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
            "assembler_version": "fixture-v1",
            "package_content_sha256": package_content_hash(entries),
            "entries": [entry.model_dump(mode="json") for entry in entries],
            "public_to_agent": ["task.md", "submission_schema.json", "data/**"],
            "manifest_self_excluded": True,
        },
    )
    return root


def test_task_package_v1_round_trip(tmp_path: Path):
    root = _package(tmp_path)
    report = validate_task_package(root)
    assert report.status == "passed", report.findings
    assert report.task_id == root.name
    assert report.task_type == "paper_reproduction"


def test_task_package_v1_rejects_unlisted_build_record(tmp_path: Path):
    root = _package(tmp_path)
    (root / "stage07_audit.json").write_text("{}\n", encoding="utf-8")
    report = validate_task_package(root)
    assert report.status == "failed"
    assert "unexpected_top_level_entry:stage07_audit.json" in report.findings


def test_task_package_v1_rejects_private_agent_allowlist(tmp_path: Path):
    root = _package(tmp_path)
    manifest_path = root / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["public_to_agent"].append("evaluation/reference.json")
    _write_json(manifest_path, manifest)
    report = validate_task_package(root)
    assert report.status == "failed"
    assert "private_entry_publicly_allowlisted:evaluation/reference.json" in report.findings


def test_task_package_v1_rejects_duplicate_answer_projection(tmp_path: Path):
    root = _package(tmp_path)
    reference_path = root / "evaluation" / "reference.json"
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference["acceptance_profiles"][0]["target"] = 1.5
    _write_json(reference_path, reference)
    report = validate_task_package(root)
    assert report.status == "failed"
    assert any("computational_reference_invalid" in item for item in report.findings)


def test_task_package_v1_requires_explicit_structured_binding_schema(tmp_path: Path):
    root = _package(tmp_path)
    schema_path = root / "submission_schema.json"
    submission = json.loads(schema_path.read_text(encoding="utf-8"))
    submission["result_schema"] = {
        "type": "object",
        "required": ["value"],
        "additionalProperties": True,
    }
    _write_json(schema_path, submission)
    entries = package_payload_entries(root)
    manifest_path = root / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["entries"] = [entry.model_dump(mode="json") for entry in entries]
    manifest["package_content_sha256"] = package_content_hash(entries)
    _write_json(manifest_path, manifest)
    report = validate_task_package(root)
    assert report.status == "failed"
    assert any("binding_schema_path_open" in item for item in report.findings)
