---
software_id: vaspkit
versions: ["1.5.1"]
topics: ["index", "navigation", "capabilities"]
aliases: ["VASPKIT", "vaspkit"]
inputs: ["POSCAR or CONTCAR and task-specific INCAR EIGENVAL DOSCAR OUTCAR PROCAR CHGCAR or LOCPOT files"]
outputs: ["task-specific KPOINTS structures tables grids plots and stdout summaries"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# VASPKIT Native Software Guide

## Installed software
- Installed version: `1.5.1`.
- Operational status: `runnable_local_nonredistributable_binary`.
- Configured runtime: `vaspkit`.
- Primary use: prepare and post-process explicitly supplied VASP structure and electronic-result files.

## When to use this interface
Run one explicitly selected VASPKIT structure or VASP-output processing task from Agent-staged files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `vaspkit` | `arguments` | `vaspkit -task 601 -file POSCAR -symprec 1e-5` | `POSCAR` |

## Supported task families
- K-point meshes.
- crystal symmetry.
- band gaps.
- bands.
- density of states.
- charge and potential analysis.

## Layer 1 typed Actions
- `analyze_crystal_symmetry`.
- `generate_vasp_kpoint_mesh`.
- `extract_vasp_band_gap`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://vaspkit.com/installation.html
- https://vaspkit.com/tutorials.html
- https://vaspkit.com/features.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
