# Private paper route

## 1. Scientific objective and author claim

The paper uses TD-DFT to explain absorption of neutral N,O-bidentate difluoroboron complexes 1a–d. It attributes red shifts to pi expansion from pyridine to isoquinoline/quinoline and notes that 1c has a weak lowest transition while stronger higher transitions dominate.

## 2. System and model boundary

1a is the 2-pyridyl complex, 1b the 1-isoquinolyl complex, 1c the 3-isoquinolyl complex, and 1d the 2-quinolyl complex. The SI supplies labeled optimized S0 Cartesian coordinates.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Ground-state calculation | S0 geometries | DFT, Gaussian 16 | B3LYP/6-31G+(d,p), neutral singlet | orbitals and geometry | ev_doc_cf0c3cabace5_000037_02aa630be257 |
| 2 | Minimum validation | optimized structures | vibrational analysis | only real frequencies | local-minimum check | ev_doc_cf0c3cabace5_000037_02aa630be257 |
| 3 | Excited states | ground-state structures | TD-DFT, Gaussian 16 | TD-SCF/B3LYP/6-31+G(d,p) | energies, oscillator strengths, orbital assignments | ev_doc_f5c04055ec78_000042_fd4d044aa2fc |
| 4 | Experimental comparison | calculated transitions | UV-vis assignment | compare solution bands | shift/intensity interpretation | ev_doc_f5c04055ec78_000056_3844cd2bfc48 |

## 4. Validation and analysis protocol

The authors checked optimized structures by vibrational analysis, then interpreted excitation energies jointly with oscillator strengths and frontier-orbital character.

## 5. Private reference results

Experimental toluene absorption maxima are 345, 375, 383, and 381 nm for 1a–d, respectively. The paper reports red shifts for 1b–d and stronger short-wavelength 1c features near 341 and 351 nm in the TD-DFT discussion.

## 6. Limitations and interpretation boundaries

Vertical isolated-molecule calculations are compared with solution bands; solvent, vibronic structure, conformers, and model chemistry affect literal agreement.
