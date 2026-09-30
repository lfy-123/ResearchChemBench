# Private paper route

## 1. Scientific objective and author claim

The paper tests whether a gas-phase DFT-optimized geometry of the dimeric 1-(4-methylphenyl)piperazinyl dithiocarbamato-S,S′ zinc(II) complex agrees with its single-crystal X-ray structure. The authors claim close agreement, summarized by mean absolute and mean square absolute errors for selected bond lengths and angles.

## 2. System and model boundary

The system is a neutral, closed-shell centrosymmetric dinuclear Zn(II) dithiocarbamate dimer. Each Zn is five-coordinate: two sulfur donors from chelating dithiocarbamate ligands plus a weak sulfur bridge from the adjacent inversion-related unit. The experimental comparison uses the atom labels and selected entries in SI Tables S1 and S2; hydrogen atoms are not needed for those reported observables.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish molecular model | SC-XRD structure deposited as CCDC 2361759 | Structure preparation from deposited crystal model | Neutral dimer; preserve crystallographic atom identity | Molecular starting geometry | ev_doc_076e1988cfd8_000303_067ca727a7f3; ev_doc_076e1988cfd8_000437_eefa97ad642c |
| 2 | Optimize molecular and electronic structure | Starting molecular geometry | DFT in Gaussian 09W, visualized with GaussView 5.0 | B3LYP/6-31G; gas phase | Optimized geometry and electronic properties | ev_doc_076e1988cfd8_000065_3b5d282a5a95 |
| 3 | Compare structure to experiment | Optimized geometry and SC-XRD values | Extract selected distances/angles and calculate AE, squared AE, means | SI Tables S1 and S2 definitions | MAE/MSAE for lengths and angles; correlation analysis | ev_doc_076e1988cfd8_000145_55cadd498122; ev_doc_d393df403cbf_000038_31f7aa0faed3; ev_doc_d393df403cbf_000040_a97ce460f9af |

## 4. Validation and analysis protocol

The authors compare selected experimental and calculated bond lengths and bond angles, report mean absolute error (MAE) and mean square absolute error (MSAE), and use correlation plots/R² as an additional agreement check. The structural interpretation is a distorted square-pyramidal Zn environment with weak Zn···S bridging across the inversion center.

## 5. Private reference results

SI Table S1 reports length MAE 0.042707 Å and MSAE 0.003557 Å². SI Table S2 reports angle MAE 3.614103° and MSAE 26.03925°². The main text reports R² values of 0.9967 (lengths) and 0.95438 (angles), and says the optimized geometry closely aligns with the SC-XRD geometry.

## 6. Limitations and interpretation boundaries

The comparison covers selected SI entries, not every geometric degree of freedom. Crystal packing, thermal motion and the gas-phase approximation limit interpretation. Agreement with the reported selected metrics does not establish uniqueness of the optimized conformer or prove catalytic performance.
