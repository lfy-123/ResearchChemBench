---
software_id: vasp
versions: ["6"]
topics: [ground-state, single-point, energy]
aliases: [VASP static calculation, periodic energy]
inputs: ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
outputs: ["OUTCAR", "vasprun.xml", "CONTCAR", "WAVECAR"]
last_smoke_tested: 2026-07-28
example_path: chemistry_toolbox/examples/native/vasp/ground_state/
---
# VASP Ground State

## Required files
Stage `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS` under those exact names. POSCAR element order and counts must match the concatenated POTCAR datasets.

## Validation
Require a normal VASP end state, reached electronic convergence, and the expected `OUTCAR`, `vasprun.xml`, and wavefunction or charge files needed downstream. A scheduler exit without convergence is not a scientific success.
