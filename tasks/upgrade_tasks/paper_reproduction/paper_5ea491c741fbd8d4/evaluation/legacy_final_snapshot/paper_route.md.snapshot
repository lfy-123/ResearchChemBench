# Private paper route

## 1. Scientific objective and author claim

For neutral singlet (E)-4-(4-methoxybenzylidene)-3-methylisoxazol-5(4H)-one (1a), the authors optimized the molecular geometry and calculated frontier molecular orbitals and Koopmans-style global descriptors. They report that the gas-phase HOMO–LUMO gap is 3.6191 eV and interpret this as a moderate gap consistent with chemical stability while retaining charge-transfer capability.

## 2. System and model boundary

The modeled object is one isolated molecule of 1a, formula C12H11NO3, in its neutral closed-shell singlet state. The scored core is the gas-phase optimized molecular structure and its HOMO energy, LUMO energy, and orbital-energy difference. Crystal packing, Hirshfeld contacts, docking, excited states, reaction chemistry, and biological efficacy are outside this core. The paper also reports a solvent-phase calculation, but does not identify the solvent or solvation model in the supplied evidence; it is therefore excluded from the reproducible benchmark.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish a molecular geometry for electronic analysis | Compound 1a, identified as the E isomer | Gaussian 09 | B3LYP hybrid density functional; 6-311+G(d,p) basis; gas phase | Optimized molecular geometry | Main paper §2.4 and §3.4; evidence `ev_doc_1eac271b4ab5_000083_c1754cccd4fc`, `ev_doc_1eac271b4ab5_000084_5e3cf62d1dce`, `ev_doc_1eac271b4ab5_000136_234f4666bf59` |
| 2 | Validate molecular geometry against experiment | Optimized geometry and X-ray structure | Structural overlay and parameter correlations | Bond lengths, bond angles, torsions; overlay RMSD | Correlation coefficients and RMSD | Main paper §3.4, Fig. 6, Tables S1–S3; evidence `ev_doc_1eac271b4ab5_000136_234f4666bf59` |
| 3 | Quantify frontier orbital energetics | Optimized geometry | Gaussian 09, B3LYP/6-311+G(d,p) | Gas phase; Koopmans approximation used for derived descriptors | HOMO energy, LUMO energy, gap and derived descriptors | Main paper §2.4, §3.4.1, Table 2; evidence `ev_doc_1eac271b4ab5_000084_5e3cf62d1dce`, `ev_doc_1eac271b4ab5_000138_ca43398f2872` |

## 4. Validation and analysis protocol

The authors compare optimized and X-ray geometries using an all-structure overlay RMSD and correlations of bond lengths, angles, and torsions. They then calculate HOMO and LUMO energies on the optimized structure, define the gap as ELUMO − EHOMO, and use orbital energies in Koopmans-style descriptors. No explicit vibrational-frequency check, conformer-search protocol, integration grid, convergence threshold, or solvent identity/model is reported in the supplied evidence.

## 5. Private reference results

Gas phase: EHOMO = -6.3362 eV; ELUMO = -2.7171 eV; gap = 3.6191 eV. Geometry/XRD comparison: overlay RMSD = 0.206 Å; bond-length, bond-angle, and torsion-angle correlation coefficients are 0.9881, 0.9968, and 0.9997. The authors describe the gap as moderate and associate it with stability plus possible charge-transfer behavior.

## 6. Limitations and interpretation boundaries

Kohn–Sham orbital gaps are model-dependent and are not experimental fundamental gaps. The paper's solvent result is not reproducible from the supplied method description because solvent and continuum model are unspecified. The crystal comparison includes packing-influenced experimental geometry, whereas the scored core is an isolated molecule. The paper provides no source-backed biological validation for inferring anticancer efficacy from these orbital quantities.
