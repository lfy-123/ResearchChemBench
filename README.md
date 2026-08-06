# ResearchChemBench

ResearchChemBench evaluates whether external autonomous agents such as Codex CLI, Claude Code, and OpenCode can independently compose atomic chemistry tools to solve scientific tasks. Every task can discover the same complete toolbox; the agent chooses the actions, call order, software backend, method, parameters, failure recovery, and stopping point. The default MCP surface loads the catalog progressively so unused Action schemas do not consume every model turn.

## Build the environments

ResearchChemBench uses one project environment and seven consolidated chemistry
environments. All eight environments are managed with Conda or Mamba, with
selected Python-only packages installed by pip.

A fresh installation keeps every environment under the repository-level
`.envs/` directory:

```text
ResearchChemBench/
├── .envs/
│   ├── researchchembench
│   ├── general-modern-openmpi5
│   ├── molecular-simulation-openff
│   ├── kinetics-legacy
│   ├── equivariant-ml
│   ├── periodic-mpich
│   ├── yambo-openmpi4
│   └── gmx-mmpbsa
```

| Environment | Prefix under `.envs/` | Main responsibility |
|---|---|---|
| ResearchChemBench framework | `researchchembench` | Evaluation CLI, Agent orchestration, project administration, tests, and bootstrap utilities |
| General | `general-modern-openmpi5` | MCP server, cheminformatics, quantum chemistry, materials analysis, and most native entry points |
| Molecular simulation | `molecular-simulation-openff` | OpenFF, AmberTools, OpenMM, GROMACS, HOOMD, free-energy analysis, and docking |
| Reaction and kinetics | `kinetics-legacy` | RMG, Arkane, KinBot, Sella, ABINIT, and LAMMPS |
| Equivariant ML | `equivariant-ml` | DeePMD, NequIP, Allegro, CPU PyTorch, and e3nn |
| Periodic MPICH | `periodic-mpich` | CP2K 2026.1 with the isolated MPICH 5 and libxc 7 stack |
| CatMAP and Yambo | `yambo-openmpi4` | CatMAP, ASE 3.17, Yambo, and OpenMPI 4 compatibility runtime |
| gmx_MMPBSA | `gmx-mmpbsa` | gmx_MMPBSA 1.6.5, AmberTools 23.6, GROMACS, and its compatible Python 3.11/NumPy 1.x stack |

### 1. Prerequisites

Use a Linux x86-64 host with Conda or Mamba available. Mamba is recommended.
The committed explicit locks reproduce the tested `linux-64` Conda artifacts
for the framework and all seven chemistry environments. On another operating
system or CPU architecture, solve from the maintained specifications instead.

Optional GUI and native smoke tests also use the Debian/Ubuntu packages listed
in `chemistry_toolbox/environment/merged/system-requirements.txt`:

```bash
sudo apt-get update
sudo apt-get install -y xauth xvfb libxkbcommon0 libgtk-3-0
```

### 2. Rebuild all eight environments

For a Linux x86-64 host, run the following commands from a fresh repository
checkout. This is the tested reconstruction path for the current layout:

```bash
git clone git@github.com:lfy-123/ResearchChemBench.git
cd ResearchChemBench

export RCB_PIP_INDEX_URL=https://pypi.org/simple
export RCB_PIP_TRUSTED_HOST=pypi.org

mkdir -p "$PWD/.envs"

bash chemistry_toolbox/scripts/setup_toolbox_env.sh \
  --env-dir "$PWD/.envs/researchchembench" \
  --from-lock --skip-verify

bash chemistry_toolbox/scripts/build_merged_environments.sh \
  --from-lock all
```

`setup_toolbox_env.sh --from-lock` replays the framework Conda lock, installs
the pinned direct pip dependencies and editable project package, checks package
consistency, and caches the English MiniLM retrieval model under `.model_cache`.
`build_merged_environments.sh --from-lock all` replays the seven chemistry Conda
locks, installs each runtime's pinned pip requirements, applies the pinned
KinBot portability patch, and enforces the documented compatibility-warning
allowlists. No `.venv`, `.toolbox_env`,
`.tool_envs`, `.tool_envs_merged`, or `.conda_envs` directory is required.

For a different platform, omit `--from-lock` so Conda resolves the maintained
specifications. This creates a compatible installation, not an exact replay of
the tested Linux artifacts:

```bash
bash chemistry_toolbox/scripts/setup_toolbox_env.sh \
  --env-dir "$PWD/.envs/researchchembench" --skip-verify
bash chemistry_toolbox/scripts/build_merged_environments.sh all
```

The standard `.envs/` layout needs no environment-variable configuration. All
build, evaluation, and submission code uses the consolidated repository
`.envs/` directory. Set `RESEARCHCHEMBENCH_ENV_ROOT=/another/path` only when
deliberately relocating all eight environments. Set
`RESEARCHCHEMBENCH_FRAMEWORK_ENV` only when the framework environment must be
placed outside that common root.

Build only selected environments by passing their specification names:

```bash
bash chemistry_toolbox/scripts/build_merged_environments.sh \
  general-modern-openmpi5 periodic-mpich
```

Use `--recreate` only when an existing managed prefix should be removed and
rebuilt:

```bash
bash chemistry_toolbox/scripts/build_merged_environments.sh \
  --recreate --from-lock all
```

The committed `*.pip-freeze.txt` files are audit inventories, not installation
inputs. Use the two build scripts above; they select the locks, maintained
requirements, target names, and compatibility policy consistently.

### 3. Restore local configuration and external assets

Create the ignored local configuration from the tracked template and provide
only the credentials needed on the target host. Never commit real credentials:

```bash
cp config.local.env.example config.local.env
chmod 600 config.local.env
${EDITOR:-vi} config.local.env
```

The public repository does not include large model weights, pseudopotentials,
third-party native distributions, licensed executables, or credentials. Place
operator-supplied resources in these project-relative directories when the
corresponding backend is required:

```text
.model_cache/
.software_cache/
```

Licensed software must be obtained and used under its applicable license. The
environment build does not download or activate commercial programs. When
migrating an existing installation, copy `.model_cache/` and `.software_cache/`
to the repository root before resource configuration. The MiniLM retrieval
model is recreated automatically; chemistry model weights and licensed software
must be restored separately.

After optional resources are present, create the configured executable links
and verify registered checksums:

```bash
.envs/researchchembench/bin/python \
  chemistry_toolbox/scripts/configure_toolbox_resources.py --quick
```

#### Cache and host portability checklist

Copying `.software_cache/` and `.model_cache/` can avoid large downloads, but
the copied directories are not a complete installation and must not be treated
as proof that every backend is runnable. Use the following checklist after
moving a checkout to another server:

1. Apply the site network proxy before any Conda, pip, curl, Agent, or Judge
   request. At PJLab the tested setup command is:

   ```bash
   source <(curl -sSL \
     http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh)
   ```

2. Build or restore all eight `.envs/` prefixes. The two cache directories do
   not contain the framework environment or the seven consolidated chemistry
   environments.
3. Run `configure_toolbox_resources.py --quick` after copying caches. It
   resolves project-relative resources, checks registered hashes, and reports
   executables or shared libraries that are still missing.
4. Verify native programs under the same runtime profile used by the toolbox.
   A copied executable may retain an RPATH or prefix from its original host.
   MPI installations in particular may require their configured `PATH`,
   `LD_LIBRARY_PATH`, and `OPAL_PREFIX`; a bare `mpirun --version` is not a
   sufficient portability check.
5. Recheck GPU backends against the target host's driver and CUDA/cuDNN
   libraries. A cached binary such as GNINA can be present while remaining
   unusable because a required `libcudnn.so` version is absent.
6. Keep `config.local.env` local and permission-restricted. Copy the placeholder
   names, not credentials, into documentation or commits.

Agent CLIs are also host-level dependencies rather than model-cache assets.
For example, an OpenCode evaluation requires an actual `opencode` executable;
`.model_cache/opencode/` may contain helper assets without containing the CLI.
Install and verify it separately when it is selected as the Agent:

```bash
curl -fsSL https://opencode.ai/install | bash
export PATH="$HOME/.opencode/bin:$PATH"
opencode --version
opencode run --help
```

The tested ResearchChemBench invocation requires the OpenCode `run` command to
support `--pure`, `--dir`, `--model`, `--format`, and `--auto`.

### 4. Verify the reconstruction

The build scripts execute package checks. Six environments should report no
broken requirements when checked directly:

```bash
for name in \
  researchchembench \
  general-modern-openmpi5 \
  molecular-simulation-openff \
  equivariant-ml \
  periodic-mpich \
  gmx-mmpbsa
do
  "$PWD/.envs/$name/bin/python" -m pip check
done
```

`kinetics-legacy` retains three legacy package platform-metadata warnings
(`quantities`, `gprof2dot`, and `periodictable`), and `yambo-openmpi4` retains
the required ASE 3.17 platform-metadata warning. The seven-environment build
script rejects every other `pip check` error.

Run the toolbox validation suite:

```bash
GENERAL_PYTHON="$PWD/.envs/general-modern-openmpi5/bin/python"

"$GENERAL_PYTHON" -m chemistry_toolbox.mcp.tool_manager validate
"$GENERAL_PYTHON" chemistry_toolbox/scripts/check_mcp_tools.py --smoke
"$GENERAL_PYTHON" chemistry_toolbox/scripts/verify_toolbox.py --smoke --no-write
"$GENERAL_PYTHON" chemistry_toolbox/scripts/check_mcp_profile_envs.py \
  --check-models --no-write
```

Finally, run a local benchmark smoke that does not call an external Agent API:

```bash
bash scripts/run_agent_eval.sh --agent mock \
  --task Electron_Isodensity_Reproduction_01_Method_Selection --no-score
```

An installation is considered ready only after package checks, toolbox smoke
tests, and representative calculations for the enabled native backends pass.

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

Before submission, inspect the CPU affinity and available memory of the current
server instead of relying on the repository defaults:

```bash
nproc
taskset -pc $$
free -m
```

Pass the usable values explicitly with `--available-cpu-cores`,
`--available-memory-mb`, and `--available-gpu-count`. These values define the
per-task evaluator budget; they do not force every backend to consume the whole
budget. Keep `--max-concurrent-runs 1` for a single validation task, or choose a
higher value only after ensuring the sum of concurrent reservations fits the
host.

Load the local configuration into the environment without printing secrets:

```bash
set -a
source config.local.env
set +a
```

When a long-lived tmux server already exists, update its global environment
before submitting so background Agent and Judge processes inherit the proxy and
Agent CLI path:

```bash
for name in \
  http_proxy https_proxy no_proxy \
  HTTP_PROXY HTTPS_PROXY NO_PROXY PATH
do
  value="${!name-}"
  if [ -n "$value" ]; then
    tmux set-environment -g "$name" "$value"
  fi
done
```

Always run a dry submission first. It checks task names, resource flags,
credentials, generated Agent configuration, and workspace layout without
calling the Agent or Judge:

```bash
bash scripts/submit_evaluation.sh submit \
  --dry-run \
  --agent opencode \
  --model "$OPENCODE_MODEL_VALUE" \
  --judge-model "$JUDGE_MODEL_NAME" \
  --available-cpu-cores "$(nproc)" \
  --available-memory-mb 30000 \
  --available-gpu-count 0 \
  --max-concurrent-runs 1 \
  --workspaces-dir workspaces/preflight \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
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
  --max-turns 600 \
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
.envs/researchchembench/bin/python -m evaluation
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
- [工具箱实现说明](docs/TOOLBOX_IMPLEMENTATION.md)
- [逐工具测试结果与未配置软件手动配置](docs/TOOL_TEST_AND_MANUAL_CONFIGURATION.md)
- [工具箱实际状态报告](chemistry_toolbox/docs/TOOLBOX_STATUS.md)
- [MCP 工具编写、增删、打包与 Agent 一键安装](docs/MCP_TOOLS_DEVELOPMENT_AND_INSTALLATION.md)
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
