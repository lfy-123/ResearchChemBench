# Private paper route

## 1. Scientific objective and author claim

The paper tests whether electronic donor/acceptor substitution and geometric distortion modulate the thermal Bergman cycloaromatization barrier of triazolyl enediyne–amino-acid hybrids. The authors claim that through-bond charge-transfer delocalization stabilizes the diradical transition state in donor–acceptor systems, while steric loss of planarity can inhibit this effect.

## 2. System and model boundary

The computational set is EDY 15 (D–D), EDY 16 (D–A1; A1 is para-cyano phenyl), and EDY 17 (A1–A1), gas-phase isolated molecules. The enediyne reactive centers are C15/C16 (diradical-forming) and C17/C32 (new C–C bond-forming); arm B is the C11–C16–C32 side attached to triazole N10 and arm A is the C12–C15–C17 side attached to N13. The reported observable is the electronic activation energy from optimized reactant to optimized Bergman-cyclization TS.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize reactant and product minima | SI geometries for EDY 15–20 | Gaussian 09 DFT | RB3LYP/6-31G(d,p), gas phase, singlet | stationary-point geometries and energies | ev_doc_2fd7cb711763_000118_3195f8e64739; ev_doc_2fd7cb711763_000120_6483533d515f; ev_doc_50d09ca50478_000260_d1936b149658; ev_doc_50d09ca50478_000278_69dedd40f6f3; ev_doc_50d09ca50478_000297_43b8ee85b66b |
| 2 | Locate Bergman cyclization TS | optimized reactant/product structures and TS guess | Gaussian 09 QST3 | UB3LYP/6-31G(d,p), singlet | TS with one imaginary frequency | ev_doc_2fd7cb711763_000120_6483533d515f; ev_doc_50d09ca50478_000267_4f20786315d0; ev_doc_50d09ca50478_000282_0f2d2f9c0c0a; ev_doc_50d09ca50478_000300_7b7d0f8f7e2e |
| 3 | Verify and compare barriers | optimized reactant/TS energies | frequency analysis and energy subtraction | ΔE‡ = E(TS) − E(reactant), converted hartree to kcal/mol | activation energies and trend | ev_doc_2fd7cb711763_000112_97e937f7e98b; ev_doc_2fd7cb711763_000131_bb1f4bb0d2f1 |
| 4 | Interpret electronic/geometric origin | NBO, FMO, dihedral and distance analyses | Gaussian 09 NBO/TD-DFT/IRC analyses | reactive-center charges, second-order interactions, c,d distance and dihedrals | CT and distortion interpretation | ev_doc_2fd7cb711763_000131_bb1f4bb0d2f1; ev_doc_2fd7cb711763_000133_664226e75adf; ev_doc_50d09ca50478_000203_24ecf9942ef7 |

## 4. Validation and analysis protocol

Reactant and product frequency analyses were required to have zero imaginary frequencies; the TS was required to have exactly one. The paper additionally used IRC calculations to connect TS and minima, compared the C17–C32 distance, and analyzed NBO charge density and perturbation energies at reactive centers. DSC onset temperatures were used as an experimental qualitative comparison, not as the electronic barrier itself.

## 5. Private reference results

Table 1 reports activation energies of 46.89 kcal/mol for EDY 15, 45.96 kcal/mol for EDY 16, and 47.69 kcal/mol for EDY 17. The paper states the computed barrier ordering 17 > 15 > 16 for this subset and interprets EDY 16 as CT-stabilized relative to EDY 15 and EDY 17, with EDY 17 additionally suffering loss of planarity and charge accumulation.

## 6. Limitations and interpretation boundaries

These are gas-phase electronic barriers at one DFT model and do not directly reproduce solid-state DSC onset temperatures. Conformer and TS-search dependence, omission of thermal/entropic corrections, and the paper's internally mixed RB3LYP/UB3LYP notation limit quantitative transferability. A failed TS search is a bounded computational outcome and must be reported rather than replaced by an unverified structure.
