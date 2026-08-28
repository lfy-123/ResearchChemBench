# Private paper route

## 1. Scientific objective and author claim

The paper studies the electrochemical bromination of diazo compounds with CBr4. For the model substrate 1a, the authors claim that anodic oxidation produces a carbon radical cation with prompt N2 extrusion; bromide capture and hydrogen-atom transfer from dichloromethane then lead to the alpha-bromo phosphonate. They also considered a competing route in which the radical cation is hydrogenated before N2 release.

## 2. System and model boundary

The computational model is the neutral, closed-shell singlet diazo phosphonate 1a, diethyl (diazo(phenyl)methyl)phosphonate, in dichloromethane represented with SMD. The authors' reported calculations include the reactant, transition structures, radical-cation intermediate A, and other intermediates along the proposed mechanism. The benchmark focuses on the activation Gibbs energies for the two competing first oxidation events, not on electrochemical electrode potentials or product-yield prediction.

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

These are single-level, implicit-solvent DFT results for a selected model system. They do not establish absolute electrochemical kinetics, electrode interfacial structure, all conformers, or a complete reaction network. Barrier comparison is meaningful only when the submitted states are the same chemical events and have documented stationary-point validation.
