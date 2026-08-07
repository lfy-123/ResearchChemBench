---
software_id: acpype
versions: ["2023.10.27"]
topics: ["index", "navigation", "capabilities"]
aliases: ["ACPYPE", "acpype"]
inputs: ["PDB MOL2 or MDL molecular structure", "or matching prmtop and inpcrd files"]
outputs: ["AMBER prmtop and inpcrd", "GROMACS top itp and gro", "optional CNS or CHARMM files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# ACPYPE Native Software Guide

## Installed software
- Installed version: `2023.10.27`.
- Operational status: `runnable`.
- Configured runtime: `acpype`.
- Primary use: generate GAFF-family molecular topologies and convert AMBER topology-coordinate pairs to GROMACS.

## When to use this interface
Generate GAFF-family molecular topologies or convert an existing AMBER topology/coordinate pair to GROMACS. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `acpype` | `arguments` | `acpype -i input.mol2 -b molecule -n 0 -m 1 -c gas -a gaff2 -q sqm -o gmx` | `input.mol2` |

## Supported task families
- small-molecule parameterization.
- GAFF and GAFF2 atom typing.
- AMBER topology generation.
- AMBER-to-GROMACS conversion.

## Layer 1 typed Actions
- `generate_small_molecule_topology`.
- `convert_amber_topology_to_gromacs`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://acpype.readthedocs.io/
- https://github.com/alanwilter/acpype

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
