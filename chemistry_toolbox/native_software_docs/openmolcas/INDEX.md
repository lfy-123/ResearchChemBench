---
software_id: openmolcas
versions: ["25.10"]
topics: ["index", "navigation", "capabilities"]
aliases: ["OpenMolcas", "openmolcas"]
inputs: ["input.inp"]
outputs: ["stdout.log", "HDF5 and orbital files", "geometry and property files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# OpenMolcas Native Software Guide

## Installed software
- Installed version: `25.10`.
- Operational status: `runnable`.
- Configured runtime: `openmolcas`.
- Primary use: multiconfigurational molecular electronic-structure calculation.

## When to use this interface
Execute an Agent-authored OpenMolcas input deck for multireference and spectroscopy calculations. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `pymolcas` | `arguments` | `pymolcas input.inp` | `input.inp` |

## Supported task families
- SCF.
- RASSCF or CASSCF.
- CASPT2.
- geometry optimization.
- frequency.
- spectroscopy.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://molcas.gitlab.io/OpenMolcas/sphinx/
- https://gitlab.com/Molcas/OpenMolcas

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
