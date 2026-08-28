# Scientific objective

Determine, by an independently designed computational investigation, whether the closed Co/g-C3N4 model and its specified OER/ORR reaction network thermodynamically favor H2O2 or O2/H2O. Report relative Gibbs free-energy profiles, potential-determining steps (PDS), DeltaDeltaG_OER = PDS(O2)-PDS(H2O2), and the ORR free-energy change from *OOH to *+H2O2. Treat plausible electronic-state and thermochemical explanations as hypotheses to discriminate from your calculations.

# Public inputs and scientific boundaries

Use every labeled POSCAR and the accompanying `system_manifest.json`. `star` means the bare CoCN slab; `starOH`, `starO`, `starOOH`, `starOO`, and `starOH2` mean the correspondingly labeled adsorbate structures. Preserve atom identities and periodic cell. Gas references are the neutral molecules named in the manifest. The boundary is thermodynamic free energies at 298.15 K and 1 atm for the listed OER and ORR bookkeeping; kinetics, solvent structure, applied potential, rates and yields are outside scope. You may choose computational methods and generate vibrational/thermal corrections, but state all charge, multiplicity/spin, protonation and convergence choices.

# Required scientific validation/investigation

Formulate plausible competing explanations for the product preference, then calculate enough of the fixed network to discriminate them. Generate a finite, explicitly named set of spin/method/conformer alternatives, deduplicate equivalent structures, and advance only states with converged energies and chemically preserved connectivity. Validate at least electronic and ionic convergence, spin-state sensitivity, and the thermochemical reference convention; report failed jobs and uncertainty. For each branch identify its PDS as the largest uphill step under your stated convention. Completion requires either converged values for every required state and both product comparisons, or a bounded-failure report naming missing states, attempted coverage and the scientifically justified limitation. Stop when all required states have validated values or no additional in-scope calculation can resolve a documented failure.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include method provenance, per-state energies/free energies, branch steps, PDS identities, both selectivity metrics, validation evidence, proposed/discriminated hypotheses, conclusion and limitations. A bounded-failure branch is allowed only with the required missing-state and coverage fields.
