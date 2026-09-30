# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to test the proposed radical cross-electrophile-coupling cycle. The central computed event is halogen-atom transfer (XAT) from propargyl bromide to the Cu(I)/L1 bromide complex, producing a Cu(II) species and a propargyl radical. The authors claim this XAT event is kinetically accessible and is preferred to direct reaction of the Cu(I) complex with the aryl electrophile. They also examine whether coordination of the ligand NMe2 group is an alternative catalyst arrangement.

## 2. System and model boundary

The modeled catalyst precursor is the Cu(I)/L1 bromide complex (Int 1 in the SI), reacting with the substituted propargylic bromide (3-bromo-5-phenylpent-1-yn-1-yl)trimethylsilane, C14H19BrSi. The SI p120 heading calls it “Propargyl bromide”, but its full 35-atom coordinates do not describe unsubstituted C#CCBr. The separate Br− and I− entries after that coordinate block are not part of the substrate. The paper's DFT boundary includes optimized stationary points, frequency-derived thermochemistry at 298.15 K, solvated single-point energies in DMF, and an IRC check for transition-state connectivity. It does not establish full solution speciation or a complete catalytic kinetics model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize minima and transition states | Structures for Cu/L1 complexes and organic partners | Gaussian 16; B3LYP-D3(BJ) | SDD for Cu and halogens; 6-31G(d) for other atoms; SMD(DMF) according to explicit SI p59 methods prose; see internal source ambiguity below | Stationary-point geometries | ev_doc_47bffbf2b157_000630_1ac3c79f3889; ev_doc_47bffbf2b157_000632_3db01e109503 |
| 2 | Assign stationary-point character and obtain thermochemistry | Optimized geometries | Gaussian 16 frequency analysis; Shermo post-processing | 298.15 K; frequency scaling 0.9813 | ZPVE, thermal corrections, Gibbs energies; minima have no imaginary mode and TSs one | ev_doc_47bffbf2b157_000632_3db01e109503; ev_doc_47bffbf2b157_000641_ee0f519e3ca6 |
| 3 | Include solvent in energies | Optimized geometries | B3LYP-D3(BJ)/SMD(DMF) single points | SDD for Cu/Br/I; 6-311+G(d,p) for other atoms | DMF single-point energies | ev_doc_47bffbf2b157_000630_1ac3c79f3889; ev_doc_47bffbf2b157_000631_1a11171e547b |
| 4 | Convert gas standard state to solution standard state | Thermochemical quantities | Shermo correction | +1.89 kcal/mol at 298.15 K for 1 atm to 1 mol L−1 | Solution-phase free energies | ev_doc_47bffbf2b157_000641_ee0f519e3ca6 |
| 5 | Verify reaction connectivity | Candidate XAT TS | IRC calculation | Connects the intended reactant and product valleys | Validated XAT transition state | ev_doc_47bffbf2b157_000632_3db01e109503 |
| 6 | Compare mechanistic alternatives | XAT and alternative pathways | Same composite protocol | Relative activation free energies | Mechanistic interpretation | ev_doc_47bffbf2b157_000646_431ff17a0fd9; ev_doc_e78636be51bd_000118_9daa03cf8caa; ev_doc_e78636be51bd_000119_4eb85191e6cb |

## 4. Validation and analysis protocol

The SI energy table reports Int 1 as a minimum and TS 1 with one imaginary frequency (104.5i). The authors use frequency analysis to classify stationary points and IRC to check that a transition state connects the intended reactant/product valleys. Their XAT interpretation is placed alongside experimental mechanistic evidence and comparisons with direct aryl-halide activation.

## 5. Private reference results

The main paper reports a TS 1 XAT activation free energy of 10.6 kcal/mol. The SI reports the alternative NMe2-coordinated XAT barrier as 15.6 kcal/mol and says that NMe2 coordination raises the system energy by 5.6 kcal/mol. The SI table lists TS 1's imaginary frequency as 104.5i and Int 1 with no imaginary frequency. These values are evaluator-private.

## 6. Limitations and interpretation boundaries

SI p59 explicitly includes DMF solvent effects in both geometry optimization and single-point calculations; the Fig. S13 composite label omits the optimization solvent. Preserve this internal ambiguity. The current verification follows the explicit methods prose and does not claim access to an unreported original Gaussian input. The XAT scientific objective and evaluator numerical values have not been changed to match a computed result.

The result is a model-chemistry free-energy barrier, not a directly measured rate constant. Implicit DMF, standard-state and vibrational corrections, conformational sampling, spin-state choices, and the treatment of open-shell Cu/radical species can affect the value. A fair task should score stationary-point identity, connectivity and transparent energy construction separately from numerical agreement, and should accept a scientifically justified bounded failure when a validated TS cannot be obtained.
