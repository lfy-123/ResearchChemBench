---
software_id: lobster
versions: ["5"]
topics: [vasp-requirements, upstream]
aliases: [LOBSTER VASP compatibility, required VASP files]
---
# LOBSTER VASP Requirements

## Required artifacts
For the installed LOBSTER 5.1.0 build, stage `lobsterin`, `POSCAR`, `POTCAR`, `WAVECAR`, `CONTCAR`, `KPOINTS`, `OUTCAR`, and `vasprun.xml` under those exact names. Some analyses also require charge-density outputs.

## Provenance
All upstream files must come from the same converged structure, pseudopotential set, k-point mesh, and electronic calculation. File existence alone does not prove compatibility.
