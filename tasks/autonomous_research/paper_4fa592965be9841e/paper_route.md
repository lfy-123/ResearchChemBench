# Private paper route

## 1. Scientific objective and author claim

The paper studies E-3-(thiophen-2-yl)-2-[4-((E)-thiophen-2-ylmethyleneamino)phenyl]acrylonitrile (Compound I, C18H12N2S2). The authors claim that gas-phase DFT reproduces its FT-IR bands and that TD-DFT explains the observed UV-visible absorptions, including substantial intramolecular charge transfer.

## 2. System and model boundary

The computed object is one neutral, singlet molecule, not the crystal lattice or protein complexes. The crystal contains two independent molecules in triclinic P-1; the paper's spectroscopy calculations treat the isolated molecule in the gas phase. The SI reports molecule A as atoms S1–S2, C1–C20, N8/N15 and H1–H20, with formula C18H12N2S2; the E geometries and connectivity are given by the crystallographic tables.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated geometry | Compound I | Gaussian 09 DFT | B3LYP/6-311++G(d,p), gas phase | optimized geometry | ev_doc_c0be135b9d31_000069_29b2a548ae71 |
| 2 | Obtain harmonic IR frequencies | optimized geometry | Gaussian 09 DFT frequency calculation | B3LYP/6-311G(+)(d,p), gas phase | frequencies and assignments | ev_doc_c0be135b9d31_000079_db10094ade15 |
| 3 | Obtain electronic excitations | optimized geometry | Gaussian 09 TD-DFT | TD-DFT; 6-311++G(d,p) stated for the computational study | wavelengths, oscillator strengths, orbital contributions | ev_doc_c0be135b9d31_000083_57c5b52050e9 |
| 4 | Compare IR | calculated and measured bands | tabulation in paper | 3000–500 cm-1 experimental region; raw reported values | band-by-band comparison | ev_doc_c0be135b9d31_000097_4799c4caf111 |
| 5 | Compare UV-visible | calculated and measured bands | tabulation/figure | two reported bands and assignments | wavelength comparison and interpretation | ev_doc_c0be135b9d31_000099_a1cbad7a4bf4 |

## 4. Validation and analysis protocol

The optimized structure should be a genuine stationary point (no imaginary frequencies). The authors compare four diagnostic IR assignments: C-S, C=C, C=N and C-H stretching. They compare two tabulated UV-visible bands, their oscillator strengths, orbital contributions and experimental wavelengths. The paper interprets the lower-energy visible transition as predominantly HOMO to LUMO+1, the higher-energy band as HOMO to LUMO+5 with pi-to-pi-star character, and reports charge-transfer character from frontier-orbital analysis.

## 5. Private reference results

Table 4 reports calculated/experimental IR pairs (cm-1): C-S 859/840, C=C 1545/1551, C=N 1618/1605, and C-H 1450/1450. Table 5 reports calculated/experimental UV bands (nm): 261/262 with oscillator strength 0.211 and H to L+5 contribution, and 409/385 with oscillator strength 1.097 and H to L+1 contribution. The paper states that the calculations show good or clear agreement and significant intramolecular charge transfer.

## 6. Limitations and interpretation boundaries

The source does not report a frequency scaling factor, solvent model, or uncertainty model. Harmonic gas-phase frequencies and vertical TD-DFT excitations are therefore method-dependent proxies for condensed-phase spectra. Charge-transfer language is a qualitative interpretation of orbital character, not a measured charge-transfer number. Agreement should not be generalized to docking, ADMET, biological potency, or a unique global conformer beyond the reported calculation.
