# Private paper route

## 1. Scientific objective and author claim

The paper studies the neutral heteroaromatic compound 3-(5-(butylthio)-1H-1,2,4-triazol-3-yl)-2-ethylimidazo[1,2-a]pyridine (C15H19N5S). The computational claim is that a gas-phase DFT treatment gives a stable optimized molecular structure close to the single-crystal structure and a comparatively large frontier-orbital gap, supporting the authors' qualitative statement of chemical stability.

## 2. System and model boundary

The molecular system is one isolated, neutral, closed-shell molecule in its ground electronic state. The crystal reference is the deposited compound-1 structure, CCDC 2449676, measured at 298(2) K in space group C 1 2/c 1. Crystal packing, solvent, counterions and protein docking are outside the quantum-chemical model boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate candidate conformations | Compound 1 molecular structure | Spartan'08 molecular mechanics | MMFF initial conformational search | Candidate conformers | ev_doc_ad0f9b6dbe28_000095_4fd0fcef4d5f |
| 2 | Refine all candidate conformers and test minima | Candidate conformer geometries | Gaussian 09 DFT | B3LYP/6-311+G(2d,p), neutral ground state, in vacuo; optimization plus frequency | Optimized structures, Gibbs energies and frequencies | ev_doc_ad0f9b6dbe28_000085_7a728bd94c45; ev_doc_ad0f9b6dbe28_000117_c39c27b77d1b |
| 3 | Estimate room-temperature conformer populations | Optimized conformer thermochemistry | Boltzmann analysis | 298 K; relative Gibbs energies and Boltzmann weighting | Conformer population table | ev_doc_ad0f9b6dbe28_000095_4fd0fcef4d5f |
| 4 | Compare optimized and experimental structure | Optimized minimum and compound-1 crystal structure | Geometric comparison reported against X-ray data | Bond lengths, bond angles and torsions; Table S1 | Agreement assessment | ev_doc_ad0f9b6dbe28_000095_4fd0fcef4d5f |
| 5 | Compute electronic stability descriptor | Optimized minimum | Gaussian 09/GaussView 5.0 DFT orbital analysis | Same B3LYP/6-311+G(2d,p) model | HOMO, LUMO and gap | ev_doc_ad0f9b6dbe28_000040_7de1864914e0; ev_doc_ad0f9b6dbe28_000117_c39c27b77d1b |

## 4. Validation and analysis protocol

The authors validate minima with frequency calculations, use relative Gibbs energies for room-temperature populations, compare structural parameters to the X-ray model, and interpret the HOMO-LUMO gap as a qualitative stability indicator. The crystallographic structure has reported quality statistics including R1 = 0.0465 for I >= 2sigma(I), wR2 = 0.1272, and goodness-of-fit 1.034. The reported intermolecular N-H...N contact has H...A distance 1.85(2) Å and angle 167(2) degrees.

## 5. Private reference results

The paper's conformer table contains conformer 1-1 with G = -1254.998003 kcal/mol, relative G = 0 and Boltzmann population 100.00%. The reported frontier orbital energies are EHOMO = -5.4012 eV and ELUMO = -0.9309 eV, giving a gap of 4.4703 eV (reported in the abstract as 4.47 eV). The paper says the optimized bond lengths, angles and torsions are roughly consistent with crystallography and within normal ranges; the detailed Table S1 values are not present in the supplied SI snapshot. The conclusion calls the DFT/X-ray structures basically coincident and identifies the intermolecular N-H...N hydrogen bond as central to packing.

## 6. Limitations and interpretation boundaries

The supplied supplementary document is a checkCIF/PLATON report rather than the referenced numerical Table S1, so hidden structural scoring must remain qualitative or use only explicitly reported crystallographic quantities. Gas-phase DFT and a single conformer search do not establish solution populations, crystal free energies, kinetic stability or biological mechanism. The paper's stability interpretation is a descriptor-level conclusion, not a measured thermodynamic stability constant.
