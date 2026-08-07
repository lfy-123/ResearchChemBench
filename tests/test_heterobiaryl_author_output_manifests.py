from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_author_output_manifests_have_complete_pairings() -> None:
    manifests = list(
        PROJECT_ROOT.glob(
            "tasks/*Reproduction*/data/benchmark_data/author_output_file_roles.json"
        )
    )
    assert manifests
    for path in manifests:
        recorded = json.loads(path.read_text(encoding="utf-8"))
        assert recorded["schema_version"] == 2
        assert recorded["summary"]["unclassified_file_count"] == 0
        assert recorded["summary"]["pairing_count"] > 0
        assert recorded["summary"]["complete_pairing_count"] == recorded["summary"][
            "pairing_count"
        ]
        assert all(pairing["complete"] for pairing in recorded["pairings"])
        assert recorded["result_values_included"] is False


def test_file_level_manifest_does_not_include_scientific_results() -> None:
    forbidden = {"energy", "barrier", "ranking", "score", "conclusion"}
    for path in PROJECT_ROOT.glob(
        "tasks/*/data/benchmark_data/author_output_file_roles.json"
    ):
        value = json.loads(path.read_text(encoding="utf-8"))
        for record in value["files"]:
            assert not forbidden & set(record)
        for pairing in value["pairings"]:
            assert not forbidden & set(pairing)


def test_autonomous_tasks_do_not_receive_author_file_role_mapping() -> None:
    for path in PROJECT_ROOT.glob(
        "tasks/Heterobiaryl_PV_[0-9]*/data/benchmark_data/author_output_manifest.json"
    ):
        value = json.loads(path.read_text(encoding="utf-8"))
        assert "files" not in value
        assert "pairings" not in value
        assert not path.with_name("author_output_file_roles.json").exists()
