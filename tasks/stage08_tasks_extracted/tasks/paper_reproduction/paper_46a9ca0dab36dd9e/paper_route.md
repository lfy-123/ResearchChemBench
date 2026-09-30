# Private paper route

## 1. Scientific objective and author claim

The authors use electronic-structure calculations to test whether the photoactive iron chloride species has ligand-to-metal charge-transfer (LMCT) character. Their representative state is excited state 22 of sextet TEAFeCl4; the paper reports that LMCT dominates its IFCT decomposition.

## 2. System and model boundary

The modeled catalyst is the ion pair tetraethylammonium tetrachloroferrate, TEAFeCl4, with a sextet Fe(III) complex. The SI coordinate appendix labels the first catalyst coordinate block Cat1 and separately lists Cl·, pCB, and reaction intermediates. The calculation concerns the isolated catalyst ion pair, not the full reaction mixture.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize catalyst geometry | Cat1 (TEAFeCl4), sextet | Gaussian 16, DFT | B3LYP-D3(BJ); SDD on Fe and 6-31G(d) on other atoms; SMD acetonitrile | Optimized geometry and frequencies | ev_doc_ab5cda8f47f8_000789_818362a654dd |
| 2 | Establish stationary-point quality and thermal terms | optimized structure | Gaussian 16 harmonic frequencies | same level; minima have no imaginary frequencies; frequencies supply thermal corrections at 298.15 K | thermal correction/free-energy terms | ev_doc_ab5cda8f47f8_000789_818362a654dd |
| 3 | Compute excited states | optimized sextet Cat1 | Gaussian 16 TD-DFT | M06-D3/6-311+G(d,p)-SDD(Fe); 30 excited states | excitation energies, wavelengths, oscillator strengths | ev_doc_ab5cda8f47f8_000812_b7e25bf06e8d; ev_doc_ab5cda8f47f8_000820_b944720c4884 |
| 4 | Analyze representative excitation | state 22 TD-DFT density | Multiwfn 3.8 (dev) | hole-electron and IFCT analyses | charge-transfer composition | ev_doc_ab5cda8f47f8_000822_8b495edcc4f1 |

## 4. Validation and analysis protocol

The authors compare spin states and identify sextet TEAFeIIICl4 as the reference ground spin state (Table S5). They inspect the 30 TD-DFT states, select representative strong transitions, and choose state 22 for hole-electron/IFCT analysis because it has the largest oscillator strength among the listed representative states. The SI reports state 22 at 3.27 eV, 379.51 nm, and oscillator strength 0.0340. The hole is mainly ligand-localized and the electron mainly Fe-localized. IFCT assigns 62.4% to LMCT; MLCT is 4.3%, while each of MCCT, LCCT, and LLCT is at most 16.9%.

## 5. Private reference results

State 22 is the selected representative state; the published IFCT LMCT fraction is 62.4% and MLCT is 4.3%. The sextet is the lowest TEAFeIIICl4 spin state; quartet and doublet are reported 46.8 and 89.8 kcal/mol above it. These values are evaluator-only.

## 6. Limitations and interpretation boundaries

IFCT percentages depend on fragment definitions, density/grid settings, geometry, functional, basis, and spin treatment. The source result supports a qualitative assignment and a reported numerical benchmark, not proof that all photoinduced chemistry follows one electronic state. A reproduction may use an independently justified protocol and must disclose deviations.
