---
software_id: sisso
versions: ["3.5 (bc18cae)"]
topics: ["index", "navigation", "capabilities"]
aliases: ["SISSO", "sisso"]
inputs: ["SISSO.in", "train.dat", "optional SISSO.out and predict.dat for evaluation"]
outputs: ["SISSO.out", "Models", "SIS_subspaces", "predict_X.out", "predict_Y.out"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SISSO Native Software Guide

## Installed software
- Installed version: `3.5 (bc18cae)`.
- Operational status: `runnable_pinned_source_build`.
- Configured runtime: `sisso`.
- Primary use: discover low-dimensional sparse analytical descriptors by feature construction, sure independence screening and sparsifying operators.

## When to use this interface
Discover sparse symbolic regression descriptors from Agent-authored SISSO inputs or evaluate an existing model with the matching official predictor. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `SISSO` | `fixed_files` | `SISSO` | `SISSO.in`, `train.dat` |
| `SISSO_predict` | `fixed_files` | `SISSO_predict` | `SISSO.out`, `predict.dat`, `SISSO_predict_para` |

## Supported task families
- symbolic regression.
- descriptor discovery.
- sparse model selection.
- multitask learning.
- classification.
- held-out prediction.

## Layer 1 typed Actions
- `discover_sparse_symbolic_descriptor`.
- `evaluate_sparse_symbolic_descriptor`.
- `summarize_sparse_symbolic_descriptor_results`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://github.com/rouyang2017/SISSO
- https://github.com/rouyang2017/SISSO/blob/master/SISSO_Guide_v3.5.pdf
- https://github.com/rouyang2017/SISSO/pull/76

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
