---
software_id: mess
versions: ["2020.1.24"]
topics: ["index", "navigation", "capabilities"]
aliases: ["MESS", "mess"]
inputs: ["input.inp", "optional external molecular or energy-transfer data"]
outputs: ["rate.out", "auxiliary diagnostic and eigenvalue files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# MESS Native Software Guide

## Installed software
- Installed version: `2020.1.24`.
- Operational status: `runnable`.
- Configured runtime: `mess`.
- Primary use: master-equation rate calculation from a complete MESS input model.

## When to use this interface
Solve an Agent-authored MESS master-equation model. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `mess` | `arguments` | `mess input.inp` | `input.inp` |

## Supported task families
- temperature-dependent rates.
- pressure dependence.
- well reduction.
- microcanonical kinetics.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://tcg.cse.anl.gov/papr/codes/mess.html
- https://github.com/Auto-Mech/MESS

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
