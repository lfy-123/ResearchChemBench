# Scientific objective

Determine how sequential hydration changes the structure and OH-stretching spectrum of neutral open-shell BaOH(H2O)n clusters for n=1–5, and identify the smallest hydration size at which the BaOH contact arrangement is replaced or substantially reorganized by a water-mediated ion-pair structure. Generate and discriminate plausible structural explanations independently.

# Public inputs and scientific boundaries

The system is BaOH(H2O)n with n ∈ {1,2,3,4,5}, total charge 0 and spin multiplicity 2. BaOH oxygen is O(1); each water oxygen is O(2) or higher according to the explicit atom map supplied by the Agent. Public experimental band positions and assignments are in `data/inputs/experimental_band_assignments.json`. The scored system is the isolated neutral cluster in the stated electronic state; do not add a host or solvent and do not infer bulk-solution behavior. The measured quantities are candidate relative energies/free energies, harmonic or anharmonic OH frequencies and intensities, Ba···O(1) distance, water coordination/hydrogen-bond topology, and optional charge or interaction descriptors. Choose and report a defensible computational model.

# Required scientific validation/investigation

For each n, generate and test at least two chemically distinct structural hypotheses using a finite candidate-generation strategy, retain candidate IDs and atom mappings, and deduplicate by a stated structural criterion. Optimize candidates and validate stationary points with a frequency or equivalent minimum test; report failures rather than silently discarding them. Advance candidates using an explicitly stated stability/spectral criterion and compare the competing hypotheses against the public bands. Completion requires either (a) validated candidates supporting a conclusion, or (b) a bounded-failure report identifying which calculations could not be completed and why. Stop when additional candidate generations no longer produce a distinct validated low-energy structure or materially change the structural/spectral conclusion, or when resources prevent that test; report coverage, stopping rule, and limitations.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`, including the required result keys for this mode. Report candidate structures, validation records, per-size observables, spectral assignments, conclusion, limitations, and provenance; include coordinates or unique structure identifiers for every scored candidate. Explain which hypothesis is supported at each n, if any, and separate evidence from interpretation.
