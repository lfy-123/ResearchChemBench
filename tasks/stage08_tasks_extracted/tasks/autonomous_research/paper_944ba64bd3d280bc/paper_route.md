# Private paper route

## 1. Scientific objective and author claim

The paper compares the E and Z isomers of 1,2-bis(tetrazol-5-yl)ethylene (H2bte) and argues that photoisomerization changes molecular geometry, packing, electronic potential, noncovalent interactions, and energetic properties. The computational claim tested here is that the isomers have measurably different ESP distributions, NCI interaction patterns, and pi-electron delocalization that are consistent with the reported stability and sensitivity differences.

## 2. System and model boundary

The molecular systems are neutral, closed-shell E-H2bte and Z-H2bte, formula C4H4N8. The molecular calculations use isolated molecules in a methanol continuum; crystal packing and experimental thermal/mechanical measurements are interpretation context, not recomputed outputs. The paper reports E-H2bte as planar and Z-H2bte as non-planar/less regularly packed, while the normalized extraction contains a contradictory phrase about near-planarity; the crystal discussion and figures are the controlling evidence for structural interpretation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain equilibrium molecular geometries | E- and Z-H2bte structures | Gaussian 09 Rev. D.01 | B3LYP-D3BJ/6-311+G**, PCM methanol | Optimized geometries and wavefunctions | ev_doc_80ef999b4c66_000081_b47af8f90c41; ev_doc_80ef999b4c66_000044_31fa3c0f350a |
| 2 | Characterize electronic excitation context | Optimized geometries | TDDFT in Gaussian | PBE1PBE/def2TZVP, SMD methanol; lowest singlets | Excitation energies, wavelengths, oscillator strengths | ev_doc_80ef999b4c66_000081_b47af8f90c41 |
| 3 | Map electrostatic potential and interactions | Optimized wavefunctions | Multiwfn 3.8 and VMD 1.9.2 | ESP surfaces; NCI analysis; LOL-p maps | ESP extrema/maps, NCI and LOL-p visualizations | ev_doc_80ef999b4c66_000044_31fa3c0f350a; ev_doc_7aa6a7e119f1_000215_6324777402a9 |
| 4 | Compare isomers and interpret properties | Outputs from steps 1–3 | Authors' comparative analysis | Compare extrema and mapped interaction/delocalization features | Explanation of stability/sensitivity differences | ev_doc_7aa6a7e119f1_000215_6324777402a9; ev_doc_7aa6a7e119f1_000228_77194ab38f7f |

## 4. Validation and analysis protocol

The authors compare the two isomers under the same analysis settings. They interpret red/blue ESP regions, green pi-stacking and blue hydrogen-bond NCI regions, and continuity of LOL-p isosurfaces. The computed interpretation is compared with the reported experimental density, decomposition onset, impact sensitivity, and friction sensitivity trends. Reproducible validation requires optimized stationary structures, explicit convergence/frequency evidence or a justified alternative, consistent surface definitions, and object-labeled comparison of E and Z.

## 5. Private reference results

The paper reports ESP extrema of E-H2bte from -40.41 to 70.01 kcal mol-1 and Z-H2bte from -46.88 to 79.07 kcal mol-1. It reports extensive intermolecular pi/pi stacking and hydrogen bonding for E, reduced versions of both for Z, and continuous versus discontinuous LOL-p isosurfaces for E versus Z. Table 2 reports decomposition onsets 265.4 versus 220.7 °C, impact sensitivity 22.5 versus 17.5 J, friction sensitivity 252 versus 144 N, and detonation velocity 8725 versus 8313 m s-1 for E versus Z.

## 6. Limitations and interpretation boundaries

ESP extrema and visual NCI/LOL-p comparisons depend on density, surface, grid, isovalue, and geometry choices; the paper does not provide machine-readable NCI scalar tables. The task therefore scores source-backed extrema and qualitative features, while requiring the agent to disclose settings and uncertainty. Molecular calculations alone do not establish crystal sensitivity causality; conclusions must be limited to consistency with the reported experimental trends.
