---
software_id: yambo
versions: ["5.3.0"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Yambo", "yambo"]
inputs: ["compatible upstream save database", "SAVE directory", "input.in", "optional restart databases"]
outputs: ["SAVE database", "report", "output data files", "restart databases"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# Yambo Native Software Guide

## Installed software
- Installed version: `5.3.0`.
- Operational status: `runnable_with_upstream_database`.
- Configured runtime: `yambo`.
- Primary use: many-body perturbation or response calculation from a converted ground-state database.

## When to use this interface
Convert compatible upstream databases and run Agent-authored Yambo MBPT/GW/BSE calculations. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `p2y` | `arguments` | `p2y` | `compatible upstream electronic-structure save database` |
| `yambo` | `arguments` | `yambo -F input.in -J job` | `input.in`, `SAVE database`, `and required restart databases` |

## Supported task families
- database conversion.
- GW.
- Bethe-Salpeter equation.
- optical spectra.
- real-time propagation.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://wiki.yambo-code.eu/wiki/index.php/Main_Page
- https://github.com/yambo-code/yambo

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
