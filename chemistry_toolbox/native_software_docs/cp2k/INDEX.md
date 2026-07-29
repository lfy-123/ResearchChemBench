---
software_id: cp2k
versions: ["2026.1"]
topics: ["index", "navigation", "capabilities"]
aliases: ["CP2K", "cp2k"]
inputs: ["input.inp", "coordinates", "basis sets and potentials when referenced"]
outputs: ["output.out", "restart files", "trajectory files", "force files", "cube files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# CP2K Native Software Guide

## Installed software
- Installed version: `2026.1`.
- Operational status: `runnable`.
- Configured runtime: `cp2k`.
- Primary use: atomistic energy, optimization, or dynamics with Quickstep or force-field methods.

## When to use this interface
Execute a complete CP2K input deck for molecular, periodic, dynamics, spectroscopy, or other supported calculations. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `cp2k` | `arguments` | `cp2k -i input.inp -o output.out` | `input.inp` |

## Supported task families
- single point.
- geometry optimization.
- cell optimization.
- molecular dynamics.
- vibrational analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://manual.cp2k.org/trunk/
- https://www.cp2k.org/howto

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
