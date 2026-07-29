---
software_id: shengbte
versions: ["installed source build"]
topics: ["index", "navigation", "capabilities"]
aliases: ["ShengBTE", "shengbte"]
inputs: ["CONTROL", "FORCE_CONSTANTS_2ND", "FORCE_CONSTANTS_3RD"]
outputs: ["BTE.kappa_tensor", "BTE.omega", "BTE.v", "BTE.* diagnostic files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# ShengBTE Native Software Guide

## Installed software
- Installed version: `installed source build`.
- Operational status: `runnable_with_force_constants`.
- Configured runtime: `shengbte`.
- Primary use: solve the phonon Boltzmann transport equation from second- and third-order force constants.

## When to use this interface
Solve lattice thermal transport from an Agent-authored ShengBTE CONTROL and force constants. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `ShengBTE` | `fixed_files` | `ShengBTE` | `CONTROL`, `FORCE_CONSTANTS_2ND`, `FORCE_CONSTANTS_3RD` |

## Supported task families
- iterative thermal conductivity.
- relaxation-time approximation.
- isotope scattering.
- convergence studies.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.shengbte.org/
- https://github.com/ShengBTE/ShengBTE

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
