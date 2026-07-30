# Contributing to ResearchChemBench

ResearchChemBench is an initial research benchmark for testing external Agent CLIs against traced ChemGraph chemistry tools. Contributions should preserve three invariants:

1. Do not modify the sibling `ChemGraph` or `ResearchClawBench` repositories from ResearchChemBench code or tests.
2. Never expose `tasks/*/target_study/ground_truth.json` to the Agent workspace.
3. Keep chemistry tool execution workspace-confined and recorded in `_tool_trace.jsonl`.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest -q
```

Chemistry integration work additionally requires:

```bash
pip install -e '.[chemistry]'
python chemistry_toolbox/scripts/check_mcp_tools.py
```

## Before submitting a change

- Run `pytest -q`.
- Run `bash scripts/run_agent_eval.sh --agent mock --task Electron_Isodensity_Reproduction_01_Method_Selection --no-score`.
- Confirm a task workspace contains no `ground_truth.json`.
- Add or update the detailed change and environment documentation when behavior changes.
- Do not commit credentials, run workspaces, model weights, or private evaluation configs.

See `docs/ENVIRONMENT_AND_TOOLS.md` and `docs/RUNNING_EVALUATIONS.md` for the runtime contract.
