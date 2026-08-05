---
software_id: lobster
versions: ["5.1.0"]
topics: ["quickstart", "staging", "submission", "resources"]
aliases: ["LOBSTER", "lobster"]
inputs: ["lobsterin", "structure and basis metadata", "compatible VASP", "Quantum ESPRESSO", "or ABINIT wavefunction outputs"]
outputs: ["lobsterout", "COHPCAR.lobster", "ICOHPLIST.lobster", "DOSCAR.lobster", "CHARGE.lobster"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# LOBSTER Quickstart

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
The primary executable is `lobster-5.1.0` and its input mode is `fixed_files`.
Required inputs: `lobsterin`, `POSCAR`, `POTCAR`, `WAVECAR`, `CONTCAR`, `KPOINTS`, `OUTCAR`, `vasprun.xml`.
Expected outputs: stdout/stderr or task-dependent outputs only.
Example classification: `scientific_template`.
Output behavior: Reads fixed filenames and writes lobsterout plus analysis files in the job directory.

## Native command template
```bash
lobster-5.1.0
```
Run that command only inside a directory containing the exact referenced files. The toolbox resolves the executable itself; do not embed shell redirection, pipes, `cd`, or environment activation in `arguments`.

## Toolbox submission template
```json
{
  "software_id": "lobster",
  "executable": "lobster-5.1.0",
  "arguments": [],
  "staged_inputs": [
    {
      "source_path": "workspace_inputs/lobsterin",
      "target_path": "lobsterin"
    },
    {
      "source_path": "workspace_inputs/POSCAR",
      "target_path": "POSCAR"
    },
    {
      "source_path": "workspace_inputs/POTCAR",
      "target_path": "POTCAR"
    },
    {
      "source_path": "workspace_inputs/WAVECAR",
      "target_path": "WAVECAR"
    },
    {
      "source_path": "workspace_inputs/CONTCAR",
      "target_path": "CONTCAR"
    },
    {
      "source_path": "workspace_inputs/KPOINTS",
      "target_path": "KPOINTS"
    },
    {
      "source_path": "workspace_inputs/OUTCAR",
      "target_path": "OUTCAR"
    },
    {
      "source_path": "workspace_inputs/vasprun.xml",
      "target_path": "vasprun.xml"
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
LOBSTER is CPU and memory intensive for large basis and k meshes; thread settings and upstream WAVECAR size must fit the allocation.
`resource_limits.memory_mb` is total memory for the entire process group, not memory per MPI rank. `cpu_cores` is the allocation ceiling. Software thread or rank controls must not exceed it. Walltime is enforced by the Supervisor; a timeout is distinct from software non-convergence.

## Collection checklist
- `request_status=accepted` confirms only that the interface accepted the request.
- `process_status=completed` confirms only process exit code zero.
- `software_status=normal` requires a recognized normal end and no fatal message when a parser exists.
- `convergence_status` must match the requested task type; an SCF marker alone cannot validate an optimization or frequency job.
- `artifact_status=valid` requires all declared results to exist and parse.
- The Judger, not the execution layer, evaluates whether the results support the requested scientific conclusion.
