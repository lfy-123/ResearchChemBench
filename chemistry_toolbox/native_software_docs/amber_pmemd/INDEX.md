---
software_id: amber_pmemd
versions: ["26"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Amber PMEMD", "amber pmemd"]
inputs: ["mdin", "topology.prmtop", "input.rst7"]
outputs: ["mdout", "output.rst7", "trajectory.nc", "mdinfo"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Amber PMEMD Native Software Guide

## Installed software
- Installed version: `26`.
- Operational status: `runnable_serial_and_mpi`.
- Configured runtime: `amber`.
- Primary use: classical molecular dynamics or minimization from prepared Amber topology and restart files.

## When to use this interface
Execute Amber PMEMD serial or MPI molecular dynamics from explicit control/topology/state files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `pmemd` | `arguments` | `pmemd -O -i mdin -o mdout -p topology.prmtop -c input.rst7 -r output.rst7 -x trajectory.nc` | `mdin`, `topology.prmtop`, `input.rst7` |
| `pmemd.MPI` | `arguments` | `pmemd.MPI -O -i mdin -o mdout -p topology.prmtop -c input.rst7 -r output.rst7 -x trajectory.nc` | `mdin`, `topology.prmtop`, `input.rst7` |

## Supported task families
- energy minimization.
- heating.
- NVT dynamics.
- NPT dynamics.
- restart continuation.

## Layer 1 typed Actions
- `minimize_system_energy`.
- `propagate_dynamics`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://ambermd.org/Manuals.php
- https://ambermd.org/tutorials/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
