# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to explain the α-selectivity of Ni-catalyzed decarboxylative C(sp3)–Ge glycosylation. The authors claim that the glycosyl radical adds to a Ni(I) intermediate through two competing anomeric transition states and that the α pathway is kinetically preferred.

## 2. System and model boundary

The computational system is the glucosyl NHPI-ester/germylzinc/Ni complex model shown in the mechanistic study, with explicit nickel, ligand, glycosyl, germylzinc and counterion components. Energies are Gibbs free energies at 298.15 K; solvent is THF represented by SMD. The scored comparison is between the two anomeric radical-addition transition states and their activation barriers.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate candidate structures | Ground- and transition-state geometries, manual conformer search | Gaussian 16 Rev. C.01 | B3LYP-D3; SDD on Ni and 6-31G(d) on other atoms | Optimized geometries and frequencies | ev_doc_e0b94f1c82da_001500_4e2b13d93368; ev_doc_e0b94f1c82da_001507_2b9f14ae3305 |
| 2 | Refine electronic energies | Optimized structures | Gaussian 16 | B3LYP-M06/def2-TZVP with SMD(THF) | Solvated single-point energies | ev_doc_e0b94f1c82da_001508_a97658e0d1ca; ev_doc_e0b94f1c82da_001512_a80a23d27a53 |
| 3 | Obtain thermochemistry | Frequencies and single-point energies | GoodVibes 3.0.2 | 298.15 K | Gibbs free energies | ev_doc_e0b94f1c82da_001512_a80a23d27a53 |
| 4 | Compare anomeric pathways | ts2 and ts2′ relative to the common radical-addition reference | Energy-profile analysis | Activation barriers and ΔΔG‡ | Selectivity rationale | ev_doc_b95a0c72c190_000203_85b2c9fb197d; ev_doc_fe7fa69a95e3_000204_85b2c9fb197d |

## 4. Validation and analysis protocol

The authors manually searched conformers, optimized the reported stationary points, applied solvent single-point corrections and GoodVibes thermochemistry, and compared the two competing radical-addition barriers. The SI Data S1 contains labeled optimized structures; Figure S9 identifies the two anomeric transition states. The reported analysis places the α route lower than the β route and uses the barrier difference to rationalize the observed α-selectivity.

## 5. Private reference results

The source reports a 7.3 kcal/mol activation barrier for ts2, an 11.2 kcal/mol barrier for ts2′, and a 3.9 kcal/mol difference favoring ts2. The α pathway leads to int2T, which relaxes to the more stable int2S. The source also reports 3.8 kcal/mol for Ni(0)-initiated SET, −89.8 kcal/mol for the radical-generation step, 21.1 kcal/mol for transmetalation and 21.2 kcal/mol for C–Ge bond formation.

## 6. Limitations and interpretation boundaries

These values are model- and protocol-dependent free energies, not direct experimental observables. The task evaluates whether an independent computational investigation identifies and validates the competing anomeric transition states and reproduces the source-supported qualitative and quantitative comparison. Alternative defensible methods must report their model, convergence, stationary-point validation and uncertainty; failure to reproduce the exact author protocol is not itself a scientific failure.
