---
software_id: pyfrag
versions: ["2019.02 (v1.0.0 af2a122d)"]
topics: ["troubleshooting", "errors", "preflight"]
aliases: ["PyFrag", "pyfrag"]
inputs: ["PyFrag input specification", "AMV or multi-XYZ reaction path", "explicit fragment partitions and reference energies", "ORCA method keywords"]
outputs: ["fragment_energies.txt", "fragment ORCA outputs", "structured activation-strain summary and validation"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# PyFrag Troubleshooting

## Diagnose in this order
1. Confirm that `inspect_software` resolves the expected executable and version.
2. Read the first fatal message in `stderr.log` or the primary software output; later messages are often consequences.
3. Verify staged target names, input-relative paths, file encodings, line endings, and required blank sections.
4. Verify task syntax against the installed version, then check method and data compatibility.
5. Compare internal MPI, thread, memory, scratch, and GPU settings with the declared job resources.
6. Only after syntax and staging pass, investigate numerical convergence or increase resources.

## Known failures and repairs
| Symptom | Likely cause | Corrective action |
|---|---|---|
| atom_list is undefined or path filename is split into characters | unpatched Python 3 tokenization is active | apply the tracked v1.0.0 compatibility patch |
| could not convert string final to float | the legacy parser is reading an ORCA 6 Total Energy heading | apply the tracked FINAL SINGLE POINT ENERGY parser patch |
| orca not found | the separately downloaded ORCA executable is absent from PATH | restore the ORCA and matching OpenMPI cache paths |
| incomplete fragment_energies table | one or more complex or isolated-fragment calculations failed | inspect every native output and correct the explicit path method charge spin or fragment settings |

## Path and staging failures
A source file existing in the benchmark workspace does not make it visible to the native process. Every dependency must be declared in `staged_inputs`. The content of an input deck must reference the staged `target_path`, not its original workspace path. Fixed-name programs are case-sensitive. Never assume the process starts in the task workspace.

## Resource failures
The pinned standalone ORCA driver runs path points serially and launches three ORCA single points per frame. The public Action is bounded to 200 frames and one CPU core per ORCA call.
If the Supervisor reports `memory_limit_exceeded`, reduce software parallelism or request a justified larger total allocation. If it reports timeout, inspect whether the software was progressing and whether the requested task can finish within the remaining evaluation lifetime. Resource increases do not repair malformed input.

## False-success prevention
Do not accept a zero exit code when the main output contains `ERROR`, `FATAL`, an abort marker, non-convergence, or missing-result diagnostics. Likewise, do not promote an electronic convergence marker to geometry, frequency, transition-state, dynamics, or projection success. Preserve the independent status axes in the final report.

## Pre-submission checklist
- Installed executable and version inspected.
- Official syntax checked for the intended calculation family.
- Input is complete and uses English/ASCII-safe filenames where possible.
- Every referenced file is staged to the exact target name.
- stdin and argument modes match the Catalog contract.
- Charge, multiplicity, periodicity, units, atom ordering, and upstream provenance are consistent.
- CPU, total memory, per-rank/per-core memory, GPU, scratch, and walltime agree.
- `validate_native_job` returns no errors.
- Required outputs and task-specific success criteria are declared before execution.
