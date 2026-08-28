# Private paper route

## 1. Scientific objective and author claim

The paper studies base-promoted C3-cyanoalkylation of oxindoles with substituted acrylonitriles without external light. Its mechanistic claim is that an oxindole enolate and cinnamonitrile form an electron-donor–acceptor (EDA) complex; inner-sphere electron transfer gives radical species and enables the observed C3-cyanoalkylation. The computationally testable central result is the Gibbs free-energy separation between the singlet ground state and triplet state of the anionic EDA complex [L1_L2]. The authors report 23.5 kcal/mol and interpret this as compatible with thermal excitation at room temperature. They additionally assign charge transfer from the oxindole enolate donor to cinnamonitrile in the excited state.

## 2. System and model boundary

L1 is the oxindole-enolate donor geometry supplied in the SI; L2 is cinnamonitrile; the evaluated object is their anionic 72-atom EDA complex, not isolated fragments. The two states are the singlet ground state (charge −1, multiplicity 1) and the triplet excited state (charge −1, multiplicity 3). The reported observable is the difference in Gibbs free energies, in kcal/mol, between separately optimized states. The source also reports a hole–electron analysis for the triplet state.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize and characterize the singlet EDA complex | SI Cartesian coordinates labeled L-1_L2; charge −1, singlet | Gaussian 16 Rev. C.01, DFT | B3LYP-GD3(BJ)/6-31+G(d,p); PCM acetonitrile when solvent effect applicable; frequency at same level | Stable singlet geometry and thermochemistry; all vibrational modes positive | ev_doc_13913a3a16a0_000499_06b60ddb1b0a; ev_doc_13913a3a16a0_000501_92e91b4df1c3; ev_doc_13913a3a16a0_000502_d011f1297eda; ev_doc_13913a3a16a0_000503_2e50abb4b6eb; ev_doc_13913a3a16a0_000504_ebf2a9b8d90e |
| 2 | Optimize and characterize the triplet EDA complex | SI Cartesian coordinates labeled L-1_L2_T1; charge −1, triplet | Gaussian 16 Rev. C.01, DFT | Same functional/basis, PCM acetonitrile, same-level frequency analysis | Stable triplet geometry and thermochemistry; all vibrational modes positive | ev_doc_13913a3a16a0_000499_06b60ddb1b0a; ev_doc_13913a3a16a0_000501_92e91b4df1c3; ev_doc_13913a3a16a0_000502_d011f1297eda; ev_doc_13913a3a16a0_000503_2e50abb4b6eb; ev_doc_13913a3a16a0_000504_ebf2a9b8d90e |
| 3 | Compare state free energies | Thermochemistry from Steps 1–2 | Post-processing of Gaussian Gibbs free energies | Convert Hartree difference to kcal/mol | ΔG(triplet − singlet) | ev_doc_13913a3a16a0_000508_71810e0cc05c; ev_doc_74e133a006f0_000043_ba94e9112784 |
| 4 | Characterize excited-state charge transfer | Triplet electronic structure | Multiwfn 3.8 (dev) hole–electron analysis | Excited-state donor/acceptor localization | Hole on oxindole-enolate donor and electron on cinnamonitrile acceptor | ev_doc_13913a3a16a0_000677_9a2d4c1fc1d0; ev_doc_13913a3a16a0_000678_0e9df4b7a2f5 |

## 4. Validation and analysis protocol

The authors used same-level frequency analyses to verify stable stationary structures and state that all vibrational modes are positive. The state comparison uses Gibbs free energies, not bare electronic energies. The excited-state interpretation is supported by hole–electron analysis, and the computational result is discussed together with the paper's EPR, radical-trapping, and UV–visible observations. The SI supplies optimized coordinate and thermodynamic blocks for L1, L2, the singlet complex, and the triplet complex.

## 5. Private reference results

For the singlet complex, the SI gives Sum of electronic and thermal Free Energies = −879.702923 Hartree. For the triplet complex, the SI gives thermal corrections and optimized coordinates but does not print a Gibbs-free-energy sum in the extracted block; Figure S4/main text reports the resulting singlet–triplet Gibbs free-energy gap as 23.5 kcal/mol. The paper states that the excited state shows charge transfer from oxindole enolate to cinnamonitrile. These are hidden evaluator references, not public task inputs.

## 6. Limitations and interpretation boundaries

The benchmark evaluates reproduction of the reported state gap and qualitative charge-transfer assignment, not proof that thermal excitation is kinetically sufficient, a complete reaction mechanism, or uniqueness of the EDA geometry. DFT functional, basis, solvation, conformer choice, thermal convention, and treatment of an open-shell state can shift the computed value. A calculation that fails to obtain a stable stationary point must be reported as such with diagnostics rather than silently converted into a successful gap.
