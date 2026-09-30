# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to relate the viscosity-dependent optical response of the cationic hemicyanine NIR-IND to its conformational and excited-state electronic structure. The authors claim that a planar, trans NIR-IND conformer in glycerol gives an allowed, delocalized ICT transition consistent with the measured glycerol absorption, whereas a perpendicular geometry is associated with a weak TICT transition.

## 2. System and model boundary

NIR-IND is the singly charged hemicyanine cation formed from a 4-(dimethylamino)cinnamaldehyde donor/linker and 1-ethyl-2,3,3-trimethylindolium acceptor. The calculations concern isolated NIR-IND in implicit water or glycerol, singlet ground-state structures and vertical singlet excitations. The donor/acceptor torsion is examined at planar (0°) and perpendicular (90°) geometries, with cis/trans planar variants.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structures | NIR-IND conformers | Gaussian 16 DFT | 6-31++G(d,p); CPCM water and glycerol; planar 0° and vertical 90° donor/acceptor torsional geometries; cis/trans planar forms | Optimized geometries | ev_doc_33e4c66e1bd8_000066_d8858a91ce27; ev_doc_33e4c66e1bd8_000067_0192a7113044; ev_doc_33e4c66e1bd8_000068_51d8fdb2a667; ev_doc_33e4c66e1bd8_000210_f5d3d2b3bb76 |
| 2 | Calculate electronic transitions | Optimized structures | Gaussian 16 TD-DFT | Same basis and CPCM solvent; B3LYP, CAM-B3LYP, PBE0, WB97XD and M062X tested; PBE0 used for comprehensive comparison | Transition energy, wavelength, oscillator strength and orbital contributions | ev_doc_33e4c66e1bd8_000075_c61e741956ce; ev_doc_33e4c66e1bd8_000210_f5d3d2b3bb76 |
| 3 | Compare with experiment and interpret | Computed transitions and solution spectra | State-by-state comparison | Glycerol absorption experiment and orbital/oscillator-strength analysis | Conformer/transition assignment and viscosity interpretation | ev_doc_33e4c66e1bd8_000075_c61e741956ce; ev_doc_68cabd8de3b3_000180_318c0359b162 |

## 4. Validation and analysis protocol

The authors inspect optimized structures, classify planar versus vertical geometries, examine frontier-orbital delocalization, and compare calculated transitions with measured absorption maxima. The paper reports that the planar transition is dominated by HOMO→LUMO character and has oscillator strength above one, while the vertical state has very small oscillator strength. It uses the agreement of the trans planar glycerol transition with the glycerol absorption to support the high-viscosity conformational assignment.

## 5. Private reference results

For NIR-IND in glycerol with PBE0, the reported trans planar transition is 1.978 eV, 2.285 oscillator strength, and 626.9 nm, with 99.0% HOMO→LUMO contribution. The glycerol experimental absorption maximum is 631 nm and the measured emission maximum is 690 nm. The reported vertical transition has oscillator strength 0.002 and wavelength 610.4 nm. These values are hidden from Agent-visible inputs.

## 6. Limitations and interpretation boundaries

The calculation uses an implicit solvent and vertical excitations; it does not model explicit glycerol, vibronic structure, excited-state relaxation, or a solution conformer population. Agreement of one calculated transition with an absorption maximum supports, but does not uniquely prove, population dominance. The paper's reported method sensitivity and imperfect OCR/layout do not justify treating the computed value as a universal experimental prediction.
