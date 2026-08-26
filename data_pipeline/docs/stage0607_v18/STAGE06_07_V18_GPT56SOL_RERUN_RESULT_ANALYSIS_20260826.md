# Stage06/07 v18 GPT-5.6-sol rerun analysis

## Test scope

The formal rerun used the five papers that had previously reached a successful
late-stage candidate state:

- `paper_2aca1dd116799b28`
- `paper_611000e1de080f6f`
- `paper_76ae2dc25f0a5aeb`
- `paper_9455a82229de2427`
- `paper_a5564360a31f760b`

Configuration was `gpt-5.6-sol`, reasoning effort `high`, base URL
`http://127.0.0.1:50917/v1`, and maximum concurrency 4. The output directory was
`runs/stage0607-v18-gpt-5.6-sol-20260826-rerun`.

## Batch outcome

| Paper | Outcome | Stage06A self-check | Stage06A external Gate | Stage06B | Stage07 |
|---|---|---|---|---|---|
| `paper_2aca1dd116799b28` | technical blocked | passed | passed | timed out after writing tree | not run |
| `paper_611000e1de080f6f` | technical blocked | passed | passed | timed out after writing tree | not run |
| `paper_76ae2dc25f0a5aeb` | published | passed | passed | passed | approved; mechanical Gate passed |
| `paper_9455a82229de2427` | technical blocked | passed | passed | timed out after writing tree | not run |
| `paper_a5564360a31f760b` | scientific rejection | receipt-only path | passed | not applicable | not run |

The batch ended as `COMPLETED_WITH_FAILURES` with 5/5 terminal records, 1
published task, 1 scientific rejection, and 3 technical blocks.

## What the rerun proves

The receipt timing fix worked. All four positive Stage06A attempts wrote an
`agent_self_check_report.json` with `status=passed`; their latest external
Stage06A reports also had `status=passed` and an empty finding list. None failed
with `construction_receipt_missing`. The installed standalone Gate in each
workspace has the same SHA-256 as the repaired source `src/stages/phase_gate.py`.

For the published paper, Stage06B self-check and external Gate passed, Stage07A
ran exactly once, scientific audit passed, mechanical pre-publish validation
passed, and the final package was published. Its evaluator reference contains
the five split files, concrete numeric/ordering/condition/semantic rules, and
bindings to `report/results.json`.

## Root cause of the three technical blocks

The three blocked papers did not fail because of a Gate finding. Their
`task_pair_builder` Agent runs succeeded and their Stage06A artifacts passed
both checks. Stage06B then created a complete `outputs/autonomous_research/`
tree and ran the local self-check to `passed`, but the Codex process timed out
after 3600 seconds before returning its final structured JSON receipt. The
recorded failure was `agent_timeout`; no external Stage06B report was written,
so Stage07 was never invoked.

The evidence is especially clear for the three workspaces:

- all required autonomous files exist (`task.md`, `task_info.json`,
  `task_spec.json`, `submission_contract.json`, `process_rubric.json`, and
  input assets);
- manually rerunning the shared Stage06B Gate returns `passed` with no
  findings for all three trees;
- the Agent stdout ends after successful self-check commands, with no final
  receipt response;
- `agent_run.json` reports `failure_class=agent_timeout`,
  `receipt_recovered_from_artifact=false`, and `resume_mode=fresh`.

One `paper_2aca...` stream also contains an upstream `502 auth_unavailable`
message from an internal per-run bridge URL. This is an execution disturbance,
not a Stage06/07 contract failure; the final blocking event was still the
one-hour converter timeout. The other two timeout cases do not show that
message.

## Code correction after the rerun

The timeout exposed a second one-shot flow gap: a complete file-first result was
discarded solely because the final response was late. The harness now supports a
trusted recovery receipt only when the orchestrator declares:

1. the fixed autonomous artifact directory;
2. the five required public files; and
3. a fixed `conversion_uncertain` response shape.

The recovery checks every declared file for existence, non-empty content, and
valid JSON where applicable. It may merge the authored
`outputs/conversion_report.json`, then returns control to the ordinary external
Gate and Stage07 path. It never starts another model call, resumes a session, or
uses arbitrary model-provided paths. A timeout without this complete declared
tree remains a technical block.

Regression status after this correction: 313 relevant Stage06/07 and pipeline
tests passed. The five-paper API batch above predates this timeout-recovery
patch and is therefore not evidence that recovery has been exercised in a live
model run.

## Scientific rejection

`paper_a5564360a31f760b` was correctly rejected by Stage06A with
`missing_source_input`: the exact methyl-substituted structures and a
deterministic geometry selection needed for the central geometry-sensitive
workflow were absent from the paper/SI/input snapshot. No task tree was emitted
and no downstream conversion was attempted. This is a scientific rejection,
not a mechanical Gate failure.

## Remaining recommendation

Run a small follow-up using the three preserved timeout workspaces or one fresh
paper after the recovery patch. The acceptance criteria are: a recovered
`agent_run.json` with `status=succeeded` and
`receipt_recovered_from_artifact=true`, one Stage06B external Gate report,
Stage07A execution, and no second Agent invocation. Do not classify the current
three timeout records as scientific failures or as evidence of evaluator
incompleteness.
