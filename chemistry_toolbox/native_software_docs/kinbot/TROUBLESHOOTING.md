---
software_id: kinbot
versions: ["2.2.2+local-nwchem-patch"]
topics: ["troubleshooting", "errors", "preflight"]
aliases: ["KinBot", "kinbot"]
inputs: ["input.json", "starting structure", "templates", "selected QM backend configuration"]
outputs: ["KinBot database", "structures", "quantum-chemistry inputs and logs", "PES files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# KinBot Troubleshooting

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
| calculator executable not found | configured Gaussian, ORCA, or other backend is unavailable | validate the backend separately and correct KinBot paths |
| invalid JSON key | input schema differs from the installed KinBot version | start from the installed example schema and add options incrementally |
| reaction or TS validation failed | geometry or frequency evidence is unsuitable | inspect the individual backend log rather than accepting the workflow label |
| Unable to run calculations when queuing is local | unpatched KinBot 2.2.2 local mode only reads precomputed output | apply the tracked local-NWChem patch and verify the installed KinBot version |
| NWChem input or Python syntax error | upstream templates target an older ASE writer or Python 2 | apply the tracked compatibility patch and use the configured NWChem command |
| PES search done but child never entered reaction search | the outer PES driver postprocessed a failed child or NWChem completion stamp was written to the wrong file | inspect every child kinbot.log and apply the tracked completion-marker patch |

## Path and staging failures
A source file existing in the benchmark workspace does not make it visible to the native process. Every dependency must be declared in `staged_inputs`. The content of an input deck must reference the staged `target_path`, not its original workspace path. Fixed-name programs are case-sensitive. Never assume the process starts in the task workspace.

## Resource failures
KinBot orchestrates many external calculations; bound concurrent children and use native provenance for each expensive backend job.
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
