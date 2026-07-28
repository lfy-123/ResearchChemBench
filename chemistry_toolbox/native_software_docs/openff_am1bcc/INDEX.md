---
software_id: openff_am1bcc
versions: ["AmberTools runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["AmberTools antechamber and sqm", "openff am1bcc"]
inputs: ["input.mol2 or another supported molecule", "explicit charge and multiplicity"]
outputs: ["charged.mol2", "ANTECHAMBER files", "sqm.in", "sqm.out"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# AmberTools antechamber and sqm Native Software Guide

## Installed software
- Installed version: `AmberTools runtime`.
- Operational status: `runnable`.
- Configured runtime: `openff`.
- Primary use: assign AM1-BCC charges and prepare a small-molecule Amber-compatible representation.

## When to use this interface
Run AmberTools charge-generation components used by explicit OpenFF/AM1-BCC preparation. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `antechamber` | `arguments` | `antechamber -i input.mol2 -fi mol2 -o charged.mol2 -fo mol2 -c bcc -nc 0` | `molecular input file` |
| `sqm` | `arguments` | `sqm -O -i sqm.in -o sqm.out` | `sqm.in` |

## Supported task families
- AM1-BCC charging.
- GAFF atom typing.
- SQM semiempirical calculation.
- MOL2 conversion.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://ambermd.org/AmberTools.php
- https://ambermd.org/Manuals.php

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
