---
software_id: nequip
versions: ["installed NequIP runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["NequIP", "nequip"]
inputs: ["config.yaml", "training and validation dataset", "optional checkpoint"]
outputs: ["training log", "checkpoints", "metrics", "packaged model"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# NequIP Native Software Guide

## Installed software
- Installed version: `installed NequIP runtime`.
- Operational status: `interface_only_without_dataset`.
- Configured runtime: `nequip`.
- Primary use: train or deploy an equivariant interatomic potential from a curated dataset.

## When to use this interface
Train a NequIP model from a complete Agent-authored configuration. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `nequip-train` | `arguments` | `nequip-train -cn config` | `config.yaml` |

## Supported task families
- training.
- validation.
- model packaging.
- inference.
- LAMMPS deployment.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://nequip.readthedocs.io/en/latest/
- https://github.com/mir-group/nequip

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
