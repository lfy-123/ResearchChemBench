---
software_id: orca
versions: ["6.1.1"]
topics: ["quickstart", "staging", "submission", "resources"]
aliases: ["ORCA", "orca"]
inputs: ["input.inp", "optional external XYZ", "basis", "point charges", "or restart files"]
outputs: ["stdout.log", ".gbw", ".xyz", ".hess", ".densities", "property files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# ORCA Quickstart

## Complete invocation flow
1. Call `inspect_software` and confirm the executable, installed version, runtime, and documentation topics.
2. Author the smallest scientifically meaningful input for the selected task and installed version.
3. Put every source file under the evaluation workspace and map it to the exact job-local target expected by the input deck.
4. Set explicit CPU, total memory, GPU, and walltime limits. Keep all software-internal parallel settings within those limits.
5. Call `validate_native_job`; repair every error before submitting.
6. Call `submit_native_job`, poll `get_execution_job`, and finally call `collect_execution_job`.
7. Check process, software, convergence, artifact, and scientific-validation axes independently.

## Working directory contract
The runner creates an isolated job directory and executes the resolved binary there without a shell. Relative paths in arguments and input files resolve from that directory, not from the benchmark workspace root. `source_path` is workspace-relative; `target_path` is job-relative. Stage nested dependencies explicitly. The runner captures `request.json`, `stdout.log`, `stderr.log`, status, hashes, and collected artifacts.

## Input mode
The primary executable is `orca` and its input mode is `arguments`.
Required inputs: `input.inp`, `any geometry/basis files referenced by input.inp`.
Output behavior: Writes the primary output to stdout and ORCA property/restart files in the job directory.

## Native command template
```bash
orca input.inp
```
Run that command only inside a directory containing the exact referenced files. The toolbox resolves the executable itself; do not embed shell redirection, pipes, `cd`, or environment activation in `arguments`.

## Toolbox submission template
```json
{
  "software_id": "orca",
  "executable": "orca",
  "arguments": [
    "input.inp"
  ],
  "staged_inputs": [
    {
      "source_path": "workspace_inputs/input.inp",
      "target_path": "input.inp"
    }
  ],
  "resource_limits": {
    "cpu_cores": 1,
    "memory_mb": 2048,
    "gpu_count": 0
  }
}
```
The paths under `workspace_inputs/` are illustrative workspace-relative sources. Replace them with real files and keep the target names synchronized with the input deck.

## stdin, arguments, and fixed files
- For `arguments`, put each token in `arguments`; never pass one shell command string.
- For `stdin_file`, stage the input and set `stdin_target`; do not put `< input` in `arguments`.
- For `arguments_and_stdin_file`, provide both the positional file arguments and `stdin_target`.
- For `fixed_files`, stage every required filename exactly and normally leave `arguments` empty.

## Resource mapping
%pal nprocs must not exceed cpu_cores; %maxcore is MiB per process, so nprocs times maxcore must remain below total memory with headroom.
`resource_limits.memory_mb` is total memory for the entire process group, not memory per MPI rank. `cpu_cores` is the allocation ceiling. Software thread or rank controls must not exceed it. Walltime is enforced by the Supervisor; a timeout is distinct from software non-convergence.

## Collection checklist
- `request_status=accepted` confirms only that the interface accepted the request.
- `process_status=completed` confirms only process exit code zero.
- `software_status=normal` requires a recognized normal end and no fatal message when a parser exists.
- `convergence_status` must match the requested task type; an SCF marker alone cannot validate an optimization or frequency job.
- `artifact_status=valid` requires all declared results to exist and parse.
- The Judger, not the execution layer, evaluates whether the results support the requested scientific conclusion.
