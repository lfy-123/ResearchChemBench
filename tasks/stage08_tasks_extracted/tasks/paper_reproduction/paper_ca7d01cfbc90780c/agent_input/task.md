# Scientific objective

Determine, by independent computation, whether the explicitly identified A36 molecule forms a stable, specifically anchored complex with human ATM kinase (PDB 6I3U) under explicit-solvent atomistic simulation. Measure complex/protein Cα-backbone RMSD versus time, residue RMSF, and intermolecular hydrogen-bond occupancy/count, and use them to reach a defensible stability conclusion. Do not treat docking score as binding affinity.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that A36 remains stably bound in the ATM active-site cavity and retains specific protein contacts during an atomistic simulation. They further interpret the binding as specifically anchored through contacts in the active-site region.

**Candidate route or mechanism.**
A candidate starting model places A36 in the ATM active-site cavity, with its heteroaromatic core oriented toward the hinge region and its basic side chain toward the adjacent pocket. Treat this as a proposed route for pose generation and testing, while allowing alternative poses within the defined active site.

**Discriminating evidence.**
Use protein Cα-backbone RMSD over time, residue RMSF, and intermolecular hydrogen-bond occupancy/count together to test retention, structural stability, and persistence of specific contacts. Assess these observables over the complete production trajectory with equilibration and time-window or block comparisons.

# Public inputs and scientific boundaries

Retrieve PDB entry 6I3U from RCSB and the exact-name PubChem record specified in `data/inputs/input_manifest.json`; record immutable retrieval identifiers and formal charge. Generate the 3-D ligand and initial pose independently. The scored system is ATM plus A36, water, counterions and salt; do not add a host or solvent beyond this explicit-solvent system. State force field, water, protonation, box, ionic strength, minimization, equilibration, production length/timestep, restraints, random seed(s), trajectory imaging and analysis definitions.

# Required scientific validation/investigation

Generate and deduplicate a finite set of plausible active-site poses, documenting pose identity and selection criteria; advance at least one pose to a physically stable solvated simulation. Validate minimization, thermodynamic stability, steric behavior, ligand retention or explained escape, and convergence/plateau behavior using block or time-window analysis. Analyze the complete production trajectory and state atom selections and hydrogen-bond geometric criteria. Completion requires either a validated production trajectory of at least 100 ns or a bounded-failure report explaining why that endpoint was not reached. Stop after the planned endpoint and validation criteria are met; otherwise stop at the declared resource limit and report search coverage, failure and limitations without fabricating values.

# Deliverables

Submit `report/results.json` plus referenced plots/data and a concise methods report. JSON must identify retrieved records, pose IDs, protocol, validation observations, RMSD post-equilibration summary, RMSF summary, hydrogen-bond summary, independently reasoned conclusion and limitations. Every numeric value needs units, time window and uncertainty/replicate context. A bounded-failure branch is valid but must include completed work, stopping reason and limitations.
