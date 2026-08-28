# Private paper route

## 1. Scientific objective and author claim

The paper characterizes the lowest singlet and triplet excitations of the cyclometalated Ir(III) arylacetylide complexes IrF2ppz/H and IrF2ppz/CN. The authors claim that phosphorescence is associated with a triplet state localized primarily on the acetylide ligand, rather than a conventional metal-to-ligand charge-transfer state.

## 2. System and model boundary

The computational systems are the neutral singlet complexes IrF2ppz/H and IrF2ppz/CN. The SI supplies optimized Cartesian geometries. The reported observables are vertical S0→S1 and S0→T1 excitation energies, frontier-orbital gaps, and dominant orbital-transition character. Singlet calculations use implicit dichloromethane when specified; triplet calculations are gas phase. The benchmark does not score emission spectra, rates, or crystal packing.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize S0 geometry | IrF2ppz/H and IrF2ppz/CN structures | Gaussian 16 Rev. C.01, ωB97X-D/def2-TZVPP | Neutral singlet; full geometry optimization | Optimized S0 geometry | ev_doc_0364be9e0d89_000399_a4d60d82f9ca; ev_doc_0364be9e0d89_000403_fb1333a400dc |
| 2 | Verify minimum | Optimized S0 geometry | Harmonic frequency analysis at same level | No imaginary frequencies reported | Minimum validation | ev_doc_0364be9e0d89_000403_fb1333a400dc |
| 3 | Compute singlet absorption | Optimized S0 geometry | TD-CAM-B3LYP/def2-TZVPP | 50 states; SMD(CH2Cl2) | S0→S1 energy and oscillator strength | ev_doc_0364be9e0d89_000407_e8c93b03a0ee; ev_doc_0364be9e0d89_000409_3f90461cffbe; ev_doc_0364be9e0d89_000410_bc363e9ebc1c; ev_doc_0364be9e0d89_000411_ab24a3f78e5c |
| 4 | Compute triplet excitation | Optimized S0 geometry | TD-CAM-B3LYP/def2-TZVPP | 50 states; gas phase | S0→T1 energy and orbital contributions | ev_doc_0364be9e0d89_000412_29d1c2a79779; ev_doc_0364be9e0d89_000413_6c06431a3f44 |
| 5 | Interpret state character | TD-DFT outputs and orbital plots | Orbital-transition analysis | Compare dominant configurations and ligand localization | Assignment of emissive-state character | ev_doc_0364be9e0d89_000303_d7cf41c09217; ev_doc_0364be9e0d89_000368_3686faf62ffa |

## 4. Validation and analysis protocol

A valid reproduction must identify the supplied geometry and charge/multiplicity, demonstrate a stationary minimum by frequency analysis, report the lowest requested singlet and triplet vertical excitations with their solvent boundaries, and retain orbital-transition evidence for the triplet assignment. Results are compared per complex and per observable; method, basis, solvation, state count, and any deviations are recorded. The authors' qualitative interpretation is evaluated independently of numerical agreement.

## 5. Private reference results

The paper reports S0→S1 peak/transition information for IrF2ppz/H and IrF2ppz/CN, and reports triplet results including 3.04 eV with HOMO→LUMO+3 (69.94%) for IrF2ppz/H and 2.70 eV with HOMO→LUMO (71.17%) for IrF2ppz/CN. The SMD frontier-orbital gaps are 4.457 eV (278 nm) and 3.999 eV (310 nm), respectively. The T1 orbitals are described as primarily acetylide-localized. These values remain private evaluator references.

## 6. Limitations and interpretation boundaries

The benchmark measures vertical electronic-structure observables, not relaxed excited-state energies or absolute photoluminescence. Agreement is method- and geometry-dependent. Orbital localization is a qualitative/partition-dependent interpretation, so the evaluator requires explicit orbital or population evidence and accepts a carefully justified equivalent analysis. Experimental emission is used only as context for the scientific claim, not as a computed target.
