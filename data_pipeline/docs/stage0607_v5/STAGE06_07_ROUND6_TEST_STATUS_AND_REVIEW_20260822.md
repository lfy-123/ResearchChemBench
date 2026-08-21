# Stage06/07 v5 Round 6 — test status and review (2026-08-22)

## Code baseline

Round 5's generic Evaluator-contract fix is present in commits `7ff1c14` and
`420f823`: string or `path`/`file` forms of `task_info.json.required_deliverables`
are projected to typed `{path, description, allow_empty}` records during the
existing mode canonicalization. The v5 objective was updated to allow up to ten
iterations (`a33d218`), while keeping the same scope and role boundaries.

The relevant regression and Stage06/07 test selections passed:

- targeted mode-contract tests: **5 passed**;
- Stage06/07 selection: **158 passed, 387 deselected**;
- the mechanical hidden-identity regression now also exercises compact string
  deliverables and passes.

## Batch submitted

The post-fix DeepSeek batch is:

`runs/stage06-07-v5-round6-deepseek10-concurrency10-20260822`

It uses DeepSeek-v4-pro-0813, Codex harness, high reasoning, and ten concurrent
papers selected with seed `20260824`. The batch manifest contains ten papers and
the correct endpoint/model settings.

After the requested 30-minute waiting window, the batch was still `RUNNING` and
had produced **0 terminal paper results**. All ten paper `run_status.json` files
were still `RUNNING`; several logs showed ordinary document/PDF parsing output,
not a pipeline exception. Therefore no scientific task tree existed to compare
with the papers yet, and it would be invalid to claim that the scope-selection
objective had passed or failed from this batch.

The previous pre-fix batch remains independent and was not stopped. Its first
terminal examples are useful only as regression evidence: one paper was
scientifically approved but mechanically blocked solely by the typed
`required_deliverables` schema mismatch, and one paper ended in a Stage06B
converter retry. The former is the defect fixed in this round; the latter is the
prompt ambiguity addressed by the preceding `d536bc0` change and must be checked
against the new batch once a converter result is available.

## Additional narrow correction after reviewing the old artifact

Inspection of the blocked paper showed that its deliverable strings were result
labels (`HOMO_energy`, `conformer_geometries`, etc.), not artifact paths. Merely
wrapping those labels as typed paths would have made Pydantic validation pass
while leaving `TaskInfo.required_deliverables` inconsistent with
`submission_contract.required_files`. Commit `e1cfe92` therefore makes the
existing generic normalizer use the declared submission artifact paths when all
incoming entries are bare labels, and adds a Stage07 prompt check that scientific
result labels belong in the task/result schema rather than a file-path field.
This is a transport-contract repair, not a paper-specific rule. The full
Stage06/07 test selection remains **158 passed, 387 deselected**.
Replaying the previously blocked `paper_12c3b0b392f4dc14` audited tree through
the current mechanical gate now gives `mechanical_pre_publish_status=passed`,
`schema_load_diagnostic=passed`, with both mode deliverable lists projected to
`report/results.json` and `report/report.md`.

## Interim conclusion

No further code or prompt defect can be responsibly inferred from the incomplete
Round 6 batch. In particular, the absence of completed tasks is not evidence of
scientific rejection, Stage07 failure, or a need for Stage07B. The batch is left
running for its own normal completion; after terminal artifacts appear, each
paper will be reviewed against the v5 objective: full-route priority, justified
core-subprocess fallback, software-gap registration without scientific refusal,
answer-blind Stage06B conversion, independent Stage07 audit, and truthful
mechanical publication state.
