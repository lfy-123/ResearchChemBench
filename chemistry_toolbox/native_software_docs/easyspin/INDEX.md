---
software_id: easyspin
versions: []
topics: [index, quickstart, native-execution, resources, convergence, troubleshooting]
aliases: ["easyspin"]
inputs: ["analysis.m", "EasySpin inputs", "and experimental data"]
outputs: ["stdout.log", "stderr.log", "software-declared output files"]
last_smoke_tested: null
generated_from: chemistry_toolbox/config/native_software_guides.yaml
---
# Easyspin Native Execution

## Purpose and supported version
Execute an Agent-authored MATLAB script using the staged EasySpin 6.0.12 toolbox when MATLAB is licensed and available.

Configured runtime: `easyspin`. Detected versions: not recorded; inspect the executable before relying on version-specific syntax.

## Working directory and staging
The execution layer creates an isolated job directory and runs the exact argv vector there without a shell. Stage every referenced input with the exact filename used by the command or input deck. Relative paths resolve from the job directory, not from the task workspace root. Use `stdin_target` only when the command input mode below requires stdin.

## Commands

### `matlab`
Synopsis: `matlab -nodisplay -nosplash -nodesktop -r "addpath('<EasySpin path>'); run('analysis.m'); exit"`

Input mode: `arguments`.

Required staged files: `analysis.m`, `EasySpin inputs`, `and experimental data`

Output behavior: Writes simulated spectra, fitted parameters, figures/data, and console output selected by the script.

Example argv: `matlab -nodisplay -nosplash -nodesktop -r run('analysis.m'); exit`.

Command-specific cautions:
- The EasySpin toolbox is staged, but execution remains unavailable until licensed MATLAB is configured.

## Resource mapping
Set `resource_limits.cpu_cores`, `memory_mb`, `gpu_count`, and `walltime_seconds` explicitly. Keep software thread, MPI, memory, and GPU settings within those requested limits. The Supervisor enforces the per-job memory limit, CPU affinity, evaluator-wide concurrent reservations, walltime, cancellation, and process-group cleanup.

## Normal termination and scientific convergence
Exit code zero only establishes process completion. Inspect stdout, stderr, and the software's primary output for fatal errors and its documented normal-termination marker. Scientific convergence is task-specific: verify the requested optimization, electronic, ionic, frequency, dynamics, fitting, or projection criteria and confirm that every required result file is present and parseable. If the toolbox has no software-specific parser for this task, the status remains `not_checked` rather than inferring convergence from the exit code.

## Common immediate failures
- A referenced file was not staged with the exact target name.
- The command was authored for a different software version.
- An input deck contains an invalid keyword, section delimiter, or path.
- Internal thread, MPI, memory, or GPU settings exceed the declared resource limits.
- The process exits successfully but the main output reports a scientific or parsing failure.

## Preflight checklist
- Confirm the installed version and executable returned by `inspect_software`.
- Read this manual and any referenced official version documentation.
- Stage every input and nested dependency using the exact job-local filename.
- Declare a calculation intent when the task has a convergence contract.
- Match software parallelism and memory settings to `resource_limits`.
- Run `validate_native_job` before submission.
- After execution, inspect all status axes and the required output artifacts.
