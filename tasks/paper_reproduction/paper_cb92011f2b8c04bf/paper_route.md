# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to test where the unpaired electron is localized in the neutral doublet syringol phenoxy radical (2,6-dimethoxyphenoxy radical). The authors claim that the para ring carbon, C4, carries the dominant spin population, rationalizing selective C4–C4′ radical coupling to the observed diphenoquinone dimer; O1 is also relatively spin-rich, while C2/C6 are disfavored by methoxy substitution and steric hindrance.

## 2. System and model boundary

The computed object is an isolated, gas-phase neutral open-shell C8H9O3 radical in its lowest relevant doublet state. The aromatic ring is numbered O1 (phenoxy oxygen), C2 and C6 (the two symmetry-equivalent methoxy-bearing ortho carbons), C4 (para carbon), with two methoxy substituents at C2/C6. The calculation concerns electronic spin localization, not a full enzyme, solvent, coupling transition state, product optimization, or electrochemical capture model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax radical geometry | Syringol phenoxy radical | Gaussian 16 DFT geometry optimization | M06-2X; 6-31+G(2d,2p); ultrafine grid; `NoSymm`; extended quadratic convergence; neutral doublet | Optimized open-shell geometry/wavefunction | ev_doc_8804d0ee1b74_000504_4b8b01e7c630 |
| 2 | Quantify unpaired-electron localization | Optimized geometry and wavefunction | Multiwfn spin-density analysis and atomic population analysis | Spin density is alpha minus beta density; inspect O1, C2/C6 and C4 | Atomic spin populations and spin-density representation | ev_doc_8804d0ee1b74_000508_6356ddd6a5a2; ev_doc_8804d0ee1b74_000106_6f9c6f4353b9 |
| 3 | Test regioselectivity interpretation | Population table | Comparison of site populations with chemical site identities | Identify largest site and compare symmetry-equivalent C2/C6 | Dominant radical site and mechanistic interpretation | ev_doc_8804d0ee1b74_000106_6f9c6f4353b9; ev_doc_8804d0ee1b74_000107_0119645d225a |

## 4. Validation and analysis protocol

The paper describes full optimization before population analysis and disables symmetry constraints to avoid bias in spin localization. A defensible reproduction should document SCF and geometry convergence, confirm the optimized structure is a stationary minimum (or report the chosen alternative validation), preserve atom identities through optimization, and report the population-analysis convention. Interpretation is limited to the isolated-radical model: population rankings are evidence relevant to, but not a direct calculation of, a bimolecular coupling rate or barrier.

## 5. Private reference results

The source text states that C4 is the predominant spin-localization site and that O1 also has relatively high spin density; C2 and C6 are alternative ortho sites whose participation is suppressed in the authors' interpretation. Figure 1C contains the numerical populations, but the normalized evidence text does not expose reliable exact values. The evaluator therefore uses source-backed ordering/semantic conclusions rather than fabricated numerical targets.

## 6. Limitations and interpretation boundaries

Atomic spin populations depend on population scheme, geometry, functional and basis. The radical calculation omits enzyme environment, solvent, dimer encounter orientation, and explicit coupling kinetics. Symmetry-equivalent C2/C6 should agree within the agent's reported numerical/optimization uncertainty; substantial inequivalence requires explanation. The paper's product characterization is experimental corroboration, not a hidden computational observable.
