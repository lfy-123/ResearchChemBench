---
software_id: automekin
versions: ["AutoMeKin2021 revision 1142"]
topics: ["index", "navigation", "capabilities"]
aliases: ["AutoMeKin", "automekin"]
inputs: ["AutoMeKin control file", "starting structure", "method-specific resources"]
outputs: ["reaction network", "transition-state structures", "product structures", "component logs"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# AutoMeKin Native Software Guide

## Installed software
- Installed version: `AutoMeKin2021 revision 1142`.
- Operational status: `workflow_with_components`.
- Configured runtime: `automekin`.
- Primary use: automated reaction discovery using configured electronic-structure components.

## When to use this interface
Invoke individual AutoMeKin and bundled MOPAC entry points from explicit native inputs. The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.

## Documentation map
- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.
- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.
- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.
- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.
- Additional topic files in this directory contain software-specific scientific mechanics where available.

## Supported command entries
| Executable | Input mode | Native invocation | Required staged inputs |
|---|---|---|---|
| `amk.sh` | `arguments` | `amk.sh input.dat` | `input.dat` |
| `mopac` | `arguments` | `mopac input.mop` | `input.mop` |
| `bbfs.exe` | `arguments` | `bbfs.exe` | None |

## Supported task families
- trajectory sampling.
- transition-state search.
- reaction-network construction.
- MOPAC component jobs.

## Required knowledge before submission
The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.

## Official references
- https://rxnkin.usc.es/index.php/automekin/
- https://github.com/emartineznunez/AutoMeKin

## Test interpretation
An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.
