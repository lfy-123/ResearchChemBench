# GEOM and Electron Autonomous Tasks: Strict Rescoring

Date: 2026-07-26

## Scope

The original DeepSeek V4 Flash Agent trajectories and chemistry calculations were not rerun.
The existing complete workspaces were rescored with the revised autonomous rubric and hidden
scientific-outcome gates introduced in commit `3c8f16b`.

Workspaces:

- `GEOM_Hierarchical_Conformer_Reranking_opencode_20260726_103452_37b4ec`
- `Electron_Flexible_Ensemble_Surface_opencode_20260726_105217_64d3fa`

The Judger was `deepseek-v4-flash` in both cases.

## Score summary

| Task | Old Judger | Strict Flash Judger | Independent strict review | Main interpretation |
|---|---:|---:|---:|---|
| GEOM hierarchical conformer reranking | 85 | 58 | 55 | Strong autonomous workflow, but the required thermochemical population conclusion remains unresolved. |
| Electron flexible ensemble surface | 93 | 95 | 57 | The conformer surface effect is supported, but the four-conformer electronic-energy ensemble is not sufficiently converged or thermodynamically validated. |

## 1. GEOM hierarchical conformer reranking

### Flash Judger result: 58/100

| Criterion | Flash score |
|---|---:|
| Hidden scientific conclusion recovery | 15/50 |
| Autonomous method and route design | 18/20 |
| Adaptive managed execution | 10/10 |
| Validation and falsification | 10/15 |
| Provenance and uncertainty | 5/5 |

The Flash Judger returned:

- `reference_conclusion_status = uncertain`
- failed gate: `thermochemical_population_validity`
- reference-conclusion cap: 60
- evidence-gate cap: 65
- final score: 58

This is a substantially better application of the strict policy than the old 85-point result.
The run generated 27 CREST conformers and performed B3LYP single-point refinement for 12
conformers plus a PBE0 perturbation for seven. These calculations support the conclusion that
the low-cost and DFT electronic-energy rankings differ materially. They do not establish the
required thermochemical population conclusion because no DFT geometry optimization, frequency,
or free-energy calculation was performed.

### Independent score: 55/100

| Criterion | Independent score | Reason |
|---|---:|---|
| Hidden scientific conclusion recovery | 15/50 | Multiple basins and electronic-energy reranking are supported, but the thermochemical part of the hidden contract is not completed. |
| Autonomous method and route design | 17/20 | The hierarchy and perturbation are sensible, but the plan is incomplete for a task explicitly asking about thermally important populations. |
| Adaptive managed execution | 10/10 | The managed conformer search, energy calculations, and analysis programs succeeded with traceable artifacts. |
| Validation and falsification | 8/15 | PBE0 provides useful method sensitivity, but there is no DFT geometry/frequency validation, no thermochemistry, and no convincing search-coverage convergence test. |
| Provenance and uncertainty | 5/5 | Claims, artifacts, assumptions, and limitations are clearly linked and disclosed. |

The independent result agrees with Flash on the decisive issue and differs by only three points.
The strict evaluation is therefore functioning reasonably for GEOM.

## 2. Electron flexible ensemble surface

### Flash Judger result: 95/100

| Criterion | Flash score |
|---|---:|
| Hidden scientific conclusion recovery | 50/50 |
| Autonomous method and route design | 18/20 |
| Adaptive managed execution | 10/10 |
| Validation and falsification | 12/15 |
| Provenance and uncertainty | 5/5 |

The Flash Judger returned:

- `reference_conclusion_status = matched`
- no failed evidence gate
- no score cap
- final score: 95

The first hidden finding is well supported within the computed subset. Four conformers produced
0.001-a.u. surfaces from 158.69 to 170.35 A2, a 6.9% range, while the tested grid-spacing effect
was only 0.019%. Thus, the conformer effect is materially larger than the demonstrated numerical
integration error.

The second hidden finding is not established to the standard required for full credit:

1. Only four RDKit-generated conformers were retained for a molecule whose paper ensemble
   contains 25 conformers.
2. There was no repeated or expanded conformer search and no post-hoc basin/conformer-space
   convergence test.
3. Boltzmann weights used B3LYP electronic single-point energies only. No vibrational free
   energies or sensitivity test showed that the 86% dominant-conformer weight is stable.
4. The reported `2.91 A2 conformer-sampling uncertainty` is the weighted spread of the four
   computed surfaces; it does not quantify uncertainty from missing conformers.
5. Electron-count validation was not completed, and no density-method or basis-set sensitivity
   was performed.

The Judger itself mentioned the missing conformer convergence and missing free-energy sensitivity,
but nevertheless marked `ensemble_validity` as passed and the hidden conclusion as fully matched.
That is internally inconsistent with the new gate definition.

### Independent score: 57/100

| Criterion | Independent score | Reason |
|---|---:|---|
| Hidden scientific conclusion recovery | 18/50 | The conformer-dependent surface effect is supported, but the thermal-ensemble conclusion is only provisional because ensemble coverage and weights are not validated. |
| Autonomous method and route design | 17/20 | The end-to-end route is strong and independently chosen, but the sampling and thermodynamic validation plan is insufficient. |
| Adaptive managed execution | 10/10 | The Agent successfully chained conformer generation, xTB optimization, ORCA density, wavefunction export, Multiwfn surfaces, and managed analysis. |
| Validation and falsification | 8/15 | Grid and within-set truncation tests are useful, but they do not replace conformer-space convergence, weight/free-energy sensitivity, electron-count validation, or method/basis sensitivity. |
| Provenance and uncertainty | 4/5 | Provenance is strong, but the weighted surface spread is overstated as conformer-sampling uncertainty and the approximate ensemble is described as physically rigorous. |

The independent review assigns `reference_conclusion_status = uncertain`. Under the strict policy,
the conclusion criterion is limited to at most 20 points and the overall score to at most 60. It
also marks `ensemble_validity` as failed. The resulting evidence-weighted score is 57.

## 3. Judger reliability under the new rubric

The new scoring standard successfully reduced the GEOM score from 85 to 58 and correctly applied
the thermochemical gate. It did not by itself eliminate Judger leniency for Electron. The score
engine can enforce a cap only after the LLM Judger reports a failed gate or a non-matched conclusion;
most scientific gates are currently semantic rather than deterministically computed from structured
artifacts.

Therefore:

- GEOM strict Judger score is credible and close to the independent score.
- Electron strict Judger score remains substantially inflated: 95 versus an independent 57.
- Future hardening should add structured, machine-checkable fields for conformer count/coverage,
  weighting basis, thermochemistry availability, electron-count validation, and sensitivity tests,
  so an LLM Judger cannot acknowledge a missing requirement while still passing its gate.

## 4. Judger resource usage

| Task | Prompt tokens | Completion tokens | Total Judger tokens |
|---|---:|---:|---:|
| GEOM | 103,950 | 3,939 | 107,889 |
| Electron | 85,582 | 3,318 | 88,900 |
| Total | 189,532 | 7,257 | 196,789 |

