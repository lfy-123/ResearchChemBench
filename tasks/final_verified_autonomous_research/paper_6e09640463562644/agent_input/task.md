# Scientific objective

Determine how sequential hydration changes the structure and OH-stretching spectrum of neutral open-shell BaOH(H2O)n clusters for n=1–5, and identify the smallest hydration size at which the BaOH contact arrangement is replaced or substantially reorganized by a water-mediated ion-pair structure. Generate and discriminate plausible structural explanations independently; no author route or candidate ranking is supplied.

# Public inputs and scientific boundaries

The system is BaOH(H2O)n with n ∈ {1,2,3,4,5}, total charge 0 and spin multiplicity 2. BaOH oxygen is O(1); each water oxygen is O(2) or higher according to the explicit atom map supplied by the Agent. Public experimental band positions, units and neutral band labels are in `data/inputs/experimental_band_assignments.json`. The physical boundary is isolated neutral clusters in the stated electronic state; do not infer bulk-solution behavior. The measured quantities are candidate relative energies/free energies, harmonic or anharmonic OH frequencies and intensities, Ba···O(1) distance, water coordination/hydrogen-bond topology, and optional charge or interaction descriptors. Choose and report a defensible computational model.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

The band labels a-f are identifiers only, not assignments to an atomic group or shell. The input file retains its legacy filename but contains measured peak positions only. Determine mode identities from computed displacements and spectra; determine any change in ion-pair arrangement by comparing the full n=1-5 series, without assuming its onset.

# Required scientific validation/investigation

For each n, propose at least two chemically distinct structural hypotheses and a finite candidate-generation strategy, retain candidate IDs and atom mappings, and deduplicate by a stated structural criterion. Optimize candidates and validate stationary points with a frequency or equivalent minimum test; report failures rather than silently discarding them. Advance candidates using an explicitly stated stability/spectral criterion and compare the competing hypotheses against the public bands. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` containing candidate structures, hypothesis labels, validation records, per-size observables, spectral assignments, conclusion, and provenance. Include coordinates or unique structure identifiers for every scored candidate. Explain which hypothesis is supported at each n, if any, and separate evidence from interpretation.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
