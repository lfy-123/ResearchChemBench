# Private paper route

## 1. Scientific objective and author claim

The paper uses TD-DFT to explain spin–fluorescence coupling in compound 1. Its local claim is that, in the low-spin (LS) first-coordination-sphere Fe(II) model, metal-centered MLCT and Fe(II) d–d absorptions overlap the ligand fluorescence and provide an efficient nonradiative energy-transfer channel; the d–d feature is assigned at 545 nm. The authors further report a weak LLCT transition at 620 nm with f = 0.0057 for compound 1.

## 2. System and model boundary

The computational object is one Fe(II) center with two pyridyl-based ligands and four cyanide ligands, two cyanides protonated for charge neutrality. The LS model is truncated from the 100 K crystal structure and is represented by the 65-atom Cartesian coordinates in SI Table S6. The paper treats the first coordination sphere, not the periodic Hofmann framework.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build LS local model | 100 K crystal-derived first-coordination-sphere geometry | Gaussian 16 | one Fe(II), two pyridyl ligands, four cyanides; two cyanides protonated | LS model | ev_doc_b03ae30ec27b_000346_5ad0c8f543dd; ev_doc_97a398ad4d08_000134_cae545bb346f |
| 2 | Remove uncertainty in X-ray H positions | LS model | Gaussian 16 constrained optimization | B3LYP*, def2-TZVP; heavy atoms fixed, only H atoms relaxed | optimized LS geometry | ev_doc_b03ae30ec27b_000346_5ad0c8f543dd |
| 3 | Compute vertical spectrum | optimized LS geometry | Gaussian 16 TD-DFT linear response | B3LYP*, def2-TZVP; 60 excited states | excitation energies and oscillator strengths | ev_doc_b03ae30ec27b_000352_9d774fab3d6d |
| 4 | Assign bands and interpret coupling | TD-DFT states and NTO/CI assignments | spectral assignment | MLCT near 400/410 nm; Fe d–d near 545/550 nm; LLCT near 620 nm | bands, oscillator strengths, energy-transfer interpretation | ev_doc_b03ae30ec27b_000295_eea6670d4198; ev_doc_b03ae30ec27b_000301_691d56c85bfa |

## 4. Validation and analysis protocol

The authors compare calculated absorption features with the experimental fluorescence envelope and inspect orbital/NTO character. They use the LS d–d feature at 545 nm and its Figure 5 assignment as the key metal-centered validation, and report the 620 nm LLCT oscillator strength for compound 1. The mechanistic interpretation is bounded to local electronic energy transfer in the truncated model; it is not a periodic solid-state rate calculation.

## 5. Private reference results

The paper reports an intense LS MLCT band near 400 nm (SI assignment at 410 nm), a weaker Fe(II) d–d band at 545 nm, and a weak LLCT transition at 620 nm with f = 0.0057 for compound 1. The 545 nm feature has Fe d–d character with partial MLCT character. These values and assignments are hidden from Agent-visible inputs.

## 6. Limitations and interpretation boundaries

The model is a truncated local complex, not the periodic framework; only hydrogen positions are optimized in the authors' route. Vertical TD-DFT transitions are not directly experimental absorption maxima, and band assignments depend on state character/NTO analysis. The evaluator therefore scores reported features and qualitative assignments within this model boundary, while accepting a scientifically justified alternate computational protocol and explicit limitations.
