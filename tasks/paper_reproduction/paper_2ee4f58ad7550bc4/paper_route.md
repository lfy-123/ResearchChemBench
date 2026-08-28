# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT local Fukui functions to rationalize why thiocyanato-bridged Cu(II) complex 2 has higher catecholase activity than complex 1. The authors claim that the Cu site in 2 is more electropositive/electrophilic, giving stronger binding/activation of 3,5-di-tert-butylcatechol (3,5-DTBC).

## 2. System and model boundary

The experimental compounds are one-dimensional μ1,3-thiocyanato Cu(II) polymers [Cu(L1)(μ1,3-NCS)]n (1) and [Cu(L2)(μ1,3-NCS)]n (2), where HL1 is N-propyl-N-(5-bromosalicylidene)ethane-1,2-diamine and HL2 is the corresponding 5-chloro ligand. The calculation uses asymmetric monomeric units 1m and 2m, plus one-electron-reduced anions, rather than the periodic chain. Neutral models are triplet (S=1 as reported); reduced models are doublet (S=1/2). The scored local atom is the Cu center.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build monomer models | CCDC crystal structures 2453268 (1) and 2453269 (2) | Extract asymmetric monomeric units from the μ1,3 chain | 1m=[Cu(L1)(μ1,3-NCS)], 2m=[Cu(L2)(μ1,3-NCS)] | Molecular geometries | ev_doc_55386850914c_000354_e291eb9f5cc6; ev_doc_55386850914c_000519_1249b6865a5a |
| 2 | Optimize neutral and reduced states | 1m, 2m | DFT in Gaussian 09 | B3LYP/6-311G; neutral triplet and one-electron-reduced doublet | Optimized geometries | ev_doc_55386850914c_000378_c116980131ef; ev_doc_55386850914c_000379_c085c4771e3e; ev_doc_55386850914c_000380_185e560e2f34; ev_doc_55386850914c_000382_18ed49074b0e; ev_doc_55386850914c_000383_54225eddb592 |
| 3 | Obtain frontier orbitals | Optimized models | DFT in Gaussian 09 | B3LYP/6-311G | HOMO/LUMO localization and energies | ev_doc_55386850914c_000289_4c886c9f52e4; ev_doc_55386850914c_000379_c085c4771e3e |
| 4 | Compute local Fukui function | Neutral and reduced optimized models | Finite difference of atomic charges | fk+ = qk(N) − qk(N+1), k=Cu | Cu fk+ for each complex | ev_doc_55386850914c_000383_54225eddb592; ev_doc_55386850914c_000385_1cf9369f55d4 |
| 5 | Compare and interpret | Cu fk+ values | Direct comparison | Larger fk+ interpreted as greater electrophilicity and stronger substrate interaction | ev_doc_55386850914c_000011_aeb90f2d205c; ev_doc_55386850914c_000012_e32dbe66c0c0 |

## 4. Validation and analysis protocol

The paper checks that neutral and reduced calculations correspond to the reported spin states, that the Cu atom is consistently identified, and that the HOMO/LUMO density is on or around Cu. It then compares the Cu fk+ values and relates the ordering to catecholase kinetics measured for oxidation of 3,5-DTBC to 3,5-DTBQ in methanol under aerobic conditions.

## 5. Private reference results

Table 4 reports fk+ = 0.0182 for 1 and 0.0299 for 2. Thus 2 > 1. The paper reports kcat = 11.15 h−1 (1) and 29.76 h−1 (2), and describes the Cu-centered electronic difference as supporting the higher activity of 2.

## 6. Limitations and interpretation boundaries

The source does not fully specify monomer termination or every population-analysis implementation, and local Fukui values can depend on charge partitioning and geometry protocol. The task therefore scores reproducible state/object identity, charge-difference definition, Cu-value reporting, and source-backed interpretation; it must not claim that fk+ alone proves a complete catalytic mechanism or periodic-polymer behavior.
