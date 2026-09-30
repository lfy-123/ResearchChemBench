# Scientific objective

Determine, by an independent computational investigation, the dominant electronic character of an excited state of the public tetraethylammonium tetrachloroferrate catalyst. Quantify charge-transfer channels for a defensibly selected low-lying excited state and decide whether the excitation is predominantly ligand-to-metal, metal-to-ligand, ligand-centered, metal-centered, ligand-to-ligand, or mixed. Requested results are state-selection evidence, excitation observables, fragment-resolved percentages, validation/sensitivity evidence, and a bounded conclusion.

# Public inputs and scientific boundaries

The sole scientific input is `data/inputs/catalyst_system.json`: tetraethylammonium cation `CC[N+](CC)(CC)CC` (charge +1) paired with an FeCl4 anion (Fe bonded to four Cl atoms, charge −1; Fe(III) notation), total charge 0 and spin multiplicity 6. The object is the isolated ion pair, excluding solvent and reaction substrates. Generate and document geometry/conformer(s) independently. The endpoint is excited-state electronic structure and IFCT/hole-electron analysis; reaction pathways and synthetic products are out of scope.

# Required scientific validation/investigation

Define a reproducible candidate set of geometries and excited states, deduplicate equivalent geometries, and state the rule used to advance a state to charge-transfer analysis (for example oscillator strength, energetic accessibility, or another justified criterion). Optimize or validate the ground-state structure, verify charge/multiplicity and convergence, and compute a state range sufficient to support coverage. Retain a per-state record for every examined state, including identity and excitation observables; for each analyzed state also retain fragment definitions and charge-transfer fractions. Perform at least one sensitivity check on geometry, electronic method, or fragment partition, or document a technically specific reason it was impossible. Stop when the chosen state(s) are justified by the reported coverage and the sensitivity check is complete. If the endpoint cannot be reached, use the bounded-failure schema branch with attempted-state and validation context rather than fabricated IFCT values. Do not assume any author mechanism or target state.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with supporting computational files referenced there. Preserve per-state identity and validation evidence, distinguish completed from failed attempts, and give a conclusion that follows from the submitted data. Include limitations and the stopping rationale. Do not use the paper/SI or general web as an information source during the investigation.
