---
software_id: gromacs
versions: ["installed 2026-era build"]
topics: ["index", "navigation", "capabilities"]
aliases: ["GROMACS", "gromacs"]
inputs: ["mdp", "topology.top", "coordinates.gro", "optional index and checkpoint"]
outputs: ["run.tpr", "run.log", "trajectory.xtc", "energy.edr", "final.gro", "checkpoint.cpt"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# GROMACS Native Software Guide

## Installed software
- Installed version: `installed 2026-era build`.
- Operational status: `runnable`.
- Configured runtime: `md`.
- Primary use: preprocess and run classical molecular dynamics with an explicit topology and MDP protocol.

## When to use this interface
Invoke one explicit GROMACS subcommand against staged topology, coordinate, trajectory, or run-input files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `gmx` | `arguments` | `gmx mdrun -deffnm production -nt 4` | None |

## Supported task families
- energy minimization.
- NVT.
- NPT.
- production MD.
- trajectory analysis.

## Layer 1 typed Actions
- `minimize_system_energy`.
- `propagate_dynamics`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://manual.gromacs.org/current/user-guide/index.html
- https://manual.gromacs.org/current/onlinehelp/gmx-mdrun.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
