# ResearchChemBench Initial Validation Report

Validation date: 2026-07-17 UTC

Toolbox expansion revalidation: the MCP server now registers 41 tools, the full suite reports `70 passed`, and `chemistry_toolbox/scripts/verify_toolbox.py` reports 25 real-smoke working tools, 16 not configured/without a safe real smoke, and 0 failed tools. The original DeepSeek V4 Flash Agent/judge validation below remains the live end-to-end benchmark validation.

After the expansion, a fresh OpenCode/DeepSeek V4 Flash run also passed with the new task-specific tool selection. It used the default `chemgraph-core` profile, called `molecule_name_to_smiles`, returned `O=S=O`, wrote the report and trace, and received an independent DeepSeek judge score of 1. Workspace:

```text
workspaces/cli_runs/batch_20260717_134742_3176fd/
└── ChemGraph_001_opencode_20260717_134742_b77260/
```

Exposing all 41 schemas to this OpenCode/DeepSeek combination produced a tool-argument JSON parsing failure before a valid call. Therefore `run_agent_eval.sh` now defaults to `--mcp-tools chemgraph-core` for the current ChemGraph tasks and supports `--mcp-tools all` or an explicit comma-separated task-specific subset.

## 1. Result summary

The initial benchmark path is operational:

```text
ChemGraph task instruction
→ external OpenCode Agent using DeepSeek V4 Flash
→ run-local Chemistry MCP server
→ ChemGraph molecule-name lookup core
→ canonical trace and full tool result
→ report/report.md
→ DeepSeek V4 Flash ChemGraph-style judge
→ score 1
```

The final live validation run completed in 11.225 seconds, made one successful `molecule_name_to_smiles` call, returned `O=S=O`, wrote the required report, and received judge score 1.

Successful run workspace:

```text
workspaces/cli_runs/batch_20260717_062651_880535/
└── ChemGraph_001_opencode_20260717_062651_683bf9/
```

## 2. Static and unit validation

The following checks passed:

| Check | Result |
|---|---|
| Python compile check for `evaluation/`, `scripts/`, and `tests/` | Passed |
| Pytest suite | `70 passed` after toolbox expansion |
| Shell syntax for `rchem-eval` and `scripts/run_agent_eval.sh` | Passed |
| JavaScript syntax for `evaluation/static/app.js` | Passed |
| JSON validation for Agent presets and task metadata | Passed |
| YAML dry-run for Codex, Claude, and OpenCode configs | Passed |
| Wheel metadata/package-data build | Passed |

The tests cover all 40 tasks, hidden ground-truth isolation, structured Agent commands, judge-key removal, scorer success/error semantics, and batch configuration expansion. They now also cover self-describing tool auto-discovery, new-tool default disablement, metadata validation, one-file/one-registration enforcement, scaffold/enable/disable/archive/restore lifecycle, failed-config-write rollback, lazy ChemGraph/backend loading, wildcard disablement, symlink and calculator-path confinement, trace sequence collision prevention, trace-setting validation, and preservation of original tool exceptions.

The management layer was additionally checked with:

```text
bash chemistry_toolbox/scripts/manage_mcp_tools.sh validate
bash chemistry_toolbox/scripts/manage_mcp_tools.sh catalog
```

Both completed successfully, and the generated catalog reports all 41 current tools as enabled and valid.

## 3. Chemistry MCP validation

### 3.1 Registered tools

The in-memory FastMCP client found all 41 expected tools. The five original ChemGraph-compatible tools remain present:

```text
calculator
extract_output_json
molecule_name_to_smiles
run_ase
smiles_to_coordinate_file
```

### 3.2 No-network functional smoke test

`python chemistry_toolbox/scripts/check_mcp_tools.py --smoke` passed this sequence:

```text
calculator
→ water SMILES to XYZ with RDKit
→ ASE/EMT single-point energy
→ JSON extraction
```

The test also verified `_tool_trace.jsonl`, `_tool_results/`, `_tool_artifacts/`, the generated XYZ, the generated energy JSON, and artifact snapshots.

### 3.3 PubChem network test

A real MCP `molecule_name_to_smiles` call for sulfur dioxide succeeded and returned:

```text
O=S=O
```

## 4. OpenCode/DeepSeek Agent validation

Installed CLI:

```text
OpenCode 1.14.41
```

Before Agent execution, `opencode mcp list --pure` parsed the run-local `opencode.json` and reported:

```text
researchchembench connected
```

The final live run used:

```text
Agent: OpenCode
Model: deepseek/deepseek-v4-flash
Endpoint: https://api.deepseek.com/v1
Task: ChemGraph_001
```

Observed process result:

| Field | Value |
|---|---|
| Run status | `completed` |
| Exit code | `0` |
| Termination | `process_exit` |
| Duration | `11.225` seconds |
| Required report | Present and non-empty |
| Chemistry tool calls | 1 |
| Successful chemistry calls | 1 |
| Failed chemistry calls | 0 |
| Tool used | `molecule_name_to_smiles` |
| Tool result | `O=S=O` |
| DeepSeek judge score | `1` |

The report correctly states the sulfur-dioxide SMILES, the lookup method, the MCP tool name/input, and the intermediate result.

## 5. DeepSeek judge behavior validation

The DeepSeek V4 Flash API configuration was read at runtime from the user-specified script. The API key was never printed, copied into ResearchChemBench, written into `opencode.json`, or saved in this report.

Two controlled scorer cases were executed through `evaluation.score.score_workspace()`:

| Case | Expected | Actual | Result |
|---|---:|---:|---|
| Correct `molecule_name_to_smiles` trace plus correct `O=S=O` report | 1 | 1 | Passed |
| Mock report with no chemistry call and no answer | 0 | 0 | Passed |

Both cases wrote `_score.json`, demonstrating the full ground-truth loading, trace normalization, prompt construction, OpenAI-compatible API call, JSON verdict parsing, and result persistence path.

The final real OpenCode run was then scored independently and also received 1.

## 6. Codex and Claude live-run observations

The CLI commands and MCP arguments for both adapters pass local construction/dry-run tests against the installed versions:

```text
Codex CLI 0.144.1
Claude Code 2.1.209
```

Live attempts exposed external environment issues:

- Codex could not resolve/connect to `api.openai.com` and exited after transport retries. No chemistry call occurred.
- Claude's configured third-party authentication endpoint returned HTTP 401.

These attempts also produced useful compatibility fixes that are now in the code:

- Agent stdin is `DEVNULL`, preventing non-interactive Codex from consuming extra stdin.
- Single-task runs honor environment-configured timeouts/max turns.
- Claude uses the accepted server-scoped allow pattern `mcp__researchchembench__*` rather than the rejected `mcp__*` wildcard.
- Claude slash commands and session persistence are disabled for cleaner benchmark isolation.

Codex/Claude live success still requires valid reachable provider/authentication state on the machine. The benchmark's external-Agent/MCP path itself was fully validated with OpenCode/DeepSeek.

## 7. Full calculator boundary

The original benchmark smoke uses ASE/EMT and RDKit. The complete 40-task suite additionally needs:

- TBLite/GFN2-xTB for 20 tasks;
- MACE-MP and the `medium-mpa-0` model for 16 tasks;
- PubChem only for the first 4 lookup tasks.

TBLite and MACE packages are now installed in `.toolbox_env`; CHGNet completed a real minimal MLIP calculation. The complete all-40 ChemGraph benchmark was not executed as part of the toolbox expansion because MACE task models can download large weights and require substantially more compute. See `TOOLBOX_SETUP.md` and `TOOLBOX_STATUS.md`.

## 8. Reference repository integrity

ResearchClawBench remained clean at revision:

```text
6bfca049f050cae559228e713cea61f9c86acc43
```

ChemGraph remained at revision:

```text
2f35bde48ce6d45cf2cd046ac754bb85badf2105
```

ChemGraph had pre-existing local modified/untracked files before this implementation; its tracked/untracked status list was unchanged by ResearchChemBench work. No patch targeted either reference repository.

## 9. Reproduction commands

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

source chemistry_toolbox/scripts/activate_toolbox_env.sh
pytest -q
python chemistry_toolbox/scripts/check_mcp_tools.py --smoke
python chemistry_toolbox/scripts/verify_toolbox.py

python -m evaluation.cli_eval eval_configs/quick_codex.yaml --dry-run --no-score
python -m evaluation.cli_eval eval_configs/quick_claude.yaml --dry-run --no-score
python -m evaluation.cli_eval eval_configs/quick_opencode.yaml --dry-run --no-score

export OPENAI_API_KEY=...
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_001 --no-score
```

Judge credentials can then be exported separately and the workspace scored through the Web UI or `evaluation.score.score_workspace()`.
