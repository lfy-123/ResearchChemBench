# MiniChem Toolbox Implementation and Test Report

Date: 2026-08-04 UTC

## 1. Result

A new independent `minichem_toolbox/` has been created for ARCHE Case1-style molecular mechanism
tasks. The original `chemistry_toolbox/`, `.software_cache/`, and `.model_cache/` were not modified.
MiniChem keeps the same three invocation layers as the comprehensive toolbox while reducing the
scientific and runtime surface to mechanism reconstruction, conformer handling, Gaussian-centered
electronic structure, transition-state/path work, thermochemistry, and electronic analysis.

Final status:

- 37 predefined Actions;
- 18 retained backends, all available;
- 7 reviewed native software interfaces;
- one portable Python runtime shared by eight logical runtime profiles;
- dedicated runtime location at `.envs/minichem`, separate from native software caches;
- independent `.mini_software_cache/` and `.mini_model_cache/`;
- Codex, Claude, and OpenCode isolated harnesses;
- OpenCode + `deepseek-v4-flash` end-to-end test passed;
- 13 focused automated tests passed;
- MCP startup from an unrelated external working directory passed.

## 2. Scientific Scope

The retained workflow covers the common inputs and calculations needed to reconstruct a small
molecular reaction-mechanism study:

1. standardize molecular records, build 3D structures, and enumerate relevant stereochemical,
   tautomeric, protonation, or coordination assignments;
2. generate, cluster, align, rank, and prescreen conformers;
3. calculate energies, forces, Hessians, optimized structures, dipoles, charges, and bond orders;
4. locate transition states, search or validate paths, scan coordinates, and run IRC calculations;
5. derive vibrational modes, spectra, RRHO/quasi-harmonic thermochemistry, populations,
   selectivity, and reaction free-energy profiles;
6. parse quantum-chemistry outputs and run wavefunction/electron-density analyses.

The profile intentionally excludes materials simulation, molecular dynamics, docking, remote
chemistry databases, and large learned interatomic-potential stacks.

The standalone source modules for those excluded domains were removed rather than merely hidden.
Some retained shared electronic/structure files still contain internal branches inherited from the
comprehensive implementation, but no excluded backend is present in the catalog, runtime mapping,
software interface, or dispatch table.

## 3. Three Invocation Layers

### 3.1 Predefined Actions

Typed Actions provide validated common operations. Important providers include RDKit, Open Babel,
CREST, xTB, Gaussian, GoodVibes, Multiwfn, pysisyphus, and Sella. The Agent must explicitly choose
the backend and all scientifically meaningful method/settings; `auto` selection and silent fallback
are not allowed.

### 3.2 Native Software

The Agent may author complete inputs and invoke allowlisted commands for:

- Gaussian: `g16`, `formchk`;
- CREST: `crest`;
- xTB: `xtb`;
- Open Babel: `obabel`;
- pysisyphus: `pysis`;
- GoodVibes: `goodvibes`;
- Multiwfn: `Multiwfn_noGUI`.

This layer is essential for Gaussian `Opt=TS`, `Freq`, `IRC`, Link1, custom route sections, and
other paper-specific jobs that should not be hidden inside a fixed Action. Inputs are staged into an
isolated job directory, commands run with `shell=false`, and status/logs/hashes are retained.

### 3.3 Agent-Authored Python

The Agent can write a Python program and submit it to the managed runtime. Declared inputs and
outputs use `researchchem_job.JobContext`; the framework validates imports, syntax, resource limits,
declared paths, and output registration. Retained libraries include RDKit, ASE, cclib, QCElemental,
NumPy, SciPy, Sella, pysisyphus, GoodVibes, ONNX Runtime, and tokenizers.

## 4. Portable Caches and Runtime

All checked-in paths are relative to `minichem_toolbox/`.

| Component | Location | Approximate size | Notes |
|---|---|---:|---|
| Gaussian 16 C.01 | `.mini_software_cache/gaussian/` | 14.1 GB | Licensed software; copied independently from the original cache |
| Multiwfn 2026.7.15 | `.mini_software_cache/multiwfn/` | 167 MB | Includes noGUI executable and upstream examples |
| MiniChem Conda runtime | `.envs/minichem/` | 2.27 GB | Python 3.11, one physical runtime |
| Relocatable runtime archive | `.envs/runtime_packs/minichem.tar.gz` | 677 MiB | gzip integrity verified |
| MiniLM model and indexes | `.mini_model_cache/` | 24 MB | Optional semantic Action/document recall |

The local model is `sentence-transformers/all-MiniLM-L6-v2`, originally downloaded from Hugging
Face. `deepseek-v4-flash` is an API model and is not stored locally. Cache manifests contain relative
paths, sizes, package versions, and SHA-256 values. Binary payloads are deliberately ignored by Git;
the manifests and environment specifications are tracked. Conda metadata is stored in
`.envs/manifest.json`, while `.mini_software_cache/manifest.json` records only Gaussian and Multiwfn.

Migration procedure:

```bash
cp -a minichem_toolbox /path/to/another/project/
cd /path/to/another/project/minichem_toolbox
bash scripts/bootstrap.sh
bash scripts/start_mcp.sh --transport stdio --discovery-mode progressive
```

`bootstrap.sh` reuses an existing prefix, unpacks the runtime archive, or reconstructs the runtime
from the relative environment files. It then reinstalls the local source mapping and verifies all
backends.

## 5. Harness Isolation

Harnesses are stored in `minichem_toolbox/tests/harnesses/`. Every run creates a new workspace under
`tests/results/<cli>/<timestamp>_<pid>/` with separate:

- `code/`, `data/`, `outputs/`, and `report/` directories;
- `_sessions/` for chat/event streams, stderr, CLI state, and exit code;
- `_tool_results/`, `_tool_artifacts/`, `tool_logs/`, and `_tool_trace.jsonl`;
- MCP launcher/config files generated for that exact workspace.

Codex and Claude harness scripts were syntax/interface checked and covered by workspace-generation
tests. The requested live model test was run through OpenCode.

## 6. Test Results

### 6.1 Direct three-layer smoke test

Water was used as a deterministic interface smoke test.

- xTB Action: GFN2 energy succeeded, `-5.065772968305 hartree`.
- Gaussian native job: B3LYP/6-31G(d) `Opt Freq` succeeded with normal termination and zero
  imaginary frequencies. Frequencies were 1712.9230, 3727.7901, and 3849.7982 cm-1.
- Managed cclib program: parsed final energy, optimized coordinates, frequencies, and termination
  state into a declared JSON output.
- GoodVibes Action: parsed the Gaussian output and returned 298.15 K RRHO thermochemistry,
  including enthalpy, entropy, Gibbs energy, point group, rotational constants, and frequencies.
- Multiwfn native job: loaded `H2O.fch`, displayed the analysis menu, and exited with return code 0.

### 6.2 OpenCode + deepseek-v4-flash

Workspace: `minichem_toolbox/tests/results/opencode/20260804T112513Z_2516114/`

The Agent independently completed all three layers, waited for both asynchronous jobs to become
terminal, collected their outputs, and wrote `report/report.md` plus
`outputs/parsed_gaussian.json`.

- harness exit code: 0;
- Gaussian native job return code: 0;
- Python analysis job return code: 0;
- model steps: 32;
- tool calls: 45;
- final context size reported by OpenCode: 82,675 tokens;
- event-stream API cost: approximately USD 0.0262.

The full chat history, OpenCode database/WAL, stderr, MCP traces, tool results, input deck, Gaussian
logs/checkpoint, cclib program, parsed JSON, and final report are preserved in that workspace.

### 6.3 Automated and portability checks

- `13 passed` in the focused pytest suite;
- catalog validation: 37 Actions, 18 backends, 7 native guides;
- backend health: 18 available, 0 unavailable;
- runtime archive: gzip integrity and expected Python/package entries verified;
- host-specific absolute path scan: no matches in checked-in MiniChem source/configuration;
- external-working-directory MCP launch: passed from `/tmp`.

## 7. Bugs Found and Fixed

1. Focused catalog overview called a removed comprehensive resource function, preventing MCP startup.
2. Adding the toolbox root to `PYTHONPATH` shadowed the official `mcp` package.
3. Batch/distributed subprocesses retained old transport module names and were unreliable after
   migration to another project directory.
4. The copied native configuration still exposed unrelated software descriptions even though the
   runtime profile filtered them.
5. The copied installer referenced the old package name and runtime defaults.
6. `conda-pack` rejected the editable source package and generated bytecode cleanup; the packer now
   explicitly handles both conditions, while `bootstrap.sh` reinstalls the local source mapping.
7. Running Python from the toolbox root exposed the physical `mcp/` directory as a top-level package
   and shadowed the official MCP SDK. The physical directory is now `mcp_tools/`, while the installed
   package remains `minichem_mcp_tools`.

## 8. Boundaries

- Gaussian is commercial software. MiniChem cannot redistribute it or relax its license terms.
- Scientific correctness still depends on the Agent reconstructing the correct molecular state,
  conformer set, functional, basis, solvent model, constraints, TS guess, standard state, and
  corrections from the paper and supporting information.
- The runtime archive targets compatible Linux x86-64 hosts; materially different operating systems
  or CPU architectures require rebuilding from the environment specifications.
- Predefined Actions deliberately do not cover every Gaussian route. Native Gaussian input is the
  intended escape hatch for paper-specific mechanism calculations.
- The programmable layer is an audit/reliability boundary, not an OS security sandbox. Untrusted
  Agents should run the MCP server inside a container or scheduler isolation boundary.

## 9. Main Deliverables

- `minichem_toolbox/README.md`: user and migration guide;
- `minichem_toolbox/TOOLBOX.md`: Chinese architecture, Action, backend, and invocation reference;
- `minichem_toolbox/mcp_tools/TOOL_CATALOG.md`: generated focused Action/backend catalog;
- `minichem_toolbox/.envs/environment.yml`: reproducible Conda specification;
- `minichem_toolbox/.envs/manifest.json`: runtime and runtime-pack manifest;
- `minichem_toolbox/.mini_software_cache/manifest.json`: native software manifest;
- `minichem_toolbox/.mini_model_cache/manifest.json`: model/index manifest;
- `minichem_toolbox/tests/harnesses/`: Codex, Claude, and OpenCode harnesses;
- `docs/mini_toolbox/IMPLEMENTATION_LOG.md`: step-by-step implementation record;
- `docs/mini_toolbox/FINAL_REPORT.md`: this report.

The initial implementation is saved in local Git commit `b766dc4`; the dedicated-environment
relocation is saved in the follow-up local commit `refactor: isolate MiniChem conda environment`.
Neither commit has been pushed to GitHub.
