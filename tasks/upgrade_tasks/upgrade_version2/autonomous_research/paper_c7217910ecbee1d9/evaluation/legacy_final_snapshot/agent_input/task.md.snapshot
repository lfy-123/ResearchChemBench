# Scientific objective

Compute the adiabatic electron affinity (AEA) of the explicitly specified isolated PAl12[B(C6F5)3]2 cluster by independently locating and validating suitable neutral and singly anionic electronic states. Determine whether the optimized states preserve the specified PAl12 metal-core framework. Report a reproducible computational conclusion supported by endpoint energies and structural evidence.

# Public inputs and scientific boundaries

AEA = E(neutral minimum) − E(anion minimum), in eV. State whether ZPE is included and retain separate electronic and ZPE terms where computed; use a consistent convention for both charge states. Framework retention here means structural preservation of the specified PAl12 core and ligand connectivity, not an additional electronic-shell or superatom-orbital proof.

Use `data/inputs/system_specification.json`. It uniquely specifies one P atom, twelve Al atoms, two intact neutral B(C6F5)3 ligands, the neutral charge-0 state and charge −1 state, and an isolated gas-phase boundary. You may generate 3-D conformers and computational models. No graphene, solvent, counterion, periodic cell, atom substitution, protonation, or omitted ligand is allowed. No author route, candidate ranking, result direction, or reference numerical result is part of this task.

# Required scientific validation/investigation

Propose and justify your own candidate-generation strategy for ligand orientations/binding-site arrangements and plausible spin multiplicities for both charge states. Explore a finite, explicitly listed set, deduplicate with a stated structural criterion, optimize advanced candidates, and retain energies and convergence information. Validate each selected endpoint as a stationary minimum with a frequency calculation or clearly justified equivalent; report imaginary-mode results and failed candidates. Completion requires at least one independently generated starting geometry per state, a coverage table, and a selection record: Compute AEA from validated endpoint energies, state ZPE treatment, compare the optimized core connectivity/framework with the public specification, and distinguish computed facts from hypotheses. Support the selected lowest-energy structures with the actual candidate energies and structural checks; additional exploration is allowed.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`. Include your scientific rationale, method/software, atom ordering/mapping, candidate identities and validation context, endpoint structures or coordinate-file paths, neutral and anion energies, AEA with units and ZPE convention, calculation coverage evidence, framework comparison, final conclusion. A bounded failure is acceptable only when all attempted calculations and missing closure are honestly documented.
