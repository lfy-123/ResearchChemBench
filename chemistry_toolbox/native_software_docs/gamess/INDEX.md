---
software_id: gamess
versions: ["2024 R2 P1"]
topics: ["index", "navigation", "capabilities"]
aliases: ["GAMESS", "gamess"]
inputs: ["job_name.inp"]
outputs: ["job_name.log", "punch file", "restart and property files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# GAMESS Native Software Guide

## Installed software
- Installed version: `2024 R2 P1`.
- Operational status: `runnable`.
- Configured runtime: `gamess`.
- Primary use: molecular electronic-structure calculation from a GAMESS input deck.

## When to use this interface
Execute a GAMESS input through the installed rungms launcher. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `rungms` | `arguments` | `rungms water 00 4` | `job_name.inp` |

## Supported task families
- single point.
- geometry optimization.
- Hessian.
- excited states.
- correlated energy.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.msg.chem.iastate.edu/gamess/documentation.html
- https://www.msg.chem.iastate.edu/gamess/GAMESS_Manual/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
