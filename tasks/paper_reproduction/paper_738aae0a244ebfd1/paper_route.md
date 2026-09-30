# Private paper route

## 1. Scientific objective and author claim

The paper uses gas-phase quantum chemistry to characterize bis(2-ammonium-2-methyl-1-propanol) trifluoroacetate (AMP-TFA). Its computational claim is that the optimized ion-pair structure is electronically stable and has a UV absorption dominated by a frontier-orbital excitation. The reported observables are a positive-minimum vibrational check, the HOMO/LUMO energies and gap, and the first listed TD-DFT excitation and a separate intensity comparison.

## 2. System and model boundary

The author-calculated model in Figure 2b is a neutral cluster of two AMP cations and two trifluoroacetate anions, formula C12H24F6N2O6, singlet, 50 atoms and 212 electrons (main p4). C6H12F3NO3 is one formula unit, not the whole calculated cluster. The crystal is triclinic P-1 and the 100 K structure is the authors' starting geometry; the supplied SI identifies datablock A545_100 and reports two formula units per asymmetric unit. The gas-phase calculation treats the isolated bis-ion-pair cluster, not the periodic crystal or a solvent.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the ion-pair geometry | X-ray AMP-TFA geometry | Gaussian16 DFT | B3LYP/6-311++G(d,p), neutral singlet, gas phase | optimized geometry | ev_doc_06793b118174_000078_c10a1061bf4e; ev_doc_06793b118174_000080_7e43b622a8c3 |
| 2 | Verify a stationary minimum and obtain vibrations | optimized geometry | Gaussian16 harmonic frequencies | same level, neutral singlet | frequencies and thermochemistry; no negative frequency reported | ev_doc_06793b118174_000080_7e43b622a8c3 |
| 3 | Compute electronic excitations | optimized geometry | Gaussian16 TD-DFT | B3LYP/6-311++G(d,p), gas phase | excitation wavelengths, oscillator strengths, orbital contributions | ev_doc_06793b118174_000331_ed7b7b652ec8; ev_doc_06793b118174_000332_a441ea1d9b8e |
| 4 | Analyze frontier orbitals and global descriptors | optimized geometry | Gaussian16 DFT output | same level | HOMO, LUMO, gap and reactivity descriptors | ev_doc_06793b118174_000349_41230c7eda75 |

## 4. Validation and analysis protocol

The authors state that the harmonic calculation has no negative frequency and call the resulting structure a global minimum. They inspect the HOMO/LUMO energies and discuss the first listed HOMO-to-LUMO UV transition. The claim that this state is strongest conflicts with Table 4: its f=0.0008 is below the second state f=0.0013. The task binds 271.84 nm to the first/lowest-energy listed singlet, not to the maximum-intensity state. The paper reports HOMO = -9.617 eV, LUMO = -3.608 eV, gap = 6.008 eV, and a HOMO-to-LUMO transition at 271.84 nm with 100% contribution and oscillator strength 0.0008. The article also reports dipole, polarizability, and hyperpolarizability, but these are outside the constructed benchmark's scored core.

## 5. Private reference results

The hidden reference gap is 6.008 eV. The hidden reference first/lowest-energy listed singlet is 271.84 nm, assigned as HOMO→LUMO and π→π* with 100% major contribution. The minimum-validation reference is zero imaginary frequencies. These values are sourced from the abstract, Section 3.4/Table 5, and Section 3.3/Table 4.

## 6. Limitations and interpretation boundaries

The article does not publish the coordinate-bearing CIF in the supplied SI, only its check report. The released task therefore uses a connectivity-complete ion-pair SMILES and permits the Agent to generate starting conformers; exact reproduction of the authors' crystal-derived orientation is not required. The benchmark evaluates the stated gas-phase observables and does not treat the reported gap as an experimental band gap or a periodic-solid property.


## 2026-09-23 factual definition correction

Main physical page 7, Section 3.3/Table 4 contradicts the abstract/conclusion wording that calls 271.84 nm the most intense transition. Both public task modes, result schema and evaluator now distinguish lowest excitation energy from maximum oscillator strength. Reference 271.84±10 nm and gap 6.008±0.5 eV are unchanged. This is not an author erratum, and it does not resolve the calculated gap mismatch or establish benchmark qualification.
