# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum chemistry to explain the push–pull electronic structure and photophysical behavior of representative bis(enamino) 4-methylene-1,4-dihydropyridines. For compound 3i, the claim is that solvated TD-DFT gives identifiable absorption and fluorescence maxima consistent with its ICT chromophore.

## 2. System and model boundary

Compound 3i is 5-(1-benzyl-2,6-bis((E)-2-(dimethylamino)vinyl)pyridin-4(1H)-ylidene)-1,3-diethyl-2-thioxodihydropyrimidine-4,6(1H,5H)-dione, neutral closed-shell singlet, in implicit DMSO. The supplied SI optimized ground-state geometry contains 71 atoms and is the starting structure.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Ground-state optimization | 3i geometry | DFT, US GAMESS 30 Sep 2021 R2 Patch 1 | B3LYP/6-31G(d,p)++; C-PCM DMSO; 298.15 K, 1 atm; RMS gradient 1e-7 Ha/Bohr; SCF 1e-5 a.u.; 96 radial/302 angular grid | optimized S0 geometry; harmonic frequencies | ev_doc_4e31a27ff5b2_000784_e3d37b2a5115, ev_doc_4e31a27ff5b2_000786_64d15c5fd5eb, ev_doc_4e31a27ff5b2_000787_897e22e6c4ed |
| 2 | Vertical absorption | optimized S0 geometry | TD-DFT, US GAMESS | CAM-B3LYP/6-31G(d,p)++; S0→S1…S7; non-equilibrium DMSO solvation; Gaussian broadening σ=0.4 eV | absorption spectrum/max | ev_doc_4e31a27ff5b2_000791_a2b8bdd064ff, ev_doc_4e31a27ff5b2_000798_1e997b1583f2 |
| 3 | Relaxed excited state | optimized S0 geometry | analytical-gradient excited-state optimization | CAM-B3LYP/6-31G(d,p)++; S1(π,π*); equilibrium DMSO; RMS gradient 1e-5 Ha/Bohr; TD-SCF 1e-6 a.u. | relaxed S1 geometry | ev_doc_4e31a27ff5b2_000796_14ea6a3efdcb, ev_doc_4e31a27ff5b2_000798_1e997b1583f2 |
| 4 | Vertical emission | relaxed S1 geometry | TD-DFT, US GAMESS | CAM-B3LYP/6-31G(d,p)++; S1→S0; non-equilibrium DMSO | emission spectrum/max | ev_doc_4e31a27ff5b2_000797_198979766cc1, ev_doc_4e31a27ff5b2_000798_1e997b1583f2 |

## 4. Validation and analysis protocol

The authors checked that optimized ground-state structures had no imaginary frequencies, optimized the first singlet excited state, plotted normalized Gaussian UV-vis spectra, and interpreted HOMO localization on donor/DHP atoms and LUMO distribution over the chromophore as evidence for ICT.

## 5. Private reference results

SI Table S1 reports for 3i in DMSO a calculated absorption maximum of 379 nm and emission maximum of 443 nm. The main paper identifies 3i as a representative bis(enamino) derivative and reports the donor-localized HOMO/extended LUMO ICT interpretation.

## 6. Limitations and interpretation boundaries

These are model-dependent calculated maxima, not experimental observables. Differences in conformer, state character, solvation implementation, broadening, numerical convergence, and software can shift values. Evaluation therefore accepts independently justified computational choices and treats the reported values as reference points rather than universal exact truths.
