---
software_id: fcclasses3
versions: ["3.0.4"]
topics: ["index", "navigation", "capabilities"]
aliases: ["FCclasses3", "fcclasses3"]
inputs: ["FCclasses3 input file", "state files", "Hessian/normal-mode files", "dipole files"]
outputs: ["spectrum data", "rate constants", "convergence/diagnostic stdout", "requested intermediate files"]
last_smoke_tested: null
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# FCclasses3 Native Software Guide

## Installed software
- Installed version: `3.0.4`.
- Operational status: `runnable_local_user_supplied`.
- Configured runtime: `quantum`.
- Primary use: vibronic electronic spectra and non-radiative-rate calculations from explicit state, dipole, and vibrational inputs.

## When to use this interface
Run an explicitly authored FCclasses3 vibronic-spectrum or non-radiative-rate calculation from complete state, dipole, and vibrational inputs. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `fcclasses3` | `arguments` | `fcclasses3 input.fcc` | `input.fcc` |

## Supported task families
- Franck-Condon spectra.
- Herzberg-Teller spectra.
- fluorescence.
- absorption.
- ECD.
- intersystem-crossing rates.
- internal-conversion rates.

## Layer 1 typed Actions
- No typed Action is registered. Use the reviewed native command layer or the documented programmable runtime.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- http://www.iccom.cnr.it/en/fcclasses/
- https://github.com/fcclasses/fcclasses3

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
