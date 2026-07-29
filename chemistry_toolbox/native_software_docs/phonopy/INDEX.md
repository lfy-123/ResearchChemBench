---
software_id: phonopy
versions: ["installed phonons runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Phonopy", "phonopy"]
inputs: ["unit cell", "displacement YAML", "force data", "optional Born charges"]
outputs: ["supercells", "phonopy_disp.yaml", "FORCE_SETS", "force_constants.hdf5", "band and DOS YAML"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Phonopy Native Software Guide

## Installed software
- Installed version: `installed phonons runtime`.
- Operational status: `runnable`.
- Configured runtime: `phonons`.
- Primary use: generate harmonic displacements or analyze phonons from completed force calculations.

## When to use this interface
Invoke an explicit Phonopy command for displacement generation, force-constant construction, or phonon analysis. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `phonopy` | `arguments` | `phonopy --dim 2 2 2 -d --vasp POSCAR` | `force` |

## Supported task families
- displacement generation.
- force-constant construction.
- band structure.
- DOS.
- thermal properties.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://phonopy.github.io/phonopy/
- https://github.com/phonopy/phonopy

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
