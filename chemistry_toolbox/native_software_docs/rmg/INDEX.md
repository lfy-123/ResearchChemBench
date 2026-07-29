---
software_id: rmg
versions: ["installed RMG runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["RMG-Py", "rmg"]
inputs: ["input.py", "RMG database", "optional seed mechanisms and libraries"]
outputs: ["chemkin files", "species dictionary", "RMG log", "HTML report", "restart data"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# RMG-Py Native Software Guide

## Installed software
- Installed version: `installed RMG runtime`.
- Operational status: `workflow_with_database`.
- Configured runtime: `rmg`.
- Primary use: automatic reaction-mechanism generation using an installed RMG database.

## When to use this interface
Generate reaction mechanisms from a complete Agent-authored RMG-Py input file. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `rmg.py` | `arguments` | `rmg.py input.py` | `input.py` |

## Supported task families
- gas-phase mechanism generation.
- liquid-phase mechanism generation.
- sensitivity.
- model enlargement.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://reactionmechanismgenerator.github.io/RMG-Py/users/rmg/index.html
- https://reactionmechanismgenerator.github.io/RMG-Py/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
