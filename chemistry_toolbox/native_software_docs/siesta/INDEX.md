---
software_id: siesta
versions: ["5.4.2"]
topics: ["index", "navigation", "capabilities"]
aliases: ["SIESTA", "siesta"]
inputs: ["input.fdf", "pseudopotential files", "optional included structure and basis files", "device and electrode Hamiltonians for transport"]
outputs: ["stdout.log", ".XV", ".DM", ".WFSX", ".bands", ".DOS and trajectory files", "transport Hamiltonians and configured transmission or current outputs"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SIESTA Native Software Guide

## Installed software
- Installed version: `5.4.2`.
- Operational status: `runnable_with_pseudopotentials`.
- Configured runtime: `periodic`.
- Primary use: localized-basis DFT and integrated TranSIESTA from FDF input; TBtrans native postprocessing of linked Hamiltonians.

## When to use this interface
Execute SIESTA including integrated TranSIESTA, or TBtrans postprocessing from explicit native input. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `siesta` | `stdin_file` | `siesta` | `input.fdf` |
| `tbtrans` | `stdin_file` | `tbtrans` | `input.fdf` |

## Supported task families
- single point.
- geometry optimization.
- molecular dynamics.
- bands.
- DOS.
- transport preparation.
- integrated TranSIESTA.
- TBtrans postprocessing.

## Layer 1 typed Actions
- `calculate_periodic_energy`.
- `calculate_periodic_forces`.
- `relax_periodic_structure`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://docs.siesta-project.org/projects/siesta/en/stable/reference/siesta.html
- https://docs.siesta-project.org/projects/siesta/en/stable/reference/tbtrans.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
