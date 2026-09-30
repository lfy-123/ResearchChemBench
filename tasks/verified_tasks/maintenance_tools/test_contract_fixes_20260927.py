"""Offline regression for two authorized instruction/evaluator repairs.

Synthetic examples test submission contracts only. No new scientific results,
QM/HPC/model calls or modifications of historical evidence are performed.
Run from the repository root with its researchchembench Python environment.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import jsonschema
from chemistry_toolbox.src.output_contract import validate_output_contract
from evaluation.repository import TaskRepository
from evaluation.scoring.adapters import load_runtime_evaluation
from evaluation.scoring.rules import check_rule

BASELINE = "5dd1e1b8ea1f7efa1a4029834e4a7188ade8d0e8"
ROOT = Path("tasks/verified_tasks")
passed = 0
failures = []
rows = []


def check(condition, label, detail=None):
    global passed
    if condition:
        passed += 1
    else:
        failures.append({"test": label, "detail": detail})


def prior(path):
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"])


def test_cases(package, actual, cases):
    contract = (package / "agent_input/submission_schema.json").read_bytes()
    schema = json.loads(contract)["result_schema"]
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    check(True, str(package) + " valid schema")
    with tempfile.TemporaryDirectory(prefix="rcb-contract-20260927-") as tmp:
        workspace = Path(tmp)
        (workspace / "report").mkdir()
        (workspace / "report/README.md").write_text(
            "SYNTHETIC contract regression only; not scientific verification.\n"
        )
        for label, result, expected in cases:
            errors = list(validator.iter_errors(result))
            check((not errors) == expected, f"{package} schema {label}",
                  [e.message[:180] for e in errors])
            (workspace / "report/results.json").write_text(json.dumps(result))
            observed = validate_output_contract(workspace, contract)
            check(observed["valid"] == expected, f"{package} runner {label}",
                  observed["errors"][:2])
    for path in (package / "agent_input/data").rglob("*"):
        if path.is_file():
            check(path.read_bytes() == prior(path), f"{path} scientific input unchanged")
    rules_path = package / "evaluation/scoring_rules.json"
    old_rules = json.loads(prior(rules_path))["rules"]
    new_rules = json.loads(rules_path.read_text())["rules"]
    def numbers(rules):
        return {r["rule_id"]: (r.get("target"), r.get("tolerance"), r.get("unit"))
                for r in rules if r.get("type") == "numeric"}
    check(numbers(old_rules) == numbers(new_rules), str(package) + " numeric gold unchanged")
    for name, key in [("reference_key_points.json", "key_point_id"),
                      ("reference_conclusions.json", "conclusion_id")]:
        path = package / "evaluation" / name
        check([i[key] for i in json.loads(prior(path))["items"]] ==
              [i[key] for i in json.loads(path.read_text())["items"]],
              str(package) + " same scientific IDs " + name)
    runtime = load_runtime_evaluation(paper_id=package.name,
                                     task_type=package.parent.name,
                                     repository=TaskRepository(roots=[ROOT]))
    check(runtime.policy_id == "dual_axis_100.scientific_results.v1",
          str(package) + " same scientific scoring policy")
    rows.append({"package": str(package), "contract_cases": len(cases)})
    return runtime.ground_truth["rule_table"]


for mode in ("autonomous_research", "paper_reproduction"):
    p = ROOT / mode / "paper_d83e607f125440cc"
    real = json.loads(Path("docs/verification/group_1/paper_d83e607f125440cc/report/results.json").read_text())
    if mode == "autonomous_research":
        real["investigation"] = {
            "plan": "SYNTHETIC format-only wrapper, not a historical AR trajectory.",
            "models_or_conformers": ["SYNTHETIC format-only field"],
            "coverage": "Existing scientific result; AR exploration was not recorded."
        }
    cases = [("historical frequencies (AR wrapper synthetic)", real, True)]
    frequency = deepcopy(real)
    frequency["minimum_validation"]["validation_method"] = "frequency"
    cases.append(("explicit frequency branch", frequency, True))
    equivalent = deepcopy(real)
    equivalent["minimum_validation"] = {
        "validation_method": "equivalent",
        "validation_statement": "SYNTHETIC branch-format example; not scientific evidence.",
        "equivalent_evidence": ["SYNTHETIC/gradient-and-full-internal-curvature.txt"]
    }
    cases.append(("equivalent without invented frequency count", equivalent, True))
    old = jsonschema.Draft202012Validator(json.loads(prior(p / "agent_input/submission_schema.json"))["result_schema"])
    check(not old.is_valid(equivalent), str(p) + " original equivalent-branch conflict reproduced")
    for label, field, value in [
        ("empty evidence", "equivalent_evidence", []),
        ("blank evidence entry", "equivalent_evidence", [""]),
        ("unsupported method", "validation_method", "declaration_only"),
        ("blank validation statement", "validation_statement", "")
    ]:
        x = deepcopy(equivalent)
        x["minimum_validation"][field] = value
        cases.append((label, x, False))
    for field in ("equivalent_evidence", "validation_method", "validation_statement"):
        x = deepcopy(equivalent)
        del x["minimum_validation"][field]
        cases.append(("missing equivalent " + field, x, False))
    for value in (-1, 0.5):
        x = deepcopy(frequency)
        x["minimum_validation"]["imaginary_frequencies"] = value
        cases.append(("invalid frequency count " + str(value), x, False))
    x = deepcopy(frequency)
    del x["minimum_validation"]["imaginary_frequencies"]
    cases.append(("frequency branch missing count", x, False))
    x = deepcopy(frequency)
    x["minimum_validation"]["imaginary_frequencies"] = 1
    cases.append(("truthful nonminimum count is format-valid, not scientific success", x, True))
    cases.append(("early failure does not invent minimum evidence", {
        "status": "bounded_failure", "failure_stage": "before optimization",
        "diagnostics": "SYNTHETIC unsuccessful attempt", "partial_results": {},
        "investigation_scope": "No successful calculation", "conclusion": "unresolved"
    }, True))
    table = test_cases(p, real, cases)
    minimum = next(r["rule"] for r in table if r["rule_id"] == "r_minimum")
    check("$.minimum_validation" in minimum["binding"]["fields"], str(p) + " rule sees both validation branches")
    check("equivalent" in minimum["expected"] and "optimization convergence alone" in minimum["expected"].lower(),
          str(p) + " evidence required, optimization alone insufficient")
    task = (p / "agent_input/task.md").read_text()
    check(("The AR investigation" in task) == (mode == "autonomous_research"),
          str(p) + " AR-only sentence correctly scoped")

p = ROOT / "paper_reproduction/paper_1a47bc00fd63b2f5"
real = json.loads(Path("docs/verification/group_3/paper_1a47bc00fd63b2f5/report/results.json").read_text())
cases = [("unchanged historical composite calculation", real, True)]
x = deepcopy(real)
x["system"]["method"] = {}
cases.append(("completed with undeclared method", x, False))
old = jsonschema.Draft202012Validator(json.loads(prior(p / "agent_input/submission_schema.json"))["result_schema"])
check(old.is_valid(x), str(p) + " original empty-method acceptance reproduced")
for field in ("optimization", "single_point", "solvent", "temperature_K", "pressure_atm", "energy_convention"):
    x = deepcopy(real)
    del x["system"]["method"][field]
    cases.append(("missing primary protocol " + field, x, False))
for field, value in (("optimization", ""), ("temperature_K", 0), ("pressure_atm", -1)):
    x = deepcopy(real)
    x["system"]["method"][field] = value
    cases.append(("invalid protocol field " + field, x, False))
x = deepcopy(real)
x["supplementary_calculations"] = [{"method": "SYNTHETIC SI Table S5 BLYP control",
    "signed_delta_delta_g_kcal_mol": 5.19, "role": "format example, not a new calculation"}]
cases.append(("separate optional control outside main numeric interval", x, True))
x = deepcopy(real)
x.update(status="bounded_failure", candidates=[],
         coverage={"conformer_generation": "failed before construction", "deduplication": "none"},
         conclusion={"claim": "unresolved"},
         barrier_comparison={"availability": "not_available", "reason": "SYNTHETIC failure"},
         failure_report={"failed_channels": ["ortho_4_hydroxybenzofuran", "para_6_hydroxybenzofuran"],
                         "attempted_candidate_ids": [], "reason": "SYNTHETIC early failure"})
x["system"]["method"] = {}
cases.append(("early failure permits unavailable method details", x, True))
x = deepcopy(real)
x["system"]["method"]["optimization"] = "SYNTHETIC different model; semantic scientific review must reject"
cases.append(("schema is not a chemistry-method validator", x, True))
table = test_cases(p, real, cases)
delta = next(r for r in table if r["rule_id"] == "r_delta")
check(set(delta["rule"]["binding"]["fields"]) == {
    "$.barrier_comparison.signed_delta_delta_g_kcal_mol", "$.system.method", "$.candidates"},
    str(p) + " numeric rule includes method and candidate evidence")
check("Actual inputs/outputs" in delta["rule"]["expected"] and
      "optional controls" in delta["rule"]["expected"], str(p) + " semantic method/evidence check explicit")
check(check_rule(delta, {"report/results.json": real})["assessment"] == "requires_semantic_review",
      str(p) + " conditional science not certified by scalar-only checker")
computed = real["barrier_comparison"]["para_barrier_kcal_mol"] - real["barrier_comparison"]["ortho_barrier_kcal_mol"]
check(abs(computed - real["barrier_comparison"]["signed_delta_delta_g_kcal_mol"]) < 1e-9 and
      abs(computed - 7.6) <= 1.5, str(p) + " unchanged real delta arithmetic")
check(all(abs(v - 7.6) > 1.5 for v in (5.95, 5.19, 5.62)),
      str(p) + " SI alternate-method counterexamples explain protocol distinction")

print(json.dumps({"passed": passed, "failed": len(failures), "failures": failures,
                  "packages": rows,
                  "scope": "Offline contract/runner/scoring-binding regression only; no new QM or LLM judge."},
                 indent=2, ensure_ascii=False))
raise SystemExit(bool(failures))
