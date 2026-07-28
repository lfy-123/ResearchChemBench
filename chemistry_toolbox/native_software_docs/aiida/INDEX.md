---
software_id: aiida
versions: ["2.8.0"]
topics: ["index", "navigation", "capabilities"]
aliases: ["AiiDA", "aiida"]
inputs: ["configured AiiDA profile", "database", "broker or core profile", "workflow script"]
outputs: ["AiiDA database nodes", "process records", "repository objects", "optional archive.aiida"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# AiiDA Native Software Guide

## Installed software
- Installed version: `2.8.0`.
- Operational status: `interface_only`.
- Configured runtime: `workflows`.
- Primary use: provenance-tracked workflow orchestration through a configured AiiDA profile.

## When to use this interface
Inspect and operate the configured AiiDA profile with explicit verdi subcommands. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `verdi` | `arguments` | `verdi status` | `subcommand-specific files` |

## Supported task families
- profile inspection.
- code registration.
- process submission.
- process monitoring.
- archive export.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://aiida.readthedocs.io/projects/aiida-core/en/stable/reference/command_line.html
- https://aiida.readthedocs.io/projects/aiida-core/en/stable/howto/run_codes.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
