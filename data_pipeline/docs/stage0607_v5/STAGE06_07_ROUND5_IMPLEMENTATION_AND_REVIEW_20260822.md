# Stage06/07 v5 Round 5 — implementation and review (2026-08-22)

## Scope

This round remains bounded by the v5 objective: prefer the paper's complete
computational route, fall back only to the most important core sub-process when
the complete route is infeasible or not closed, record unavailable software
without scientifically rejecting the task, preserve Stage06B answer blindness,
and keep Stage07's scientific decision separate from transport publication
checks.

## Finding carried into this round

The current mechanical gate already filters `acceptance_profiles` by
`applies_to_modes`; that suspected defect was therefore not changed. The
reproducible transport defect was narrower: an Agent may emit
`task_info.json.required_deliverables` as strings such as
`["report/results.json"]`, while the evaluator schema requires objects with a
`path` (and optional `description`/`allow_empty`). This can leave a scientifically
approved task mechanically unpublished.

## Change

Commit `7ff1c14` adds the generic `normalize_required_deliverables()` projection
to the shared Stage06 contract validator and invokes it from
`canonicalize_mode_task_contract()` for `task_info.json`. It accepts string and
`path`/`file` object spellings, supplies only transport defaults, and does not
invent scientific deliverables. A regression test covers mixed string/object
inputs and the resulting Evaluator-compatible records.

No paper-specific rule, molecule name, expected value, or task-specific prompt
was added.

## Verification

- Targeted mode-contract tests: **5 passed**.
- Stage06/07-related tests (`pytest -k 'stage0607 or stage06 or stage07'`):
  **158 passed, 387 deselected**.
- The code change was committed without staging unrelated workspace changes.

## Test batch status

The existing DeepSeek batch remains active and was not stopped or duplicated:

`runs/stage06-07-v5-round5-deepseek10-concurrency10-20260822`

It was started with Codex harness, DeepSeek-v4-pro-0813, high reasoning, and
concurrency 10. After its completion (or the requested waiting window), results
will be reviewed against the v5 objective, with scientific inadequacy separated
from Prompt/Agent failures and transport bugs.

## Remaining audit gate

Before any new batch is submitted, inspect the current batch for recurring
patterns. A Stage07B narrow repair phase is not enabled by this round: one
isolated contract normalization defect is insufficient evidence for a separate
agent, and the defect is now handled as a small generic transport projection.
