from __future__ import annotations

import json
from pathlib import Path

from chemistry_toolbox.scripts.run_action_backend_matrix_smokes import all_cases
from researchchem_toolbox.catalog import action_specs
from researchchem_toolbox.paths import CONFIG_ROOT, DOCS_ROOT


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_matrix_checkpoint_contains_every_registered_gap_case():
    expected = {(case.action, case.backend) for case in all_cases()}
    payload = _json(CONFIG_ROOT / "action_backend_matrix_smoke_status.json")
    observed = {(item["action"], item["backend"]) for item in payload["cases"]}
    assert len(expected) == 65
    assert observed == expected
    assert payload["summary"]["observed_pair_count"] == len(expected)
    assert payload["summary"]["missing_pair_count"] == 0


def test_combined_coverage_partitions_the_complete_catalog():
    payload = _json(CONFIG_ROOT / "action_test_coverage.json")
    successful = {tuple(pair) for pair in payload["successful_action_backend_pairs"]}
    failed = {tuple(pair) for pair in payload["failed_action_backend_pairs"]}
    catalog = {
        (action.id, backend_id)
        for action in action_specs().values()
        for backend_id in action.backend_ids
    }
    assert len(catalog) == 246
    assert successful.isdisjoint(failed)
    assert successful | failed == catalog
    assert payload["unobserved_action_backend_pairs"] == []


def test_completion_report_lists_every_action_and_backend():
    report = (DOCS_ROOT / "ACTION_BACKEND_COMPLETE_AUDIT_20260721.md").read_text(
        encoding="utf-8"
    )
    for action in action_specs().values():
        assert f"`{action.id}`" in report
        for backend_id in action.backend_ids:
            assert f"`{backend_id}`" in report
