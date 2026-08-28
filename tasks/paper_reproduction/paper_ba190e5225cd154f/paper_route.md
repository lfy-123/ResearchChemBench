# Private paper route

## 1. Scientific objective and author claim

The paper evaluates internal reorganization energies for electron and hole transfer in four cyanophenyl-imidazole derivatives. The author interpretation is that the calculated charge-state energy cycles characterize charge-carrier transport, with PImCY2 described as having the smallest hole reorganization energy and relatively balanced transport.

## 2. System and model boundary

The systems are isolated gas-phase molecular derivatives BImCY2, PImCY2, BImDCY and PImDCY. The route uses neutral, cation (+1) and anion (-1) electronic states; singlet neutral and doublet ions are implied by the charge-state protocol. Environmental, crystal-packing and external transport factors are outside the reported reorganization-energy calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize neutral geometry | SI Cartesian coordinates | DFT, Gaussian 09 | B3LYP/6-31+G(d,p), neutral | optimized neutral geometry | ev_doc_08104a65f813_000055_38e1f83545d4; ev_doc_23351db9f389_000039_ad3785db1c5c |
| 2 | Evaluate neutral-geometry charge states | optimized neutral geometry | single-point DFT, Gaussian 09 | neutral, cation and anion | E0^0, E0^+, E0^- | ev_doc_08104a65f813_000217_7a2ded5fc825 |
| 3 | Optimize cation | neutral starting geometry | DFT, Gaussian 09 | B3LYP/6-31+G(d,p), +1 doublet | optimized cation geometry | ev_doc_08104a65f813_000235_25f97159c4fa |
| 4 | Evaluate neutral and cation energies on cation geometry | optimized cation | single-point DFT | 0 and +1 | E+^0, E+^+ | ev_doc_08104a65f813_000217_7a2ded5fc825 |
| 5 | Optimize anion | neutral starting geometry | DFT, Gaussian 09 | B3LYP/6-31+G(d,p), -1 doublet | optimized anion geometry | ev_doc_08104a65f813_000235_25f97159c4fa |
| 6 | Evaluate neutral and anion energies on anion geometry | optimized anion | single-point DFT | 0 and -1 | E-^0, E-^- | ev_doc_08104a65f813_000217_7a2ded5fc825 |
| 7 | Form reorganization energies | six energies | algebraic analysis | λe=(E0^-−E-^-)+(E-^0−E0^0); λh=(E0^+−E+^+)+(E+^0−E0^0) | λe and λh | ev_doc_08104a65f813_000217_7a2ded5fc825 |

## 4. Validation and analysis protocol

The paper compares computed reorganization energies across the four named molecules and interprets relative λe/λh values as transport tendencies. It reports single-point energies on optimized geometries and does not explicitly report a frequency-based minimum check for this analysis. The task therefore requires the agent to document optimization convergence and any minimum/stationarity validation it performs, while distinguishing computed evidence from the paper's interpretation.

## 5. Private reference results

For BImCY2, Table 7 reports λe = 0.5153 eV and λh = 0.4152 eV. Across the four compounds, the reported λh values are 0.4152, 0.2139, 0.3736 and 0.2786 eV, and λe values are 0.5153, 0.3790, 0.3922 and 0.3617 eV in the order BImCY2, PImCY2, BImDCY, PImDCY. The paper states that λh is lower than λe for each compound and highlights PImCY2 as the lowest-λh case.

## 6. Limitations and interpretation boundaries

The source does not specify all Gaussian keywords, SCF/grid settings or an explicit solvent model. The values are isolated-molecule electronic-structure results, not direct mobility measurements; morphology, packing, disorder and environmental relaxation are not included.
