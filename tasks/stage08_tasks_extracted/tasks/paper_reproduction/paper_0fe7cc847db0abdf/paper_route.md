# Private paper route

## 1. Scientific objective and author claim

The paper asks whether the three cationic half-sandwich Ir(III) complexes Ir1–Ir3 have excited-state energetics compatible with sensitization of triplet oxygen to singlet oxygen. The authors claim that their computed adiabatic S0–T1 gaps exceed 0.98 eV, supporting a type-II photodynamic pathway.

## 2. System and model boundary

Ir1 is [(Cp*)Ir(phen)Cl]+, Ir2 is [(Cp*)Ir(5-nitro-1,10-phenanthroline)Cl]+, and Ir3 is [(Cp*)Ir(5-amino-1,10-phenanthroline)Cl]+. The PF6− counterion is omitted; the modeled species is the +1 cation. The SI supplies optimized Cartesian geometries for all three complexes.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize S0 geometry | Ir1–Ir3 cation geometries | Gaussian 16 A.03, DFT | B3LYP; LANL2DZ/LANL2 ECP for Ir; 6-31G** for H,C,N,O,Cl; CPCM water; singlet, charge +1 | optimized S0 | ev_doc_3575d3e99a62_000191_89ef326d5856; ev_doc_c7825c5f1b18_000082_fb58516badc8 |
| 2 | Verify minima | optimized S0 | Gaussian frequency calculation | same level; no imaginary frequencies | vibrational validation | ev_doc_c7825c5f1b18_000093_0ad51b8d2233; ev_doc_c7825c5f1b18_000101_3f996a80be1e |
| 3 | Obtain singlet excitation | S0 geometry | TD-DFT | CPCM water; lowest singlet excitation | S1 energy | ev_doc_c7825c5f1b18_000095_0b7176d946ee; ev_doc_c7825c5f1b18_000097_dc402fda59a8 |
| 4 | Obtain triplet state | S0 geometry | unrestricted DFT | charge +1, multiplicity 3; same basis/model | T1 energy and optimized T1 minimum | ev_doc_c7825c5f1b18_000095_0b7176d946ee; ev_doc_c7825c5f1b18_000097_dc402fda59a8 |
| 5 | Compare states | S0/T1 and reported state energies | energy analysis | adiabatic S0–T1 gap; compare to oxygen sensitization threshold | gaps for Ir1–Ir3 | ev_doc_3575d3e99a62_000215_0a0f6bf4c071; ev_doc_3575d3e99a62_000220_9157011cc375 |

## 4. Validation and analysis protocol

The authors checked optimized S0 and T1 structures as local minima and compared optimized structures qualitatively with the crystal structure. They interpreted a gap above 0.98 eV as energetically sufficient for singlet-oxygen generation and related that result to DPBF photochemical evidence.

## 5. Private reference results

The reported S0–T1 gaps, in Ir1/Ir2/Ir3 order, are 2.50, 2.15, and 2.26 eV. The authors state that all exceed 0.98 eV. The paper additionally reports that all three generate singlet oxygen, with quantum yields in the 0.11–0.14 range, and that Ir2 has the strongest overall antibacterial performance.

## 6. Limitations and interpretation boundaries

The paper does not provide complete input/output files or a numerical uncertainty analysis. The public task therefore scores the source-reported gaps and defensible validation/reporting, while allowing method-dependent deviations and requiring their disclosure. The gap criterion supports energetic plausibility; it does not by itself prove a complete photochemical mechanism or biological efficacy.
