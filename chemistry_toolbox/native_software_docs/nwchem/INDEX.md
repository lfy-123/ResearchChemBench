---
software_id: nwchem
versions: ["installed NWChem runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["NWChem", "nwchem"]
inputs: ["input.nw", "optional basis", "geometry", "restart", "or data files"]
outputs: ["stdout.log", "database file", "movecs", "geometry and property files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# NWChem Native Software Guide

## Installed software
- Installed version: `installed NWChem runtime`.
- Operational status: `runnable`.
- Configured runtime: `nwchem`.
- Primary use: molecular or periodic electronic-structure calculation from an NWChem input deck.

## When to use this interface
Execute an Agent-authored NWChem input deck for molecular or periodic calculations supported by the installed build. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `nwchem` | `arguments` | `nwchem input.nw` | `input.nw` |

## Supported task families
- single point.
- optimization.
- frequency.
- excited states.
- molecular dynamics.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://nwchemgit.github.io/
- https://nwchemgit.github.io/Getting-Started.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
