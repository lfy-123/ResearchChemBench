---
software_id: vasp
versions: ["6"]
topics: [index]
aliases: [VASP navigation, periodic DFT]
inputs: ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
outputs: ["OUTCAR", "vasprun.xml", "CONTCAR", "WAVECAR"]
last_smoke_tested: null
---
# VASP Native Guide

## Topics
- `ground-state`: required input set and electronic minimization.
- `relaxation`: ionic and cell relaxation.
- `lobster-upstream`: VASP settings required by LOBSTER.
- `troubleshooting`: file compatibility, electronic convergence, resources, and termination.
