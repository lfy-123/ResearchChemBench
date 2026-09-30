# Scientific objective

Determine, by an independent computational investigation, the dominant electronic character of the highest-oscillator-strength physical state in the documented low-lying sextet excited-state manifold of the public tetraethylammonium tetrachloroferrate catalyst. Quantify its charge-transfer channels and decide whether the excitation is predominantly ligand-to-metal, metal-to-ligand, ligand-centered, metal-centered, ligand-to-ligand, or mixed. Requested results are state-selection evidence, excitation observables, fragment-resolved percentages, validation/sensitivity evidence, and a calculation-based conclusion. The selection rule defines the measured state, not its unknown electronic character or software state number.

# Public inputs and scientific boundaries

The sole scientific input is `data/inputs/catalyst_system.json`: tetraethylammonium cation `CC[N+](CC)(CC)CC` (charge +1) paired with an FeCl4 anion (Fe bonded to four Cl atoms, charge −1; Fe(III) notation), total charge 0 and spin multiplicity 6. The object is the ion pair in implicit acetonitrile, without explicit solvent molecules or reaction substrates. Generate and document geometry/conformer(s) independently. The endpoint is excited-state electronic structure and IFCT/hole-electron analysis; reaction pathways and synthetic products are out of scope.

# Required scientific validation/investigation

Independently define a reproducible candidate set of geometries and excited states, deduplicate equivalent geometries, and establish sufficient state-space coverage. The primary charge-transfer analysis must use the highest-f selection rule below. States selected for other reasons, such as energetic accessibility, may be examined as auxiliary or sensitivity cases but must not replace that primary state. Optimize or validate the ground-state structure, verify charge/multiplicity and convergence, and compute a state range sufficient to support coverage. Retain a per-state record for every examined state, including identity and excitation observables; for each analyzed state also retain fragment definitions and charge-transfer fractions. Perform at least one sensitivity check on geometry, electronic method, or fragment partition, or document a technically specific reason it was impossible. If the endpoint cannot be reached, use the bounded-failure schema branch with attempted-state and validation context rather than fabricated IFCT values. Do not assume an author mechanism, a particular software state number, or the charge-transfer result.

Use an implicit acetonitrile environment; excluding solvent molecules means no explicit solvent, not gas phase. Examine the low-lying sextet excited-state manifold, report at least the three largest oscillator strengths, and select the largest-f physical state in that manifold for the primary analysis. Resolve near degeneracy/state mixing with reported physical character and coverage, never by closeness to a charge-transfer target or by a fixed software state number. The common primary IFCT convention is a Mulliken-like transition-density decomposition into three disjoint fragments: all four Cl ligands, Fe, and the complete TEA+ cation. LMCT means Cl -> Fe and MLCT Fe -> Cl. Normalize over all fragment-to-fragment channels (including local channels); report the full matrix/normalization in supporting analysis. Other partitions/population schemes are sensitivity only.

Retain and explain signed fragment contributions and any numerical normalization residuals produced by the declared population scheme; do not normalize LMCT and MLCT alone to 100%.

The top-level `state_selection` and `ifct` results must describe the same primary highest-f physical state. Keep analyses of other states in `ifct_records` with their state identities and auxiliary/sensitivity roles explicit; a charge-transfer fraction from another state must not be substituted into the primary summary.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with supporting computational files referenced there. Preserve per-state identity and validation evidence, distinguish completed from failed attempts, and give a conclusion that follows from the submitted data. Do not use the paper/SI or general web as an information source during the investigation.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
