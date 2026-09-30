# Private paper route

## 1. Scientific objective and author claim

The paper studies the acid/base-dependent optical switching of phenolic azobenzene-substituted iso-diketopyrrolopyrrole dye 2a.  The computational claim is that distinct protonation states have distinct low-lying singlet absorption profiles and that the acid/base structural assignment explains the observed halochromic response.  The authors report the strongest gas-phase transitions as part of this claim, but those numerical reference values are private to evaluation.

## 2. System and model boundary

The computed systems are the two charged protonation-state structures identified as 2a-acid and 2a-base.  The SI supplies their S0 optimized Cartesian geometries in angstroms.  The acid structure is the doubly protonated phenolic form (+2 formal charge); the base structure is the doubly deprotonated phenolate form (−2 formal charge).  Both are treated as closed-shell singlets.  The benchmark route concerns gas-phase vertical singlet excitations from the supplied S0 geometries; solution cLR-PCM/water calculations and NMR calculations are outside the benchmark endpoint.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish protonation-state structural assignments | 2a and its acid/base forms; experimental pH-dependent 1H NMR | DFT/NMR analysis in Gaussian 16 | CAM-B3LYP/6-31+G(d); GIAO; DMSO PCM for NMR validation | Assigned acid, neutral and base models; shifts near hydroxyl groups | ev_doc_9c2364c83da2_000168_a856c849f802; ev_doc_773e38335bc9_000030_a51650a10a81; ev_doc_773e38335bc9_000031_0b2757a8aeaa |
| 2 | Optimize ground-state geometries | Acid and base molecular structures | DFT in Gaussian 16 | CAM-B3LYP/6-31+G(d), gas phase for the optical models | S0 optimized geometries | ev_doc_9c2364c83da2_000078_6f9dba21d607; ev_doc_773e38335bc9_000030_a51650a10a81; ev_doc_773e38335bc9_000031_0b2757a8aeaa |
| 3 | Compute low-lying optical states | Optimized S0 geometries | TD-DFT in Gaussian 16 | CAM-B3LYP/6-31+G(d), gas phase; first few singlet states | Excitation energies and oscillator strengths | ev_doc_9c2364c83da2_000078_6f9dba21d607; ev_doc_9c2364c83da2_000176_f5c3b699cb77 |
| 4 | Interpret the switching origin | Bright-state orbitals and spectra | Kohn-Sham orbital analysis and spectral comparison | Bright transitions assigned to azobenzene/iso-DPP electronic system | Qualitative π–π* / charge-transfer interpretation and acid/base spectral separation | ev_doc_9c2364c83da2_000188_9d48ec63966d; ev_doc_773e38335bc9_000026_26db6ed43afb |

## 4. Validation and analysis protocol

The paper compares the first few singlet transitions for both structures and identifies the brightest transition by oscillator strength.  It uses NMR calculations to validate protonation-state assignments, then compares gas-phase TD-DFT spectra; additional water cLR-PCM calculations and B3LYP calculations are qualitative cross-checks.  The reported experimental context is a pH-dependent chromatic shift for 2a and reversible acid/base sensor response.

## 5. Private reference results

Table 3 reports gas-phase CAM-B3LYP/6-31+G(d) values for S1–S4 of each structure.  The brightest acid transition is S3 and the brightest base transition is S1; the exact energies and oscillator strengths, including the reported bathochromic ordering, are hidden evaluator references.  The table rows are source-backed by ev_doc_9c2364c83da2_000176_f5c3b699cb77 and the accompanying narrative by ev_doc_9c2364c83da2_000181_718e8e3894c0 and ev_doc_9c2364c83da2_000184_b4403fdf8f65.

## 6. Limitations and interpretation boundaries

The gas-phase benchmark does not reproduce aqueous solvent shifts, NMR chemical shifts, vibronic envelopes, experimental band maxima, or sensor fabrication.  Excitation energies and oscillator strengths are method- and geometry-dependent.  A submitted calculation may use an independent defensible protocol, but it must state the electronic-state assignment, geometry treatment, number/state-selection rule, convergence evidence, and limitations.  The benchmark scores source-supported state observables and the qualitative optical-switching conclusion, not an unreported mechanistic detail.
