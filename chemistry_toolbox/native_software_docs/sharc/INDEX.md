---
software_id: sharc
versions: ["installed source build"]
topics: ["index", "navigation", "capabilities"]
aliases: ["SHARC", "sharc"]
inputs: ["SHARC input", "initial conditions", "interface resources", "overlap input and orbital files"]
outputs: ["trajectory directories", "output.dat", "populations", "geometries", "overlap data"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SHARC Native Software Guide

## Installed software
- Installed version: `installed source build`.
- Operational status: `workflow_with_electronic_structure`.
- Configured runtime: `sharc`.
- Primary use: surface-hopping nonadiabatic dynamics with a configured electronic-structure interface.

## When to use this interface
Execute SHARC surface-hopping dynamics or wavefunction-overlap analysis from complete native inputs. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `sharc.x` | `arguments` | `sharc.x input` | None |
| `wfoverlap.x` | `stdin_file` | `wfoverlap.x` | None |

## Supported task families
- initial conditions.
- SHARC dynamics.
- wavefunction overlap.
- trajectory analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://sharc-md.org/?page_id=50
- https://github.com/sharc-md/sharc

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
