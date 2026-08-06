---
software_id: bagel
versions: ["1.2.2-3ubuntu1 (bfceffea)"]
topics: ["troubleshooting", "errors", "preflight"]
aliases: ["BAGEL", "bagel"]
inputs: ["BAGEL JSON input with geometry basis active space state manifold method and derivative target"]
outputs: ["state energies", "convergence diagnostics", "nuclear gradients", "nonadiabatic coupling vectors"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# BAGEL Troubleshooting

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
| Could not find basis set | the JSON basis name was not resolved to the cached basis directory | use the configured wrapper and an installed explicit basis name |
| CBLAS parameter error | the selected active space or very small model is numerically invalid | validate electron count orbital partition basis and state manifold |
| Second-order optimization did not converge | the CASSCF reference failed its explicit thresholds | inspect iterations and revise the scientifically justified initial space or convergence plan |
| MPI library or Hydra launcher missing | only part of the cache-local runtime was migrated | copy the complete .software_cache/installations/bagel/1.2.2 directory |

## Path and staging failures
A source file existing in the benchmark workspace does not make it visible to the native process. Every dependency must be declared in `staged_inputs`. The content of an input deck must reference the staged `target_path`, not its original workspace path. Fixed-name programs are case-sensitive. Never assume the process starts in the task workspace.

## Resource failures
The local runtime is an Ubuntu 22.04 MPICH binary plus a cache-local library closure. Keep MPI ranks times BAGEL threads within cpu_cores; no system package or shared Conda dependency is required.
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
