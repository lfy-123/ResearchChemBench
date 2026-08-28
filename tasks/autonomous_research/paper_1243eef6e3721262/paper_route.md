# Private paper route

## 1. Scientific objective and author claim

The paper asks whether interpenetration is thermodynamically favored in pillar-layered Co6 MOFs. For HIAM-234b (Co6-bub-bpy), the authors claim that the experimentally observed two-fold interpenetrated (2IP) framework is stabilized relative to a hypothetical non-interpenetrated (NIP) framework.

## 2. System and model boundary

The system is solvent-free HIAM-234b, a tfz framework built from Co6(μ3-OH)6 clusters, the bub tricarboxylate linker and bpy pillars. The comparison uses periodic crystal models with the crystallographic cell fixed and atomic coordinates optimized. The NIP model is the one-net counterpart of the deposited 2IP structure.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build solvent-free models | HIAM-234b crystal and one-net counterpart | Periodic model construction | CCDC 2478962; retain the reported cell; remove one net for NIP | 2IP and NIP coordinates | ev_doc_85a918476c86_000002_20c178c1dd56; ev_doc_660b7fb47649_000117_aa04ee32860f |
| 2 | Relax atoms at fixed cell | Both coordinate models | CP2K Quickstep periodic DFT | spin-polarized PBE, GPW, DZVP, GTH, 400 Ry, Γ point, P1; force 9×10^-4 au and geometry change 6×10^-3 au | optimized coordinates | ev_doc_85a918476c86_000087_af3a16d73914; ev_doc_85a918476c86_000088_c8b347d7d66e; ev_doc_85a918476c86_000089_39c697b5d45d; ev_doc_85a918476c86_000090_9ba21d8c04c3; ev_doc_85a918476c86_000091_6f31285fa58a |
| 3 | Obtain energies | Optimized models | Single-point periodic DFT in the same CP2K setup | same basis, cutoff, pseudopotentials and Γ sampling | total energies | ev_doc_85a918476c86_000087_af3a16d73914 |
| 4 | Normalize and compare | Total energies and net counts | ΔE = E(2IP)/2 − E(NIP)/1 | kcal mol−1 per net | stabilization of 2IP relative to NIP | ev_doc_660b7fb47649_000154_4588b474407d |

## 4. Validation and analysis protocol

The authors compare solvent-free simulated structures with experimentally obtained structures and normalize the total energy by the number of nets. Structural optimization changes atomic coordinates only; cell parameters remain fixed. Their interpretation is an intrinsic framework-energy comparison, not a complete prediction of crystallization probabilities.

## 5. Private reference results

For HIAM-234b, the paper reports an energy stabilization of 188.3 kcal mol−1 for 2IP relative to NIP (Figure 4a and associated text). The expected conclusion is that the 2IP model is lower in normalized energy and that the calculation supports a thermodynamic advantage for interpenetration.

## 6. Limitations and interpretation boundaries

The calculation uses solvent-free models and therefore does not include guest, solvent, entropy or kinetic effects. It supports an intrinsic energetic trend, not a complete probability-of-formation model. Alternative reasonable electronic-structure choices may shift the numerical value; the evaluator therefore checks the reported sign, normalization and source-consistent magnitude with an authored tolerance.
