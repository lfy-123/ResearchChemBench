# Private paper route

> Packaging correction (2026-08-30): SI Table S1 assigns CCDC 2512981 to
> compound 2, and the supplied CIF formula C18H14B2F12N6O12S4 is consistent
> with that tetra(triflate) derivative. The earlier compound-1 task identity was
> wrong. The released task now uses the complete compound-2 CIF directly;
> database retrieval is not scored.

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to explain how substituents on boron tune the N6-centred pi system and UV-vis absorption of boron-bridged hexazenes. For compound 2, the tetra(triflate) derivative, the authors attribute the dominant calculated absorption to an N6-related transition whose occupied orbital is strongly stabilized relative to the frontier pair.

## 2. System and model boundary

The target is neutral compound 2, formula C18H14B2F12N6O12S4: a boron-bridged hexazene with two boron atoms, a conjugated six-nitrogen framework and four B-O-SO2CF3 substituents. The complete tetra(triflate) molecule must be retained. The requested calculation is the isolated molecular electronic structure in dichloromethane represented by a continuum solvation model; crystal packing, vibronic structure, emission, and electrochemistry are outside the scored endpoint.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax the ground-state structure | Complete compound 2 geometry | Gaussian 16 geometry optimization | B3LYP; 6-31+G(d); SMD dichloromethane; DFT-D3BJ | Optimized ground-state geometry | ev_doc_5eb0affa079c_000117_00e0873d52bb; ev_doc_ced2213a1270_000127_7b0ffcdbe341 |
| 2 | Estimate the UV-vis spectrum | Optimized geometry from step 1 | Gaussian 16 TD-DFT single point | Same B3LYP/6-31+G(d), SMD(dichloromethane), DFT-D3BJ model | Singlet excitation energies, wavelengths and oscillator strengths | ev_doc_5eb0affa079c_000117_00e0873d52bb; ev_doc_ced2213a1270_000127_7b0ffcdbe341 |
| 3 | Identify the dominant near-UV/visible transition | TD-DFT state list | Inspection of state energies, oscillator strengths and orbital assignments | Select the state carrying the dominant oscillator strength; authors assign it mainly as HOMO-4 to LUMO | Dominant excitation and qualitative orbital assignment | ev_doc_5eb0affa079c_000119_e84fb1c9ec64; ev_doc_5eb0affa079c_000120_1cc9e6f995dd; ev_doc_ced2213a1270_000133_97a25df0559c; ev_doc_ced2213a1270_000134_06926d150144 |

## 4. Validation and analysis protocol

The authors' workflow requires a converged ground-state optimization before TD-DFT. A defensible independent implementation should report the optimization termination and, where performed, a frequency/Hessian sanity check; it should list enough low-lying singlet states to establish which state carries the dominant near-UV/visible oscillator strength and provide the principal orbital-transition character. For compound 2, the paper's qualitative interpretation is that the electron-withdrawing triflate substituents stabilize the occupied N6-related orbitals, shifting the dominant configuration away from a simple HOMO-LUMO assignment.

## 5. Private reference results

SI Table S3 reports that compound 2's fifth singlet state carries the dominant oscillator strength: 3.8436 eV, 322.58 nm and f=0.4243, with a dominant 217 -> 222 contribution of 0.70241. This corresponds to the reported HOMO-4 -> LUMO assignment. The main article prints 4.33 eV together with 323 nm and f=0.4243; because 323 nm corresponds to about 3.84 eV, the main-text energy is internally inconsistent. The detailed SI state table (3.8436 eV) is therefore the numeric evaluator reference, while the discrepancy is retained as a source limitation.

## 6. Limitations and interpretation boundaries

The paper does not provide a ready-to-use Cartesian input for compound 2 in the supplied SI. The released task therefore includes the pinned CCDC 2512981 CIF rather than evaluating database access. The CIF may require deterministic symmetry/component and disorder handling, but all four covalently bound triflate substituents belong to the target and must not be discarded as counterions. Differences from crystal packing, disorder choice, conformer choice, integration/convergence settings, number of TD states, and software implementations should be reported as limitations. The inconsistent main-text energy and detailed SI state energy are not conflated.
