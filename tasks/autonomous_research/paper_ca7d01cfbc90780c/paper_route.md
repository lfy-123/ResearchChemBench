# Private paper route

## 1. Scientific objective and author claim

The authors used docking and atomistic molecular dynamics to support the structural rationale for the optimized ATM inhibitor A36. Their claim is that A36 remains stably bound in the ATM active-site cavity and retains specific protein contacts during a 100 ns simulation.

## 2. System and model boundary

The simulated system is human ATM kinase bound to A36. The receptor starting structure is PDB 6I3U. The SI specifies a periodic cubic box, AMBER14SB protein force field, TIP3P water, physiological 150 mM NaCl, restrained NPT equilibration for 100 ps after minimization, and 100 ns production with a 2 fs integration step. Analyses concern protein Cα-backbone RMSD, residue RMSF, radius of gyration, SASA, and intermolecular hydrogen bonds.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Select a structural model for the A36 complex | ATM PDB 6I3U and A36 | Molecular docking; software not specified in the paper | Active-site cavity; qualitative contacts to ILE685, Trp684, Tyr670, Lys636 and Asp762 | Docked A36–ATM model | ev_doc_53b029e6367b_000178_8060773c9bf0 |
| 2 | Build solvated MD system | Docked complex | GROMACS 2025.3; AMBER14SB/TIP3P; ligand topology from sobtop | Cubic periodic box; 150 mM NaCl | Solvated, neutralized system | ev_doc_baa6d3d5842e_000040_cc9eacd9ead2 |
| 3 | Relax and equilibrate | Solvated system | Energy minimization and restrained NPT | 100 ps stepwise NPT; heavy-atom position restraints | Equilibrated complex | ev_doc_baa6d3d5842e_000040_cc9eacd9ead2 |
| 4 | Sample binding stability | Equilibrated complex | GROMACS MD | 100 ns; 2 fs timestep | Trajectory | ev_doc_53b029e6367b_000179_fe09f533d7be; ev_doc_baa6d3d5842e_000040_cc9eacd9ead2 |
| 5 | Quantify stability and contacts | Centered, PBC-corrected trajectory | Trajectory analysis (implementation not named) | Cα-backbone RMSD, RMSF, Rg, SASA, protein–ligand H bonds | Time series and residue metrics | ev_doc_baa6d3d5842e_000180_072fce83b0e8; ev_doc_baa6d3d5842e_000040_cc9eacd9ead2 |

## 4. Validation and analysis protocol

The paper interprets equilibration from the complex RMSD trace, reports the post-equilibration RMSD level, summarizes the RMSF distribution, and counts intermolecular hydrogen bonds over time. The authors use these jointly as evidence for a stable, specifically anchored complex; the conclusions are qualitative and do not establish binding free energy.

## 5. Private reference results

The published trace reaches equilibrium at approximately 60 ns and fluctuates around 2.1 Å thereafter. RMSF values are mostly below 2.3 Å. Protein–A36 hydrogen bonds range from 0 to 2 and predominantly number 1. The authors conclude that A36–ATM binding is stable, with tight RMSD convergence, low residue flexibility, and sustained intermolecular hydrogen bonding.

## 6. Limitations and interpretation boundaries

The paper does not disclose every MD control parameter, replicate/seed, docking score, or analysis implementation. The docking pose is referenced as a supplementary PDB asset but is not present in the supplied SI text. These omissions make exact numerical reproduction impossible; fair evaluation therefore rewards an independently documented, reproducible protocol and source-consistent qualitative/quantitative trends, not identity with an undisclosed trajectory.
