---
software_id: gnina
versions: ["1.3.3"]
topics: ["index", "navigation", "capabilities"]
aliases: ["GNINA", "gnina"]
inputs: ["receptor file", "ligand file", "box center and dimensions", "optional model"]
outputs: ["poses.sdf", "docking log", "affinity and CNN scores"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# GNINA Native Software Guide

## Installed software
- Installed version: `1.3.3`.
- Operational status: `runnable_cpu_or_gpu`.
- Configured runtime: `docking`.
- Primary use: molecular docking or CNN rescoring in a defined receptor box.

## When to use this interface
Run GNINA docking/rescoring with explicitly selected receptor, ligand, box, CNN model, and search settings. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `gnina` | `arguments` | `gnina -r receptor.pdbqt -l ligand.sdf --center_x 0 --center_y 0 --center_z 0 --size_x 20 --size_y 20 --size_z 20 -o poses.sdf` | `ligand.sdf` |

## Supported task families
- docking.
- score-only evaluation.
- local optimization.
- CNN rescoring.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://github.com/gnina/gnina
- https://gnina.github.io/gnina/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
