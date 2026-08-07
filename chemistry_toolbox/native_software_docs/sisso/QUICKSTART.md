---
software_id: sisso
versions: ["3.5 (bc18cae)"]
topics: ["quickstart", "staging", "submission", "resources"]
aliases: ["SISSO", "sisso"]
inputs: ["SISSO.in", "train.dat", "optional SISSO.out and predict.dat for evaluation"]
outputs: ["SISSO.out", "Models", "SIS_subspaces", "predict_X.out", "predict_Y.out"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SISSO Quickstart

## Complete invocation flow
1. Call `inspect_software` and confirm the executable, installed version, runtime, and documentation topics.
2. Author the smallest scientifically meaningful input for the selected task and installed version.
3. Put every source file under the evaluation workspace and map it to the exact job-local target expected by the input deck.
4. Set explicit CPU, total memory, GPU, and walltime limits. Keep all software-internal parallel settings within those limits.
5. Call `validate_native_job`; repair every error before submitting.
6. Call `submit_native_job`, then supervise all independent job IDs with `wait_execution_jobs`; use focused inspection or full collection only when needed.
7. Check process, software, convergence, artifact, and scientific-validation axes independently.

## Working directory contract
The runner creates an isolated job directory and executes the resolved binary there without a shell. Relative paths in arguments and input files resolve from that directory, not from the benchmark workspace root. `source_path` is workspace-relative; `target_path` is job-relative. Stage nested dependencies explicitly. The runner captures `request.json`, `stdout.log`, `stderr.log`, status, hashes, and collected artifacts.

## Input mode
The primary executable is `SISSO` and its input mode is `fixed_files`.
Required inputs: `SISSO.in`, `train.dat`.
Expected outputs: `SISSO.out`, `Models/data_top1/desc_D001.dat`, `SIS_subspaces/Uspace.expressions`.
Example classification: `scientific_template`.
Output behavior: Writes SISSO.out, Models, SIS_subspaces, CONTINUE state when applicable, and progress to stdout.

## Native command template
```bash
SISSO
```
Run that command only inside a directory containing the exact referenced files. The toolbox resolves the executable itself; do not embed shell redirection, pipes, `cd`, or environment activation in `arguments`.

## Toolbox submission template
```json
{
  "software_id": "sisso",
  "executable": "SISSO",
  "arguments": [],
  "staged_inputs": [
    {
      "source_path": "workspace_inputs/SISSO.in",
      "target_path": "SISSO.in"
    },
    {
      "source_path": "workspace_inputs/train.dat",
      "target_path": "train.dat"
    }
  ],
  "resource_limits": {
    "cpu_cores": 1,
    "memory_mb": 4096,
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
Feature spaces can grow combinatorially. CPU processes must not exceed the requested budget and memory must be assessed against operator set, complexity, features, samples and SIS size. The wrapper sets only the stack limit.
`resource_limits.memory_mb` is total memory for the entire process group, not memory per MPI rank. `cpu_cores` is the allocation ceiling. Software thread or rank controls must not exceed it. Walltime is enforced by the Supervisor; a timeout is distinct from software non-convergence.

## Collection checklist
- `request_status=accepted` confirms only that the interface accepted the request.
- `process_status=completed` confirms only process exit code zero.
- `software_status=normal` requires a recognized normal end and no fatal message when a parser exists.
- `convergence_status` must match the requested task type; an SCF marker alone cannot validate an optimization or frequency job.
- `artifact_status=valid` requires all declared results to exist and parse.
- The Judger, not the execution layer, evaluates whether the results support the requested scientific conclusion.
