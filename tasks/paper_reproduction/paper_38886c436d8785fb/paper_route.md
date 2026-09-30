# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum chemistry to test whether the ionic liquid [C8MIm][NTf2] strengthens the association of 1,3,5-triformylbenzene (Tb) with p-phenylenediamine (Pa), supporting the proposed explanation for rapid, high-crystallinity TbPa-COF membrane formation. The reported interaction-energy change is from −16.5 to −95.2 kJ/mol.

## 2. System and model boundary

The molecular identities are neutral Tb, neutral Pa and [C8MIm][NTf2]. The current finite molecular calculation includes Tb·Pa, C8-IL·Tb, and C8-IL·Tb·Pa. SI Fig. 35b explicitly compares Pa binding to Cn-IL–Tb: the ternary energy reference must keep the ion pair and Tb together, not subtract all four isolated molecules. Fig. 3e and the publisher's Source Data label the control “Hex-Tb-Pa”; the retrieved methods do not resolve whether this implies an explicit/implicit hexane treatment or only labels the experimental control. Isolated gas phase is therefore a disclosed reconstruction, not a verified exact control model. Periodic COF formation, polymer growth and the separate MD simulations are outside the assessment sub-question.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize every molecular/complex geometry | Tb, Pa, C8-IL and complexes | Gaussian 09 | B3LYP/6-311G(d); isolated-molecule model | optimized geometries | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 2 | Verify stationary points | optimized geometries | Gaussian 09 frequency calculation | no imaginary frequency required for local minima | frequency-validated minima | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 3 | Evaluate interaction energies | optimized monomers and complexes | Gaussian 09 | B3LYP-D3(BJ)/6-311G(d) | Tb·Pa and C8-IL·Tb·Pa binding energies | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 4 | Interpret noncovalent contacts | optimized wavefunctions | Multiwfn + VMD | Hirshfeld IGM, isosurface 0.001 a.u. | interaction-region visualization | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 5 | Relate computation to mechanism | computed interaction strengthening plus experiments/MD | qualitative synthesis | IL ion/H-bond network and water encapsulation | mechanistic interpretation | ev_doc_5891573f19ff_000088_4ab34ceb2f98; ev_doc_5891573f19ff_000089_849b61cb66c0 |

## 4. Validation and analysis protocol

The authors optimized structures, used frequencies to identify local minima, then evaluated dispersion-corrected interaction energies. The interaction is interpreted together with IGM contact maps and the paper's WAXS/RDF/FT-IR and reverse-phase-microemulsion observations. The DFT result is a qualitative mechanistic support, not a direct calculation of a crystallization barrier.

## 5. Private reference results

Fig. 3e reports −16.5 kJ/mol for the Hex-Tb-Pa control and −95.2 kJ/mol for C8-IL-Tb-Pa. Source Data sheet “Supplementary Fig. 35b” confirms the latter, while the SI caption identifies the partners as Cn-IL–Tb and Pa. These are reference observations, not raw computed energies to insert into a reproduction. Numerical targets and tolerances are unchanged, but exact model correspondence must be checked before comparison. Water encapsulation and acid-mediated kinetics belong to the paper's separate mechanistic evidence.

## 6. Limitations and interpretation boundaries

The retrieved main text, SI and relevant publisher Source Data sheets do not provide unique Cartesian coordinates, raw SCF energies, the exact Hex-control implementation, or an unambiguous relaxed/frozen/BSSE prescription. These limitations must not be replaced with guessed author settings or hidden target-nearest selection. Use E(C8-IL·Tb·Pa) − E(C8-IL·Tb) − E(Pa) for the defined partner grouping, explicitly state the fragment geometry convention, and retain the unresolved source boundaries. Molecular interaction energies do not establish a crystallization barrier or the complete experimental mechanism. No scientific-goal reduction is authorized by this correction.

Source correction audited 2026-09-18 against main PDF pp. 3/5/8, SI p. 36 Fig. 35, and [publisher Source Data](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-67569-9/MediaObjects/41467_2025_67569_MOESM5_ESM.xlsx). Hashes, archived prior task files and failed-model evidence are in `docs/verification/group_2/paper_38886c436d8785fb/provenance/source_model_review_20260918/`.
