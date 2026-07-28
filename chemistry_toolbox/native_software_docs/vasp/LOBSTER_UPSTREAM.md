---
software_id: vasp
versions: ["6"]
topics: [lobster-upstream, wavefunction]
aliases: [VASP for LOBSTER, WAVECAR compatibility]
inputs: ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
outputs: ["OUTCAR", "vasprun.xml", "CONTCAR", "WAVECAR"]
last_smoke_tested: null
---
# VASP Inputs for LOBSTER

## Compatibility
Use a LOBSTER-supported PAW basis and preserve consistent POSCAR, POTCAR, INCAR, KPOINTS, WAVECAR, and charge information. Generate the files in one compatible converged VASP workflow.

## Electronic settings
Follow the installed LOBSTER version requirements for projection-related VASP settings, band count, symmetry, and wavefunction output. Do not combine artifacts from different structures or k-point meshes.
