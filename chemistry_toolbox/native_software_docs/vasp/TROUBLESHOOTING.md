---
software_id: vasp
versions: ["6"]
topics: [troubleshooting, errors]
aliases: [VASP failed, POTCAR mismatch, electronic convergence]
inputs: ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
outputs: ["OUTCAR", "vasprun.xml", "CONTCAR", "WAVECAR"]
last_smoke_tested: null
---
# VASP Troubleshooting

## Immediate input failure
Check that all four required files exist under exact uppercase names, atom counts match, POTCAR ordering matches POSCAR, and INCAR values are valid for the installed version.

## Convergence failure
Do not interpret energies from an unconverged step. Diagnose the electronic algorithm, mixing, smearing, cutoff, k-point sampling, and starting wavefunction before only increasing `NELM`.
