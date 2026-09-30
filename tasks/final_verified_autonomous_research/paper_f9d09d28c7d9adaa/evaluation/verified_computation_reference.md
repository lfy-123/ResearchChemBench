# Verified computation reference — paper_f9d09d28c7d9adaa (autonomous_research)

Private feasibility evidence for the S1-core contract revision of 2026-09-23. Four preserved ground-state minima and newly completed TD/NTO/IFCT analyses support the computation chain. This is not a blind agent replay, and matching qualitative trends is not exact reproduction of author percentages.

## Ground-state evidence

[Reaudited ground-state record](../../../../docs/verification/group_1/paper_f9d09d28c7d9adaa/artifacts/ground_state_reaudit_20260919/raw_results.json) contains the public-name-derived molecular graphs, original inputs/logs/checkpoints, optimized coordinates, indexed connectivity checks and overlap-aware Multiwfn Mulliken MO populations. All four B3LYP/6-31G(d,p) geometries completed optimization and have 3N−6 real modes with no imaginary frequencies. TfACFy terminates through Gaussian's negligible-force convergence branch; the verification does not claim every printed convergence column is YES.

| Molecule | Real / imaginary modes | α3 magnitude / ° | β1 plane angle / ° | HOMO acridine / % | LUMO principal localization |
|---|---:|---:|---:|---:|---|
| MeAC | 231 / 0 | 90.186961 | not applicable | 97.24873 | core 49.98485%, bridge 44.88034% |
| TfAC | 231 / 0 | 90.468049 | not applicable | 97.28111 | short-axis substituted aryl 70.41699% |
| MeACFy | 267 / 0 | 89.655247 | 88.697017 | 93.57180 | core 49.23911%, bridge 45.80047% |
| TfACFy | 267 / 0 | 90.247213 | 89.812951 | 93.56706 | short-axis substituted aryl 69.14633% |

β1 uses normalized least-squares-plane normals for the mapped complete aryl rings. The raw four-anchor torsions −166.690266/+167.095781° describe another observation and cannot replace β1. The previous plane-normal normalization and coefficient-square-population summaries are superseded by this reanalysis. The public atom-map selectors are graph identifiers; they need not equal an agent's output-file indices.

## Added excited-state verification

[Four Gaussian job records](../../../../docs/evalution/f9d09_core_validation_20260923/td_results.json) · [Four full analyses](../../../../docs/evalution/f9d09_core_validation_20260923/excitation_results.json).

Copied checkpoints preserve the original calculations. Gaussian 16 C.01 TD-B3LYP/6-31G(d,p), three singlet roots on each corresponding S0 geometry, SCF=(Tight,XQC,MaxCycle=512), NoSymm and IOp(9/40=4), completed normally for all four systems. Formatted checkpoints and printed excitation coefficients describe matching orbitals/geometry. The additional roots establish the low-lying state ordering; a bright higher state was not substituted for S1.

Multiwfn 2026.7.15 uses each matching fchk/log to generate S1 NTOs and IFCT. The declared three fragments are exhaustive, disjoint and include hydrogens with their heavy-atom parent. The primary IFCT calculation uses a Mulliken-like partition. NTO eigenvalues, exported orbitals, fragment populations, diagonal LE terms and directed CT terms are retained in each job directory, with exact stdin and analysis logs. Both analyses use the same S1.

| Molecule | SI S1 / eV | Calculated S1 / eV | SI CT / % | Calculated CT / % | Calculated LE / % | Dominant NTO weight |
|---|---:|---:|---:|---:|---:|---:|
| MeAC | 3.0446 | 3.0335 | 46.60 | 36.990 | 63.010 | 0.999642 |
| TfAC | 2.9162 | 2.9054 | 58.94 | 51.745 | 48.255 | 0.999540 |
| MeACFy | 3.0716 | 3.0811 | 45.95 | 36.492 | 63.508 | 0.999652 |
| TfACFy | 2.9552 | 2.9522 | 56.42 | 49.955 | 50.045 | 0.999536 |

The calculated oscillator strengths round to 0.0000 at the Gaussian output precision: these roots are dark/very weak, not absent states. The dominant NTO hole is about 99.95% on the combined donor/bridge fragment. Its electron population is distributed between that group and the other two fragments; the same-group IFCT contribution includes the bridge and must not be described as a spatial hole–electron overlap integral. Fragment LE/CT and spatial NTO interpretation are complementary, not interchangeable observables.

## Quantitative boundary

The added calculations establish feasibility of four same-state energy/NTO/IFCT records. They recover increased CT with CF3 (+14.755 and +13.463 percentage points) and slightly increased LE with Fy (+0.498 and +1.790 points). Absolute CT differs from the author by 6.465–9.610 points. A same-geometry MeAC Hirshfeld sensitivity check gives CT=37.986%, versus 36.990% with Mulliken-like partition; this does not resolve the source discrepancy. [Recorded sensitivity output](../../../../docs/evalution/f9d09_core_validation_20260923/MeAC/hirshfeld_probe_result.txt).

The exact author geometries, atom partition implementation and numerical details are not fully available. Their relative contribution to this offset is unknown. No source value is replaced, no acceptance tolerance is fitted to the local results, and exact IFCT numerical reproduction is not certified. Evaluators must distinguish quantitative agreement, qualitative trend support and unsupported assertions. Stronger automatic CT cutoffs require further independent calibration; these tasks currently retain semantic scientific assessment with explicit quantitative references.

References: main PDF pp.2–4 Fig.2/3 and §2.3; SI PDF pp.2–5 Fig.S1, p.6 Table S1 and p.7 Table S2. Multiwfn: T. Lu and F. Chen, J. Comput. Chem. 33, 580 (2012), DOI 10.1002/jcc.22885; T. Lu, J. Chem. Phys. 161, 082503 (2024), DOI 10.1063/5.0216272.

This contract includes new S1 scientific endpoints and has a new package content hash. Historical ground-state-only outputs retain their original frozen contracts and scores; they are not used as complete submissions to the new task. Triplet kinetics, RISC and device efficiency are not validated by this S1 subset.
