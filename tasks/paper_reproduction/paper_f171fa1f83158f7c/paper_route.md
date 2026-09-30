# Private paper route

## 1. Scientific objective and author claim

The paper assigns the absolute configuration of clathriamine A (1), a dicationic bis-indole/bis-guanidinium natural product, by comparing the solution ECD spectrum of the isolated material with Boltzmann-weighted TD-DFT ECD predictions for an enantiomeric model. The authors claim that the isolated material has (1S,2R,3S,4R) configuration; the modeled comparison structure is its opposite, (1R,2S,3R,4S)-1.

## 2. System and model boundary

The explicit computational model is C22H22Br2N8 (54 atoms), charge +2, singlet, in methanol, as counted from all 54 Cartesian rows in original SI S10. The main-text neutral/HRMS C22H20Br2N8 formula is not the elemental count of this diprotonated computational model. The earlier thesis-derived 52-atom input had different connectivity and is withdrawn. The computational ensemble is restricted to the two retained optimized conformers below 10 kJ/mol of the next-lowest conformer; the lowest conformer was excluded because its geometry conflicted with the solution NOE H-4′/H-1 observation. The observable is the electronic circular dichroism (ECD) spectrum, represented by wavelength-dependent rotatory-strength bands and compared with the experimental spectrum.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate and optimize conformers | Cationic clathriamine A model | CREST/GFN2-xTB, then Gaussian16 | MeOH implicit solvation; charge +2; 298.15 K corrections; ωB97X-D/def2-SVP/IEFPCM(MeOH) optimization and frequencies | Stationary-point geometries and thermochemistry | ev_doc_7686ed923580_000244_fdc9480eb58a; SI S8/S10/S12 |
| 2 | Select solution-relevant ensemble | Optimized conformers | Visual NOE check and SpectroIBIS filtering | Remove NOE-inconsistent lowest conformer; remove redundant structures; retain states within 10 kJ/mol | Two retained conformers and populations | ev_doc_7686ed923580_000244_fdc9480eb58a; ev_doc_7686ed923580_000140_80144110d10c |
| 2a | Compute composite Gibbs energies for populations | Validated minima and thermal corrections | Gaussian16 | B3LYP-D3(BJ)/def2-TZVP/IEFPCM(MeOH) electronic energy + wB97X-D/def2-SVP/IEFPCM(MeOH) thermal correction at 298.15 K | Composite Gibbs energies and weights | Main PDF p6 Computational Details; SI S10/S12 |
| 3 | Compute excited-state chiroptical properties | Two retained geometries | Gaussian16 TD-DFT | PBE0 and ωB97X-D/def2-TZVP/IEFPCM(MeOH); first 30 states | Wavelengths, oscillator strengths, rotatory strengths | ev_doc_7686ed923580_000246_04a19974dfda; SI S13/S14 |
| 4 | Form ensemble ECD predictions | Transition properties and populations | SpectroIBIS and SpecDis | Boltzmann weighting at 298.15 K; half-height bandwidth 0.2 eV; redshifts 15 nm (ωB97X-D) and 5 nm (PBE0) | Smoothed predicted ECD spectra | ev_doc_7686ed923580_000139_29adb67baf67; ev_doc_7686ed923580_000246_04a19974dfda |
| 5 | Assign configuration | Experimental and predicted ECD | Visual spectrum comparison | Near mirror-image relationship and Cotton-effect sign pattern | Absolute-configuration assignment | ev_doc_7686ed923580_000132_578681bda69c; ev_doc_7686ed923580_000139_29adb67baf67 |

## 4. Validation and analysis protocol

The authors checked stationary points with frequencies, compared conformer geometries against solution NOEs, filtered redundant/high-energy structures, and performed an explicit ten-methanol CREST microsolvation investigation. They judged the assignment from the near mirror-image relationship between predicted and experimental ECD curves, using both PBE0 and ωB97X-D predictions.

## 5. Private reference results

SI S12 reports the retained conformer populations as 90.82% and 9.18%, with a 5.682 kJ/mol separation. SI S13/S14 provide the complete 30-state transition tables for both functionals. The paper reports that the predicted spectrum for (1R,2S,3R,4S)-1 is near the mirror image of the natural-product spectrum and therefore assigns the isolated compound as (1S,2R,3S,4R)-1.

## 6. Limitations and interpretation boundaries

ECD assignment is conditional on the conformer ensemble, solvent model, electronic-structure approximation, band broadening/redshift, and the reliability of the experimental spectrum. Agreement of signs and broad features supports an assignment but is not an independent proof of connectivity or a mechanistic explanation. The autonomous task therefore accepts a bounded, explicitly reported computational investigation and requires uncertainty/limitations reporting.
