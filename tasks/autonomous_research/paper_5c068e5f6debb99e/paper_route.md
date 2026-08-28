# Private paper route

## 1. Scientific objective and author claim

For sulfur transfer from N-(p-tolylthio)phthalimide 2a to N-hydroxy-3-oxo-N-phenylbutanamide 5a under sodium tert-butoxide, determine why initial C–S formation at the 1,3-dicarbonyl carbon competes successfully with O–S formation at the hydroxylamine oxygen. The authors claim the C-site substitution has the lower solution free-energy barrier and is stabilized by stronger sodium-associated and pi-stacking interactions.

## 2. System and model boundary

The authors modeled a closed-shell, base-associated ensemble of 2a, 5a, and sodium counterions. A deprotonated sodium-associated reactant complex, INT1, is the common zero. TS1 forms O–S while cleaving N–S; TS2 forms C–S while cleaving N–S. The comparison concerns only initial substitution in DME, not the complete cascade to oxazolone 7a.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define reference | 2a, 5a, sodium base | Molecular modeling | Deprotonated, sodium-associated singlet | INT1 | ev_doc_3d9c7105809c_001078_1c823dd1b40b; ev_doc_3d9c7105809c_001091_5edb96411500 |
| 2 | Optimize minimum | INT1 | Gaussian 09, M06-2X/6-31G(d) | Frequencies; SMD(DME) | Validated minimum | ev_doc_3d9c7105809c_001077_7f13f9f52857 |
| 3 | Locate O-site TS | INT1, O-attack guess | Same optimization level | One imaginary mode; IRC | TS1 | ev_doc_3d9c7105809c_001101_3c3aa904fb11; ev_doc_3d9c7105809c_001107_55cf45d84fbb |
| 4 | Locate C-site TS | INT1, C-attack guess | Same optimization level | One imaginary mode; IRC | TS2 | ev_doc_3d9c7105809c_001116_426c7d3a8ce7; ev_doc_3d9c7105809c_001122_db06c534f633 |
| 5 | Refine energies | INT1, TS1, TS2 | M06-2X/6-311+G(d,p) | Single points; SMD(DME); thermal corrections | Relative solution barriers | ev_doc_3d9c7105809c_001077_7f13f9f52857 |
| 6 | Explain ordering | TS1, TS2 | NPA, NCI, VMD | Charges, Na–pi and pi–pi contacts, bond distances | Interaction interpretation | ev_doc_143c7d2f593e_000093_1774c200603b; ev_doc_143c7d2f593e_000101_bf0a6d399cd7; ev_doc_143c7d2f593e_000112_8aa781cdbd99 |

## 4. Validation and analysis protocol

Minima have zero imaginary frequencies; transition states have one imaginary frequency and IRC confirmation. Barriers are solution Gibbs free energies relative to INT1. Because TS1 has a shallow reported imaginary mode, mode identity and endpoint connectivity are essential.

## 5. Private reference results

- O-site barrier: 20.0 kcal/mol; C-site barrier: 11.3 kcal/mol; C-site advantage: 8.7 kcal/mol (ev_doc_143c7d2f593e_000089_7a32ead6853e).
- TS2: N–S 1.95 Å, forming C–S 2.33 Å. TS1: N–S 2.32 Å, forming O–S 1.86 Å (ev_doc_143c7d2f593e_000112_8aa781cdbd99).
- NPA values do not explain the ordering: TS1 Q(S)=+0.469 e, Q(O)=−0.617 e; TS2 Q(S)=+0.424 e, Q(C)=−0.584 e (ev_doc_143c7d2f593e_000093_1774c200603b).
- Authors attribute TS2 stabilization to stronger Na–pi(phenyl) and pi–pi interactions (ev_doc_143c7d2f593e_000101_bf0a6d399cd7; ev_doc_143c7d2f593e_000112_8aa781cdbd99).

## 6. Limitations and interpretation boundaries

The result addresses two initial substitution channels in one sodium-associated model. It does not establish exhaustive aggregation/conformer coverage, a full cascade pathway, product ratios, or a unique interaction explanation. The SI explicitly says later steps and inorganic-base participation remain incompletely understood.
