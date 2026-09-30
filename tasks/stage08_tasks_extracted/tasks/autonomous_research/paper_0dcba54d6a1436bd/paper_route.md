# Private paper route

## 1. Scientific objective and author claim
The paper uses computation to rationalize acceptor-dependent photophysics in carbazole–cyanostilbene emitters. It claims that separated frontier orbitals and TD-DFT transitions support ICT for NPCZCS and AQCZCS and that M06/6-31G(d,p)/PCM(DCM) is the best benchmarked functional.

## 2. System and model boundary
Neutral closed-shell NPCZCS and AQCZCS monomers in the gas-phase optimized ground state, followed by vertical singlet excitations in dichloromethane PCM. No aggregates, vibronic structure, or solid-state packing are part of the computational target.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Ground-state geometry | NPCZCS and AQCZCS Cartesian structures | Gaussian 09W DFT | B3LYP/6-31G(d,p), no symmetry constraints, neutral singlet | optimized minima | ev_doc_d911feeb2792_000101_5e5f9f8b1b6; ev_doc_7b7d744c61ea_000135_d0e098c6d1e0 |
| 2 | Minimum validation | optimized structures | harmonic frequencies | absence of imaginary frequencies | confirmed minima | ev_doc_7b7d744c61ea_000135_d0e098c6d1e0 |
| 3 | Functional benchmark | optimized NPCZCS/AQCZCS | TD-DFT Gaussian 09W | six functionals with 6-31G(d,p)/PCM(DCM) | absorption wavelength and oscillator strength comparison | ev_doc_7b7d744c61ea_000138_abea0b27f941; ev_doc_d911feeb2792_000205_f74a1f8cf43d |
| 4 | Production excited states | optimized structures | TD-DFT | M06/6-31G(d,p)/PCM(DCM), neutral singlet | singlet transitions, f values, orbital configurations | ev_doc_d911feeb2792_000212_75db7cf57992; ev_doc_d911feeb2792_000214_d9bc23006b37 |
| 5 | Electronic interpretation | production states | FMO/NTO analysis | hole/particle localization | ICT versus LE interpretation | ev_doc_7b7d744c61ea_000148_fafedce25020 |

## 4. Validation and analysis protocol
The paper compares computed absorption features with experimental spectra, checks that optimized structures are minima, and interprets the leading S1 transition using frontier orbitals and NTOs. The benchmark tables report the lowest five singlet states for each of NPCZCS and AQCZCS.

## 5. Private reference results
NPCZCS S1–S5: 2.9521/419.99/0.4988, 3.2985/375.88/0.8847, 3.3637/368.59/0.2256, 3.6504/339.65/0.0656, 3.7792/328.07/0.1233 (eV/nm/f). AQCZCS S1–S5: 2.5853/479.58/0.1928, 3.0280/409.45/0.0832, 3.1077/398.96/0.0041, 3.2424/382.38/1.0178, 3.3895/365.79/0.0006. Dominant configurations and qualitative NTO conclusions are given in SI Tables S7–S8 and main-text Figure 5 discussion.

## 6. Limitations and interpretation boundaries
These are vertical single-molecule TD-DFT values and should not be treated as relaxed emission energies, solid-state spectra, or unique mechanistic proof. Differences from the reference can arise from geometry, state ordering, numerical settings, and software implementation.
