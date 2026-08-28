# Private paper route

## 1. Scientific objective and author claim

The paper tests how sequential hydration changes the structure of neutral open-shell BaOH(H2O)n clusters (n=1–5), and claims that the Ba–OH contact-ion-pair (CIP) arrangement persists for n=1–2 but begins a solvent-shared-ion-pair (SIP) separation at n=3. The structural assignment is supported by stationary-point calculations, harmonic IR spectra, charge/interaction analysis, and finite-temperature dynamics.

## 2. System and model boundary

Neutral BaOH(H2O)n clusters, n=1,2,3,4,5, in the lowest doublet electronic state (charge 0, multiplicity 2). The BaOH oxygen is O(1); water oxygens are O(2) onward in the authors' discussion. Structural observables include the Ba···O(1) separation, water coordination and hydrogen-bond topology; spectroscopic observables are OH-stretching and related harmonic frequencies. The paper also discusses a 3B→3A rearrangement and AIMD of 3A.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate/relax low-lying cluster structures | BaOH(H2O)n, n=1–5 | Gaussian 16 | MP2(full), aug-cc-pVTZ on O,H and def2-TZVPP on Ba; neutral doublet | optimized stationary points | ev_doc_448fba39c103_000053_c7e9131ea867; ev_doc_d6b0f05409fa_000025_ebd8503e2a06; ev_doc_d6b0f05409fa_000026_d8a4627d2150 |
| 2 | Verify minima/transition states | optimized structures | Gaussian 16 harmonic frequencies; Berny/IRC for TSs | no imaginary frequencies for minima; IRC connectivity for TSs; ZPE included in relative energies | validated minima/TSs and relative energies | ev_doc_d6b0f05409fa_000026_d8a4627d2150; ev_doc_d6b0f05409fa_000027_0b32b1890a28 |
| 3 | Compare harmonic spectra with experiment | validated structures | Gaussian 16 | frequencies scaled by 0.951; 10 cm−1 FWHM Gaussian broadening | assigned bands and spectral comparison | ev_doc_448fba39c103_000084_c9b40a298a84; ev_doc_d6b0f05409fa_000027_0b32b1890a28 |
| 4 | Analyze interaction/charge evolution | nA structures | sobEDA/TPSSh-D3(BJ)/SDD&6-311G* and Mulliken analysis | Ba···O(1)H fragment interaction components | charges, distances, EDA trends | ev_doc_448fba39c103_000084_c9b40a298a84; ev_doc_d6b0f05409fa_000253_11077c3a1423 |
| 5 | Include anharmonic/thermal effects | selected optimized structures | CP2K AIMD | BLYP-D3, GPW 450 Ry, 15 Å box, 0.5 fs step, 5 ps equilibration, 150 ps production, 50–200 K | DTCF IR spectra and distance distributions | ev_doc_d6b0f05409fa_000117_f45fedc599c6; ev_doc_448fba39c103_000303_a81f3025dd01 |

## 4. Validation and analysis protocol

The authors compare calculated OH bands to the experimental assignments in Table 1 and SI Tables S1–S2, inspect the Ba···O(1)H distance and Mulliken charges (SI Table S3), and interpret the sobEDA components (SI Table S4). For n=3 they compare the dissociated and nondissociated structures and analyze a reaction path/IRC. AIMD spectra and distance distributions are used as a finite-temperature robustness check, with the authors explicitly noting that the AIMD model omits explicit zero-point and quantum nuclear effects and does not fully reproduce experiment.

## 5. Private reference results

Source-backed references include: calculated band a for the O(1)H group shifts from about 3735 cm−1 (n=1) to 3712 (n=2) and 3703–3701 (n=3–5); band c shifts from 2962 (n=1) and 2868 (n=2) to 2506 cm−1 (n=3), then splits at n=4–5; Ba···O(1)H distances for 1A–5A are 2.331, 2.515, 3.311, 3.172 and 3.103 Å; the n=3 dissociated structure is 1.69 kcal/mol below 3B and the reported 3B→3A barrier is 2.69 kcal/mol; the solvent-shell charge becomes more negative through n=3 and the O(1)H charge is −0.77, −0.66 and −0.55 for n=1–3. Full reference values and mappings remain evaluator-private.

## 6. Limitations and interpretation boundaries

The source reports harmonic spectra, finite-temperature AIMD spectra, and qualitative structural assignments; these are model-dependent and not a direct bulk-solution free-energy surface. Mulliken and sobEDA quantities are method-dependent descriptors, and AIMD temperature is not identical to the laser-source experiment. The benchmark therefore scores reproducible structural/spectral evidence and appropriately qualified conclusions, not an unsupported claim of universal solution-phase behavior.
