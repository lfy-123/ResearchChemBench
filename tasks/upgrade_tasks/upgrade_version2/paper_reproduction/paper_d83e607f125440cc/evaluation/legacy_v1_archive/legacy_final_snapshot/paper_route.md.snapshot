# Private paper route

## 1. Scientific objective and author claim

The paper studies chemoselective oxidation of benzylic alcohols by an electrophotocatalytic flavinium system. For the methylsulfanyl substrate, the authors claim that the radical cation has unusually large spin/electron density on sulfur and that benzylic C–H abstraction is thermodynamically more difficult than for the methoxy analogue; these features are offered as a qualitative explanation for the low aldehyde yield.

## 2. System and model boundary

The computational system is isolated 4-(methylsulfanyl)benzyl alcohol radical cation (20 atoms, charge +1, doublet) in the gas phase, with a comparison to 4-methoxybenzyl alcohol radical cation for the BDE trend. The observables are Hirshfeld spin density on sulfur, vibrational minimum character, and B3LYP electronic benzylic C–H BDEs in kJ mol−1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize radical-cation structures | Cartesian structures in SI S7 | Gaussian 16 | B3LYP/6-311+G(d), vacuum, charge +1, multiplicity 2 | optimized geometry | ev_doc_deac309c9c26_000415_19e74dcba886; ev_doc_deac309c9c26_000428_c2ead0b3aa65 |
| 2 | Verify minima | optimized geometry | Gaussian 16 frequency calculation | no imaginary frequencies expected for a minimum | vibrational frequencies | ev_doc_deac309c9c26_000415_19e74dcba886; ev_doc_deac309c9c26_000422_5c66f2f9a0c1 |
| 3 | Quantify localization | optimized 2g•+ | Gaussian 16 Hirshfeld population analysis; MaSK visualization | spin-density isosurface 0.025 for visualization | sulfur and para-carbon Hirshfeld spin densities | ev_doc_deac309c9c26_000416_d71ba7ff8344; ev_doc_deac309c9c26_000413_ef8d2ac4f1e2 |
| 4 | Compute C–H dissociation energetics | optimized radical-cation and fragments | B3LYP electronic-energy differences in vacuum (the SI HF energy label is not a Hartree–Fock method specification) | benzylic C–H bond; report kJ mol−1 | BDE for 2g and comparison 2a | ev_doc_deac309c9c26_000426_681e8001fc15 |

## 4. Validation and analysis protocol

The optimized radical cation must be a stationary minimum by vibrational analysis. The sulfur atom is the unique S atom in the public structure and the benzylic C–H bond is the C–H bond at the CH2OH substituent. The localization result is interpreted together with the BDE comparison and the experimentally reported low yield for the methylsulfanyl derivative. The numerical reference values are used only in the private evaluator.

## 5. Private reference results

SI Table S8 reports sulfur-neighboring-atom/group spin density 0.401 for 2g•+ and para-carbon spin density 0.115. SI Table S16 reports 198.5 kJ mol−1 for 2g and 173.7 kJ mol−1 for 2a. SI Table S10 reports zero imaginary frequencies for both relevant radical cations. The main text reports relatively low aldehyde yield for 2g and proposes sulfur oxidation/less favorable H elimination as qualitative explanations.

## 6. Limitations and interpretation boundaries

The benchmark tests the reported gas-phase electronic-structure descriptors, not a complete reaction free-energy surface or product-yield prediction. Population analyses and BDEs depend on method, geometry, and fragmentation conventions; deviations should be discussed. A calculation that does not reproduce the exact author protocol can still be scientifically useful if its model and validation are clearly disclosed, but the evaluator's numeric references are tied to the SI definitions.
