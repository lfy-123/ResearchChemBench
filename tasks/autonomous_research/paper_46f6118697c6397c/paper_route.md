# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to explain how boron substituents tune the N6-centred pi system and UV-vis absorption of boron-bridged hexazenes. For compound 1 (the previously reported tolyl-substituted B2N6 compound), the authors claim that the visible absorption is predominantly a HOMO-LUMO excitation.

## 2. System and model boundary

The target is neutral compound 1, a boron-bridged hexazene with two boron atoms, a conjugated six-nitrogen framework and tolyl groups on boron. The requested calculation is the isolated molecular electronic structure in dichloromethane represented by a continuum solvation model; crystal packing, vibronic structure, emission, and electrochemistry are outside the scored endpoint.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax the ground-state structure | Compound 1 geometry | Gaussian 16 geometry optimization | B3LYP; 6-31+G(d); SMD dichloromethane; DFT-D3BJ | Optimized ground-state geometry | ev_doc_5eb0affa079c_000117_00e0873d52bb; ev_doc_ced2213a1270_000127_7b0ffcdbe341 |
| 2 | Estimate the UV-vis spectrum | Optimized geometry from step 1 | Gaussian 16 TD-DFT single point | Same B3LYP/6-31+G(d), SMD(dichloromethane), DFT-D3BJ model | Singlet excitation energies, wavelengths and oscillator strengths | ev_doc_5eb0affa079c_000117_00e0873d52bb; ev_doc_ced2213a1270_000127_7b0ffcdbe341 |
| 3 | Identify the dominant visible transition | TD-DFT state list | Inspection of state energies, oscillator strengths and orbital assignments | Dominant state is the strong visible absorption; authors discuss HOMO-LUMO character | Dominant excitation and qualitative orbital assignment | ev_doc_5eb0affa079c_000119_e84fb1c9ec64; ev_doc_5eb0affa079c_000120_1cc9e6f995dd; ev_doc_ced2213a1270_000133_97a25df0559c; ev_doc_ced2213a1270_000134_06926d150144 |

## 4. Validation and analysis protocol

The authors' workflow requires a converged ground-state optimization before TD-DFT. A defensible independent implementation should report the optimization termination and, where performed, a frequency/Hessian sanity check; it should list enough low-lying singlet states to establish which state carries the dominant visible oscillator strength and provide the principal orbital-transition character. The paper's qualitative interpretation is that compound 1 has an N6-pi-dominated HOMO with some B-C sigma contribution and an N6-centred pi-star LUMO.

## 5. Private reference results

The SI Table S2 reports for compound 1's first singlet state 3.0119 eV, 411.64 nm and f=0.3456, with a dominant 173 -> 174 contribution of 0.69626. The main article rounds the corresponding dominant visible absorption energy to 3.52 eV while discussing the comparative orbital picture; the SI state table is the machine-readable reference used for this task. The source-reported state is singlet-A and has <S**2>=0.000.

## 6. Limitations and interpretation boundaries

The paper does not provide a ready-to-use Cartesian input for compound 1 in the supplied SI; its crystallographic identity is tied to CCDC 2512981 in the paper/SI context, so the released task uses that controlled record identifier. Differences from crystal packing, conformer choice, integration/convergence settings, number of TD states, and software implementations should be reported as limitations rather than treated as evidence of a different chemical identity. The rounded main-text energy and the detailed SI state energy are not conflated.
