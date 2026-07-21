# Environment and Chemistry Tool Configuration

> Current deployment uses dependency-isolated MCP profiles. See
> [MCP_PROFILE_ENVIRONMENTS.md](MCP_PROFILE_ENVIRONMENTS.md) for the authoritative
> architecture and [MCP_PROFILE_STATUS.md](../chemistry_toolbox/docs/MCP_PROFILE_STATUS.md) for live status.

## 1. Repository layout

ResearchChemBench expects the following sibling checkout layout by default:

```text
benchmark/
├── ChemGraph/
├── ResearchClawBench/
└── ResearchChemBench/
```

No source files in the two reference repositories are modified. ResearchChemBench imports ChemGraph code from `../ChemGraph/src` and runs its own benchmark-specific MCP wrappers.

Override the default ChemGraph location with:

```bash
export CHEMGRAPH_ROOT=/absolute/path/to/ChemGraph
```

## 2. Recommended Python environment

Use `.toolbox_env` for the benchmark runner/core tools, then create the isolated MCP
profile environments. ChemGraph source is loaded directly from `CHEMGRAPH_ROOT/src`.

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

bash chemistry_toolbox/scripts/setup_toolbox_env.sh
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py --continue-on-error
```

The conda-forge package list, pip package list, and ABI-sensitive pins are kept under `environment/`. See `TOOLBOX_SETUP.md` for all setup options and the actual installed/unavailable backend split.

If only the runner and Mock Agent tests are needed:

```bash
pip install -e '.[test]'
pytest -q
```

Real Chemistry MCP startup requires access to `CHEMGRAPH_ROOT/src` and the relevant chemistry dependencies in `CHEMGRAPH_PYTHON`.

## 3. Environment file

Copy the root-level local configuration template:

```bash
cp config.local.env.example config.local.env
```

Important fields:

```env
JUDGE_API_KEY="sk-xxx"
JUDGE_API_BASE="https://api.openai.com/v1"
JUDGE_MODEL_NAME="gpt-5.1"

MP_API_KEY=""
OPENAI_API_KEY=""

RESEARCHCHEMBENCH_AGENT_TIMEOUT_SECONDS="7200"
RESEARCHCHEMBENCH_MAX_TURNS="200"
```

`config.local.env` is ignored by version control and automatically loaded by the shell runner
and MCP profile loader. Never put real keys in `config.local.env.example`.

## 4. Calculator requirements

The imported task set uses two important calculator families:

| Runtime requirement | Count | Task IDs |
|---|---:|---|
| PubChem lookup only | 4 | `ChemGraph_001`–`ChemGraph_004` |
| MACE-MP (`medium-mpa-0`) | 16 | `005`, `006`, `009`, `012`, `015`, `017`, `019`, `021`, `022`, `025`, `029`, `031`, `033`, `035`, `037`, `039` |
| TBLite / GFN2-xTB | 20 | `007`, `008`, `010`, `011`, `013`, `014`, `016`, `018`, `020`, `023`, `024`, `026`, `027`, `028`, `030`, `032`, `034`, `036`, `038`, `040` |

The abbreviated numeric IDs in the last two rows all use the `ChemGraph_` prefix.

### TBLite / GFN2-xTB

Install through the ResearchChemBench chemistry extra or the explicit requirements file:

```bash
pip install -e '.[chemistry]'
# or: pip install -r evaluation/requirements-chemistry.txt
```

Verify:

```bash
python -c 'import tblite; print(tblite.__version__)'
```

### MACE-MP

ChemGraph declares `mace-torch`. The first calculation using a model such as `medium-mpa-0` may download model weights and can consume substantial memory and runtime.

ResearchChemBench stores downloaded weights under the ignored project directory
`.model_cache/mace/`, rather than under `chemistry_toolbox/mcp/` or an Agent CLI's
global cache. Set `RESEARCHCHEMBENCH_MODEL_CACHE` in `config.local.env` to override
the cache root.

Verify the Python package:

```bash
python -c 'import mace; print(mace.__file__)'
```

For an initial Agent integration test, prefer a SMILES lookup task before running MACE calculations.

## 5. Network requirements

`molecule_name_to_smiles` uses PubChem and therefore requires outbound network access. Model downloads may also require network access.

On a proxied system, configure the standard variables before launching the benchmark:

```bash
export HTTP_PROXY=http://proxy.example:3128
export HTTPS_PROXY=http://proxy.example:3128
export NO_PROXY=127.0.0.1,localhost
```

For local persistent PubChem access, store a PubChem-only proxy in the ignored
`config.local.env` file without changing the proxy behavior of other services:

```bash
RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL=http://proxy.example:3128
```

PubChem actions and
`chemistry_toolbox/scripts/check_pubchem_connectivity.py` load only the proxy
variables from this file when no proxy is already exported. Set
`RESEARCHCHEMBENCH_PUBCHEM_PROXY_MODE=off` to disable this local auto-loading.

For local Streamable HTTP MCP, ensure localhost is excluded from the proxy.

## 6. Agent CLI setup

### Codex CLI

Verify installation and authentication:

```bash
codex --version
codex login status
```

ResearchChemBench runs Codex with:

```text
codex exec
--ignore-user-config
--skip-git-repo-check
--sandbox workspace-write
--json
```

The benchmark injects a per-run MCP server through `-c mcp_servers...` overrides. It does not modify global `~/.codex/config.toml`.

### Claude Code

Verify installation and authentication:

```bash
claude --version
claude auth status
```

For each run, ResearchChemBench generates:

```text
workspace/.mcp.json
```

Claude is started with `--strict-mcp-config`, so only the benchmark MCP configuration is loaded. Built-in tools are restricted to reading and writing workspace files; Chemistry MCP tools are separately allowed with dynamically generated server-scoped rules such as `mcp__researchchem_services__*`. Slash commands are disabled and session persistence is disabled for benchmark isolation.

### OpenCode with an OpenAI-compatible API

Verify the CLI:

```bash
opencode --version
```

The default preset uses DeepSeek V4 Flash through the OpenAI-compatible endpoint:

```bash
export OPENAI_API_KEY=...
export RESEARCHCHEMBENCH_OPENCODE_BASE_URL=https://api.deepseek.com/v1
export RESEARCHCHEMBENCH_OPENCODE_MODEL=deepseek/deepseek-v4-flash
```

ResearchChemBench writes a run-local `opencode.json` containing the provider metadata and Chemistry MCP command, but never writes the API key into that file. OpenCode is invoked with `--pure`, JSON output, the run workspace as `--dir`, and non-interactive permission approval.

## 7. Chemistry MCP servers

The server is implemented at:

```text
chemistry_toolbox/mcp/server.py
chemistry_toolbox/mcp/tools/*.py
```

The 41 auto-discovered tools are divided across task-selectable, namespaced MCP servers.
Tool source remains one-file-per-tool; `chemistry_toolbox/config/mcp_profiles.yaml` owns only environment and
server grouping. The authoritative tool list is generated at
`chemistry_toolbox/mcp/TOOL_CATALOG.md`.

The MCP wrappers call ChemGraph core functions rather than ChemGraph's LangGraph workflow. Each public tool has one self-describing file with a `TOOL_SPEC`; `registry.py` discovers those files automatically, while the explicit allow-list in `tool_config.json` controls which reviewed tools are enabled. The whole `mcp_tools/` directory remains an independently installable package. See `MCP_TOOLS_DEVELOPMENT_AND_INSTALLATION.md` for tool lifecycle management and extension guidance.

## 8. MCP workspace confinement

Every MCP process receives:

```env
RESEARCHCHEMBENCH_WORKSPACE=/absolute/run/workspace
RESEARCHCHEMBENCH_RUN_ID=<run-id>
```

All tool file paths are resolved against this directory. Any `../` or absolute path escaping the workspace is rejected.

The wrapper also snapshots files changed by each call into:

```text
_tool_artifacts/<sequence>/
```

and records hashes in `_tool_trace.jsonl`.

## 9. MCP validation

After installation, verify every profile with its own interpreter:

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_profile_envs.py --live-materials-project
```

The command checks that all 41 enabled tool names are assigned exactly once and that every
profile can import its required modules and find its required commands. `tool_manager validate`
additionally checks each tool file and `TOOL_SPEC` registration contract.

Run a local no-network functional smoke test:

```bash
python chemistry_toolbox/scripts/check_mcp_tools.py --smoke
```

This executes calculator → water SMILES/XYZ → ASE/EMT energy → JSON extraction and verifies the canonical trace, full results, and artifact snapshots. Run `python chemistry_toolbox/scripts/verify_toolbox.py` for the broader real-backend/API status report.

Run the complete test suite:

```bash
pytest -q
```

Tests marked `integration` or `agent` should be run explicitly only when chemistry dependencies, credentials, and compute resources are available.

## 10. Judge configuration

The judge is independent from Agent CLI authentication. It uses an OpenAI-compatible Chat Completions endpoint.

`JUDGE_API_KEY` is removed from the environment passed to the tested Agent subprocess. Codex/Claude authentication variables and their normal credential stores remain available to the respective CLI.

Because this initial release is not a container boundary, a same-user Agent with broad
filesystem-read capability could still try to read `config.local.env` outside its workspace.
For sensitive leaderboard credentials, prefer a separate scoring process/container or inject
short-lived credentials through an external secret manager.

Required variables:

```env
JUDGE_API_KEY=...
JUDGE_API_BASE=...
JUDGE_MODEL_NAME=...
```

If they are absent, run with:

```bash
--no-score
```

Agent outputs and process files are still preserved and can be scored later from the Web UI or by calling `evaluation.score.score_workspace()`.
