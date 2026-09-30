# Private paper route

## 1. Scientific objective and author claim

The paper tests whether explicit excited-state contributions improve thermodynamic prediction of photocatalytic H2O2 versus O2/H2O formation on Co single-atom g-C3N4. The authors claim that their most complete relaxed constrained-occupation treatment gives H2O2 as a viable product, consistent with prior experiments.

## 2. System and model boundary

The model is a Co atom embedded in a heptazine-based monolayer g-C3N4 M-N4 site, represented by a 2x2 hexagonal periodic slab with 57 atoms (56 C/N host atoms plus one Co atom) and 15 Å vacuum. Reaction intermediates are *, *OH, *O, *OOH, *OO, and *(OH)2; gas references include H2, H2O, H2O2 and O2.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state intermediates | Co/g-C3N4 structures | spin-polarized plane-wave DFT, VASP | HSE06+D3(BJ), PAW cutoff 400 eV, 2x2x1 Gamma grid, force 0.01 eV/A, electronic 1e-6 eV; selected atoms relaxed | optimized geometries and E0 | ev_doc_1b5acf18f451_000007_789ff9b060d5; ev_doc_1b5acf18f451_000015_0178933c1ed6 |
| 2 | Ground-state thermochemistry | optimized structures | vibrational/thermal correction | G=E0+G(T), ZPE, enthalpy and entropy at 298 K, 1 atm; H+/e- referenced to 1/2 H2 | G0 and reaction profiles | ev_doc_1b5acf18f451_000022_72aa76bdc51f; ev_doc_b5ebfd57001d_000001_b7efb6a6ac3 |
| 3 | Excited-state energies | ground-state structures | constrained-occupation Delta-SCF in VASP | VBM hole/CBM electron, Co midgap occupations retained; fixed occupations | VEE/AEE | ev_doc_1b5acf18f451_000033_1f4790716609; ev_doc_1b5acf18f451_000039_c2f62da62ace |
| 4 | Excited free energies | G0 and AEE | additive excited-state construction | G*=G0+AEE (Level 2a) | excited profiles | ev_doc_b5ebfd57001d_000134_43e4676626a1; ev_doc_b5ebfd57001d_000140_e15c9fe2bef0 |
| 5 | Selectivity analysis | profiles for OER/ORR branches | PDS and product comparison | compare O2 and H2O2 branches | DeltaDeltaG and preference | ev_doc_b5ebfd57001d_000258_f3b13e55f08b; ev_doc_b5ebfd57001d_000268_ec440defa46d |

## 4. Validation and analysis protocol

The authors compare gas-phase thermochemistry with experiment, test cutoff convergence, inspect excited-ground charge-density differences, and compare protocol levels and functionals. The OER branches are *+H2O-*OH-*O-*OOH-*OO-*+O2 and *+H2O-*OH-*(OH)2-*+H2O2; ORR is assessed through *OOH to H2O2.

## 5. Private reference results

At HSE-L2a the reported OER selectivity metric is DeltaDeltaG_OER = DeltaG_PDS-O2 - DeltaG_PDS-H2O2 = 0.35 eV, and the ORR quantity G(*+H2O2)-G(*OOH) is -0.35 eV. The paper reports H2O2 preference/viability at this level. At ground state the O2 PDS is lower than the H2O2 PDS.

## 6. Limitations and interpretation boundaries

This is thermodynamic, not kinetic, prediction; solvent, explicit interface dynamics and applied potential are omitted. The excited-state treatment assumes rapid charge separation and non-equilibrium ground-state thermochemistry. Pseudopotential names and some implementation details are not fully enumerated in the source.
