---
software_id: theodore
versions: ["installed TheoDORE runtime"]
topics: ["index", "navigation", "capabilities"]
aliases: ["TheoDORE", "theodore"]
inputs: ["dens_ana.in or subcommand input", "excited-state output", "orbital and density files"]
outputs: ["summary tables", "charge-transfer matrices", "NTO files", "spectra and plots"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# TheoDORE Native Software Guide

## Installed software
- Installed version: `installed TheoDORE runtime`.
- Operational status: `runnable_with_excited_state_data`.
- Configured runtime: `theodore`.
- Primary use: analyze transition densities, charge transfer, and excited-state character from supported electronic-structure results.

## When to use this interface
Run TheoDORE excited-state and transition-density analyses from explicit subcommands and quantum-chemistry files. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `theodore` | `arguments` | `theodore analyze_tden -f dens_ana.in` | `subcommand-specific excited-state`, `orbital`, `or density files` |

## Supported task families
- transition-density analysis.
- charge-transfer numbers.
- natural transition orbitals.
- spectrum analysis.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://theodore-qc.sourceforge.io/docs/
- https://github.com/felixplasser/theodore-qc

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
