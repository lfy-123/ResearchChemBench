---
software_id: lammps
versions: ["installed build"]
topics: ["index", "navigation", "capabilities"]
aliases: ["LAMMPS", "lammps"]
inputs: ["input.lammps", "optional data file", "potential files", "included scripts"]
outputs: ["log.lammps", "dump files", "restart files", "user-defined tables"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# LAMMPS Native Software Guide

## Installed software
- Installed version: `installed build`.
- Operational status: `runnable`.
- Configured runtime: `md`.
- Primary use: classical atomistic simulation from a LAMMPS input script.

## When to use this interface
Execute a complete LAMMPS input script. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `lmp` | `arguments` | `lmp -in input.lammps` | `input.lammps`, `all data/potential files referenced by it` |

## Supported task families
- energy minimization.
- molecular dynamics.
- Monte Carlo-assisted workflows.
- materials deformation.
- trajectory generation.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://docs.lammps.org/Manual.html
- https://docs.lammps.org/Commands_all.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
