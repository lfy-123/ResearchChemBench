# Private paper route

## 1. Scientific objective and author claim

The paper studies 7-azaindole (AI) dimerization in trihexyltetradecylphosphonium ionic liquids and uses quantum-chemical AI–anion interaction energies to rationalize anion-dependent dimerization. The authors claim that AI–[OTf]−, AI–[BF4]−, and AI–Br− interactions are close to the AI dimer interaction, whereas AI–[NF2]−, AI–[NTf2]−, AI–[NNf2]−, and AI–[DCA]− are less negative.

## 2. System and model boundary

The computational boundary is gas-phase isolated AI, AI2, the seven isolated anions [NF2]−, [NTf2]−, [NNf2]−, [OTf]−, [BF4]−, [DCA]−, Br−, and their corresponding AI–anion complexes. The reported observable is the counterpoise-corrected interaction energy in kcal mol−1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain equilibrium geometries | anions, AI monomer, AI dimer, AI–anion clusters | Gaussian 16 | ωB97XD/6-311++G(d,p) | optimized structures | ev_doc_0c327d609e77_000124_850f985ab047 |
| 2 | Obtain atomic charges | optimized anions, AI monomer and dimer | Gaussian 16 NBO 3.1 | natural bond population analysis | natural charges | ev_doc_0c327d609e77_000036_4d77a8212e0e; ev_doc_af1fdc01300f_000202_39265e6bde53 |
| 3 | Quantify association | optimized AI–anion clusters and AI dimer | Gaussian 16 | Boys–Bernardi counterpoise correction | interaction energies | ev_doc_0c327d609e77_000124_850f985ab047; ev_doc_0c327d609e77_000515_6d1c596395f0 |
| 4 | Compare association strengths | energies from step 3 | authors' analysis | compare anion complexes with AI2 | anion-dependent interpretation | ev_doc_0c327d609e77_000362_753bda1c2257; ev_doc_0c327d609e77_000399_ef03aa13b124 |

## 4. Validation and analysis protocol

The authors inspect optimized cluster geometries (Fig. 9), calculate counterpoise-corrected interaction energies, and compare them with the AI dimer value. Their qualitative interpretation is that the three OTf/BF4/Br complexes are close to AI2 and the remaining four anion complexes are less negative. Br− is excluded from the K-versus-energy fit because its NMR-derived K is unavailable.

## 5. Private reference results

Table 5 values (kcal mol−1): AI–[NF2]− −13.13; AI–[NTf2]− −13.60; AI–[NNf2]− −14.18; AI–[OTf]− −17.54; AI–[BF4]− −17.42; AI–[DCA]− −14.94; AI–Br− −18.25; AI–AI −17.98.

## 6. Limitations and interpretation boundaries

These are isolated-cluster electronic interaction energies, not solution free energies or dimerization constants. The paper does not establish uniqueness of every conformer, and the evaluator therefore requires explicit conformer search/coverage reporting and treats alternative validated conformers as a limitation rather than silently equating them with the authors' structure.
