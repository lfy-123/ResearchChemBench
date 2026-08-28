# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to test whether push-pull substitution on 9,10-bis(triphenylaminophenylethynyl)anthracene annihilators tunes the singlet excited state while leaving the triplet state nearly unchanged, supporting solvent-tunable TTA upconversion. The qualitative interpretation is peripheral donor/acceptor control of relaxed LE/CT character with a relatively anthracene-centered triplet.

## 2. System and model boundary

The systems are neutral singlet TPAAN-OMe (C58H44N2O4), TPAAN-H (C54H36N2), and TPAAN-CHO (C56H36N2O2), in implicit n-hexane and chloroform. The supplied Cartesian geometries are the authors' S0 structures; no explicit solvent molecules or sensitizer are included. Requested electronic quantities are relaxed S1->S0 emission energies and S0-geometry S0->T1 energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground and singlet excited geometries | TPAAN structures | Gaussian09 DFT | wB97XD/def2-SVP, SMD, each solvent, neutral singlet | optimized S0 and S1 geometries | ev_doc_3cd8ad8692a2_000172_8d0ddbbde8dd |
| 2 | Compute relaxed singlet transition | optimized S1 geometry | Gaussian09 TD-DFT | wB97XD/def2-SVP/SMD; S1->S0 | S1 energy and oscillator strength | ev_doc_3cd8ad8692a2_000239_a3cc16fd690e |
| 3 | Compute triplet transition | optimized S0 geometry | Gaussian09 TD-DFT | wB97XD/def2-SVP/SMD; S0->T1, no spin-orbit coupling | T1 energy, zero oscillator strength | ev_doc_3cd8ad8692a2_000239_a3cc16fd690e |
| 4 | Compare substituent and solvent effects | calculated transitions | tabulation/trend analysis | compare six compound-solvent cases | tuning of S1 and stability of T1 | ev_doc_e6c2c7f8c32e_000033_2e9348150554 |

## 4. Validation and analysis protocol

The authors select low-lying transitions and report oscillator strengths and dominant H->L character in SI Table S1. They compare the six S1 values and six T1 values across substituents and solvents, and use the resulting state picture with transient absorption and solvatochromic emission analysis. The computational claim is limited to this implicit-solvent TD-DFT model and these geometries.

## 5. Private reference results

SI Table S1 reports S1->S0 energies (eV): OMe 2.16 (hexane), 2.11 (chloroform); CHO 2.18, 2.14; H 2.20, 2.16. S0->T1 energies are OMe 1.27/1.27, CHO 1.27/1.28, and H 1.27/1.27 eV (hexane/chloroform). The corresponding S1 oscillator strengths are 1.7955, 1.7554, 1.6746, 1.7143, 1.6843, and 1.7121 in the same table order.

## 6. Limitations and interpretation boundaries

These are vertical/relaxed-state TD-DFT observables in SMD, not experimental spectra or a full nonadiabatic mechanism. Conformer coverage, functional/basis sensitivity, and the physical accuracy of implicit solvation are limitations. The triplet comparison supports solvent insensitivity within the reported model, not universal invariance.
