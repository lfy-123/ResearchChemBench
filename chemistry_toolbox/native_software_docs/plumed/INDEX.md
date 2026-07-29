---
software_id: plumed
versions: ["installed MD runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["PLUMED", "plumed"]
inputs: ["plumed.dat", "trajectory", "optional topology or masses"]
outputs: ["COLVAR", "HILLS", "grids", "stdout.log"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# PLUMED Native Software Guide

## Installed software
- Installed version: `installed MD runtime`.
- Operational status: `runnable_with_trajectory`.
- Configured runtime: `md`.
- Primary use: evaluate collective variables or biasing logic on a trajectory with plumed driver.

## When to use this interface
Run an explicit PLUMED subcommand for enhanced sampling support or trajectory analysis. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `plumed` | `arguments` | `plumed driver --plumed plumed.dat --mf_xtc trajectory.xtc` | `plumed.dat`, `trajectory.xtc` |

## Supported task families
- trajectory post-processing.
- collective variables.
- metadynamics input validation.
- restraint analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.plumed.org/doc-v2.10/user-doc/html/index.html
- https://www.plumed.org/doc-v2.10/user-doc/html/driver.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
