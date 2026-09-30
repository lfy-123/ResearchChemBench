# Private paper route

## 1. Scientific objective and author claim

The paper characterizes the electrophilic diferric μ-1,2-peroxo intermediate 1H, [(susan){FeIII(μ-O)(μ-O2)FeIII}]2+, by combining spectroscopy with DFT. The computational claim relevant here is that a broken-symmetry, antiferromagnetically coupled singlet model is a minimum and reproduces the short Fe···Fe separation and Mössbauer isomer shift associated with 1H. The authors further use the model to support assignment of the μ-1,2-peroxo core and its electrophilic reactivity.

## 2. System and model boundary

The modeled species is the cationic susan-supported diferric complex [(susan){FeIII(μ-O)(μ-O2)FeIII}]2+, with two Fe centers, one μ-oxo and one μ-1,2-peroxo bridge. The calculation uses the isolated cation, charge +2, an open-shell broken-symmetry singlet (St = 0) representation, implicit acetonitrile solvation (ε = 36.6), and no counterions or explicit solvent molecules. Reported observables are the Fe···Fe distance, vibrational minimum character, relative stability of broken-symmetry and high-spin solutions, and 57Fe Mössbauer isomer shift.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Prepare the 1H model | 1H molecular model; SI Table S10 geometry | ORCA 5.0.4; model construction described with PyMOL 2.5.4 | [(susan){FeIII(μ-O)(μ-O2)FeIII}]2+; charge +2; singlet broken-symmetry state | Starting structure | ev_doc_3df505570ad9_000528_4798922891b3 |
| 2 | Optimize geometry and compare spin solutions | Starting 1H structure | DFT geometry optimization in ORCA | TPSSh; scalar ZORA; relativistically recontracted def2-TZVP; D3BJ; CPCM CH3CN ε=36.6; RIJCOSX/def2/J; broken-symmetry (“brokensym”); high-spin optimization followed by antiferromagnetic low-spin optimization | Optimized low-spin and high-spin structures and energies | ev_doc_3df505570ad9_000149_6cbb5d5545f3; ev_doc_3df505570ad9_000160_4caa0c140517 |
| 3 | Establish a minimum | Optimized structures | Numerical vibrational frequency calculation in ORCA | Same level as optimization | Frequencies and absence/presence of imaginary modes | ev_doc_3df505570ad9_000160_4caa0c140517 |
| 4 | Compute Mössbauer density | Optimized broken-symmetry 1H | ORCA single point | TPSSh/RIJCOSX; ZORA-def2-TZVP; SARC/J; D3BJ; TightSCF; DefGrid3; CPCM CH3CN ε=36.6 | Fe-nuclear electron density ρ0 | ev_doc_3df505570ad9_000167_4a4201add61d; ev_doc_3df505570ad9_000168_077bf62f0674 |
| 5 | Convert density to isomer shift | ρ0 at each Fe nucleus | Reported calibration | δ = A(ρ0 − C) + B; A = −0.309785357, B = 0.325438551, C = 13785 | Calculated δ in mm s−1 | ev_doc_3df505570ad9_000167_4a4201add61d; ev_doc_3df505570ad9_000168_077bf62f0674 |

## 4. Validation and analysis protocol

The authors optimize a high-spin state and an antiferromagnetically coupled broken-symmetry low-spin state, compare their energies, and use a numerical frequency calculation to test minimum character. They report that the broken-symmetry solutions are lower in energy and that the final states are minima. Fe···Fe distances are read from the optimized structures. Mössbauer parameters are obtained from the optimized low-spin structure using the density calibration above; the paper notes an absolute calibration error of ±0.07 mm s−1 and a maximum error of 0.19 mm s−1. Table 1 reports for 1H a calculated Fe···Fe distance of 3.086 Å and calculated isomer shifts of 0.52 mm s−1 for both Fe centers; the experimental Fe···Fe reference is 3.17 Å by EXAFS and the experimental isomer shift is 0.47 mm s−1.

## 5. Private reference results

For the reproduced 1H calculation, the source-backed structural target is Fe···Fe = 3.086 Å (Table 1). The source-backed calculated Mössbauer targets are δ(Fe1) = 0.52 mm s−1 and δ(Fe2) = 0.52 mm s−1 (Table 1; average 0.52 mm s−1). The reference qualitative checks are: broken-symmetry antiferromagnetic singlet lower in energy than high spin; no imaginary frequencies for the optimized low-spin structure; and both Fe sites have approximately equal calculated isomer shifts.

## 6. Limitations and interpretation boundaries

The task tests one isolated molecular model, not the full experimental formation kinetics or reactivity. DFT energies, spin contamination, conformer dependence, basis/functional sensitivity, and the Mössbauer calibration uncertainty limit interpretation. The source reports rounded observables and an empirical density-to-shift calibration; evaluator tolerances must therefore be wider than numerical integration noise and must not be interpreted as experimental uncertainty estimates. The coordinates in SI Table S10 are an optimized-structure starting point, so reproduction is not a claim that an independent unconstrained search will find a unique global conformer.
