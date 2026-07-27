# Running Agents and Evaluations

## 1. Shell script parameter reference

Display the complete help text:

```bash
bash scripts/run_agent_eval.sh --help
```

Important parameters:

| Parameter | Meaning | Example |
|---|---|---|
| `--agent`, `-a` | Agent preset | `--agent opencode` |
| `--task`, `-t` | One ChemGraph task ID | `--task ChemGraph_015` |
| `--config`, `-c` | YAML batch configuration; replaces `--agent/--task` | `--config eval_configs/quick_codex.yaml` |
| `--no-score` | Preserve results without calling the judge | `--no-score` |
| `--dry-run` | Print planned runs without Agent execution | `--dry-run` |
| `--timeout-seconds` | Per-Agent wall-time limit | `--timeout-seconds 1800` |
| `--max-turns` | Maximum Agent turns where supported | `--max-turns 80` |
| `--workspaces-dir` | Change the output root | `--workspaces-dir /tmp/rchem-runs` |
| `--tasks-dir` | Use another task directory | `--tasks-dir /path/to/tasks` |
| `--chemgraph-root` | Use another ChemGraph checkout | `--chemgraph-root /path/to/ChemGraph` |
| `--chemgraph-python` | Python used to start Chemistry MCP | `--chemgraph-python .toolbox_env/bin/python` |
| `--mcp-tools` | Compatibility option; the current benchmark accepts only `all` | `--mcp-tools all` |
| `--mcp-profiles` | Dependency-isolated MCP server profiles | `--mcp-profiles core,services,quantum` |
| `--opencode-model` | OpenCode provider/model | `--opencode-model deepseek/deepseek-v4-flash` |
| `--opencode-base-url` | OpenAI-compatible endpoint | `--opencode-base-url https://api.deepseek.com/v1` |
| `--list-agents` | Print valid Agent names | — |
| `--list-tasks` | Print all tasks grouped by category | — |

Discover available values:

```bash
bash scripts/run_agent_eval.sh --list-agents
bash scripts/run_agent_eval.sh --list-tasks
```

Run any single task by changing `--agent` and `--task`:

```bash
bash scripts/run_agent_eval.sh \
  --agent opencode \
  --task ChemGraph_010 \
  --mcp-tools chemgraph-core \
  --timeout-seconds 1800 \
  --max-turns 80 \
  --no-score
```

The older positional form remains supported:

```bash
bash scripts/run_agent_eval.sh opencode ChemGraph_010 --no-score
```

For batch mode, values inside the YAML file such as `timeout_seconds` and `max_turns` take precedence over shell defaults.

The current benchmark always exposes the same complete task-independent catalog.
`--mcp-tools` is retained for compatibility but accepts only `all`. Use
`--tool-discovery-mode progressive` to load Action schemas on demand or `full`
to expose the historical eager surface.

For the installed multi-environment toolbox, `--mcp-profiles` validates selected
runtime compatibility classes. It does not filter the public Action catalog or
perform backend selection:

```bash
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_003 \
  --mcp-profiles core,services --no-score

bash scripts/run_agent_eval.sh --agent codex --task ChemGraph_010 \
  --mcp-profiles core,quantum,psi4 --timeout-seconds 3600 --no-score
```

The script automatically loads root-level `config.local.env`, which is ignored by version
control. Use `config.local.env.example` as the publishable template.

## 1.1 Persistent multi-task submission

Use `submit_evaluation.sh` when tasks should survive terminal disconnection and
need compact status, follow, attach, stop, and summary commands:

```bash
bash scripts/submit_evaluation.sh submit \
  --model deepseek-v4-flash \
  --judge-model deepseek-v4-flash \
  --timeout-seconds 10800 \
  --max-turns 200 \
  --max-concurrent-runs 1 \
  --follow \
  Task_A Task_B Task_C
```

The command prints the submission root and tmux session. Query it later with:

```bash
bash scripts/submit_evaluation.sh status --run-root workspaces/submissions/<UTC>
bash scripts/submit_evaluation.sh follow --run-root workspaces/submissions/<UTC>
bash scripts/submit_evaluation.sh summary --run-root workspaces/submissions/<UTC>
bash scripts/submit_evaluation.sh attach --session rcb_<UTC>
bash scripts/submit_evaluation.sh stop --session rcb_<UTC>
```

`stop` sends SIGINT to the evaluator so the active Agent and detached chemistry
jobs are cleaned up and final metadata is written.

## 2. Local harness smoke test

The Mock Agent does not call an API or chemistry package. It validates workspace creation, subprocess execution, JSONL capture, report completion, and batch reporting.

```bash
bash scripts/run_agent_eval.sh --agent mock --task ChemGraph_001 --no-score
```

Batch smoke test:

```bash
python -m evaluation.cli_eval eval_configs/quick_mock.yaml --no-score
bash scripts/run_agent_eval.sh --config eval_configs/quick_mock.yaml --no-score
```

## 3. Dry-run an Agent configuration

```bash
python -m evaluation.cli_eval eval_configs/quick_codex.yaml --dry-run --no-score
python -m evaluation.cli_eval eval_configs/quick_claude.yaml --dry-run --no-score
python -m evaluation.cli_eval eval_configs/quick_opencode.yaml --dry-run --no-score
```

Dry-run validates tasks and Agent keys without creating run workspaces or invoking an Agent.

## 4. Run a single task

Without scoring:

```bash
bash scripts/run_agent_eval.sh --agent codex --task ChemGraph_001 --no-score
bash scripts/run_agent_eval.sh --agent claude --task ChemGraph_003 --no-score
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_001 --no-score
```

With scoring:

```bash
export JUDGE_API_KEY=...
export JUDGE_API_BASE=...
export JUDGE_MODEL_NAME=...

bash scripts/run_agent_eval.sh --agent codex --task ChemGraph_001
```

Equivalent Python invocation:

```bash
python -m evaluation.cli_eval --agent codex --task ChemGraph_001 --no-score
```

## 5. Batch evaluation

```bash
python -m evaluation.cli_eval eval_configs/quick_codex.yaml
python -m evaluation.cli_eval eval_configs/quick_claude.yaml
python -m evaluation.cli_eval eval_configs/quick_opencode.yaml --no-score
python -m evaluation.cli_eval eval_configs/full.yaml

# Equivalent shell-script form
bash scripts/run_agent_eval.sh --config eval_configs/quick_codex.yaml
```

The `full.yaml` configuration runs all 40 tasks and can be computationally expensive.

Example YAML:

```yaml
name: custom_run
agents:
  - codex
  - claude
tasks:
  - ChemGraph_001
  - ChemGraph_005
repeats: 2
max_concurrent_runs: 1
timeout_seconds: 7200
max_turns: 200
judge:
  enabled: true
```

## 6. Web UI

```bash
python -m evaluation
```

The UI provides:

- task selection grouped by ChemGraph category;
- Agent selection;
- start/stop controls;
- live Agent stdout events;
- live normalized Chemistry MCP trace;
- workspace file inspection;
- final report inspection;
- on-demand judge scoring;
- recent run history.

## 7. Run workspace

Web runs are stored under:

```text
workspaces/<run-id>/
```

CLI batches are stored under:

```text
workspaces/cli_runs/batch_<UTC timestamp>_<suffix>/<run-id>/
```

After every run, the shell/CLI output prints the exact `workspace=...` path, followed by the batch directory and evaluation-report path. Therefore no manual directory search is required.

Key files:

| File | Meaning |
|---|---|
| `INSTRUCTIONS.md` | Prompt supplied to the Agent |
| `_agent_output.jsonl` | Raw CLI stdout |
| `_model_io.jsonl` | Redacted event-sourced model input/output trajectory for primary and child Agent sessions |
| `_tool_trace.jsonl` | Agent-independent MCP tool trace |
| `_tool_results/` | Full serialized return value per tool call |
| `_tool_artifacts/` | Snapshot of files changed by each tool call |
| `_meta.json` | Run status, command, duration, model, and process metrics |
| `report/report.md` | Required final Agent answer |
| `_score.json` | ChemGraph-style judge result |
| `_score_history.jsonl` | Append-only history of judge calls, scores, model, timestamp, and token usage |
| `results.json` | Stable summary of status, models, scores, criterion scores, tools, failures, Agent/Judge tokens, and artifact paths |

After a CLI batch finishes, the batch directory also contains `results.json`.
Its `summary` aggregates completion counts, scores, duration, tool calls, failed
tool calls, Agent tokens, Judge tokens, and combined tokens. Its `runs` array
contains the complete per-task summaries.

Agent token usage is reconstructed from `_opencode/opencode.db` and separated
into uncached input, cache read, cache write, output, reasoning, and total.
Judge prompt/completion/total tokens come from `_score.json`.

See [`MODEL_IO_TRAJECTORY_FORMAT.md`](MODEL_IO_TRAJECTORY_FORMAT.md) for the
trajectory schema, reconstruction procedure, redaction rules, and fidelity
limits.

## 8. Completion semantics

A run is `completed` only when:

```text
Agent exit code == 0
AND termination == process_exit
AND report/report.md exists
AND report/report.md is non-empty
```

A successful process that fails to write the report is marked `failed`.

## 9. Scoring semantics

The initial judge returns `0` or `1` and evaluates both:

- final report correctness;
- observable Chemistry MCP tool sequence.

The prompt preserves ChemGraph's important rules:

- numerical tolerance of approximately 5%;
- key calculator, model/method, driver, temperature, molecule, SMILES, unit, and stoichiometry must be correct;
- optional/default arguments and harmless extra calls are acceptable;
- the logical dependency chain must be preserved.

## 10. Choosing tasks for early testing

Start with:

```text
ChemGraph_001–004: SMILES lookup
```

Then try a low-cost installed calculator task. Leave reaction thermochemistry and MACE tasks until the environment has been validated, because they involve multiple geometry/thermochemistry calculations.

## 11. Current fairness limitation

The MCP trace reliably records calls made through Chemistry MCP. However, Codex still has workspace shell capability and could theoretically solve a task using another installed package. The initial prompt explicitly requests Chemistry MCP use and the judge evaluates the MCP call sequence, but this is not a hardened enforcement boundary.

For a controlled-tool leaderboard, run each Agent in a container and deny unrelated network, package installation, and executables.
