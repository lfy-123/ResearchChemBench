# Private paper route

## 1. Scientific objective and author claim

The authors used DFT to test whether the isolated free ligand 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline (compound 1) has a stable optimized geometry consistent with its single-crystal structure. They claim that most optimized bond lengths agree within 0.002–0.006 Å, with bond-length RMSE 0.004 Å and linear-fit R² 0.998, and that vibrational analysis gives a local minimum with no imaginary frequencies.

## 2. System and model boundary

The system is the neutral closed-shell organic ligand 1, formula C15H13N3, treated as an isolated gas-phase molecule. The experimental comparison is to the intramolecular geometry of crystal record CCDC 2433822 (compound 1), not to periodic crystal packing. The paper notes that the calculated pyridine-ring orientation differs from the solid-state orientation because packing is absent.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain starting geometry | Crystal coordinates for ligand 1 | Gaussian 03 | Neutral singlet; isolated molecule | Starting molecular geometry | ev_doc_ffa109983c32_000098_782c4a28fc72; ev_doc_ffa109983c32_000100_5237824e897a |
| 2 | Optimize ground-state geometry | Starting geometry | Gaussian 03 | B3LYP/6-311+G(2d,p) | Optimized structure | ev_doc_ffa109983c32_000098_782c4a28fc72; ev_doc_ffa109983c32_000099_2d4fddfc4629; ev_doc_ffa109983c32_000314_f58897638e8d |
| 3 | Verify local minimum | Optimized structure | Gaussian 03 | Harmonic vibrational analysis at same level | Frequencies; no imaginary modes claimed | ev_doc_ffa109983c32_000100_5237824e897a; ev_doc_ffa109983c32_000314_f58897638e8d |
| 4 | Compare to experiment | Optimized structure and selected crystal geometry | In-paper/SI analysis | Bond-length RMSE and linear regression | RMSE, regression and R² | ev_doc_ffa109983c32_000100_5237824e897a; ev_doc_ffa109983c32_000102_94c6ad17fc35; ev_doc_ffa109983c32_000105_9fb4f0f5ebe3 |

## 4. Validation and analysis protocol

The optimized structure was accepted as a local minimum from the vibrational modes. Selected bond lengths in SI Table S2 were compared with their experimental values; the paper reports the RMS error and a linear regression of calculated against experimental distances. The paper also reports that the calculated pyridine orientation is opposite to the crystal orientation, a limitation attributable to gas-phase versus packed-solid environments.

## 5. Private reference results

The reported ligand-1 bond-length RMSE is 0.004 Å; the reported regression is d_calc = 1.0467 d_exp − 0.0647 with R² = 0.998; and the optimized structure has no imaginary frequencies. These are hidden evaluator references.

## 6. Limitations and interpretation boundaries

This is a molecule-versus-crystal-geometry validation, not a prediction of crystal packing, polymorphism, solution structure, or experimental spectroscopy. Alternative defensible computational methods may be reported, but comparison must identify method sensitivity and cannot claim exact reproduction if the input record, atom mapping, or observable definition changes. The authors' gas-phase conformer can differ in ring orientation from the packed crystal.
