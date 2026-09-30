# Private paper route

## 1. Scientific objective and author claim

The paper studies the electrochemical bromination of diazo compounds with CBr4. For the model substrate 1a, the authors claim that anodic oxidation produces a carbon radical cation with prompt N2 extrusion; bromide capture and hydrogen-atom transfer from dichloromethane then lead to the alpha-bromo phosphonate. They also considered a competing route in which the radical cation is hydrogenated before N2 release.

## 2. System and model boundary

The SI coordinate model labelled 1a is neutral dimethyl (diazo(phenyl)methyl)phosphonate, C9H11N2O3P, in SMD dichloromethane. The former public diethyl identity has been corrected to this 26-atom source composition. This does not establish the charges, multiplicities or reference energies of the oxidation transition states: the alternative SI block includes Br, whereas the public scored boundary excludes Br. The benchmark's two-event comparison is retained, but its numerical reference is not qualified until this boundary and the electron reference are reconciled.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the 1a reactant | 1a geometry | Gaussian 16 DFT optimization and frequency | B3LYP-D3/6-311+G(d,p), SMD dichloromethane | Minimum and Gibbs free energy | ev_doc_5f0fe876b254_000140_0b2666c4c34d; ev_doc_5f0fe876b254_000141_a84585769cbf |
| 2 | Locate the N2-loss oxidation transition structure | 1a and TS guess | Gaussian 16 DFT optimization and frequency | Same level and solvent | TS-1a and one imaginary frequency | ev_doc_5f0fe876b254_000142_7ce5d173afe9; ev_doc_5f0fe876b254_000144_3f6fa745de9d |
| 3 | Verify the intended reaction connection | optimized TS-1a | IRC | Same electronic-structure model and SMD solvent | Connection to 1a and A | ev_doc_5f0fe876b254_000142_7ce5d173afe9 |
| 4 | Compute the competing N2-loss barrier | 1a and TS-1a thermochemistry | Gibbs free-energy difference | Same level and solvent | activation Gibbs energy | ev_doc_bd2093e21cd6_000124_ce5347799950; ev_doc_bd2093e21cd6_000141_f986bec8671a |
| 5 | Locate the N2-retention oxidation transition structure | 1a and alternative TS guess | Gaussian 16 DFT optimization and frequency | Same level and solvent | alternative TS and one imaginary frequency | ev_doc_5f0fe876b254_000142_7ce5d173afe9; ev_doc_5f0fe876b254_000146_e1ad406530e5 |
| 6 | Compute the competing N2-retention barrier | 1a and alternative TS thermochemistry | Gibbs free-energy difference | Same level and solvent | activation Gibbs energy | ev_doc_bd2093e21cd6_000136_9e14b75c5690; ev_doc_bd2093e21cd6_000137_a8be1d8ef289 |

## 4. Validation and analysis protocol

The source protocol requires frequency confirmation of minima (zero imaginary frequencies) and transition structures (one imaginary frequency), plus IRC verification of the intended saddle-point connections. The two barriers are compared on the same Gibbs free-energy convention and the mechanistic interpretation is limited to relative favorability of the modeled oxidation events.

## 5. Private reference results

The reported activation Gibbs energy for the prompt N2-extrusion route is 28.3 kcal/mol. The reported activation Gibbs energy for the N2-retention route is 34.3 kcal/mol. Thus the modeled prompt N2-extrusion route is lower by 6.0 kcal/mol. The main paper describes the former as delivering radical-cation A and the latter as less favorable.

## 6. Limitations and interpretation boundaries

These are source-reported single-level implicit-solvent DFT results. The route table describes the claimed intended steps, not a fully recovered executable protocol. SI S17 specifies B3LYP/6-311+G(d,p), SMD(DCM), with D3 and a BJ-damping reference. The SI printed G(TS-1a) minus G(1a) equals 32.463575 kcal/mol, not the main-text 28.3. The alternative block's neutral electron count is 153, incompatible with a singlet; its intended charge/multiplicity and electrochemical zero remain unresolved. Do not guess a charge, remove Br, or relabel the old diethyl computations as author reproduction. The 28.3/34.3 values and tolerances remain unchanged pending source reconciliation; this task is blocked, not validated (2026-09-25).
