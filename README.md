# ResearchChemBench

ResearchChemBench evaluates whether external autonomous agents such as Codex CLI, Claude Code, and OpenCode can independently compose atomic chemistry tools to solve scientific tasks. Every task can discover the same complete toolbox; the agent chooses the actions, call order, software backend, method, parameters, failure recovery, and stopping point. The default MCP surface loads the catalog progressively so unused Action schemas do not consume every model turn.

## Build the environments

The current runtime layout uses one project environment plus six consolidated
chemistry environments. The former one-profile-per-prefix layout under
`.tool_envs/` is retained only as a temporary compatibility fallback and is not
the recommended installation target.

| Environment | Default prefix | Main responsibility |
|---|---|---|
| Project environment | `.toolbox_env` | Evaluation CLI, bootstrap utilities, project tests, and local administration |
| General | `.tool_envs_merged/general-modern-openmpi5` | MCP server, cheminformatics, quantum chemistry, materials analysis, MACE/CHGNet, and most native software entry points |
| Molecular simulation | `.tool_envs_merged/molecular-simulation-openff` | OpenFF/AmberTools, OpenMM, GROMACS, HOOMD, free-energy analysis, and docking |
| Reaction and kinetics | `.tool_envs_merged/kinetics-legacy` | RMG/Arkane, reaction exploration, KinBot/Sella, ABINIT, and LAMMPS |
| Equivariant ML | `.tool_envs_merged/equivariant-ml` | DeePMD, NequIP, Allegro, CPU PyTorch, and e3nn |
| Periodic MPICH | `.tool_envs_merged/periodic-mpich` | CP2K 2026.1 with its isolated MPICH 5/libxc 7 stack |
| CatMAP and Yambo | `.tool_envs_merged/yambo-openmpi4` | CatMAP/ASE 3.17 and Yambo/OpenMPI 4 compatibility runtime |

### 1. Prerequisites

Use a Linux x86-64 host with Conda or Mamba available. Mamba is recommended.
The exact locks reproduce the tested `linux-64` package builds; use the
maintained specifications instead when deploying to another platform.

Optional GUI/native smoke tests also use the Debian/Ubuntu packages listed in
`chemistry_toolbox/environment/merged/system-requirements.txt`:

```bash
sudo apt-get update
sudo apt-get install -y xauth xvfb libxkbcommon0 libgtk-3-0
```

These host packages may be omitted when the corresponding GUI capabilities are
not needed.

### 2. Build the project environment

Run from the repository root. `--skip-verify` defers the complete toolbox
verification until the six backend environments are present.

```bash
cd /path/to/ResearchChemBench
bash chemistry_toolbox/scripts/setup_toolbox_env.sh --skip-verify
```

This creates `.toolbox_env`, installs the editable ResearchChemBench package,
and caches the offline semantic-retrieval model used by progressive discovery.

### 3. Build the six consolidated chemistry environments

For another compatible Linux x86-64 server, replay the committed Conda
artifacts. This is the preferred migration and reproducibility path:

```bash
export RCB_PIP_INDEX_URL=https://pypi.org/simple
export RCB_PIP_TRUSTED_HOST=pypi.org

bash chemistry_toolbox/scripts/build_merged_environments.sh --from-lock all
```

The `--from-lock` option exactly replays the tested Conda artifacts. Pip-only
packages are then installed from the pinned/VCS requirements committed beside
each environment definition.

To solve the environments from the maintained specifications instead of the
Linux locks:

```bash
bash chemistry_toolbox/scripts/build_merged_environments.sh all
```

Build only selected environments by passing their specification names:

```bash
bash chemistry_toolbox/scripts/build_merged_environments.sh \
  general-modern-openmpi5 periodic-mpich
```

Use `--recreate` only when existing managed prefixes should be removed and
rebuilt:

```bash
bash chemistry_toolbox/scripts/build_merged_environments.sh \
  --recreate --from-lock all
```

### 4. Relocate or select the consolidated layout

The toolbox automatically selects the consolidated layout when all required
prefixes exist. Set the layout explicitly during deployment and validation:

```bash
export RESEARCHCHEM_ENV_LAYOUT=merged
```

The six environments may live on a separate data volume. Set the same root
while building and running:

```bash
export RCB_MERGED_ENV_ROOT=/data/researchchem-envs
bash chemistry_toolbox/scripts/build_merged_environments.sh --from-lock all
```

For a temporary controlled fallback, set
`RESEARCHCHEM_ENV_LAYOUT=legacy`. Do not use the legacy layout for a new
installation.

### 5. Configure models, scientific data, and native software

Conda environments do not contain the large external assets. Restore or
prepare these project-relative directories separately:

```text
.model_cache/       # MACE, NequIP, Allegro, and DeePMD models
.software_cache/    # pseudopotentials, parameter sets, native/licensed software
```

Licensed programs such as ORCA, Gaussian, VASP, AMBER, CHARMM, and LOBSTER
must be supplied legally by the operator. The tracked `config.local.env` is a
placeholder-only template; replace its values locally and never commit real
credentials.

After the assets and six environments are present, create the configured
executable links and verify registered checksums:

```bash
.toolbox_env/bin/python \
  chemistry_toolbox/scripts/configure_toolbox_resources.py --quick
```

Fill only the values needed on the current server:

```bash
chmod 600 config.local.env
```

### 6. Verify the installation

```bash
export RESEARCHCHEM_ENV_LAYOUT=merged
GENERAL_PYTHON="${RCB_MERGED_ENV_ROOT:-$PWD/.tool_envs_merged}/general-modern-openmpi5/bin/python"

"$GENERAL_PYTHON" -m chemistry_toolbox.mcp.tool_manager validate
"$GENERAL_PYTHON" chemistry_toolbox/scripts/check_mcp_tools.py --smoke
"$GENERAL_PYTHON" chemistry_toolbox/scripts/verify_toolbox.py --smoke --no-write
"$GENERAL_PYTHON" chemistry_toolbox/scripts/check_mcp_profile_envs.py \
  --check-models --no-write
```

Run the local no-API benchmark smoke after environment verification:

```bash
bash scripts/run_agent_eval.sh --agent mock \
  --task Electron_Isodensity_Reproduction_01_Method_Selection --no-score
```

The environment definitions, compatibility boundaries, and lock-maintenance
commands are documented in
[`chemistry_toolbox/environment/merged/README.md`](chemistry_toolbox/environment/merged/README.md).

## Architecture

```text
ResearchChemBench task instruction
        │
        ▼
isolated run workspace
        │
        ▼
Codex / Claude / OpenCode / Mock agent CLI
        │ MCP
        ▼
one complete Chemistry MCP server
        │
        ├── compact domain index + neutral Action/Backend/resource discovery
        ├── explicit execute_action transport for versioned Scientific/Data Actions
        ├── bounded atomic Data Actions
        ├── explicitly selectable BackendSpecs
        ├── software-native and programmable execution primitives
        └── no workflow tool, automatic backend, or fallback
        │
        ▼
report/report.md + tool artifacts + JSONL traces
        │
        ▼
dual-axis scientific LLM judge
```

The benchmark does **not** expose `run_ase`, `run_xtb`, `run_cp2k`, or other software/workflow runners. Agent CLIs own the reasoning loop; software packages are internal backends of scientifically named atomic actions.

## Run the benchmark

ResearchChemBench is self-contained at the source-code level. The evaluation
runner and Chemistry MCP server import only modules shipped in this repository;
no sibling ChemGraph checkout or `CHEMGRAPH_ROOT` setting is required.

Use `scripts/submit_evaluation.sh` for normal evaluations. It validates the
task list, writes an immutable submission configuration, launches the run in a
background `tmux` session, and provides status, stop, and summary commands.
Model and judge credentials are read from the local `config.local.env`.

Set the consolidated environment layout before submitting:

```bash
export RESEARCHCHEM_ENV_LAYOUT=merged
```

Preview a submission without calling an Agent or Judge:

```bash
bash scripts/submit_evaluation.sh submit \
  --dry-run \
  --model deepseek-v4-flash \
  --judge-model deepseek-v4-flash \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
```

Submit one scored task. The command returns after creating the background
`tmux` session:

```bash
bash scripts/submit_evaluation.sh submit \
  --model deepseek-v4-flash \
  --judge-model deepseek-v4-flash \
  --workspaces-dir workspaces/example_run \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
```

Submit multiple tasks to the same result root:

```bash
bash scripts/submit_evaluation.sh submit \
  --model deepseek-v4-flash \
  --judge-model deepseek-v4-flash \
  --workspaces-dir workspaces/reproduction_batch \
  --max-concurrent-runs 1 \
  GEOM_Hierarchical_Conformer_Reranking_Reproduction \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
```

The default per-task limits are 48 CPU cores, 204800 MiB memory, no GPU, a
10800-second compute Action/job timeout, a 14000-second MCP tool timeout, and a
14400-second Agent timeout. Override them explicitly when a different fixed
evaluation budget is required:

```bash
bash scripts/submit_evaluation.sh submit \
  --available-cpu-cores 48 \
  --available-memory-mb 204800 \
  --available-gpu-count 0 \
  --fast-action-timeout-seconds 240 \
  --compute-action-timeout-seconds 10800 \
  --mcp-tool-timeout-seconds 14000 \
  --timeout-seconds 14400 \
  --max-turns 200 \
  --workspaces-dir workspaces/fixed_budget_run \
  Electron_Isodensity_Reproduction_01_Method_Selection
```

Add `--no-score` to skip the Judge, `--foreground` for local debugging, or
`--follow` to display progress immediately after background submission. Use
`--tool-discovery-mode full` only for regression comparisons with the
historical eager Action surface; normal runs should keep the default
`progressive` mode.

The submit command prints the submission root and `tmux` session. Use those
values to inspect or control the run:

```bash
bash scripts/submit_evaluation.sh status \
  --run-root workspaces/example_run

bash scripts/submit_evaluation.sh follow \
  --run-root workspaces/example_run \
  --interval 30

bash scripts/submit_evaluation.sh attach \
  --session rcb_<printed_session_name>

bash scripts/submit_evaluation.sh stop \
  --session rcb_<printed_session_name>

bash scripts/submit_evaluation.sh summary \
  --run-root workspaces/example_run
```

List available Agents and tasks, or inspect all submission options:

```bash
bash scripts/run_agent_eval.sh --list-agents
bash scripts/run_agent_eval.sh --list-tasks
bash scripts/submit_evaluation.sh --help
```

`scripts/run_agent_eval.sh` remains available as the lower-level foreground
runner, but it is not the recommended interface for persistent benchmark
submissions.

Launch the Web UI:

```bash
.toolbox_env/bin/python -m evaluation
```

Open <http://localhost:5000>.

## Outputs

Every run creates a workspace containing:

```text
INSTRUCTIONS.md
data/
code/
outputs/
report/report.md
_agent_output.jsonl
_tool_trace.jsonl
_tool_results/
_tool_artifacts/
_meta.json
_score.json
```

The default `progressive` discovery mode initially exposes a compact set of
catalog search/inspection tools, one explicit Action dispatcher, and the
software-native/program execution primitives. `search_actions` and
`inspect_action` reveal exact contracts on demand. This changes context loading
only: there is no task-specific filtering, ranking, backend selection, or
fallback. Set `--tool-discovery-mode full` to reproduce the historical eager
surface.

## Documentation

- [Environment and chemistry tool configuration](docs/ENVIRONMENT_AND_TOOLS.md)
- [工具箱可复现环境配置](docs/TOOLBOX_SETUP.md)
- [原子工具完整目录](chemistry_toolbox/mcp/TOOL_CATALOG.md)
- [重构实施总结](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_REFACTOR_REPORT.md)
- [工具、后端与资源完整矩阵](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md)
- [软件能力与候选能力矩阵](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md)
- [能力扩展实施计划](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_CAPABILITY_EXPANSION_PLAN.md)
- [2026-07-20 能力扩展总结报告](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_CAPABILITY_EXPANSION_REPORT_20260720.md)
- [用户请求软件配置状态](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md)
- [六个 Heterobiaryl P(V) 任务验证台账](docs/verification/HETEROBIARYL_PV_SIX_TASK_VERIFICATION_20260722.md)
- [当前 Actions、Backends 与软件能力目录](docs/verification/CHEMISTRY_TOOLBOX_CURRENT_CAPABILITY_CATALOG_20260722.md)
- [Action–Backend 233个组合完整测试与软件接入审计](chemistry_toolbox/docs/ACTION_BACKEND_COMPLETE_AUDIT_20260721.md)
- [11个失败组合修复与PubChem连通性报告](chemistry_toolbox/docs/ACTION_BACKEND_REPAIR_REPORT_20260721.md)
- [MCP 后端运行环境](docs/MCP_PROFILE_ENVIRONMENTS.md)
- [MCP 多环境当前检查状态](chemistry_toolbox/docs/MCP_PROFILE_STATUS.md)
- [工具箱实现说明](docs/TOOLBOX_IMPLEMENTATION.md)
- [逐工具测试结果与未配置软件手动配置](docs/TOOL_TEST_AND_MANUAL_CONFIGURATION.md)
- [工具箱实际状态报告](chemistry_toolbox/docs/TOOLBOX_STATUS.md)
- [MCP 工具编写、增删、打包与 Agent 一键安装](docs/MCP_TOOLS_DEVELOPMENT_AND_INSTALLATION.md)
- [化学工具箱自动配置与可迁移部署](chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_PORTABLE_BOOTSTRAP.md)
- [Running agents and evaluations](docs/RUNNING_EVALUATIONS.md)
- [Persistent evaluation submission commands](scripts/submit_evaluation.md)
- [Detailed ResearchClawBench → ResearchChemBench code changes](docs/RESEARCHCLAWBENCH_CODE_CHANGES.md)
- [Initial validation report, including live DeepSeek Agent/judge results](docs/VALIDATION_REPORT.md)

## Important limitations

- Initial release is an open-agent benchmark, not a hardened container sandbox.
- Codex has workspace-write shell access and may use non-MCP methods unless stronger isolation is added.
- MACE/CHGNet and other MLIP calculations require a reviewed model and may be expensive.
- PubChem, RCSB, Catalysis-Hub, and Materials Project lookups require network access; Materials Project also needs `MP_API_KEY`.
- Registered wrappers for unavailable/licensed software return structured `unavailable`; registration does not mean that backend is installed.
- The initial judge is an LLM-based binary evaluator; deterministic chemistry scorers are future work.
