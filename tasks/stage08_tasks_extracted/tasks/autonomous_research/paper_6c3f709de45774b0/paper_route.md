# Private paper route

## 1. Scientific objective and author claim

The paper assigns the relative configuration of citrinin analogue 10, 4-hydroxy-6-(3-hydroxybutan-2-yl)-3,5-dimethyl-2H-pyran-2-one. The authors first establish the constitution and the 7R assignment from spectroscopy and optical rotation, then compare calculated NMR data for the two remaining diastereomers, (7R,8R)-10 and (7R,8S)-10, and use DP4+; an ECD calculation is reported as additional confirmation. The author claim is that the 7R,8S relative configuration is supported.

## 2. System and model boundary

Neutral closed-shell C11H16O4 compound 10 in the reported protonation state. The scored computational object is the comparison of the two explicitly defined diastereomeric graphs/configurations at C7 and C8 against experimental 13C and 1H NMR data measured in DMSO-d6. Conformers, geometries, shielding tensors, Boltzmann populations and DP4+ post-processing are computational intermediates, not public inputs.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate and optimize conformers | Both diastereomers of 10 | Gaussian 09; PM6, then HF/6-31G(d), then B3LYP/6-31G(d) | 7 kcal/mol energy window; maximum 100; RMSD cutoff 0.2 Å; duplicate removal; harmonic frequencies for stability | Stable optimized conformers | ev_doc_44d6cf47f28f_000200_5f1c40b08907; ev_doc_44d6cf47f28f_000206_2796541e2eb9; ev_doc_ab62f38ef3b8_000205_5e18f97fa9ef; ev_doc_ab62f38ef3b8_000206_006af5a5029f |
| 2 | Predict NMR shifts | Stable conformers | Gaussian 09 GIAO MPW1PW91/6-311+G(2d,p), IEFPCM DMSO | TMS correction; Boltzmann averaging | Averaged 13C/1H shifts for each diastereomer | ev_doc_44d6cf47f28f_000206_2796541e2eb9; ev_doc_44d6cf47f28f_000280_516cf891ad29; ev_doc_ab62f38ef3b8_000207_eef9e6e9d814; ev_doc_ab62f38ef3b8_000208_292e0e4952d0 |
| 3 | Assign configuration statistically | Experimental and calculated shifts | DP4+ Excel template/post-processing | mPW1PW91; 6-311+G(d,p); IEFPCM; carbon, proton and combined data | DP4+ probabilities and R2, CMAD, LAD, RMSD | ev_doc_44d6cf47f28f_000220_bacc27842618; ev_doc_44d6cf47f28f_000283_f223f75e7062; ev_doc_44d6cf47f28f_000284_9f844449fca8; ev_doc_44d6cf47f28f_000285_37cc96675fd1; ev_doc_ab62f38ef3b8_000209_3caee1853bbc |
| 4 | Independent confirmation | Optimized conformers | TDDFT B3LYP/6-311G(d,p), IEFPCM MeOH | Gaussian 09; ECD curves with sigma 0.3 eV and 10 nm UV shift | Calculated ECD comparison | ev_doc_44d6cf47f28f_000200_5f1c40b08907; ev_doc_44d6cf47f28f_000206_2796541e2eb9 |

## 4. Validation and analysis protocol

The authors accept conformers inside the stated energy/RMSD limits, remove optimized duplicates, verify minima by frequencies, Boltzmann-average NMR shifts, regress calculated against experimental shifts, and apply DP4+ to the two candidates. The configuration assignment is interpreted jointly with the reported spectroscopic/optical-rotation boundary and the ECD comparison.

## 5. Private reference results

The SI reports DP4+ combined-data probabilities of 9.55% for isomer 1 and 90.45% for isomer 2. The paper reports for the favored configuration R2=0.9985 (13C) and 0.9915 (1H), CMAD=1.74 and 0.08 ppm, LAD=4.68 and 0.15 ppm, and RMSD=2.60 and 0.10 ppm, respectively; the paper text states that the DP4+ analysis gives 100% probability for 10b in its reported analysis. These values are hidden evaluator references.

## 6. Limitations and interpretation boundaries

The benchmark evaluates reproducibility of the NMR/DP4+ evidence, not a universal truth claim about stereochemistry. Results can depend on conformer coverage, geometry method, solvent treatment, shielding convention, atom assignment and DP4+ implementation. ECD and optical rotation are contextual validation, and should not be treated as interchangeable numeric targets unless independently computed and documented.
