---
software_id: sisso
versions: ["3.5 (bc18cae)"]
topics: ["troubleshooting", "errors", "preflight"]
aliases: ["SISSO", "sisso"]
inputs: ["SISSO.in", "train.dat", "optional SISSO.out and predict.dat for evaluation"]
outputs: ["SISSO.out", "Models", "SIS_subspaces", "predict_X.out", "predict_Y.out"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SISSO Troubleshooting

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
| mpiifort not found or gfortran MPI interface errors | SISSO 3.5 requires its pinned Intel toolchain build | restore the complete toolchain cache and do not rebuild with an unvalidated compiler |
| bc not found | the official SISSO_predict expression evaluator lacks its runtime dependency | install the declared bc 1.07.1 package |
| Cannot read parameter | SISSO.in does not match version 3.5 syntax or the data dimensions | regenerate from the matching template and verify every explicit parameter |
| killed or out of memory | the feature space or saved model count exceeds resources | reduce only scientifically justified search bounds or allocate more memory |

## Path and staging failures
A source file existing in the benchmark workspace does not make it visible to the native process. Every dependency must be declared in `staged_inputs`. The content of an input deck must reference the staged `target_path`, not its original workspace path. Fixed-name programs are case-sensitive. Never assume the process starts in the task workspace.

## Resource failures
Feature spaces can grow combinatorially. CPU processes must not exceed the requested budget and memory must be assessed against operator set, complexity, features, samples and SIS size. The wrapper sets only the stack limit.
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
