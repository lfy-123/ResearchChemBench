# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical vibrational calculations to validate superlet-transform assignments of low-frequency Rhodamine 101 vibrations in methanol for the ground state S0 and first singlet excited state S1. The authors claim close agreement between calculated and SLT frequencies and use the assignments to interpret vibrational energy redistribution.

## 2. System and model boundary

Rhodamine 101, C32H30N2O3, neutral singlet, in methanol represented by an SMD continuum. The calculated observables are harmonic vibrational frequencies below 125 cm−1 for optimized S0 and S1 structures; experimental comparison is to the Table 1 mode list, with missing experimental entries retained as missing.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structure | SI S0 coordinates | Gaussian 16 DFT | B3LYP/aug-cc-pVDZ, Grimme D3 with Becke–Johnson damping, SMD methanol, charge 0, multiplicity 1 | S0 optimized geometry | ev_doc_cf03f6a65a59_000145_58cc334ae615; ev_doc_6d7fadd76fad_000005_4875bb836ad8 |
| 2 | Optimize first excited-state structure | SI S1 coordinates | Gaussian 16 TD-DFT | first singlet excited state with the same functional/basis, D3(BJ), SMD methanol | S1 optimized geometry | ev_doc_cf03f6a65a59_000145_58cc334ae615; ev_doc_6d7fadd76fad_000012_ff481dd8ea3c |
| 3 | Obtain harmonic frequencies | optimized S0/S1 geometries | Gaussian 16 | harmonic frequency calculation in the corresponding state/solvent model | unscaled frequencies | ev_doc_cf03f6a65a59_000145_58cc334ae615 |
| 4 | Correct harmonic frequencies | unscaled frequencies | post-processing | multiply by 0.9670 | scaled frequencies | ev_doc_cf03f6a65a59_000145_58cc334ae615 |
| 5 | Compare and assign modes | scaled frequencies and SLT values | tabulation/analysis | compare modes in 0–125 cm−1 | Table 1 comparison and assignments | ev_doc_cf03f6a65a59_000235_8f2bf02a2177; ev_doc_cf03f6a65a59_000266_0c5117ec02e5 |

## 4. Validation and analysis protocol

The optimized structures were treated as minima/state-specific stationary structures, and calculated low-frequency modes were compared mode-by-mode with SLT peaks. The paper reports that the maximum calculated–experimental deviation is below 3 cm−1. It notes a SLT peak near 107 cm−1 without a corresponding calculated mode, plausibly due to coupling, and interprets xanthene-associated modes as redshifting and carboxyphenyl-associated modes as blueshifting from S0 to S1. The S0 ν13 and S1 ν8 modes are described as prominent hot modes.

## 5. Private reference results

Table 1 reports (calculated, experimental; cm−1): mode 1 S0 (20.9,18.7), S1 (22.9,21.9); 2 (28.0,25.0), (26.8,26.2); 3 (30.3,30.7), (31.1,31.3); 4 (38.6,40.0), (42.1,39.7); 5 (47.5,46.3), (51.3,51.1); 6 (57.7,60.7), (65.3,65.2); 7 (69.6, missing), (68.5,69.5); 8 (74.2,77.3), (74.2,75.7); 9 (85.7,85.8), (82.0,81.4); 10 (91.5,92.8), (87.7,86.6); 11 (99.3,98.0), (93.3,90.4); 12 (117.1, missing), (117.9,117.7); 13 (120.2,120.1), (123.1,122.9). Assignments and qualitative conclusions are taken from Table 1 and Section 4.3.

## 6. Limitations and interpretation boundaries

These are harmonic, continuum-solvent calculations and not direct experimental frequency measurements. Low-frequency modes can mix structural motions; the tentative assignments are not unique normal-mode labels. The 107 cm−1 SLT feature is not treated as a required calculated mode. The task evaluates reproducible observables and validation reasoning, not exact software identity.
