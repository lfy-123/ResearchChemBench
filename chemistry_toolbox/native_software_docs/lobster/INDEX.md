---
software_id: lobster
versions: ["5.1.0"]
topics: ["index", "navigation", "capabilities"]
aliases: ["LOBSTER", "lobster"]
inputs: ["lobsterin", "POSCAR", "POTCAR", "WAVECAR", "CONTCAR", "KPOINTS", "OUTCAR", "vasprun.xml"]
outputs: ["lobsterout", "COHPCAR.lobster", "ICOHPLIST.lobster", "DOSCAR.lobster", "CHARGE.lobster"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# LOBSTER Native Software Guide

## Installed software
- Installed version: `5.1.0`.
- Operational status: `runnable_with_vasp_upstream`.
- Configured runtime: `lobster`.
- Primary use: chemical-bonding projection from a compatible completed VASP calculation.

## When to use this interface
Analyze bonding from compatible electronic-structure outputs using a native LOBSTER input. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `lobster-5.1.0` | `fixed_files` | `lobster-5.1.0` | `lobsterin`, `POSCAR`, `POTCAR`, `WAVECAR`, `CONTCAR`, `KPOINTS`, `OUTCAR`, `vasprun.xml` |

## Supported task families
- COHP.
- COOP.
- COBI.
- projected DOS.
- charge analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.cohp.de/
- https://lobsterpy.readthedocs.io/en/latest/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
