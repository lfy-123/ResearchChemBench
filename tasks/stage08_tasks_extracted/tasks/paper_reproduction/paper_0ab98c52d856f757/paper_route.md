# Private paper route

## 1. Scientific objective and author claim

The paper explains visible-light formation of the 3,9-diazatetraasterane dimer 2a from 1a. The authors' preferred qualitative route is sequential triplet-sensitized/intermolecular then intramolecular [2+2] cycloaddition (Path A): triplet 1a attacks ground-state 1a, a biradical is formed, spin inversion occurs at MECP1-A, and subsequent re-excitation/cyclization gives 2a. The rate-determining spin-inversion step is reported as kinetically accessible.

## 2. System and model boundary

The computational system is the neutral closed-shell 1,4-dihydropyridine 1a dimer and its S0/T1 crossing reached after the first intermolecular bond-forming event. Energies are relative Gibbs free energies at 298.15 K and 1 atm in a THF:MeOH 1:3 continuum; the measured target is the MECP1-A barrier relative to the reactant reference used for Path A.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points and obtain frequencies | 1a, intermediates, TSs | Gaussian 16; B3LYP-D3/6-31G(d,p) | PCM THF:MeOH=1:3; 298.15 K, 1 atm corrections | optimized structures, frequencies, thermal corrections | ev_doc_707001aa2ceb_000174_282820e3f66b; ev_doc_707001aa2ceb_000210_b53d0219845a |
| 2 | Classify minima/TSs | optimized structures | frequency analysis at same level | minima: 0 imaginary; TS: 1 imaginary | stationary-point validation | ev_doc_707001aa2ceb_000210_b53d0219845a |
| 3 | Refine electronic energies | optimized structures | M06-2X-D3/def2-TZVP single points | PCM THF:MeOH=1:3 | higher-level energies | ev_doc_707001aa2ceb_000174_282820e3f66b; ev_doc_707001aa2ceb_000214_1720c5993282 |
| 4 | Locate spin crossing | IM1-A-like S0/T1 dimer | modified MECP program | S0/T1 crossing search | MECP1-A structure and energy | ev_doc_707001aa2ceb_000208_4296aa5b83b3; ev_doc_707001aa2ceb_000174_282820e3f66b |
| 5 | Build energy profile | validated stationary points and MECP | relative Gibbs-energy assembly | MECP free energy defined as electron-energy difference from minimum plus minimum free energy | Path-A barrier | ev_doc_e93528a20fc6_000280_4ee893c5d2c1 |

## 4. Validation and analysis protocol

The SI reports frequency-based classification of minima and transition states, thermodynamic corrections at 298.15 K/1 atm, and a modified-MECP analysis between T1 and S0. The paper compares the resulting energy profile with competing paths and identifies the largest/ rate-determining step for Path A. Structural connectivity, spin multiplicity, crossing character, and energy-reference consistency are required for interpretation.

## 5. Private reference results

The paper reports 3.8 kcal/mol for TS1-A, 5.2 kcal/mol for the MECP1-A spin-inversion step, 2.4 kcal/mol for IM3-A formation, and 4.7 kcal/mol for MECP2-A. It identifies the 5.2 kcal/mol spin inversion as rate-determining for formation of 2a. These values and conclusions are evaluator-only.

## 6. Limitations and interpretation boundaries

The benchmark evaluates reproduction of the published computational claim, not experimental rate prediction or proof of a unique photophysical mechanism. MECP energies depend on electronic-structure model, conformer coverage, solvent treatment, and the chosen energy reference. A calculation that fails to locate a crossing must report the failure and diagnostics rather than fabricate a barrier.
