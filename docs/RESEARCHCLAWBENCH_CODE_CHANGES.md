# ResearchClawBench → ResearchChemBench Detailed Code-Change Audit

## 1. Purpose and scope

This document records how the initial ResearchChemBench implementation was derived from ResearchClawBench and where ChemGraph is reused. It is intended to support a file-by-file code review.

ResearchChemBench has a deliberately split architecture:

- ResearchClawBench supplies the benchmark-harness pattern: task directories, isolated run workspaces, external Agent execution, persisted process output, a Web UI, batch evaluation, and run reports.
- ChemGraph supplies the chemistry task set, reference answers, tool schemas, and chemistry implementations.
- ResearchChemBench supplies the adapter layer: Agent CLI adapters, MCP exposure, workspace confinement, canonical tool traces, ChemGraph-style scoring, and chemistry-specific documentation/tests.

ResearchChemBench does **not** run ChemGraph's LangGraph workflow. Codex CLI or Claude Code owns the reasoning/action loop and calls the Chemistry MCP server directly.

## 2. Reference repositories and non-modification guarantee

The implementation was created in:

```text
${PROJECT_ROOT}
```

The two sibling reference repositories were treated as read-only:

```text
../ResearchClawBench
../ChemGraph
```

Observed reference revisions at the end of implementation:

| Repository | Git revision |
|---|---|
| ResearchClawBench | `6bfca049f050cae559228e713cea61f9c86acc43` |
| ChemGraph | `2f35bde48ce6d45cf2cd046ac754bb85badf2105` |

ResearchClawBench was clean when checked. ChemGraph already contained local modified/untracked files in the shared workspace; ResearchChemBench implementation did not write to them. In particular, no patch in this implementation targeted a path under `ChemGraph/` or `ResearchClawBench/`.

The initial framework copy excluded:

- `.git/`, so ResearchChemBench is independent of ResearchClawBench Git metadata;
- `ResearchClawBench/tasks/`, because paper-reproduction tasks are not part of this benchmark;
- `ResearchClawBench/workspaces/`, because previous Agent runs must not leak into the new benchmark;
- Python bytecode/cache directories.

ChemGraph tasks were converted by reading its source ground-truth file and writing new, benchmark-owned task files under `ResearchChemBench/tasks/`.

## 3. Top-level architectural difference

### 3.1 ResearchClawBench execution model

ResearchClawBench is designed around open-ended scientific research/reproduction tasks:

```text
task + data + related papers
        ↓
research Agent / ResearchHarness
        ↓
code + figures + research report
        ↓
weighted checklist and image/text LLM judge
```

The original generic `TaskRunner` accepts a shell command template, replaces `<PROMPT>` and `<WORKSPACE>`, and executes it with `shell=True`. Its scorer compares a report and generated images with a paper-derived checklist on a 0–100 scale.

### 3.2 ResearchChemBench execution model

ResearchChemBench tests autonomous chemistry-tool use:

```text
ChemGraph natural-language task
        ↓
per-run workspace + chemistry-specific INSTRUCTIONS.md
        ↓
Codex CLI / Claude Code / Mock Agent
        ↓ MCP stdio
traced ResearchChemBench Chemistry MCP server
        ↓
ChemGraph chemistry core functions
        ↓
report/report.md + raw Agent output + tool results + artifact snapshots
        ↓
ChemGraph-style binary LLM judge over answer and tool sequence
```

The key design change is ownership of the loop:

- ChemGraph's original `LLMAgent` + LangGraph workflow owns graph nodes, state, checkpoints, interruption, and tool dispatch.
- ResearchChemBench does not instantiate that workflow.
- The external Agent CLI owns planning, retries, context, and termination.
- MCP is the stable tool boundary between the Agent and ChemGraph chemistry functions.
- ResearchChemBench owns run isolation, traces, artifacts, completion checks, and evaluation.

## 4. File-level change summary

The following table is the main review index.

| Path | Status relative to copied ResearchClawBench | Review summary |
|---|---|---|
| `.github/workflows/tests.yml` | Modified | Replaced old unittest/StructAI dependency setup with editable package install and `pytest -q`. |
| `.gitignore` | Modified | Keeps benchmark workspaces, virtual environments, private configs, Claude state, and caches out of version control. |
| `CONTRIBUTING.md` | Rewritten | Replaced ResearchClawBench contribution text with ResearchChemBench invariants and test procedure. |
| `LICENSE` | Retained | Retains the copied upstream license. |
| `README.md` | Rewritten | Describes chemistry MCP architecture, setup, runs, outputs, and limitations. |
| `assets/` | Retained | Copied visual assets are retained; the simplified initial UI does not depend on most of them. |
| `pyproject.toml` | Added | Defines the installable `researchchembench` package, dependencies, scripts, and pytest markers. |
| `rcb-eval` | Removed | Old ResearchClawBench launcher was not carried forward. |
| `rcb-clear` | Removed | Old paper-task cleanup launcher was not carried forward. |
| `rchem-eval` | Added | Thin ResearchChemBench evaluation launcher. |
| `eval_configs/*.yaml` | Replaced | ResearchHarness examples were replaced by Mock, Codex, Claude, OpenCode/DeepSeek, and full chemistry suites. |
| `evaluation/.env.example` | Rewritten | Separates judge credentials from Agent CLI auth and adds ChemGraph/MCP interpreter settings. |
| `evaluation/agents.json` | Rewritten | Defines `mock`, `codex`, `claude`, and OpenCode/DeepSeek presets with explicit adapter kinds. |
| `evaluation/cli_clear.py` | Removed | Its assumptions about duplicated paper data and `related_work/` do not apply to this initial benchmark. |
| `evaluation/cli_eval.py` | Rewritten | Adds simple Agent × task × repeat expansion, concurrency, scoring, dry-run, and JSON/Markdown reports. |
| `evaluation/config.py` | Rewritten | Loads `evaluation/.env` and adds overridable ChemGraph/task/workspace paths, limits, judge config, and MCP command construction. |
| `evaluation/instructions_tmpl.py` | Rewritten | Replaces paper-reproduction instructions with autonomous chemistry-tool protocol and required report fields. |
| `chemistry_toolbox/mcp/` | Added/refactored | Portable, self-describing MCP package with one tool per file, automatic discovery, explicit enable/disable policy, lifecycle management, shared confinement/tracing, standalone wheel metadata, and Codex/Claude/OpenCode installer. |
| `evaluation/mock_agent.py` | Added | Provides a no-API subprocess smoke Agent. |
| `evaluation/requirements.txt` | Rewritten | Matches the new Flask/OpenAI/Pydantic/MCP/FastMCP harness stack. |
| `evaluation/requirements-chemistry.txt` | Added | Installs chemistry engines without installing or writing into the sibling ChemGraph checkout. |
| `evaluation/run_task.py` | Rewritten | Builds isolated workspaces and invokes each CLI with structured argv and per-run MCP configuration. |
| `evaluation/score.py` | Rewritten | Replaces 0–100 paper checklist scoring with ChemGraph-style 0/1 answer+tool judging. |
| `evaluation/server.py` | Rewritten | Exposes task/run/stream/trace/file/score/delete APIs for chemistry evaluation. |
| `evaluation/static/app.js` | Rewritten | Implements the new task, Agent stream, tool trace, workspace, score, and run-history UI. |
| `evaluation/static/style.css` | Rewritten | Simplifies styling for the chemistry runner UI. |
| `evaluation/templates/index.html` | Rewritten | Replaces the paper benchmark dashboard with a chemistry run console. |
| `evaluation/task_schema.py` | Added | Validates public task metadata and private ground truth with Pydantic. |
| `evaluation/trace.py` | Added | Loads canonical MCP trace and converts it to ChemGraph-compatible call records/metrics. |
| `evaluation/utils.py` | Rewritten | Adds schema validation, category grouping, CLI-run discovery, ground truth loading, and safe file traversal. |
| `scripts/import_chemgraph_tasks.py` | Added | Deterministically converts ChemGraph's 40 ground-truth entries into benchmark task folders. |
| `chemistry_toolbox/scripts/check_mcp_tools.py` | Added | Lists registered tools and optionally runs a no-network calculator→RDKit→ASE/EMT→JSON trace/artifact smoke flow. |
| `scripts/run_agent_eval.sh` | Added | Requested Agent evaluation script with named Agent/task/config/runtime/model/path parameters, discovery commands, help text, positional compatibility, and YAML batch mode. |
| `tasks/ChemGraph_001..040/` | Added/generated | Public instruction plus private reference for every ChemGraph evaluation task. |
| `tests/` | Replaced | Focuses on task integrity, hidden references, path safety, runner behavior, tracing, scorer, and CLI configs. |
| `docs/ENVIRONMENT_AND_TOOLS.md` | Added | Full dependency, calculator, CLI auth, network, MCP, and judge setup. |
| `docs/MCP_TOOLS_DEVELOPMENT_AND_INSTALLATION.md` | Added | Chinese guide for writing, enabling, deleting, packaging, migrating, installing, and uninstalling MCP tools. |
| `docs/RUNNING_EVALUATIONS.md` | Added | Mock, dry-run, single, batch, UI, output, completion, and scoring usage. |
| `docs/RESEARCHCLAWBENCH_CODE_CHANGES.md` | Added | This audit. |
| `docs/VALIDATION_REPORT.md` | Added | Static, MCP, real OpenCode/DeepSeek Agent, controlled judge, and external CLI validation evidence. |

## 5. Task conversion in detail

### 5.1 Source

The importer reads:

```text
../ChemGraph/src/chemgraph/eval/data/ground_truth.json
```

It expects a JSON list. Entries are processed in source order and assigned stable benchmark IDs:

```text
entry 1  → ChemGraph_001
entry 2  → ChemGraph_002
...
entry 40 → ChemGraph_040
```

The original ChemGraph `id` is retained as string field `source_id`.

### 5.2 Public task metadata

Each task exposes only `task_info.json` and optional files under `data/`:

```json
{
  "task_id": "ChemGraph_001",
  "source_id": "1",
  "category": "smiles_lookup",
  "task": "Provide the SMILES string corresponding to this molecule: sulfur dioxide",
  "data": []
}
```

The initial ChemGraph tasks have no input attachments, so every `data/` contains only `.gitkeep`. The schema already supports future task data with `name`, `path`, `type`, and `description`.

### 5.3 Private reference

The answer is converted to:

```text
tasks/<task-id>/target_study/ground_truth.json
```

with fields:

```json
{
  "expected_tool_calls": [],
  "expected_result": "...",
  "expected_structured_output": null
}
```

`TaskRunner.setup_workspace()` copies only `data/`; it never copies `target_study/`. Tests explicitly verify that a run workspace contains no `ground_truth.json`.

### 5.4 Imported category distribution

| Category | Task count |
|---|---:|
| `smiles_lookup` | 4 |
| `optimization_from_name` | 4 |
| `thermochemistry_from_name` | 4 |
| `energy_from_name` | 4 |
| `vibrations_from_name` | 2 |
| `dipole_from_name` | 2 |
| `optimization_from_smiles` | 2 |
| `vibrations_from_smiles` | 2 |
| `thermochemistry_from_smiles` | 2 |
| `dipole_from_smiles` | 2 |
| `energy_from_smiles` | 2 |
| `reaction_energy` | 10 |
| **Total** | **40** |

### 5.5 Reimport behavior

Normal import refuses to overwrite an existing task directory. `--force` removes and recreates generated task directories. This prevents accidental silent drift while allowing an intentional refresh after the ChemGraph source data changes.

```bash
python scripts/import_chemgraph_tasks.py --force
```

## 6. Chemistry MCP adapter in detail

### 6.1 Why MCP was introduced

ResearchClawBench executes an Agent, but its tools are tied to the selected research runtime. ChemGraph registers tools inside a LangChain/LangGraph workflow. Neither directly provides a tool boundary reusable by Codex CLI, Claude Code, and OpenCode.

The new MCP layer makes the chemistry API Agent-independent:

- Codex and Claude receive the same server and tool schemas.
- Agent-specific transcript formats do not determine the canonical tool log.
- The server can reject unsafe paths before calling ChemGraph.
- Full results and changed files can be preserved outside the Agent's context window.

### 6.2 `chemistry_toolbox/mcp/server.py`, automatic registry, `ToolSpec`, configuration, and tool files

The original centralized `evaluation/mcp/chemistry_server.py` was replaced by a portable package. `server.py` now only creates the FastMCP server and transport. `registry.py` automatically scans direct, non-underscore Python files under `chemistry_toolbox/mcp/tools/`, validates each module's `TOOL_SPEC` and `register(mcp)`, applies the explicit allow/deny policy in `tool_config.json`, and calls `register(mcp)` only for enabled modules. Every public tool is isolated in one self-describing file; adding a file does not require editing the server or a duplicate central metadata list, and a newly added unreviewed file remains disabled until explicitly enabled.

The tool modules import ChemGraph core functions rather than LangChain `BaseTool` wrappers or graph nodes:

```text
chemgraph.tools.cheminformatics_core.molecule_name_to_smiles_core
chemgraph.tools.cheminformatics_core.smiles_to_coordinate_file_core
chemgraph.tools.ase_core.run_ase_core
chemgraph.tools.ase_core.extract_output_json_core
chemgraph.schemas.ase_input.ASEInputSchema
```

The registry currently discovers and enables five FastMCP tools:

| MCP name | ChemGraph implementation | Benchmark-specific behavior |
|---|---|---|
| `molecule_name_to_smiles` | `molecule_name_to_smiles_core` | Traced PubChem-backed name lookup. |
| `smiles_to_coordinate_file` | `smiles_to_coordinate_file_core` | Resolves output path inside workspace and rewrites returned paths to relative form. |
| `run_ase` | `run_ase_core` | Validates `ASEInputSchema`, confines input/output paths, captures stdout, and returns result metadata. |
| `extract_output_json` | `extract_output_json_core` | Confines and requires the JSON result path before reading. |
| `calculator` | ChemGraph-equivalent arithmetic | Uses `numexpr` for reaction-energy arithmetic and records the expression/result. |

The process changes its current directory to the run workspace before serving tools. Stdio is the normal Agent transport; Streamable HTTP is included for manual/integration use. Adding or disabling a tool no longer requires editing the server module.

### 6.3 `chemistry_toolbox/mcp/workspace.py` and settings

ResearchChemBench runs set `RESEARCHCHEMBENCH_WORKSPACE` explicitly. The portable package also accepts `RESEARCHCHEM_MCP_WORKSPACE`; when neither is set, it confines tools to the MCP process working directory so the installed package can follow the active Agent project. Every tool path is resolved and checked with `relative_to(workspace_root)`.

The following are rejected:

- relative traversal such as `../ground_truth.json`;
- absolute paths outside the run directory;
- missing required input paths;
- a configured workspace path that does not exist.

Parent directories may be created only after the resolved destination is proven to be inside the workspace.

`settings.py` locates ChemGraph using `CHEMGRAPH_ROOT` first, then searches conventional parent/sibling locations. It does not import `evaluation.settings`, which is what allows the directory to be copied outside ResearchChemBench.

### 6.4 `chemistry_toolbox/mcp/tracing.py`

`execute_traced()` wraps the actual chemistry function and performs these steps:

1. Allocate a monotonically increasing sequence number.
2. Snapshot regular workspace files before the call.
3. Record UTC start time and monotonic duration.
4. Execute the core function.
5. Persist the full serialized return value or error.
6. Snapshot every file whose size/mtime changed during the call.
7. Hash changed artifacts with SHA-256.
8. Append a canonical JSON event to `_tool_trace.jsonl`.
9. Return the original result or re-raise the original exception.

Trace event fields are:

```text
sequence
run_id
tool
arguments
status
started_at
duration_seconds
result_path
result_preview
error
artifacts[]
```

Full tool results are stored as:

```text
_tool_results/0001_<tool>.json
```

Changed files are copied to:

```text
_tool_artifacts/0001/<original-relative-path>
```

Trace-internal files, Agent state, tool logs, metadata, and score files are excluded from recursive artifact snapshots.

### 6.5 `evaluation/trace.py`

This reader is deliberately independent of Codex/Claude output formats. It:

- tolerates malformed individual JSONL lines;
- returns raw trace events to the UI;
- normalizes successful events to ChemGraph's expected list format, for example `{"run_ase": {"params": ...}}`;
- computes call count, success/failure counts, total tool runtime, and ordered tool names.

## 7. External Agent invocation in detail

### 7.1 Structured subprocess arguments

ResearchClawBench's original generic runner builds a string template and uses `shell=True`. ResearchChemBench uses a list of arguments and `shell=False` for built-in adapters. This avoids prompt interpolation through a shell and makes the exact adapter behavior reviewable.

The parent environment is inherited, then the benchmark adds unbuffered output and the per-run MCP environment. Agent stdout and stderr are merged and persisted line-by-line in `_agent_output.jsonl`.

Agent stdin is connected to `DEVNULL` so non-interactive CLIs cannot wait for or accidentally consume terminal/pipeline input after receiving the benchmark prompt. Single-task mode uses the same environment-configurable timeout and max-turn defaults as normal `TaskRunner` construction.

### 7.2 Common per-run environment

The MCP process receives:

| Variable | Meaning |
|---|---|
| `RESEARCHCHEMBENCH_WORKSPACE` | Absolute current run workspace. |
| `RESEARCHCHEMBENCH_RUN_ID` | Unique run identifier used in trace events. |
| `PYTHONPATH` | ResearchChemBench project plus `ChemGraph/src` plus any inherited path. |
| `CHEMGRAPH_LOG_DIR` | Run-local tool log directory. |

The executable for the server is selected by `CHEMGRAPH_PYTHON` and defaults to the current interpreter.

### 7.3 Codex CLI adapter

Codex is invoked with the equivalent of:

```text
codex exec
  --ignore-user-config
  --skip-git-repo-check
  -C <workspace>
  --sandbox workspace-write
  --json
  --output-last-message <workspace>/_final_message.txt
  -c mcp_servers.researchchembench.command=...
  -c mcp_servers.researchchembench.args=...
  -c mcp_servers.researchchembench.required=true
  -c mcp_servers.researchchembench.startup_timeout_sec=30
  -c mcp_servers.researchchembench.tool_timeout_sec=3600
  -c mcp_servers.researchchembench.env.<KEY>=...
  <prompt>
```

Important decisions:

- `--ignore-user-config` reduces contamination by unrelated user MCP servers and settings.
- MCP configuration is injected per run; global `~/.codex/config.toml` is not changed.
- `workspace-write` allows report and output creation.
- The final response is separately retained while the complete JSON event stream remains in `_agent_output.jsonl`.

### 7.4 Claude Code adapter

For every workspace the runner writes `.mcp.json` with one stdio server named `researchchembench`. Claude is invoked with:

```text
claude -p
  --strict-mcp-config
  --mcp-config <workspace>/.mcp.json
  --output-format stream-json
  --verbose
  --max-turns <limit>
  --tools Read,Write,Edit
  --allowedTools Read,Write,Edit,mcp__researchchembench__*
  --permission-mode dontAsk
  --disable-slash-commands
  --no-session-persistence
  <prompt>
```

`--strict-mcp-config` prevents global MCP configuration from being merged. The MCP allow rule is server-scoped because current Claude Code rejects the broader `mcp__*` wildcard. Slash commands and session persistence are disabled to reduce unrelated local skill/session influence. The benchmark allows workspace file operations and MCP calls without an interactive approval dialog because benchmark runs have no human in the loop.

### 7.5 Mock Agent adapter

The Mock Agent is not a chemistry solver. It reads the prompt, creates `report/report.md`, and emits JSON events. Its purpose is to verify:

- workspace preparation;
- subprocess invocation;
- stream capture;
- final-report completion logic;
- batch report generation;
- CI without Agent credentials or chemistry dependencies.

It should never be interpreted as a benchmark score baseline.

### 7.6 OpenCode / DeepSeek adapter

The OpenCode adapter is included so an OpenAI-compatible model endpoint can drive the same external-CLI benchmark path. Each run receives a local `opencode.json` with:

- provider name/model and base URL;
- no serialized API key;
- one local MCP server command and run-scoped environment;
- the DeepSeek V4 Flash default `deepseek/deepseek-v4-flash`.

The equivalent command is:

```text
opencode run
  --pure
  --dir <workspace>
  --model deepseek/deepseek-v4-flash
  --format json
  --dangerously-skip-permissions
  <prompt>
```

`--pure` avoids external OpenCode plugins. The API credential is inherited through `OPENAI_API_KEY`, matching the OpenAI-compatible provider behavior; it is not placed in task metadata or `opencode.json`.

## 8. Workspace lifecycle and process records

### 8.1 Run identity

Run IDs include task, Agent key, UTC timestamp, and a short random suffix:

```text
ChemGraph_001_codex_20260717_120000_a1b2c3
```

The suffix avoids collisions for concurrent or repeated runs started in the same second.

### 8.2 Workspace construction

`TaskRunner.setup_workspace()` creates:

```text
data/
code/
outputs/
report/
report/images/
tool_logs/
_tool_results/
_tool_artifacts/
INSTRUCTIONS.md
.mcp.json
opencode.json
_meta.json
```

Files copied into `data/` are changed to mode `0444`. No `related_work/` folder is created because ChemGraph tasks do not use reference papers.

### 8.3 Prompt contract

The chemistry prompt explicitly states:

- no human is available;
- Chemistry MCP tools must be used for lookup/calculation/arithmetic;
- values that should come from a tool must not be invented;
- failed calls should be diagnosed and retried;
- all file access must remain in the workspace;
- hidden references and ground truth must not be accessed;
- `data/` must not be modified;
- `report/report.md` is mandatory.

The required report includes the direct answer, units, method/calculator/model, driver, temperature and relevant parameters, important intermediate results, output paths, and reaction stoichiometry/arithmetic when applicable.

### 8.4 Streaming and timeout handling

The runner reads subprocess output through a queue so it can simultaneously:

- flush output to disk for live UI consumption;
- detect process exit;
- enforce an Agent timeout;
- respond to a stop request;
- terminate and then kill an unresponsive child if required.

`_meta.json` records termination reason, exit code, duration, model when detectable, command preview with the full prompt redacted, report presence, and process metrics from the MCP trace.

### 8.5 Strict completion semantics

A run is completed only if all conditions hold:

```text
subprocess exit code == 0
termination reason == process_exit
report/report.md exists
report/report.md is non-empty
```

This is stricter than treating any zero-exit Agent process as success. Missing the required report produces a failed run even if the CLI itself exits cleanly.

## 9. Batch CLI changes

ResearchClawBench's batch CLI is ResearchHarness/model-endpoint oriented and contains detailed model/scorer secret routing. ResearchChemBench instead benchmarks installed external CLI Agents.

### 9.1 Configuration schema

The initial YAML fields are:

```yaml
name: quick_codex
agents:
  - codex
tasks:
  - ChemGraph_001
repeats: 1
max_concurrent_runs: 1
timeout_seconds: 7200
max_turns: 200
judge:
  enabled: true
```

`tasks: all` expands to all 40 current tasks. The Cartesian product is task × Agent × repeat.

### 9.2 Supplied configurations

| File | Intended use |
|---|---|
| `quick_mock.yaml` | Dependency-light local/CI runner smoke test. |
| `quick_codex.yaml` | Small real Codex CLI trial. |
| `quick_claude.yaml` | Small real Claude Code trial. |
| `quick_opencode.yaml` | Small OpenCode/DeepSeek OpenAI-compatible trial. |
| `full.yaml` | All imported tasks; potentially expensive. |

### 9.3 Outputs

Each batch creates:

```text
workspaces/cli_runs/batch_<UTC timestamp>_<random suffix>/
├── <run workspace>/
├── eval_report.json
└── eval_report.md
```

The report records task, Agent, repeat, status, score, duration, workspace and run ID, plus completion counts and binary-score mean/pass rate.

### 9.4 Single-task mode

`--task` plus `--agent` creates a uniquely named temporary one-run YAML configuration, uses the same batch path, and removes the temporary file afterward. This avoids both a second execution implementation and collisions between simultaneous single-task commands.

## 10. Scoring changes

### 10.1 Removed ResearchClawBench scoring assumptions

The inherited scorer expected:

- `target_study/checklist.json`;
- paper-derived weighted criteria;
- optional target and generated images;
- a 0–100 score per checklist item;
- StructAI-based parallel judging.

These concepts do not fit ChemGraph's exact tool-use tasks and were removed from the score path.

### 10.2 New ChemGraph-style judge input

The ResearchChemBench judge receives:

1. Original natural-language query.
2. Expected ChemGraph tool-call list.
3. Expected final result/structured answer.
4. Successful canonical MCP tool calls.
5. Agent-generated `report/report.md`.

The judge returns one JSON object with `score` 0 or 1 and a rationale.

### 10.3 Preserved ChemGraph evaluation principles

The initial rubric preserves these ChemGraph-style rules:

- numerical answers should be within approximately 5% relative tolerance;
- units, calculator, model/method, driver, temperature, molecule identity, SMILES, and stoichiometry are key;
- harmless extra calls, defaults, file names, formatting, and rounding are acceptable;
- the logical dependency chain matters;
- fabricated values, wrong chemistry identity/method, failed calculations, or missing key results fail.

### 10.4 Score record

`_score.json` contains:

```text
run_id
task_id
agent_key
agent_name
query
expected_tool_calls
actual_tool_calls
expected_result
score
rationale
parse_error
process_metrics
```

Judge endpoint configuration uses OpenAI-compatible Chat Completions and is independent from Codex/Claude authentication. A judge configuration/API/parse failure is recorded as `score: null` plus `error`/`parse_error`; it is not silently counted as a chemistry failure with score 0.

## 11. Flask API and UI changes

The original dashboard was simplified around execution auditing instead of paper assets.

### 11.1 API surface

| Endpoint | Purpose |
|---|---|
| `GET /api/config` | Agent presets safe for UI display. |
| `GET /api/tasks` | Tasks grouped by ChemGraph category. |
| `GET /api/tasks/<id>/info` | Public task metadata only. |
| `GET /api/tasks/<id>/files` | Public `data/` tree only. |
| `GET /api/tasks/<id>/file` | Safely read one public task input. |
| `GET /api/runs` | Web and CLI run history. |
| `POST /api/runs` | Start one asynchronous Agent run. |
| `POST /api/runs/<id>/stop` | Request child-process termination. |
| `GET /api/runs/<id>/meta` | Run metadata. |
| `GET /api/runs/<id>/output` | Raw Agent stream. |
| `GET /api/runs/<id>/trace` | Canonical Chemistry MCP trace. |
| `GET /api/runs/<id>/stream` | Server-Sent Events for Agent and tool streams. |
| `GET /api/runs/<id>/files` | Workspace artifact tree. |
| `GET /api/runs/<id>/file` | Safely inspect a workspace file. |
| `POST /api/runs/<id>/score` | Run the ChemGraph-style judge. |
| `DELETE /api/runs/<id>` | Stop if active and delete the selected run. |

### 11.2 User interface

The initial page provides:

- ChemGraph category/task selector;
- Agent selector;
- start, stop, and score controls;
- public task JSON view;
- raw Agent output panel;
- canonical tool-trace panel;
- run workspace file tree and viewer;
- recent run history.

SSE reads appended Agent output and tool trace independently. The start button is restored when a run reaches completed/failed state.

## 12. Packaging and environment changes

### 12.1 `pyproject.toml`

The new package requires Python 3.10+ and declares harness-level dependencies:

```text
Flask
flask-cors
openai
python-dotenv
pydantic
PyYAML
mcp
fastmcp
numexpr
uvicorn
```

The `test` extra adds pytest and pytest-asyncio. The `chemistry` extra adds ASE, RDKit, PubChemPy, pymatgen, MACE, TBLite, and the ChemGraph-compatible NumPy version. ChemGraph itself is **not** installed editable: the MCP subprocess imports its source from `CHEMGRAPH_ROOT/src`, avoiding generated package metadata in the reference repository.

Package data explicitly includes Agent presets, environment/requirements templates, the Flask HTML template, CSS/JavaScript/favicon, and Agent logos so installed entry points retain the Web UI assets.

### 12.2 Entry points

Installed console scripts:

```text
researchchembench      → evaluation.web.server:main
researchchembench-eval → evaluation.cli:main
```

Repository wrapper:

```text
./rchem-eval
```

Requested shell launcher:

```text
bash scripts/run_agent_eval.sh --agent <agent> --task <task> [runtime flags]
bash scripts/run_agent_eval.sh <agent> <task> [--no-score|--dry-run]
bash scripts/run_agent_eval.sh --config <eval-config.yaml> [extra CLI flags]
```

The shell launcher activates `.venv` when present, supplies default sibling `CHEMGRAPH_ROOT`, selects the active Python as `CHEMGRAPH_PYTHON`, and delegates to the Python CLI.

### 12.3 CI change

The GitHub workflow now installs `-e '.[test]'` and runs pytest. It intentionally does not install the large ChemGraph calculator stack or invoke external Agents. Real MCP/Agent runs are environment-gated integration work, while unit tests remain fast and credential-free.

### 12.4 Standalone MCP tool package

`chemistry_toolbox/pyproject.toml` independently builds `researchchem-mcp-tools`. The standalone wheel maps the same source files to the installed package name `researchchem_mcp_tools` and includes every one-file tool module plus the `ToolSpec`/registry/manager implementation, `tool_config.json`, generated tool catalog, and README.

Standalone entry points:

```text
researchchem-mcp-server  → researchchem_mcp_tools.server:main
researchchem-mcp-install → researchchem_mcp_tools.installer:main
researchchem-tool        → researchchem_mcp_tools.tool_manager:main
```

`chemistry_toolbox/mcp/install.sh` can install the package (optionally with MACE/TBLite/RDKit/ASE dependencies) and then configure Codex, Claude Code, OpenCode, or all available Agents. Codex/Claude are configured through their official `mcp add/remove` CLI commands. OpenCode JSON is merged with backup creation.

## 13. Test-suite replacement

The copied ResearchClawBench tests targeted its old CLI cleanup and ResearchHarness configuration. They were removed/replaced with the following tests.

| Test file | Assertions |
|---|---|
| `tests/test_tasks.py` | All 40 task directories exist, metadata/reference schemas validate, and IDs are stable. |
| `tests/test_workspace_and_runner.py` | Workspace is created correctly, ground truth is not copied, report completion is enforced, Agent argv is structured, and judge credentials are stripped from the child environment. |
| `tests/test_trace_and_paths.py` | Traversal outside workspace is rejected, traces persist results, and process metrics normalize correctly. |
| `tests/test_score.py` | Scorer prompt contains expected/actual evidence, injected judge verdict is persisted, and judge/API failure remains unscored rather than becoming a false zero. |
| `tests/test_cli_eval.py` | Supplied YAML expands to valid task/Agent specifications and dry-run succeeds. |
| `tests/test_mcp_tool_package.py` | Manifest entries map one-to-one to tool files, cwd fallback is confined, and OpenCode configuration is merged/backed up. |
| `tests/conftest.py` | Makes the repository package importable in source-tree tests. |

The Mock Agent makes the runner and batch path testable without PubChem, MACE, TBLite, Codex, Claude, or judge credentials.

## 14. Deliberately retained files

The upstream `LICENSE` is retained. ResearchClawBench assets and static logos are also retained in the initial copy for provenance and possible UI reuse, although the simplified UI uses only the selected Agent logos. Their presence does not affect task execution or scoring.

`evaluation/__main__.py` retains the same general entry-point idea (`python -m evaluation`) but now imports the rewritten ResearchChemBench Flask server.

## 15. Security and fairness boundaries

### 15.1 Implemented controls

- Hidden task references are not copied to workspaces.
- MCP file paths cannot escape the run workspace.
- Input files are made read-only in the normal runner path.
- Agent subprocesses use structured argv, not shell command templates.
- `JUDGE_API_KEY` is stripped from the tested Agent child environment.
- Codex global configuration is ignored.
- Claude uses strict per-run MCP configuration.
- Every MCP call is recorded independently of Agent transcript formatting.
- Full results and changed artifacts are retained with hashes.
- UI file reads use safe path resolution.

### 15.2 Important limitations

- This is not yet a hardened container sandbox.
- Codex has workspace-write shell capability and may be able to use installed non-MCP chemistry packages.
- Judge keys are removed from the child environment, but a same-user non-container Agent may still have filesystem-read access to `config.local.env`; sensitive evaluations should separate Agent execution and scoring credentials.
- The judge sees observable MCP calls, but calls made outside the MCP server are not captured.
- PubChem and MACE model retrieval may require outbound network access.
- MACE tasks may use significant GPU/CPU time, memory, and disk.
- The first scorer is LLM-based and binary; deterministic molecule/SMILES/numeric/trajectory checks are not yet implemented.
- Concurrent calculator workloads are not assigned resource quotas by the harness.
- Reproducibility still depends on ChemGraph/calculator versions, downloaded model weights, hardware, and Agent CLI versions.

For a leaderboard-quality release, the next hardening step should be a per-run container with pinned chemistry images, explicit network policy, resource limits, immutable task inputs, and an Agent-independent event channel.

## 16. Review checklist

A reviewer can verify the implementation with the following sequence:

```bash
cd ${PROJECT_ROOT}

# Unit tests
pytest -q

# No-API end-to-end runner
bash scripts/run_agent_eval.sh --agent mock --task ChemGraph_001 --no-score

# Validate Agent configuration without invocation
python -m evaluation.cli eval_configs/examples/quick_codex.yaml --dry-run --no-score
python -m evaluation.cli eval_configs/examples/quick_claude.yaml --dry-run --no-score

# Once ChemGraph dependencies are installed
python chemistry_toolbox/scripts/check_mcp_tools.py

# Inspect exact framework differences, excluding generated tasks/runs
diff -qr ../ResearchClawBench . \
  --exclude=.git \
  --exclude=tasks \
  --exclude=workspaces \
  --exclude=__pycache__ \
  --exclude=.pytest_cache
```

For any generated run, verify:

```text
1. report/report.md is non-empty for completed status.
2. target_study/ and ground_truth.json are absent.
3. _meta.json contains the expected task and Agent identity.
4. Chemistry calls appear in _tool_trace.jsonl.
5. Full results exist in _tool_results/.
6. Chemistry-created files are snapshotted in _tool_artifacts/.
7. _score.json is present only after judge scoring.
```

## 17. Initial implementation boundary

This version is intentionally an initial benchmark rather than a final standardized leaderboard. It establishes the core path requested:

```text
ChemGraph instruction
→ autonomous external Agent CLI
→ configured ChemGraph chemistry tools through MCP
→ result and process artifacts
→ ChemGraph-style evaluation
```

Future work can add additional Agent CLI adapters, deterministic chemistry validators, containerized isolation, task version manifests, calculator caching, retry/resource policies, and aggregate leaderboard statistics without restoring ChemGraph's LangGraph workflow inside the benchmark runner.

## 18. 2026-07-18 dependency-isolated MCP extension

The original ResearchChemBench implementation started one Chemistry MCP process from a
single Python environment. The expanded chemistry toolbox exposed ABI and solver conflicts,
so the runner was extended without changing ResearchClawBench or ChemGraph.

### 18.1 New configuration and runtime layer

- `chemistry_toolbox/config/mcp_profiles.yaml` assigns every one-file tool to exactly one compatibility profile,
  declares profile-specific conda/pip packages, executable mappings, and health checks.
- `chemistry_toolbox/mcp/profiles.py` validates complete/non-duplicate coverage of all 41 tools,
  resolves per-profile interpreters and cross-environment executable paths, and constructs MCP
  server specifications.
- `chemistry_toolbox/mcp/server.py` accepts `--profile` and registers only that profile's tools.
- `evaluation/config.py` returns either the legacy single server or multiple profile servers.
- `evaluation/run_task.py` now writes multiple Claude/OpenCode MCP entries and multiple Codex
  `mcp_servers.*` overrides. Server names provide the Agent-visible tool namespaces.

### 18.2 Installer and verification

- `chemistry_toolbox/scripts/setup_mcp_profile_envs.py` creates resumable per-profile environments, records each
  package operation, supports recreation/timeouts, and separately manages executable-only
  support environments.
- `chemistry_toolbox/scripts/probe_mcp_profile.py` runs inside a target interpreter and checks imports, commands,
  exact MCP tool listing, and optional Materials Project live access.
- `chemistry_toolbox/scripts/check_mcp_profile_envs.py` orchestrates all probes and writes
  `docs/MCP_PROFILE_STATUS.{md,json}` without serializing credential values.
- `config.local.env` is an ignored root-level local configuration loaded by the shell runner and
  MCP profile loader; `config.local.env.example` is the publishable template.

### 18.3 Conflict discovered and resolved

Installing CP2K and DFTB+ sequentially in one periodic environment caused conda to downgrade
CP2K 2026.1 to an old Python 3.8 build. The conflicted generated environment was removed and
replaced with isolated `qe`, `cp2k`, `periodic`, `phonons`, and executable-only `abinit`
environments. The periodic dispatcher receives absolute paths to sibling executables.

### 18.4 Functional fixes

`query_materials_project` now normalizes `material_id` from the public document attribute.
This works around an observed mp-api/emmet/Pydantic serialization combination that returned
`mp-ft` from `model_dump(mode="json")` while the actual object correctly held `mp-149`.

### 18.5 Current boundary

All required checks pass for 12 profiles and 41 tools. ORCA and GNINA remain explicit manual
backends. NequIP, DeepMD, FAIRChem, and AIMNet2 are not installed as `run_mlip` requirements
because their model-loading adapters and checkpoint policies are not implemented; package
presence alone would not make those tool branches functional.
