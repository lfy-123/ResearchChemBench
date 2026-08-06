---
software_id: censo
versions: ["2.1.2"]
topics: ["index", "navigation", "capabilities"]
aliases: ["CENSO", "censo"]
inputs: ["conformers.xyz", ".censorc or explicit configuration", "selected QM executable"]
outputs: ["anmr_enso", "crest_conformers.xyz", "censo logs", "ranked ensemble"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# CENSO Native Software Guide

## Installed software
- Installed version: `2.1.2`.
- Operational status: `runnable_with_external_qm`.
- Configured runtime: `censo`.
- Primary use: multilevel energetic refinement of a CREST conformer ensemble.

## When to use this interface
Run CENSO ensemble refinement from an Agent-selected conformer ensemble and explicit settings. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `censo` | `arguments` | `censo -i conformers.xyz` | `conformers.xyz` |

## Supported task families
- prescreening.
- DFT ranking.
- thermostatistics.
- conformer sorting.

## Layer 1 typed Actions
- No typed Action is registered. Use the reviewed native command layer or the documented programmable runtime.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://xtb-docs.readthedocs.io/en/latest/CENSO_docs/censo.html
- https://github.com/grimme-lab/CENSO

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
