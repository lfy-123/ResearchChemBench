# Private paper route

## 1. Scientific objective and author claim

The paper uses a bipyridyl–Cu model to explain MOF-253-Cu catalysis of the reaction of quinoline N-oxide with N,N′-dicyclohexylcarbodiimide (DCC). The computational claim is that Cu(II) coordination enables a stepwise pathway and lowers the key cycloaddition barrier relative to the uncatalyzed concerted pathway.

## 2. System and model boundary

The modeled system is quinoline N-oxide + DCC, with a Cu(II) site bound to 2,2'-bipyridine-5,5'-dicarboxylic acid (both COOH groups protonated), not unsubstituted bipyridine. The SI pp16–17 catalyst has 47 atoms, C16H20CuN2O6S2, including two DMSO ligands. Cat-IM1 has 84 atoms (catalyst + DCC); Cat-TS1, Cat-IM2 and Cat-TS2 have 82 atoms and no DMSO. Thus the balanced comparison is Cat-IM1 + quinoline N-oxide (102 atoms) versus Cat-TSn + two free DMSO molecules (102 atoms). The public model identity was corrected from the SI on 2026-09-15 without changing the barrier-comparison objective. The full MOF is represented by this molecular fragment; the uncatalyzed reference contains only the two organic reactants.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | SI coordinate geometries | Gaussian 16 Rev. C.012; unrestricted B3LYP-D3(BJ) | 6-31G(d) for H/C/N/O and LANL2DZ for Cu; Cu model charge +2, doublet | optimized structures | ev_doc_5c0521c119d7_000182_1e64cfa0c6b4; ev_doc_5c0521c119d7_000184_31989d590cb7; ev_doc_5c0521c119d7_000186_c2897c9a671c; ev_doc_5c0521c119d7_000188_c8f366789fd3 |
| 2 | Verify stationary-point character and obtain thermal corrections | optimized structures | Gaussian harmonic frequencies at the optimization level | minima have no imaginary modes; TS have one imaginary mode | frequency corrections and assignment | ev_doc_5c0521c119d7_000188_c8f366789fd3 |
| 3 | Refine energies in solvent | optimized structures | Gaussian single points, M06/SMD(DMSO) | 6-311+G(d,p) for light atoms including S; LANL2DZ for Cu | E_sol | ev_doc_5c0521c119d7_000189_1a11171e547b; ev_doc_5c0521c119d7_000190_88c54e48a49d |
| 4 | Build free-energy profile | E_sol and frequency corrections | arithmetic post-processing | G_sol = E_sol + frequency-derived correction; relative energies in kcal mol−1 | catalyzed and uncatalyzed barriers | ev_doc_5c0521c119d7_000199_9af3eee5ff12; ev_doc_5c0521c119d7_000202_277d9a271af8 |

## 4. Validation and analysis protocol

The authors compare the highest transition state reached from the relevant reactant reference in each pathway. Cat-TS2 is the rate-determining catalyzed step; Uncat-TS1 is the uncatalyzed concerted transition state. Use G(Cat-TS2) + 2G(DMSO) − G(Catalyst) − G(DCC) − G(quinoline N-oxide), not the unbalanced direct TS−Cat-IM1 subtraction. The reference is the separated bis-DMSO catalyst and two organic reactants; changing it to Cat-IM1 + quinoline N-oxide shifts the source barrier by about 0.7 kcal/mol. Figure S10 supplies optimized structures and selected distances, and Figure S11 reports a linear scan for the subsequent Cat-IM3 fragmentation, for which no separate transition state was found.

## 5. Private reference results

The main text reports a catalyzed key barrier of 31.7 kcal mol−1 and an uncatalyzed concerted barrier of 34.8 kcal mol−1. The catalyzed pathway is described as stepwise and energetically favored; Cu coordination to DCC and Lewis-acid activation are identified as the origin of the reduction. The first catalyzed transition state is reported at 20.9 kcal mol−1, while the alternative catalyst-pre-bound-to-quinoline route has a 35.3 kcal mol−1 transition state.

## 6. Limitations and interpretation boundaries

These are model-cluster results, not a periodic calculation on the full MOF. Relative free energies depend on conformer choice, charge/spin treatment, standard-state conventions and the chosen electronic-structure model. The evaluator therefore scores the explicitly defined barrier observables and stationary-point validation, and does not treat a different but documented model chemistry as automatically scientifically invalid.

SI p14 calls the thermal contribution enthalpic, whereas SI p16 explicitly labels the resulting table Gsol and describes Gibbs free energies. Preserve this wording inconsistency; evaluate the G construction against the table and do not silently substitute H. The source-table arithmetic (31.6892 and 34.8268 kcal/mol at printed precision) validates reference bookkeeping only and is not a new computed verification result.
