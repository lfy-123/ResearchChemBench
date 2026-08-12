# Stage05 Recall-Gate Adjustment (2026-08-13)

## Goal

The previous Stage05 builder-entry gate was too strict. On the 24-paper calibration set it
forwarded only 2 papers, overlapping 1 of 4 GPT-5.6-sol forward decisions and 2 of 12 manual
full-text forward decisions. Overall binary agreement was misleading because rejecting every
paper would already score well on this imbalanced set.

Stage05 is now a recall-oriented candidate gate. It may forward bounded gaps to Stage06, while
Stage06 Builder and Stage07 Judge remain responsible for final task validity. It must still reject
missing task-defining chemistry, uncovered required software, target leakage, unscoreable tasks,
bespoke unavailable assets, and out-of-budget work.

## Implementation

### Builder routes

Every forwarded candidate has one explicit route:

- `exact_reproduction`: supplied evidence fixes the task and all audit dimensions.
- `evidence_recovery`: Stage06 only extracts or verifies cited evidence and identifiers.
- `normalized_reconstruction`: Stage06 may use the frozen
  `researchchembench_normalized_v1` protocol for ordinary numerical settings or bounded,
  target-independent enumeration.

The route is derived from the validated recovery plan. Stage06 receives the route, recovery plan,
protocol ID, provenance requirement, and hidden-target isolation requirement.

### Relaxed but nontrivial workflow gate

- The minimum workflow is two dependent scientific stages instead of three.
- Setup, launching software, and reading output do not count as scientific stages.
- Supporting calculations may qualify when they test a chemical claim and provide a
  machine-scoreable value, ordering, class, sign, threshold, or structured trend.
- Missing ready-made files or ordinary convergence settings are not hard blockers by themselves.

### Evidence-backed rejection

A reject response must contain structured `hard_blockers` with a valid blocker code, audit
dimension, reason, and evidence IDs. Contract retries are limited to schema errors. A retry may
repair the response shape but cannot change the original scientific decision class.

### Recovery safety

The validator permits evidence extraction, explicit-identifier retrieval, format conversion,
bounded evidence-anchored construction, and the frozen normalized protocol. It rejects:

- hidden-target-guided model or parameter selection;
- missing charge, composition, structure identity, defect placement, reaction path, or force-field
  family;
- arbitrary replacement of an unspecified supported cluster or interface;
- custom grain-boundary, amorphous, equilibrated, or randomly selected author configurations;
- exact coordinate recovery from a figure;
- ambiguous protonation, morphology, metric, or other task-defining choices.

Both the recovery procedure and its assumptions are checked. Previously only assumptions were
checked, which allowed scientific choices written in the procedure to bypass validation.

### Deterministic context and evaluation

The auditor evidence packet previously iterated routed evidence IDs through a Python `set`.
Different hash seeds changed block priority, request hashes, and occasionally model decisions.
The packet now preserves router field order and first occurrence with deterministic de-duplication.

The evaluation report now records forward-set precision, recall, Jaccard, overlap IDs, false
positives, and false negatives for both GPT-5.6-sol and manual full-text labels. This prevents a
high reject-majority accuracy from hiding zero or low useful-paper recall.

## Evaluation

The final evaluation uses the same 24 papers, Flash evidence routing, and Pro candidate auditing.
The final metrics are an offline replay of the saved final API responses after applying the last
validator fix, so model sampling cannot change the comparison.

| Metric | Previous gate | Adjusted gate |
|---|---:|---:|
| Forwarded papers | 2/24 | 5/24 |
| GPT-5.6-sol forward overlap | 1/4 | 2/4 |
| GPT-5.6-sol forward recall | 25.0% | 50.0% |
| Manual full-text forward overlap | 2/12 | 5/12 |
| Manual full-text forward precision | 100.0% | 100.0% |
| Manual full-text forward recall | 16.7% | 41.7% |

The five final forwarded papers are:

| Paper | GPT-5.6-sol | Manual full text | Stage05 route |
|---|---|---|---|
| `paper_02edc655062b6fbe` | pass | pass | evidence recovery |
| `paper_03362ac793543bf7` | pass | needs Builder review | normalized reconstruction |
| `paper_03623c7ee35aacf6` | reject | pass | evidence recovery |
| `paper_1054a2171ce17c89` | reject | needs Builder review | evidence recovery |
| `paper_1089382cc545ebea` | reject | needs Builder review | normalized reconstruction |

GPT-5.6-sol also forwards `paper_0826aceebc3c3120` and `paper_194b1609fd2f6cfb`, but the manual
full-text labels reject both. The first lacks a uniquely recoverable task model and has an uncovered
required workflow dependency; the second lacks a recoverable quantitative target. They were not
forced through merely to improve agreement with one reference model.

Artifacts:

- Final fixed-response replay:
  `data_pipeline/runs/stage05-recall-gate-eval-20260813-final-replay/`
- Final online model responses:
  `data_pipeline/runs/stage05-recall-gate-eval-20260813-final-online/model_calls/`
- GPT-5.6-sol reference:
  `data_pipeline/docs/stage05_gpt56_fulltext_agent_reference_20260812.jsonl`
- Manual calibration labels:
  `data_pipeline/docs/stage05_calibration_labels_20260812.jsonl`

## Verification

- `311` data-pipeline tests passed.
- Ruff passed for `src`, `tests`, and the Stage05 evaluation script.
- `git diff --check` passed.
- The final replay completed all 24 papers with no processing errors.

## Remaining risk

This 24-paper set is a calibration set, not an independent gold holdout. GPT-5.6-sol and manual
full-text labels disagree on several papers, and a single Pro call still shows scientific judgment
variance. Do not tune more paper-specific rules on this set. The next quality measurement should
use a new independently labeled holdout and report forward precision/recall, not only overall
agreement. Stage06 and Stage07 must continue to abstain or reject candidates whose normalized
reconstruction cannot be frozen without hidden-target leakage.
