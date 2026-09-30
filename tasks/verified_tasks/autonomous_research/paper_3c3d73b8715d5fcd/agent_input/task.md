# Scientific objective

For the supplied model 1,7-allenene 1D and Rh catalyst, independently discover and test the chemically plausible catalytic pathways connecting substrate to cycloisomerization and [2+2] products. Quantify the solution-phase Gibbs free-energy profile at 298.15 K in 1,4-dioxane, identify the kinetically controlling event, and compare the two OCM alternatives. No author mechanism is supplied; formulate and discriminate hypotheses from the structures and calculations.

# Public inputs and scientific boundaries

`data/inputs/model_substrate_1D.xyz` is the neutral singlet model substrate 1D; `data/inputs/rhodium_catalyst.xyz` is neutral singlet [Rh(CO)2Cl]2. Coordinates are in Angstrom and XYZ atom labels are authoritative. The system is limited to these species, their monomeric Rh representation if used, optional explicitly modeled CO, and stationary points connecting them. Measure frequencies, validated connectivity, relative Gibbs free energies in 1,4-dioxane at 298.15 K, the cycloisomerization activation free energy, and the endo/exo-OCM transition-state difference. Choose and report software, model chemistry, conformer strategy, standard states, thermal and solvation treatments. Do not claim experimental yields.

For quantitative comparison, use 1 M standard states for molecular solutes and 8.5 mM for free CO in 1,4-dioxane at 298.15 K. Balance all species, including released CO, against one common catalyst/substrate reference. Define the endo/exo difference as G(TS_exo) − G(TS_endo); identify the actual resting-state and controlling-TS pair used for the overall activation free energy. State any alternative convention separately so its energies are not compared as if identical.

# Required scientific validation/investigation

Define a finite candidate-generation strategy covering at least catalyst coordination, both possible OCM orientations, cycloisomerization, and [2+2] closure; explain why additional hypotheses were or were not explored. Deduplicate by connectivity and meaningful conformational identity while retaining per-candidate identity. Optimize and validate minima with zero imaginary frequencies and transition states with one imaginary frequency and a mode or IRC/alternative test connecting the assigned neighbors. Advance only converged, chemically continuous candidates. Report all attempted candidates, failures and coverage. Completion requires either a validated path for each requested channel or a bounded-failure account with all missing validations and attempted alternatives; stop when the stated generation strategy yields no new validated connectivity and report that stopping basis.

Keep successful main-path candidate records in `candidates`; place unsuccessful extra attempts in the optional `attempts` list. A `partial` or `bounded_failure` report may have no candidate geometry, frequency or energy yet; omit unavailable fields and give the actual diagnostics in `failure_account`. Do not claim complete channel coverage from a partial calculation.

Generic limitations or uncertainty prose is optional and unscored. Keep the required scientific identities, computed evidence, coverage and actual failure diagnostics. Additional scientifically motivated calculations are allowed and should be separated from the primary results; optional work not performed needs no disclaimer.

# Deliverables

Submit `report/results.json` conforming to the schema. In the complete branch, include hypotheses, method/settings and energy assembly, an explicit identity and input-geometry link for every attempted candidate, per-candidate outcome, validation evidence, energies, requested observables and conclusion. If the required validated paths cannot be completed after the finite search, use the bounded-failure or partial branch: report all hypotheses, attempted candidates and failures, coverage and stopping basis in `failure_account`, and do not fabricate missing energies or observables. Do not invent a discovery narrative unsupported by calculations.
