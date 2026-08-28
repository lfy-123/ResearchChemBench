# Scientific objective

Determine, by an independently planned periodic electronic-structure calculation, the thermodynamic ORR overpotential and active-site sulfur p-band center for the specified Ni-substituted 2H-MoS2(001) basal-plane model. Test the authors' qualitative hypothesis that substitutional transition-metal doping can activate a basal-plane sulfur site through electronic/structural reorganization; do not assume a particular numerical outcome or adsorption geometry.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. Resolve host structure only from Materials Project record mp-2815 (2H-MoS2), cleave the (001) surface, make the stated 3x3x1 periodic slab with 15 Å vacuum, and replace exactly one Mo site with Ni. Preserve charge, stoichiometry, periodicity, and explicit atom indexing in every submitted structure. The measured quantities are the CHE free energies for OOH*, O*, and OH* along the associative four-electron ORR sequence at U=0 V, pH=0, T=298.15 K, the resulting overpotential η, and the 3p projected-band first moment εp of one explicitly identified top-layer S atom directly bonded to the Ni neighborhood. No paper/SI or general-web searching is allowed; controlled database access is limited to mp-2815.

# Required scientific validation/investigation

Report the independent computational method, magnetic/charge state, slab and adsorption conformer generation, relaxation convergence, k-point/cutoff choices, CHE corrections, and p-band integration window/reference. Validate that the final slab is the stated composition and periodic model, that each OOH*/O*/OH* state is a stationary relaxed state (or clearly label an alternative validation and its limitation), and that the free-energy bookkeeping uses the same four elementary proton/electron steps. Identify the potential-determining step from the submitted ΔG values. Completion requires either a converged validated result for all requested observables or a bounded-failure report naming the failed state, diagnostics, attempted alternatives, and uncertainty. Stop after the declared convergence tests and adsorption-conformer search are exhausted; if resources prevent that, stop and report coverage and limitations rather than inventing values.

# Deliverables

Submit `report/results.json` matching `submission_schema.json`, including object identity, numerical observables with units, four ΔG values, PDS, validation evidence, method provenance, and a final conclusion. A bounded-failure branch is permitted but must contain truthful diagnostics and coverage.
