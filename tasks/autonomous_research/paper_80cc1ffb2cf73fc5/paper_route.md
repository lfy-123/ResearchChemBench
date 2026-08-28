# Private paper route

## 1. Scientific objective and author claim

The paper tests whether the mHBDI anion supports dipole-bound and dipole-resonance states near electron detachment and whether calculated Franck–Condon (FC) structure accounts for the observed cryogenic action spectrum. The authors claim that DFT/FC calculations reproduce prominent features and that one low-energy neutral-radical mode is especially active.

## 2. System and model boundary

The system is the gas-phase deprotonated meta-GFP model chromophore (mHBDI−), with the Z1/Z2/E1/E2 constitutional/geometric isomers considered by the authors. The reported experiment probes 19,400–20,100 cm⁻¹ near the detachment threshold. The computational comparison uses the anion S0 as initial state and neutral radical D0 as final state; the diffuse excess electron and the neutral core are treated within the electronic-structure model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize anion and neutral geometries | Four isomer structures | Gaussian 16; ωB97X-D/aug-cc-pVTZ | Anion charge −1, singlet; neutral radical charge 0, doublet | Optimized geometries and energies | ev_doc_3d70e28ee4ff_000112_3a3e9eff53dd; ev_doc_28294488cf6d_000010_5e03ffac1ddc |
| 2 | Obtain harmonic normal modes | Optimized structures | Gaussian 16 frequency calculation at same level | Harmonic frequencies and normal modes | Frequencies/modes for anion and neutral | ev_doc_3d70e28ee4ff_000116_1bdab8c7b9b0; ev_doc_28294488cf6d_000030_d8921e89ea2b |
| 3 | Simulate vibronic spectrum | Anion S0 and neutral D0 geometries/modes | Gaussian 16 Franck–Condon implementation | 6 K; scale frequencies by 0.9566; Gaussian broadening FWHM 4 cm⁻¹; linear direct-attachment background from detachment energy | Stick/convoluted spectra | ev_doc_3d70e28ee4ff_000112_3a3e9eff53dd; ev_doc_28294488cf6d_000015_0d478d107ed9 |
| 4 | Compare with action spectrum and assign modes | Calculated spectra and measured spectrum | Align calculated 0→0 to experimental origin; inspect progressions | Z1 and Z2 comparisons; third normal mode emphasized | Peak correspondence and mode assignment | ev_doc_3d70e28ee4ff_000118_746a027fed1f; ev_doc_3d70e28ee4ff_000143_421c5825b43f |

## 4. Validation and analysis protocol

The optimized structures were checked through harmonic frequencies. The FC spectrum was shifted to the lowest observed band, scaled, broadened, and compared with the measured spectrum. The authors compared all four isomers and inspected the low-energy progression and normal-mode visualization. They caution that many observed bands remain unassigned and that diffuse DBSs challenge DFT.

## 5. Private reference results

The measured DBS origin is 19,444 cm⁻¹ and the VDE is 19,620 cm⁻¹, giving 176 cm⁻¹ binding energy. Figure 3 identifies a prominent feature 304 cm⁻¹ above the origin (19,748 cm⁻¹). The calculated Z1 spectrum was shifted by 512 cm⁻¹ to the origin. The particularly active vibration is the third normal mode, an in-plane bending mode; its reported low-energy frequencies are approximately 80 cm⁻¹ for Z1 and 82 cm⁻¹ for Z2. The authors reproduce several prominent features but not all bands.

## 6. Limitations and interpretation boundaries

The calculation is a harmonic, single-level DFT/FC model of a highly diffuse electron and cannot guarantee assignment of every experimental band. Isomer mixtures, internal rotation, broadening, and unmodeled nonadiabatic effects may contribute. Agreement with prominent peak positions supports, but does not prove, a unique microscopic mechanism; the DRS doorway-state interpretation is qualitative.
