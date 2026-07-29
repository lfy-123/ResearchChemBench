---
software_id: vina
versions: ["f458505-mod"]
topics: ["index", "navigation", "capabilities"]
aliases: ["AutoDock Vina", "vina"]
inputs: ["receptor.pdbqt", "ligand.pdbqt", "box center and size"]
outputs: ["poses.pdbqt", "docking log", "affinity table"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# AutoDock Vina Native Software Guide

## Installed software
- Installed version: `f458505-mod`.
- Operational status: `runnable`.
- Configured runtime: `docking`.
- Primary use: dock a prepared PDBQT ligand into a prepared receptor box.

## When to use this interface
Run AutoDock Vina docking or scoring with explicitly selected receptor, ligand, box, and search settings. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `vina` | `arguments` | `vina --receptor receptor.pdbqt --ligand ligand.pdbqt --center_x 0 --center_y 0 --center_z 0 --size_x 20 --size_y 20 --size_z 20 --out poses.pdbqt --exhaustiveness 8` | `receptor.pdbqt`, `ligand.pdbqt` |

## Supported task families
- docking.
- score-only.
- local optimization.
- batch docking.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://autodock-vina.readthedocs.io/en/latest/
- https://github.com/ccsb-scripps/AutoDock-Vina

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
