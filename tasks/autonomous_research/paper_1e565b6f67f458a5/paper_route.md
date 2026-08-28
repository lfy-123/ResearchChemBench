# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT thermochemistry to support a hydrogen-radical-mediated self-regeneration cycle for sulfhydryl sites on PEI/L-cysteine-modified rice straw (CPRS). In the authors' Reaction 3, a hydrogen radical cleaves an oxidized cystine disulfide linkage and regenerates thiol sites; the reported reaction Gibbs energy is −34.7 kcal/mol. This calculation is part of the explanation for high reusability.

## 2. System and model boundary

The molecular model is an L-cystine/disulfide motif (Int4) and the corresponding disulfide-cleavage transition structure (Ts3), with the hydrogen-radical-mediated reaction and the solution thermochemical convention used by the authors. The calculation is a molecular approximation to a surface process; the straw/PEI matrix, explicit solvent, counterions and periodic solid are not included in the DFT model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize molecular stationary points | Int4 cystine and Ts3 cleavage structure | Gaussian16 Rev. C.01 | PBE0/ma-SVP, DFT-D3(BJ), SMD | Optimized geometries and thermal corrections | ev_doc_0c418fd4e9b8_000005_7ea3114aff17; ev_doc_0c418fd4e9b8_000014_6fb0838d42fd |
| 2 | Refine electronic energies | Optimized structures | Gaussian16 | PBE0/ma-TZVP, DFT-D3(BJ), SMD | Single-point energies | ev_doc_0c418fd4e9b8_000005_7ea3114aff17 |
| 3 | Assemble standard Gibbs energies | Thermal corrections and refined energies | Authors' thermochemical assembly | Gs = Gcorr(ma-SVP) + E(ma-TZVP) + Gstd; Gstd = 1.89 kcal/mol | Gs for each state | ev_doc_0c418fd4e9b8_000005_7ea3114aff17 |
| 4 | Evaluate Reaction 3 | State free energies and hydrogen/proton convention | Reaction free-energy cycle | Authors report absolute solvation energies H+ = −265.9 and OH− = −105.0 kcal/mol | ΔG for disulfide regeneration | ev_doc_0c418fd4e9b8_000005_7ea3114aff17; ev_doc_8493e1ded013_000230_6c0862f8a095; ev_doc_8493e1ded013_000231_a524ce9c43e9 |

## 4. Validation and analysis protocol

The authors' figure identifies Int4 as cystine and Ts3 as the cystine state undergoing disulfide breaking. A defensible implementation verifies optimization convergence, confirms Int4 is a minimum, and characterizes Ts3 as the intended first-order saddle (one imaginary mode along the S–S cleavage coordinate). The reported thermochemical result is compared with the main-text Reaction 3 value. Interpretation is limited to the molecular model and standard-state convention.

## 5. Private reference results

The main text reports Reaction 3 ΔG = −34.7 kcal/mol. The paper describes it as spontaneous and as supporting regeneration of C–SH sites; the authors also report 92.2% initial performance retained after ten adsorption–desorption cycles. Other reaction values in the mechanism are −21.8 (Reaction 1), −47.7 (Reaction 2), −6.0 (Reaction 6), and −2.8 kcal/mol (Reaction 7), but they are not targets of this task.

## 6. Limitations and interpretation boundaries

The paper does not provide machine-readable Cartesian coordinates for Int4/Ts3 in the supplied SI. The released task therefore supplies the unambiguous L-cystine connectivity and requires independent conformer/transition-state construction. The reported value is a hidden reference, not a precision claim for all methods; submissions must disclose model choices and uncertainty. A transition-state search may fail or locate a different chemically justified stationary point, so bounded failure and limitations are reportable.
