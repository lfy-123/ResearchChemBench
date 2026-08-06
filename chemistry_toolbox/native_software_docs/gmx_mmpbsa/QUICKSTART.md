---
software_id: gmx_mmpbsa
versions: ["1.6.5"]
topics: ["quickstart", "staging", "submission", "resources"]
aliases: ["gmx_MMPBSA", "gmx mmpbsa"]
inputs: ["mmpbsa.in", "complex TPR", "index NDX", "trajectory XTC", "topology TOP and ITP includes"]
outputs: ["FINAL_RESULTS_MMPBSA.dat", "FINAL_RESULTS_MMPBSA.csv", "optional FINAL_DECOMP_MMPBSA.dat and CSV"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# gmx_MMPBSA Quickstart

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
The primary executable is `gmx_MMPBSA` and its input mode is `arguments`.
Required inputs: `mmpbsa.in`, `complex.tpr`, `index.ndx`, `trajectory.xtc`, `topology.top`, `toppar/forcefield.itp`.
Expected outputs: `FINAL_RESULTS_MMPBSA.dat`, `FINAL_RESULTS_MMPBSA.csv`.
Example classification: `scientific_template`.
Output behavior: Writes final summary and per-frame energy tables; explicit -do and -deo options additionally write residue-decomposition results.

## Native command template
```bash
gmx_MMPBSA -O -i mmpbsa.in -cs complex.tpr -ci index.ndx -cg 3 4 -ct trajectory.xtc -cp topology.top -o FINAL_RESULTS_MMPBSA.dat -eo FINAL_RESULTS_MMPBSA.csv -nogui
```
Run that command only inside a directory containing the exact referenced files. The toolbox resolves the executable itself; do not embed shell redirection, pipes, `cd`, or environment activation in `arguments`.

## Toolbox submission template
```json
{
  "software_id": "gmx_mmpbsa",
  "executable": "gmx_MMPBSA",
  "arguments": [
    "-O",
    "-i",
    "mmpbsa.in",
    "-cs",
    "complex.tpr",
    "-ci",
    "index.ndx",
    "-cg",
    "3",
    "4",
    "-ct",
    "trajectory.xtc",
    "-cp",
    "topology.top",
    "-o",
    "FINAL_RESULTS_MMPBSA.dat",
    "-eo",
    "FINAL_RESULTS_MMPBSA.csv",
    "-nogui"
  ],
  "staged_inputs": [
    {
      "source_path": "workspace_inputs/mmpbsa.in",
      "target_path": "mmpbsa.in"
    },
    {
      "source_path": "workspace_inputs/complex.tpr",
      "target_path": "complex.tpr"
    },
    {
      "source_path": "workspace_inputs/index.ndx",
      "target_path": "index.ndx"
    },
    {
      "source_path": "workspace_inputs/trajectory.xtc",
      "target_path": "trajectory.xtc"
    },
    {
      "source_path": "workspace_inputs/topology.top",
      "target_path": "topology.top"
    },
    {
      "source_path": "workspace_inputs/toppar/forcefield.itp",
      "target_path": "toppar/forcefield.itp"
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
The fixed runtime uses Python 3.11, AmberTools 23.6, GROMACS 2025.4, and MPI. It must remain isolated from the shared Python 3.12 and AmberTools 26 environment.
`resource_limits.memory_mb` is total memory for the entire process group, not memory per MPI rank. `cpu_cores` is the allocation ceiling. Software thread or rank controls must not exceed it. Walltime is enforced by the Supervisor; a timeout is distinct from software non-convergence.

## Collection checklist
- `request_status=accepted` confirms only that the interface accepted the request.
- `process_status=completed` confirms only process exit code zero.
- `software_status=normal` requires a recognized normal end and no fatal message when a parser exists.
- `convergence_status` must match the requested task type; an SCF marker alone cannot validate an optimization or frequency job.
- `artifact_status=valid` requires all declared results to exist and parse.
- The Judger, not the execution layer, evaluates whether the results support the requested scientific conclusion.
