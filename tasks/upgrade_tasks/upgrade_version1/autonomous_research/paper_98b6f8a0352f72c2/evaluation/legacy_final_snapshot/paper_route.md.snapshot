# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum chemistry to explain the photophysics of phenazine derivatives 12a–f. For the representative neutral closed-shell compound 12a, the author claim is that a ground-state DFT geometry followed by TD-DFT in chloroform gives a useful S1 absorption description and that the first transition has predominantly internal charge-transfer character with electron density delocalized over the phenazine framework. The computed quantities are S1 energy, wavelength, oscillator strength, transition dipole, and radiative lifetime.

## 2. System and model boundary

12a is 5-(4-(N,N-dimethylamino)phenyl)benzo[a]phenazine, formula C24H19N3, neutral singlet. The authors model an isolated molecule with a chloroform polarizable-continuum environment; no explicit solvent molecules, aggregates, counterions, thermal ensemble, or solid-state effects are included.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax ground-state structure | 3D geometry of each 12a–f molecule | ORCA 4.2 DFT | ωB97X-D3, def2-TZVP/def2-J, CPCM CHCl3, no symmetry constraint, charge 0, multiplicity 1 | Optimized ground-state geometry | ev_doc_100a35fc592f_000261_2781ecb61339; ev_doc_100a35fc592f_000207_342a52d7f97e |
| 2 | Obtain absorption states | Optimized geometry | ORCA 4.2 TD-DFT | Same functional, basis, auxiliary basis and CPCM CHCl3; 40 singlet states; Lorentz-fit theoretical spectrum | Excitation energies, oscillator strengths, transition dipoles and simulated spectrum | ev_doc_100a35fc592f_000261_2781ecb61339; ev_doc_100a35fc592f_000145_52f54bf06200 |
| 3 | Estimate radiative lifetime | Each calculated state’s energy and oscillator strength | Einstein oscillator-strength expression | τf = 1.4999/(f E²), with E in cm−1; values reported for five lowest states in each solvent | Radiative lifetime | ev_doc_100a35fc592f_000143_2d3b0e4050f9; ev_doc_100a35fc592f_000144_5a87d78ad9a7; ev_doc_36d3623749e7_000087_7b5e05cbbfe6 |
| 4 | Interpret excitation | TD-DFT orbitals | Natural transition orbital analysis | S1 and higher-energy transitions inspected visually | NTO assignment and localization | ev_doc_100a35fc592f_000108_113fd1bf4f7f; ev_doc_36d3623749e7_000042_207e74049d41 |

## 4. Validation and analysis protocol

The authors compare simulated UV–Vis spectra in CHCl3 with measured spectra and inspect NTOs for S1. They compare the computed S1 parameters across 12a–f and relate them to substituent-dependent absorption. The paper separately reports experimental fluorescence and radiative quantities in Table 1; those measurements are not the computational endpoint. The reported S1 values for 12a are energy 3.65 eV, wavelength 340.0 nm, oscillator strength 0.64, and transition dipole 3.65 D (Table 2). The task lifetime reference is derived from the same main-paper energy and oscillator strength using the printed Einstein relation, not quoted as an exact Table S1 value.

## 5. Private reference results

For 12a in CHCl3, Table 2 reports S1 energy 3.65 eV, wavelength 340.0 nm, oscillator strength 0.64, and dipole moment 3.65 D. The Einstein expression using those energy and oscillator-strength values gives a radiative lifetime of approximately 2.70 ns (derived from main PDF p.5 Table 2 and the equation below it; do not identify this rounded derived value as a literal SI Table S1 entry). The NTO discussion assigns the dominant S1 character to n→π* internal charge transfer from the aromatic amine toward the phenazine unit and describes delocalization over the phenazine skeleton. These values and interpretations are private evaluator references.

## 6. Limitations and interpretation boundaries

The paper does not establish a unique conformer protocol, grid, SCF convergence settings, or an uncertainty estimate. Initial conformers and implementation details can therefore change numerical results. Fair comparison should assess a reproducible calculation on the supplied connectivity and solvent boundary, report the actual method and convergence, and treat deviations as method/conformer sensitivity rather than experimental disagreement. The NTO assignment is qualitative and should not be inferred from oscillator strength alone.
