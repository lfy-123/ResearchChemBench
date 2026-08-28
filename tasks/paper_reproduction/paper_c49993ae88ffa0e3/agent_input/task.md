# Scientific objective

Independently test the authors' qualitative hypothesis that the first reducing hydrogen-equivalent transfer from lowest-singlet photoexcited 9,10-phenanthrenehydroquinone (H₂PQ) to pyridine N-oxide (PyO) can occur by either proton transfer followed by electron transfer or electron transfer followed by proton transfer, and that explicit water can alter the stability of the ionic intermediates. Compute the solution Gibbs free energy of the first proton-transfer endpoint and the first electron-transfer endpoint, each without and with the defined explicit-water model, then state what these results do and do not support. The hypothesis is not a result: do not assume either order is favorable or preferred.

# Public inputs and scientific boundaries

Use `data/inputs/system.json` for the unique molecular graphs, charges, state identities and four endpoint classes, and `data/inputs/conditions.json` for the thermodynamic equations and reporting conditions. The research object is H₂PQ + unsubstituted PyO, not a substituted catalyst or substrate. Report ΔG in kcal/mol at 298.15 K and a 1 M solution convention in acetonitrile. For hydrated comparisons use exactly two explicit waters total—one associated with each fragment—on both sides of the comparison. The target is the first elementary event only; rates, the second hydrogen transfer and overall deoxygenation are outside scope.

# Required scientific validation/investigation

Generate three-dimensional structures independently. For each of `pt_dry`, `et_dry`, `pt_hydrated` and `et_hydrated`, generate distinct chemically reasonable conformers or encounter/water-placement motifs, deduplicate them by connectivity, proton location, charge/spin state and geometric similarity, and retain per-candidate identity and validation evidence. Advance candidates until additional distinct starting motifs repeatedly relax to already represented minima or remain outside the stated energy window used for ensemble convergence. Validate endpoint connectivity, proton location, total charge, multiplicity/open-shell coupling, excited-state character where applicable, and stationary-point character or provide an equivalent endpoint-validity test. Use consistent standard states and quantify either method/solvation sensitivity or why it remains a limitation. A successful investigation is complete when all four endpoint classes have comparable validated ensembles, numerical ΔG values, water-induced shifts, and a supported conclusion. Stop when the stated convergence rule is met or when the available method repeatedly fails after chemically distinct starts; in the latter bounded-failure case, report attempted states, diagnostics, partial values that are scientifically valid, and the resulting limitation without fabricating missing numbers.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For success, include the computational method, common reference convention, per-state ΔG values, individual candidate records with state identity and validation evidence, conformer/water-placement coverage, water shifts, sensitivity assessment and final conclusion. For bounded failure, include the attempted state classes, failure diagnostics, validated partial results, coverage and a conclusion limited to what the calculations support.
# Scientific objective

Independently test the authors' qualitative hypothesis that the first reducing hydrogen-equivalent transfer from lowest-singlet photoexcited 9,10-phenanthrenehydroquinone (H₂PQ) to pyridine N-oxide (PyO) can occur by either proton transfer followed by electron transfer or electron transfer followed by proton transfer, and that explicit water can alter ionic-intermediate stability. Compute the first proton-transfer and electron-transfer endpoint free energies, dry and hydrated, then state what is supported without assuming a result.

# Public inputs and scientific boundaries

Use `data/inputs/system.json` for molecular graphs, charges, states and endpoint definitions, and `data/inputs/conditions.json` for equations and reporting conditions. The object is H₂PQ + unsubstituted PyO in acetonitrile, at 298.15 K and 1 M, with two explicit waters total in hydrated comparisons. Score only the first elementary event; rates, the second transfer and full deoxygenation are outside scope.

# Required scientific validation/investigation

Generate independent 3D structures and multiple conformers or encounter/water-placement motifs for each endpoint. Deduplicate by connectivity, proton location, charge/spin state and geometry; retain per-candidate identity and validation evidence. Validate atom mapping, stoichiometry, charge, multiplicity/open-shell coupling, excited-state character and stationary-point or endpoint character. Continue until new chemically distinct starts repeatedly return to represented minima or cannot affect the declared ensemble conclusion; report coverage and any energy window. Completion requires four comparable ΔG values, water-induced shifts, validation evidence, sensitivity or limitation, and a conclusion. Stop at that convergence rule or after repeated chemically distinct failures; report bounded failure and partial results honestly if needed.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with method/reference convention, per-state values, candidate validation records, coverage, water shifts, sensitivity and conclusion; bounded failure must include attempted states, diagnostics, valid partial results and limitations.
