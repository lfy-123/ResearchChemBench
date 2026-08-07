---
software_id: pdb_tools
versions: ["installed Python package"]
topics: ["index", "navigation", "capabilities"]
aliases: ["pdb-tools", "pdb tools"]
inputs: ["input.pdb"]
outputs: ["stdout PDB stream or redirected PDB file"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# pdb-tools Native Software Guide

## Installed software
- Installed version: `installed Python package`.
- Operational status: `runnable`.
- Configured runtime: `core`.
- Primary use: deterministic line-oriented cleanup and selection of PDB records.

## When to use this interface
Apply individual pdb-tools text transformations to PDB records. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `pdb_selchain` | `arguments` | `pdb_selchain -A input.pdb` | `input.pdb` |
| `pdb_reres` | `arguments` | `pdb_reres -1 input.pdb` | `input.pdb` |
| `pdb_tidy` | `arguments` | `pdb_tidy input.pdb` | `input.pdb` |

## Supported task families
- chain selection.
- residue renumbering.
- record tidying.
- atom and residue filtering.

## Layer 1 typed Actions
- `select_structure_subset`.
- `renumber_biomolecular_structure`.
- `normalize_pdb_records`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.bonvinlab.org/pdb-tools/
- https://github.com/haddocking/pdb-tools

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
