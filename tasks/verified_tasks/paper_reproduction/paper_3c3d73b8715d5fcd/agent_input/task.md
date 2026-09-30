# Scientific objective

Determine, for the supplied model 1,7-allenene 1D and Rh catalyst, whether an independently planned quantum-chemical investigation supports the proposed endo-oxidative-cyclometalation route and quantify the solution-phase Gibbs free-energy profile for the cycloisomerization and competing [2+2] channel. Report the activation free energy for the cycloisomerization and the transition-state energy difference between endo- and exo-OCM.

# Author-provided scientific guidance

The author hypothesis is that the reaction begins by catalyst coordination followed by endo-OCM; treat this as a hypothesis to test, not as an assumed result.

# Public inputs and scientific boundaries

`data/inputs/model_substrate_1D.xyz` is the neutral singlet model substrate 1D; `data/inputs/rhodium_catalyst.xyz` is neutral singlet [Rh(CO)2Cl]2. Coordinates are in Angstrom and the XYZ atom labels are authoritative. The chemical system is limited to these species, their monomeric Rh representation if used, optional CO explicitly reported in the calculation, and stationary points connecting them. The measured quantities are stationary-point frequencies, relative Gibbs free energies in 1,4-dioxane at 298.15 K, the cycloisomerization activation free energy, and the endo/exo-OCM transition-state difference. Do not claim experimental yields or structures not computed. You may choose software, model chemistry, conformer strategy and execution order, but state them and state standard states and thermal/solvation treatments.

For quantitative comparison, use 1 M standard states for molecular solutes and 8.5 mM for free CO in 1,4-dioxane at 298.15 K. Balance all species, including released CO, against one common catalyst/substrate reference. Define the endo/exo difference as G(TS_exo) − G(TS_endo); identify the actual resting-state and controlling-TS pair used for the overall activation free energy. State any alternative convention separately so its energies are not compared as if identical.

# Required scientific validation/investigation

Generate a finite, identity-preserving set of conformers and pathway guesses for catalyst coordination, endo-OCM, exo-OCM, [2+2] reductive elimination and the cycloisomerization sequence. Deduplicate by connectivity and meaningful conformational identity, and retain the mapping from each candidate to its input geometry. Optimize candidates and validate minima by zero imaginary frequencies and transition states by one imaginary frequency whose mode connects the claimed neighboring structures; use an IRC or an explicitly justified alternative connectivity test. Advance only candidates with chemically continuous connectivity and converged calculations. Assemble energies with one internally consistent reference and report every attempted candidate and failure. The investigation is complete when both OCM alternatives and at least one complete cycloisomerization path plus the [2+2] competitor have passed structural validation or are explicitly documented as bounded failures; stop after no new validated connectivity is found from the stated search generation strategy and report coverage.

Keep successful main-path candidate records in `candidates`; place unsuccessful extra attempts in the optional `attempts` list. A `partial` or `bounded_failure` report may have no candidate geometry, frequency or energy yet; omit unavailable fields and give the actual diagnostics in `failure_account`. Do not claim complete channel coverage from a partial calculation.

Generic limitations or uncertainty prose is optional and unscored. Keep the required scientific identities, computed evidence, coverage and actual failure diagnostics. Additional scientifically motivated calculations are allowed and should be separated from the primary results; optional work not performed needs no disclaimer.

# Deliverables

Submit `report/results.json` conforming to the schema. In the complete branch, include method/settings, an explicit identity and input-geometry link for every attempted candidate, per-candidate outcome, validation evidence, relative energies, requested observables, conclusion and completion status. If the required validated paths cannot be completed after the finite search, use the bounded-failure or partial branch: report every attempted candidate and failure, coverage and stopping basis in `failure_account`, and do not fabricate missing energies or observables.
