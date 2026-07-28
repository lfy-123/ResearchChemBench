---
software_id: qcengine
versions: ["0.50.0"]
topics: ["index", "navigation", "capabilities"]
aliases: ["QCEngine", "qcengine"]
inputs: ["QCSchema JSON", "selected program name"]
outputs: ["QCSchema result JSON", "structured error record", "provenance"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# QCEngine Native Software Guide

## Installed software
- Installed version: `0.50.0`.
- Operational status: `runnable_with_program`.
- Configured runtime: `workflows`.
- Primary use: execute a QCSchema AtomicInput or procedure with an installed backend program.

## When to use this interface
Invoke the QCEngine command-line interface on an Agent-authored QCSchema input and explicitly selected program. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `qcengine` | `arguments` | `qcengine run <program> input.json` | `QCSchema AtomicInput or procedure input JSON` |

## Supported task families
- single computation.
- gradient.
- Hessian.
- optimization procedure.
- program discovery.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://molssi.github.io/QCEngine/
- https://molssi.github.io/QCEngine/cli.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
