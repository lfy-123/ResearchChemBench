#!/usr/bin/env python3
"""Submission-format regression tests; synthetic report variants, no chemistry jobs.

Run with the project's .envs/researchchembench/bin/python. Temporary submissions
exercise the same format validator used by the runner. Passing here is not a
scientific score; the real calculation witnesses are unchanged private inputs.
"""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[2]
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
import jsonschema
from chemistry_toolbox.src.output_contract import validate_output_contract


class SubmissionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract_bytes = (PACKAGE / "agent_input/submission_schema.json").read_bytes()
        cls.schema = json.loads(cls.contract_bytes)["result_schema"]
        jsonschema.validators.validator_for(cls.schema).check_schema(cls.schema)
        cls.witnesses = [json.loads((PACKAGE / "evaluation/task_provenance" / name).read_text())
                         for name in ("cif_7a_20260920_reprocessed.json", "si_conformer_20260920_reprocessed.json")]

    def witness(self):
        return copy.deepcopy(self.witnesses[0])

    def validate(self, document, expected=True):
        schema_errors = list(jsonschema.validators.validator_for(self.schema)(self.schema).iter_errors(document))
        self.assertEqual(not schema_errors, expected,
                         "\n".join(str(e) for e in schema_errors[:3]))
        # These are disposable local fixtures, never production run artifacts.
        with tempfile.TemporaryDirectory(prefix="a396_submission_test_") as directory:
            workspace = Path(directory)
            report = workspace / "report"
            report.mkdir()
            (report / "results.json").write_text(json.dumps(document, allow_nan=False))
            result = validate_output_contract(workspace, self.contract_bytes)
            self.assertEqual(result["valid"], expected, result)
        return document

    def partial(self, count=1, selected=True):
        doc = self.witness()
        doc["status"] = "bounded_failure"
        doc["failure_reason"] = "Synthetic test: required primary work is unavailable; no replacement result is invented."
        doc["models"] = doc["models"][:count]
        names = {m["name"] for m in doc["models"]}
        for field in ("observables", "metrics", "inversion_comparison"):
            doc[field] = [r for r in doc[field] if r["model"] in names]
        if not count:
            doc["mapping"] = None
        if not selected:
            doc["comparison"]["model_pair"] = []
        doc["comparison"]["per_kind"] = [
            {"kind": kind, "mae_preference": "unresolved", "rmse_preference": "unresolved"}
            for kind in ("bond", "angle", "torsion")]
        doc["comparison"]["overall"] = "unresolved_incomplete"
        doc["comparison"]["interpretation"] = "No complete primary-pair comparison is available."
        doc["conclusion"] = "Only genuine partial results are supplied; the task is not complete."
        return doc

    def test_01_existing_uniform_witness_still_valid(self):
        self.validate(copy.deepcopy(self.witnesses[0]))

    def test_02_existing_mixed_witness_still_valid(self):
        self.validate(copy.deepcopy(self.witnesses[1]))

    def test_03_complete_plus_failed_supplementary_attempt(self):
        doc = self.witness()
        doc["attempts"] = [{"model": "extra_start", "role": "supplementary", "status": "failed",
                            "reason": "Synthetic format test: no result was obtained.", "artifacts": []}]
        self.validate(doc)
        for key in ("models", "observables", "metrics", "comparison", "conclusion"):
            self.assertEqual(doc[key], self.witnesses[0][key])

    def test_04_complete_plus_failed_primary_retry(self):
        doc = self.witness()
        doc["attempts"] = [{"model": doc["models"][0]["name"], "role": "primary", "status": "failed",
                            "reason": "Synthetic earlier attempt; the later successful result is in models."}]
        self.validate(doc)

    def test_05_completed_supplementary_result_is_separate(self):
        doc = self.witness()
        other = self.witnesses[1]["models"][0]
        doc["attempts"] = [{"model": "alternate_" + other["name"], "role": "supplementary",
                            "status": "completed", "artifacts": other["calculation_artifacts"]}]
        self.validate(doc)

    def test_06_not_started_attempt_needs_no_nonexistent_file(self):
        doc = self.witness()
        doc["attempts"] = [{"model": "optional_extra_model", "role": "supplementary",
                            "status": "not_started", "reason": "Synthetic optional run not launched."}]
        self.validate(doc)

    def test_07_one_real_primary_result_can_be_reported(self):
        doc = self.partial(1)
        self.assertEqual(len(doc["observables"]), 47)
        self.validate(doc)

    def test_08_zero_results_with_known_primary_pair(self):
        doc = self.partial(0)
        doc["attempts"] = [{"model": name, "role": "primary", "status": "not_started",
                            "reason": "Synthetic startup failure before geometry generation."}
                           for name in doc["comparison"]["model_pair"]]
        self.validate(doc)

    def test_09_zero_results_before_model_selection(self):
        self.validate(self.partial(0, selected=False))

    def test_10_zero_results_with_failure_row_explanations(self):
        doc = self.partial(0)
        doc["observables"] = [{"model": doc["comparison"]["model_pair"][0], "selector": "Cl1-C14",
                               "kind": "bond", "unit": "Angstrom", "failure": "No calculated coordinates."}]
        self.validate(doc)

    def test_11_incomplete_torsion_set_preserves_null_metric(self):
        doc = self.partial(2)
        model = doc["models"][0]["name"]
        missing = next(r for r in doc["observables"] if r["model"] == model and r["kind"] == "torsion")
        doc["observables"].remove(missing)
        metric = next(r for r in doc["metrics"] if r["model"] == model and r["observable_kind"] == "torsion")
        metric.update(mae=None, rmse=None, n_rows=10)
        inv = next(r for r in doc["inversion_comparison"] if r["model"] == model)
        inv.update(selected_reference_sign=None, branches=[])
        self.validate(doc)

    def test_12_missing_partial_failure_reason_rejected(self):
        doc = self.partial()
        del doc["failure_reason"]
        self.validate(doc, False)

    def test_13_partial_cannot_claim_complete_overall_comparison(self):
        doc = self.partial()
        doc["comparison"]["overall"] = "mixed"
        self.validate(doc, False)

    def test_14_one_primary_model_cannot_be_complete(self):
        doc = self.partial()
        doc["status"] = "complete"
        self.validate(doc, False)

    def test_15_zero_primary_models_cannot_be_complete(self):
        doc = self.partial(0)
        doc["status"] = "complete"
        self.validate(doc, False)

    def test_16_failed_primary_endpoint_cannot_be_complete(self):
        doc = self.witness()
        doc["models"][0].update(converged=False, stationary=False)
        self.validate(doc, False)

    def test_17_complete_result_requires_mapping(self):
        doc = self.witness()
        doc["mapping"] = None
        self.validate(doc, False)

    def test_18_partial_model_also_requires_mapping(self):
        doc = self.partial()
        doc["mapping"] = None
        self.validate(doc, False)

    def test_19_numerical_observable_requires_mapping(self):
        doc = self.partial(0)
        doc["observables"] = [copy.deepcopy(self.witnesses[0]["observables"][0])]
        self.validate(doc, False)

    def test_20_failed_attempt_requires_reason(self):
        doc = self.witness()
        doc["attempts"] = [{"model": "extra", "role": "supplementary", "status": "failed"}]
        self.validate(doc, False)

    def test_21_completed_attempt_requires_real_artifact_reference(self):
        doc = self.witness()
        doc["attempts"] = [{"model": "extra", "role": "supplementary", "status": "completed", "artifacts": []}]
        self.validate(doc, False)

    def test_22_extra_results_must_not_mix_into_primary_models(self):
        doc = self.witness()
        extra = copy.deepcopy(doc["models"][0])
        extra["name"] = "supplementary_model"
        doc["models"].append(extra)
        self.validate(doc, False)

    def test_23_missing_geometry_still_rejects_complete(self):
        doc = self.witness()
        doc["observables"].pop()
        self.validate(doc, False)

    def test_24_missing_metric_still_rejects_complete(self):
        doc = self.witness()
        doc["metrics"].pop()
        self.validate(doc, False)

    def test_25_incomplete_metric_cannot_be_complete(self):
        doc = self.witness()
        doc["metrics"][0]["mae"] = None
        self.validate(doc, False)

    def test_26_complete_still_requires_two_primary_names(self):
        doc = self.witness()
        doc["comparison"]["model_pair"] = doc["comparison"]["model_pair"][:1]
        self.validate(doc, False)

    def test_27_complete_still_requires_inversion_evidence(self):
        doc = self.witness()
        del doc["inversion_comparison"]
        self.validate(doc, False)

    def test_28_primary_model_requires_raw_artifacts(self):
        doc = self.witness()
        doc["models"][0]["calculation_artifacts"] = []
        self.validate(doc, False)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SubmissionContractTests)
    names = [test.id().rsplit(".", 1)[-1] for test in suite]
    transcript = io.StringIO()
    result = unittest.TextTestRunner(stream=transcript, verbosity=2).run(suite)
    print(json.dumps({"mode": PACKAGE.parent.name, "tests_run": result.testsRun,
                      "passed": result.wasSuccessful(), "cases": names,
                      "transcript": transcript.getvalue(),
                      "scope": "Synthetic submission-format regression through JSON Schema and the shared runner validator; no new quantum calculation, LLM judge or scientific scoring."},
                     ensure_ascii=False, indent=2))
    sys.exit(0 if result.wasSuccessful() else 1)
