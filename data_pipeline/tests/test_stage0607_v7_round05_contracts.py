"""Round05 regression tests for hidden-contract ownership and phase boundaries.

The fixtures are intentionally chemistry-neutral.  They test only transport
ownership, mode scope, and publication behavior; no scientific target is
interpreted here.
"""

from __future__ import annotations

from pathlib import Path

from src.contracts import read_json, write_json
from src.stages.stage06_task_builder.validation import hidden_reference_transport_findings
from src.stages.stage07_task_judge.validation import stage07_mechanical_pre_publish_check


def _binding(field: str = "$.value") -> dict:
    return {
        "artifact_paths": ["report/results.json"],
        "observed_fields": [field],
        "canonical_projection": {"value": 1},
        "comparison": "numeric_tolerance",
    }


def _truth(identifier: str, profile: str, modes: list[str]) -> dict:
    return {
        "ground_truth_id": identifier,
        "acceptance_profile_id": profile,
        "acceptance_type": "numeric_tolerance",
        "canonical_answer": 1.0,
        "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
        "evidence_grade": "A",
        "claim_role": "final",
        "applies_to_modes": modes,
    }


def _profile(
    identifier: str,
    modes: list[str] | None = None,
    *,
    matrix: dict[str, dict] | None = None,
    shared: dict | None = None,
) -> dict:
    row = {
        "acceptance_profile_id": identifier,
        "type": "numeric_tolerance",
    }
    if modes is not None:
        row["applies_to_modes"] = modes
    if matrix is not None:
        row["mode_submission_bindings"] = matrix
    if shared is not None:
        row["submission_binding"] = shared
    return row


def _hidden(truths: list[dict], profiles: list[dict], *, status: str = "ready") -> dict:
    return {
        "status": status,
        "task_pair_id": "round05-pair",
        "evaluation_mode": "binary",
        "score_max": 1,
        "expected_result": {},
        "ground_truth_items": truths,
        "acceptance_profiles": profiles,
        "scientific_conclusion_rubric": [
            {
                "id": truth["ground_truth_id"],
                "statement": "A declared result is supported.",
                "acceptance_rule": "Apply the typed acceptance profile.",
                "ground_truth_ids": [truth["ground_truth_id"]],
                "acceptance_profile_ids": [truth["acceptance_profile_id"],],
                "required_evidence": ["ev-round05"],
            }
            for truth in truths
        ],
    }


def _pair(tmp_path: Path, hidden: dict) -> Path:
    pair = tmp_path / "pair"
    (pair / "hidden_reference").mkdir(parents=True)
    write_json(pair / "hidden_reference" / "ground_truth_common.json", hidden)
    for mode, task_mode, suffix in (
        ("paper_reproduction", "guided_reproduction", "_reproduction"),
        ("autonomous_research", "open_discovery", "_autonomous"),
    ):
        root = pair / mode
        (root / "data" / "inputs").mkdir(parents=True)
        (root / "data" / "inputs" / "input.xyz").write_text(
            "1\nneutral input\nH 0 0 0\n", encoding="utf-8"
        )
        (root / "task.md").write_text("Document the declared result.\n", encoding="utf-8")
        info = {
            "task_id": f"round05-pair{suffix}",
            "task_pair_id": "round05-pair",
            "source_id": "source-round05",
            "category": "computational_chemistry",
            "mode": mode,
            "scientific_mode": mode,
            "task_mode": task_mode,
        }
        write_json(root / "task_info.json", info)
        write_json(
            root / "task_spec.json",
            {
                "task_id": info["task_id"],
                "task_pair_id": info["task_pair_id"],
                "mode": mode,
                "scientific_mode": mode,
                "complexity_profile": {"level": "medium", "rationale": "fixture"},
            },
        )
        write_json(
            root / "submission_contract.json",
            {
                "required_files": ["report/results.json"],
                "results_schema": {
                    "type": "object",
                    "properties": {"value": {"type": "number"}},
                },
            },
        )
        write_json(
            root / "process_rubric.json",
            [
                {
                    "id": "process-1",
                    "criterion_type": "route_fidelity",
                    "max_score": 1,
                    "evidence_artifacts": ["report/process_trace.jsonl"],
                }
            ],
        )
    return pair


def test_stage07_requires_all_rows_for_applicable_modes(tmp_path: Path) -> None:
    truth = _truth("gt-both", "ap-both", ["paper_reproduction", "autonomous_research"])
    pair = _pair(
        tmp_path,
        _hidden(
            [truth],
            [
                _profile(
                    "ap-both",
                    ["paper_reproduction", "autonomous_research"],
                    matrix={"paper_reproduction": _binding()},
                )
            ],
        ),
    )
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert any(
        "evaluator_submission_binding_missing:autonomous_research:ap-both" in finding
        for finding in report["findings"]
    )


def test_orphan_profile_is_blocked_and_raw_contract_is_preserved(tmp_path: Path) -> None:
    truth = _truth("gt-valid", "ap-valid", ["paper_reproduction", "autonomous_research"])
    hidden = _hidden(
        [truth],
        [
            _profile(
                "ap-valid",
                ["paper_reproduction", "autonomous_research"],
                shared=_binding(),
            ),
            _profile(
                "ap-orphan",
                ["paper_reproduction", "autonomous_research"],
                shared=_binding(field="$..value"),
            ),
        ],
    )
    pair = _pair(tmp_path, hidden)
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "acceptance_profile_orphan:ap-orphan" in report["findings"]
    raw = read_json(pair / "hidden_reference" / "ground_truth_common.json")
    assert [row.get("acceptance_profile_id") for row in raw["acceptance_profiles"]] == [
        "ap-valid",
        "ap-orphan",
    ]
    assert raw["acceptance_profiles"][1]["submission_binding"]["observed_fields"] == [
        "$..value"
    ]


def test_duplicate_profile_owner_is_blocked(tmp_path: Path) -> None:
    truths = [
        _truth("gt-1", "ap-shared", ["paper_reproduction", "autonomous_research"]),
        _truth("gt-2", "ap-shared", ["paper_reproduction", "autonomous_research"]),
    ]
    pair = _pair(
        tmp_path,
        _hidden(
            truths,
            [
                _profile(
                    "ap-shared",
                    ["paper_reproduction", "autonomous_research"],
                    shared=_binding(),
                )
            ],
        ),
    )
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "acceptance_profile_not_item_specific:ap-shared" in report["findings"]


def test_shared_and_mode_matrix_binding_is_ambiguous(tmp_path: Path) -> None:
    truth = _truth("gt-ambiguous", "ap-ambiguous", ["paper_reproduction", "autonomous_research"])
    profile = _profile(
        "ap-ambiguous",
        ["paper_reproduction", "autonomous_research"],
        matrix={"paper_reproduction": _binding(), "autonomous_research": _binding()},
        shared=_binding(field="$.other"),
    )
    pair = _pair(tmp_path, _hidden([truth], [profile]))
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "acceptance_submission_binding_ambiguous:ap-ambiguous" in report["findings"]
    raw = read_json(pair / "hidden_reference" / "ground_truth_common.json")
    assert "submission_binding" in raw["acceptance_profiles"][0]
    assert "mode_submission_bindings" in raw["acceptance_profiles"][0]


def test_truth_and_profile_mode_scopes_must_agree(tmp_path: Path) -> None:
    truth = _truth("gt-scope", "ap-scope", ["paper_reproduction", "autonomous_research"])
    profile = _profile(
        "ap-scope",
        ["paper_reproduction"],
        matrix={"paper_reproduction": _binding()},
    )
    pair = _pair(tmp_path, _hidden([truth], [profile]))
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "ground_truth_profile_mode_scope_mismatch:gt-scope" in report["findings"]


def test_profile_scope_cannot_expand_beyond_owned_truth(tmp_path: Path) -> None:
    truth = _truth("gt-narrow", "ap-narrow", ["paper_reproduction"])
    profile = _profile(
        "ap-narrow",
        ["paper_reproduction", "autonomous_research"],
        matrix={
            "paper_reproduction": _binding(),
            "autonomous_research": _binding(),
        },
    )
    pair = _pair(tmp_path, _hidden([truth], [profile]))
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "ground_truth_profile_mode_scope_mismatch:gt-narrow" in report["findings"]


def test_ready_contract_requires_at_least_one_ground_truth(tmp_path: Path) -> None:
    pair = _pair(tmp_path, _hidden([], []))
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="round05-pair")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "hidden_ground_truth_empty" in report["findings"]


def test_nonready_legacy_envelope_remains_compatible() -> None:
    assert hidden_reference_transport_findings(
        {"evaluation_mode": "binary", "expected_result": {}},
        require_ready_ground_truth=True,
    ) == []
