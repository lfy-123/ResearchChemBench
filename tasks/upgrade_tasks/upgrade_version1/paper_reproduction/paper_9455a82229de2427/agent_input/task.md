# Scientific objective

Identify a finite, defensible set of cyclic SiNC5H7 products and distinguish thermodynamic compatibility from dynamical accessibility under a single collision.

# Author-provided scientific guidance

The source uses Gaussian 16 CBS-QB3 and a finite reaction PES; terminal addition, rearrangement, ring closure and H elimination motivate cyclic products. Published channels include two methylazasilacyclohexadienylidenes. They are hypotheses for PR, not compulsory winners. The benchmark additionally requires a main and an energetically competitive connected route with equal zero and explicit spin bookkeeping; full scattering/RRKM is not assumed.

# Public inputs and scientific boundaries

Reactants SiN (0, doublet) and isoprene C5H8 (0, singlet) produce SiNC5H7 (0, singlet) plus H (0, doublet). Doublet SiNC5H8 addition/rearrangement structures share the reactant atom map. Use separated reactants as zero for E0=Eelectronic+ZPE at 0 K. Collision energy 25±1 kJ/mol and experimental channel exoergicity -162±27 kJ/mol are observations, not computed answers. Enumerate terminal-C1/C4 attack by Si and N, then at least ring closure and H-loss alternatives. Declare explored bond edits and remaining search limits.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **candidate_space.** Cover `terminal_C1_Si`, `terminal_C4_Si`, `terminal_C1_N`, `terminal_C4_N`. Provide mapped graph-edit enumeration, attempted structures, state validity and products for the four attack families. Multiple seeds collapsing to one product are legitimate only with raw mapped evidence; no requirement for four distinct products. Required numeric fields are `lowest_E0_kJ_mol`, `product_reaction_E0_kJ_mol`.

2. **connected_routes.** Cover `main_route`, `competitor_route`. Submit ordered mapped nodes/edges, optimized endpoints, TS and IRC files or continuous no-barrier path evidence. Recompute all nodes relative to SiN+isoprene, including the free H atom. Required numeric fields are `maximum_relative_E0_kJ_mol`, `reaction_E0_kJ_mol`, `collision_margin_kJ_mol`.

3. **accessibility.** Cover `thermodynamic_vs_kinetic`, `method_sensitivity`. Separate lowest-energy product, channel exoergicity and accessible barrier. Compare collision margins and demonstrate method/ZPE sensitivity; no 298 K equilibrium abundance or branching ratio inference. Required numeric fields are `main_minus_competitor_kJ_mol`, `uncertainty_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Full scattering, exact branching ratios and a complete RRKM network are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
