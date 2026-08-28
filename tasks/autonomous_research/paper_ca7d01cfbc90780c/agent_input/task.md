# Scientific objective

Determine, by independent computation, whether the explicitly identified A36 molecule forms a stable, specifically anchored complex with human ATM kinase (PDB 6I3U) under explicit-solvent atomistic simulation. Measure complex/protein Cα-backbone RMSD versus time, residue RMSF, and intermolecular hydrogen-bond occupancy/count, and use them to reach a defensible stability conclusion. Do not treat docking score as binding affinity.

# Public inputs and scientific boundaries

Retrieve PDB entry 6I3U from RCSB and the exact-name PubChem record specified in `data/inputs/input_manifest.json`; record immutable retrieval identifiers and formal charge. Generate the 3-D ligand and initial pose independently. The system boundary is ATM plus A36, water, counterions and salt. State force field, water, protonation, box, ionic strength, minimization, equilibration, production length/timestep, restraints, random seed(s), trajectory imaging and analysis definitions. The paper/SI, general web searching and copying any paper-derived docked pose are disallowed. No author mechanism or candidate ranking is supplied.

# Required scientific validation/investigation

Generate and deduplicate a finite set of plausible active-site poses, documenting pose identity and selection criteria; advance at least one pose to a physically stable solvated simulation. Validate minimization, thermodynamic stability, steric behavior, ligand retention or explained escape, and convergence/plateau behavior using block or time-window analysis. Analyze the complete production trajectory and state atom selections and hydrogen-bond geometric criteria. Completion requires either a validated production trajectory of at least 100 ns or a bounded-failure report explaining why that endpoint was not reached. Stop after the planned endpoint and validation criteria are met; otherwise stop at the declared resource limit and report search coverage, failure and limitations without fabricating values.

# Deliverables

Submit `report/results.json` plus referenced plots/data and a concise methods report. JSON must identify retrieved records, pose IDs, protocol, validation observations, RMSD post-equilibration summary, RMSF summary, hydrogen-bond summary, independently reasoned conclusion and limitations. Every numeric value needs units, time window and uncertainty/replicate context. A bounded-failure branch is valid but must include completed work, stopping reason and limitations.
