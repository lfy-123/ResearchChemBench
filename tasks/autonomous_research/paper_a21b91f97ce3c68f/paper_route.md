# Private paper route

## 1. Scientific objective and author claim

The paper tests whether one-bond ^119Sn–^13C couplings in anomeric tributyltin compounds track antiperiplanar donor→σ*(C–Sn) hyperconjugation. The authors claim that stronger donation weakens/lengthens C–Sn and lowers the coupling magnitude; β/equatorial congeners generally have larger couplings than α/axial congeners. They also report an empirical sign/magnitude correction for absolute agreement with experiment.

## 2. System and model boundary

The benchmark system is the neutral singlet, axial galactose-derived tributyltin structure labelled 1a (43 atoms), with the SnBu3 group bonded at the anomeric carbon. The reported observable is ^1J(^119Sn–^13C_Bu), the average one-bond coupling over the three Sn–butyl carbon pairs; the anomeric Sn–C coupling and NBO donor terms are secondary analyses.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate low-energy conformers | 2D/starting geometry for each structure | CREST/GFN2-xTB | Lowest-energy axial and equatorial structures selected | Selected conformer | ev_doc_b3b050e4eca6_000020_de771cfa704f |
| 2 | Obtain stationary geometry and donor analysis | Selected conformer | Gaussian16 | (GD3)B3LYP/Def2TZVPP, gas phase; optimization, frequencies, NBO 3.1/3.17 | Optimized minimum and NBO donor energies | ev_doc_b3b050e4eca6_000020_de771cfa704f |
| 3 | Compute heavy-atom couplings | Optimized geometry | Gaussian16 | (GD3)B3LYP/TZP-ZORA; nmr=(spinspin,mixed,readatoms); integral=NoXCTest | ^1J(Sn–C) couplings and single-point properties | ev_doc_b3b050e4eca6_000020_de771cfa704f; ev_doc_b3b050e4eca6_000021_298c8dc9c778 |
| 4 | Compare with experiment | Calculated couplings | Author analysis | Average Sn–C_Bu values; empirical linear correction reported in SI | Corrected coupling and error/trend analysis | ev_doc_63683f376088_000028_fcd1e21c9979; ev_doc_b3b050e4eca6_000052_* |

## 4. Validation and analysis protocol

The authors benchmarked C–H couplings (maximum error about 9 Hz; MAE about 5 Hz), checked axial/equatorial trends, examined solvent sensitivity, and compared calculated tin couplings with available experimental data. Frequencies establish minima. Solvent tests retained qualitative trends and showed a maximum gas/solvent difference of 6.65 Hz for the tested structures.

## 5. Private reference results

For 1a, the SI reports the optimized anomeric coupling as −248.14 Hz and the average butyl coupling as −217 Hz. The main paper/SI report the experimental ^1J(Sn–C) values and a fitted correction J(corrected)=−1.419·J(calculated); these values are evaluator-only.

## 6. Limitations and interpretation boundaries

This is a single-structure reproduction/calibration test, not a claim of universal predictive accuracy. Heavy-atom coupling signs differ between quantum-chemical convention and common experimental reporting. Conformer selection, functional/basis sensitivity, relativistic treatment, solvent, and averaging over butyl sites should be reported as limitations. Agreement with one experimental value cannot establish the full mechanistic model.
