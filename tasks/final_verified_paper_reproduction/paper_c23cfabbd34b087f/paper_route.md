# Private paper route

## 1. Scientific objective and author claim

The paper uses model compounds to assign the intense low-energy UV–vis absorption of the 1-series PAHs. For 1M-TIPS, the authors claim that a TD-DFT vertical transition reproduces the near-700-nm band and is a HOMO-to-LUMO, delocalized π–π* excitation.

## 2. System and model boundary

1M-TIPS is the neutral singlet model compound in which the TIPS-acetylene substituents are represented by –C≡C–SiH3 groups. The supplied stationary-point geometry contains 102 atoms (C58H42Si2). The calculation is gas-phase geometry optimization/frequency followed by a vertical excitation in a CHCl3 continuum.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the model and establish a minimum | 1M-TIPS Cartesian geometry | Gaussian 09; dispersion-corrected DFT | (u)B3LYP-D3/def2-SVP; neutral singlet model | optimized stationary point and Hessian | ev_doc_6d706569f912_000470_52f281b0ceb6; ev_doc_6d706569f912_000471_ef4e0e599cae; ev_doc_6d706569f912_000472_749afafc8b7f; ev_doc_6d706569f912_000473_ee6b64824d08; ev_doc_6d706569f912_000474_31a0d0c3b7a2 |
| 2 | Compute vertical absorption properties | optimized 1M-TIPS geometry | TD-DFT with implicit solvent | PCM(CHCl3), same B3LYP-D3/def2-SVP level | excitation energies/wavelengths and oscillator strengths | ev_doc_6d706569f912_000479_401997cee9b0; ev_doc_7cc730197b18_000101_867703d9d235 |
| 3 | Assign the intense band | TD-DFT state list and orbitals | orbital/state inspection | compare energy and oscillator strength; inspect transition character | HOMO→LUMO π–π* assignment | ev_doc_7cc730197b18_000109_a785b37a682f; ev_doc_7cc730197b18_000110_5e7d2710cc90 |

## 4. Validation and analysis protocol

The SI says all species were frequency-characterized and had positive-definite Hessians. The main paper assigns the strong low-energy transition from excitation energy, oscillator strength, and orbital character. The reference comparison is to the reported 1M-TIPS vertical wavelength and oscillator strength, with the transition assignment checked qualitatively.

## 5. Private reference results

For 1M-TIPS the paper reports λcalc = 735 nm and oscillator strength 1.24 for the intense low-energy transition. It identifies the transition as HOMO→LUMO between highly delocalized π orbitals, hence π–π*.

## 6. Limitations and interpretation boundaries

This is a vertical, model-compound calculation rather than a vibronic spectrum or a calculation on the full dodecyl/TIPS experimental molecule. Agreement is a benchmark of the reported computational claim, not proof that one functional/basis is universally accurate. Geometry and state ordering can be method-sensitive; the evaluator therefore scores reported numerical observables and evidence-backed assignment/validation separately.
