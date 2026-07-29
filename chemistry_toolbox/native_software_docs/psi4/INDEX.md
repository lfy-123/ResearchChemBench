---
software_id: psi4
versions: ["1.11"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Psi4", "psi4"]
inputs: ["input.dat"]
outputs: ["output.dat", "optional molecule", "wavefunction", "cube", "and scratch files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Psi4 Native Software Guide

## Installed software
- Installed version: `1.11`.
- Operational status: `runnable`.
- Configured runtime: `psi4`.
- Primary use: molecular electronic-structure calculation from a Psi4 input file.

## When to use this interface
Execute a complete Agent-authored Psi4 input file. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `psi4` | `arguments` | `psi4 input.dat output.dat -n 4` | `input.dat` |

## Supported task families
- single point.
- optimization.
- frequency.
- SAPT.
- excited states.
- properties.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://psicode.org/psi4manual/master/
- https://psicode.org/psi4manual/master/psithoninput.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
