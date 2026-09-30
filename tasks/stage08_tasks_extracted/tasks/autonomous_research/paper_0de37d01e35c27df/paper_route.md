# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT structures of neutral norDTCO and its radical cation to test whether one-electron oxidation produces a sulfur–sulfur two-center/three-electron interaction; the reported shortening of the nonbonded S–S separation is interpreted as structural support for that interaction.

## 2. System and model boundary

The system is gas-phase norDTCO (C12H18S2), in the neutral singlet and radical-cation doublet states. The scored observable is the distance between the two sulfur atoms (SI atom numbers 16 and 17; these are the two S atoms in the supplied Cartesian ordering). The study also discusses the dication, electrochemistry, solvent effects, orbital orientation and alternative chemical fates, but those are outside this benchmark's public calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize neutral norDTCO | X-ray-derived Cartesian structure | Gaussian 16 DFT | unrestricted BP86/TZVP as reported; charge 0, multiplicity 1 | optimized neutral geometry; S–S distance | ev_doc_fd980bebc5ed_000065_fdec778b2423; ev_doc_487ba5831e78_000068_87cbbeac1582 |
| 2 | Optimize norDTCO radical cation | optimized neutral geometry | Gaussian 16 DFT | unrestricted BP86/TZVP; charge +1, multiplicity 2 | optimized radical-cation geometry; S–S distance | ev_doc_fd980bebc5ed_000074_0d3cd827aa28; ev_doc_487ba5831e78_000095_3f203c1146eb |
| 3 | Compare structures | two optimized geometries | coordinate measurement | distance between S1 and S2; Δd = d(neutral) − d(radical cation) | structural change | ev_doc_487ba5831e78_000082_c1b2e1700640; ev_doc_487ba5831e78_000095_3f203c1146eb |

## 4. Validation and analysis protocol

The authors required optimized neutral and radical structures to be stationary points; the paper explicitly notes no imaginary frequencies for the neutral structure. They interpreted a modest S–S contraction on oxidation, retained twist geometry, and sulfur-centered oxidation as consistent with a 2c–3e interaction. They caution that other radical conformations can lie within a few kcal/mol, so the structural interpretation is not an absolute mechanistic proof.

## 5. Private reference results

Table 1 reports d(S–S) = 4.056 Å for neutral norDTCO and 3.983 Å for norDTCO+•, a contraction of 0.073 Å. The paper attributes this contraction to a transannular 2c–3e S–S interaction. The neutral has no imaginary frequencies; the twist conformation is retained in the radical cation.

## 6. Limitations and interpretation boundaries

These are gas-phase DFT structural results, not a complete solution-phase redox free-energy calculation. The contraction is supporting evidence, not by itself a unique proof of bonding. Method dependence, alternative conformers, spin contamination and the absence of explicit solvent should be reported as limitations.
