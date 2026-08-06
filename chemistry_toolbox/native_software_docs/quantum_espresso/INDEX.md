---
software_id: quantum_espresso
versions: ["7.5"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Quantum ESPRESSO pw.x", "quantum espresso"]
inputs: ["input.in", "one pseudopotential per species"]
outputs: ["stdout.log", "prefix.save database", "charge density", "wavefunctions", "relaxed structure"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Quantum ESPRESSO pw.x Native Software Guide

## Installed software
- Installed version: `7.5`.
- Operational status: `runnable_with_pseudopotentials`.
- Configured runtime: `qe`.
- Primary use: periodic plane-wave SCF, relaxation, or molecular dynamics calculation.

## When to use this interface
Execute an Agent-authored Quantum ESPRESSO pw.x input deck. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `pw.x` | `arguments` | `pw.x -in input.in` | `input.in` |

## Supported task families
- scf.
- nscf.
- bands.
- relax.
- vc-relax.
- molecular dynamics.

## Layer 1 typed Actions
- `calculate_periodic_energy`.
- `calculate_periodic_forces`.
- `calculate_periodic_stress`.
- `relax_periodic_structure`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.quantum-espresso.org/Doc/INPUT_PW.html
- https://www.quantum-espresso.org/documentation/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
