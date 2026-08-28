# Scientific objective

Determine the thermodynamically plausible nature of the first elementary reducing hydrogen-equivalent-transfer event between lowest-singlet photoexcited 9,10-phenanthrenehydroquinone (H₂PQ) and pyridine N-oxide (PyO) in acetonitrile, and determine how the defined explicit-water environment changes the candidate landscape. Independently propose chemically distinct first-event hypotheses, compute comparable solution Gibbs free energies, discriminate the supported explanations, and state the limits of the conclusion.

# Public inputs and scientific boundaries

Use only `data/inputs/system.json` for molecular graphs and the starting/event/hydration boundaries and `data/inputs/conditions.json` for the physical reporting conditions. Report ΔG in kcal/mol at 298.15 K and a 1 M solution convention. The dry and two-water environments must use identical atom and water stoichiometry within each comparison. The scored object ends after the first elementary event; the second hydrogen transfer, product formation, catalytic turnover and kinetic rate prediction are outside scope. No candidate mechanism or preferred result is supplied.

# Required scientific validation/investigation

First enumerate chemically explicit candidate classes that could realize the bounded event, including distinct electron, proton, hydrogen-atom or coupled transfers when chemically definable, plus any other defensible first-event class. Record why each was advanced, merged as duplicate or rejected. For every advanced class, generate and deduplicate conformers, encounter geometries, proton locations, spin couplings and water placements by explicit scientific criteria. Continue candidate generation until new chemically distinct starts repeatedly return to represented endpoints, are invalid under the event boundary, or lie outside a declared energy window that no longer affects the conclusion. Validate connectivity, stoichiometry, charge, multiplicity/open-shell character, electronic/excited-state identity and endpoint/stationary-point character per candidate. Compare all valid candidates on a common free-energy reference in both environments where meaningful, and assess method/solvation sensitivity or identify it as a limitation. Completion requires a documented hypothesis inventory, per-candidate validation, enough search coverage to justify stopping, comparable computed results and a bounded conclusion. Stop under the declared coverage rule or after repeated failures from distinct starts; a bounded-failure submission must preserve attempted hypotheses, diagnostics, validated partial results and the scientific limitation without invented values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. A successful report must contain the method and reference convention, hypothesis inventory, individual candidate records and validation, search coverage, numerical free energies for validated candidates, environment effects, sensitivity analysis, selected explanation and limitations. A bounded-failure report must contain attempted hypotheses, per-attempt diagnostics, any validated partial results, coverage and a conclusion restricted to the evidence obtained.
# Scientific objective

Determine the thermodynamically plausible nature of the first elementary reducing hydrogen-equivalent-transfer event between lowest-singlet photoexcited H₂PQ and PyO in acetonitrile, and how two explicit waters alter the candidate landscape. Independently propose chemically distinct first-event hypotheses, compute comparable solution Gibbs free energies, discriminate supported explanations and state limitations.

# Public inputs and scientific boundaries

Use only `data/inputs/system.json` and `data/inputs/conditions.json`. Report ΔG in kcal/mol at 298.15 K and 1 M. Dry and hydrated environments must preserve identical atom and water stoichiometry within comparisons. The event ends after the first elementary transfer; later transfer, product formation, turnover and rates are outside scope. No mechanism or preferred result is supplied.

# Required scientific validation/investigation

Enumerate explicit candidate classes including electron, proton, hydrogen-atom and coupled transfers where chemically definable, plus any other defensible first-event class. Record advancement, merging and rejection reasons. Generate and deduplicate conformers, encounter geometries, proton locations, spin couplings and water placements. Validate connectivity, stoichiometry, charge, multiplicity/open-shell character, state identity and endpoint/stationary-point character per candidate. Continue until new distinct starts repeatedly return to represented endpoints, are invalid, or lie outside a declared energy window; report coverage. Completion requires a hypothesis inventory, validated candidates, comparable free energies in both environments where meaningful, sensitivity/limitation, and a bounded conclusion. Stop at the coverage rule or repeated failures; preserve diagnostics and partial results without invented values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, containing method/reference, hypothesis inventory, candidate records, validation, coverage, free energies, environment effects, sensitivity, selected explanation and limitations; bounded failure must include attempted hypotheses and diagnostics.
