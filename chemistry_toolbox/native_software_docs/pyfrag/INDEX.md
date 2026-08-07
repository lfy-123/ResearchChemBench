---
software_id: pyfrag
versions: ["2019.02 (v1.0.0 af2a122d)"]
topics: ["index", "navigation", "capabilities"]
aliases: ["PyFrag", "pyfrag"]
inputs: ["PyFrag input specification", "AMV or multi-XYZ reaction path", "explicit fragment partitions and reference energies", "ORCA method keywords"]
outputs: ["fragment_energies.txt", "fragment ORCA outputs", "structured activation-strain summary and validation"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# PyFrag Native Software Guide

## Installed software
- Installed version: `2019.02 (v1.0.0 af2a122d)`.
- Operational status: `runnable_pinned_patched_source`.
- Configured runtime: `reaction`.
- Primary use: calculate activation-strain analysis profiles from explicitly supplied molecular reaction paths using ORCA single-point energies.

## When to use this interface
Calculate an activation-strain profile from an explicit reaction path and explicit ORCA/fragment settings. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `pyfrag-orca` | `arguments` | `pyfrag-orca pyfrag.inp scratch` | `pyfrag.inp`, `reaction_path.amv` |

## Supported task families
- activation strain model.
- distortion interaction analysis.
- reaction path energy decomposition.
- fragment strain analysis.

## Layer 1 typed Actions
- `analyze_activation_strain_profile`.
- `summarize_activation_strain_profile`.
- `validate_activation_strain_profile`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://pyfragdocument.readthedocs.io/en/latest/
- https://pyfragdocument.readthedocs.io/en/latest/install.html
- https://github.com/TheoChem-VU/PyFrag

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
