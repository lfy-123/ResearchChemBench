# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to support the UV–Vis interpretation of complex 1, the cationic silver(I) species [Ag(N-Mephtz)4]+ (N-Mephtz = N-methylphenothiazine). The author claim is that TD-DFT spectra provide two prominent calculated absorption bands and that the experimental feature near 310 nm can be understood from several occupied-to-virtual transitions with ligand-to-silver character.

## 2. System and model boundary

Complex 1 is the monocation [Ag(N-Mephtz)4]+ with four sulfur-bound N-methylphenothiazine ligands; triflate and one-third hydrate belong to the isolated salt but are not part of the modeled cation. The cation is closed-shell Ag(I), charge +1 and singlet. The paper discusses gas-phase optimized geometries and a DMSO continuum for the UV–Vis calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize molecular geometry | [Ag(N-Mephtz)4]+ | DFT in Gaussian 09 | B3LYP/LANL2DZ and M06/LANL2DZ; gas phase | optimized structures | ev_doc_8040742dc4b6_000598_21a41a4d524f |
| 2 | Verify stationary point | each optimized structure | harmonic vibrational analysis | no imaginary frequencies | local-minimum check | ev_doc_8040742dc4b6_000598_21a41a4d524f |
| 3 | Simulate UV–Vis absorption | optimized geometry | TD-DFT | SMD solvent model, DMSO; retain/contribute peaks with oscillator strength f > 0.05 | excitation wavelengths/intensities | ev_doc_8040742dc4b6_000598_21a41a4d524f; ev_doc_8040742dc4b6_000600_6b8fe6ac7dfe |
| 4 | Interpret the band | excited-state output and Kohn–Sham orbitals | orbital visualization/analysis | inspect the transitions contributing to the prominent feature | transition assignments and ligand/Ag character | ev_doc_8040742dc4b6_000137_77cd0a04c879; ev_doc_24bd28ca2fc1_000054_98c068dbef52 |

## 4. Validation and analysis protocol

The authors compared simulated and experimental spectra. They state that optimized structures had no imaginary frequencies. For UV–Vis, they selected peaks using oscillator strength and reported the prominent calculated bands. Their orbital analysis used Kohn–Sham orbitals (SI Fig. S12) to relate the experimental band near 310 nm to HOMO−1 → LUMO, HOMO−2 → LUMO, and HOMO−2 → LUMO+1, with ligand-to-Ag character.

## 5. Private reference results

At M06, the two reported major calculated absorption wavelengths are 319 nm and 288 nm. At B3LYP they are 319 nm and 284 nm. The paper states these are red-shifted by about 20–30 nm relative to the experimental spectrum. The cited orbital assignment for the experimental band near 310 nm is HOMO−1 → LUMO, HOMO−2 → LUMO, and HOMO−2 → LUMO+1, primarily ligand-to-silver(I) in character.

## 6. Limitations and interpretation boundaries

The reported values are method- and geometry-dependent TD-DFT results, not experimental constants. A reproduction may use a different implementation and must report method, solvent, geometry provenance, state-selection rule, and convergence evidence. Orbital labels are not invariant across software or geometry; transition assignments should therefore be tied to the submitted orbital/state analysis rather than treated as unique observables. The paper's public deposition is CCDC 2483173, but this package does not depend on an external coordinate download.
