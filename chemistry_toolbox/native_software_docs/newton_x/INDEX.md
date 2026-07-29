---
software_id: newton_x
versions: ["26a"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Newton-X", "newton x"]
inputs: ["control files", "initial conditions", "geometry", "electronic-structure interface files"]
outputs: ["TRAJ directories", "dynamics logs", "populations", "geometries", "test reports"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Newton-X Native Software Guide

## Installed software
- Installed version: `26a`.
- Operational status: `workflow_with_electronic_structure`.
- Configured runtime: `newtonx`.
- Primary use: nonadiabatic dynamics or initial-condition generation with a configured electronic-structure interface.

## When to use this interface
Generate and run Newton-X nonadiabatic dynamics from Agent-authored control files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `nx_geninp` | `arguments_or_stdin` | `nx_geninp` | None |
| `nx_moldyn` | `fixed_files` | `nx_moldyn` | None |
| `nx_test` | `arguments` | `nx_test 1` | None |

## Supported task families
- initial-condition generation.
- surface hopping.
- spectrum simulation.
- trajectory analysis.
- installation tests.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://newtonx.org/documentation/
- https://github.com/light-and-molecules/newtonx

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
