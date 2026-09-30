"""Read-only numerical/source audit; output is diagnostic JSON, not a PASS."""
from pathlib import Path
from collections import Counter
import json
import re
import fitz
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/verification/group_1/paper_9a58a1fa6ed7d780'


def xyz(path):
    rows = path.read_text().splitlines()[2:]
    return [r.split()[0] for r in rows], np.array([[float(v) for v in r.split()[1:4]] for r in rows])


def align(x, y):
    xc, yc = x - x.mean(0), y - y.mean(0)
    u, _, vt = np.linalg.svd(xc.T @ yc)
    rotation = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
    diff = xc @ rotation - yc
    return {'aligned_rmsd_A': float(np.sqrt((diff * diff).sum() / len(x))),
            'max_atom_displacement_A': float(np.linalg.norm(diff, axis=1).max()),
            'max_pair_distance_delta_A': float(np.abs(np.linalg.norm(x[:, None] - x[None, :], axis=2) - np.linalg.norm(y[:, None] - y[None, :], axis=2)).max())}


def fchk_arrays(p, keys):
    result = {}
    with p.open() as f:
        for line in f:
            key = line[:43].strip()
            if key not in keys:
                continue
            m = re.search(r'N=\s*(\d+)', line)
            if not m:
                continue
            count, values = int(m[1]), []
            while len(values) < count:
                values.extend(map(float, next(f).split()))
            result[key] = np.array(values)
            if len(result) == len(keys):
                break
    assert set(result) == set(keys)
    return result


def main():
    pdf = fitz.open(ROOT / 'papers/paper_9a58a1fa6ed7d780/documents/supplementary_001.pdf')
    table = pdf[48].get_text().split('Table S21.')[1] + pdf[49].get_text().split('Table S22.')[0]
    rows = re.findall(r'(?m)^(\d+)\s*\n([A-Z][a-z]?)\s*\n([-\d.]+)\s*\n([-\d.]+)\s*\n([-\d.]+)', table)
    assert [int(r[0]) for r in rows] == list(range(1, 41))
    symbols = [r[1] for r in rows]
    source_xyz = np.array([[float(v) for v in r[2:]] for r in rows])
    geometry = {}
    for mode in ['autonomous_research', 'paper_reproduction']:
        p = ROOT / 'tasks' / ('final_verified_' + mode) / 'paper_9a58a1fa6ed7d780/agent_input/data/inputs/bn_akflu_s0.xyz'
        elements, coords = xyz(p)
        geometry[mode] = {'same_element_order': elements == symbols, 'max_abs_SI_coordinate_delta_A': float(np.abs(coords-source_xyz).max())}
    elements, optimized = xyz(BASE / 'artifacts/gaussian_batch/supp_bn_akflu_b3lyp_optfreq/optimized_geometry.xyz')
    geometry['optimized_vs_SI'] = {'same_element_order': elements == symbols, **align(source_xyz, optimized)}
    keys = ['Atomic numbers', 'Current cartesian coordinates', 'Shell types', 'Primitive exponents', 'Contraction coefficients', 'Alpha Orbital Energies', 'Alpha MO coefficients']
    old = fchk_arrays(BASE / 'artifacts/gaussian_batch/supp_bn_akflu_td_b3lyp_optgeom/supp_bn_akflu_td_b3lyp_optgeom.fchk', keys)
    new = fchk_arrays(BASE / 'provenance/local_recovery_20260918/BN_AkFlu_TD6_fullcoeff_resume_20260918/fullcoeff.fchk', keys)
    geometry['recovered_fchk_vs_optimized'] = align(new['Current cartesian coordinates'].reshape(-1, 3) * .529177210903, optimized)
    wavefunction_deltas = {k: {'count': len(old[k]), 'max_abs_change': float(np.abs(old[k]-new[k]).max())} for k in keys}
    log = (BASE / 'provenance/local_recovery_20260918/BN_AkFlu_TD6_fullcoeff_resume_20260918/gaussian.log').read_text()
    states = re.findall(r'Excited State\s+(\d+):\s+Singlet-\S+\s+([\d.]+) eV\s+([\d.]+) nm\s+f=([\d.]+)', log)
    assert len(states) == 6
    reference = [(2.1406,.0080), (2.8505,.0001), (2.9880,0), (3.4014,0), (3.6113,1.8524), (3.7197,0)]
    spectrum = [{'state': int(s[0]), 'computed_energy_eV':float(s[1]), 'SI_energy_eV':r[0], 'delta_energy_eV':float(s[1])-r[0], 'computed_f':float(s[3]), 'SI_f':r[1]} for s,r in zip(states,reference)]
    audit = {'scope':'SI versus public inputs and actual verification artifacts; not a new computation or unconditional qualification',
             'SI_geometry_source':'PDF pages49-50 TableS21', 'SI_spectrum_source':'PDFpage42 TableS14',
             'actual_formula':dict(Counter(symbols)), 'geometry':geometry, 'recovered_vs_original_fchk':wavefunction_deltas,
             'spectrum':spectrum, 'SI_missing_details':['hole-electron configuration coefficient cutoff','integration grid','specific input/output pair for TableS11','separate energy/orbital identity attached to each TableS11 row']}
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
