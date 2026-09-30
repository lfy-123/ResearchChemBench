# Private paper route

## 1. Scientific objective and author claim

The paper uses a bipyridyl–Cu model to explain MOF-253-Cu catalysis of the reaction of quinoline N-oxide with N,N′-dicyclohexylcarbodiimide (DCC). The computational claim is that Cu(II) coordination enables a stepwise pathway and lowers the key cycloaddition barrier relative to the uncatalyzed concerted pathway.

## 2. System and model boundary

The modeled system is quinoline N-oxide + DCC, with a Cu(II) bipyridyl site and DMSO ligation for the catalyzed model. The reported stationary-point labels are Cat-IM1, Cat-TS1, Cat-IM2, Cat-TS2, Cat-IM3 and Uncat-TS1. The full MOF is represented by a molecular bipyridyl-Cu fragment; the uncatalyzed reference contains only the two organic reactants.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | SI coordinate geometries | Gaussian 16 Rev. C.012; unrestricted B3LYP-D3(BJ) | 6-31G(d) for H/C/N/O and LANL2DZ for Cu; Cu model charge +2, doublet | optimized structures | ev_doc_5c0521c119d7_000182_1e64cfa0c6b4; ev_doc_5c0521c119d7_000184_31989d590cb7; ev_doc_5c0521c119d7_000186_c2897c9a671c; ev_doc_5c0521c119d7_000188_c8f366789fd3 |
| 2 | Verify stationary-point character and obtain thermal corrections | optimized structures | Gaussian harmonic frequencies at the optimization level | minima have no imaginary modes; TS have one imaginary mode | frequency corrections and assignment | ev_doc_5c0521c119d7_000188_c8f366789fd3 |
| 3 | Refine energies in solvent | optimized structures | Gaussian single points, M06/SMD(DMSO) | 6-311+G(d,p) for H/C/N/O and LANL2DZ for Cu | E_sol | ev_doc_5c0521c119d7_000189_1a11171e547b; ev_doc_5c0521c119d7_000190_88c54e48a49d |
| 4 | Build free-energy profile | E_sol and frequency corrections | arithmetic post-processing | G_sol = E_sol + frequency-derived correction; relative energies in kcal mol−1 | catalyzed and uncatalyzed barriers | ev_doc_5c0521c119d7_000199_9af3eee5ff12; ev_doc_5c0521c119d7_000202_277d9a271af8 |

## 4. Validation and analysis protocol

The authors compare the highest transition state reached from the relevant reactant reference in each pathway. Cat-TS2 is the rate-determining catalyzed step; Uncat-TS1 is the uncatalyzed concerted transition state. Figure S10 supplies optimized structures and selected distances, and Figure S11 reports a linear scan for the subsequent Cat-IM3 fragmentation, for which no separate transition state was found.

## 5. Private reference results

The main text reports a catalyzed key barrier of 31.7 kcal mol−1 and an uncatalyzed concerted barrier of 34.8 kcal mol−1. The catalyzed pathway is described as stepwise and energetically favored; Cu coordination to DCC and Lewis-acid activation are identified as the origin of the reduction. The first catalyzed transition state is reported at 20.9 kcal mol−1, while the alternative catalyst-pre-bound-to-quinoline route has a 35.3 kcal mol−1 transition state.

## 6. Limitations and interpretation boundaries

These are model-cluster results, not a periodic calculation on the full MOF. Relative free energies depend on conformer choice, charge/spin treatment, standard-state conventions and the chosen electronic-structure model. The evaluator therefore scores the explicitly defined barrier observables and stationary-point validation, and does not treat a different but documented model chemistry as automatically scientifically invalid.
