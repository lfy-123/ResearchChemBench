# Stage05 DeepSeek V4 Pro Evaluation (2026-08-12)

## Scope

This evaluation used all 24 papers whose main paper and known supplementary documents completed Stage04 MinerU
normalization in batch 0001 of `stage00-04-batches-10000-strict-stage03-20260811`. Every paper was inspected against
the normalized main text and SI before the final calibration labels were assigned.

Stage05 is a paper gate before the expensive Builder. It must answer whether a scientifically meaningful,
toolbox-covered, cost-bounded candidate is worth Builder effort. It must not require a finished input deck or final
hidden-answer package.

## Final Manual Calibration Labels

The final labels contain 2 `pass`, 10 `needs_builder_review`, and 12 `reject` papers. The 12 forwarded candidates
cover molecular optimization/thermochemistry, electron-density analysis, periodic adsorption and reaction paths,
molecular dynamics/property calculations, vibrational spectroscopy, and computed descriptors.

The detailed machine-readable labels are stored in `stage05_calibration_labels_20260812.jsonl`. Four initial labels
were revised after a second full-text review:

- The TBUPP-Cu adsorption paper was changed to reject because its periodic coordinates do not uniquely define the
  terminated molecular cluster used for the reported energetics.
- The model-compound IR paper was changed to Builder review because a CCDC structure plus optimization, frequency
  calculation, simulated IR, and experimental-spectrum comparison form a complete candidate.
- The three-oxide d-band paper was changed to Builder review because optimization, DOS, descriptor extraction, and
  mechanistic comparison form a bounded descriptor workflow on standard unit cells.
- The electrolyte reaction-path paper was changed to reject because the SI supplies qualitative figures but no
  recoverable numerical energy/barrier target for an objective score.

## Iteration Results

| Iteration | Effective result | Main finding |
|---|---:|---|
| Baseline | 0 forwarded; 22 abstain; 2 API/JSON failures | Stage05 incorrectly required Builder-complete assets. |
| Iteration 1 | 0 forwarded; 19 reject; 1 invalid; 4 API/JSON failures | Three-state contract alone did not fix the overly strict asset policy. |
| Iteration 2 | 8 forwarded; 9 reject; 7 contract-invalid | Evidence and asset rules improved, but shortened evidence IDs were rejected. |
| Iteration 3 (r11) | 2 pass; 10 review; 12 reject; 0 failures | All 24 decisions match the final manually reviewed calibration labels. |

Iteration 3 made 26 calls including contract retries, used 1,031,404 total API tokens, and completed in about 335
seconds wall time with eight concurrent workers. One first response ended at the output length limit and was repaired
by the existing contract retry. This is a prompt-development calibration set, not an independent holdout; the 100%
agreement must not be reported as generalized accuracy.

## Implemented Changes

- Added `pass`, `needs_builder_review`, and `reject` semantics. Builder review is allowed only for recoverable input,
  parameter, or ground-truth uncertainty; software and cost must already be confirmed.
- Defined hard asset boundaries: standard molecules/crystals/facets may be reconstructed and verified, while absent
  amorphous structures, custom interfaces, grain boundaries, trajectories, force fields, and trained models block a
  task when reconstruction needs scientific guesses.
- Required a meaningful claim, at least three dependent scientific stages, an objective hidden target, validation,
  and a machine-computable score. A single calculation split into preparation/run/readout does not qualify.
- Added taxonomy scope descriptions, including MD structural/transport observables and descriptor workflows.
- Treated only actual required compute/preprocessing/analysis software as gate facts. Background, instrument,
  visualization, and optional tools no longer become false software blockers.
- Replaced sequential evidence truncation with per-document title coverage, computation/method/result/cost relevance,
  neighboring context, and distributed sampling. Oversized MinerU table blocks retain a bounded marked prefix.
- Deterministically resolves a model-shortened MinerU evidence ID only when it uniquely maps to one full hashed ID.
- Raised the default Stage05 output limit from 4096 to 8192 to prevent DeepSeek reasoning from consuming the output
  allowance and returning empty/truncated JSON.

## Final Stage05 Flow

1. Read all Stage04-successful main and SI MinerU blocks.
2. Build a bounded cross-document evidence packet without losing late SI methods/results.
3. Pass immutable required-software facts, resource budget, workflow summary, and taxonomy scope to the suitability
   model.
4. Select at most one smallest scientifically faithful candidate.
5. Validate taxonomy, workflow depth, scoring, cost, buildability state, software coverage, and evidence references.
6. Retry one structurally invalid response without changing the scientific conclusion.
7. Forward `pass` and `needs_builder_review`; retain `reject`, `contract_invalid`, and processing failures for audit.

## Remaining Work

- Build a new publisher/task-diverse holdout set not used for prompt development and report precision/recall there.
- Validate Stage05 coarse runtime estimates against Builder-generated workflows and probe runs; the present estimates
  remain model-derived upper bounds.
- When the requested GPU worker becomes available, recover the 308 Stage04 document attempts interrupted by service
  loss, then test MinerU concurrency 8, 12, and 16 while tracking GPU utilization, GPU memory, host RAM, latency, and
  failure rate. Stop increasing concurrency when throughput plateaus or errors/resource pressure rise.
