# Scientific objective

For the supplied model 1,7-allenene 1D and Rh catalyst, independently discover and test chemically plausible catalytic pathways connecting substrate to cycloisomerization and [2+2] products. Quantify the solution-phase Gibbs free-energy profile at 298.15 K in 1,4-dioxane, identify the kinetically controlling event, and compare the two OCM alternatives.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the reaction begins with catalyst coordination followed by endo oxidative cyclometalation (endo-OCM), and interpret this as the initiating event for the cycloisomerization sequence. This proposed explanation should be tested against the supplied model and competing channel.

**Candidate route or mechanism.**
Prioritize a candidate sequence from coordinated substrate through endo-OCM and downstream cycloisomerization steps, while explicitly considering the alternative exo-OCM orientation and competing [2+2] closure. Treat these as proposed candidates requiring validation.

**Discriminating evidence.**
Use optimized stationary points, frequency counts, and a transition-state mode plus IRC or another justified connectivity test to establish the proposed sequence and alternatives. Compare consistently assembled solution-phase Gibbs free energies for the OCM alternatives and the cycloisomerization and [2+2] channels, retaining candidate identity throughout.

# Public inputs and scientific boundaries

`data/inputs/model_substrate_1D.xyz` is the neutral singlet model substrate 1D; `data/inputs/rhodium_catalyst.xyz` is neutral singlet [Rh(CO)2Cl]2. Coordinates are in Angstrom and XYZ atom labels are authoritative. The scored system is the isolated molecule: use only these species, their monomeric Rh representation if used, optional explicitly modeled CO, and stationary points connecting them; do not add a host or solvent. Measure frequencies, validated connectivity, relative Gibbs free energies in 1,4-dioxane at 298.15 K, the cycloisomerization activation free energy, and the endo/exo-OCM transition-state difference. Choose and report software, model chemistry, conformer strategy, standard states, thermal and solvation treatments. Do not claim experimental yields.

# Required scientific validation/investigation

Define a finite candidate-generation strategy covering catalyst coordination, both orientations needed for the requested OCM comparison, cycloisomerization, and [2+2] closure; explain why additional hypotheses were or were not explored. Deduplicate by connectivity and meaningful conformational identity while retaining per-candidate identity. Optimize and validate minima with zero imaginary frequencies and transition states with one imaginary frequency and a mode or IRC/alternative test connecting the assigned neighbors. Advance only converged, chemically continuous candidates. Report all attempted candidates, failures, coverage and limitations. Completion requires either a validated path for each requested channel or a bounded-failure account with all missing validations and attempted alternatives; stop when the stated generation strategy yields no new validated connectivity and report that stopping basis.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. In the complete branch, include hypotheses, method/settings and energy assembly, an explicit identity and input-geometry link for every attempted candidate, per-candidate outcome, validation evidence, energies, requested observables, conclusion and limitations. If the required validated paths cannot be completed after the finite search, use the bounded-failure or partial branch: report all hypotheses, attempted candidates and failures, coverage and stopping basis in `failure_account`, and do not fabricate missing energies or observables. Do not invent a discovery narrative unsupported by calculations.
