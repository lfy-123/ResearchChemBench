---
software_id: wannier90
versions: ["3.1.0 local source build"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Wannier90", "wannier90"]
inputs: ["seedname.win", "and for full runs seedname.amn", "seedname.mmn", "seedname.eig"]
outputs: ["seedname.nnkp", "seedname.wout", "seedname.chk", "interpolated data"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Wannier90 Native Software Guide

## Installed software
- Installed version: `3.1.0 local source build`.
- Operational status: `runnable_with_upstream_matrices`.
- Configured runtime: `qe`.
- Primary use: preprocess or construct maximally localized Wannier functions from an upstream electronic-structure calculation.

## When to use this interface
Preprocess and execute Wannier90 from an Agent-authored seedname.win and upstream interface files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `wannier90.x` | `arguments` | `wannier90.x -pp seedname` | None |

## Supported task families
- preprocessing.
- Wannierization.
- interpolation.
- bands.
- Berry and transport properties.

## Layer 1 typed Actions
- No typed Action is registered. Use the reviewed native command layer or the documented programmable runtime.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://wannier.org/ford/
- https://github.com/wannier-developers/wannier90

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
