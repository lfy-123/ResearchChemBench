# Private paper route

## 1. Scientific objective and author claim

The paper tests whether local cut-wise reconstruction can recover insulin's global atomic mutual-information (AMI) and residue-level fragment mutual-information (FMI) map from overlapping quantum-chemical fragments. The authors claim that electronic correlations are sufficiently local that stitched fragment results reproduce the full-protein DFT correlation landscape, including chemically meaningful bonds and contacts.

## 2. System and model boundary

The system is the 51-residue, two-chain insulin structure represented by PDB 3I40 (782 protein atoms in the reported prepared system). Solvent and ions are removed before quantum calculations. AMI is the sum of orbital mutual informations over orbitals assigned to atoms; FMI is the sum of AMI over atoms assigned to residues. The principal reconstruction uses 51 spherical cuts centered at residue alpha carbons with radius 5.0 Å; 4.0 and 6.0 Å are sensitivity cases.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Prepare geometry | PDB 3I40 | GROMACS | protonation; steepest descent; OPLS-AA/TIP3P | minimized insulin | ev_doc_cd8dfb426e8c_000021_67214e12dfe9; ev_doc_cd8dfb426e8c_000025_96be81d97064 |
| 2 | Make local cuts | minimized insulin | geometric extraction and GROMACS restrained minimization | 51 alpha-carbon centers; 5.0 Å sphere; NH2/COOH caps; cap atoms excluded later | capped minimized fragments | ev_doc_cd8dfb426e8c_000025_96be81d97064; ev_doc_cd8dfb426e8c_000029_b67bbcbde83c |
| 3 | Compute electronic structure | each fragment and full protein | ORCA 6.0.1 DFT | omegaB97M-V/6-31G(d); solvent/ions absent | wavefunctions/RDMs | ev_doc_cd8dfb426e8c_000029_b67bbcbde83c; ev_doc_368a79886ed7_000037_72b97e797f54 |
| 4 | Coarse-grain correlation | wavefunctions | orbital RDM entropies and MI summation | AMI and FMI definitions in SI | fragment/full AMI and FMI | ev_doc_cd8dfb426e8c_000017_24233f4ebc49; ev_doc_cd8dfb426e8c_000018_d3be213b4a8c |
| 5 | Stitch and benchmark | fragment AMIs; full AMI | average all fragment contributions for each atom pair | overlap average; compare 5.0 Å stitch to full DFT | global reconstructed matrices and comparison | ev_doc_368a79886ed7_000037_72b97e797f54; ev_doc_368a79886ed7_000042_f199613825c5 |

## 4. Validation and analysis protocol

The authors compare stitched and full-protein AMI pair values, inspect scatter agreement and missing interactions, and inspect FMI heat maps/SPAWN plots. They examine disulfide pairs, peptide-bond bands, hydrogen-bond/helix patterns, and the Glu17(A)-Arg22(B) salt bridge across radii. Fragment preparation differences are assessed by RMSD; reported weighted mean RMSDs are 0.18, 0.15, and 0.17 Å for 4, 5, and 6 Å cuts.

## 5. Private reference results

The 5.0 Å stitched AMI scatter clusters near the identity relation with the full-protein calculation; interactions absent from the stitch are reported below 0.1 nat. FMI identifies Cys6A-Cys11A, Cys7A-Cys7B, and Cys20A-Cys19B disulfide correlations. The Glu17A-Arg22B salt bridge is absent at 4.0 Å and recovered at 5.0 and 6.0 Å. The source does not tabulate the individual Fig. 4 AMI values in the supplied evidence.

## 6. Limitations and interpretation boundaries

Locality makes long-range recovery dependent on overlap radius; fragment restrained minimization perturbs local geometry. Heat-map and semantic validation cannot substitute for unavailable tabulated pairwise values. The benchmark therefore scores reproducible protocol, coverage, matrix construction, and source-backed qualitative conclusions, and asks agents to report numerical metrics they actually obtain without imposing hidden target numbers.
