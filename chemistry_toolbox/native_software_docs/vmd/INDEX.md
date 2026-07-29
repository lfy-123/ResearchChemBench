---
software_id: vmd
versions: ["1.9.3"]
topics: ["index", "navigation", "capabilities"]
aliases: ["VMD", "vmd"]
inputs: ["analysis.tcl", "referenced structures and trajectories"]
outputs: ["stdout.log", "user-defined tables", "structures", "images when rendering is configured"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# VMD Native Software Guide

## Installed software
- Installed version: `1.9.3`.
- Operational status: `runnable_headless`.
- Configured runtime: `vmd`.
- Primary use: headless Tcl-based structure or trajectory analysis.

## When to use this interface
Run an Agent-authored VMD/Tcl trajectory, structure, selection, measurement, or rendering script in text mode. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `vmd` | `arguments` | `vmd -dispdev text -e analysis.tcl` | `analysis.tcl` |

## Supported task families
- structure inspection.
- trajectory analysis.
- atom selections.
- measurements.
- scripted export.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://www.ks.uiuc.edu/Research/vmd/current/ug/
- https://www.ks.uiuc.edu/Research/vmd/script_library/

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
