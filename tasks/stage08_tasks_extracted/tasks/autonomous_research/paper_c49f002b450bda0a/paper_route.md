# Private paper route

## 1. Scientific objective and author claim

The authors used quantum chemistry to compare the free energies of the four stereoisomeric 2-azidocyclohexan-1-ol products that can formally arise from azide opening of cyclohexene oxide: (1R,2R), (1S,2S), (1S,2R), and (1R,2S). Their claim is that the mixed-configuration products, (1S,2R) and (1R,2S), are thermodynamically less stable than the RR/SS pair, supporting their exclusion from the stereochemical analysis of enzyme-controlled attack.

## 2. System and model boundary

The modeled chemical objects are neutral, closed-shell 2-azidocyclohexan-1-ol stereoisomers in hydrated/aqueous conditions. The comparison concerns product-state free energies and does not calculate enzyme-bound transition states, reaction barriers, rates, or mutant-specific enantioselectivity. The paper describes a “hydrated cluster” with SMD but does not specify the number or placement of explicit water molecules in the preserved text, so that aspect is not reproducible exactly from the snapshot.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define the stereochemical comparison | Four product stereoisomers: (1R,2R), (1S,2S), (1S,2R), (1R,2S) | Structure construction (implementation details not reported) | Neutral product states; described as hydrated clusters in SMD | Four initial stereochemical models | Main paper §4.9, `ev_doc_93bdceea3cb5_000235_94363255a28e` |
| 2 | Locate equilibrium geometries | Four hydrated product models | ORCA 4.2.1; B3LYP/6-31G(d,p) | SMD continuum solvation; aqueous/hydrated model | Optimized geometries | Main paper §4.9, `ev_doc_93bdceea3cb5_000235_94363255a28e` |
| 3 | Validate stationary points and obtain corrections | Optimized geometries | Harmonic frequency calculations at the optimization level | Zero-point, thermal, and entropic corrections; text states validation of minima/saddle points but is editorially damaged | Stationary-point classification and free-energy corrections | Main paper §4.9, `ev_doc_93bdceea3cb5_000235_94363255a28e` |
| 4 | Refine relative energies | Optimized models plus thermal corrections | M06-2X/def2-TZVP single-point treatment in the stated solvated model | Relative free energies reported in kcal/mol | Four-state relative-free-energy comparison | Main paper §4.9 and SI Figure S10 caption, `ev_doc_93bdceea3cb5_000235_94363255a28e`, `ev_doc_39335fd059e6_000013_30b54d5a5cd3` |
| 5 | Interpret stereochemical accessibility | Relative free energies | Qualitative thermodynamic comparison | Compare mixed configurations against RR/SS products | Exclusion of higher-energy (1S,2R)/(1R,2S) products on thermodynamic grounds | Main paper mechanistic discussion, `ev_doc_93bdceea3cb5_000061_86cebd898f14` |

## 4. Validation and analysis protocol

The reported workflow optimized all four products and performed harmonic frequency calculations to classify stationary points and estimate zero-point, thermal, and entropic corrections. Relative free energies were then calculated at a higher-level electronic-structure treatment. The scientifically relevant analysis is the four-isomer ordering, especially whether both mixed configurations lie above the RR/SS pair. The paper does not report conformer-generation details, conformer counts, standard-state convention, temperature, explicit-water count, or method-sensitivity tests in the preserved evidence.

## 5. Private reference results

The current-paper claim is that (1R,2S) and (1S,2R) are the two higher-energy, unstable diastereomeric configurations and that the QM free-energy comparison supports their thermodynamic exclusion. SI Figure S10 is explicitly captioned as M06-2X/def2-TZVP relative free energies in kcal/mol for the four chiral isomers. The embedded figure values are absent from the immutable normalized SI snapshot, so no exact numeric targets are asserted or scored.

## 6. Limitations and interpretation boundaries

Product thermodynamic ordering alone does not establish enzyme-bound kinetics, transition-state selectivity, or the absolute product ratio. Enantiomers should be degenerate in an achiral idealized environment; deviations can reflect conformer sampling, numerical noise, or an incompletely specified hydrated cluster. The authors' explicit-water model cannot be reconstructed uniquely from the snapshot. The benchmark therefore permits an independently chosen, documented aqueous free-energy model and evaluates robust grouping/order plus validation, while requiring limitations and method sensitivity to be reported.
