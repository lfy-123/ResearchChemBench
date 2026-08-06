---
software_id: gmx_mmpbsa
versions: ["1.6.5"]
topics: ["index", "navigation", "capabilities"]
aliases: ["gmx_MMPBSA", "gmx mmpbsa"]
inputs: ["mmpbsa.in", "complex TPR", "index NDX", "trajectory XTC", "topology TOP and ITP includes"]
outputs: ["FINAL_RESULTS_MMPBSA.dat", "FINAL_RESULTS_MMPBSA.csv", "optional FINAL_DECOMP_MMPBSA.dat and CSV"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# gmx_MMPBSA Native Software Guide

## Installed software
- Installed version: `1.6.5`.
- Operational status: `runnable_isolated_runtime`.
- Configured runtime: `gmx_mmpbsa`.
- Primary use: calculate MM/GBSA or MM/PBSA end-state binding energies and residue decompositions from GROMACS trajectories.

## When to use this interface
Calculate end-state binding energies or residue decompositions from an explicit gmx_MMPBSA input deck and matching GROMACS files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `gmx_MMPBSA` | `arguments` | `gmx_MMPBSA -O -i mmpbsa.in -cs complex.tpr -ci index.ndx -cg 3 4 -ct trajectory.xtc -cp topology.top -o FINAL_RESULTS_MMPBSA.dat -eo FINAL_RESULTS_MMPBSA.csv -nogui` | `mmpbsa.in`, `complex.tpr`, `index.ndx`, `trajectory.xtc`, `topology.top`, `toppar/forcefield.itp` |

## Supported task families
- binding free energy.
- MM GBSA.
- MM PBSA.
- per-frame energy analysis.
- residue decomposition.

## Layer 1 typed Actions
- `calculate_end_state_binding_free_energy`.
- `calculate_end_state_energy_decomposition`.
- `summarize_end_state_free_energy_results`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://valdes-tresanco-ms.github.io/gmx_MMPBSA/dev/installation/
- https://valdes-tresanco-ms.github.io/gmx_MMPBSA/dev/input_file/
- https://valdes-tresanco-ms.github.io/gmx_MMPBSA/dev/examples/Protein_ligand/ST/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
