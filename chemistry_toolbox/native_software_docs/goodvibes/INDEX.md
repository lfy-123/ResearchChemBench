---
software_id: goodvibes
versions: []
topics: [index, quickstart, native-execution, resources, convergence, troubleshooting]
aliases: ["goodvibes"]
inputs: ["one or more Gaussian 09/16", "ORCA 5/6", "NWChem", "Q-Chem 6", "xTB", "or ASE-extxyz output files"]
outputs: ["stdout.log", "stderr.log", "software-declared output files"]
last_smoke_tested: null
generated_from: chemistry_toolbox/config/native_software_guides.yaml
---
# Goodvibes Native Execution

## Purpose and supported version
Apply GoodVibes 4.3.0 thermochemistry, ensemble, selectivity, consistency, and reaction-profile analysis to explicit completed quantum-chemistry outputs.

Configured runtime: `goodvibes`. Detected versions: not recorded; inspect the executable before relying on version-specific syntax.

## Working directory and staging
The execution layer creates an isolated job directory and runs the exact argv vector there without a shell. Stage every referenced input with the exact filename used by the command or input deck. Relative paths resolve from the job directory, not from the task workspace root. Use `stdin_target` only when the command input mode below requires stdin.

## Commands

### `goodvibes`
Synopsis: `goodvibes OUTPUT... --temp K [state/scaling/qh options] [analysis option] --json result.json`

Input mode: `arguments`.

Required staged files: `one or more Gaussian 09/16`, `ORCA 5/6`, `NWChem`, `Q-Chem 6`, `xTB`, `or ASE-extxyz output files`

Output behavior: Writes a GoodVibes_NAME.dat report and, when requested, structured JSON/CSV/Parquet plus plots or XYZ files in the isolated job directory.

Example argv: `goodvibes output.log --temp 298.15 --conc 1.0 --qs grimme --qh --fs 100 --fh 100 -v 0.99 --zpe-vscal 0.98 --json result.json`.

Command-specific cautions:
- Temperature, concentration/standard state, frequency scaling, quasi-harmonic treatment, and solvation corrections are scientific choices.
- Use -v/--vscal for vibrational scaling. --fs is the quasi-harmonic entropy cutoff in cm-1; it is not a scale factor.
- Omit -v only when deliberately choosing GoodVibes level-of-theory auto lookup; record that choice in the task trace.
- Use --boltz energy or --boltz gibbs for ensemble populations, --dedup with explicit cutoffs for duplicate filtering, and --check for consistency diagnostics.
- Use repeated --label NAME=PATTERN or --selectivity labels.yaml for N-way selectivity; prefer the non-deprecated interfaces over --ee.
- Use --pes profile.yaml for a reaction profile. The YAML defines pathways, species file membership, zero references, and output units; --nogconf and --lowest-only select the conformer treatment.
- Use --ti START,END,STEP for the native integer-grid temperature report. The predefined temperature-scan Action instead accepts an explicit temperature list and returns structured results at every point.
- --json/--export writes schema 1.0 in GoodVibes 4.3.0, but upstream describes the schema as preview before v5; consumers should retain schema_version and goodvibes_version.

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
