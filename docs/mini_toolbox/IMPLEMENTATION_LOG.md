# MiniChem Toolbox Implementation Log

## Scope

- Create a portable `minichem_toolbox/` without modifying the existing `chemistry_toolbox/`.
- Preserve three invocation layers: typed Actions, reviewed native software jobs, and Agent-authored Python programs.
- Focus on ARCHE Case1-style molecular reaction-mechanism, transition-state, thermochemistry, selectivity, and electronic-analysis workflows.
- Keep all checked-in paths relative. Runtime launchers may resolve their own absolute location dynamically.
- Store copied software under `minichem_toolbox/.mini_software_cache/` and retained local models under `minichem_toolbox/.mini_model_cache/`.
- Add portable Codex, Claude, and OpenCode harnesses. Execute the OpenCode harness with `deepseek-v4-flash`.
- Make local Git commits only. Do not push to a remote repository.

## Step 1 - Initial Audit

Status: completed on 2026-08-04 UTC.

### Repository state

- Active branch: `codex/consolidate-toolbox-envs-20260729`.
- Existing unrelated untracked files were found and will not be modified:
  - `ResearchChemBench_data_pipeline_server.zip`
  - `docs/results/CHEMISTRY_TOOLBOX_AVAILABLE_TOOLS_20260801.md`
- Existing `chemistry_toolbox/` source size: approximately 102 MB.

### CLI availability

- Codex CLI: `0.145.0`
- Claude Code: `2.1.119`
- OpenCode: `1.18.10`

### Relevant cache inventory

- Gaussian 16 cache: approximately 14 GB.
  - Contains the licensed `g16`, `formchk`, link executables, basis data, and supporting runtime files.
  - The runtime cannot be represented by only the `g16` launcher; the complete required runtime tree must remain together.
- Multiwfn cache: approximately 231 MB.
- Existing root model cache: approximately 7.7 GB in total, but most entries are unrelated to the mini toolbox.
- Existing consolidated Conda environments are large and contain installation-prefix references, so raw directory copies are not considered portable.

### Portability decisions

1. Copy required proprietary/native software trees into `.mini_software_cache`; do not symlink to the old cache.
2. Exclude copied software and model payloads from Git while tracking manifests and bootstrap metadata.
3. Reconstruct Python environments from a reduced lock/specification instead of copying the existing Conda prefixes.
4. Keep the core profile model-free. The `deepseek-v4-flash` test model is accessed through an API and is not a local toolbox model.
5. Copy only a small local documentation-search embedding model if semantic documentation search remains enabled after pruning.
6. Rename the Python and MCP package identities to avoid collisions when the comprehensive and mini toolboxes coexist.

### Initial retained scientific scope

- Structure and conformer handling: RDKit, Open Babel, CREST, xTB.
- Reaction-path and transition-state support: pysisyphus and Sella, plus native Gaussian `Opt=TS`, `Freq`, and `IRC` jobs.
- Core electronic structure: Gaussian 16.
- Parsing and thermochemistry: cclib and GoodVibes.
- Mechanistic analysis: Multiwfn and deterministic reaction/free-energy analysis.
- Supporting schemas and runtime libraries: QCElemental, ASE, NumPy, SciPy, and required internal helpers.

## Step 2 - Focused Catalog and Portable Roots

Status: completed on 2026-08-04 UTC.

- Copied `chemistry_toolbox` to the independent `minichem_toolbox` directory and renamed the Python/MCP package identities.
- Added a centralized MiniChem profile that exposes only mechanism-oriented structure preparation, conformer search, Gaussian/xTB electronic structure, transition-state/path, thermochemistry, and output-analysis capabilities.
- Preserved all three execution layers: predefined Actions, allowlisted native software, and Agent-authored Python programs.
- Changed the default project root to the toolbox itself and introduced `.mini_software_cache` and `.mini_model_cache` as toolbox-local cache roots.
- Renamed the MCP resources and command entry points to MiniChem-specific names.
- Fixed the source-checkout package shim so imports work both from the parent repository and from an installed environment.

## Step 3 - Reduced Runtime Configuration

Status: completed on 2026-08-04 UTC.

- Replaced the comprehensive multi-environment configuration with one physical MiniChem runtime and eight stable logical runtime names.
- Repointed Gaussian and Multiwfn to `.mini_software_cache` and all local model/embedding paths to `.mini_model_cache`.
- Removed unrelated scientific-resource declarations; this profile requires no external model checkpoint, pseudopotential, or materials database.
- Added `MINICHEM_HOME`, `MINICHEM_ENV_ROOT`, and `MINICHEM_MODEL_CACHE` relocation hooks while keeping relative defaults.
- Restricted software discovery and native-job validation to Gaussian, CREST, xTB, Open Babel, pysisyphus, GoodVibes, and Multiwfn; hidden comprehensive-toolbox software cannot be invoked by guessing its identifier.
- Added cache manifests/readmes, a reduced reproducible environment specification, relocation-aware bootstrap and MCP launch scripts, and an optional `conda-pack` workflow.

## Step 4 - Isolated Agent Harnesses

Status: completed on 2026-08-04 UTC.

- Added Codex, Claude, and OpenCode harnesses that generate a fresh workspace per run.
- Each workspace keeps the prompt, MCP config, CLI event stream, stderr, session database/config, tool trace, tool results, generated inputs, and calculation outputs.
- Added a common three-layer smoke task requiring one predefined xTB Action, one native Gaussian optimization/frequency job, and one managed cclib Python analysis.
- OpenCode defaults to `deepseek/deepseek-v4-flash`; the API key is read from `OPENAI_API_KEY` and never serialized.
- Replaced the copied comprehensive README with a migration-oriented MiniChem manual covering scientific scope, all retained tools, the three invocation layers, cache/model provenance, relative layout, bootstrap, and harness usage.
- Replaced the comprehensive toolbox test suite in the copied directory with focused tests for the 37-Action profile, portable runtime mapping, native allowlist, three-layer contract, and isolated harness generation.

### Runtime installation repair

- The first environment build reached the pip phase but the host's default internal package index did not expose `fastmcp`.
- Split Conda and pip dependencies and made the pip index explicit/configurable through `MINICHEM_PYPI_INDEX_URL`; the partially created Conda prefix can now be resumed rather than rebuilt.
- Stopped the second attempt before the resolver could upgrade NumPy through the newest JAX; pinned JAX/JAXlib 0.4.35 and repeated the NumPy/SciPy/ASE compatibility constraints used by the reaction stack.
- The resumed build completed and all 18 retained backends passed health probing.
- The first live MCP startup exposed a stale `resource_snapshot()` reference in the overview generator; replaced both occurrences with the focused backend-filtered resource view and added an MCP registration regression test.
- Pytest then exposed that adding the toolbox root to `PYTHONPATH` shadows the official `mcp` package with the physical transport directory. Removed the root entry from tests, launchers, and runtime environments; only `src/` is added, while the transport comes from the editable package mapping.

## Step 5 - Scientific and Agent Integration Tests

Status: completed on 2026-08-04 UTC.

### Direct three-layer calculation

- Predefined Action: `calculate_energy` with xTB/GFN2 on neutral singlet water succeeded and returned `-5.065772968305 hartree` with a complete artifact record.
- Native software: an Agent-style Gaussian 16 C.01 `B3LYP/6-31G(d) Opt Freq` input was validated, submitted asynchronously, polled, and collected. It terminated normally in approximately 14.4 seconds with no imaginary frequency.
- Programmable analysis: a managed Python job used cclib and `researchchem_job.JobContext` to parse the Gaussian output. It wrote a declared JSON artifact containing the final electronic energy, optimized coordinates, three vibrational frequencies, and normal-termination flag.
- GoodVibes analysis: the retained `derive_thermochemistry` Action parsed the same Gaussian output at 298.15 K and returned RRHO enthalpy, entropy, Gibbs energy, point group, rotational data, and frequency metadata.
- Multiwfn native interface: `Multiwfn_noGUI` loaded the bundled `H2O.fch` example through an explicitly staged command stream and exited successfully, confirming executable discovery, staging, stdin handling, and collection.

### OpenCode + deepseek-v4-flash

- Ran `tests/harnesses/run_opencode.sh` with `deepseek/deepseek-v4-flash`.
- The Agent independently discovered the focused Action catalog, ran xTB, authored and validated a Gaussian input, waited for the Gaussian job to become terminal, authored a cclib program, waited for the analysis job, collected both jobs, copied the declared result to the requested workspace path, and wrote `report/report.md`.
- Exit code: 0. Both asynchronous jobs finished with return code 0.
- Saved workspace: `minichem_toolbox/tests/results/opencode/20260804T112513Z_2516114/`.
- Saved evidence includes `chat.jsonl`, OpenCode database/WAL, stderr, MCP tool traces, 23 persisted MCP result files, chemistry inputs, job state/logs, parsed JSON, and the Agent report.
- The run used 32 model steps, 45 tool calls, a final context size of 82,675 tokens, and approximately USD 0.0262 according to the OpenCode event stream.

### Repairs made during testing

1. Corrected two stale focused-resource calls that prevented the MCP server from starting.
2. Prevented the physical `mcp/` source directory from shadowing the official Python `mcp` package.
3. Replaced old `minichem_toolbox.mcp.*` subprocess module names with the installed `minichem_mcp_tools.*` transport package, which is required when launching from another project directory.
4. Pruned native-software configuration to the seven retained software interfaces instead of carrying unrelated comprehensive-toolbox commands.
5. Corrected the local MCP installer package name, default server name, and runtime Python selection.
6. Clarified asynchronous polling during manual testing: outer tool-call `status=success` means the query succeeded; terminality must be read from `terminal` or `job.status`.

## Step 6 - Portability Metadata and Packaging

Status: completed on 2026-08-04 UTC.

- Added generated software/model manifests with relative paths, component sizes, versions, and SHA-256 hashes for principal executables and all retained model files.
- Regenerated the checked-in 37-Action catalog and removed copied comprehensive-toolbox examples, test helpers, bytecode, and editable-install metadata from the source tree.
- Deleted the standalone molecular-dynamics, periodic/materials, docking, remote-data, licensed-MD, and GPAW backend modules and their Action declarations; the remaining Action aggregator loads only the five MiniChem scientific domains.
- Confirmed checked-in MiniChem source and configuration contain no host-specific absolute paths.
- Added a relocatable `conda-pack` workflow. The packer must ignore editable-package metadata because MiniChem source is migrated beside the runtime and reinstalled by `bootstrap.sh`.
- During cleanup, bytecode under the ignored Conda prefix was also removed. These files are reproducible; the packer now ignores missing generated bytecode, and final backend verification is repeated after packaging.
- Produced `.mini_software_cache/runtime_packs/minichem.tar.gz` (approximately 677 MiB), verified its gzip integrity, and confirmed that it contains Python and the installed MiniChem transport metadata.
- Final verification reported all 18 backends available, 37 Actions registered, seven native guides valid, and 13 focused tests passing.
- Started the MCP server from `/tmp` rather than the repository directory to confirm that relative root discovery and installed transport-module references survive cross-project use.

## Step 7 - Local Git Checkpoint

Status: completed on 2026-08-04 UTC.

- Reviewed staged paths to confirm that Gaussian, Multiwfn, model files, the Conda prefix, runtime archive, and Agent test workspaces remain ignored by Git.
- Confirmed no API keys or host-specific absolute paths were present in the tracked MiniChem source and documentation.
- Created local implementation commit `b766dc4` (`feat: add portable MiniChem toolbox`).
- No remote branch was created or pushed. The original comprehensive toolbox and its caches remain unchanged.
