"""Regression checks for the two confirmed evaluator-data repairs."""
from __future__ import annotations

import json
from pathlib import Path

from chemistry_toolbox.src.recovery_io import control_directory
from evaluation.repository import TaskRepository, materialize_agent_files


ROOT = Path(__file__).resolve().parents[1]


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_0a62_identity_correction_follows_atom_composition_and_preserves_paths():
    package = ROOT / "tasks/final_verified_autonomous_research/paper_0a62b797f51de2c0"
    correction = _read(package / "evaluation/identity_correction.json")
    identity_expected = next(
        item["expected"]
        for item in _read(package / "evaluation/reference_key_points.json")["items"]
        if item["key_point_id"] == "ar_process_identity"
    )
    # The tracked package contains the corrected verification excerpt; local
    # docs and calculation archives are not required in a fresh checkout.
    reference = (package / "evaluation/verified_computation_reference.md").read_text(encoding="utf-8")
    result = json.loads(reference.split("```json\n", 1)[1].split("\n```", 1)[0])
    rows = {row["id"]: row for row in result["molecules"]}
    identities = {row["source_label"]: row["chemical_identity"] for row in correction["mapping"]}
    assert correction["status"] == "confirmed"
    assert all(identities[row["source_label"]] == row["id"] for row in rows.values())
    assert "public chemical identities" in identity_expected
    assert "historical source labels" not in identity_expected
    assert rows["M-Th-1CN"]["structure"]["smiles"] == "s1c(Br)c(C#N)cc1Br"
    assert rows["M-Th-2CN"]["structure"]["smiles"] == "s1c(Br)c(C#N)c(C#N)c1Br"
    assert rows["M-Th-1CN"]["structure"]["file"].endswith("M-Th-2CN_xtbopt.xyz")
    assert rows["M-Th-2CN"]["structure"]["file"].endswith("M-Th-1CN_xtbopt.xyz")
    assert result["comparison"]["dipole_ordering"] == ["M-Th-0CN", "M-Th-1CN", "M-Th-2CN"]
    assert result["comparison"]["author_route_dipole_totals_debye"] == [1.1744, 3.3867, 6.0547]


def test_c625_mk_route_is_reference_only_in_active_contract():
    package = ROOT / "tasks/final_verified_autonomous_research/paper_c625cba3ce868eb1"
    task = (package / "agent_input/task.md").read_text(encoding="utf-8")
    rule = next(r for r in _read(package / "evaluation/scoring_rules.json")["rules"] if r["rule_id"] == "ar_r5")
    conclusion = _read(package / "evaluation/reference_conclusions.json")["items"][0]["expected"]
    assert "Choose software, model chemistry, solvation model, charge partition" in task
    assert "MK is an admissible charge partition, not a mandatory one" in rule["expected"]
    assert "both (1)" in rule["expected"] and "(2)" in rule["expected"]
    assert "or equivalent electronic-density descriptor" not in rule["expected"]
    assert "method-specific charge model mandatory" in conclusion
    assert "does not require the MK partition" in (package / "evaluation/verified_computation_reference.md").read_text(encoding="utf-8")


def test_recovery_scoring_selects_frozen_snapshot_before_current_repository(tmp_path):
    """A finalized recoverable run must remain tied to its captured contract."""
    from evaluation.scoring.service import _prepare
    from test_task_package_v19 import package, refresh_manifest

    workspace = tmp_path / "run"
    control = control_directory(workspace, "run")
    frozen_root = control / "task_snapshot"
    frozen = package(frozen_root)
    current_root = tmp_path / "current_repository"
    current = package(current_root)
    current_rules = _read(current / "evaluation/scoring_rules.json")
    current_rules["rules"][0]["target"] = 99.9
    (current / "evaluation/scoring_rules.json").write_text(
        json.dumps(current_rules, indent=2) + "\n", encoding="utf-8"
    )
    refresh_manifest(current)
    repository = TaskRepository([frozen_root])
    materialize_agent_files(
        paper_id="paper_fixture",
        task_type="autonomous_research",
        destination=workspace,
        repository=repository,
    )
    (workspace / "report").mkdir(parents=True, exist_ok=True)
    (workspace / "report/report.md").write_text("saved report", encoding="utf-8")
    (workspace / "report/results.json").write_text(
        json.dumps({"barrier": 12.3, "conclusion": "path A"}), encoding="utf-8"
    )
    manifest = _read(frozen / "package_manifest.json")
    meta = {
        "run_id": "run",
        "paper_id": "paper_fixture",
        "task_type": "autonomous_research",
        "status": "completed",
        "recovery_enabled": True,
        "task_package_content_sha256": manifest["package_content_sha256"],
    }
    (workspace / "_meta.json").write_text(json.dumps(meta), encoding="utf-8")
    prepared = _prepare(workspace, meta, None, None, None, 250000)
    assert prepared["rules_source"] == "original_run_frozen_rules"
    assert prepared["task_package_content_sha256"] == manifest["package_content_sha256"]
    assert prepared["truth"]["rule_table"][0]["rule"]["target"] == 12.3

    # A different current repository must not silently replace the frozen
    # contract.  An explicit rules_root remains the opt-in path for a new
    # versioned re-score.
    prepared_explicit = _prepare(workspace, meta, current_root, None, None, 250000)
    assert prepared_explicit["rules_source"] == "explicit_rules"
    assert prepared_explicit["truth"]["rule_table"][0]["rule"]["target"] == 99.9
