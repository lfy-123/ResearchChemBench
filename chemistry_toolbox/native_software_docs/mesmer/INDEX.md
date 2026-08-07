---
software_id: mesmer
versions: ["7.1"]
topics: ["index", "navigation", "capabilities"]
aliases: ["MESMER", "mesmer"]
inputs: ["input.xml"]
outputs: ["output.xml", "console log", "rate tables", "optional grain and diagnostic files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# MESMER Native Software Guide

## Installed software
- Installed version: `7.1`.
- Operational status: `runnable`.
- Configured runtime: `mesmer`.
- Primary use: master-equation kinetics from an explicit molecular and reaction XML model.

## When to use this interface
Solve an Agent-authored MESMER master-equation XML model. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `mesmer` | `arguments` | `mesmer input.xml -o output.xml` | `input.xml` |

## Supported task families
- pressure-dependent rates.
- phenomenological kinetics.
- fitting.
- sensitivity analysis.

## Layer 1 typed Actions
- `solve_master_equation`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://github.com/MESMER-kinetics/MESMER-code
- https://www.chem.leeds.ac.uk/mesmer.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
