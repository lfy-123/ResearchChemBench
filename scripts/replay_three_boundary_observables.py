#!/usr/bin/env python3
"""Read-only arithmetic replay of existing verification outputs, never a DFT job.

Print an evaluator-private JSON record. Do not modify group archives, select an
input from a target energy, or promote orbital projections to optical selection
rules. The historical band 133 is inspected as a *legacy candidate*, not chosen
as the correct band by this program.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ("paper_1b285cf9f763f2cf", "paper_534ae3b6e2fb695f", "paper_b815e2622b0d6085")


def read_json(path):
    return json.loads(Path(path).read_text())


def poscar(path):
    lines = Path(path).read_text().splitlines()
    scale = float(lines[1]); cell = np.array([list(map(float, x.split())) for x in lines[2:5]]) * scale
    symbols = lines[5].split(); counts = list(map(int, lines[6].split()))
    elements = [s for s, n in zip(symbols, counts) for _ in range(n)]
    i = 7 + int(lines[7].lower().startswith("s"))
    direct = lines[i].lower().startswith("d")
    coords = np.array([list(map(float, x.split()[:3])) for x in lines[i + 1:i + 1 + len(elements)]])
    return elements, (coords @ cell if direct else coords * scale), cell


def torsion(coords, atoms):
    a, b, c, d = [coords[i - 1] for i in atoms]
    axis = c - b; axis = axis / np.linalg.norm(axis)
    v = a - b; v = v - np.dot(v, axis) * axis
    w = d - c; w = w - np.dot(w, axis) * axis
    return float(np.degrees(np.arctan2(np.dot(np.cross(axis, v), w), np.dot(v, w))))


def plane_angle(coords, rings):
    normals = []
    for ring in rings:
        points = coords[np.array(ring) - 1]
        normals.append(np.linalg.svd(points - points.mean(axis=0))[2][-1])
    return math.degrees(math.acos(float(np.clip(abs(np.dot(*normals)), 0, 1))))


def first_shell_geometry(elements, coords, cell):
    """All nominal first-shell bonds/angles, never a target-nearest pair."""
    anions = [i for i, e in enumerate(elements) if e in ("O", "F")]
    result = []
    for i, e in enumerate(elements):
        if e not in ("Zn", "Li", "Si", "Al", "Fe"):
            continue
        n = 4 if e in ("Zn", "Li", "Si") else 6
        neighbors = []
        for j in anions:
            for shift in itertools.product((-1, 0, 1), repeat=3):
                v = coords[j] + np.array(shift) @ cell - coords[i]
                neighbors.append((float(np.linalg.norm(v)), j, shift, v))
        # Distances for symmetry-equivalent periodic neighbours can differ by
        # a few floating-point ulps depending on the NumPy/Python build.  A
        # raw distance sort therefore produced different shell membership on
        # different environments (for example O30 vs O36).  Treat distances
        # within 1e-8 Å as tied, then use atom index and image as stable
        # deterministic tie-breakers.  This is an extraction/archival rule,
        # not a change to the underlying coordinates or evaluator target.
        ordered = sorted(neighbors, key=lambda x: (round(x[0], 8), x[1], x[2]))
        shell = ordered[:n]
        angles = []
        for a, b in itertools.combinations(shell, 2):
            angle = math.degrees(math.acos(float(np.clip(np.dot(a[3], b[3]) / (a[0] * b[0]), -1, 1))))
            angles.append({"endpoints_1based": [a[1] + 1, i + 1, b[1] + 1],
                           "endpoint_images": [list(a[2]), list(b[2])],
                           "label": f"{elements[a[1]]}-{e}-{elements[b[1]]}", "degrees": angle})
        result.append({"center_1based": i + 1, "element": e, "nominal_shell_size": n,
                       "next_neighbor_distance_A": ordered[n][0],
                       "neighbors": [{"atom_1based": a[1] + 1, "image": list(a[2]),
                                      "element": elements[a[1]], "distance_A": a[0]} for a in shell],
                       "angles": angles})
    return result


def geometry_summary(geometry):
    """Summarize ALL extracted shells; no cherry-picked representative angle."""
    bonds, angles = {}, {}
    for center in geometry:
        for neighbor in center["neighbors"]:
            label = f'{center["element"]}-{neighbor["element"]}'
            bonds.setdefault(label, []).append(neighbor["distance_A"])
        for angle in center["angles"]:
            # Endpoint order is immaterial (O-Al-F and F-Al-O are one class).
            left, middle, right = angle["label"].split("-")
            ends = sorted((left, right))
            label = f"{ends[0]}-{middle}-{ends[1]}"
            angles.setdefault(label, []).append(angle["degrees"])
    def stats(groups):
        return {k: {"count": len(v), "mean": float(np.mean(v)), "minimum": min(v), "maximum": max(v)}
                for k, v in sorted(groups.items())}
    return {"cation_center_count": len(geometry), "bond_distributions_A": stats(bonds),
            "angle_distributions_deg": stats(angles),
            "extraction": "All nominal shells; bonds and all unordered neighbor-pair angles. Full per-center trace can be printed with --full-geometry."}


def replay_spinel(full_geometry=False):
    base = ROOT / "docs/verification/group_5" / PAPERS[0]
    rows = []
    for uc in (1, 2, 3):
        run = base / f"provenance/qzcli_hpc/uc{uc}_spinel_relax_u036_retry/1"
        elements, coords, cell = poscar(run / "CONTCAR")
        initial, _, initial_cell = poscar(run / "POSCAR")
        if Counter(initial) != Counter(elements) or not np.allclose(cell, initial_cell):
            raise ValueError("The archived endpoint changed the prescribed composition/cell")
        geometry = first_shell_geometry(elements, coords, cell)
        rows.append({"state_id": f"UC-{uc}", "source": str(run.relative_to(ROOT)),
                     "element_counts": dict(Counter(elements)), "atom_count": len(elements),
                     "nominal_ionic_charge_sum": sum({"Zn": 2, "Li": 1, "Si": 4, "Al": 3, "Fe": 3, "F": -1, "O": -2}[e] for e in elements),
                     "geometry": geometry if full_geometry else geometry_summary(geometry)})
    return {"states": rows, "scope": "One archived candidate per state; neutral electronic compensation, fixed cell. No exhaustive site-search or optical validation claimed.",
            "corrections": ["The historical composition prose omitted one Zn in each state.",
                            "Full nominal first-shell angle sets replace selection of a pair nearest a source angle."]}


def replay_diamines():
    base = ROOT / "docs/verification/group_6" / PAPERS[1]
    old = read_json(base / "provenance/tzvp_multiwfn_postprocessing_corrected_20260903.json")
    inputs = read_json(ROOT / "tasks/final_verified_autonomous_research" / PAPERS[1] / "agent_input/data/inputs/monomers.json")
    definitions = {m["id"]: m for m in inputs["molecules"]}
    rows = []
    for item in old["molecules"]:
        label = item["label"]; definition = definitions[label]
        xyz = ROOT / item["xyz"]; lines = xyz.read_text().splitlines()
        coords = np.array([list(map(float, x.split()[1:4])) for x in lines[2:2 + int(lines[0])]])
        cdft = base / f"artifacts/multiwfn/cdft_{label}_identity_corrected/CDFT.txt"
        text = cdft.read_text()
        def ev(name):
            return float(re.search(name + r"[^\n]*?([-+\d.]+)\s+eV", text).group(1))
        homo = ev(r"E_HOMO\(N\):"); global_n = ev(r"\n Nucleophilicity index:")
        local = []
        start = text.index("Condensed local electrophilicity/nucleophilicity index")
        end = text.index("Condensed local softness", start)
        for atom, value in re.findall(r"^\s*(\d+)\(N\s*\)\s+[-+\d.]+\s+([-+\d.]+)", text[start:end], re.M):
            local.append({"atom_map_id": int(atom), "value": float(value), "unit": "e*eV"})
        rows.append({"molecule_id": label, "xyz_source": item["xyz"], "cdft_source": str(cdft.relative_to(ROOT)),
                     "global_nucleophilicity_eV": global_n, "homo_eV": homo,
                     "reference_homo_eV_from_printed_output": homo - global_n,
                     "nitrogen_local_nucleophilicity": local,
                     "ring_plane_angle_deg": plane_angle(coords, definition["ring_atom_map_ids"]),
                     "linker_torsions": [{"atom_map_ids": a, "angle_deg": torsion(coords, a)} for a in definition["linker_torsion_atom_map_ids"]]})
    return {"molecules": rows, "corrections": ["Global N uses a TCE HOMO reference, not a vertical total-energy difference.",
            "PFMB central bond is 3-12, not 4-12; ether torsions are continuous bonded paths.",
            "Ring-plane angles and individual linker torsions are distinct observables; source four-atom numbers are not ring-plane targets."]}


def eigenval(path):
    lines = Path(path).read_text().splitlines()
    spins = int(lines[0].split()[3]); nelect, nk, nb = map(int, lines[5].split()); i = 6; rows = []
    for _ in range(nk):
        while not lines[i].strip():
            i += 1
        k = [float(x) for x in lines[i].split()[:3]]; i += 1
        for band in range(1, nb + 1):
            tokens = lines[i].split(); i += 1
            for s in range(spins):
                rows.append({"spin": s + 1, "band": band, "k": k,
                             "energy_eV": float(tokens[1 + s]), "occupation": float(tokens[1 + spins + s])})
    return rows, spins, nk


def k_key(k):
    """Fractional reciprocal points modulo reciprocal-lattice translations."""
    return tuple(round(float(x) % 1, 7) % 1 for x in k)


def summarize_edges(rows, spin=None, conduction_band=None):
    occupied = [r for r in rows if (spin is None or r["spin"] == spin) and r["occupation"] > 0.5]
    empty = [r for r in rows if (spin is None or r["spin"] == spin) and r["occupation"] <= 0.5
             and (conduction_band is None or r["band"] == conduction_band)]
    if not occupied or not empty:
        raise ValueError("No occupied/empty states for the requested comparison")
    vbm = max(occupied, key=lambda r: r["energy_eV"]); cbm = min(empty, key=lambda r: r["energy_eV"])
    occupied_by_k_spin = {}
    for v in occupied:
        key = (k_key(v["k"]), v["spin"])
        occupied_by_k_spin[key] = max(v["energy_eV"], occupied_by_k_spin.get(key, -math.inf))
    direct = min(r["energy_eV"] - occupied_by_k_spin[(k_key(r["k"]), r["spin"])] for r in empty)
    # Degenerate extrema may have several valid locations, not just the first row.
    tolerance = 1e-5
    vks = {k_key(r["k"]) for r in occupied if abs(r["energy_eV"] - vbm["energy_eV"]) <= tolerance}
    cks = {k_key(r["k"]) for r in empty if abs(r["energy_eV"] - cbm["energy_eV"]) <= tolerance}
    return {"spin": spin, "vbm": vbm, "conduction_edge": cbm,
            "edge_gap_eV": cbm["energy_eV"] - vbm["energy_eV"], "minimum_same_k_gap_eV": direct,
            "vbm_k_set": sorted(vks), "conduction_edge_k_set": sorted(cks),
            "degeneracy_tolerance_eV": tolerance,
            "directness_on_sampled_mesh": "direct" if vks & cks else "indirect"}


def component_projection_summary(run, full_records=False):
    """Inspect existing collinear PROCAR; no transition/optical calculation.

    Raw three-decimal ion projections are normalized by their sum (not treated
    as exact whole-space orbital populations). Organic Br is identified by
    short C-Br connectivity, not its element name alone.
    """
    elements, coords, cell = poscar(run / "POSCAR")
    carbon = [i for i, e in enumerate(elements) if e == "C"]
    halogens = [i for i, e in enumerate(elements) if e in ("Cl", "Br", "I")]
    shifts = np.array(list(itertools.product((-1, 0, 1), repeat=3))) @ cell
    # Broad covalent-bond cutoffs; in these archived structures all assignments
    # have large margins. Store distances so this assumption is auditable.
    cutoffs = {"Cl": 2.2, "Br": 2.4, "I": 2.6}
    distances = {i: min(float(np.linalg.norm(coords[j] + shift - coords[i]))
                        for j in carbon for shift in shifts) for i in halogens}
    organic_halogen = {i for i in halogens if distances[i] < cutoffs[elements[i]]}
    organic = {i for i, e in enumerate(elements) if e in ("C", "H", "N")} | organic_halogen
    framework = set(range(len(elements))) - organic
    if len(organic_halogen) != 4 or Counter(elements[i] for i in framework) != {"Pb": 4, "Br": 12}:
        raise ValueError("Unexpected organic/inorganic atom partition")
    records = []; current_k = None; kindex = 0; spin = 1
    lines = (run / "PROCAR").read_text().splitlines(); i = 0
    while i < len(lines):
        line = lines[i]; i += 1
        m = re.match(r"\s*k-point\s+(\d+)\s*:\s*(\S+)\s+(\S+)\s+(\S+)", line)
        if m:
            new_index = int(m[1])
            if new_index < kindex:
                spin += 1
            kindex = new_index; current_k = list(map(float, m.groups()[1:])); continue
        m = re.match(r"\s*band\s+(\d+)\s+# energy\s+(\S+)\s+# occ\.\s+(\S+)", line)
        if not m or float(m[3]) > 0.5:
            continue
        while i < len(lines) and not lines[i].strip().startswith("ion"):
            i += 1
        columns = lines[i].split()[1:]; i += 1
        values = np.array([list(map(float, x.split()[1:])) for x in lines[i:i + len(elements)]]); i += len(elements)
        total_index = columns.index("tot"); total = float(values[:, total_index].sum())
        pb_p = sum(float(values[j, columns.index(o)]) for j, e in enumerate(elements) if e == "Pb" for o in ("px", "py", "pz"))
        pb_total = sum(float(values[j, total_index]) for j, e in enumerate(elements) if e == "Pb")
        framework_total = sum(float(values[j, total_index]) for j in framework)
        groups = {}
        for element in sorted(set(elements)):
            indices = [j for j, e in enumerate(elements) if e == element]
            for angular, names in (("s", ("s",)), ("p", ("px", "py", "pz")),
                                   ("d", ("dxy", "dyz", "dz2", "dxz", "x2-y2"))):
                groups[element + "_" + angular] = sum(float(values[j, columns.index(o)]) for j in indices for o in names) / total
        component_groups = {}
        if full_records:
            for component, atoms in (("organic", organic), ("framework", framework)):
                for element in sorted({elements[j] for j in atoms}):
                    indices = [j for j in atoms if elements[j] == element]
                    for angular, names in (("s", ("s",)), ("p", ("px", "py", "pz")),
                                           ("d", ("dxy", "dyz", "dz2", "dxz", "x2-y2"))):
                        component_groups[f"{component}:{element}:{angular}"] = sum(
                            float(values[j, columns.index(o)]) for j in indices for o in names) / total
        records.append({"band": int(m[1]), "spin": spin, "k": current_k, "energy_eV": float(m[2]),
                        "normalized_framework_weight": framework_total / total,
                        "normalized_organic_weight": 1 - framework_total / total,
                        "normalized_Pb_p_weight": pb_p / total,
                        "raw_Pb_total": pb_total, "raw_total_projection": total,
                        "normalized_element_orbital_groups": groups})
        if full_records:
            ranked = sorted(component_groups, key=lambda key: (-component_groups[key], key))
            records[-1].update(normalized_component_orbital_groups=component_groups,
                               leading_group=ranked[0],
                               leading_margin=component_groups[ranked[0]] - component_groups[ranked[1]])
    low_bands = sorted({r["band"] for r in records})[:10]
    summary = {}
    for band in low_bands:
        rs = [r for r in records if r["band"] == band]
        summary[str(band)] = {"minimum_energy_record": min(rs, key=lambda r: r["energy_eV"]),
                              "framework_weight_range": [min(r["normalized_framework_weight"] for r in rs), max(r["normalized_framework_weight"] for r in rs)],
                              "Pb_p_weight_range": [min(r["normalized_Pb_p_weight"] for r in rs), max(r["normalized_Pb_p_weight"] for r in rs)]}
    result = {"source": str((run / "PROCAR").relative_to(ROOT)), "record_count": len(records),
            "organic_atom_indices_1based": sorted(i + 1 for i in organic),
            "framework_atom_indices_1based": sorted(i + 1 for i in framework),
            "halogen_nearest_carbon_A": {str(i + 1): d for i, d in distances.items()},
            "organic_halogen_cutoffs_A": cutoffs,
            "lowest_ten_unoccupied_bands": summary,
            "scope": "Existing sampled collinear wavefunctions; rounded atom-projection normalization only. This supports orbital character, not optical allowedness or full-zone manifold tracking."}
    if full_records:
        result["all_unoccupied_records"] = records
    return result


def xyz_atoms(path):
    lines = Path(path).read_text().splitlines()
    atoms = [line.split() for line in lines[2:2 + int(lines[0])]]
    if len(atoms) != int(lines[0]):
        raise ValueError(f"Truncated XYZ: {path}")
    return [row[0] for row in atoms], np.array([row[1:4] for row in atoms], dtype=float)


def orca_record(run):
    """Application evidence, not scheduler success. Does not run ORCA."""
    text = (run / "orca_stdout.log").read_text()
    inp = (run / "input.inp").read_text()
    energies = re.findall(r"FINAL SINGLE POINT ENERGY\s+([-+\d.]+)", text)
    spin = re.search(r"\*\s+xyz\s+(-?\d+)\s+(\d+)", inp, re.I)
    if not energies or "ORCA TERMINATED NORMALLY" not in text or not spin:
        raise ValueError(f"No complete ORCA result: {run}")
    return {"output": str((run / "orca_stdout.log").relative_to(ROOT)),
            "input": str((run / "input.inp").relative_to(ROOT)),
            "route": next(line for line in inp.splitlines() if line.startswith("!")),
            "charge": int(spin[1]), "multiplicity": int(spin[2]),
            "normal_termination": True, "final_electronic_energy_Eh": float(energies[-1]),
            "optimization_completed": "OPTIMIZATION RUN DONE" in text}


def release_diamine_details():
    """Complete mapping/residual/probe provenance absent from the legacy replay."""
    from rdkit import Chem

    base = ROOT / "docs/verification/group_6" / PAPERS[1]
    definitions = {m["id"]: m for m in read_json(ROOT / "tasks/final_verified_autonomous_research" /
                   PAPERS[1] / "agent_input/data/inputs/monomers.json")["molecules"]}
    records = replay_diamines()["molecules"]
    multiwfn = {}
    for stamp in ("023800", "023945"):
        path = base / f"provenance/cdft_multiwfn_short_20260903T{stamp}Z.json"
        for entry in read_json(path)["records"]:
            multiwfn[entry["label"]] = (path, entry)
    for row in records:
        label = row["molecule_id"]; definition = definitions[label]
        geometry_path = ROOT / row["xyz_source"]
        elements, coords = xyz_atoms(geometry_path)
        mol = Chem.MolFromSmiles(definition["atom_mapped_smiles"])
        maps = {a.GetAtomMapNum(): a.GetSymbol() for a in mol.GetAtoms()}
        if any(elements[i - 1] != element for i, element in maps.items()):
            raise ValueError(f"Element map mismatch: {label}")
        expected = {tuple(sorted((b.GetBeginAtom().GetAtomMapNum(), b.GetEndAtom().GetAtomMapNum())))
                    for b in mol.GetBonds()}
        radii = Chem.GetPeriodicTable()
        observed = {tuple(sorted((a, b))) for a, b in itertools.combinations(maps, 2)
                    if np.linalg.norm(coords[a - 1] - coords[b - 1]) <
                    1.25 * (radii.GetRcovalent(maps[a]) + radii.GetRcovalent(maps[b]))}
        if expected != observed:
            raise ValueError(f"Heavy-atom graph mismatch: {label}")
        row["atom_mapping"] = [{"map_id": i, "xyz_index_1based": i, "element": maps[i]} for i in sorted(maps)]
        row["mapping_check"] = {"all_mapped_elements_match": True, "heavy_atom_edges": sorted(expected),
                                "distance_graph_matches": True, "covalent_radii_multiplier": 1.25,
                                "scope": "Element and heavy-atom connectivity; not an energy-based identity match."}
        row["plane_fits"] = []
        for ring in definition["ring_atom_map_ids"]:
            points = coords[np.array(ring) - 1]; centered = points - points.mean(axis=0)
            normal = np.linalg.svd(centered)[2][-1]; residuals = centered @ normal
            row["plane_fits"].append({"atom_map_ids": ring, "rms_residual_A": float(np.sqrt(np.mean(residuals**2))),
                                      "max_absolute_residual_A": float(np.max(np.abs(residuals)))})
        opt = orca_record(geometry_path.parent)
        hess_path = geometry_path.parent / "input.hess"
        block = hess_path.read_text().split("$vibrational_frequencies", 1)[1].split("$", 1)[0].splitlines()
        block = [line.split() for line in block if line.strip()]
        frequencies = [float(line[1]) for line in block[1:]]
        if len(frequencies) != int(block[0][0]) or len(frequencies) != 3 * len(elements):
            raise ValueError(f"Incomplete Hessian frequencies: {label}")
        opt["frequency_validation"] = {"source": str(hess_path.relative_to(ROOT)), "count_3N": len(frequencies),
            "frequencies_cm_1": frequencies, "imaginary_count": sum(f < -1e-6 for f in frequencies),
            "minimum_vibrational_frequency_cm_1": min(frequencies[6:]),
            "translation_rotation_count": sum(abs(f) <= 1e-6 for f in frequencies)}
        row["optimization"] = opt
        record_path, mw = multiwfn[label]
        row["multiwfn"] = {"execution_record": str(record_path.relative_to(ROOT)), "stdout": mw["stdout"],
                           "stdin": mw["stdin_file"], "route": mw["route"], "probes": {}}
        for probe, key in (("N", "N_wfn"), ("Nminus1", "Nminus1"), ("Nplus1", "Nplus1")):
            wfn_path = ROOT / mw["wfn_files"][probe]["path"]
            wfn_bytes = wfn_path.read_bytes()
            matches = [p.parent for p in (base / f"provenance/qzcli_hpc/{label}_{key}_cdft_tzvp_sp").glob("*/input.wfn")
                       if p.read_bytes() == wfn_bytes]
            if len(matches) != 1:
                raise ValueError(f"Nonunique actual WFN source: {label}/{probe}: {matches}")
            run = matches[0]; calculation = orca_record(run)
            wfn_text = wfn_bytes.decode()
            nuclei = re.findall(r"^\s*([A-Za-z]+)\s*\d+\s+\(CENTRE\s+\d+\)\s+(\S+)\s+(\S+)\s+(\S+)", wfn_text, re.M)
            if [n[0] for n in nuclei] != elements:
                raise ValueError(f"WFN atom order mismatch: {label}/{probe}")
            wfn_coords = np.array([n[1:] for n in nuclei], dtype=float) * 0.529177210903
            error = float(np.max(np.abs(wfn_coords - coords)))
            if error > 2e-6:
                raise ValueError(f"Probe not on the recorded neutral geometry: {label}/{probe}: {error}")
            calculation.update(wfn_source=str(wfn_path.relative_to(ROOT)), same_neutral_geometry=True,
                               maximum_coordinate_difference_A=error)
            row["multiwfn"]["probes"][probe] = calculation
        cdft = (ROOT / row["cdft_source"]).read_text().split("Condensed local electrophilicity", 1)[0]
        row["nitrogen_charge_probes"] = [
            {"atom_map_id": int(m[0]), **dict(zip(("q_N_e", "q_Nplus1_e", "q_Nminus1_e", "f_minus_e"), map(float, m[1:])))}
            for m in re.findall(r"^\s*(\d+)\(N\s*\)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", cdft, re.M)]
    return {"molecules": records, "new_quantum_calculations": False, "agent_visible": False,
            "calibration": "The public fixed TCE HOMO is an approved benchmark convention, not a uniquely recovered author formula.",
            "rounding": "CDFT charges/HOMO/global N have four decimals, local N five. Do not demand exact multiplication of independently rounded printed values."}


def release_spinel_details():
    result = replay_spinel(full_geometry=True)
    host = ROOT / "tasks/final_verified_autonomous_research" / PAPERS[0] / "agent_input/data/inputs/host_initial.cif"
    atoms = [line.split() for line in host.read_text().splitlines()]
    atoms = [a for a in atoms if len(a) == 6 and a[1] in ("Zn", "Al", "O")]
    host_frac = np.array([a[2:5] for a in atoms], dtype=float)
    for row in result["states"]:
        run = ROOT / row["source"]
        elements, coords, cell = poscar(run / "POSCAR")
        final_elements, _, _ = poscar(run / "CONTCAR")
        if elements != final_elements:
            raise ValueError("Endpoint changed atom ordering")
        mapping = []
        for index, point in enumerate(coords @ np.linalg.inv(cell)):
            delta = host_frac - point; delta -= np.round(delta)
            distances = np.linalg.norm(delta @ cell, axis=1)
            hits = np.flatnonzero(distances < 1e-8)
            if len(hits) != 1:
                raise ValueError("Ambiguous retained host-label mapping")
            atom = atoms[int(hits[0])]
            mapping.append({"file_index_1based": index + 1, "host_label": atom[0],
                            "parent_element": atom[1], "final_element": elements[index]})
        if len({m["host_label"] for m in mapping}) != len(elements):
            raise ValueError("Duplicated host label")
        row["retained_atom_mapping"] = mapping
        for center in row["geometry"]:
            center["host_label"] = mapping[center["center_1based"] - 1]["host_label"]
            center["shell_gap_to_next_neighbor_A"] = center["next_neighbor_distance_A"] - max(n["distance_A"] for n in center["neighbors"])
            if len({(n["atom_1based"], tuple(n["image"])) for n in center["neighbors"]}) != center["nominal_shell_size"]:
                raise ValueError("Repeated periodic image in shell")
            for neighbor in center["neighbors"]:
                neighbor["host_label"] = mapping[neighbor["atom_1based"] - 1]["host_label"]
            for angle in center["angles"]:
                angle["host_labels"] = [mapping[i - 1]["host_label"] for i in angle["endpoints_1based"]]
        text = (run / "OUTCAR").read_text()
        magnetization = re.findall(r"number of electron\s+(\S+)\s+magnetization\s+(\S+)", text)
        if not magnetization or "reached required accuracy" not in text or "General timing and accounting" not in text:
            raise ValueError(f"Incomplete spinel relaxation: {run}")
        force_blocks = re.findall(r"TOTAL-FORCE \(eV/Angst\)\s*\n\s*-+\n(.*?)\n\s*-+", text, re.S)
        forces = np.array([line.split()[3:6] for line in force_blocks[-1].splitlines()], dtype=float)
        row["validation"] = {"output": str((run / "OUTCAR").relative_to(ROOT)),
            "input": str((run / "INCAR").relative_to(ROOT)), "normal_timing_footer": True,
            "required_force_accuracy_reached": True, "maximum_force_norm_eV_A": float(np.max(np.linalg.norm(forces, axis=1))),
            "electron_count": float(magnetization[-1][0]), "integrated_magnetization_muB": float(magnetization[-1][1]),
            "magnetic_scope": "ISPIN=2 with initial Fe moment 5 muB; integrated final moment is not an assigned Fe oxidation state.",
            "incar": (run / "INCAR").read_text(), "kpoints": (run / "KPOINTS").read_text()}
        row["complete_set_summary"] = geometry_summary(row["geometry"])
    return {**result, "new_quantum_calculations": False, "agent_visible": False}


def replay_bands():
    base = ROOT / "docs/verification/group_6" / PAPERS[2]
    archive = read_json(base / "artifacts/native/b815_hse06_projection_analysis.json")
    result = {}
    for label, runs in archive["objects"].items():
        entry = {}
        for name in ("parent_2x2", "stability_3x3"):
            path = ROOT / runs[name]["run_directory"] / "EIGENVAL"
            rows, spins, nk = eigenval(path)
            entry[name] = {"source": str(path.relative_to(ROOT)), "nkpoints": nk,
                           "fundamental": [summarize_edges(rows, s) for s in range(1, spins + 1)],
                           "legacy_band_133_candidate": [summarize_edges(rows, s, 133) for s in range(1, spins + 1)],
                           "combined_spin_fundamental": summarize_edges(rows),
                           "combined_spin_legacy_candidate": summarize_edges(rows, conduction_band=133)}
        for quantity in ("edge_gap_eV", "minimum_same_k_gap_eV"):
            values = [entry[n]["combined_spin_legacy_candidate"][quantity] for n in ("parent_2x2", "stability_3x3")]
            entry[quantity + "_mesh_change"] = {"signed_eV": values[1] - values[0], "absolute_eV": abs(values[1] - values[0])}
        entry["component_projection_check"] = component_projection_summary(Path(runs["projection_2x2"]["run_directory"]))
        entry["assignment_status"] = "legacy_candidate_only; projections do not alone establish optical allowedness or exhaustive manifold assignment"
        result[label] = entry
    return {"objects": result, "corrections": ["Directness compares two edge k points, not whether a point is Gamma.",
            "A minimum same-k transition differs from the gap between independently extremized band edges.",
            "No scalar-relativistic result is an SOC result; finite mesh checks do not prove full-zone extrema."]}


def release_band_details():
    """Character-first candidate selection. Missing mesh projections stay missing.

    This function never consults gold energies or a predetermined band number.
    Detailed lower-band records are retained, while the full PROCAR is linked.
    It does not certify wavefunction continuity from eigenvalue proximity alone.
    """
    base = ROOT / "docs/verification/group_6" / PAPERS[2]
    archive = read_json(base / "artifacts/native/b815_hse06_projection_analysis.json")
    result = {}
    for label, runs in archive["objects"].items():
        run = Path(runs["projection_2x2"]["run_directory"])
        projection = component_projection_summary(run, full_records=True)
        records = projection.pop("all_unoccupied_records")
        by_band = {band: [r for r in records if r["band"] == band] for band in sorted({r["band"] for r in records})}
        edges = [min(rs, key=lambda r: r["energy_eV"]) for rs in by_band.values()]
        candidates = [r for r in edges if r["leading_group"] == "framework:Pb:p"]
        if not candidates:
            result[label] = {"projection": projection, "assignment_status": "ambiguous_no_Pb_leading_edge"}
            continue
        edge = min(candidates, key=lambda r: r["energy_eV"])
        selected = by_band[edge["band"]]
        lower = [r for r in edges if r["energy_eV"] < edge["energy_eV"]]
        rows, spins, nk = eigenval(run / "EIGENVAL")
        lookup = {(r["spin"], r["band"], k_key(r["k"])): r for r in rows}
        error = max(abs(r["energy_eV"] - lookup[(r["spin"], r["band"], k_key(r["k"]))]["energy_eV"]) for r in records)
        if error > 1e-5:
            raise ValueError("PROCAR energies do not match the same-run EIGENVAL")
        # Keep every k/spin record of all lower-band candidates and the first
        # Pb-leading band, including mixed k points, rather than one chosen edge.
        relevant = {r["band"] for r in lower} | {edge["band"]}
        projection["lower_and_candidate_records"] = [r for r in records if r["band"] in relevant]
        entry = {"projection": projection, "same_run_energy_max_difference_eV": error,
                 "candidate_edge": edge, "all_lower_band_edges": lower,
                 "candidate_leading_groups_across_mesh": sorted({r["leading_group"] for r in selected}),
                 "candidate_Pb_p_weight_range": [min(r["normalized_Pb_p_weight"] for r in selected), max(r["normalized_Pb_p_weight"] for r in selected)],
                 "primary_fundamental": summarize_edges(rows),
                 "primary_character_selected_candidate": summarize_edges(rows, conduction_band=edge["band"]),
                 "numerical_comparisons": {}, "raw_validation": {}}
        for name in ("parent_2x2", "projection_2x2", "stability_3x3"):
            path = Path(runs[name]["run_directory"])
            out = (path / "OUTCAR").read_text(); incar = (path / "INCAR").read_text()
            entry["raw_validation"][name] = {
                "source": str(path.relative_to(ROOT)), "incar": incar, "kpoints": (path / "KPOINTS").read_text(),
                "normal_timing_footer": "General timing and accounting" in out,
                "electronic_convergence_recorded": "aborting loop because EDIFF is reached" in out,
                "projection_present": (path / "PROCAR").exists()}
            if name == "projection_2x2":
                continue
            check_rows, _, _ = eigenval(path / "EIGENVAL")
            comparison = {"fundamental": summarize_edges(check_rows),
                          "same_ordinal_candidate_not_independently_reassigned": summarize_edges(check_rows, conduction_band=edge["band"])}
            for quantity, primary, check in (
                    ("fundamental", entry["primary_fundamental"], comparison["fundamental"]),
                    ("framework_candidate", entry["primary_character_selected_candidate"], comparison["same_ordinal_candidate_not_independently_reassigned"])):
                comparison[quantity + "_changes"] = {}
                for key in ("edge_gap_eV", "minimum_same_k_gap_eV"):
                    delta = check[key] - primary[key]
                    comparison[quantity + "_changes"][key] = {"signed_eV": delta, "absolute_eV": abs(delta)}
            entry["numerical_comparisons"][name] = comparison
        entry["assignment_status"] = "primary_character_candidate_supported; cross_mesh_state_identity_not_independently_verified"
        entry["limitations"] = [
            "The first candidate is selected by its leading component/element/angular group, not band ordinal or target energy.",
            "All lower edges and candidate k/spin character are included. Mixed character is retained, not forced above 50 percent.",
            "The archived 3x3 mesh has no PROCAR. Its same-ordinal comparison is a spectral sensitivity diagnostic, not proof of an identical framework manifold.",
            "No transition matrix elements: optical_allowedness remains not_established. No SOC or full-Brillouin-zone claim."]
        result[label] = entry
    return {"objects": result, "new_quantum_calculations": False, "agent_visible": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", choices=PAPERS)
    parser.add_argument("--full-geometry", action="store_true", help="Print every spinel shell bond and angle instead of complete-set summaries")
    parser.add_argument("--release-details", action="store_true", help="Read full mapping, application and observable evidence; never writes archives")
    args = parser.parse_args()
    if args.release_details:
        replay = {PAPERS[0]: release_spinel_details, PAPERS[1]: release_diamine_details, PAPERS[2]: release_band_details}[args.paper]()
    else:
        replay = (replay_spinel(full_geometry=args.full_geometry) if args.paper == PAPERS[0]
                  else {PAPERS[1]: replay_diamines, PAPERS[2]: replay_bands}[args.paper]())
    print(json.dumps({"paper_id": args.paper, "record_type": "existing_output_arithmetic_replay",
                      "new_quantum_calculations": False, "agent_visible": False, **replay}, indent=2))


if __name__ == "__main__":
    main()
