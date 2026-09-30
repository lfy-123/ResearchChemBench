# Private paper route

## 1. Scientific objective and author claim

The paper evaluates whether Pd 4d-to-2p X-ray emission spectroscopy (XES), interpreted with DFT, can distinguish Pd coordination and ligand environments. For compound 8, the authors claim that the broad, intense shoulder near 3170 eV is caused by several intense Pd–Cl transitions enabled by the D2h chloride environment and multiple filled chloride valence orbitals.

## 2. System and model boundary

Compound 8 is the neutral singlet Pd2Cl6 unit supplied as an optimized geometry in the SI. The calculation is a molecular model with two Pd and six Cl atoms; the reported solid-state D2h environment motivates interpretation but is not a periodic calculation. The observable is a normalized Pd 4d-to-2p XES spectrum, including transition energies and intensities, with comparison focused on the lower-energy shoulder and the principal Lβ2-region feature.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize molecular geometry and check stationary point | SI optimized XYZ for 8 | ORCA 5.03 | UKS PBE0; ZORA; ZORA-def2-TZVP; SARC-ZORA-TZVP on Pd; AutoAux; CPCM; charge 0, multiplicity 1; TightSCF, Opt, AnFreq | optimized geometry, frequencies, orbital file | ev_doc_7ab7405d6efe_000063_4cf061177b4b; ev_doc_7ab7405d6efe_000097_e313a177a70e; ev_doc_f847f60b8067_000236_f296e196cf56 |
| 2 | Compute Pd 4d-to-2p emission transitions | optimized orbitals/geometry | ORCA 5.03 XES module | RIJCOSX; PBE0/ZORA basis; CPCM; coreorb 2,2,3,3,4,4; orbop 0,1,0,1,0,1; CoreOrbSOC 4,5,6,7,8,9; DoSOC and DoQuad true | raw transition energies and intensities | ev_doc_7ab7405d6efe_000063_4cf061177b4b; ev_doc_f847f60b8067_000240_d785d5de326c |
| 3 | Make a plotted spectrum | raw transitions | ORCA orca_mapspc | normalize to maximum; +22 eV shift; Voigt FWHM 2.46 eV | simulated XES curve | ev_doc_f847f60b8067_000059_f3d1c14757b4; ev_doc_f847f60b8067_000123_803921089e3c |
| 4 | Interpret spectral regions and orbital origin | spectrum and orbital analysis | orca_mapspc/MOAna/ChemCraft | inspect transitions in approximately 3167–3171 and 3171–3174 eV; relate intensity to Pd d character and Pd–Cl mixing | feature comparison and mechanistic interpretation | ev_doc_f847f60b8067_000142_6a04ed2754a3; ev_doc_f847f60b8067_000175_1e9621c5769b |

## 4. Validation and analysis protocol

The authors compared optimized structures with available structural metrics (Table S2), used frequency analysis, and compared calculated and experimental normalized spectra. Their analysis emphasizes the lower-energy 3166–3171 eV region, the principal feature around 3171–3174 eV, and transition/orbital composition. They note that the applied broadening is larger than apparent in experiment, so line-shape agreement is qualitative rather than a claim of exact linewidth reproduction.

## 5. Private reference results

The paper reports that DFT predicts the main spectral features for 8. Experimentally, 8 has a broader and more intense shoulder centered near 3170 eV. The calculated high-intensity transitions arise from multiple orbitals with substantial Pd d character; the D2h symmetry, number and energy of filled chloride orbitals permit multiple Pd–Cl interactions spread approximately 3167–3171 eV. The paper also reports that the method's 2.46 eV broadening overestimates apparent experimental broadening.

## 6. Limitations and interpretation boundaries

The paper does not tabulate a digitized spectrum or exact peak/intensity values for 8 in the supplied evidence. Evaluation therefore uses source-backed feature locations, relative shoulder behavior, orbital/interaction interpretation, and validation process rather than invented numerical targets. The public task must not expose the paper's route details or these reference conclusions in autonomous mode.
