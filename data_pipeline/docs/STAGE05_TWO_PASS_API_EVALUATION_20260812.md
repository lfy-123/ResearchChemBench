# Stage05 Two-Pass API Gate: Implementation and Evaluation

Date: 2026-08-12

## Objective

Stage05 was changed from one model call over a heuristically truncated document packet to a two-pass API gate:

1. Stage05A uses `deepseek-v4-flash` as a high-recall Evidence Router.
2. Stage05B uses `deepseek-v4-pro` as a Candidate Auditor.

No Agent harness is used. The 24-paper development set is exactly the set that passed Stage04 in batch 0001 of
`stage00-04-batches-10000-strict-stage03-20260811`. The external comparison is
`stage05_gpt56_fulltext_agent_reference_20260812.jsonl`.

## Final Flow

### Stage05A Evidence Router

The router receives a balanced 60,000-character index built from the main paper and every Stage04-successful SI,
the Stage03 workflow inventory, frozen toolbox coverage facts, and the ten-task taxonomy. Code performs broad
keyword/software localization first. The model returns up to three workflow clusters with separate evidence IDs
for methods, inputs, parameters, results, claims, and cost.

`no_candidate_located` is not a rejection. Stage05B always receives code-selected fallback evidence, so a Router
false negative cannot by itself remove a paper.

### Stage05B Candidate Auditor

The auditor receives routed blocks expanded to their same section and neighboring blocks, plus a balanced
main/SI fallback, bounded to 90,000 characters. It returns at most one candidate and audits eight dimensions:

- scientific significance;
- workflow completeness;
- input assets;
- parameters;
- ground truth;
- software;
- cost;
- leakage risk.

The workflow must be a connected DAG with at least three scientific steps and a final computed artifact linked to
a paper claim. `pass` requires all dimensions confirmed. `needs_builder_review` is limited to uncertain inputs,
parameters, or ground truth with a deterministic recovery plan. Software, cost, significance, workflow, and
leakage safety must already be confirmed.

### Deterministic Contract

Recovery is limited to evidence extraction, format conversion, or retrieval by an explicit identifier present in
cited evidence. Valid external identifiers are SMILES/InChI, DOI, or an actual CCDC/ICSD/COD/PubChem/Materials
Project accession. Generic chemical names, facets, "standard databases", typical settings, manual docking,
chemical intuition, target matching, and customary defaults are not valid recovery plans.

Unknown evidence references are removed when other valid references remain. Stage03 software facts are immutable.
The code derives the legacy five-field `buildability_checks` object for Stage06 compatibility. A forwarded model
response that remains contract-invalid after one repair attempt becomes a Stage05 `reject` with the complete
validation reason preserved; an uninterpretable decision remains `contract_invalid`.

## Final 24-Paper Result

The final run is `runs/stage05-two-pass-eval-20260812`.

| Metric | Result |
|---|---:|
| Papers | 24 |
| `needs_builder_review` | 1 |
| `reject` | 23 |
| Processing failures | 0 |
| `contract_invalid` | 0 |
| Wall time | 251.6 s |
| GPT-5.6-sol exact three-class agreement | 19/24 (79.2%) |
| GPT-5.6-sol forward/reject agreement | 19/24 (79.2%) |

The final run used 24 Router results and 44 Auditor attempts including contract repair. The Router calls were cache
replays in the final iteration. Auditor attempts used about 1.86 million tokens in total. `deepseek-v4-pro`
thinking mode was tested but is not used in the final configuration: on this endpoint, long structured prompts
frequently consumed the complete output allowance as reasoning and returned empty JSON even at a 20,000-token
limit. Non-thinking Pro completed all papers reliably.

## Comparison With GPT-5.6-sol

| Paper | DOI | GPT-5.6-sol | Final Stage05 | Existing manual calibration | Analysis |
|---|---|---|---|---|---|
| `paper_02edc655062b6fbe` | 10.1002/anie.202402800 | pass | reject | pass | SI coordinates and a barrier exist, but the reactant/TS methods differ and exact TS construction/route settings remain inferred. Strict recovery correctly refuses to silently supply them. This is a likely recall loss under the current gate. |
| `paper_03362ac793543bf7` | 10.1002/anie.202400960 | pass | reject | needs_builder_review | Polymer/MD models lack exact oligomer structures, simulation boxes, and paper-specific force-field parameters. The final rejection is defensible and avoids a Builder task based on guessed models. |
| `paper_03623c7ee35aacf6` | 10.1002/anie.202402233 | reject | needs_builder_review | pass | SI contains labeled Cartesian coordinates and thermochemical values. Recovery is only deterministic extraction, so forwarding is well supported. GPT-5.6-sol appears overly strict here. |
| `paper_0826aceebc3c3120` | 10.1002/anie.202402694 | needs_builder_review | reject | reject | The periodic cell does not uniquely define the terminated Gaussian cluster used for adsorption energetics. Final rejection agrees with full-text manual calibration. |
| `paper_194b1609fd2f6cfb` | 10.1002/anie.202316790 | needs_builder_review | reject | reject | Parsed paper/SI provide qualitative reaction-path figures but no recoverable quantitative energy or barrier target. Final rejection avoids inventing ground truth. |

The GPT and existing manual labels disagree substantially: the final Stage05 binary agreement with the manual
calibration is 13/24, while the GPT and manual references themselves agree on only 12/24 binary decisions. Neither
reference is an independent gold set. This 24-paper set has been repeatedly used for prompt development and must be
treated as a calibration set, not a generalized accuracy estimate.

## Iteration Findings

- A Router plus targeted evidence expansion prevents the final model from relying only on a mixed heuristic sample.
- A scientific workflow graph is more reliable than counting three natural-language steps.
- Software, cost, and leakage decisions are derived facts and do not always need a single source block; requiring a
  fake citation caused contract failures.
- Multiple independent reference calculations are valid graph roots only when a downstream step joins them.
- Free-text recovery plans hide assumptions. A structured and code-validated plan removed false positives involving
  default pseudopotentials, typical slabs, hand-built interfaces, arbitrary conformer searches, and target-guided
  parameter selection.
- Model response truncation and scientific rejection must be distinct. The API client now reports reasoning
  exhaustion explicitly rather than a generic JSON decoding error.

## Remaining Risk and Next Evaluation

The final gate is intentionally high precision and low recall: it forwards only 1/24 papers, and it rejects one
paper labeled pass by both historical references. Before production-scale use, create a new publisher- and
task-diverse holdout that was not used in this work. Report forward precision/recall, false-negative reasons,
Builder success rate, and cost per built task. The current 79.2% GPT agreement is descriptive only.

Machine-readable outputs are available in:

- `runs/stage05-two-pass-eval-20260812/stage_05_benchmark_suitability/decisions.jsonl`;
- `runs/stage05-two-pass-eval-20260812/stage_05_benchmark_suitability/evidence_routes.jsonl`;
- `runs/stage05-two-pass-eval-20260812/stage_05_benchmark_suitability/candidate_audits.jsonl`;
- `runs/stage05-two-pass-eval-20260812/comparison_rows.jsonl`;
- `runs/stage05-two-pass-eval-20260812/comparison_summary.json`.
