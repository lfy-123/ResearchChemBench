# Environment and Chemistry Tool Configuration

> The root [README](../README.md) and [TOOLBOX_SETUP.md](TOOLBOX_SETUP.md)
> define the authoritative seven-environment reconstruction procedure.

## 1. Repository layout

ResearchChemBench is a self-contained source checkout:

```text
ResearchChemBench/
├── evaluation/
├── chemistry_toolbox/
├── tasks/
└── scripts/
```

The evaluation runner and Chemistry MCP server load only code shipped in this
repository. No sibling ChemGraph checkout or ChemGraph-specific Python path is
required.

## 2. Environment layout

Use the framework environment plus the six chemistry environments under the
repository `.envs/` directory. No alternate environment layout is supported.

```bash
cd /path/to/ResearchChemBench
bash chemistry_toolbox/scripts/setup_toolbox_env.sh --from-lock --skip-verify
bash chemistry_toolbox/scripts/build_environments.sh --from-lock all
```

The framework is `.envs/researchchembench`; all chemistry runtimes map directly
to one of the other six prefixes. Exact Linux locks, maintained specifications,
and pip requirements are kept under `chemistry_toolbox/environment/`. See the
root README and `TOOLBOX_SETUP.md` for reconstruction and external-asset steps.

Run tests with the framework interpreter:

```bash
.envs/researchchembench/bin/python -m pytest -q
```

Real Chemistry MCP startup requires the relevant chemistry dependencies and any
operator-supplied licensed executables, model caches, or scientific resources.

## 3. Environment file

Edit the placeholder-only root configuration and restrict its permissions:

```bash
chmod 600 config.local.env
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

`config.local.env` is automatically loaded by the shell runner and MCP profile
loader. The repository copy contains placeholders only; never commit real keys.

## 4. Calculator requirements

The paper-derived task set may use lookup services, quantum chemistry,
periodic-structure codes, conformer tools, thermochemistry, and ML potentials.
Each task declares its scientific inputs and required deliverables; backend
availability is reported by the Chemistry MCP catalog.

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

The toolbox supports `mace-torch`. The first calculation using a model such as
`medium-mpa-0` may download model weights and can consume substantial memory and runtime.

ResearchChemBench stores downloaded weights under the ignored project directory
`.model_cache/mace/`, rather than under `chemistry_toolbox/mcp/` or an Agent CLI's
global cache. Set `RESEARCHCHEMBENCH_MODEL_CACHE` in `config.local.env` to override
the cache root.

Verify the Python package:

```bash
python -c 'import mace; print(mace.__file__)'
```

For an initial Agent integration test, use the Mock Agent task shown in the root
README before running expensive chemistry calculations.

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

After installation, verify the runtime catalog and configured resources:

```bash
.envs/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/check_mcp_profile_envs.py --check-models --no-write
```

The command checks every physical runtime's modules, commands, and optional
models. `tool_manager validate` additionally checks Action, BackendSpec, and MCP
registration contracts.

Run a local no-network functional smoke test:

```bash
.envs/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/check_mcp_tools.py --smoke
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
