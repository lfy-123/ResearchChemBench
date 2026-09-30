#!/usr/bin/env python3
"""Read-only recheck of this task's approved repair; no quantum jobs or file writes.

Run from any cwd. Requires numpy, RDKit, jsonschema. Prints a private JSON archive.
The witnesses replay already completed source-informed calculations, not blind
agent submissions. Tests check local arithmetic/schema, not external judge scores.
"""
import copy
import csv
import json
import re
from collections import Counter
from pathlib import Path

import jsonschema
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, rdDetermineBonds, rdMolTransforms

PACKAGE = Path(__file__).resolve().parents[2]
REPO = Path(__file__).resolve().parents[5]
INPUT = PACKAGE / "agent_input/data/inputs"
SOURCE = REPO / "docs/verification/group_2/paper_a3968806251093cd/provenance/cif_hold_acceptance_20260921"
KINDS = ("bond", "angle", "torsion")
COUNTS = {"bond": 13, "angle": 23, "torsion": 11}
TOL = {"bond": 1e-6, "angle": 1e-4, "torsion": 1e-4}
ATOM_MAP = json.loads((INPUT / "atom_map.json").read_text())
LABELS = {k: v - 1 for k, v in ATOM_MAP["label_to_atom_map_number"].items()}
ROWS = list(csv.DictReader((INPUT / "experimental_geometry.csv").open()))
SCHEMA = json.loads((PACKAGE / "agent_input/submission_schema.json").read_text())["result_schema"]
IDENTITY = Chem.MolFromSmiles(json.loads((INPUT / "molecule.json").read_text())["smiles"])


def xyz(path):
    lines = Path(path).read_text().splitlines()
    n = int(lines[0])
    data = [line.split() for line in lines[2:2 + n]]
    assert len(data) == n == 46
    return [line[0] for line in data], np.array([[float(v) for v in line[1:4]] for line in data])


def measure(coords, kind, indices):
    assert len(set(indices)) == len(indices), "Degenerate selector / invalid mapping"
    p = coords[indices]
    if kind == "bond":
        return float(np.linalg.norm(p[1] - p[0]))
    if kind == "angle":
        v, w = p[0] - p[1], p[2] - p[1]
        assert np.linalg.norm(v) > 1e-12 and np.linalg.norm(w) > 1e-12
        return float(np.degrees(np.arccos(np.clip(np.dot(v, w) / np.linalg.norm(v) / np.linalg.norm(w), -1, 1))))
    u = p[2] - p[1]
    assert np.linalg.norm(u) > 1e-12
    u /= np.linalg.norm(u)
    v, w = p[0] - p[1], p[3] - p[2]
    v, w = v - np.dot(v, u) * u, w - np.dot(w, u) * u
    assert np.linalg.norm(v) > 1e-12 and np.linalg.norm(w) > 1e-12
    return float(np.degrees(np.arctan2(np.dot(np.cross(u, v), w), np.dot(v, w))))


def circular(a, b):
    return np.abs((np.asarray(a) - np.asarray(b) + 180) % 360 - 180)


def invert_stats(values, refs):
    branches = []
    for sign in (1, -1):
        err = circular(values, sign * np.array(refs))
        branches.append({"reference_sign": sign, "sse_degree2": float(err @ err),
                         "mae_degree": float(err.mean()), "rmse_degree": float(np.sqrt(np.mean(err ** 2)))})
    first, second = branches
    if abs(first["sse_degree2"] - second["sse_degree2"]) > 1e-8:
        chosen = min(branches, key=lambda b: b["sse_degree2"])
    elif abs(first["mae_degree"] - second["mae_degree"]) > 1e-8:
        chosen = min(branches, key=lambda b: b["mae_degree"])
    else:
        chosen = first
    return chosen, branches


def extract(coords, name, labels=LABELS):
    obs, metrics, inversion = [], [], None
    for kind in KINDS:
        rows = [r for r in ROWS if r["kind"] == kind]
        assert len(rows) == len({r["selector"] for r in rows}) == COUNTS[kind]
        assert {r["selector"] for r in rows} == set(ATOM_MAP[kind + "_rows"])
        values = [measure(coords, kind, [labels[k] for k in r["selector"].split("-")]) for r in rows]
        refs = [float(r["experimental_value"]) for r in rows]
        if kind == "torsion":
            chosen, branches = invert_stats(values, refs)
            errors = circular(values, chosen["reference_sign"] * np.array(refs))
            inversion = {"model": name, "selected_reference_sign": chosen["reference_sign"], "branches": branches}
        else:
            errors = np.abs(np.array(values) - refs)
        obs += [{"model": name, "kind": kind, "selector": r["selector"], "value": value,
                 "unit": r["unit"], "reference_comparison": "Public SCXRD observations; protocol a396_geometry_comparison_v2."}
                for r, value in zip(rows, values)]
        metrics.append({"model": name, "observable_kind": kind, "mae": float(errors.mean()),
                        "rmse": float(np.sqrt(np.mean(errors ** 2))), "n_rows": len(rows),
                        "unit": rows[0]["unit"], "torsion_error_convention":
                        "global reference sign chosen on all 11 rows, circular differences" if kind == "torsion" else "not applicable"})
    return obs, metrics, inversion


def comparison(metrics, pair):
    table = {(m["model"], m["observable_kind"]): m for m in metrics}
    kinds, all_votes = [], []
    for kind in KINDS:
        row = {"kind": kind}
        for field in ("mae", "rmse"):
            a, b = [table[(name, kind)][field] for name in pair]
            vote = "tie" if abs(a - b) <= TOL[kind] else "first" if a < b else "second"
            row[field + "_preference"] = vote
            all_votes.append(vote)
        kinds.append(row)
    votes = set(all_votes) - {"tie"}
    overall = ("indistinguishable_on_reported_metrics" if not votes else
               "mixed" if len(votes) == 2 else next(iter(votes)) + "_uniformly_no_worse")
    return {"model_pair": pair, "per_kind": kinds, "overall": overall,
            "interpretation": "Comparison of the actual computed conformers; not a universal functional ranking."}


def raw_audit(model):
    text = (REPO / model["stdout"]).read_text()
    elements, coords = xyz(REPO / model["coordinates"])
    assert Counter(elements) == {"C": 20, "H": 17, "N": 6, "O": 1, "S": 1, "Cl": 1}
    orientations = re.findall(r"(?:Standard|Input) orientation:\s*\n\s*-+\n.*?\n.*?\n\s*-+\n(.*?)\n\s*-+", text, re.S)
    last = np.array([[float(v) for v in line.split()[3:6]] for line in orientations[-1].splitlines()])
    assert np.max(np.abs(last - coords)) <= 1e-9
    atomic_numbers = [int(line.split()[1]) for line in orientations[-1].splitlines()]
    assert [Chem.GetPeriodicTable().GetElementSymbol(z) for z in atomic_numbers] == elements
    freqs = [float(v) for line in re.findall(r"Frequencies --([^\n]+)", text) for v in line.split()]
    assert len(freqs) == 132 and min(freqs) > 0
    assert text.count("Normal termination") == 2 and "Error termination" not in text
    assert "Optimization completed" in text
    assert set(re.findall(r"Charge\s*=\s*(-?\d+)\s+Multiplicity\s*=\s*(\d+)", text)) == {("0", "1")}
    inp = (REPO / model["directory"] / "input.com").read_text()
    assert model["route"] in inp
    start_lines = inp.split("\n0 1\n", 1)[1].strip().splitlines()[:46]
    start = np.array([[float(v) for v in line.split()[1:4]] for line in start_lines])
    mol = Chem.MolFromXYZBlock((REPO / model["coordinates"]).read_text())
    rdDetermineBonds.DetermineConnectivity(mol)
    expected_edges = {frozenset((b.GetBeginAtom().GetAtomMapNum() - 1, b.GetEndAtom().GetAtomMapNum() - 1))
                      for b in IDENTITY.GetBonds()}
    actual_edges = {frozenset((b.GetBeginAtomIdx(), b.GetEndAtomIdx())) for b in mol.GetBonds()
                    if b.GetBeginAtom().GetSymbol() != "H" and b.GetEndAtom().GetSymbol() != "H"}
    assert expected_edges == actual_edges
    for atom in IDENTITY.GetAtoms():
        actual = mol.GetAtomWithIdx(atom.GetAtomMapNum() - 1)
        assert actual.GetSymbol() == atom.GetSymbol()
        assert sum(n.GetSymbol() == "H" for n in actual.GetNeighbors()) == atom.GetTotalNumHs()
    e = measure(coords, "torsion", [LABELS[k] for k in ("C8", "C17", "N3", "N4")])
    assert abs(e) > 90
    independent_delta = []
    funcs = {"bond": rdMolTransforms.GetBondLength, "angle": rdMolTransforms.GetAngleDeg,
             "torsion": rdMolTransforms.GetDihedralDeg}
    for row in ROWS:
        indices = [LABELS[k] for k in row["selector"].split("-")]
        ours = measure(coords, row["kind"], indices)
        theirs = funcs[row["kind"]](mol.GetConformer(), *indices)
        independent_delta.append(float(circular(ours, theirs)) if row["kind"] == "torsion" else abs(ours - theirs))
    assert max(independent_delta) < 1e-8
    result = {"model": model["model"], "source_log": model["stdout"], "source_coordinates": model["coordinates"],
              "coordinates_equal_final_log_orientation": True, "mapped_graph_and_hydrogens_match": True,
              "charge": 0, "multiplicity": 1, "E_imine_torsion_degree": e,
              "normal_terminations": 2, "optimization_completed": True,
              "positive_frequencies": len(freqs), "minimum_frequency_cm1": min(freqs),
              "numpy_rdkit_max_difference": max(independent_delta)}
    return coords, start, result


def check_complete(witness, coordinate_table):
    """Local numeric/coverage check only; raw log authenticity is checked separately."""
    jsonschema.validate(witness, SCHEMA)
    assert witness["status"] == "complete"
    names = [m["name"] for m in witness["models"]]
    assert len(set(names)) == len(names)
    assert set(witness["comparison"]["model_pair"]).issubset(names)
    assert len(witness["observables"]) == 47 * len(names)
    assert len(witness["metrics"]) == 3 * len(names)
    assert len(witness["inversion_comparison"]) == len(names)
    all_metrics = []
    for name in names:
        base = witness["mapping"]["coordinate_index_base"]
        mapping = witness["mapping"].get("model_label_to_atom", {}).get(name, witness["mapping"]["label_to_atom"])
        labels = {k: v - base for k, v in mapping.items()}
        assert labels["Cl1"] == labels["Cl2"]
        expected, metrics, inv = extract(coordinate_table[name], name, labels)
        supplied = [r for r in witness["observables"] if r["model"] == name]
        assert len({(r["kind"], r["selector"]) for r in supplied}) == 47
        tab = {(r["kind"], r["selector"]): r for r in supplied}
        for row in expected:
            actual = tab[(row["kind"], row["selector"])]
            assert row["unit"] == actual["unit"]
            delta = circular(row["value"], actual["value"]) if row["kind"] == "torsion" else abs(row["value"] - actual["value"])
            assert delta <= TOL[row["kind"]]
        actual_metrics = [r for r in witness["metrics"] if r["model"] == name]
        assert len({r["observable_kind"] for r in actual_metrics}) == 3
        for exp in metrics:
            act = next(r for r in actual_metrics if r["observable_kind"] == exp["observable_kind"])
            assert act["n_rows"] == exp["n_rows"]
            for field in ("mae", "rmse"):
                assert abs(act[field] - exp[field]) <= TOL[exp["observable_kind"]]
        actual_inv = next(r for r in witness["inversion_comparison"] if r["model"] == name)
        assert actual_inv["selected_reference_sign"] == inv["selected_reference_sign"]
        assert {r["reference_sign"] for r in actual_inv["branches"]} == {1, -1}
        for branch in inv["branches"]:
            act = next(r for r in actual_inv["branches"] if r["reference_sign"] == branch["reference_sign"])
            for field in ("sse_degree2", "mae_degree", "rmse_degree"):
                assert abs(act[field] - branch[field]) < 1e-5
        all_metrics += metrics
    expected = comparison(all_metrics, witness["comparison"]["model_pair"])
    assert witness["comparison"]["per_kind"] == expected["per_kind"]
    assert witness["comparison"]["overall"] == expected["overall"]


def main():
    tests, branches_out, witnesses = [], [], {}
    identity3d = Chem.AddHs(IDENTITY)
    assert AllChem.EmbedMolecule(identity3d, randomSeed=396) == 0
    idx = {a.GetAtomMapNum(): a.GetIdx() for a in IDENTITY.GetAtoms()}
    assert str(IDENTITY.GetBondBetweenAtoms(idx[17], idx[23]).GetStereo()) == "STEREOE"
    assert abs(rdMolTransforms.GetDihedralDeg(identity3d.GetConformer(), *[idx[i] for i in (8, 17, 23, 24)])) > 90
    tests.append("Public mapped graph generates 46-atom E-imine 3D independently; no quantum calculation performed.")
    for filename in ("PRIMARY_CIF_RESULTS.json", "SECONDARY_SI_RESULTS.json"):
        source = json.loads((SOURCE / filename).read_text())
        models, coords_table, starts, audits, obs, metrics, inversions = [], {}, [], [], [], [], []
        for model in source["models"]:
            name = model["model"]
            coords, start, audit = raw_audit(model)
            coords_table[name] = coords
            starts.append(start)
            audits.append(audit)
            rows, stats, inversion = extract(coords, name)
            old_rows = [r for r in source["observations"] if r["model"] == name]
            for row in rows:
                old = next(r for r in old_rows if r["selector"] == row["selector"] and r["kind"] == row["kind"])
                assert abs(old["value"] - row["value"]) < 1e-8
            obs += rows
            metrics += stats
            inversions.append(inversion)
            models.append({"name": name, "method": model["route"], "coordinates": model["coordinates"],
                           "starting_coordinates": model["directory"] + "/input.com",
                           "calculation_artifacts": [model["directory"] + "/input.com", model["stdout"]],
                           "converged": True, "stationary": True,
                           "identity_validation": "Correct mapped C20H17ClN6OS E-imine N5-H thione, 0/1; raw coordinate graph rechecked.",
                           "stationarity_evidence": f"132 positive frequencies; minimum {audit['minimum_frequency_cm1']} cm^-1; real Opt/Freq logs.",
                           "rationale": "Archived source-informed author pair; this is not a blind autonomous model-selection history."})
        assert np.max(np.abs(starts[0] - starts[1])) < 1e-9
        comp = comparison(metrics, [m["name"] for m in models])
        expected_outcome = "second_uniformly_no_worse" if filename.startswith("PRIMARY") else "mixed"
        assert comp["overall"] == expected_outcome
        witness = {"status": "complete", "models": models,
                   "mapping": {"label_to_atom": {k: v + 1 for k, v in LABELS.items()},
                               "coordinate_index_base": 1, "mapping_basis": "Fixed source graph labels; Cl1/Cl2 alias. Raw source-informed historical calculations."},
                   "observables": obs, "metrics": metrics, "inversion_comparison": inversions, "comparison": comp,
                   "conclusion": ("The computed source-CIF conformers support CAM on all six metrics." if filename.startswith("PRIMARY")
                                  else "CAM has lower bond/angle MAE and RMSE; B3LYP lower torsion errors. This is a complete mixed comparison, not CAM-wins replication."),
                   "archive_context": "PRIVATE evidence of scientific calculability from successful source-informed runs. Not a blind-agent submission or an exact SI-theory reproduction."}
        check_complete(witness, coords_table)
        tests.append(filename + ": real calculation, full coverage, schema and arithmetic pass without limitations field.")
        for variant in ("mirror", "proper_rotation_translation", "row_reordering"):
            candidate = copy.deepcopy(witness)
            new_coords, rows, stats, invs = {}, [], [], []
            for name, coords in coords_table.items():
                if variant == "mirror":
                    altered = coords * [-1, 1, 1]
                    labels = LABELS
                elif variant == "proper_rotation_translation":
                    altered = coords @ np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) + [17, -2, 8]
                    labels = LABELS
                else:
                    order = np.arange(46)[::-1]
                    altered = coords[order]
                    labels = {k: int(np.where(order == v)[0][0]) for k, v in LABELS.items()}
                    candidate["mapping"].setdefault("model_label_to_atom", {})[name] = {k: v + 1 for k, v in labels.items()}
                new_coords[name] = altered
                r, s, inv = extract(altered, name, labels)
                rows += r
                stats += s
                invs.append(inv)
            candidate.update(observables=rows, metrics=stats, inversion_comparison=invs,
                             comparison=comparison(stats, comp["model_pair"]))
            check_complete(candidate, new_coords)
            assert candidate["comparison"]["overall"] == comp["overall"]
            for a, b in zip(stats, metrics):
                assert abs(a["mae"] - b["mae"]) < 1e-8 and abs(a["rmse"] - b["rmse"]) < 1e-8
            tests.append(filename + ": " + variant + " preserves normalized metrics and comparison (synthetic representation test).")
        for defect in ("missing_row", "duplicate_selector", "wrong_metric", "false_winner", "wrong_mapping",
                       "rowwise_sign_flip", "wrong_global_sign", "invalid_minimum"):
            bad = copy.deepcopy(witness)
            if defect == "missing_row":
                bad["observables"].pop()
            elif defect == "duplicate_selector":
                bad["observables"][1] = copy.deepcopy(bad["observables"][0])
            elif defect == "wrong_metric":
                bad["metrics"][0]["mae"] += 0.1
            elif defect == "false_winner":
                bad["comparison"]["overall"] = "first_uniformly_no_worse"
            elif defect == "wrong_mapping":
                bad["mapping"]["label_to_atom"]["N1"] = 22
            elif defect == "rowwise_sign_flip":
                row = next(r for r in bad["observables"] if r["kind"] == "torsion" and 10 < abs(r["value"]) < 170)
                row["value"] = -row["value"]
            elif defect == "wrong_global_sign":
                bad["inversion_comparison"][0]["selected_reference_sign"] *= -1
            else:
                bad["models"][0]["stationary"] = False
            try:
                check_complete(bad, coords_table)
            except (AssertionError, jsonschema.ValidationError, KeyError):
                tests.append(filename + ": rejects synthetic " + defect + ".")
            else:
                raise AssertionError("Failed to reject " + defect)
        branches_out.append({"source": str((SOURCE / filename).relative_to(REPO)), "raw_audits": audits,
                             "common_primary_start_confirmed": True, "metrics": metrics,
                             "inversion_comparison": inversions, "comparison": comp})
        witnesses[source["branch"]] = witness
    assert abs(float(circular(179, -179)) - 2) < 1e-12
    selected, _ = invert_stats([0] * 11, [0] * 11)
    assert selected["reference_sign"] == 1
    tests.append("Circular wrap 179/-179 gives 2 degrees; exact inversion tie chooses +1.")
    print(json.dumps({"scope": "Local postprocessing/schema and raw-evidence recheck only; no quantum jobs, external judge call or blind-agent replay.",
                      "protocol_id": "a396_geometry_comparison_v2", "tests_passed": len(tests), "tests": tests,
                      "branches": branches_out, "private_author_route_witnesses": witnesses}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
