---
software_id: namd
versions: ["3.0.2"]
topics: ["index", "navigation", "capabilities"]
aliases: ["NAMD", "namd"]
inputs: ["input.conf", "PSF", "coordinates", "parameter files", "optional restart files"]
outputs: ["stdout.log", "trajectory.dcd", "restart coordinates and velocities", "extended-system file"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# NAMD Native Software Guide

## Installed software
- Installed version: `3.0.2`.
- Operational status: `runnable`.
- Configured runtime: `namd`.
- Primary use: classical molecular dynamics from a NAMD configuration and prepared molecular system.

## When to use this interface
Execute a complete NAMD configuration. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `namd3` | `arguments` | `namd3 +p4 input.conf` | `input.conf`, `topology`, `coordinates`, `parameters`, `and restart files referenced by it` |

## Supported task families
- minimization.
- heating.
- equilibration.
- production MD.
- free-energy protocols.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.ks.uiuc.edu/Research/namd/3.0/ug/
- https://www.ks.uiuc.edu/Training/Tutorials/namd/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
