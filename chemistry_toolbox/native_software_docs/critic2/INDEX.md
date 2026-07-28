---
software_id: critic2
versions: ["installed build"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Critic2", "critic2"]
inputs: ["input.cri", "structure file", "density or wavefunction field"]
outputs: ["stdout.log", "critical-point tables", "basin integrations", "optional grids"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# Critic2 Native Software Guide

## Installed software
- Installed version: `installed build`.
- Operational status: `runnable_with_field_data`.
- Configured runtime: `critic2`.
- Primary use: topological analysis of an electron-density field.

## When to use this interface
Run Critic2 topology and field analysis from an Agent-authored native input. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `critic2` | `arguments` | `critic2 input.cri` | `input.cri`, `field/structure files referenced by input.cri` |

## Supported task families
- critical-point search.
- basin integration.
- noncovalent interaction analysis.
- crystal-field analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://aoterodelaroza.github.io/critic2/manual/
- https://github.com/aoterodelaroza/critic2

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
