"""Software/contract regressions, never new scientific verification results."""
from copy import deepcopy
import json
import re
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository

from scripts.audit_final_verified_tasks import (
    canonical_status, compact_success, successful_execution_payload,
    successful_artifact_evidence, successful_execution_steps, _result_scalar_leaves,
    unresolved_geometry_failure,
)

ROOT = Path(__file__).resolve().parents[1]
MODES = ("autonomous_research", "paper_reproduction")


def package(mode, paper):
    candidates = [ROOT / "tasks" / f"{stage}_verified_{mode}" / paper for stage in ("final", "hold")]
    present = [path for path in candidates if path.is_dir()]
    assert len(present) == 1, f"Expected exactly one maintained package: {candidates}"
    return present[0]


def read(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("stage", ("final", "hold"))
def test_verified_directory_alias_preserves_mode_checks(tmp_path, mode, stage):
    source = package(mode, "paper_6492e1e5d38d23ae")
    final_parent = tmp_path / f"{stage}_verified_{mode}"
    final = final_parent / source.name
    shutil.copytree(source, final)
    assert validate_task_package(final).status == "passed"
    canonical_parent = tmp_path / mode
    final_parent.rename(canonical_parent)
    assert validate_task_package(canonical_parent / source.name).status == "passed"
    opposite = "paper_reproduction" if mode == "autonomous_research" else "autonomous_research"
    wrong_parent = tmp_path / f"{stage}_verified_{opposite}"
    canonical_parent.rename(wrong_parent)
    report = validate_task_package(wrong_parent / source.name)
    assert any("task_directory_type_mismatch" in finding for finding in report.findings)


@pytest.mark.parametrize("mode", MODES)
def test_release_holds_are_separate_from_final_and_not_auto_discovered(tmp_path, mode):
    held = {"paper_6492e1e5d38d23ae", "paper_8b7bf002cc6a4ba9", "paper_b815e2622b0d6085"}
    final_root = ROOT / "tasks" / f"final_verified_{mode}"
    hold_root = ROOT / "tasks" / f"hold_verified_{mode}"
    for paper in held:
        assert (hold_root / paper).is_dir()
        assert not (final_root / paper).exists()
        assert validate_task_package(hold_root / paper).status == "passed"
    assert (final_root / "paper_84efbea3ab8e6e20").is_dir()
    assert not (hold_root / "paper_84efbea3ab8e6e20").exists()
    # A storage alias for validation must not enroll held tasks in an index.
    root = tmp_path / "tasks"
    shutil.copytree(hold_root / "paper_6492e1e5d38d23ae",
                    root / f"hold_verified_{mode}" / "paper_6492e1e5d38d23ae")
    assert TaskRepository(roots=[root]).list() == []


@pytest.mark.parametrize("state", ["cancelled", "canceled", "timeout", "running", "failed", "invalid"])
def test_failed_status_overrides_zero_wrapper_exit(state):
    assert not successful_execution_payload({"status": state, "return_code": 0})
    assert compact_success({"nested": {"status": state, "energy": 12}}) == {}
    assert canonical_status(state) != "SUCCESS_EVIDENCE_CANDIDATE"


def test_nonzero_exit_and_negative_application_evidence_override_success():
    for fields in ({"return_code": -15}, {"exit_code": "1"}, {"normal_termination": False}):
        assert not successful_execution_payload({"status": "success", **fields})


@pytest.mark.parametrize("marker", [
    "*** FAILED TO CONVERGE GEOMETRY OPTIMIZATION IN 498 ITERATIONS ***",
    "THE OPTIMIZATION DID NOT CONVERGE",
])
def test_application_geometry_failure_overrides_successful_wrapper(tmp_path, marker):
    # Synthetic log fixture, not a scientific calculation or recorded result.
    run = tmp_path / "successful_wrapper"
    run.mkdir()
    (run / "status.json").write_text(json.dumps({"status": "success", "return_code": 0}))
    (run / "stdout.log").write_text(marker + "\nnormal termination of xtb\n" + "footer\n" * 60000)
    assert unresolved_geometry_failure(run)
    assert not successful_artifact_evidence(tmp_path)
    assert not successful_execution_steps(tmp_path)


def test_later_explicit_convergence_closes_same_log_retry(tmp_path):
    run = tmp_path / "retry2"
    run.mkdir()
    (run / "status.json").write_text(json.dumps({"status": "success", "return_code": 0}))
    (run / "stdout.log").write_text(
        "FAILED TO CONVERGE GEOMETRY OPTIMIZATION\nGEOMETRY OPTIMIZATION CONVERGED AFTER 5 ITERATIONS\n")
    assert not unresolved_geometry_failure(run)
    assert len(successful_execution_steps(tmp_path)) == 1


def test_successful_retry_and_complete_arrays_are_preserved():
    record = {"states": [{"status": "success", "nested": {"a": {"b": {"c": {"energy": i}}}}}
                         for i in range(14)],
              "TS_retry2": {"status": "success", "return_code": 0, "path": "runs/TS_retry2/output.log"}}
    assert compact_success(record) == record
    assert successful_execution_payload(record["TS_retry2"])


def test_execution_inventory_does_not_drop_late_stages_or_fifth_artifact(tmp_path):
    """Synthetic file-index test only; no scientific result is fabricated."""
    for index in range(205):
        run = tmp_path / f"step_{index:03d}"
        run.mkdir()
        (run / "status.json").write_text(json.dumps({"status": "success", "return_code": 0}))
        if index == 204:
            for filename in ("a.inp", "b.log", "c.xyz", "d.csv", "e.hess", "f.out", "CONTCAR"):
                (run / filename).write_text("synthetic metadata-index fixture, not an application result")
    artifacts = successful_artifact_evidence(tmp_path)
    steps = successful_execution_steps(tmp_path)
    assert len(steps) == 205
    assert {Path(row["path"]).name for row in artifacts if row["path"].startswith("step_204/")} == {
        "status.json", "a.inp", "b.log", "c.xyz", "d.csv", "e.hess", "f.out", "CONTCAR"}


def test_result_leaf_index_retains_all_candidates_and_full_definitions():
    payload = [{"value": i, "definition": "long synthetic definition " * 25} for i in range(250)]
    rows = _result_scalar_leaves(payload, prefix="$.states")
    assert len(rows) == 500
    assert rows[-1] == {"path": "$.states[249].definition", "value": payload[-1]["definition"]}


@pytest.mark.parametrize("mode", MODES)
def test_08c_keeps_paths_but_does_not_demand_full_mep(mode):
    p = package(mode, "paper_08c040bf4e456891")
    task = (p / "agent_input/task.md").read_text()
    assert "Full multidimensional minimum-energy-path proof is not required" in task
    rules = read(p / "evaluation/scoring_rules.json")["rules"]
    assert sorted(r["target"] for r in rules if r["type"] == "numeric") == [11.9, 12.4, 13.5]
    assert "Correct energies alone do not pass path validation" in json.dumps(rules)


@pytest.mark.parametrize("mode", MODES)
def test_5286_public_protocol_has_no_ordering_answer(mode):
    p = package(mode, "paper_5286f393dfa5a49a")
    task = (p / "agent_input/task.md").read_text()
    assert "wB97M-V/def2-TZVP" in task and "SMD dichloromethane" in task
    assert "6.56" not in task
    assert "You may select an implicit solvent" not in task
    assert "optional, separate sensitivity" in task
    assert "-6.56" in (p / "evaluation/scoring_rules.json").read_text()


@pytest.mark.parametrize("mode", MODES)
def test_84ef_lifetime_is_evaluator_private_and_state_character_stays_required(mode):
    p = package(mode, "paper_84efbea3ab8e6e20")
    s = read(p / "agent_input/submission_schema.json")
    s = s.get("result_schema", s)
    c = s["properties"]["conclusion"]
    assert "computed_comparison" in c["required"]
    assert "lifetime_comparison" not in c["required"]
    assert "state_character" in s["properties"]["molecules"]["items"]["oneOf"][0]["required"]
    task = (p / "agent_input/task.md").read_text()
    assert "Experimental lifetimes and their ordering are not supplied" in task
    assert all(v not in task for v in ("3.96", "4.27", "5.20"))
    assert "Do not require the agent" in (p / "evaluation/scoring_rules.json").read_text()


def software_only_conformer_result():
    """Synthetic schema fixture; not stored in group results or a reference."""
    return {
        "status": "complete", "method": {"software": "fixture", "description": "software test",
                                            "temperature_K": 298.15, "phase": "gas"},
        "initial_attempts": [{"initial_id": f"1-{i}", "endpoint_ids": [f"end-{i}"], "outcome": "done"}
                             for i in (1, 2, 3)],
        "conformers": [{"id": f"end-{i}", "status": "success", "initial_ids": [f"1-{i}"],
                        "minimum_validation": {"passed": True, "evidence": "synthetic"},
                        "endpoint_evidence": {"geometry_file": "synthetic.xyz", "atom_mapping": "synthetic",
                                              "distinguishing_features": "synthetic"},
                        "relative_gibbs_kcal_mol": i - 1, "population_percent": 100 / 3}
                       for i in (1, 2, 3)],
        "normalization": {"scope": "synthetic three-member set", "formula": "test only",
                          "population_sum_percent": 100},
        "most_populated_conformer": "end-1", "conclusion": "software only", "limitations": "not chemistry",
    }


@pytest.mark.parametrize("mode", MODES)
def test_9d_complete_and_merged_partial_branches(mode):
    p = package(mode, "paper_9d091f4337662e78")
    schema = read(p / "agent_input/submission_schema.json")["result_schema"]
    v = Draft202012Validator(schema)
    complete = software_only_conformer_result()
    v.validate(complete)
    swapped = deepcopy(complete); swapped["conformers"].reverse(); v.validate(swapped)
    merged = deepcopy(complete); merged["conformers"].pop()
    assert list(v.iter_errors(merged))
    merged["status"] = "partial"; merged["most_populated_conformer"] = None
    merged["normalization"]["population_sum_percent"] = None
    for row in merged["conformers"]: row["population_percent"] = None
    merged["initial_attempts"][2]["endpoint_ids"] = ["end-2"]
    merged["conformers"][1]["initial_ids"].append("1-3")
    v.validate(merged)
    # Schema checks shape/count only; scientific deduplication is an explicit
    # evaluator duty, not falsely certified by this synthetic fixture.
    rules = read(p / "evaluation/scoring_rules.json")["rules"]
    energy_rules = [r for r in rules if r["type"] == "numeric"]
    assert sorted(r["target"] for r in energy_rules) == [0, 0.6804861, 0.771969325]
    assert all("never from energy proximity" in r["expected"] for r in energy_rules)


@pytest.mark.parametrize("mode", MODES)
def test_6492_signed_convention_is_public_but_target_and_tolerance_stay_fixed(mode):
    p = package(mode, "paper_6492e1e5d38d23ae")
    task = (p / "agent_input/task.md").read_text()
    convention = "W(rutile TiO2(110)) - W(anatase TiO2(101))"
    assert convention in task
    schema = read(p / "agent_input/submission_schema.json")["result_schema"]
    assert convention in schema["properties"]["comparison"]["properties"]["difference_eV"]["description"]
    numeric = [r for r in read(p / "evaluation/scoring_rules.json")["rules"] if r["type"] == "numeric"]
    assert sorted((r["target"], r["tolerance"]) for r in numeric) == [(6.871, 0.5), (7.009, 0.5)]
    a, r = 6.36999978845305, 7.189349995247433
    assert r - a == pytest.approx(0.8193502067943825)
    assert abs(a - 6.871) > 0.5
    reference = (p / "evaluation/verified_computation_reference.md").read_text()
    assert "+0.8193502067943825" in reference
    assert "D1 remains open" in reference


@pytest.mark.parametrize("mode", MODES)
def test_8b7_archive_uses_printed_debye_and_rejects_unconverged_precursors(mode):
    g = ROOT / "docs/verification/group_5/paper_8b7bf002cc6a4ba9"
    reference = (package(mode, g.name) / "evaluation/verified_computation_reference.md").read_text()
    assert "full conformer-stability/dipole conclusion is not established" in reference
    for candidate in read(g / "report/validation.json")["candidates"]:
        raw = (ROOT / candidate["orca"]["output"]).read_text()
        debye = float(re.findall(r"Magnitude \(Debye\)\s*:\s*([-\d.]+)", raw)[-1])
        assert f"{debye:.9f}" in reference
        xtb_dir = g / "native_workspace/outputs/execution_jobs" / candidate["xtb_job"]
        assert unresolved_geometry_failure(xtb_dir)
    assert "not paper targets or validated conformer rankings" in reference


@pytest.mark.parametrize("mode", MODES)
def test_84ef_archive_keeps_real_triplet_evidence_without_claiming_author_hlct(mode):
    p = package(mode, "paper_84efbea3ab8e6e20")
    reference = (p / "evaluation/verified_computation_reference.md").read_text()
    assert "specific CZ2B/T4 HLCT interpretation is not established" in reference
    assert "clearly evidenced alternative" in reference
    assert "T1" in reference and "T4-HLCT" in reference
    data = read(ROOT / "docs/verification/group_6" / p.name /
                "provenance/spin_resolved_nto_reconstruction_20260915/analysis.json")
    for row in data["records"]:
        for triplet in row["triplets"]:
            assert triplet["multiplicity"] == 3
            for kind in ("hole_population", "particle_population"):
                assert f'{triplet[kind]["Bpin"]["state_weighted_Loewdin"]:.9f}' in reference
    assert '"current_recovery"' not in reference


def test_no_failed_execution_object_in_archived_successful_chain():
    def check(value):
        if isinstance(value, dict):
            assert value.get("status") not in {"cancelled", "canceled", "running", "queued", "failed", "timeout"}
            assert value.get("return_code", 0) in (None, 0, "0")
            for child in value.values():
                check(child)
        elif isinstance(value, list):
            for child in value:
                check(child)
    for mode in MODES:
        for stage in ("final", "hold"):
            for path in (ROOT / "tasks" / f"{stage}_verified_{mode}").glob("paper_*/evaluation/verified_computation_reference.md"):
                match = re.search(r"## Successful calculation chain\n.*?```json\n(.*?)\n```", path.read_text(), re.S)
                if match:
                    check(json.loads(match[1]))
