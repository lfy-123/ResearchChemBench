# Private paper route

## 1. Scientific objective and author claim

The paper develops an energy-minimization model for the equilibrium inner radius of spontaneously formed in-plane Janus-TMD/traditional-TMD nanoscrolls and validates it with molecular dynamics (MD). For a 200 nm MoSSe/MoS2 ribbon with equal-length segments, the authors report a stable scroll and an MD inner radius of 2.69 nm.

## 2. System and model boundary

The system is a free-standing, two-segment planar nanoribbon: an inner/leading MoSSe segment and an outer MoS2 segment, each 0.5L, with L=200 nm. The continuum cross-section is represented by joined Archimedean spiral segments. Material data are the SI values: kappa(MoSSe)=15.2 eV, C(MoSSe)=0.018 A^-1, kappa(MoS2)=11.6 eV, C(MoS2)=0, h(MoSSe/MoSSe S-Se)=6.329 A, h(MoS2/MoS2)=6.066 A, gamma(MoSSe)=0.0282 eV/A2, gamma(MoS2)=0.0256 eV/A2, and gamma(interface MoSSe/MoS2 S-Se)=0.0288 eV/A2.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build heterostructured ribbon | MoSSe and MoS2 nanoribbon segments | LAMMPS atomistic model | 200 nm total length; 50% MoSSe; armchair width orientation | Initial ribbon | ev_doc_b59c2e361daf_000106_ecee70fa54e4; ev_doc_b59c2e361daf_000165_7f75a8d61f3a |
| 2 | Simulate spontaneous scrolling | Initial ribbon | LAMMPS MD with hybrid SW+LJ | NVT, 1 K, Nose-Hoover, Verlet, 1 fs; fixed ~2 nm traditional-TMD end; release below 10 nm unrolled; 3000 ps relaxation; FIRE minimization | Relaxed nanoscroll | ev_doc_b59c2e361daf_000106_ecee70fa54e4; ev_doc_b59c2e361daf_000107_fdd4fdf57fe0; ev_doc_b59c2e361daf_000108_cf66f6b9b405 |
| 3 | Measure radius | Relaxed scroll | Fit/average curvature from Mo atoms in innermost turn; R_in=1/kappa-hbar/2 | Stable Archimedean-like cross-section | R_MD | ev_doc_b59c2e361daf_000166_d24f2bd8a61c; ev_doc_b59c2e361daf_000167_2e2e41cde851 |
| 4 | Compare to theory | R_MD and continuum parameters | Numerically solve dE_total/dR_in=0; parity/RMSD analysis | Complete-turn and incomplete-turn regimes | R_theory and agreement metric | ev_doc_b59c2e361daf_000175_4febb55d5813; ev_doc_b59c2e361daf_000191_334ec104a61d |

## 4. Validation and analysis protocol

The authors check stable scrolling morphology, finite-width effects, and temperature sensitivity. The 1 K structure is close to an Archimedean spiral; a 2.5 nm finite-width control has negligible edge effect, while 100 K produces deviations. The thermodynamic equations use area conservation, bending energy relative to spontaneous curvature, intrasegment vdW energy, and interfacial vdW energy. The outer segment is treated with a complete-turn expression when its angular span is at least 2pi and an incomplete-turn expression otherwise.

## 5. Private reference results

For the 200 nm, 50:50 MoSSe/MoS2 case the paper reports R_MD=2.69 nm. The MD/theory parity analyses report RMSD values of 0.093–0.164 nm for the length-series comparisons, and MD radii are slightly larger than theory. The paper reports a decreasing radius with increasing MoSSe fraction and a nonmonotonic length dependence for Janus-containing ribbons.

## 6. Limitations and interpretation boundaries

The continuum model assumes ideal Archimedean geometry and energetically favorable stacking; atomistic MD has nonideal stacking and a free inner tip. The source does not provide exact coordinates or a complete reproducible LAMMPS data file, so the public benchmark uses the source-supported continuum boundary and does not score atomistic trajectory identity.
