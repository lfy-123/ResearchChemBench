# ResearchChemBench

ResearchChemBench evaluates whether external autonomous agents such as Codex CLI, Claude Code, and OpenCode can independently compose atomic chemistry tools to solve scientific tasks. Every task receives the same complete toolbox; the agent chooses the actions, call order, software backend, method, parameters, failure recovery, and stopping point.

## Architecture

```text
ChemGraph task instruction
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
        ├── 40 atomic Scientific Actions
        ├── 4 atomic Data Actions
        ├── 45 explicitly selectable BackendSpecs
        └── no workflow tool, automatic backend, or fallback
        │
        ▼
report/report.md + tool artifacts + JSONL traces
        │
        ▼
ChemGraph-style binary LLM judge
```

The benchmark does **not** expose `run_ase`, `run_xtb`, `run_cp2k`, or other software/workflow runners. Agent CLIs own the reasoning loop; software packages are internal backends of scientifically named atomic actions.

## Quick start

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
bash scripts/setup_toolbox_env.sh
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py --continue-on-error
cp config.local.env.example config.local.env
```

The installer registers the project environments as `researchchem-*` Conda names. Verify or
activate them with:

```bash
conda env list | grep researchchem
conda activate researchchem-quantum
```

This installs chemistry dependencies into the ResearchChemBench environment but does not install or write into the sibling ChemGraph checkout. Its source is loaded from `CHEMGRAPH_ROOT/src` at runtime.

Run the local no-API smoke benchmark:

```bash
bash scripts/run_agent_eval.sh --agent mock --task ChemGraph_001 --no-score
```

Preview a Codex run without executing it:

```bash
python -m evaluation.cli_eval eval_configs/quick_codex.yaml --dry-run --no-score
```

Run a real Agent task:

```bash
bash scripts/run_agent_eval.sh --agent codex --task ChemGraph_001 --no-score
bash scripts/run_agent_eval.sh --agent claude --task ChemGraph_003 --no-score
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_001 --no-score

# Every run exposes the same full 44-action catalog.
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_001 --no-score
```

Set judge credentials and omit `--no-score` to score the run.

List all parameters, Agents, or tasks:

```bash
bash scripts/run_agent_eval.sh --help
bash scripts/run_agent_eval.sh --list-agents
bash scripts/run_agent_eval.sh --list-tasks
```

Launch the Web UI:

```bash
python -m evaluation
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

## Documentation

- [Environment and chemistry tool configuration](docs/ENVIRONMENT_AND_TOOLS.md)
- [工具箱可复现环境配置](docs/TOOLBOX_SETUP.md)
- [原子工具完整目录](evaluation/mcp_tools/TOOL_CATALOG.md)
- [重构实施总结](docs/tools/CHEMISTRY_TOOLBOX_REFACTOR_REPORT.md)
- [MCP 后端运行环境](docs/MCP_PROFILE_ENVIRONMENTS.md)
- [MCP 多环境当前检查状态](docs/MCP_PROFILE_STATUS.md)
- [工具箱实现说明](docs/TOOLBOX_IMPLEMENTATION.md)
- [逐工具测试结果与未配置软件手动配置](docs/TOOL_TEST_AND_MANUAL_CONFIGURATION.md)
- [工具箱实际状态报告](docs/TOOLBOX_STATUS.md)
- [MCP 工具编写、增删、打包与 Agent 一键安装](docs/MCP_TOOLS_DEVELOPMENT_AND_INSTALLATION.md)
- [Running agents and evaluations](docs/RUNNING_EVALUATIONS.md)
- [Detailed ResearchClawBench → ResearchChemBench code changes](docs/RESEARCHCLAWBENCH_CODE_CHANGES.md)
- [Initial validation report, including live DeepSeek Agent/judge results](docs/VALIDATION_REPORT.md)

## Important limitations

- Initial release is an open-agent benchmark, not a hardened container sandbox.
- Codex has workspace-write shell access and may use non-MCP methods unless stronger isolation is added.
- MACE/CHGNet and other MLIP calculations require a reviewed model and may be expensive.
- PubChem, RCSB, Catalysis-Hub, and Materials Project lookups require network access; Materials Project also needs `MP_API_KEY`.
- Registered wrappers for unavailable/licensed software return structured `unavailable`; registration does not mean that backend is installed.
- The initial judge is an LLM-based binary evaluator; deterministic chemistry scorers are future work.
