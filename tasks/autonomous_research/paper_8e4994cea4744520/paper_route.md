# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT calculations on five diphenylamine side-chain fragments to quantify how para fluorination versus para butyl substitution changes fragment dipole moments, supporting its interpretation of electrostatic-potential patterns in GA-2F-E and GA-2F. The author claim is that the asymmetric mixed fragment is strongly polar and that the placement of fluorinated and butyl-containing side chains changes the electrostatic environment relevant to packing and charge transport.

## 2. System and model boundary

The computed objects are isolated, neutral, closed-shell fragments: 4-fluoroaniline, 4-butylaniline, bis(4-fluorophenyl)amine, (4-butylphenyl)-N-(4-fluorophenyl)amine, and bis(4-butylphenyl)amine. The SI calls these simplified acceptor/side-chain models and reports gas-phase DFT geometry optimization. The full GA-2F-E/GA-2F molecules, solid-state packing, solvent, and device are outside this calculation boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define simplified side-chain fragments | Five named diphenylamine-related fragments | Molecular structures shown in Fig. 1a | Neutral closed-shell fragments | Molecular models | ev_doc_4632d9adaef6_000044_7cdb807b213e; ev_doc_4632d9adaef6_000045_c60509d74669 |
| 2 | Obtain stationary-point geometries | Fragment molecular models | Gaussian 09 Rev. D.01 DFT geometry optimization | PBE0/6-311G(d) | Optimized geometries | ev_doc_ad05541ed02e_000001_152a4aea9d5b; ev_doc_ad05541ed02e_000016_152a4aea9d5b |
| 3 | Evaluate molecular polarity | Optimized fragment geometries | DFT calculation; results processed with Multiwfn | Dipole magnitude reported in Debye | Five dipole moments | ev_doc_ad05541ed02e_000001_152a4aea9d5b; ev_doc_ad05541ed02e_000016_152a4aea9d5b; ev_doc_4632d9adaef6_000044_7cdb807b213e |
| 4 | Interpret side-chain electrostatics | Fragment dipoles and full-acceptor ESP illustrations | Qualitative comparison | Relate fluorination position to ESP distribution and packing/transport interpretation | Structural-property interpretation | ev_doc_4632d9adaef6_000044_7cdb807b213e; ev_doc_4632d9adaef6_000045_c60509d74669 |

## 4. Validation and analysis protocol

The source-supported process validation is that each optimized structure should be a genuine minimum, checked by vibrational analysis for absence of imaginary frequencies. Dipole magnitudes are compared fragment-by-fragment with the published values, and aggregate MAE, RMSE, and maximum absolute error are reported. Dipole magnitudes are scalar observables; orientation conventions and arbitrary coordinate frames do not affect the comparison. The paper's ESP discussion is qualitative and is not treated as a hidden numeric target.

## 5. Private reference results

The published dipole magnitudes (Debye), in the fragment order above, are 3.55, 1.76, 2.05, 2.26, and 0.68. The mixed (4-butylphenyl)-N-(4-fluorophenyl)amine has the highest reported dipole among the three diarylamines; it is not the highest among all five named fragments. These values are evaluator-only references.

## 6. Limitations and interpretation boundaries

The paper does not provide Cartesian starting coordinates or a complete machine-readable input deck, and dipole values can depend on conformer and implementation details. The task therefore requires the Agent to state how starting structures and conformers were generated, retain the tested conformers, and report convergence and frequency evidence. Agreement is assessed against the source-reported scalar values, while no claim is made that this fragment calculation alone proves solid-state packing or device performance.

## Source-scope correction (2026-09-15)

Source boundary reviewed 2026-09-15: main p3 lists 3.55/1.76 D for the two monoarylamines and 2.05/2.26/0.68 D for the three diarylamines. Thus mixed is highest only within the three-diarylamine subset, not all five. Fig. 1a labels bis(4-butylphenyl)amine 1.76 D, conflicting with main-text 0.68 D. The existing 0.68 D main-text numeric target is retained with this explicit unresolved source conflict; no tolerance or scientific objective is reduced.
