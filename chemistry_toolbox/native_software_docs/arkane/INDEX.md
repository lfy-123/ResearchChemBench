---
software_id: arkane
versions: ["RMG environment"]
topics: ["index", "navigation", "capabilities"]
aliases: ["Arkane", "arkane"]
inputs: ["input.py", "species files", "transition-state files", "quantum-chemistry logs"]
outputs: ["output.py", "chem.inp", "supporting_information.csv", "plots"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Arkane Native Software Guide

## Installed software
- Installed version: `RMG environment`.
- Operational status: `runnable_with_quantum_outputs`.
- Configured runtime: `rmg`.
- Primary use: statistical mechanics and pressure-dependent kinetics from validated quantum-chemistry results.

## When to use this interface
Run Arkane thermochemistry, kinetics, pressure-dependence, or statmech jobs from a complete input file. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `Arkane.py` | `arguments` | `Arkane.py input.py` | `input.py` |

## Supported task families
- thermochemistry.
- transition-state theory.
- rotor treatment.
- pressure dependence.
- sensitivity analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://reactionmechanismgenerator.github.io/RMG-Py/users/arkane/index.html
- https://reactionmechanismgenerator.github.io/RMG-Py/reference/arkane/index.html

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
