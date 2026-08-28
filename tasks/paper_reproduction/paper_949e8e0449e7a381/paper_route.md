# Private paper route

## 1. Scientific objective and author claim

The paper explains the improved catalytic performance of MnKstD2 A395G toward 4-PG by changes in the enzyme–substrate–FAD pre-reaction geometry. The authors claim that replacing Ala395 with Gly reduces steric hindrance, stabilizes 4-PG near FAD N5 and catalytic Tyr359/Tyr532, increases the population of productive conformations, and is consistent with improved kinetic performance.

## 2. System and model boundary

The system is MnKstD2 from *Mycolicibacterium neoaurum* ATCC 25795 (GenBank AHG53938), in WT and A395G forms, with FAD and the steroid substrate Δ4,16(17)-diene-progesterone (4-PG). The paper uses an AlphaFold2 model, docking of FAD/4-PG, explicit TIP3P water, and classical MD; its analysis concerns distances C1(4-PG)–N5(FAD), C2(4-PG)–OH(Tyr359), OH(Tyr532)–O3(4-PG) hydrogen bonding, and backbone RMSD/RMSF.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain enzyme model and identify binding-site positions | MnKstD2 sequence; FAD and 4-PG | AlphaFold2/ColabFold; AutoDock Vina; PyMOL | Highest-confidence AF2 model; Vina default parameters; lowest-energy docked configuration; 23 residues within 5 Å of docked 4-PG considered for mutagenesis | Protein–ligand starting model and mutagenesis set | ev_doc_1b2bad0c80f2_000124_a49ebd25638d; ev_doc_1b2bad0c80f2_000265* |
| 2 | Parameterize nonstandard components | Docked 4-PG and FAD | Gaussian 16; ACPYPE/AmberTools | Geometry optimization and RESP charges | GROMACS-compatible ligand/cofactor parameters | ev_doc_1b2bad0c80f2_000355_49d133a7327c |
| 3 | Sample WT and mutant complexes | WT and A395G complexes | GROMACS/Amber workflow | Cubic TIP3P box, 10 Å padding; three minimizations; 0–300 K NVT heating for 500 ps; 500 ps unrestrained equilibration; 50 ns NPT production and reported additional 100 ns equilibration; 2 fs step | Trajectories | ev_doc_1b2bad0c80f2_000355_49d133a7327c |
| 4 | Analyze catalytic geometry and stability | Trajectories | Amber 20 analyses | Distance distributions, productive-frame fraction, backbone RMSD/RMSF, hydrogen-bond occupancy; lowest-energy frame used as representative complex | Comparative WT/A395G geometry and interaction results | ev_doc_1b2bad0c80f2_000355_49d133a7327c; ev_doc_1b2bad0c80f2_000229* |

## 4. Validation and analysis protocol

The authors compare WT and A395G under the same simulation setup, quantify the two reaction-coordinate distances and the fraction of frames meeting the chosen productive-geometry criteria, inspect backbone RMSD/RMSF, and compare OH(Y532)–O3 substrate hydrogen-bond occupancy. They relate the structural result to the reported kinetic trend and to the 1.47-fold kcat increase of A395G.

## 5. Private reference results

The paper reports productive conformations in 48.2% of WT frames and 95.7% of A395G frames. Representative C1–N5 distances are 4.1 Å (WT) and 3.4 Å (A395G); the C3-keto-group interaction distance to catalytic tyrosine hydroxyls is reported as 5.1 Å and 2.7 Å, respectively. OH(Y532)–O3 substrate hydrogen-bond occupancy is 6.1-fold higher for A395G. A395G has reduced backbone structural fluctuations, and its kcat is 1.47-fold higher; catalytic efficiency is reported as 2.6-fold higher. These are hidden evaluator references, not public task inputs.

## 6. Limitations and interpretation boundaries

The source does not provide deposited coordinates for the exact AF2 model, complete trajectory files, uncertainty estimates, or a fully specified force-field/version. The benchmark therefore scores reproducible comparative trends and explicitly reported observables, accepts independent model chemistry, and requires reporting of model, protonation, conformer, sampling, convergence, and sensitivity limitations. MM-PBSA is not used as the central scored objective because the supplied source evidence does not expose its numerical values.
