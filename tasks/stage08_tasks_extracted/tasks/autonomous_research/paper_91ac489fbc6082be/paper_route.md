# Private paper route

## 1. Scientific objective and author claim

Assign the absolute configuration of runakamala B (compound 2) by quantitative comparison of experimental and calculated VCD spectra. The authors claim the R assignment is supported.

## 2. System and model boundary

Neutral closed-shell compound 2; isolated-molecule vibrational calculation with benzene continuum; experimental VCD window 2200–850 cm-1, with a solvent-absorption gap near 1330 cm-1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Conformer generation | Compound 2 | Spartan 20 MMFF search | 55 geometries within 2.3 kcal/mol | candidate geometries | ev_doc_089a48ea8c0a_000736_8a86f780549c |
| 2 | Optimization/selection | candidate geometries | Gaussian 16 M06-2X with PCM benzene | eight stable conformers within 1.0 kcal/mol | optimized conformers | ev_doc_089a48ea8c0a_000736_8a86f780549c |
| 3 | VCD calculation | optimized conformers | Gaussian 16 | frequencies, dipole and rotational strengths | spectra | ev_doc_089a48ea8c0a_000737_9256b3b793c6 |
| 4 | Ensemble comparison | spectra and energies | GaussView 6 | 298 K Boltzmann weights, scale 0.99, half-width 12 cm-1 | weighted VCD and similarity | ev_doc_089a48ea8c0a_000738_3e1f8f10920c |

## 4. Validation and analysis protocol

Compare both enantiomeric assignments with observed VCD using the Debie et al. similarity procedure; assess aggregation as a limitation using concentration-dependent spectra.

## 5. Private reference results

SI Table S3: R similarity 49.4; S similarity 13.9; enantiomer similarity index 35.5; confidence level 73.

## 6. Limitations and interpretation boundaries

Aggregation can change vibrational spectra; agreement supports an assignment within the computational/measurement boundary and is not proof that aggregation is absent.
