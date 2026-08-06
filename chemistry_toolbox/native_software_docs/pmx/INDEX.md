---
software_id: pmx
versions: ["0+untagged.1.g0dd5f0a"]
topics: ["index", "navigation", "capabilities"]
aliases: ["pmx", "pmx"]
inputs: ["hydrogen-complete PDB or GRO", "GROMACS TOP or ITP", "ligand PDB pairs", "XVG work files"]
outputs: ["hybrid structures", "hybrid topologies", "atom-pair maps", "mapping scores", "free-energy estimates"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# pmx Native Software Guide

## Installed software
- Installed version: `0+untagged.1.g0dd5f0a`.
- Operational status: `runnable_pinned_development_version`.
- Configured runtime: `pmx`.
- Primary use: prepare and analyze explicitly defined GROMACS alchemical transformations.

## When to use this interface
Prepare explicit alchemical mutations and hybrid topologies, map ligand atoms, or analyze supplied nonequilibrium work data. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `pmx` | `arguments` | `pmx mutate -f protein.pdb -o hybrid.pdb -ff amber99sb-star-ildn-mut --script mutations.txt` | `protein.pdb`, `mutations.txt` |

## Supported task families
- protein DNA and RNA mutation.
- B-state hybrid topology generation.
- ligand atom mapping.
- nonequilibrium work analysis.

## Layer 1 typed Actions
- `mutate_biomolecular_residues_for_alchemy`.
- `generate_alchemical_hybrid_topology`.
- `map_alchemical_ligand_atoms`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://degrootlab.github.io/pmx/
- https://github.com/deGrootLab/pmx

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
