---
software_id: deepmd
versions: ["3.2.0b0"]
topics: ["index", "navigation", "capabilities"]
aliases: ["DeePMD-kit", "deepmd"]
inputs: ["training JSON or YAML", "DeepMD dataset", "optional checkpoint or frozen model"]
outputs: ["training logs", "checkpoints", "frozen model", "test metrics"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# DeePMD-kit Native Software Guide

## Installed software
- Installed version: `3.2.0b0`.
- Operational status: `interface_only_without_dataset`.
- Configured runtime: `deepmd`.
- Primary use: train, freeze, test, or compress a deep potential model.

## When to use this interface
Invoke a specific DeePMD-kit command selected by the Agent. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `dp` | `arguments` | `dp test -m model.pb -s test_data` | `subcommand-specific Agent-authored input and data files` |

## Supported task families
- training.
- model freezing.
- model testing.
- model compression.
- dataset conversion.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://docs.deepmodeling.com/projects/deepmd/en/master/
- https://github.com/deepmodeling/deepmd-kit

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
