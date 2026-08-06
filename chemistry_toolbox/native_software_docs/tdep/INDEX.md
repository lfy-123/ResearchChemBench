---
software_id: tdep
versions: ["25.03 (d38f435)"]
topics: ["index", "navigation", "capabilities"]
aliases: ["TDEP", "tdep"]
inputs: ["unit-cell POSCAR", "supercell POSCAR", "packed simulation HDF5", "fitted force constants"]
outputs: ["effective force constants", "thermal configurations", "phonon dispersion and HDF5 data"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# TDEP Native Software Guide

## Installed software
- Installed version: `25.03 (d38f435)`.
- Operational status: `runnable`.
- Configured runtime: `tdep`.
- Primary use: fit and analyze temperature-dependent effective lattice-dynamical models.

## When to use this interface
Fit temperature-dependent effective force constants, sample canonical configurations, or calculate phonons from explicit TDEP files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `extract_forceconstants` | `fixed_files` | `extract_forceconstants -rc2 5.0` | `infile.ucposcar`, `infile.ssposcar`, `infile.sim.hdf5` |
| `canonical_configuration` | `fixed_files` | `canonical_configuration --nconf 10 --temperature 300 --quantum` | `infile.ucposcar`, `infile.ssposcar`, `infile.forceconstant` |
| `phonon_dispersion_relations` | `fixed_files` | `phonon_dispersion_relations --unit thz -nq 100` | `infile.ucposcar`, `infile.forceconstant` |

## Supported task families
- effective force-constant fitting.
- canonical thermal sampling.
- phonon dispersion.
- vibrational thermodynamics.
- thermal transport.

## Layer 1 typed Actions
- `fit_effective_force_constants`.
- `generate_thermal_displacement_configurations`.
- `calculate_temperature_dependent_phonon_dispersion`.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://tdep-developers.github.io/tdep/
- https://github.com/tdep-developers/tdep/blob/25.03/INSTALL.md

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
