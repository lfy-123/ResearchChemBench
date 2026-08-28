# Private paper route

## 1. Scientific objective and author claim

The paper develops sulfide HAT catalysts under visible-light photoredox conditions. Its computational claim is that 2-thiazolyl substitution redirects HAT from weak S–H formation to stronger N–H formation. A hydrocarbon benchmark is needed to interpret whether an N–H BDE is thermodynamically competitive with abstraction from a typical C–H bond.

## 2. System and model boundary

The authors computed radical cations and protonated cations of sulfides, with an explicit BF4− counterion, using DFT and dichloromethane solvation. Table S2 also contains a cyclohexyl radical/cyclohexane pair used as the hydrocarbon reference. The reference bond is the C–H bond formed by adding an H atom to cyclohexyl radical; all quantities are gas-phase molecular enthalpies corrected consistently within the reported calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate stationary structures | sulfide radical cations and protonated cations; explicit BF4− | Gaussian 16 DFT geometry optimization | B3LYP+D3/cc-pVTZ; SMD dichloromethane | optimized geometries | ev_doc_f0efae9992d2_000112_191474afd4d8 |
| 2 | Obtain thermochemical quantities | optimized structures | Gaussian 16 | same model/solvent; enthalpies from optimized species | enthalpies for radical/cation pairs and H atom | ev_doc_f0efae9992d2_000112_191474afd4d8; ev_doc_f0efae9992d2_000113_3f009c667408 |
| 3 | Evaluate X–H BDE | enthalpies of X-centered radical, X–H cation and H atom | algebraic thermochemical cycle | Δ(X+H−XH) | BDEs for S–H and N–H | ev_doc_f0efae9992d2_000113_3f009c667408 |
| 4 | Compare with hydrocarbon reference | cyclohexyl radical and cyclohexane enthalpies | same level of theory | C–H BDE from radical + H − closed-shell hydrocarbon | reference for exergonicity interpretation | ev_doc_f0efae9992d2_000113_3f009c667408 |

## 4. Validation and analysis protocol

The authors compare weak S–H BDEs with typical alcohol, aldehyde, ether and hydrocarbon C–H BDEs, and compare N–H BDEs with cyclohexane computed at the same level. They additionally inspect the S12 precursor radical SOMO; negligible amplitude at pyridine nitrogen is used to favor the thiazole nitrogen as reactive site. The energetic comparison is interpreted together with the paper's fluorescence-quenching and deuterium-labeling evidence for radical-cation HAT.

## 5. Private reference results

Table S2 reports cyclohexyl radical and cyclohexane enthalpies and a C–H BDE of 96.54 kcal/mol. It reports S12 S–H and N–H BDEs of 73.57, 100.40 and 104.85 kcal/mol, respectively. The paper summarizes these as 73.6, 100.4 and 104.9 kcal/mol and states that N-centered HAT is mildly exergonic relative to cyclohexane.

## 6. Limitations and interpretation boundaries

The benchmark does not establish a reaction barrier or rate, and a BDE comparison alone does not prove the full photoredox mechanism. Results depend on conformer coverage, spin treatment, thermal conventions and the chosen electronic-structure model. The public task therefore requires reporting method choices, stationary-point validation and limitations rather than treating agreement with one number as mechanistic proof.
