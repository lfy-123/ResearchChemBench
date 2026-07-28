---
software_id: phono3py
versions: ["installed phonons runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["phono3py", "phono3py"]
inputs: ["unit cell", "displacement configuration", "force data", "optional Born charges"]
outputs: ["supercell displacement structures", "phono3py_disp.yaml", "fc2.hdf5", "fc3.hdf5", "kappa files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# phono3py Native Software Guide

## Installed software
- Installed version: `installed phonons runtime`.
- Operational status: `runnable_with_force_data`.
- Configured runtime: `phonons`.
- Primary use: generate third-order displacements or compute lattice thermal conductivity from force data.

## When to use this interface
Invoke an explicit Phono3py command for third-order force constants and lattice thermal transport. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `phono3py` | `arguments` | `phono3py --dim 2 2 2 -d --pa auto POSCAR` | `mode-specific structure`, `displacement`, `force`, `and configuration files` |

## Supported task families
- third-order displacement generation.
- force-set creation.
- phonon lifetimes.
- thermal conductivity.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://phonopy.github.io/phono3py/
- https://github.com/phonopy/phono3py

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
