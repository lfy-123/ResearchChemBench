# Private paper route

## 1. Scientific objective and author claim

The paper studies local XHNBR/metal-oxide interfaces to relate carboxyl binding to crosslinking. For the ZnO cluster benchmark, the authors report a strongly stabilizing carboxyl contact involving proton transfer to cluster oxygen and coordination of the resulting carboxylate to Zn sites.

## 2. System and model boundary

The system is the neutral 24-atom (ZnO)12 finite cluster and neutral 16-atom XHNBR carboxyl fragment from SI Sections 3.1 and 3.2. The observable is the interaction enthalpy of the optimized complex, with bond distances and bonding descriptors used for interpretation. This is not a periodic bulk-surface calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated fragments and complex | SI Cartesian models | DFT, Gaussian 16 | ωB97XD/6-31+G(d,p) | optimized structures | ev_doc_1d025df0e7c0_000035_d5e322596a51; ev_doc_1d025df0e7c0_000036_3ebf5c36f3c6; ev_doc_7a2382071f82_000038_a9ecf94f8667 |
| 2 | Verify minima and obtain thermal corrections | optimized structures | harmonic frequencies, Gaussian 16 | same DFT level | frequencies and enthalpy corrections | ev_doc_1d025df0e7c0_000035_d5e322596a51; ev_doc_1d025df0e7c0_000037_4973e7563aa5 |
| 3 | Refine electronic energy | optimized structures | single-point DFT | ωB97XD/6-311++G(2df,2p) | refined energies | ev_doc_1d025df0e7c0_000037_4973e7563aa5 |
| 4 | Compute interaction enthalpy | complex, cluster, fragment | H(complex) − H(cluster) − H(fragment) | electronic energy plus thermal corrections | ΔH | ev_doc_1d025df0e7c0_000038_6abf02e2a6cb; ev_doc_1d025df0e7c0_000043_d652d7e69a62 |
| 5 | Characterize bonding | optimized complex and wavefunction | NBO and QTAIM/AIMAll | BCP density, Laplacian, H and donor–acceptor terms | bonding interpretation | ev_doc_1d025df0e7c0_000010_a0856f645fe2; ev_doc_1d025df0e7c0_000035_d5e322596a51 |

## 4. Validation and analysis protocol

The authors compare optimized carboxyl distances and interaction enthalpies across ZnO, MgO, CaO and MgO2. For ZnO, the reported geometry has a short new O–H contact to cluster oxygen, unequal carboxyl C–O distances, and multiple Zn–O contacts. QTAIM and NBO are used to classify the interaction.

## 5. Private reference results

SI Table 1 reports ΔH = −58.74 kcal mol−1 for (ZnO)12/carboxyl, with carboxyl R1=1.568, R2=1.013, R3=1.927, R4=1.250 and R5=1.284 Å. The main paper reports proton transfer and QTAIM values for the associated bonds; ZnO is the only system in the set with partially covalent metal–oxygen character in the summarized analysis.

## 6. Limitations and interpretation boundaries

The finite cluster is a local model and does not establish bulk surface energetics, kinetics or macroscopic crosslink density. Results depend on the electronic-structure method and local minimum. Independent work must report starting-structure coverage and any competing minima found.
