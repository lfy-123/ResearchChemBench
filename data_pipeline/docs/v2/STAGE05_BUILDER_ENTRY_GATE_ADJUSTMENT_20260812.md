# Stage05 Builder Entry Gate Adjustment

Date: 2026-08-12

## Purpose

Stage05 is the last paper-level gate before Stage06 Builder. It decides whether a paper contains at least one
scientifically meaningful, toolbox-covered, affordable, and scoreable computational candidate. It does not require
the final benchmark task, executable input files, or hidden-answer package to have already been built.

The previous contract confused evidence readiness with file readiness. In the 24-paper calibration run, the
auditor returned 19 `needs_builder_review` decisions, but deterministic validation converted 18 of them to
`reject`, mostly because input assets were not already materialized. This was too strict for a pre-Builder gate.

## Decision Boundary

### `pass`

Forward directly to Builder when all eight audit dimensions are confirmed from supplied main-paper or SI evidence:

- the task reproduces a meaningful claim or key intermediate;
- the workflow has dependent scientific steps and machine-computable scoring;
- required software is covered by the frozen Stage03 toolbox inventory;
- a bounded implementation fits the configured resource budget;
- inputs, task-defining parameters, and ground truth are semantically fixed by supplied evidence;
- public inputs can be frozen without looking at hidden target values.

Confirmed does not mean pre-built. Builder may extract labeled SI coordinates, parse numeric tables, normalize
units, convert file formats, and write native software input decks.

The auditor may select one explicitly identified, evidence-complete workflow from a larger paper. It does not
require every analogous molecule, pathway, surface, or state in that paper to be reconstructable. The bounded
subset must be frozen from public identifiers before hidden targets are read, and must still support a nontrivial
workflow and concrete scientific claim. Quantitative targets may be distributed across multiple cited blocks or SI
tables when each target maps unambiguously to that frozen candidate.

### `needs_builder_review`

Forward with a review requirement when significance, workflow, software, cost, and leakage safety are confirmed,
but inputs, parameters, or ground truth require a bounded verification. Every uncertain dimension must have a
structured, evidence-cited, target-independent recovery plan. Supported resolution types are:

- `evidence_extraction`;
- `format_conversion`;
- `evidence_verification`;
- `evidence_anchored_construction`;
- `explicit_identifier_retrieval`.

Examples include checking a structure-to-label mapping, verifying a partially parsed parameter table, resolving an
explicit deposition, or following a fully stated construction protocol.

An evidence-anchored construction is valid only when cited evidence freezes every task-defining choice. "Standard",
"reasonable", customary, or target-matching choices are not a recovery plan. These include unspecified slab size,
vacuum, adsorption site, termination, spin state, k-point mesh, force-field parameter, defect placement, and initial
configuration.

`evidence_verification` may resolve a supplied label, mapping, transcription, or interpretation, but cannot hide
construction of a missing scientific model. A plan that constructs a slab, structure, defect model, configuration,
coordinate set, force field, simulation box, or supercell must use `evidence_anchored_construction`.

### `reject`

Reject when any hard gate fails:

- scientific workflow or claim is trivial/incomplete;
- essential software is not covered or cannot be identified;
- the smallest scientifically faithful task exceeds the budget;
- a quantitative ground truth is absent;
- a required bespoke asset is unavailable;
- task-defining inputs or parameters require customary defaults, scientific guesswork, or target-guided selection;
- public input construction would leak hidden answers.

## Deterministic Validation

The validator checks schema, evidence IDs, software facts, workflow graph, cost bounds, decision consistency, and
recovery-plan structure. It conservatively rejects explicit customary/default/target-guided choices in recovery
prose, and `target_independent` must be true with an empty assumptions list. The scientific conclusion remains the
auditor's responsibility; this lexical check is only a safety backstop for an otherwise structured plan.

An explicit identifier retrieval remains stricter: the exact DOI, SMILES/InChI, or repository accession must occur
in cited evidence and match its identifier format.

## Pipeline Flow

1. Stage05A routes high-recall evidence for up to three coherent computational workflows.
2. Stage05B independently audits the strongest candidate over routed and fallback main/SI evidence.
3. Deterministic validation enforces scientific structure and the decision contract.
4. `pass` and `needs_builder_review` are written to `candidates.jsonl` for Stage06.
5. Stage06 Builder materializes assets and may still abstain if extraction or verification fails.
6. Stage07 judges the generated task; Stage05 forwarding is not a guarantee of final benchmark inclusion.

## Evaluation Rule

The existing 24 papers are a development/calibration set, not an independent accuracy benchmark. A change is
accepted only when supplied assets no longer fail merely for requiring materialization, bounded uncertainties stay
reviewable, and papers requiring subjective reconstruction remain rejected. Final precision must be measured on a
new holdout using Builder success and Judge outcomes, not a target Stage05 pass rate.

## 24-Paper Regression

Final run: `runs/stage05-builder-entry-eval-20260812-final-r2`.

| Metric | Result |
|---|---:|
| Papers | 24 |
| `pass` | 0 |
| `needs_builder_review` | 2 |
| `reject` | 22 |
| Processing errors | 0 |
| GPT-5.6-sol binary forward/reject agreement | 20/24 (83.3%) |
| Runtime | 881.5 seconds |

The runtime was dominated by API-side queueing; previous iterations over the same 24 papers completed in roughly
107-163 seconds. Both forwarded papers contain supplied coordinate/result evidence and require bounded label/table
verification. A CeO2 slab candidate that previously passed through `evidence_verification` was rejected after the
validator required missing model construction to use the stricter `evidence_anchored_construction` contract.

Zero direct `pass` decisions in this small run does not mean zero usable papers. Both review candidates are sent to
Stage06 and can become tasks if deterministic materialization succeeds. Conversely, Stage05 does not target a pass
rate: papers with unavailable bespoke inputs, incomplete task-defining parameters, subjective slab/MD construction,
or insufficient quantitative ground truth remain rejected.
