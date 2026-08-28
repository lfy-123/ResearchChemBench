# Private paper route

## 1. Scientific objective and author claim

Assign the relative configuration of pyrethalkaline A (1), a C30H45N3O3 pentacyclic triamino alkaloid, by comparing calculated and experimental 13C NMR data for two diastereomers. The authors claim that (8S*,9aR*,12aR*)-1a is the supported relative configuration.

## 2. System and model boundary

Neutral singlet pyrethalkaline A; candidates (8S*,9aR*,12aR*)-1a and (8R*,9aR*,12aR*)-1b. Experimental data are 30 carbon shifts in CDCl3. The claim concerns relative, not absolute, configuration.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate conformers | Candidate structures | BALLOON PM3 | Initial geometry search | Conformer ensembles | ev_doc_8e10e4449620_000017_be0dfed71f9a |
| 2 | Optimize and screen | Conformers | Gaussian 09 | M06-2X-D3/def2-SVP and B3LYP/6-31G(d), gas phase | Stable conformers/populations | ev_doc_8e10e4449620_000051_65e3b9804221; ev_doc_8e10e4449620_000055_f29c8eb21701 |
| 3 | Predict shifts | Selected conformers | Gaussian 09 GIAO | mPW1PW91/6-311G(d,p), PCM, unscaled shifts | Calculated 13C shifts | ev_doc_af50a5f28e54_000148_dddab195e9ea |
| 4 | Assign configuration | Calculated and experimental shifts | DP4+ | Carbon-data and all-data variants | Isomer probabilities | ev_doc_8e10e4449620_000004_e99eca734108 |

## 4. Validation and analysis protocol

The authors compare linear-correlation R2 and DP4+ probabilities, with NOESY and crystal data as orthogonal support.

## 5. Private reference results

SI Table S2 reports R2 values 0.9986 and 0.9983 and unscaled carbon DP4+ probabilities 100.00% and 0.00% for the two candidates, respectively.

## 6. Limitations and interpretation boundaries

The calculation tests relative configuration only. Results depend on conformer coverage, optimization, shielding-to-shift treatment, and DP4+ implementation.
