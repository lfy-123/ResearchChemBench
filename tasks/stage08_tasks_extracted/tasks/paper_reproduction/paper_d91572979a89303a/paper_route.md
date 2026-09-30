# Private paper route

## 1. Scientific objective and author claim

The paper studies metal-free thioaromatization of N-(4-bromophenyl)-S-phenyl sulfenamide (1a) with [1.1.1]propellane (2), catalysed by thioxanthone (TXT), to form sulfur-substituted methylenecyclobutane 3a. The authors claim a sulfur-ylide formation, [2,3]-Wittig rearrangement, TXT-assisted Alder-type aromatization, and deamination; the deamination barrier is identified as rate limiting.

## 2. System and model boundary

The model system is 1a + 2 + TXT in the gas-phase optimisation/thermal-correction and toluene continuum-solvent energetic refinement. Species discussed in the calculated cycle are 1a, 2a, TS1A, INT1A, TS2A, INT2A, TXT, TS3A-TXT, INT3A-TXT, TS4A-TXT, TS3B (uncatalysed comparison), and 3a. The reported product is 4-bromo-2-(3-methylene-1-(phenylthio)cyclobutyl)aniline.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimise stationary points | Starting geometries for intermediates and TSs | Gaussian 09, DFT | ωB97X-D3(BJ)/def2-SVP, gas phase | Optimised geometries | ev_doc_5c9d1cfdb571_000428_c65b83cbeac9 |
| 2 | Establish stationary-point nature and thermal terms | Optimised geometries | Gaussian 09 frequency calculation | Same level; minima/TS assignment from frequencies | Frequencies and thermal corrections | ev_doc_5c9d1cfdb571_000428_c65b83cbeac9 |
| 3 | Refine electronic energies for solvent | Optimised geometries | Gaussian 09 single points | ωB97X-D3(BJ)/def2-TZVP, IEFPCM(toluene) | Solvent electronic energies | ev_doc_5c9d1cfdb571_000428_c65b83cbeac9 |
| 4 | Assemble corrected free energies | Electronic and thermal terms | Paper arithmetic | Half of the entropy correction (0.5TS) | Gsol values and relative profile | ev_doc_5c9d1cfdb571_000436_015c159f65e1 |
| 5 | Interpret the cycle | Relative Gsol profile | Authors' mechanistic analysis | Compare catalysed and uncatalysed alternatives | Barrier and rate-determining-step claims | ev_doc_1791ce11c5dd_000080_fceba7d6d35c |

## 4. Validation and analysis protocol

The SI says frequencies were used to confirm each minimum or transition state. The paper analyses the ordered cycle from initial sulfur attack through ylide, rearrangement, catalysed aromatisation, and deamination, and compares the catalysed aromatisation with the uncatalysed TS3B/TS3A route. Relative barriers are read from the corrected solvent free-energy profile.

## 5. Private reference results

The main paper reports activation free energies of 30.4 kcal mol−1 for TS1A, 43.2 kcal mol−1 for uncatalysed TS3A, 19.8 kcal mol−1 for TXT-assisted TS3A-TXT, and 32.7 kcal mol−1 for TS4A-TXT. TS4A-TXT is reported as the highest barrier and rate-determining step. The SI Table S1 provides the underlying labelled stationary-point energy columns and Cartesian-coordinate blocks.

## 6. Limitations and interpretation boundaries

These are single-model DFT results with continuum solvation and an empirical half-entropy treatment; they are not a direct kinetic measurement. Stationary-point connectivity and frequency character must be checked independently, and alternative conformers/pathways may change quantitative barriers. The reference claims support comparison within this model system and protocol, not universal mechanistic proof.
