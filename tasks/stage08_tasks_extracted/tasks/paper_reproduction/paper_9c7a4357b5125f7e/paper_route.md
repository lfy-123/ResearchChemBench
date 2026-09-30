# Private paper route

## 1. Scientific objective and author claim

The paper analyzes the first acylation/nucleophilic-substitution step used to generate carbon suboxide from malonic acid (MA) and acetic anhydride (Ac2O) at 140 °C. The authors claim that the uncatalyzed MA/Ac2O sequence proceeds through two six-membered-ring transition states and that acylation is rate-determining for C3O2 generation. The first reported free-energy barrier is the key quantitative reference for this task.

## 2. System and model boundary

The modeled reactants are neutral malonic acid and neutral acetic anhydride in an Ac2O continuum solvent at 140 °C (413.15 K), singlet electronic state. The scored state is the first transition state relative to the separated/associated reactant reference used by the investigator. DMAP is outside the scored uncatalyzed route.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize reactant and transition-state structures | MA/Ac2O reaction path | Gaussian 16 | M06-2X-D3/6-311+G(d,p), PCM(Ac2O), 140 °C | optimized geometries and frequencies | ev_doc_e9be935daee0_000080_06af82ea6981; ev_doc_e9be935daee0_000081_d38a7d04d1b9; ev_doc_e9be935daee0_000245_025b3a473c73 |
| 2 | Refine electronic energies | optimized structures | Gaussian 16 | M06-2X-D3/def2-QZVPPD, SMD(Ac2O) | single-point energies | ev_doc_e9be935daee0_000082_b8b1c75e299b; ev_doc_e9be935daee0_000083_fbe61ad0a23f |
| 3 | Assemble thermal free energies | frequency and single-point outputs | Shermo/post-processing | temperature-dependent Gibbs energies | ΔG‡ values and TST quantities | ev_doc_e9be935daee0_000084_1221b068f430; ev_doc_f684accfbd42_000064_1a150b15b4b7 |
| 4 | Validate reaction paths | each optimized TS | IRC calculation | reactant/product-side connectivity check | validated reaction path | ev_doc_e9be935daee0_000085_f00da0c97d4a; ev_doc_e9be935daee0_000065_7b904efcddf5 |

## 4. Validation and analysis protocol

The authors use frequency calculations to characterize stationary points and IRC calculations to verify each reaction path. The SI states that the first two nucleophilic-substitution steps have barriers of 152.4 and 158.6 kJ mol−1 and corresponding TST rates of 4.92 × 10−7 and 8.29 × 10−8 s−1 M−1. The first barrier is interpreted together with the second step and the faster HAc-removal sequence to identify acylation as rate-determining.

## 5. Private reference results

For the first MA + Ac2O substitution step, ΔG‡ = 152.4 kJ mol−1. The paper reports that the path belongs to a two-step sequence with six-membered-ring TSs; the all-path IRC validation is part of the computational protocol. These values and interpretations are evaluator-only.

## 6. Limitations and interpretation boundaries

The supplied SI text contains figure/table descriptions but no machine-readable Cartesian coordinate appendix. Consequently, the released task uses canonical molecular identities and requires the investigator to generate and validate geometries. Agreement is interpreted within the stated model/system boundary; conformer, standard-state, thermal-correction and numerical-method sensitivity must be reported as limitations rather than silently treated as author-equivalent.
