# Scientific objective

Determine the internal electron (λe) and hole (λh) reorganization energies of the named compound BImCY2, 4-(1-(4-(cyanomethyl)phenyl)-4,5-diphenyl-1H-imidazol-2-yl)benzonitrile, using an independently selected computational protocol and a transparent adiabatic neutral/cation/anion energy cycle. Draw only scope-limited transport implications from the computed values.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret a smaller internal reorganization energy as a lower structural adjustment cost for the corresponding carrier. They propose that molecular twisting or non-planarity in BImCY2 may localize charge and increase this cost.

**Candidate route or mechanism.**
Consider charge-induced structural relaxation in a twisted molecular framework as a candidate explanation for the electron and hole reorganization energies. The authors’ computational approach uses density-functional geometry optimizations and single-point electronic energies to compare relaxed and unrelaxed charge states.

**Discriminating evidence.**
The authors use energy differences between neutral and ionized structures at optimized and cross-state geometries to quantify relaxation costs, then compare the resulting electron and hole reorganization energies to assess carrier tendencies. Use these computed costs to assess the proposed interpretation without inferring bulk mobility.

# Public inputs and scientific boundaries

Use `data/inputs/problem_definition.json`, which gives the source-supported chemical name, molecular formula, answer-neutral connectivity, charge/multiplicity states, units and physical boundary for BImCY2. Generate initial three-dimensional geometry or geometries from that connectivity. Evaluate neutral singlet, cation +1 doublet and anion -1 doublet. The target is internal structural reorganization energy of the isolated molecule; do not add solvent or a crystal environment. Limit transport implications to this molecular observable. Choose, justify and disclose a defensible protocol, and do not use the paper, SI or general web during the investigation.

# Required scientific validation/investigation

Generate and test your own explanations for the relative electron and hole reorganization energies. Generate and test your own explanations for the relative electron and hole reorganization energies. Generate and test your own explanations for the relative electron and hole reorganization energies. Independently plan and execute a complete direct calculation: generate defensible starting geometry or geometries, optimize neutral, cation and anion states, evaluate each charge state on its own optimized geometry and the required cross-state energies, convert units consistently, and show the algebra. Use the public labels `E_neutral_at_neutral`, `E_cation_at_neutral`, `E_anion_at_neutral`, `E_neutral_at_cation`, `E_cation_at_cation`, `E_neutral_at_anion`, and `E_anion_at_anion`. Compute λh = (`E_cation_at_neutral` − `E_cation_at_cation`) + (`E_neutral_at_cation` − `E_neutral_at_neutral`) and λe = (`E_anion_at_neutral` − `E_anion_at_anion`) + (`E_neutral_at_anion` − `E_neutral_at_neutral`). Validate convergence and charge/multiplicity separately for every named state, identify whether stationary-point/frequency checks were performed, and independently recompute λe and λh from submitted components. Success requires every energy term, reproducible arithmetic and stated limitations. Stop after this closed BImCY2 cycle is complete. If one or more states cannot be completed after documented reasonable attempts, submit the bounded-failure branch with all available partial state/energy evidence, failed-state diagnostics, attempted remedies and a scientific reason; do not invent missing values.

# Deliverables

Write `report/results.json` conforming to exactly one outcome branch of the local `submission_schema.json`. A success submission includes justified method choices; separately identified neutral, cation and anion records; all seven energy-cycle terms; λe and λh; per-state and cycle validation; a scope-limited comparison of the two carrier reorganization energies; and limitations. A bounded-failure submission includes the attempted method, all available partial state and energy evidence, failed states, missing terms, diagnostics, attempted remedies, conclusion and limitations, without placeholder numbers. Include paths or hashes that identify computational artifacts.
