---
software_id: gpaw
versions: ["installed GPAW runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["GPAW", "gpaw"]
inputs: ["program.py", "optional structure and restart files", "GPAW datasets"]
outputs: ["program output", ".gpw restart", "trajectories", "property data"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# GPAW Native Software Guide

## Installed software
- Installed version: `installed GPAW runtime`.
- Operational status: `python_driver_interface`.
- Configured runtime: `gpaw`.
- Primary use: execute a GPAW Python calculation in the configured GPAW runtime.

## When to use this interface
Run an Agent-authored GPAW Python program using the GPAW command wrapper. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `gpaw` | `arguments` | `gpaw python program.py` | `program.py` |

## Supported task families
- molecular energy.
- periodic ground state.
- optimization.
- band structure.
- response properties.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://gpaw.readthedocs.io/
- https://gpaw.readthedocs.io/tutorialsexercises/index.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
