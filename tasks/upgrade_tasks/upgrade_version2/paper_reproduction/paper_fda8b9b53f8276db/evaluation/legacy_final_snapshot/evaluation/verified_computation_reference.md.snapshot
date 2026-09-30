# Verified computation reference — paper_fda8b9b53f8276db (paper_reproduction)

Evaluator-private verification of the author cis local-minimum geometry and its six paired SI Table S2 bond lengths. Reconciled 2026-09-23 using existing raw calculations; no new optimization was required. The public task supplies experimental observations only, and the agent independently constructs the requested conformer.

## Source and calculation

Main PDF §2.4 identifies a cis theoretical pyridyl orientation compared with the crystal trans orientation. SI Table S2 gives the six paired distances below; Table S3 and Fig. S11 support the theoretical geometry. The source regression is calculated from the printed experimental precision, with experimental x and calculated y, an intercept, and direct bond residuals for RMSE.

The existing Gaussian 16 C.01 calculation uses B3LYP/6-311+G(2d,p) in the gas phase, optimization and frequency analysis, charge 0 and multiplicity 1. It contains 31 atoms, completed optimization, normal termination and 87 real frequencies (zero imaginary modes). The author used Gaussian 03; the local software release and numerical settings are verification choices, not claimed identical author inputs.

[Raw cis input/output](../../../../docs/verification/group_2/paper_fda8b9b53f8276db/provenance/qzcli_hpc/author_CIF_derived_cis_conformer_optfreq_20260916_20260916T105546Z) · [Independent geometry/mapping audit](../../../../docs/verification/group_2/paper_fda8b9b53f8276db/provenance/cis_final_closure_20260918/FINAL_AUDIT.md) · [Optimized cis coordinates](../../../../docs/verification/group_2/paper_fda8b9b53f8276db/provenance/cis_final_closure_20260918/computed_cis_minimum.xyz).

## Matched cis endpoint

| SI label pair | Gaussian atom indices (1-based) | SI experimental / Å | SI theoretical / Å | Local calculated / Å |
|---|---|---:|---:|---:|
| C1–C2 | 9–8 | 1.483 | 1.489 | 1.4893852605 |
| C2–C3 | 8–14 | 1.429 | 1.426 | 1.4256881387 |
| N1–C1 | 3–9 | 1.341 | 1.339 | 1.3393531829 |
| N2–C2 | 1–8 | 1.319 | 1.316 | 1.3161630391 |
| N3–C3 | 2–14 | 1.314 | 1.310 | 1.3099109186 |
| C1–C10 | 9–16 | 1.394 | 1.399 | 1.3989153534 |

The mapped N1–C1–C2–N2 torsion has magnitude 36.669013°. Its mirror-related sign is equivalent; this is the cis family specified in the public task. The local electronic energy is approximately 5.45909 kcal/mol above a separately computed trans minimum, so these data establish a cis local minimum, not global stability.

- Local cis vs supplied SI experimental values: RMSE **0.004150935968 Å**, fitted-intercept OLS R² **0.997884657422**, slope **1.046981907819**, intercept **−0.064932383924 Å**.
- Printed SI theoretical vs experimental values: RMSE **0.004062019202 Å**, OLS R² **0.998042651229**, slope **1.046746184880**, intercept **−0.064676401801 Å**. These reproduce the source precision of 0.004 Å, 0.998, 1.0467 and −0.0647.
- Local vs SI theoretical distances: RMSE **0.000262076183 Å**. The independent full heavy-atom distance-matrix comparison is approximately **0.000700 Å**.

The six rows, conformer mapping, raw geometry, stationarity and common experimental precision must be considered together. A high correlation or a smaller overall RMSE alone does not establish the same scientific object. The independent numbers are feasibility evidence; source references remain the grading references and the existing numeric tolerance has not been fitted to these results. Historical run outputs and scores are not changed by this contract revision.
