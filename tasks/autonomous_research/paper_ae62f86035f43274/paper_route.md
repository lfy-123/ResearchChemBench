# Private paper route

## 1. Scientific objective and author claim

The paper studies neutral and singly anionic \((\mathrm{CuIn})_n\mathrm{Te}_2\) clusters for n=1–8. The focused claim used here is that the n=2 composition, \(\mathrm{Cu}_2\mathrm{In}_2\mathrm{Te}_2\), is an especially stable cluster and has a large neutral HOMO–LUMO gap; its anion has a distinct low-lying geometry and reported ADE/VDE values. The authors claim the neutral low-energy geometry is a three-dimensional structure associated with a flat rhombus and triangular-prism motif, while the anion can include an In–In contact.

## 2. System and model boundary

The system is an isolated six-atom cluster with composition Cu2 In2 Te2, considered at charge 0 and charge −1. The calculations use a periodic cubic vacuum cell (20 Å for clusters shorter than 10 Å), Γ-point sampling, plane waves and ultrasoft pseudopotentials. The reported electronic observables are neutral binding energy and HOMO–LUMO gap, and anion adiabatic and vertical detachment energies. The paper describes non-spin-polarized calculations; its treatment of the odd-electron anion multiplicity is not explicitly resolved.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate candidate structures | Cu, In and Te atoms in hypothetical symmetric and nonsymmetric arrangements | VASP DFT | Multiple planar and 3-D arrangements | Initial isomer geometries | ev_doc_3518f7d32645_000020_b21d9c733e09; ev_doc_3518f7d32645_000022_06706137319f |
| 2 | Relax neutral isomers | Candidate Cu2In2Te2 geometries | VASP plane-wave DFT | 20 Å cubic cell, Γ point, 240 eV cutoff, ultrasoft pseudopotentials, conjugate-gradient relaxation, forces <10^-4 eV Å^-1 | Optimized neutral structures and energies | ev_doc_3518f7d32645_000020_b21d9c733e09; ev_doc_3518f7d32645_000022_06706137319f; ev_doc_3518f7d32645_000023_0ca7bc07c538 |
| 3 | Relax anionic isomers | Candidate Cu2In2Te2− geometries | Same VASP workflow with one extra electron | Same cell/cutoff/Γ-point/force criterion; anionic charge | Optimized anion structures and energies | ev_doc_3518f7d32645_000018_a14d157636f5; ev_doc_3518f7d32645_000022_06706137319f |
| 4 | Select low-energy structures | Relaxed isomer energies | Energy comparison | Total energies normalized to lowest isomer | Relative-energy ordering | ev_doc_a09d6c43c479_000016_29459fe68f1e; ev_doc_a09d6c43c479_000202_30c5f53d2b72 |
| 5 | Calculate electronic properties | Lowest neutral and anionic structures | VASP electronic-structure analysis | DOS Gaussian width 0.01 eV; frontier orbital energies | HL gap, BE, ADE and VDE | ev_doc_a09d6c43c479_000004_bb5d3b49727c; ev_doc_a09d6c43c479_000202_30c5f53d2b72; ev_doc_a09d6c43c479_000203_1c24dee774ec |

## 4. Validation and analysis protocol

The authors compare multiple converged isomers and normalize relative energies to the lowest structure. They inspect bond lengths, angles and motifs, then report frontier-level gaps, binding energies and detachment energies for the low-lying isomers. The n=2 neutral is described as having Cu–Cu 2.62 Å, typical Cu–In 2.69 Å, Cu–Te 2.42 Å and In–Te 2.84 Å contacts, with representative angles 49.2° and 62.4°. The anion discussion reports an In–In contact near 3.05 Å and altered Cu–Te/Cu–In distances.

## 5. Private reference results

For the first neutral isomer, Table 1 reports BE 3.166 eV, HL gap 1.652 eV, DE 3.958 eV, VDE 2.85 eV, ADE 2.37 eV and AIP 6.44 eV. Section 3.2.2 states that neutral isomers 2(a) and 2(b) are degenerate, with 2(c) and 2(d) higher by 0.087 and 0.105 eV relative to the lower pair (wording/layout places the comparison around these values). The low-lying anion has ADE 2.37 eV and VDE 2.85 eV. These values and route-specific structural details are private evaluator references.

## 6. Limitations and interpretation boundaries

The paper does not provide machine-readable Cartesian coordinates, a complete enumeration rule for all starting isomers, explicit exchange-correlation naming in the SI, or an unambiguous spin/multiplicity treatment for the odd-electron anion. Consequently, an independent task must score reproducible process, candidate identity, convergence and qualitative structural conclusions, while treating exact numerical agreement as method-dependent. The paper's labels 2(a)–2(d) are not public identities and are not used as public input identifiers.
