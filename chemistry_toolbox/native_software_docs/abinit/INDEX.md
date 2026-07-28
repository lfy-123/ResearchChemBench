---
software_id: abinit
versions: ["10.0.3"]
topics: ["index", "navigation", "capabilities"]
aliases: ["ABINIT", "abinit"]
inputs: ["run.abi", "one pseudopotential per element"]
outputs: ["run.abo", "run.o_WFK", "run.o_DEN", "stdout.log", "stderr.log"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# ABINIT Native Software Guide

## Installed software
- Installed version: `10.0.3`.
- Operational status: `runnable`.
- Configured runtime: `abinit`.
- Primary use: periodic ground-state total-energy calculation.

## When to use this interface
Execute a complete ABINIT input deck. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `abinit` | `arguments` | `abinit input.abi` | `input.abi`, `pseudopotentials and files referenced by it` |

## Supported task families
- ground-state SCF.
- geometry optimization.
- band structure.
- density of states.
- DFPT.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://docs.abinit.org/guide/abinit/
- https://docs.abinit.org/tutorial/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
