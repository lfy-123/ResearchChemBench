# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to test whether four phenanthroimidazole emitters (MeAC, TfAC, MeACFy and TfACFy) have deliberately distorted donor–acceptor geometries and frontier-orbital distributions compatible with hybridized local-and-charge-transfer (HLCT) emission. The authors claim that the acridine donor is nearly orthogonal to the connecting phenyl bridge, that the spirofluorene substituent is likewise highly twisted, and that HOMO density is concentrated mainly on acridine while LUMO density is concentrated mainly on the phenanthroimidazole/π-bridge acceptor region. They further interpret fluorene as increasing the local-excitation component and CF3 as strengthening charge-transfer character.

## 2. System and model boundary

The systems are neutral, closed-shell singlet molecules named and formulated in the paper: MeAC (C43H33N3), TfAC (C43H30F3N3), MeACFy (C53H35N3), and TfACFy (C53H32F3N3). The molecular graphs are fixed by the systematic product names and the Buchwald–Hartwig products described in the main paper and SI. The calculations concern isolated-molecule electronic structure; no crystal packing, solvent, aggregation, or experimental electrochemical calibration is part of the computational target.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Find optimized ground-state structures | Four neutral molecular graphs | Gaussian 09 W DFT | B3LYP/6-31G(d,p), singlet ground state | Optimized geometries | ev_doc_539505645b47_000045_07848638b61c; ev_doc_539505645b47_000178_642424ea9cff |
| 2 | Inspect twist and frontier orbitals | Optimized geometries | Gaussian 09 W; visualization of FMO densities | Measure α1, α2, α3 and β1 where present; inspect HOMO/LUMO | Dihedrals, orbital energies and density locations | ev_doc_539505645b47_000045_07848638b61c; ev_doc_539505645b47_000046_cc9e54afbd63 |
| 3 | Characterize excited-state HLCT behavior | Optimized geometries | TD-DFT and Multiwfn | TD-DFT at the same stated level; NTO and IFCT analysis | Excited-state energies, NTOs, CT/LE percentages | ev_doc_539505645b47_000178_642424ea9cff; ev_doc_a21214c5585c_000061_4fda97fccaf2 |
| 4 | Relate structural changes to orbital levels | Four computed molecules | Comparative interpretation | Me/Tf and AC/ACFy paired comparisons | Directional substituent effects | ev_doc_539505645b47_000046_cc9e54afbd63; ev_doc_539505645b47_000056_ba3365049409 |

## 4. Validation and analysis protocol

An optimization was accepted only when it reached a stationary point under the program's convergence criteria. The authors measured the labeled dihedrals on the optimized structures and inspected HOMO/LUMO density plots. For the excited-state interpretation they used NTO overlap/separation and fragment charge-transfer decomposition into phenanthrimidazole, the methylphenyl/bridge portion, and acridine-containing donor fragments. The source reports S1 CT/LE percentages of 46.60/53.40, 58.94/41.06, 45.95/54.05 and 56.42/43.58% for MeAC, TfAC, MeACFy and TfACFy, respectively, and near-degenerate S1–T2 or S1–T3 gaps of 0.011, 0.009, 0.011 and 0.008 eV.

## 5. Private reference results

The reported α3 values (MeAC, TfAC, MeACFy, TfACFy) are 89.17°, 87.11°, 87.11° and 88.70°. The reported β1 values for MeACFy and TfACFy are 87.11° and 88.02°. The paper states that α1 is relatively large and α2 relatively small, but does not provide machine-readable numerical values in the supplied evidence. HOMO is mainly on acridine, with some density on bridge/substituents; LUMO is mainly on phenanthrimidazole and π bridges. CF3 shifts LUMO density toward the short-axis substituent and lowers HOMO/LUMO, especially LUMO; fluorene slightly lowers both levels and increases LE character.

## 6. Limitations and interpretation boundaries

The paper does not provide initial Cartesian coordinates or a complete numerical table of the ground-state HOMO/LUMO eigenvalues in the supplied evidence. Therefore the released task must not score a unique starting conformer or exact ground-state orbital eigenvalues. Dihedral signs are convention-dependent, so comparisons should use absolute dihedral magnitudes or an explicitly documented atom order. Different legitimate conformers and computational models can change numerical values; the evaluator should reward converged, independently justified calculations and source-supported qualitative conclusions rather than claim universal method transferability.
