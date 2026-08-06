---
software_id: vasp
versions: ["6.3.2"]
topics: ["index", "navigation", "capabilities"]
aliases: ["VASP", "vasp"]
inputs: ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
outputs: ["OUTCAR", "vasprun.xml", "OSZICAR", "CONTCAR", "WAVECAR", "CHGCAR"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# VASP Native Software Guide

## Installed software
- Installed version: `6.3.2`.
- Operational status: `runnable_licensed`.
- Configured runtime: `vasp`.
- Primary use: periodic plane-wave electronic-structure calculation from fixed-name VASP inputs.

## When to use this interface
Execute a VASP calculation from the standard Agent-prepared input set. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `vasp_std` | `fixed_files` | `vasp_std` | `INCAR`, `POSCAR`, `POTCAR`, `KPOINTS` |

## Supported task families
- single point.
- relaxation.
- cell relaxation.
- static DOS.
- bands.
- molecular dynamics.
- frequency.

## Layer 1 typed Actions
- `calculate_periodic_energy`.
- `calculate_periodic_forces`.
- `calculate_periodic_stress`.
- `relax_periodic_structure`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.vasp.at/wiki/index.php/The_VASP_Manual
- https://www.vasp.at/wiki/index.php/Category:Calculation

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
