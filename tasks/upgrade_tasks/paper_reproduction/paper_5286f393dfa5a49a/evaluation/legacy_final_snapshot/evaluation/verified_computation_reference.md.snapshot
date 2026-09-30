# Verified computation reference — paper_5286f393dfa5a49a (paper_reproduction)

> Evaluator-private archive of real successful historical calculations. This is not an evaluator, answer input or claim of a blind agent replay. Scoring remains defined by the task/evaluator key points and conclusions.

## Current scope and source

Reviewed 2026-09-15 by reading existing outputs and performing arithmetic only. No new electronic-structure jobs were run. docs/verification is read-only: discrepancies in its historical status/prose are reconciled here, without changing those records. This replaces the old truncated automatic excerpt; its prior version remains in Git 40a6cb60.

Unmodified historical scientific record: [results.json](../../../../docs/verification/group_5/paper_5286f393dfa5a49a/report/results.json). Verification history: [verification_report.md](../../../../docs/verification/group_5/paper_5286f393dfa5a49a/verification_report.md).

Author coordinates/routes used in verification remain private. Their use does not invalidate author-route feasibility; no independent discovery from the current public starter is claimed. The two modes share numerical verification evidence, not the same public information.

Primary source: [SI](../../../../papers/paper_5286f393dfa5a49a/documents/supplementary_001.pdf) PDF p.7 §1.6 and p.14 Fig.S10; main paper p.2. The authors optimize at B3LYP-D3/def2-TZVP(-f)/SMD(DCM), then refine with ωB97M-V/def2-TZVP/SMD(DCM). Approved D3 fixes the benchmark inputs and uses only that energy-refinement method for the primary three-geometry comparison. It does not require a new optimization/frequency step.

## Effective successful chain

1. Identify the three fixed, labeled 138-atom neutral singlet geometries: crystal, (RRRR)-MM and (SSSS)-MM, composition C80H42Cl4N4O8. Preserve atom order and coordinates.
2. Execute the already archived ORCA 6.1.1 wB97M-V/def2-TZVP/def2-J, RIJCOSX, SMD(dichloromethane), TightSCF/MaxIter300 single points. Each linked output has normal termination and the final single-point energy listed below.
3. Extract E_i and compute (E_i−E_crystal)×2625.4996394799 kJ/mol; separately compute (E_RRRR−E_SSSS) with the same conversion.
4. Interpret only this finite fixed-geometry comparison. No minimum or frequency success is fabricated for a single-point job.

| Geometry | E Eh | Relative to crystal kJ/mol | Raw successful output |
|---|---:|---:|---|
| crystal | -5736.001929929570 | 0.000000000 | [crystal ORCA](../../../../docs/verification/group_5/paper_5286f393dfa5a49a/provenance/qzcli_hpc/crystal_fixed_wb97mv_smd_author_energy_retry2/1_20260908T041145097377225_266/orca_stdout.log) |
| (RRRR)-MM | -5735.996111646958 | 15.275898901 | [(RRRR)-MM ORCA](../../../../docs/verification/group_5/paper_5286f393dfa5a49a/provenance/qzcli_hpc/rrrr_mm_fixed_wb97mv_smd_author_energy_retry2/1_20260908T041146153734166_344/orca_stdout.log) |
| (SSSS)-MM | -5735.993609645396 | 21.844903100 | [(SSSS)-MM ORCA](../../../../docs/verification/group_5/paper_5286f393dfa5a49a/provenance/qzcli_hpc/ssss_mm_fixed_wb97mv_smd_author_energy_retry2/1_20260908T050624559206176_343/orca_stdout.log) |

E_RRRR−E_SSSS = −6.569004199 kJ/mol. The paper reports −6.56 kJ/mol; the reference is not derived by copying this local value into the evaluator. The fixed geometries rank crystal < RRRR < SSSS under the approved primary protocol.

## Separate sensitivity evidence and limits

The prior gas-phase B3LYP-D3BJ/def2-SVP fixed-geometry comparison (+12.922450 kJ/mol for RRRR−SSSS) is a different-model sensitivity, not a failed author-method result or the primary comparison. Its records remain in [independent_results.json](../../../../docs/verification/group_5/paper_5286f393dfa5a49a/artifacts/independent_results.json). Do not splice methods or require an arbitrary alternative method to give identical ordering.

The primary fixed-input identity/SCF/convergence/relative-energy key points are supported; this does not establish optimized minimum identities, lattice energy or global conformer thermodynamics. Source ORCA 6.0 versus local 6.1.1 is recorded. An agent may submit optimization as a separate optional sensitivity branch.

## Maintenance boundary

This document records successful scientific dependencies rather than queue chronology. Failed/cancelled jobs are not steps in this chain; an actually successful retry-labeled output is valid. Full vectors, settings and arrays are retained in the linked evidence, not silently cut to eight entries. The archive is not a requirement that a future agent copy the author route.
