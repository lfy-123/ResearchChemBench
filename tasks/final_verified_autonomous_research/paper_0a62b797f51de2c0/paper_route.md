# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to relate cyano substitution at the 3/4 positions of thiophene building blocks to molecular electrostatic potential (MESP), dipole moment, and polarization of the resulting edge-activated conjugated polymers. The author claim is that electron-withdrawing cyano groups create electron-rich/electron-deficient sectors at opposite ends, producing a stronger dipole field and directional charge-transfer tendency.

## 2. System and model boundary

The computational objects are the three monomers M-Th-0CN, M-Th-1CN, and M-Th-2CN, and polymer-fragment models L-Th-0CN, L-Th-1CN, and L-Th-2CN containing three repeat units. The monomer identities are 2,5-dibromothiophene, 2,5-dibromo-3-cyanothiophene, and 2,5-dibromo-3,4-dicyanothiophene. Calculations concern neutral closed-shell ground-state electronic structures; no solvent, excited-state, or periodic-solid correction is specified.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize structural-unit geometries | Monomer/polymer-fragment structures | Gaussian 09 | B3LYP/6-311G** | Optimized geometries | ev_doc_6a6661d37024_000123_571920e2cd0b |
| 2 | Obtain dipole moments | Optimized structures | Gaussian 09 | CAM-B3LYP/6-311G** | Dipole moments | ev_doc_6a6661d37024_000123_571920e2cd0b |
| 3 | Construct electrostatic-potential distributions | Optimized structures/wavefunctions | Multiwfn and VMD | ESP/MESP visualization and potential difference | MESP maps and potential differences | ev_doc_6a6661d37024_000123_571920e2cd0b |
| 4 | Interpret polarization and charge separation | MESP, dipoles, orbital maps | Comparison with structural series | Increasing cyano substitution; polymer fragments within three repeat units | Directional polarization interpretation | ev_doc_47250c8470bc_000168_413265c0a85d; ev_doc_47250c8470bc_000109_7388b4d4ed62 |

## 4. Validation and analysis protocol

The paper compares the three substitution levels. It reports polymer-fragment MESP potential differences of 19.86, 45.79, and 50.10 kcal mol−1 for L-Th-0CN, L-Th-1CN, and L-Th-2CN, respectively. The monomer figure (SI Figure S11) displays MESP and dipole moments. The interpretation is that positive potential/charge is concentrated near the thiophene region and negative potential near cyano substituents, with increasing asymmetry and dipole on cyano substitution. The paper additionally interprets L-Th-2CN orbital separation and in-situ XPS shifts as directional S-to-N electron transfer, but those are not required as primary computational observables here.

## 5. Private reference results

Hidden references include the SI Figure S11 monomer dipole/MESP displays and the explicitly reported polymer-fragment MESP differences: 19.86, 45.79, and 50.10 kcal mol−1 for 0CN, 1CN, and 2CN. The source supports the monotonic increase in monomer dipole with cyano count and the positive-thiophene/negative-cyano spatial pattern. Exact graphical monomer values are retained privately because they are image-derived.

## 6. Limitations and interpretation boundaries

The source does not specify coordinates, conformer protocol, numerical convergence thresholds, ESP isosurface/grid settings, or a complete graphical transcription of S11. Independent calculations may therefore differ quantitatively. Evaluation emphasizes identity, reproducibility, validation evidence, the substitution trend, polarity pattern, and honest uncertainty; polymer numerical values are reference checks only when the agent elects to calculate the corresponding three-repeat-unit models.
