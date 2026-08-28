# Scientific objective

Test whether the explicitly identified A36 molecule forms a stable, specifically anchored complex with human ATM kinase (PDB 6I3U) under explicit-solvent atomistic simulation. The authors proposed that the heteroaromatic core anchors in the hinge region and the basic side chain occupies the adjacent pocket; independently design calculations to test this hypothesis. Measure complex/protein Cα-backbone RMSD versus time, residue RMSF, and intermolecular hydrogen-bond occupancy/count. Do not treat docking score as binding affinity.

# Public inputs and scientific boundaries

Retrieve PDB entry 6I3U from RCSB and the exact-name PubChem record specified in `data/inputs/input_manifest.json`; record immutable retrieval identifiers and formal charge. Generate the 3-D ligand and an initial pose independently. The system boundary is ATM plus A36, water, counterions and salt. A fair protocol must state force field, water, protonation, box, ionic strength, minimization, equilibration, production length/timestep, restraints, random seed(s), trajectory imaging and analysis definitions. The paper/SI, general web searching and copying the paper’s supplementary docked pose are disallowed. The reported experimental activity is context only.

# Required scientific validation/investigation

Generate and deduplicate a finite set of plausible active-site poses, documenting the pose identity and selection criteria; advance at least one pose to a physically stable solvated simulation. Validate energy minimization, temperature/pressure stability, absence of persistent severe steric clashes, ligand retention or a scientifically explained escape, and convergence/plateau behavior using block or time-window analysis. Analyze the complete production trajectory and state atom selections and hydrogen-bond geometric criteria. Completion requires either a validated production trajectory of at least 100 ns or a bounded-failure report explaining why that endpoint was not reached. Stop after the planned endpoint and validation criteria are met; if resources prevent this, stop at the declared limit and report coverage, failure and limitations rather than fabricating values.

# Deliverables

Submit `report/results.json` plus referenced plots/data and a concise methods report. JSON must identify the retrieved records, pose IDs, protocol, validation observations, RMSD post-equilibration summary, RMSF summary, hydrogen-bond summary, conclusion and limitations. Every numeric value needs units, time window and uncertainty/replicate context. A bounded-failure branch is valid but must include completed work, stopping reason and limitations.
