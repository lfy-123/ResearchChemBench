# Private paper route

## 1. Scientific objective and author claim

The paper studies how the 3-position halogen (Cl, Br, or I) in isostructural quasi-1D 3-X-C5H4NH-PbBr3 changes the electronic band gap. The author claim is that the substituent changes the crystallographic a-axis and thereby changes the electronic structure; iodine additionally changes band-edge character through iodine/organic orbital mixing.

## 2. System and model boundary

The systems are four-formula-unit monoclinic P21/c crystals measured at 300 K: 3-Cl-C5H4NH-PbBr3, 3-Br-C5H4NH-PbBr3, and 3-I-C5H4NH-PbBr3. The computational boundary is periodic electronic structure of the experimental cells. Reported primary values are HSE06 band gaps without SOC; SOC is treated indirectly with smaller model cells and is therefore a trend correction rather than an exact property of the parent cells.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish parent structures | 300 K experimental crystals | VASP 6.3.0 PAW | P21/c, four formula units; CCDC 2499860/2499861/2499862 | periodic cells | ev_doc_bb6e4f756d2c_000178_0d4f5a4fb1d4; ev_doc_bb6e4f756d2c_000310_ac23b9c709ae |
| 2 | Obtain electronic states | each parent cell | HSE06 periodic DFT in VASP | SCF energy convergence 1.0×10^-7 eV; pseudopotential-default kinetic cutoffs; Gamma-centered Monkhorst-Pack sampling; scalar-relativistic PAW | self-consistent states | ev_doc_bb6e4f756d2c_000057_20b506efb7ff; ev_doc_bb6e4f756d2c_000058_cca7b07822eb; ev_doc_bb6e4f756d2c_000059_f6c5652fb0c2 |
| 3 | Plot and inspect bands/DOS | converged states | VASPKIT 1.3.1 and VASP | path Gamma-Z-D-B-Gamma-A-E-Z-C2-Y2-Gamma; 50 points per segment | band dispersion and DOS | ev_doc_bb6e4f756d2c_000061_447852ce6d75 |
| 4 | Assign gap and orbital character | bands/DOS | post-processing | lowest energy allowed VB-to-Pb-derived-CB transition, excluding symmetry-forbidden p-to-pi* transitions | gap and band-edge interpretation | ev_doc_bb6e4f756d2c_000145_b18a4cc481f7; ev_doc_bb6e4f756d2c_000149_861dd7011649 |
| 5 | Estimate SOC trend | reduced model cells retaining N positions and ring halogen | HSE06+SOC | model retains P21/c; parent-to-model comparison | SOC shrinkage trend and corrected estimates | ev_doc_6b93b851c80c_000022_36aa63c1f945; ev_doc_6b93b851c80c_000023_41b9ad2c8112; ev_doc_6b93b851c80c_000024_aa00da2d6d5c |

## 4. Validation and analysis protocol

The authors compare the three isostructural cells, inspect band structures and DOS, identify the valence and conduction edge locations, and use smaller isotypical models to estimate SOC shrinkage. The reported analysis links increasing a-axis length to decreasing gap and discusses iodine contribution/overlap at the band edges. The paper explicitly warns that model-cell SOC corrections show trends rather than accurate parent-cell values.

## 5. Private reference results

The reported HSE06 gaps are 4.63 eV (Cl), 4.64 eV (Br), and 4.44 eV (I). The corresponding direct Gamma-to-Gamma transitions are 4.43, 4.39, and 4.17 eV. The model SOC shrinkages are 0.27, 0.31, and 0.31 eV, yielding estimated HSE06+SOC parent gaps of 4.36, 4.33, and 4.13 eV. The primary trend is a lower gap from Cl/Br to I and correlation with a-axis elongation.

## 6. Limitations and interpretation boundaries

The exact k-point dimensions are not stated in the indexed text, so reproduction must report the chosen convergence criterion or density. SOC is not a direct parent-cell HSE06+SOC calculation; the model correction is explicitly approximate. Band-edge/orbital assignments should be supported by the submitted band/DOS evidence and not inferred from chemical intuition alone.
