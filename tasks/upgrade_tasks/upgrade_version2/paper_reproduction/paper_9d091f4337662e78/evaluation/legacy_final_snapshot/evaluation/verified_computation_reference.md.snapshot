# Verified computation reference — paper_9d091f4337662e78 (paper_reproduction)

> Private record of actual successful verification; evaluation remains based on intermediate key points and final conclusions.

## Release reconciliation (2026-09-15)

This evaluator-private reference replaces the old truncated automatic archive. `docs/verification` remains read-only. No quantum calculation, HPC action or optimization of the current public starters was performed.

## Paper and approved scope

The [SI](../../../../papers/paper_9d091f4337662e78/documents/supplementary_001.pdf), PDF p. 5 Table S1, reports gas-phase M06-2X-D3 conformer Gibbs energies at 298.15 K. The first three relative values are 0, 0.680486100 and 0.771969325 kcal/mol; these are the existing evaluator targets, not numbers inferred from local verification. The table labels its full 16-member ensemble as 16-1…16-16, while coordinate Tables S2–S4 (PDF pp. 6–8) identify the selected structures as 1-1/1-2/1-3. The published 32.77/10.39/8.90% belong to the full ensemble and must not be compared directly with the approved three-member task.

D6 is approved: retain three distinct final conformer identities, separate starter IDs from endpoint IDs, count merged endpoints once and do not claim complete three-member populations if a member is missing. Identity is established by graph, atom mapping and final conformational features, never by proximity to a target energy. The independently generated public starters remain unchanged.

## Successful author-route chain

1. Historical validation used the SI-derived three conformers, with one-based interleaved coordinate-row mapping retained, neutral singlet C24H24N2O4 (54 atoms). This was not an autonomous discovery trajectory.
2. Each structure completed Gaussian M06-2X/6-311G(d,p), EmpiricalDispersion=GD3 Opt/Freq in gas phase. All three outputs record optimization completion, normal termination and 156 positive modes (3N−6).
3. Each matched endpoint was used for the corresponding M06-2X-GD3/6-311+G(2d,p) single-point refinement. All refinements terminated normally; the optimized and SP coordinate distance matrices are identical at printed precision. Earlier plain-M062X and failed jobs are not part of this primary chain.
4. Extract G_i = E_refined,i + thermal_G_correction_i using the matched 298.15 K Gaussian correction. Use ΔG_i = (G_i − min G) × 627.5094740631 kcal/mol per Eh.
5. Compute three-member populations p_i = 100 exp(−ΔG_i/RT)/Σ_j exp(−ΔG_j/RT), with R=0.00198720425864083 kcal mol⁻¹ K⁻¹ and T=298.15 K. Do not reuse the full 16-member SI population percentages.
6. Bind each endpoint to its source identity by chemical mapping and distinguishing torsions, then compare the unchanged numerical targets/tolerances. Distinct opposite-sign torsion classes below show that these three historical endpoints are not duplicates. The public initial windows are not optimization constraints or target angles.

## Actual thermochemistry

| Source identity | Refined E / Eh | Thermal G correction / Eh | G / Eh | ΔG / kcal mol⁻¹ | Three-member population / % | Lowest frequency / cm⁻¹ |
|---|---:|---:|---:|---:|---:|---:|
| 1-1 | -1339.25858491 | 0.380809 | -1338.87777591 | 0.000000000 | 59.609070 | 7.8008 |
| 1-2 | -1339.25851552 | 0.381700 | -1338.87681552 | 0.602653824 | 21.555794 | 10.1768 |
| 1-3 | -1339.25840413 | 0.381716 | -1338.87668813 | 0.682592256 | 18.835136 | 12.0814 |

The older group summary uses a more rounded Eh-to-kcal/mol conversion and reports 0.602653369/0.682591740 kcal/mol and 59.6090505/21.5558037/18.8351458%. The independently re-extracted differences above differ by less than 0.000001 kcal/mol; this is conversion precision, not a different calculation or changed target. Both comparisons satisfy the existing ±0.5 kcal/mol rules. The most populated member is source 1-1 within the declared subset.

## Endpoint identity evidence (private, not input targets)

Atom numbers below use the public one-based map. All endpoints share the same graph and stereochemical object; the feature pair distinguishes the final conformers independently of their energies.

| Identity | Torsion 23–21–17–9 / ° | Torsion 45–43–41–39 / ° | Shared 25–23–21–17 / ° | Shared 29–39–41–43 / ° |
|---|---:|---:|---:|---:|
| 1-1 | -54.465135 | 38.229976 | -89.682888 | -179.068861 |
| 1-2 | -54.830119 | -38.409686 | -89.813079 | 178.462386 |
| 1-3 | 60.978513 | 37.383731 | -103.780281 | -178.616718 |

## Exact successful logs

- 1-1: [Opt/Freq](../../../../docs/verification/group_3/paper_9d091f4337662e78/provenance/qzcli_hpc/conf11_hpc20_v2_p3/1/gaussian.log); [matched refined SP](../../../../docs/verification/group_3/paper_9d091f4337662e78/provenance/qzcli_hpc/conf11_refine_6311plusg2dp_hpc20_p3_fallback/1/gaussian.log). Each log contains the actual geometry/atom order; no missing geometry is reconstructed from target energies.
- 1-2: [Opt/Freq](../../../../docs/verification/group_3/paper_9d091f4337662e78/provenance/qzcli_hpc/conf12_hpc20_v2/1/gaussian.log); [matched refined SP](../../../../docs/verification/group_3/paper_9d091f4337662e78/provenance/qzcli_hpc/conf12_refine_6311plusg2dp_hpc20_p3_fallback/1/gaussian.log). Each log contains the actual geometry/atom order; no missing geometry is reconstructed from target energies.
- 1-3: [Opt/Freq](../../../../docs/verification/group_3/paper_9d091f4337662e78/provenance/qzcli_hpc/conf13_hpc20_v2_p3/1/gaussian.log); [matched refined SP](../../../../docs/verification/group_3/paper_9d091f4337662e78/provenance/qzcli_hpc/conf13_refine_6311plusg2dp_hpc20_p3_fallback/1/gaussian.log). Each log contains the actual geometry/atom order; no missing geometry is reconstructed from target energies.

## Qualification and limits

Historical status: the source author-route thermochemical result supports the three-member task under the current contract. The former archive's retry/syntax-retry inventories are not all successful scientific steps and are intentionally absent from this curated chain; their source files remain untouched. This reference is not a requirement to force agents down the same method or initial geometry.

No current-public-starter blind replay is claimed or required for author-route validation; no calculation from those new starters was performed. Complete submissions require three chemically identified, distinct minima; merged/missing/ambiguous members use the partial branch with full-subset populations and most-populated member null. Correctly reporting a failed search does not prove the full scientific objective. The history supports the selected three endpoints, not global exploration of all 16 conformers.
